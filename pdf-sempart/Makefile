setup:
	pip install -e .[dev]
lint:
	ruff check src tests
test:
	pytest -q
run-demo:
	python -m pdf_sempart.cli.sempart --in examples/demo_input.json --out examples/demo_docmap.json --config config/defaults.yaml
