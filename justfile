startOnlineFedora:
    cd /home/archons/vex_tournament
    git stash
    git pull
    ./venv/bin/pip3 install -r requirements.txt
    ./venv/bin/python3 manage.py makemigrations
    ./venv/bin/python3 manage.py migrate --run-syncdb
    ./venv/bin/python3 manage.py collectstatic --noinput
    nohup ./venv/bin/gunicorn vex_tournament.wsgi:application --bind 0.0.0.0:8100
