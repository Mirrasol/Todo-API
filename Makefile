lint:
	uv run ruff check .

install:
	uv sync

dev:
	uv run python manage.py runserver

run:
	uv run python -m gunicorn todo.asgi:application -k uvicorn_worker.UvicornWorker

test:
	uv run python manage.py test tests
