@echo off
setlocal
title Contract Management System - Launcher
cd /d "%~dp0"

echo ============================================================
echo   Contract Management System - Setup and Launch
echo ============================================================
echo.

REM ---- Check Python is installed ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found on this computer.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo and make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM ---- Create virtual environment if it does not exist ----
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/4] Virtual environment already exists. Skipping creation.
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing/updating dependencies (Flask, OpenCV, Pillow, pandas, openpyxl)...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt

echo [4/4] Starting local server...
echo.
echo The app will open automatically in your default browser at:
echo   http://127.0.0.1:5000
echo.
echo Keep this window OPEN while using the app. Close it to stop the server.
echo ============================================================

REM ---- Open the browser after a short delay, then start Flask ----
start "" cmd /c "timeout /t 2 >nul && start http://127.0.0.1:5000"
python app.py

pause
