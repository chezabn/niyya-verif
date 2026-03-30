# ==================================================================================== #
# VARIABLES
# ==================================================================================== #
# Fichier .env par défaut
ENV_FILE := .env

# ==================================================================================== #
# HELPERS
# ==================================================================================== #
## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ":" | sed -e 's/^/ /'

# ==================================================================================== #
# MIGRATIONS
# ==================================================================================== #

## load-env: Load env file
.PHONY: load-env
load-env:
	set -a; source ${ENV_FILE}; set +a;

## migrations: make migrations
.PHONY: migrations
migrations:
	python manage.py makemigrations

## migrate: migrate
.PHONY: migrate
migrate:
	python manage.py migrate

## db: update database with makemigrations and migrate
.PHONY: db
db:load-env migrations migrate

## shell: Open a Django shell with env loaded
.PHONY: shell
shell:
	python manage.py shell

# ==================================================================================== #
# RUN SERVER
# ==================================================================================== #

## run-server: launch server
.PHONY: run-server
run-server:
	python manage.py runserver 0.0.0.0:5001

# ==================================================================================== #
# TEST
# ==================================================================================== #

## test: test auth app
.PHONY: test-auth
test-auth:
	python manage.py test authentication


## test: test company app
.PHONY: test-comp
test-comp:
	python manage.py test company

## test: test publication app
.PHONY: test-publ
test-publ:
	python manage.py test publication

## test: test all app in project
.PHONY: test
test:
	python manage.py test

# ==================================================================================== #
# FORMAT
# ==================================================================================== #

## black: do black for all project
.PHONY: black
black:
	black .


# ==================================================================================== #
# FREEZE
# ==================================================================================== #

## freeze-dev: Add dependancies to requirements-dev.txt
.PHONY: freeze-dev
freeze-dev:
	pip freeze > requirements-dev.txt

## freeze-prod: Add dependancies to requirements.txt
.PHONY: freeze-prod
freeze-prod:
	pip freeze > requirements.txt
