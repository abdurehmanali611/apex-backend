@echo off
REM Run Django migrations using the project venv if present.
REM Usage: double-click or run from BackEnd folder: migrate.bat

cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
  echo Using venv\Scripts\python.exe
  "venv\Scripts\python.exe" manage.py migrate %*
  exit /b %ERRORLEVEL%
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Using Windows Python launcher: py -3
  py -3 manage.py migrate %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Using python from PATH
  python manage.py migrate %*
  exit /b %ERRORLEVEL%
)

echo.
echo No Python found. Install Python 3 from https://www.python.org/downloads/
echo Or create a venv: py -3 -m venv venv
echo Then: venv\Scripts\pip install -r requirements.txt
echo Then run this script again.
exit /b 9009
