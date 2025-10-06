
from app.config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_completion_sync(prompt: str, system: str = "Eres StudySprint, conciso y pedagógico.") -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=900
    )
    return resp.choices[0].message.content.strip()

async def chat_completion(prompt: str, system: str = "Eres StudySprint, conciso y pedagógico.") -> str:
    # Para simplicidad, uso la versión síncrona dentro de la async (en producción: ejecutor).
    return chat_completion_sync(prompt, system)
