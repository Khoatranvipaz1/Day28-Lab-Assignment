@echo off
REM Lab 28 - Complete Automated Setup & Test Runner
REM Chạy tất cả từ A-Z: venv, dependencies, Docker, tests

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo 🚀 LAB 28 - COMPLETE AUTOMATED RUNNER (with Docker restart)
echo ======================================================================
echo.

REM Step 1: Create venv
echo [1/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ venv created
) else (
    echo ✅ venv already exists
)
echo.

REM Step 2: Activate venv and install dependencies
echo [2/6] Installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Step 3: Check/Restart Docker
echo [3/6] Checking Docker status...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker not responding.
    echo Please manually restart Docker Desktop and press any key to continue...
    pause

    REM Wait for Docker to be ready
    echo Waiting for Docker to start...
    timeout /t 15 /nobreak

    REM Check again
    docker ps >nul 2>&1
    if errorlevel 1 (
        echo ❌ Docker still not responding. Please restart Docker Desktop manually.
        pause
        exit /b 1
    )
) else (
    echo ✅ Docker is responding
)
echo.

REM Step 4: Start services
echo [4/6] Starting Docker services...
docker compose down >nul 2>&1
timeout /t 5 /nobreak
docker compose up -d
echo Waiting 30 seconds for services to initialize...
timeout /t 30 /nobreak
echo ✅ Docker services started
echo.

REM Step 5: Verify all services
echo [5/6] Verifying Docker services...
docker compose ps
echo.

REM Step 6: Run all tests
echo [6/6] Running all tests...
echo ======================================================================
python run_all_tests.py
set TEST_RESULT=!errorlevel!
echo ======================================================================
echo.

if !TEST_RESULT! equ 0 (
    echo ✅ ALL TESTS PASSED!
) else (
    echo ⚠️  Some tests failed. Check output above.
)
echo.
pause
