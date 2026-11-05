# syntax=docker/dockerfile:1

FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DB_PATH=/app/data/backlog.db

WORKDIR /app

# Install dependencies separately to preserve the dependency cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use a fixed, unprivileged UID/GID for predictable volume permissions.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app/data \
    && chown -R app:app /app

COPY --chown=app:app . .

USER 10001:10001

EXPOSE 5000

# The application currently shares one SQLite connection at module scope.
# Keep Gunicorn single-worker/single-thread until DB connections are scoped safely.
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=1", "--threads=1", "--access-logfile=-", "--error-logfile=-", "app:app"]
