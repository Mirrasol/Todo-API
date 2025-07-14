lint:
	uv run ruff check .

install:
	uv sync

dev:
	uv run python manage.py runserver

test:
	uv run python manage.py test tests
