SRC_PATH = iterpy
MAKEFLAGS = --no-print-directory

# Dependency management
install:
	uv sync

dev:
	uv sync --all-extras

test:
	@uv run pytest --cov=$(SRC_PATH) $(SRC_PATH) --cov-report xml:.coverage.xml --cov-report lcov:.coverage.lcov

test-with-coverage: 
	@echo "––– Testing –––"
	@make test
	@uv run diff-cover .coverage.xml
	@echo "✅✅✅ Tests passed ✅✅✅"

lint: ## Format code
	@echo "––– Linting –––"
	@uv run ruff format .
	@uv run ruff . --fix --unsafe-fixes \
		--extend-select F401 \
		--extend-select F841
	@echo "✅✅✅ Lint ✅✅✅"

types: ## Type-check code
	@echo "––– Type-checking –––"
	@uv run pyright .
	@echo "✅✅✅ Types ✅✅✅"

validate_ci: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
	## CI doesn't support local coverage report, so skipping full test
	@make test

docker_ci: ## Run all checks in docker
	@echo "––– Running all checks in docker –––"
	@docker rm -f iterpy || true
	@docker build -t iterpy:latest -f Dockerfile .
	@docker run iterpy make validate_ci

pr: ## Submit a PR
	@uv run lm sync --squash --automerge