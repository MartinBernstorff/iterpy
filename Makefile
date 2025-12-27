# This project uses mise for dependency and environment management, particularly to enable parallel execution in CI environments.

docker_ci: ## Run all checks in docker
	@echo "––– Running all checks in docker –––"
	@docker rm -f iterpy || true
	@docker build -t iterpy:latest -f Dockerfile .