
import asyncio

class Pomodoro:
    def __init__(self, work_min=25, break_min=5):
        self.work_min = work_min
        self.break_min = break_min

    async def run(self, send_func, topic: str):
        await send_func("⏱️ Sprint de {} min sobre: *{}*. ¡Empieza ya!".format(self.work_min, topic))
        # Para demo, reducimos los tiempos; en producción usa work_min*60
        await asyncio.sleep(1)
        await send_func("🔔 Fin del bloque. Descanso {} min.".format(self.break_min))
        await asyncio.sleep(1)
        await send_func("✅ Descanso terminado. ¿Otro bloque?")
