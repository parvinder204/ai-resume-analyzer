.PHONY: install run test lint clean

install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

run:
	streamlit run app.py

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	flake8 src/ tests/ app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage
