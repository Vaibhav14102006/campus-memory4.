@echo off
REM Quick Start Script for Campus Memory + ML Integration
REM This script sets up and runs the entire system

echo ================================================================================
echo   Campus Memory + ML Integration - Quick Start
echo ================================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/6] Checking Python dependencies...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing Python packages...
pip install -r requirements.txt --quiet

echo.
echo [2/6] Checking ML models...
if not exist "recommendation_model.pkl" (
    echo [WARNING] ML models not found. Run train_model.py first.
    echo Training models now... (this may take 2-3 minutes)
    python train_model.py
)

echo.
echo [3/6] Creating sample events data...
python event_management.py

echo.
echo [4/6] Checking Next.js dependencies...
cd CampusMemory\CampusMemory

if not exist "node_modules" (
    echo Installing Node.js packages... (this may take 3-5 minutes)
    call npm install
) else (
    echo Node.js packages already installed.
)

cd ..\..

echo.
echo [5/6] Starting Backend Server (API on port 8000)...
start "Campus Memory Backend" cmd /k "uvicorn backend_server:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 8 /nobreak >nul

echo.
echo [6/6] Starting Frontend Server with API Proxy...
start "Campus Memory Frontend" cmd /k "cd CampusMemory\CampusMemory && npm run dev"

echo.
echo ================================================================================
echo   Setup Complete!
echo ================================================================================
echo.
echo   Access Your Application: http://localhost:3000
echo.
echo   Everything runs through port 3000:
echo   - Frontend UI: Available at http://localhost:3000
echo   - Backend API: Proxied through http://localhost:3000/api/*
echo   - Direct Backend: http://localhost:8000 (for development/testing)
echo   - API Docs: http://localhost:8000/docs
echo.
echo   Two new terminal windows have opened:
echo   - Backend Server (Python FastAPI on port 8000)
echo   - Frontend Server (Next.js on port 3000 with API proxy)
echo.
echo   Press Ctrl+C in each window to stop the servers
echo ================================================================================
echo.

pause
