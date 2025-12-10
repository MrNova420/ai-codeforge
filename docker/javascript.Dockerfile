# AI CodeForge - JavaScript/Node.js Execution Environment
# Secure, minimal Docker image for running JavaScript code

FROM node:18-slim

# Install common npm packages globally
RUN npm install -g \
    jest@29.7.0 \
    mocha@10.2.0 \
    express@4.18.0 \
    axios@1.6.0 \
    lodash@4.17.21

# Security: Create non-root user
RUN useradd -m -u 1000 -s /bin/bash runner && \
    mkdir -p /code /tmp && \
    chown -R runner:runner /code /tmp

# Switch to non-root user
USER runner

# Set working directory
WORKDIR /code

# Default command
CMD ["node"]

# Labels
LABEL maintainer="AI CodeForge"
LABEL description="Secure Node.js execution environment"
LABEL version="1.0.0"
