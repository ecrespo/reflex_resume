ARG UBUNTU_VERSION=26.04
ARG PYTHON_VERSION=3.13.17
ARG UV_VERSION=0.13.5

# UV stage to allow static --from references (no ARG expansion in --from)
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# Build stage: Install dependencies and compile Reflex app
FROM ubuntu:${UBUNTU_VERSION} AS builder

ARG PYTHON_VERSION

# Install system dependencies required for Reflex compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=uv /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Never install the dev dependency group (lint/security tools) in the image.
# Ubuntu does not ship Python 3.13, so uv installs a managed interpreter in
# /opt/python; the runtime stage copies it to the same path the venv points to.
ENV UV_NO_DEV=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON=${PYTHON_VERSION} \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_PYTHON_PREFERENCE=only-managed

RUN uv python install --no-cache

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .

# Set environment variables for build
ENV PATH="/app/.venv/bin:$PATH"

# Initialize and compile Reflex app (creates .web directory and other necessary files)
RUN uv run reflex init

# Runtime stage: Minimal production image
FROM ubuntu:${UBUNTU_VERSION}

ARG PYTHON_VERSION

LABEL authors="Ernesto Crespo <ecrespo@gmail.com>"
LABEL description="Reflex Resume"

ENV UV_NO_DEV=1 \
    UV_PYTHON=${PYTHON_VERSION} \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_PYTHON_PREFERENCE=only-managed

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (the Ubuntu image already has an "ubuntu" user with UID 1000)
RUN userdel --remove ubuntu && useradd -m -u 1000 appuser

WORKDIR /app

# Copy uv for runtime
COPY --from=uv /uv /bin/

# Copy the uv-managed Python interpreter the virtual environment links to
COPY --from=builder /opt/python /opt/python

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy compiled .web directory from builder
COPY --from=builder --chown=appuser:appuser /app/.web /app/.web

# Copy application code
COPY --chown=appuser:appuser . .
COPY --chown=appuser:appuser .python-version .

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run","reflex","run","--backend-only"]
EXPOSE 8000