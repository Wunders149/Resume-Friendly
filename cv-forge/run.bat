@echo off
REM CV Forge - Resume Builder
REM Quick start script for Windows

echo.
echo ======================================
echo   CV Forge - Resume Builder
echo ======================================
echo.

REM Check if venv exists
if exist "venv" (
    echo Virtual environment found. Activating...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Install/Update requirements
echo Installing dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run the app
echo.
echo Starting CV Forge...
echo.
python app.py

pause
