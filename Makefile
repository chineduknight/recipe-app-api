start:
	docker-compose up

lint:
	docker-compose run --rm app sh -c "black ."

test:
	docker-compose run --rm app sh -c "python manage.py test && flake8"

restart:
	docker-compose down && docker-compose up

migrate:
	docker-compose run --rm app sh -c "python manage.py makemigrations && python manage.py wait_for_db && python manage.py migrate"