FROM python:3.10-bullseye

# Set the working directory to /app
WORKDIR /app

# Dev experience
COPY Makefile ./
COPY dev-requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip make install-dev 
RUN pyright .

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip make install-deps

COPY pyproject.toml ./
COPY . /app
RUN pip install .
RUN git init