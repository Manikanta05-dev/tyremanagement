@echo off
echo Starting Tire Shop Backend...
cd backend
call venv\Scripts\activate
python init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
