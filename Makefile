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
	docker compose up airflow-init && docker compose up --build -d

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

.PHONY: requirements
## install development requirements
requirements:
	@python -m pip install -U -r requirements.txt
  