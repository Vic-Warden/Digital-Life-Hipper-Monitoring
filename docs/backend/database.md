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

