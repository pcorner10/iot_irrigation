# migrations
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

libraries:
	pip install -r requirements.txt

# Run server
run:
	python manage.py runserver