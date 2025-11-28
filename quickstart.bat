@echo off
REM Quick start script for House Price Predictor

echo.
echo ========================================
echo House Price Predictor - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    exit /b 1
)

echo ✅ Python found

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
)

echo.
echo 🧪 Testing API locally...
python test_api.py
echo.
echo ========================================
echo 🚀 To start the server, run:
echo    python main.py
echo.
echo 📊 Server will be available at:
echo    http://localhost:10000
echo.
echo 🌐 To deploy on Render:
echo    1. Push to GitHub: git push -u origin main
echo    2. Go to https://render.com
echo    3. Connect your GitHub repo
echo    4. Deploy with Start Command:
echo       uvicorn main:app --host=0.0.0.0 --port=10000
echo ========================================
echo.
