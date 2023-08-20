
test-unit:
	python -m pytest -m "unit" --cov-report term-missing --cov-fail-under=60
	coverage-badge -o coverage.svg -f
