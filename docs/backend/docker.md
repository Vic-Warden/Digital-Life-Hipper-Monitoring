# Docker Compose Overview

This setup defines a MySQL database and an Nginx web server using Docker Compose for local development. It is also extremely useful to show progress to anyone involved such as the Product Owner.

## Services

### 1. MySQL (`hipper-mysql`)
- **Builds from**: `./src/back-end/database`
- **Exposes**: `3306:3306`
- **Env file**: `./src/back-end/database/.env`
- **Init script**: Mounts `init.sql` to initialize DB on startup

**Purpose**: Provides a backend database with custom setup using a Dockerfile and environment variables.

### 2. Nginx (`hipper-nginx`)
- **Image**: `nginx:alpine`
- **Exposes**: `8080:80`
- **Mounts**:
  - Static files: `./src/app/templates → /usr/share/nginx/html`
  - Config: `./src/app/config/nginx/default.conf → /etc/nginx/conf.d/default.conf`

**Purpose**: Serves static content and uses a custom Nginx config.

## Usage

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

## Access

- Web: http://localhost:8080

- MySQL: localhost:3306 (credentials found in src/back-end/database.env)

## Sources used

- ChatGPT to help with script
- Indigo's first sql docker file