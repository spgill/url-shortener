FROM python:3-slim-bullseye
SHELL ["/bin/bash", "-c"]

# Copy over source code
COPY . /tmp/src/
WORKDIR /tmp/src/

# Install necessary tools
RUN apt update && \
    apt -y install --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# Install UI deps and build the UI
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash && \
    source ~/.bashrc && \
    nvm install && \
    npm install && \
    npm run build && \
    rm -rf ./node_modules && \
    rm -rf ~/.nvm

# Install python runtime dependencies
RUN python -m pip install -r requirements.txt

EXPOSE 5000/tcp
ENTRYPOINT [ "./docker-entrypoint.sh" ]
