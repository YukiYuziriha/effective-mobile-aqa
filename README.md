# Effective Mobile QA Automation

## 🛡️ Engineering Standards

This project demonstrates a **zero-compromise approach** to code quality and reliability. It is engineered to meet strict production-grade standards, ensuring that the test suite is as robust and maintainable as the software it tests.

- **Strict Static Analysis:** The codebase is 100% compliant with `mypy --strict`. We enforce explicit type hints for all functions, fixtures, and Page Objects, banning implicit `Any` and untyped definitions.
- **Comprehensive Linting:** Powered by `ruff`, we enforce a rigorous ruleset (including `flake8-bugbear`, `pylint`, `pyupgrade`, and `isort`) to guarantee idiomatic, modern, and efficient Python 3.10+ code.
- **Automated Governance:** Quality gates are enforced via `pre-commit` hooks, preventing unverified code from entering the repository.

This repository contains UI automation tests for the main page of [effective-mobile.ru](https://effective-mobile.ru), implemented using Python, Playwright, and Allure.

## Project Description

The project uses the **Page Object Model (POM)** pattern to ensure maintainability and readability. Tests cover navigation through the main blocks of the site (About, Contacts, Services, etc.).

## Local Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone [<repository_url>](https://github.com/YukiYuziriha/effective-mobile-aqa)
   cd effective-mobile-aqa
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/MacOS
   # venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

5. (Optional) Install developer tools (Linter, Type Checker):
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

## Running Tests Locally

To run the tests using pytest:

```bash
pytest
```

To run tests and generate Allure results:

```bash
pytest --alluredir=allure-results
```

## Running via Docker

1. Build the Docker image:
   ```bash
   docker build -t effective-mobile-tests .
   ```

2. Run the tests in a container:
   ```bash
   docker run --rm effective-mobile-tests
   ```

## Viewing Allure Report

To view the report locally (requires Allure commandline tool):

```bash
allure serve allure-results
```
