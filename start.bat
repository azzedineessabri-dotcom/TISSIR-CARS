@echo off
echo Demarrage de LocAuto Maroc...
echo.
echo Adresse: http://localhost:5000
echo.
cd /d "%~dp0"
start "" http://localhost:5000
"C:\Users\aessabri\AppData\Local\Programs\Python\Python312\python.exe" -c "import sys; sys.path.insert(0, 'C:/Users/aessabri/car-rental'); from app import app; app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)"
pause
