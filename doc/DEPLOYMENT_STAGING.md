# Staging Deployment Guide

**Version:** 1.0  
**Date:** December 7, 2025  
**Environment:** Staging

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Configuration](#configuration)
4. [Deployment Steps](#deployment-steps)
5. [Verification](#verification)
6. [Rollback Procedure](#rollback-procedure)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1.1 Required Access

- ✅ Docker Hub account access
- ✅ Staging server SSH access
- ✅ Database access credentials
- ✅ Environment variable access
- ✅ GitHub repository access

### 1.2 Required Tools

- Docker 20.10+ installed
- Docker Compose 2.0+ installed
- Git installed
- SSH client installed
- kubectl (if using Kubernetes)

### 1.3 Required Knowledge

- Docker container management
- Linux command line
- Environment variable management
- Database migration procedures

---

## Environment Setup

### 2.1 Server Requirements

**Minimum Specifications:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS or similar

**Network Requirements:**
- Port 80 (HTTP)
- Port 443 (HTTPS)
- Port 5432 (PostgreSQL - internal)
- Port 6379 (Redis - internal)

### 2.2 Docker Environment

Ensure Docker is installed and running:

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Verify Docker is running
docker ps
```

---

## Configuration

### 3.1 Environment Variables

Create `.env.staging` file with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@postgres:5432/saleor_staging
POSTGRES_DB=saleor_staging
POSTGRES_USER=saleor
POSTGRES_PASSWORD=<secure-password>

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Application Configuration
SECRET_KEY=<generate-secure-secret-key>
ALLOWED_HOSTS=staging.example.com,staging-api.example.com
DEBUG=False

# Email Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=staging@example.com
EMAIL_HOST_PASSWORD=<email-password>

# Payment Gateway (Test Mode)
PAYMENT_GATEWAY_API_KEY=<test-api-key>
PAYMENT_GATEWAY_MODE=test

# Docker Hub
DOCKERHUB_USERNAME=<your-username>
DOCKERHUB_TOKEN=<your-token>
```

### 3.2 Docker Compose Configuration

Create `docker-compose.staging.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    image: ${DOCKERHUB_USERNAME}/saleor:staging-latest
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./media:/app/media
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
```

---

## Deployment Steps

### 4.1 Pre-Deployment Checklist

- [ ] All tests passing in CI/CD pipeline
- [ ] Code reviewed and approved
- [ ] Database backup created
- [ ] Environment variables configured
- [ ] Docker images built and pushed
- [ ] Deployment window scheduled

### 4.2 Step 1: Pull Latest Code

```bash
# SSH into staging server
ssh user@staging-server

# Navigate to application directory
cd /opt/saleor-staging

# Pull latest code
git pull origin develop
```

### 4.3 Step 2: Pull Latest Docker Image

```bash
# Login to Docker Hub
echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin

# Pull latest staging image
docker pull ${DOCKERHUB_USERNAME}/saleor:staging-latest
```

### 4.4 Step 3: Run Database Migrations

```bash
# Run migrations in a temporary container
docker run --rm \
  --env-file .env.staging \
  --network saleor-staging_default \
  ${DOCKERHUB_USERNAME}/saleor:staging-latest \
  python manage.py migrate
```

### 4.5 Step 4: Collect Static Files

```bash
# Collect static files
docker run --rm \
  --env-file .env.staging \
  --network saleor-staging_default \
  -v $(pwd)/media:/app/media \
  ${DOCKERHUB_USERNAME}/saleor:staging-latest \
  python manage.py collectstatic --noinput
```

### 4.6 Step 5: Deploy Application

```bash
# Stop existing containers
docker compose -f docker-compose.staging.yml down

# Start new containers
docker compose -f docker-compose.staging.yml up -d

# Verify containers are running
docker compose -f docker-compose.staging.yml ps
```

### 4.7 Step 6: Health Check

```bash
# Wait for services to be ready
sleep 30

# Check application health
curl http://localhost:8000/health/

# Check container logs
docker compose -f docker-compose.staging.yml logs web
```

---

## Verification

### 5.1 Application Health

**Health Check Endpoint:**
```bash
curl http://staging.example.com/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
```

### 5.2 Functional Verification

**Test Checklist:**
- [ ] Homepage loads correctly
- [ ] User can register/login
- [ ] Products are visible
- [ ] Shopping cart works
- [ ] Checkout process works
- [ ] Payment processing works (test mode)
- [ ] Admin panel accessible
- [ ] API endpoints respond correctly

### 5.3 Performance Verification

```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://staging.example.com/

# Monitor resource usage
docker stats
```

**Expected Metrics:**
- Response time: < 500ms
- CPU usage: < 70%
- Memory usage: < 80%

---

## Rollback Procedure

### 6.1 When to Rollback

- Critical bugs discovered
- Performance degradation
- Data corruption
- Security vulnerabilities

### 6.2 Rollback Steps

```bash
# 1. Stop current containers
docker compose -f docker-compose.staging.yml down

# 2. Pull previous stable image
docker pull ${DOCKERHUB_USERNAME}/saleor:staging-<previous-version>

# 3. Update docker-compose to use previous image
# Edit docker-compose.staging.yml to use previous tag

# 4. Start containers with previous version
docker compose -f docker-compose.staging.yml up -d

# 5. Verify rollback
curl http://staging.example.com/health/
```

### 6.3 Database Rollback

```bash
# Restore database from backup
docker exec -i saleor-staging-db-1 psql -U saleor -d saleor_staging < backup.sql
```

---

## Troubleshooting

### 7.1 Common Issues

#### Issue: Container won't start
**Solution:**
```bash
# Check logs
docker compose -f docker-compose.staging.yml logs web

# Check container status
docker ps -a

# Restart container
docker compose -f docker-compose.staging.yml restart web
```

#### Issue: Database connection errors
**Solution:**
```bash
# Verify database is running
docker compose -f docker-compose.staging.yml ps db

# Check database logs
docker compose -f docker-compose.staging.yml logs db

# Test connection
docker exec -it saleor-staging-db-1 psql -U saleor -d saleor_staging
```

#### Issue: Static files not loading
**Solution:**
```bash
# Re-collect static files
docker compose -f docker-compose.staging.yml exec web python manage.py collectstatic --noinput

# Check file permissions
ls -la media/
```

### 7.2 Log Locations

- **Application logs:** `docker compose logs web`
- **Database logs:** `docker compose logs db`
- **System logs:** `/var/log/syslog`

### 7.3 Support Contacts

- **DevOps Team:** devops@example.com
- **Development Team:** dev@example.com
- **On-Call Engineer:** [Phone Number]

---

## Post-Deployment

### 8.1 Monitoring

- Monitor application metrics for 24 hours
- Check error logs regularly
- Monitor performance metrics
- Verify all integrations working

### 8.2 Documentation

- Update deployment log
- Document any issues encountered
- Update runbook if procedures changed

---

**Last Updated:** December 7, 2025  
**Next Review:** [TBD]

