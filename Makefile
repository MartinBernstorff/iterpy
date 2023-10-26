SRC_PATH = FunctionalPython

install-dev:
	pip install -r dev-requirements.txt

install-deps:
	pip install -r requirements.txt

install:
	make install-deps
	make install-dev
	pip install -e .

test: ## Run tests
	pytest $(SRC_PATH)

lint: ## Format code
	ruff check . --fix
	ruff format . 

type-check: ## Type-check code
	pyright $(SRC_PATH)

validate: ## Run all checks
	make lint
	make type-check
	make test

create-and-merge-pr:
	gh pr create -w || true
	gh pr merge --auto --merge --delete-branch

pr: ## Run relevant tests before PR
	make create-and-merge-pr
	make validate