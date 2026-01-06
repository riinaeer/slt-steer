@echo off
setlocal

set "ROOT=%~dp0.."
set "PY=%ROOT%\backend\venv\Scripts\python.exe"
set "WORK=%ROOT%\backend\src"

start "Backend (Uvicorn)" /D "%WORK%" "%PY%" -m uvicorn main:app --reload

endlocal
exit /b 0
