@echo off
echo.
echo ========================================
echo   SEEDING DATABASE WITH DUMMY DATA
echo ========================================
echo.

cd backend
call .venv\Scripts\activate
python seed_data.py

echo.
echo ========================================
echo   SEEDING COMPLETE!
echo ========================================
echo.
echo Press any key to exit...
pause > nul
