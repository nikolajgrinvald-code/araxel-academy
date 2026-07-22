@echo off
echo Creating local users migration...
call C:\Users\nikol\.venv\Scripts\activate.bat
set DATABASE_URL=
python manage.py makemigrations users
echo.
echo Now apply migrations to PostgreSQL:
echo set DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DB
echo python manage.py migrate
echo python manage.py createsuperuser
echo python manage.py collectstatic --noinput
pause
