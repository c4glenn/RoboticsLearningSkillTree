#!/bin/sh

set -e

# Wait for PostgreSQL
echo "Waiting for Postgres..."
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Postgres is ready"

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Running migrations..."
  python manage.py migrate --noinput
fi

exec "$@"
