FROM python:3.9

WORKDIR /code
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py migrate && python manage.py init_admin && python manage.py full_db && python manage.py collectstatic --no-input && gunicorn backend.wsgi:application --bind 0.0.0.0:8000
