@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
TITLE StudySprint - Iniciar (Windows)

cd /d "%~dp0"

echo === StudySprint - Inicio automatizado ===

if not exist ".venv" (
    echo [1/6] Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo Error creando el entorno virtual. Revisa que Python 3.10+ este en PATH.
        pause
        exit /b 1
    )
) else (
    echo [1/6] Entorno virtual detectado.
)

echo [2/6] Activando entorno...
call .\.venv\Scripts\activate
if errorlevel 1 (
    echo No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

echo [3/6] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error instalando dependencias.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [4/6] Creando archivo .env desde .env.example...
    copy /Y .env.example .env >nul
    echo -> Edita .env con tu OPENAI_API_KEY y TELEGRAM_BOT_TOKEN si aun no lo hiciste.
)

echo [5/6] Inicializando base de datos...
python -m app.db_init
if errorlevel 1 (
    echo Error inicializando la base de datos.
    pause
    exit /b 1
)

echo [6/6] Lanzando servidor en http://localhost:8000 ...
start "" http://localhost:8000
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo Servidor detenido.
pause
