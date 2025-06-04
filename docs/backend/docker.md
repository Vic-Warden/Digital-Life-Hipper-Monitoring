# Docker Compose Overview

This setup defines a MySQL database and a Flask web server using Docker Compose for local development. It is also extremely useful to show progress to anyone involved such as the Product Owner.

## Services

### 1. MySQL (`hipper-mysql`)
- **Builds from**: `./src/back-end/database`
- **Exposes**: `3306:3306`
- **Env file**: `./src/back-end/database/.env`
- **Init script**: Mounts `init.sql` to initialize DB on startup
- **Healthcheck**:
  - Ensures the container is only marked healthy if it can connect using provided credentials.
  - **Test**: `mariadb -h 127.0.0.1 -u $MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD || exit 1`
  - **Interval**: Every 5 seconds
  - **Timeout**: 3 seconds
  - **Retries**: 10
- **Restart policy**: `unless-stopped`

**Purpose**: Provides a backend database with a custom setup using a Dockerfile and environment variables. The healthcheck ensures Flask does not start until MySQL is ready.

### 2. Flask (`hipper-webapp`)
- **Builds from**: `.`
- **Image**: Custom build using `python:3.11-slim`
- **Exposes**: `5000:5000`
- **Dependencies**: Installed via `requirements.txt`
- **Working directory**: `/app` (mounted from `./src/app`)
- **Command**: Runs Flask app on `0.0.0.0:5000`
- **Environment**:
  - `FLASK_APP=__init__.py`
- **Depends on**: MySQL (waits until MySQL is healthy)
- **Volumes**: Mounts the app directory for live development
- **Env file**: Reuses MySQL `.env` for shared config

**Purpose**: Serves as the application backend using Flask, with support for MySQL and dotenv for configuration. Volume mounting allows local development without rebuilding the image for every code change.

## Important

The Flask service is built from a `Dockerfile` located at the root of this project.


## Usage

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

## Access

- Web: http://localhost:5000

- MySQL: localhost:3306 (credentials found in src/back-end/database/database.env)

## Sources used

- ChatGPT to discover issues and help with the script
- Google Gemini to discover issues and help with the script
- Indigo's first sql docker file