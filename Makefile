SRC_PATH = functionalpy

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

sync-pr:
	git push --set-upstream origin HEAD
	git push

create-pr:
	gh pr create -w || true

merge-pr:
	gh pr merge --auto --merge --delete-branch

pr: ## Run relevant tests before PR
	make sync-pr
	make create-pr
	make validate
	make merge-pr