#!/bin/bash

echo "=========================================="
echo "PostgreSQL Docker Setup"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from env.template..."
    cp env.template .env
    echo "✅ Created .env file"
    echo "📝 Please edit .env with your credentials if needed"
else
    echo "✅ .env file found"
fi

echo ""
echo "Starting Docker containers..."
docker compose up -d --build

echo ""
echo "Waiting for database to be ready..."
sleep 5

echo ""
echo "Running migrations..."
docker compose exec -T web python manage.py migrate

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "📌 Your application is running at: http://localhost:8000"
echo "📌 Database: PostgreSQL on localhost:5432"
echo ""
echo "Next steps:"
echo "  1. Create superuser: docker compose exec web python manage.py createsuperuser"
echo "  2. View logs: docker compose logs -f"
echo "  3. Stop: docker compose down"
echo ""
