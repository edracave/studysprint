
from app.services.prompts import EXPLAIN_PROMPT
from app.services.llm import chat_completion

async def explain_topic(topic: str, level: str = "intermedio") -> str:
    return await chat_completion(EXPLAIN_PROMPT(topic, level))
