startOnlineFedora:
    cd /home/archons/vex_tournament
    git stash
    git pull
    pip3 install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate --run-syncdb
    python3 manage.py collectstatic --noinput
    nohup gunicorn vex_tournament.wsgi:application --bind 0.0.0.0:8100
