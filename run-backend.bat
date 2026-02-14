@echo off
echo ============================================
echo   Starting Backend Server
echo ============================================
cd backend
call venv\Scripts\activate.bat
python main.py
