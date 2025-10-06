from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY no está definida.")
    raise SystemExit(1)

client = OpenAI(api_key=api_key)

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Responde EXACTAMENTE: ok"},
        {"role": "user", "content": "Contesta ahora."}
    ],
    temperature=0.0,
    max_tokens=2
)
print("Respuesta:", resp.choices[0].message.content.strip())