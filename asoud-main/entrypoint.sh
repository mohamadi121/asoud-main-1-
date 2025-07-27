#!/bin/sh

# Check environment to determine database host
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.production" ]; then
    DB_HOST="db2"
else
    DB_HOST="db"
fi

echo "Waiting for PostgreSQL on $DB_HOST..."
while ! nc -z $DB_HOST 5432 ; do
    echo "Waiting for the PostgreSQL Server ($DB_HOST)"
    sleep 3
done

echo "PostgreSQL is ready!"
exec "$@"
