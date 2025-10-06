
from app.services.prompts import QUIZ_PROMPT
from app.services.llm import chat_completion

async def gen_quiz(topic: str) -> str:
    return await chat_completion(QUIZ_PROMPT(topic))

def grade_quiz(user_answers, key):
    total = min(len(user_answers), len(key))
    score = sum(1 for a, k in zip(user_answers, key) if str(a).strip().upper() == str(k).strip().upper())
    return {"score": score, "total": total}
