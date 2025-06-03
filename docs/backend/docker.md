# Docker Compose Overview

This setup defines a MySQL database and an Nginx web server using Docker Compose for local development. It is also extremely useful to show progress to anyone involved such as the Product Owner.

## Services

### 1. MySQL (`hipper-mysql`)
- **Builds from**: `./src/back-end/database`
- **Exposes**: `3306:3306`
- **Env file**: `./src/back-end/database/.env`
- **Init script**: Mounts `init.sql` to initialize DB on startup

**Purpose**: Provides a backend database with custom setup using a Dockerfile and environment variables.

### 2. Flask (`hipper-webapp`)
- **Builds from**: `.`
- **Image**: Custom build using `python:3.11-slim`
- **Exposes**: `5000:5000`
- **Dependencies**: Installed via `requirements.txt`
- **Working directory**: `/app`
- **Command**: Runs Flask app on `0.0.0.0:5000`

**Purpose**: Serves as the application backend using Flask, with support for MySQL and dotenv for configuration.

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

- ChatGPT to help with script
- Indigo's first sql docker file