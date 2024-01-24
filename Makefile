run:
	python3 main.py

lint:
	docker-compose run --rm app sh -c "black ."

test:
	docker-compose run --rm app sh -c "python manage.py test && flake8"

restart:
	docker-compose down && docker-compose up