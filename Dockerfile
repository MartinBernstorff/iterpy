FROM ghcr.io/astral-sh/uv:python3.9-bookworm

# Set the working directory to /app
WORKDIR /app

# Install mise
RUN curl https://mise.run | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY . /app
RUN mise trust
RUN mise install
RUN mise validate
