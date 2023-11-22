SRC_PATH = functionalpy
MAKEFLAGS = --no-print-directory

install-dev:
	@pip install --upgrade -r dev-requirements.txt

install-deps:
	@pip install --upgrade -r requirements.txt

install:
	@make install-deps
	@make install-dev
	@pip install -e .

# Tasks
generate_coverage:
	@pytest --cov=$(SRC_PATH) $(SRC_PATH) --cov-report xml:.coverage.xml --cov-report lcov:.coverage.lcov

test: ## Run tests
	@echo "––– Testing –––"
	@make generate_coverage
	@diff-cover .coverage.xml --fail-under=80
	@echo "✅✅✅ Tests passed ✅✅✅"

lint: ## Format code
	@echo "––– Linting –––"
	@ruff format . 
	@ruff . --fix \
 		--extend-select F401 \
 		--extend-select F841
	@echo "✅✅✅ Lint ✅✅✅"

types: ## Type-check code
	@echo "––– Type-checking –––"
	@pyright $(SRC_PATH)
	@echo "✅✅✅ Types ✅✅✅"

validate: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
	@make test

validate_ci: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
## CI doesn't support local coverage report, so skipping full tests
	@make generate_coverage 

# PR management
merge-main:
	@echo "––– Merging main –––"
	@git fetch
	@git merge --no-edit origin/main

push:
	@echo "––– Pushing to origin/main –––"
	@git push --set-upstream origin HEAD
	@git push
create-pr:
	@echo "––– Creating PR –––"
	@gh pr create --title "$$(git rev-parse --abbrev-ref HEAD | tr -d '[:digit:]' | tr '-' ' ')" --body "Auto-created" || true

enable-automerge:
	@gh pr merge --auto --merge --delete-branch

pr-status:
	@gh pr view | cat | grep "title" 
	@gh pr view | cat | grep "url" 
	@echo "✅✅✅ PR created ✅✅✅"

################
# Compositions #
################
setup-pr: ## Update everything and setup the PR
	@make merge-main
	@make push
	@make create-pr
 
finalise-pr:
	@make enable-automerge
	@make pr-status
 
pr: ## Run relevant tests before PR
	@make setup-pr
	@make validate
	@make finalise-pr