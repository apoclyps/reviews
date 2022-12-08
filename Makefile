.PHONY: help build.test build.cli run start debug stop clean logs shell lint test test-shell

GIT_SHA = $(shell git rev-parse HEAD)
DOCKER_REPOTAG = $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_NAME):$(GIT_SHA)

default: help

build: build.cli build.test ## Build the cli and test containers

build.cli: ## Build the cli container
	@docker-compose build cli

build.test: ## Build the test container
	@docker-compose build test

build.lint: ## Build the lint container
	@docker-compose build test

build.all: build.cli build.test build.lint  ## Build all containers

help: ## show this help
	@echo
	@fgrep -h " ## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -Ee 's/([a-z.]*):[^#]*##(.*)/\1##\2/' | column -t -s "##"
	@echo

run: start  ## run the cli locally

start: ## run the cli locally in the background
	@docker-compose up --build cli

stop: ## stop the cli
	@docker-compose down --remove-orphans

clean: ## delete all data from the local databases
	@docker-compose down --remove-orphans --volumes

network: ## Create the reviews network if it doesn't exist
	docker network create --driver bridge reviews || true

shell: ## shell into a development container
	@docker-compose build cli
	@docker-compose run --rm cli sh

test: build.test network ## Run the unit tests and linters
	@docker-compose -f docker-compose.yml run --rm test

test-shell: build.test network ## Run the unit tests and linters
	@docker-compose -f docker-compose.yml run --rm test bash

lint: ## lint and autocorrect the code
	@docker-compose build test
	@docker-compose run --rm --no-deps test isort .
	@docker-compose run --rm --no-deps test black --line-length 119 --check .
	@docker-compose run --rm --no-deps test mypy .
	@docker-compose run --rm --no-deps test flake8 .
	@docker-compose run --rm --no-deps test pylint --rcfile=.pylintrc reviews
	@docker-compose run --rm --no-deps test bandit reviews
	@docker-compose run --rm --no-deps test vulture --min-confidence 90 reviews
	@docker-compose run --rm --no-deps test codespell reviews
	@docker-compose run --rm --no-deps test find . -name '*.py' -exec pyupgrade {} +


install: ## build and install the cli
	sudo pip install -e .
