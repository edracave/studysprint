
def detect_intent(text: str, state: str | None = None) -> str:
    t = (text or "").lower()
    if any(k in t for k in ["plan","calendario","organiza"]):
        return "generate_plan"
    if any(k in t for k in ["explica","no entiendo","resume"]):
        return "explain_topic"
    if any(k in t for k in ["quiz","test","preguntas"]):
        return "quiz_topic"
    if any(k in t for k in ["sprint","pomodoro","25"]):
        return "start_sprint"
    if any(k in t for k in ["reporte","progreso","semana"]):
        return "weekly_report"
    if any(k in t for k in ["premium","pagar","suscribir"]):
        return "upgrade_prompt"
    return "fallback"
