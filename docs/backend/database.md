# MariaDB Docker Setup

This guide outlines how to set up a MariaDB container using Docker Compose, with optional SQL initialization and environment configuration.

## File Structure

```
project-root/
├── docker-compose.yml
├── Dockerfile
├── .env
└── init.sql   # optional
```

## docker-compose.yml

```yaml
version: '3.8'

services:
  mysql:
    build: .
    ports:
      - "3306:3306"
    env_file:
      - .env
    # volumes:
    #   - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```

## Dockerfile

```dockerfile
FROM mariadb:latest

EXPOSE 3306

# COPY ./init.sql /docker-entrypoint-initdb.d/
```

## .env

```env
MYSQL_DATABASE=hipperdb
MYSQL_USER=hipper_user
MYSQL_PASSWORD=supersecurepassword
MYSQL_ROOT_PASSWORD=evenmoresecurepassword
```

> Tip: Add `.env` to `.gitignore` to avoid committing sensitive data.

## Usage

Build and start the service:

```bash
docker-compose up --build
```

Stop the service:

```bash
docker-compose down
```

