@echo off
call .venv\Scripts\activate.bat
python -m uvicorn backend.main:app --reload --port 8000
pause
