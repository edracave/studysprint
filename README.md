
# StudySprint — MVP (FastAPI + Telegram)

Entrenador de estudio con planificador, sprints (Pomodoro), explicaciones breves y quizzes.
Listo para desplegar en Render/Vercel (server) o en un VPS. Webhook de Telegram incluido.

## 1) Requisitos

- Python 3.10+
- Cuenta en OpenAI (API key)
- Bot de Telegram (token de @BotFather)
- (Opcional) Cuenta Stripe para suscripción Premium

## 2) Configuración

1. Clona el proyecto y crea el entorno:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copia `.env.example` a `.env` y completa variables:
   - `OPENAI_API_KEY`: tu clave de OpenAI
   - `TELEGRAM_BOT_TOKEN`: token del bot
   - `BASE_URL`: URL pública donde corre tu FastAPI (para el webhook)
   - `STRIPE_WEBHOOK_SECRET` y `STRIPE_PRICE_ID` (opcional si activas Premium)
   - `ADMIN_USER_IDS`: lista separada por comas para administración (opcional)

3. Inicializa la base de datos (SQLite):
   ```bash
   python -m app.db_init
   ```

4. Ejecuta en local:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Configura el Webhook de Telegram (sustituye BASE_URL):
   ```bash
   curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook"      -d "url=${BASE_URL}/telegram/webhook"
   ```

6. Prueba en Telegram: envía "plan", "sprint", "explica fotosíntesis", "quiz membranas" al bot.

## 3) Estructura

```
app/
  __init__.py
  main.py            # rutas FastAPI
  config.py          # gestión .env
  models.py          # ORM SQLite
  services/
    planner.py       # planificación y calendario
    prompts.py       # plantillas LLM
    llm.py           # wrapper OpenAI
    quiz.py          # generación/corrección
    explain.py       # explicación breve/extendida
    sprint.py        # lógica Pomodoro
    quota.py         # límites Free/Premium
  telegram/
    webhook.py       # parsing y routing
    intents.py       # detección de intent
  db_init.py         # crea tablas SQLite
static/
  landing.html       # landing mínima
```

## 4) Variables de entorno (.env)

```
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=
BASE_URL=http://localhost:8000
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_ID=
ADMIN_USER_IDS=
```

## 5) Despliegue rápido (Render.com)

- Subir repo a GitHub.
- Nuevo servicio **Web Service** → Python.
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- Variables de entorno según `.env`.
- Configura el webhook con la URL pública resultante.

## 6) Seguridad y cumplimiento

- No permite trampas (cheating) ni subida de exámenes protegidos.
- Antialucinación: si no hay temario, genera esquema genérico y pide confirmación.
- Logs mínimos. No almacenar contenido sensible innecesario.

## 7) Premium (opcional)

- Endpoint Stripe webhook en `/stripe/webhook`.
- `quota.py` aplica límites: Free = 20 msg/día; Premium ≈ 200 msg/día.
- Upsell automático al exceder cuota.

## 8) Roadmap

- Integrar Google Calendar.
- Multi-idioma (EN/PT).
- Panel web con métricas y progreso.
- Sprints por voz (TTS).
