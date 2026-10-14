# QE API Testing Lab

A demonstration Quality Engineering (QE) REST API testing lab built with Python, FastAPI, and pytest.

## Features
- FastAPI property-management REST API with bearer token authentication
- Automated pytest suite with regression coverage
- GitHub Actions CI workflow for continuous testing

## Setup & Running Tests
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export QE_API_TOKEN="local-test-token"
python -m pytest -v
