redis: redis-server
worker: celery -A pia.application.celery worker --loglevel=info
web: gunicorn pia.application:app -w 2 --error-log -
