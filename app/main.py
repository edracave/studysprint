from fastapi import FastAPI, HTMLResponse, Request, HTTPException
from .db import engine, Base

app = FastAPI(title="StudySprint", version="0.1.0")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/telegram/webhook")
async def telegram_webhook_proxy(request: Request):
    try:
        from .telegram.webhook import telegram_webhook as impl
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import error in webhook handler: {e!r}")
    return await impl(request)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!doctype html><html lang="es"><head>
      <meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
      <title>StudySprint</title>
      <style>
        body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,'Helvetica Neue',Arial;margin:0;background:#0b1020;color:#eef1f7}
        .wrap{max-width:880px;margin:8vh auto;padding:24px}
        .badge{display:inline-block;padding:6px 10px;border:1px solid #3a4a7a;border-radius:999px;font-size:14px;opacity:.9}
        h1{font-size:42px;line-height:1.15;margin:18px 0 8px} p{font-size:18px;opacity:.92}
        ul{margin-top:12px;line-height:1.9;opacity:.95}
        .cta{margin-top:24px;display:inline-flex;gap:12px}
        .btn{appearance:none;border:none;border-radius:12px;padding:14px 18px;font-weight:600;cursor:pointer;text-decoration:none}
        .primary{background:#5b8cff;color:white}.ghost{background:transparent;border:1px solid #3a4a7a;color:#cdd6f4}
        .foot{margin-top:40px;opacity:.6;font-size:14px}
      </style>
    </head><body>
      <div class="wrap">
        <span class="badge">StudySprint</span>
        <h1>Convierte el estudio en un proceso planificado, medible y motivador.</h1>
        <p>Un asistente que te genera planes de estudio, sprints de enfoque (25/5), explicaciones claras y quizzes con feedback.</p>
        <ul>
          <li><b>Plan de estudio automático</b></li>
          <li><b>Sprints de enfoque (25/5)</b></li>
          <li><b>Explicaciones claras</b></li>
          <li><b>Quizzes con feedback</b></li>
        </ul>
        <div class="cta">
          <a class="btn primary" href="https://t.me/StudySprinthelper_bot" target="_blank" rel="noopener">Pruébalo en Telegram</a>
          <a class="btn ghost" href="/docs">API Docs</a>
        </div>
        <div class="foot">© {year} StudySprint</div>
      </div>
      <script>document.querySelector('.foot').innerHTML="© "+new Date().getFullYear()+" StudySprint";</script>
    </body></html>
    """

