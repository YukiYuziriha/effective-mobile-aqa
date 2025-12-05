# Effective Mobile QA Automation

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
   git clone <repository_url>
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
