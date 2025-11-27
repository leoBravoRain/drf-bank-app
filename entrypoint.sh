#!/bin/sh

# Get database host from environment variable, default to 'db' for backward compatibility
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
while ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}"; do
  sleep 1
done

echo "PostgreSQL is ready!"
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"
