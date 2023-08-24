web: python manage.py migrate && gunicorn HeartReadrSite.wsgi

gunicorn app.wsgi:application -w 2 --timeout 18000