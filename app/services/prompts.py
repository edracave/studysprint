
def PLAN_PROMPT(ctx: dict) -> str:
    return f"""Eres StudySprint, entrenador académico.
Organiza un plan para el examen "{ctx['exam_name']}".
Días hasta examen: {ctx['days_to_exam']}. Horas/día: {ctx['daily_hours']}.
Dificultad: {ctx['difficulty_self']}. Total de temas: {ctx['topics_total']}.
Etiquetas de temas (si existen): {ctx.get('topics_labels')}.

Tarea:
1) Divide el temario en objetivos diarios realistas hasta la fecha límite.
2) Cada día: lista de objetivos (tema + subtemas), tiempo estimado y 1 tarea de consolidación.
3) Recomendaciones semanales.
Formato por semanas y días con fecha (YYYY-MM-DD). Cierra con 3 reglas de oro y 3 riesgos/mitigaciones.
No inventes temario específico si no hay etiquetas; usa bloques genéricos (Fundamentos/Intermedio/Avanzado) y pide confirmación.
"""

def EXPLAIN_PROMPT(topic: str, level: str) -> str:
    return f"""Explica el tema: {topic}
Nivel: {level}.
Formato: definición clara (<=3 líneas), 3 ideas clave, 1 ejemplo práctico,
errores frecuentes y mini-check (2 preguntas).
Sé conciso y pedagógico.
"""

def QUIZ_PROMPT(topic: str) -> str:
    return f"""Genera 4 preguntas tipo test sobre: {topic}.
Cada pregunta con 4 opciones (A-D), una sola correcta. Devuelve también el gabarito al final.
"""
