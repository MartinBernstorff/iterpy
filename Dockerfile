FROM python:3.9

# Set the working directory to /app
WORKDIR /app

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" RYE_TOOLCHAIN="/usr/local/bin/python" bash
RUN rye config --set-bool behavior.use-uv=true
RUN rye config --set-bool behavior.global-python=true
RUN rye config --set default.dependency-operator="~="

COPY Makefile ./
COPY pyproject.toml ./
RUN make install
RUN make types # Type-check to warm the cache

COPY . /app
RUN make quicksync