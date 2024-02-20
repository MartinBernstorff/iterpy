FROM python:3.9

# Set the working directory to /app
WORKDIR /app

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"
RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" RYE_TOOLCHAIN_VERSION=3.9 bash
RUN rye config --set-bool behavior.use-uv=true

COPY Makefile ./
COPY pyproject.toml ./
RUN make install

COPY . /app
RUN make install