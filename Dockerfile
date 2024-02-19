# Use an official Python runtime as a parent image
FROM python:3.9-bookworm

####################
# Install Graphite #
####################
ENV NVM_DIR=$HOME/.nvm
RUN mkdir -p $NVM_DIR
ENV NODE_VERSION=18.2.0

# Install nvm with node and npm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH=$NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN npm install -g @withgraphite/graphite-cli@stable

################
# Install deps #
################
COPY pyproject.toml ./

# Install the entire app
COPY . /app
