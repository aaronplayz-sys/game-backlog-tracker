# Game Backlog Tracker

A database-backed game and media tracker that began as a Valencia College course project. The application includes a console interface, a Flask web interface, SQLite persistence, and TMDB integration.

## Requirements

- Docker Engine and the Docker Compose plugin for containerized use
- Python 3.12+ for native execution
- A TMDB API key for movie and TV search features

## Run with Docker

Clone the repository and enter its directory:

```bash
git clone https://github.com/aaronplayz-sys/game-backlog-tracker.git
cd game-backlog-tracker
```

Create your local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env`.

Edit `.env` and set:
- `TMDB_API_KEY`: your TMDB API key
- `FLASK_SECRET_KEY`: a long, random secret used to sign Flask sessions
- `USERSCRIPT_API_SECRET`: a separate random secret for the userscript API
- `APP_PORT`: optional host port; defaults to `5000`

Generate random secrets with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Do not commit your real `.env` file.

Build and start the web application:

```bash
docker compose up -d --build
```

Open http://localhost:5000. If you changed `APP_PORT`, use that port instead.

Useful commands:

```bash
docker compose ps
docker compose logs -f backlog-tracker
docker compose exec backlog-tracker python load_sample_data.py
```

Sample data is optional and is not loaded automatically.

### Existing database volumes

The container now runs as the unprivileged UID/GID `10001`. A database volume created by an older root-running image may need its ownership changed to UID/GID `10001` before the updated container can write to it. Back up your database before performing any ownership migration. Do not remove the named volume when upgrading; it contains your persistent data.

### Run the console application in Docker

The default container command starts the Flask web interface. To run the original console application instead:

```bash
docker compose run --rm backlog-tracker python main.py
```

## Run natively with Python

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file with `TMDB_API_KEY` and `FLASK_SECRET_KEY` configured. Start the console application with `python main.py`, or start the Flask development server with `python app.py`.

The Flask development server is for local development. The Docker deployment uses Gunicorn.

## Container design notes

- The image uses a non-root application user (UID/GID `10001`).
- SQLite data is stored in the persistent `backlog_data` named volume.
- Flask session signing uses the required `FLASK_SECRET_KEY` environment variable.
- The userscript API fails closed when `USERSCRIPT_API_SECRET` is unset.
- Gunicorn is configured with one worker and one thread because the current application creates and shares a SQLite connection at module import. Increase concurrency only after refactoring database connection lifecycle and testing concurrent access.
- The container health check requests the Flask home page.

For application changes, rebuild with `docker compose up -d --build`.

## Project checklist

- [x] Console application
- [x] Flask web interface
- [x] SQLite persistence
- [x] Dockerfile and Compose configuration
- [x] Containerized deployment instructions
- [ ] Expand application documentation
