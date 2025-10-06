
from datetime import date
from app.services.prompts import PLAN_PROMPT
from app.services.llm import chat_completion

async def generate_plan(ctx: dict) -> str:
    today = date.today()
    deadline = date.fromisoformat(ctx["deadline_date"])
    days = max(1, (deadline - today).days)
    ctx["days_to_exam"] = days
    prompt = PLAN_PROMPT(ctx)
    return await chat_completion(prompt)
