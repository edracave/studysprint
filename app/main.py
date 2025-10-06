
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.telegram.webhook import router as tg_router
from app.config import STRIPE_WEBHOOK_SECRET
import stripe

app = FastAPI(title="StudySprint MVP")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/landing.html", "r", encoding="utf-8") as f:
        return f.read()

app.include_router(tg_router)

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    if not STRIPE_WEBHOOK_SECRET:
        return JSONResponse({"status": "ignored (no secret configured)"})
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig, secret=STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    # TODO: manejar eventos y marcar premium
    return {"received": True}
