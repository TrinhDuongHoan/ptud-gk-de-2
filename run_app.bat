@echo off
set VENV_NAME=duonghoan


if not exist %VENV_NAME% (
    echo create virtual environment...
    python -m venv %VENV_NAME%
)

echo activate virtual environment...
call %VENV_NAME%\Scripts\activate

echo Upgrade pip...
python -m pip install --upgrade pip

if exist requirements.txt (
    echo Install library in requirements.txt...
    pip install -r requirements.txt
) else (
    echo No such file requirements.txt!
    pause
    exit
)

echo Apply migrations...
python manage.py makemigrations
python manage.py migrate

echo Run server Django...
python manage.py runserver

echo ===========================================
echo Django server stopped!
echo Press any to exit...
echo ===========================================
pause
