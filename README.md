# Ideal Temperature
Ideal Temperature is a web based custom temperature monitoring tool. The software consists of two parts. Temperature collection software designed to run on a Raspberry Pi which then reports the temperature back to a central web server. The web server is built on the Django framework and runs in a series of docker containers for easy deployment with Nginx, Gunicorn and PostgreSQL.

## Setup web server
The following deployment directions are written for Ubuntu 18.04.
1. Install Docker CE and Docker Compose using the directions from the Docker website
https://docs.docker.com/install/linux/docker-ce/ubuntu/
3. Copy docker-compose_template.yml to docker-compose.yml
4. Fill in the blank environment variables in docker-compose.yml
5. Run the following command to build the containers
```
docker-compose up -d
```

### Add superuser
The first time Ideal Temperature is run you will need to add a superuser using the following command.
```
docker exec -it idealtemperature_web_1 python manage.py createsuperuser
```
## Setup Raspberry Pi temperature sensors
TBD

## Start postgreSQL docker container (for development)
If you would like to run an independent postgres container for use with the django development web server us the following command.
```
docker run --name postgres-dev -p 5432:5432 -e POSTGRES_USER=<username> -e POSTGRES_PASSWORD=<password> -v <DB data dir>:/var/lib/postgresql/data -d postgres
```
