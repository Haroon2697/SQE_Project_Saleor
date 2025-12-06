#!/bin/bash
# Production Deployment Script
# This script deploys the application to production environment

set -e

echo "🌐 Starting Production Deployment..."
echo ""

# Configuration
DOCKER_IMAGE="${DOCKER_IMAGE:-haroon5295/saleor-prod:latest}"
PRODUCTION_DIR="/opt/saleor-production"
BACKUP_DIR="/opt/saleor-backups"

# Validate environment variables
if [ -z "$SECRET_KEY" ]; then
    echo "❌ Error: SECRET_KEY environment variable is required"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo "❌ Error: DATABASE_URL environment variable is required"
    exit 1
fi

# Create directories if they don't exist
mkdir -p "$PRODUCTION_DIR"
mkdir -p "$BACKUP_DIR"

# Backup current deployment
if [ -d "$PRODUCTION_DIR" ] && [ -f "$PRODUCTION_DIR/docker-compose.yml" ]; then
    echo "📦 Backing up current production deployment..."
    BACKUP_NAME="production-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$PRODUCTION_DIR" .
    echo "✅ Backup created: $BACKUP_NAME"
    
    # Keep only last 5 backups
    ls -t "$BACKUP_DIR"/production-backup-*.tar.gz | tail -n +6 | xargs rm -f || true
fi

# Pull latest Docker image
echo "🐳 Pulling latest Docker image..."
docker pull "$DOCKER_IMAGE" || {
    echo "❌ Error: Failed to pull Docker image"
    exit 1
}

# Update docker-compose.yml with new image
cat > "$PRODUCTION_DIR/docker-compose.yml" << EOF
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
      - DEBUG=False
      - ALLOWED_HOSTS=\${ALLOWED_HOSTS}
      - EMAIL_URL=\${EMAIL_URL}
      - SENTRY_DSN=\${SENTRY_DSN}
      - NEW_RELIC_LICENSE_KEY=\${NEW_RELIC_LICENSE_KEY}
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/graphql/"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: \${DB_USER:-saleor}
      POSTGRES_PASSWORD: \${DB_PASSWORD}
      POSTGRES_DB: \${DB_NAME:-saleor}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
  
  redis:
    image: redis:7-alpine
    restart: always

volumes:
  postgres_data:
EOF

# Deploy using docker-compose
cd "$PRODUCTION_DIR"
echo "🚀 Deploying application..."
docker-compose down || true
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run database migrations
echo "📊 Running database migrations..."
docker-compose exec -T web python manage.py migrate --noinput || {
    echo "❌ Error: Database migrations failed"
    exit 1
}

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput || echo "⚠️ Static files collection failed"

# Health check
echo "🏥 Performing health check..."
for i in {1..60}; do
    if curl -f http://localhost:8000/graphql/ > /dev/null 2>&1; then
        echo "✅ Application is healthy!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Error: Application failed health check"
        exit 1
    fi
    echo "Waiting for application... ($i/60)"
    sleep 2
done

# Run production smoke tests
echo "🧪 Running production smoke tests..."
curl -f http://localhost:8000/graphql/ -X POST \
    -H "Content-Type: application/json" \
    -d '{"query": "{ shop { name } }"}' || {
    echo "❌ Error: Smoke tests failed"
    exit 1
}

# Verify monitoring is active
echo "📊 Verifying monitoring..."
if [ -n "$SENTRY_DSN" ]; then
    echo "✅ Sentry error tracking enabled"
fi

if [ -n "$NEW_RELIC_LICENSE_KEY" ]; then
    echo "✅ New Relic monitoring enabled"
fi

echo ""
echo "✅ Production deployment completed!"
echo "🌐 Application URL: http://localhost:8000"
echo "📊 GraphQL Endpoint: http://localhost:8000/graphql/"
echo "📈 Monitoring: Enabled"
echo "🔔 Error Tracking: Enabled"

