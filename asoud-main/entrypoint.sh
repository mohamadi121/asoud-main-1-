#!/bin/sh

while ! nc -z db2 5432 ; do
    echo "Waiting for the PostgreSQL Server"
    sleep 3
done

exec "$@"
