
from fastapi import APIRouter
from app.config import TELEGRAM_BOT_TOKEN
from app.telegram.intents import detect_intent
from app.models import SessionLocal, User, Plan
from sqlalchemy import select
from app.services.planner import generate_plan
from app.services.explain import explain_topic
from app.services.quiz import gen_quiz
from app.services.sprint import Pomodoro
from app.services.quota import check_and_decrement_quota
import httpx

router = APIRouter()

async def send_message(chat_id: int, text: str, parse_mode: str | None = "Markdown"):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=20.0
        )

@router.post("/telegram/webhook")
async def telegram_webhook(update: dict):
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    async with SessionLocal() as session:
        tg_user_id = str(message.get("from", {}).get("id"))
        res = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
        user = res.scalar_one_or_none()
        if not user:
            user = User(tg_user_id=tg_user_id)
            session.add(user)
            await session.commit()
            await send_message(chat_id, "Hola 👋 Soy StudySprint. Di 'plan' para crear tu plan de estudio.")
            return {"ok": True}

        ok = await check_and_decrement_quota(user, session)
        if not ok:
            await session.commit()
            await send_message(chat_id, "Has alcanzado tu límite diario. Desbloquea Premium (9 €/mes) para uso ampliado.")
            return {"ok": True}

        intent = detect_intent(text)

        if intent == "generate_plan":
            parts = text.split("|")
            # Uso rápido: "plan|OPE Digestivo|2025-11-15|2|24|media"
            if len(parts) < 6:
                await send_message(chat_id, "Formato rápido: plan|EXAMEN|YYYY-MM-DD|HORAS_DIA|TOTAL_TEMAS|dificultad(facil/media/dificil)")
            else:
                _, exam, deadline, hours, topics, diff = parts[:6]
                ctx = {
                    "exam_name": exam.strip(),
                    "deadline_date": deadline.strip(),
                    "daily_hours": float(hours),
                    "topics_total": int(topics),
                    "difficulty_self": diff.strip()
                }
                plan_text = await generate_plan(ctx)
                plan = Plan(
                    user_id=user.id,
                    exam_name=ctx["exam_name"],
                    deadline_date=ctx["deadline_date"],
                    daily_hours=ctx["daily_hours"],
                    topics_total=ctx["topics_total"],
                    difficulty_self=ctx["difficulty_self"],
                    topics_plan={"raw": plan_text}
                )
                session.add(plan)
                await session.commit()
                await send_message(chat_id, plan_text[:3900])
                if len(plan_text) > 3900:
                    await send_message(chat_id, plan_text[3900:7800])
            await session.commit()
            return {"ok": True}

        if intent == "explain_topic":
            topic = text.replace("explica", "").replace("resume", "").strip() or "tema genérico"
            out = await explain_topic(topic, level="intermedio")
            await send_message(chat_id, out[:3900])
            await session.commit()
            return {"ok": True}

        if intent == "quiz_topic":
            topic = text.replace("quiz", "").replace("test", "").strip() or "tema genérico"
            out = await gen_quiz(topic)
            await send_message(chat_id, out[:3900])
            await session.commit()
            return {"ok": True}

        if intent == "start_sprint":
            topic = text.replace("sprint", "").replace("pomodoro", "").strip() or "tu tema de hoy"
            pomo = Pomodoro()
            await pomo.run(lambda msg: send_message(chat_id, msg), topic)
            await session.commit()
            return {"ok": True}

        await send_message(chat_id, "Opciones: 'plan|EXAMEN|YYYY-MM-DD|HORAS|TEMAS|media', 'explica [tema]', 'quiz [tema]', 'sprint [tema]'.")
        await session.commit()
        return {"ok": True}
