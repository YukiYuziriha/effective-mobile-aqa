.PHONY: install test clean docker-build docker-run

VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
PLAYWRIGHT = $(VENV_DIR)/bin/playwright

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install chromium

test:
	$(PYTEST)

test-allure:
	$(PYTEST) --alluredir=allure-results
	@echo "To view report: allure serve allure-results"

clean:
	rm -rf $(VENV_DIR) allure-results .pytest_cache

docker-build:
	docker build -t effective-mobile-tests .

docker-run:
	docker run --rm effective-mobile-tests
