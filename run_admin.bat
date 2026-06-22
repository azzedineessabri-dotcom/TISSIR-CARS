@echo off
cd /d "%~dp0"
echo Stopping any previous instance...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
echo Starting LocAuto Maroc - Admin Panel
echo.
echo Public site:  http://localhost:5000
echo Admin panel:  http://localhost:5000/admin/login
echo Identifiants: admin / admin123
echo.
start "" "C:\Users\aessabri\AppData\Local\Programs\Python\Python312\python.exe" -c "import sys; sys.path.insert(0, 'C:/Users/aessabri/car-rental'); from app import app; app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)"
timeout /t 3 /nobreak >nul
start "" http://localhost:5000
echo.
echo Server running. Close this window to stop.
pause
