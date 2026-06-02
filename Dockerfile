FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies first for layer caching (project is a "virtual" project —
# no [build-system] in pyproject.toml — so only deps get installed).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the application source.
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
