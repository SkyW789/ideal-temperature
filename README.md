# ideal-temperature
Web based custom temperature monitoring tool

## Start postgres docker container

```
docker run --name postgres-dev -p 5432:5432 -e POSTGRES_USER=<username> -e POSTGRES_PASSWORD=<password> -v <DB data dir>:/var/lib/postgresql/data -d postgres
```

## Fill in the settings.py file
In the settings-raw.py file located at website/web/settings-raw.py update the database information and change the file name to settings.py. When ready for deployment set debug to false and insert a static key.
