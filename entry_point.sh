sleep 1 # experimental, let other services be READY to listen on ports :)
python manage.py migrate
python manage.py init_admin
python manage.py collectstatic --noinput
uwsgi --ini /uwsgi.ini
