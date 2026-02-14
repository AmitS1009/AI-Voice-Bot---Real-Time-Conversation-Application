@echo off
echo ============================================
echo   AI Voice Bot - Project Setup
echo ============================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it and add your Google API key.
) else (
    echo .env file already exists.
)

echo.
echo [3/4] Setting up Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo [4/4] Setup Complete!
echo.
echo ============================================
echo   Next Steps:
echo ============================================
echo 1. Edit backend\.env and add your Google API key
echo    Get it from: https://aistudio.google.com/apikey
echo.
echo 2. Run the application:
echo    - Backend: run-backend.bat
echo    - Frontend: run-frontend.bat
echo.
echo ============================================
pause
