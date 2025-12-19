SRC_PATH = iterpy
MAKEFLAGS = --no-print-directory

# Dependency management
install:
	uv sync

dev:
	uv sync --all-extras

test:
	@uv run pytest

lint: ## Format code
	@echo "––– Linting –––"
	@uv run ruff format .
	@uv run ruff . --fix --unsafe-fixes \
		--extend-select F401 \
		--extend-select F841
	@echo "✅✅✅ Lint ✅✅✅"

types: ## Type-check code
	@echo "––– Type-checking –––"
	@uv run ty check .
	@uv run pyright .
	@echo "✅✅✅ Types ✅✅✅"

validate_ci: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
	@make test

docker_ci: ## Run all checks in docker
	@echo "––– Running all checks in docker –––"
	@docker rm -f iterpy || true
	@docker build -t iterpy:latest -f Dockerfile .
	@docker run iterpy make validate_ci

pr: ## Submit a PR
	@uv run lm sync --squash --automerge