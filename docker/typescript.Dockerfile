# AI CodeForge - TypeScript Execution Environment
# Secure, minimal Docker image for running TypeScript code

FROM node:18-slim

# Install TypeScript and common packages
RUN npm install -g \
    typescript@5.3.0 \
    ts-node@10.9.0 \
    @types/node@20.10.0 \
    jest@29.7.0 \
    @types/jest@29.5.0

# Security: Create non-root user
RUN useradd -m -u 1000 -s /bin/bash runner && \
    mkdir -p /code /tmp && \
    chown -R runner:runner /code /tmp

# Switch to non-root user
USER runner

# Set working directory
WORKDIR /code

# Default command
CMD ["ts-node"]

# Labels
LABEL maintainer="AI CodeForge"
LABEL description="Secure TypeScript execution environment"
LABEL version="1.0.0"
