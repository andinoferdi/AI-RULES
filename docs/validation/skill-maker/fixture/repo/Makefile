.PHONY: test lint migrate-check

test:
	python -m pytest -q

lint:
	ruff check .
	ruff format --check .

migrate-check:
	python scripts/migrate_check.py
