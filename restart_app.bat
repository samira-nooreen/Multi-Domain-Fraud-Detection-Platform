@echo off
echo Restarting Flask App...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 /nobreak >nul
start cmd /k "python app.py"
echo Flask app restarted!
