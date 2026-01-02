@echo off
echo Starting Smart Health Backend...
echo.

echo Starting MongoDB service...
net start MongoDB
if %errorlevel% neq 0 (
    echo MongoDB service failed to start. Please run as Administrator or start MongoDB manually.
    echo.
)

echo Starting Backend Server...
cd smart_health\server
npm run dev

pause