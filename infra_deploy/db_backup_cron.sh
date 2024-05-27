#!/bin/bash

# delete local copy of a previous backup
find . -name '*.bac' -delete

# create a db backup from a docker container
DB_CONTAINER=$(docker ps --format "{{.Names}}" | grep "postgres")
FILENAME="postgres_backup_$(date +%Y-%m-%d-%H-%M).bac"
echo "Creating a backup of a database"
docker exec -i $DB_CONTAINER pg_dump -U lyubimovka lyubimovka > $FILENAME

# execute a script of an upload to Yandex Disk
echo "Uploading $FILENAME to Yandex Disk"
python3 yadisk_upload.py
echo "Postgres backup upload complete"
