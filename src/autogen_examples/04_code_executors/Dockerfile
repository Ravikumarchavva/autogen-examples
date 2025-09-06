# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Copy the docker example project files
COPY . /app

# Install the project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Optional: install bash and other useful tools
RUN apt-get update && apt-get install -y bash curl git && rm -rf /var/lib/apt/lists/*

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"


# Run jupyter lab by default
CMD ["python3"]
