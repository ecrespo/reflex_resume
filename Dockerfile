ARG PYTHON_VERSION=3.13.9
ARG UV_VERSION=latest

# UV stage to allow static --from references (no ARG expansion in --from)
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# Build stage: Install dependencies and compile Reflex app
FROM python:${PYTHON_VERSION}-slim-trixie AS builder

# Install system dependencies required for Reflex compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=uv /uv /uvx /bin/

# Set working directory
WORKDIR /app

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
FROM python:${PYTHON_VERSION}-slim-trixie

LABEL authors="Ernesto Crespo <ecrespo@gmail.com>"
LABEL description="Reflex Resume"

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy uv for runtime
COPY --from=uv /uv /bin/

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