@echo off
echo ========================================
echo Tire Shop Management System
echo Setup Verification Script
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    goto :error
) else (
    python --version
    echo [OK] Python is installed
)
echo.

echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16 or higher
    goto :error
) else (
    node --version
    echo [OK] Node.js is installed
)
echo.

echo [3/5] Checking PostgreSQL installation...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] PostgreSQL command line tools not found
    echo Make sure PostgreSQL is installed and running
) else (
    psql --version
    echo [OK] PostgreSQL is installed
)
echo.

echo [4/5] Checking backend files...
if exist "backend\requirements.txt" (
    echo [OK] Backend files found
) else (
    echo [ERROR] Backend files not found
    goto :error
)
echo.

echo [5/5] Checking frontend files...
if exist "frontend\package.json" (
    echo [OK] Frontend files found
) else (
    echo [ERROR] Frontend files not found
    goto :error
)
echo.

echo ========================================
echo Verification Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Create PostgreSQL database: tire_shop_db
echo 2. Update backend\.env with your database password
echo 3. Run: start-backend.bat
echo 4. Run: start-frontend.bat (in new terminal)
echo 5. Open: http://localhost:3000
echo.
echo For detailed instructions, see QUICK_START.md
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo Verification Failed!
echo ========================================
echo Please fix the errors above and try again.
echo See SETUP.md for detailed instructions.
echo.
pause
exit /b 1
