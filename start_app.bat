@echo off
echo Starting MDFDP Flask Application...
echo.
echo Please wait while the server starts...
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat
python app.py

pause
