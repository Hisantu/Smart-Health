@echo off
echo ========================================
echo Smart Health Selenium Test Automation
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting automated tests...
echo Make sure both servers are running:
echo - Backend: http://localhost:4000
echo - Frontend: http://localhost:5173
echo.

pause

python test_automation.py

pause