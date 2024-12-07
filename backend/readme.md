pip install -r requirements.txt

python manage.py makemigrations livetracking
python manage.py makemigrations maintenance
python manage.py makemigrations scheduling

python manage.py migrate

python manage.py runserver