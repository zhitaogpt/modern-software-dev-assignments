.PHONY: run test format lint seed web-install web-dev web-build

run:
	PYTHONPATH=. uvicorn backend.app.main:app --reload --host $${HOST:-127.0.0.1} --port $${PORT:-8000}

test:
	PYTHONPATH=. pytest -q backend/tests

format:
	black .
	ruff check . --fix

lint:
	ruff check .

seed:
	PYTHONPATH=. python -c "from backend.app.db import apply_seed_if_needed; apply_seed_if_needed()"

web-install:
	cd frontend-react && npm install

web-dev:
	cd frontend-react && npm run dev

web-build:
	cd frontend-react && npm run build
