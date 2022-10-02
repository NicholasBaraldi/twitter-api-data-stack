help:
	@echo 'Makefile for managing web application                              '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo ' make build            build images                                '
	@echo ' make up               creates containers and starts service       '
	@echo ' make start            starts service containers                   '
	@echo ' make stop             stops service containers                    '
	@echo ' make down             stops service and removes containers        '
	@echo '                                                                   '
	@echo ' make migration        create migration m="message"                '
	@echo ' make migrate-up       run all migration                           '
	@echo ' make migrate-dow      roll back last migration                    '
	@echo ' make test             run tests                                   '
	@echo ' make test-cov         run tests with coverage.py                  '
	@echo ' make test-fast        run tests without migrations                '
	@echo ' make lint             run flake8 linter                           '
	@echo '                                                                   '
	@echo ' make attach           attach to process inside service            '
	@echo ' make logs             see container logs                          '
	@echo ' make shell            connect to api container in new bash shell  '
	@echo ' make shell-ipython    connect to api container in new bash shell  '
	@echo ' make shell-db         shell into psql inside database container   '
	@echo ' make view-dash        view task queue dashboardd                  '
	@echo '                                                                   '

up:
	docker compose up -d

down:
	docker compose down

sh:
	docker exec -ti webserver bash

pytest:
	docker exec -ti webserver pytest -p no:warnings -v /opt/airflow/test

format:
	docker exec -ti webserver python -m black -S --line-length 79 .

isort:
	docker exec -ti webserver isort .

type:
	docker exec -ti webserver mypy --ignore-missing-imports /opt/airflow

lint: 
	docker exec -ti webserver flake8 /opt/airflow/dags

ci: isort format type lint pytest

.PHONY: requirements-dev
## install development requirements
requirements-dev:
	@python -m pip install -U -r requirements.dev.txt

.PHONY: requirements-minimum
## install prod requirements
requirements-minimum:
	@python -m pip install -U -r requirements.txt

.PHONY: requirements
## install requirements
requirements: requirements-dev requirements-minimum

.PHONY: style-check
## run code style checks with black
style-check:
	@echo ""
	@echo "Code Style"
	@echo "=========="
	@echo ""
	@python -m black --check --exclude="build/|buck-out/|dist/|_build/|pip/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" . && echo "\n\nSuccess" || (echo "\n\nFailure\n\nRun \"make black\" to apply style formatting to your code"; exit 1)

.PHONY: quality-check
## run code quality checks with flake8
quality-check:
	@echo ""
	@echo "Flake 8"
	@echo "======="
	@echo ""
	@python -m flake8 && echo "Success"
	@echo ""

.PHONY: type-check
## run code type checks with mypy
type-check:
	@echo ""
	@echo "Mypy"
	@echo "======="
	@echo ""
	@python -m mypy --install-types --non-interactive recommendation_app && echo "Success"
	@echo ""

.PHONY: checks
## run all code checks
checks: style-check quality-check type-check

.PHONY: apply-style
## fix stylistic errors with black and isort
apply-style:
	@python -m black --exclude="build/|buck-out/|dist/|_build/|pip/|\\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" .
  
.PHONY: tests
## run unit tests with coverage report
tests:
	@echo ""
	@echo "Unit Tests"
	@echo "=========="
	@echo ""
	@python -m pytest --cov-config=.coveragerc --cov=serasa_twitter/clients --cov-report term --cov-report html:htmlcov --cov-report xml:coverage.xml --cov-fail-under=75 tests