@echo off
title Employee Tracker

echo.
echo  ========================================
echo   DOSYE SOTRUDNIKA - Employee Tracker
echo  ========================================
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo [OSHIBKA] Python ne najden. Ustanovite Python 3.10+
    pause
    exit /b 1
)

if not exist "venv" (
    echo [1/3] Sozdayom virtual'noe okruzhenie...
    python -m venv venv
    if errorlevel 1 (
        echo [OSHIBKA] Ne udalos' sozdat' venv
        pause
        exit /b 1
    )
)

echo [2/3] Ustanavlivayom zavisimosti...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [OSHIBKA] Ne udalos' aktivirovat' venv
    pause
    exit /b 1
)

pip install -r requirements.txt -q
if errorlevel 1 (
    echo [OSHIBKA] Oshibka ustanovki zavisimostej
    pause
    exit /b 1
)

echo.
echo  Nastrojki PostgreSQL (Enter = znachenie po umolchaniyu):
echo.

set DB_USER=postgres
set /p DB_USER="  User [postgres]: "

set DB_PASS=password
set /p DB_PASS="  Password: "

set DB_HOST=localhost
set /p DB_HOST="  Host [localhost]: "

set DB_PORT=5432
set /p DB_PORT="  Port [5432]: "

set DB_NAME=employee_tracker
set /p DB_NAME="  Database [employee_tracker]: "

set DATABASE_URL=postgresql+psycopg://%DB_USER%:%DB_PASS%@%DB_HOST%:%DB_PORT%/%DB_NAME%

echo.
echo [3/3] Zapuskaem prilozhenie...
echo.
echo  http://localhost:5000
echo  http://%COMPUTERNAME%:5000
echo.
echo  Ctrl+C dlya ostanovki
echo  ----------------------------------------
echo.

python app.py
pause
