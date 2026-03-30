# ==================================================================================== #
# VARIABLES
# ==================================================================================== #
# Fichier .env par défaut
ENV_FILE := .env

# Test folder
TEST_FOLDER := ./tests

# ==================================================================================== #
# HELPERS
# ==================================================================================== #
## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ":" | sed -e 's/^/ /'

# ==================================================================================== #
# TEST
# ==================================================================================== #

## test: test all app in project
.PHONY: test
test:
	pytest ${TEST_FOLDER}/libs/*

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
