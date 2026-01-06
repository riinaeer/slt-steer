@echo off
setlocal

cd /d %~dp0\..

cd backend

if not exist venv\Scripts\python.exe (
  python -m venv venv
)

call venv\Scripts\activate.bat

python -m pip install --upgrade pip

echo Installing backend dependencies from requirements.lock...
python -m pip install -r requirements.lock

REM Optional setup scripts
if exist src\setup_env.py (
  python src\setup_env.py
)

if exist src\setup\setup_env.py (
  python src\setup\setup_env.py
)

cd ..\frontend
npm install

cd ..
echo Install complete.
endlocal
