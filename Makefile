SRC_PATH = iterpy
MAKEFLAGS = --no-print-directory

# Dependency management
install:
	rye sync --features=dev

test:
	@rye run pytest --cov=$(SRC_PATH) $(SRC_PATH) --cov-report xml:.coverage.xml --cov-report lcov:.coverage.lcov

test-with-coverage: ## Run tests
	@echo "––– Testing –––"
	@rye run diff-cover .coverage.xml --fail-under=80
	@echo "✅✅✅ Tests passed ✅✅✅"

lint: ## Format code
	@echo "––– Linting –––"
	@rye run ruff format .
	@rye run ruff . --fix \
		--extend-select F401 \
		--extend-select F841
	@echo "✅✅✅ Lint ✅✅✅"

types: ## Type-check code
	@echo "––– Type-checking –––"
	@rye run pyright $(SRC_PATH)
	@echo "✅✅✅ Types ✅✅✅"

validate_ci: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
	## CI doesn't support local coverage report, so skipping full tests
	@make test
