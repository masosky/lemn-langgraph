USING_UV := $(shell command -v uv >/dev/null 2>&1 && echo 1 || echo 0)

ifeq ($(USING_UV),1)
UVICORN := uv run uvicorn
ALEMBIC := uv run alembic
PYTHON := uv run python
PYTEST := uv run pytest
else
UVICORN := uvicorn
ALEMBIC := alembic
PYTHON := python
PYTEST := pytest
endif

run:
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	$(ALEMBIC) upgrade head

seed:
	$(PYTHON) -m app.routes.seed

test:
	$(PYTEST) -q
