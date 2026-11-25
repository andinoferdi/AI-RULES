.PHONY: test lint fmt dbt-build

test:
	pytest -q tests

lint:
	ruff check tidewater tests

fmt:
	ruff format tidewater tests

dbt-build:
	dbt build --project-dir models --target $${TARGET:-dev}
