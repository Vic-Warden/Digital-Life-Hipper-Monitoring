FROM mariadb:latest

# Expose MySQL port
EXPOSE 3306

# Copy initialization SQL script
COPY ./init.sql /docker-entrypoint-initdb.d/