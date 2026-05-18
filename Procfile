web: gunicorn talamkopo.wsgi --log-file -
release: python3 manage.py makemigrations && python3 manage.py migrate && python3 seed_data.py
