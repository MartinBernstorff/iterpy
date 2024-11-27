FROM ghcr.io/astral-sh/uv:python3.9-bookworm

# Set the working directory to /app
WORKDIR /app

COPY Makefile ./
COPY pyproject.toml ./
RUN make dev
RUN make types # Type-check to warm the cache

COPY . /app
RUN make dev
RUN make validate_ci