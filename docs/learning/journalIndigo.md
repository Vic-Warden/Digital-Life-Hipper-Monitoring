# Learning Journal

### Learning story #203

I wanted to find out how I could containerize a `mysql/mariadb` database so that our team can work from their laptops without having to connect to a remote database.

In order to achieve this I used this source from [Medium](https://vijayasimhabr.medium.com/running-mysql-database-server-with-docker-ad10533473c7), they explained in a clear manner how this could be achieved.

They explained that  should have a  `docker-compose.yml`. I created that and also made a Dockerfile which contained the actual mysql installation, this way I could seperate the two and have more control over each part.

```yml
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

I chose to expose port 3306 because it is the default MySQL database port. I also stored the sensitive information such as usernames and passwords inside a `.env` file, which gets passed down onto the container. This prevents users from accessing the password if they have breached the container.

I also chose not to use a volume as I wanted the environment to be purgable very quickly for testing purposes.

Here is the corresponding Dockerfile

```Dockerfile
FROM mariadb:latest

# Expose MySQL port
EXPOSE 3306

# Copy initialization SQL script
COPY ./init.sql /docker-entrypoint-initdb.d/
```

Here we are using the ltest version of the `mariadb` container. We are also copying the `init.sql` file into our `entrypointdb` for our container to run/use it when it gets initialized.