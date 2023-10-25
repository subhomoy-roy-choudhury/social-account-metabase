#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$MODE" = "server" ]
then 
  python manage.py flush --no-input
  python manage.py migrate
  python manage.py collectstatic --no-input --clear
  gunicorn main.wsgi:application --bind 0.0.0.0:8000
elif [ "$MODE" = "celery_beat" ]
then
  celery -A main beat -l info --logfile=celery.beat.log
elif [ "$MODE" = "celery_worker" ]
then
  celery -A main worker -l info --logfile=celery.log
fi

exec "$@"