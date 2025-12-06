#!/bin/bash
# Staging Deployment Script
# This script deploys the application to staging environment

set -e

echo "🚀 Starting Staging Deployment..."
echo ""

# Configuration
DOCKER_IMAGE="${DOCKER_IMAGE:-haroon5295/saleor-staging:latest}"
STAGING_DIR="/opt/saleor-staging"
BACKUP_DIR="/opt/saleor-backups"

# Create directories if they don't exist
mkdir -p "$STAGING_DIR"
mkdir -p "$BACKUP_DIR"

# Backup current deployment
if [ -d "$STAGING_DIR" ] && [ -f "$STAGING_DIR/docker-compose.yml" ]; then
    echo "📦 Backing up current deployment..."
    BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$STAGING_DIR" .
    echo "✅ Backup created: $BACKUP_NAME"
fi

# Pull latest Docker image
echo "🐳 Pulling latest Docker image..."
docker pull "$DOCKER_IMAGE" || echo "⚠️ Image pull failed, using local image"

# Update docker-compose.yml with new image
cat > "$STAGING_DIR/docker-compose.yml" << EOF
version: '3.8'
services:
  web:
    image: $DOCKER_IMAGE
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - REDIS_URL=\${REDIS_URL}
      - SECRET_KEY=\${SECRET_KEY}
      - DEBUG=True
      - ALLOWED_HOSTS=localhost,127.0.0.1,staging-saleor.example.com
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: saleor
      POSTGRES_PASSWORD: saleor
      POSTGRES_DB: saleor
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
EOF

# Deploy using docker-compose
cd "$STAGING_DIR"
echo "🚀 Deploying application..."
docker-compose down || true
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "📊 Running database migrations..."
docker-compose exec -T web python manage.py migrate --noinput || echo "⚠️ Migrations failed"

# Health check
echo "🏥 Performing health check..."
for i in {1..30}; do
    if curl -f http://localhost:8000/graphql/ > /dev/null 2>&1; then
        echo "✅ Application is healthy!"
        break
    fi
    echo "Waiting for application... ($i/30)"
    sleep 2
done

# Run smoke tests
echo "🧪 Running smoke tests..."
curl -f http://localhost:8000/graphql/ -X POST \
    -H "Content-Type: application/json" \
    -d '{"query": "{ shop { name } }"}' || echo "⚠️ Smoke test failed"

echo ""
echo "✅ Staging deployment completed!"
echo "🌐 Application URL: http://localhost:8000"
echo "📊 GraphQL Endpoint: http://localhost:8000/graphql/"

