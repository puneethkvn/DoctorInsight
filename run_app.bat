@echo off
title DoctorInsight - Medical Document Intelligence
echo ==============================================================
echo    DoctorInsight - Medical Document Intelligence
echo ==============================================================
echo.
echo Starting application on http://localhost:5173/login ...
start http://localhost:5173/login
python -m uvicorn app:app --host 127.0.0.1 --port 5173 --reload
pause
