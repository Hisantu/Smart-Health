@echo off
echo ========================================
echo Smart Health Queue Management System
echo ========================================
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd smart_health\server && npm run dev"
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Application...
start "Frontend App" cmd /k "cd smart_health\web && npm run dev"
echo.
echo ========================================
echo Application is starting...
echo Backend: http://localhost:4000
echo Frontend: http://localhost:5173
echo Display Board: http://localhost:5173/display
echo ========================================
echo.
echo Login Credentials:
echo Admin: admin / admin123
echo Receptionist: receptionist / recep123
echo ========================================
pause
