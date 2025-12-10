# AI CodeForge - Python Execution Environment
# Secure, minimal Docker image for running Python code

FROM python:3.11-slim

# Install common Python packages
RUN pip install --no-cache-dir \
    pytest>=7.4.0 \
    requests>=2.31.0 \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    flask>=3.0.0 \
    fastapi>=0.104.0 \
    pydantic>=2.4.0

# Security: Create non-root user
RUN useradd -m -u 1000 -s /bin/bash runner && \
    mkdir -p /code /tmp && \
    chown -R runner:runner /code /tmp

# Switch to non-root user
USER runner

# Set working directory
WORKDIR /code

# Default command
CMD ["python3"]

# Labels
LABEL maintainer="AI CodeForge"
LABEL description="Secure Python execution environment"
LABEL version="1.0.0"
