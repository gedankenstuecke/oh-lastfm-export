release: python manage.py migrate
web: gunicorn myapi.wsgi:application --log-file -
worker: celery -A main worker --concurrency 1
