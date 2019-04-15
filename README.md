# Ideal Temperature
Ideal Temperature is a web based custom temperature monitoring tool. The software consists of two parts. Temperature collection software designed to run on a Raspberry Pi which then reports the temperature back to a central web server. The web server is built on the Django framework and runs in a series of docker containers for easy deployment with Nginx, Gunicorn and PostgreSQL.

## Setup web server
The following deployment directions are written for Ubuntu 18.04.
1. Install Docker CE and Docker Compose using the directions from the Docker website
https://docs.docker.com/install/linux/docker-ce/ubuntu/
1. Copy docker-compose_template.yml to docker-compose.yml
1. Fill in the blank environment variables in docker-compose.yml for the web container
    1. SECRET_KEY - Django secret key. The dollar symbols must either be escaped or removed from the key.
    1. SQL_ENGINE - sqlengine django should used. Should be django.db.backend.postgresql for postgresql
    1. SQL_USER - username of the owner of the database in postgresql. This user will be setup during deployment.
    1. SQL_PASSWORD - password for the SQL_USER.
    1. SQL_HOST - Name of the docker container hosting the postgresql database. Should be set to db.
    1. SQL_PORT - Port number the postgresql server is listening on. This will typically be 5432.
    1. ALLOWED_HOST - Domain name of the server hosting the website. Right now this variable only allows a single value. However since the Django config allows a list in future updates this variable should also allow multiple values.
1. Fill in the blank environment variables in docker-compose.yml for the db container
    1. POSTGRES_USER - This must match the SQL_USER defined as a web container environment variable.
    1. POSTGRES_PASSWORD - This must match the SQL_PASSWORD defined as a web container environment variable.
1. Run the following command to build and start the containers
```
docker-compose up -d
```

### Add superuser
The first time Ideal Temperature is run you will need to add a superuser using the following command.
```
docker exec -it idealtemperature_web_1 python manage.py createsuperuser
```

## Cleanup the database
Use the following command to thin out database records.
```
python manage.py cleanTemperatureRecords <record age in days> <new interval in minutes>
```
\<record age in days\> is the point where any records older then this number of days will be thined.
\<new interval in minutes\> is the new interval used. For all records older than the provided record age there will only be one record in each interval. The rest of the records will be deleted.
For example, if temperature records are initially collected at a rate of one new measurement every 5 minutes then to preserve one temperature record every 30 minutes once the records are at least 120 days old use the following command.
```
python manage.py cleanTemperatureRecords 120 30
```
The cleanTemperatureRecords command is run as a cron job inside the web container. By defaul the job is run once a day at midnight with a record age of 7 days and an interval of 60 minutes. The cronjob is defined in the cronjobs.txt file. If you wish to make changes then update the file and rebuild the web container.

## Setup Raspberry Pi temperature sensors
TBD

## Start postgreSQL docker container (for development)
If you would like to run an independent postgres container for use with the django development web server us the following command.
```
docker run --name postgres-dev -p 5432:5432 -e POSTGRES_USER=<username> -e POSTGRES_PASSWORD=<password> -v <DB data dir>:/var/lib/postgresql/data -d postgres
```
