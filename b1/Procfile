redis: redis-server
worker: celery -A bamboo.application.celery worker --loglevel=info
web: gunicorn bamboo.application:app -w 2 --error-log -
