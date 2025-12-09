# Deployment Instructions
## Comprehensive Guide for Staging and Production Deployment

---

## Document Information

| Field | Value |
|-------|-------|
| **Document Title** | Deployment Instructions for Saleor E-Commerce Platform |
| **Project Name** | SQE Project - Saleor |
| **Version** | 1.0 |
| **Date** | December 2024 |
| **Prepared By** | SQE Project Team |

---

## Executive Summary

This document provides comprehensive instructions for deploying the Saleor E-Commerce Platform to both staging and production environments. It covers manual deployment procedures, automated CI/CD deployment, Docker-based deployment, and cloud platform deployment options.

---

## Table of Contents

1. [Deployment Overview](#1-deployment-overview)
2. [Prerequisites](#2-prerequisites)
3. [Environment Configuration](#3-environment-configuration)
4. [Local Development Deployment](#4-local-development-deployment)
5. [Docker Deployment](#5-docker-deployment)
6. [Staging Environment Deployment](#6-staging-environment-deployment)
7. [Production Environment Deployment](#7-production-environment-deployment)
8. [CI/CD Automated Deployment](#8-cicd-automated-deployment)
9. [Database Migration](#9-database-migration)
10. [Monitoring and Logging](#10-monitoring-and-logging)
11. [Rollback Procedures](#11-rollback-procedures)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Deployment Overview

### 1.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SALEOR DEPLOYMENT ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   GitHub Repo   │
                              │  (Source Code)  │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  GitHub Actions │
                              │   (CI/CD)       │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
           ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
           │  Development  │  │    Staging    │  │  Production   │
           │  Environment  │  │  Environment  │  │  Environment  │
           └───────────────┘  └───────────────┘  └───────────────┘
                    │                  │                  │
                    ▼                  ▼                  ▼
           ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
           │   localhost   │  │ staging.domain│  │  prod.domain  │
           │   :8000/:9000 │  │     .com      │  │     .com      │
           └───────────────┘  └───────────────┘  └───────────────┘
```

### 1.2 Deployment Environments

| Environment | Purpose | URL | Deployment Method |
|-------------|---------|-----|-------------------|
| **Development** | Local testing | localhost:8000 | Manual |
| **Staging** | Pre-production testing | staging.example.com | CI/CD Auto |
| **Production** | Live application | example.com | CI/CD + Approval |

### 1.3 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Backend | Python/Django | 3.12/5.x |
| API | GraphQL/Graphene | 2.x |
| Database | PostgreSQL | 15 |
| Cache | Redis | 7 |
| Task Queue | Celery | 5.x |
| Web Server | Uvicorn | 0.32 |
| Containerization | Docker | Latest |
| Orchestration | Docker Compose | 3.8 |
| CI/CD | GitHub Actions | Latest |

---

## 2. Prerequisites

### 2.1 System Requirements

#### 2.1.1 Hardware Requirements

| Component | Development | Staging | Production |
|-----------|-------------|---------|------------|
| **CPU** | 2 cores | 4 cores | 8+ cores |
| **RAM** | 4 GB | 8 GB | 16+ GB |
| **Disk** | 20 GB | 50 GB | 100+ GB |
| **Network** | Local | 100 Mbps | 1 Gbps |

#### 2.1.2 Software Requirements

```bash
# Required Software Versions
Python >= 3.12
Node.js >= 20.x
PostgreSQL >= 15
Redis >= 7
Docker >= 24.0
Docker Compose >= 2.0
Git >= 2.40
```

### 2.2 Account Requirements

| Service | Purpose | Required For |
|---------|---------|--------------|
| GitHub | Source code, CI/CD | All environments |
| Docker Hub | Container registry | Staging, Production |
| Cloud Provider | Hosting | Staging, Production |

### 2.3 Access Requirements

| Access Type | Development | Staging | Production |
|-------------|-------------|---------|------------|
| Repository | Read/Write | Read | Read |
| Server SSH | N/A | Required | Required |
| Database | Local | Remote | Remote (Restricted) |
| Secrets | .env file | GitHub Secrets | GitHub Secrets |

---

## 3. Environment Configuration

### 3.1 Environment Variables

#### 3.1.1 Required Variables

```bash
# =============================================================================
# SALEOR ENVIRONMENT CONFIGURATION
# =============================================================================

# Django Settings
SECRET_KEY=your-super-secret-key-here-min-50-chars
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DATABASE_URL=postgres://user:password@host:5432/saleor

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# Email Configuration
EMAIL_URL=smtp://user:password@smtp.example.com:587/?tls=True
DEFAULT_FROM_EMAIL=noreply@example.com

# Media and Static Files
STATIC_URL=/static/
MEDIA_URL=/media/
AWS_STORAGE_BUCKET_NAME=your-bucket  # If using S3

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Sentry (Error Tracking)
SENTRY_DSN=https://xxx@sentry.io/xxx

# API Configuration
GRAPHQL_JWT_SECRET_KEY=your-jwt-secret
```

#### 3.1.2 Environment-Specific Variables

**Development (.env.development)**
```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://saleor:saleor@localhost:5432/saleor
REDIS_URL=redis://localhost:6379/0
EMAIL_URL=console://
```

**Staging (.env.staging)**
```bash
DEBUG=False
ALLOWED_HOSTS=staging.example.com
DATABASE_URL=postgres://saleor:password@staging-db:5432/saleor
REDIS_URL=redis://staging-redis:6379/0
EMAIL_URL=smtp://...
SENTRY_DSN=https://...@sentry.io/staging
```

**Production (.env.production)**
```bash
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgres://saleor:password@prod-db:5432/saleor
REDIS_URL=redis://prod-redis:6379/0
EMAIL_URL=smtp://...
SENTRY_DSN=https://...@sentry.io/production
SECURE_SSL_REDIRECT=True
```

### 3.2 GitHub Secrets Configuration

#### 3.2.1 Setting Up Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | `your-50-char-secret` |
| `DOCKERHUB_USERNAME` | Docker Hub username | `your-username` |
| `DOCKERHUB_TOKEN` | Docker Hub access token | `dckr_pat_xxx` |
| `DATABASE_URL_STAGING` | Staging DB connection | `postgres://...` |
| `DATABASE_URL_PROD` | Production DB connection | `postgres://...` |
| `SENTRY_DSN` | Sentry error tracking | `https://...` |

#### 3.2.2 Generating Secret Key

```bash
# Generate a secure Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Or use openssl
openssl rand -base64 50
```

---

## 4. Local Development Deployment

### 4.1 Initial Setup

#### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/SQE_Project_Saleor.git
cd SQE_Project_Saleor
```

#### Step 2: Create Virtual Environment

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

#### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Saleor dependencies
pip install -e .

# Install development dependencies
pip install pytest pytest-django pytest-cov
```

#### Step 4: Configure Environment

```bash
# Create environment file
cp .env.example .env

# Edit .env with your local settings
nano .env
```

#### Step 5: Setup Database

```bash
# Start PostgreSQL (if using Docker)
docker run -d \
  --name saleor-db \
  -e POSTGRES_USER=saleor \
  -e POSTGRES_PASSWORD=saleor \
  -e POSTGRES_DB=saleor \
  -p 5432:5432 \
  postgres:15

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser --email admin@example.com

# Populate sample data (optional)
python manage.py populatedb --createsuperuser
```

#### Step 6: Start Development Server

```bash
# Start Redis (if using Docker)
docker run -d --name saleor-redis -p 6379:6379 redis:7-alpine

# Start Django development server
python manage.py runserver 0.0.0.0:8000

# Or use uvicorn for ASGI
uvicorn saleor.asgi:application --reload --host 0.0.0.0 --port 8000
```

### 4.2 Accessing the Application

| Component | URL |
|-----------|-----|
| GraphQL API | http://localhost:8000/graphql/ |
| GraphQL Playground | http://localhost:8000/graphql/ |
| Admin Panel | http://localhost:8000/admin/ |
| Dashboard | http://localhost:9000/ (separate setup) |

---

## 5. Docker Deployment

### 5.1 Docker Single Container

#### Step 1: Build Docker Image

```bash
# Build the Docker image
docker build -t saleor:latest .

# Verify the image
docker images | grep saleor
```

#### Step 2: Run Container

```bash
# Run with environment variables
docker run -d \
  --name saleor-app \
  -p 8000:8000 \
  -e DATABASE_URL=postgres://saleor:saleor@host.docker.internal:5432/saleor \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  saleor:latest
```

### 5.2 Docker Compose Deployment

#### 5.2.1 Development Compose

**docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://saleor:saleor@db:5432/saleor
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=dev-secret-key-not-for-production
      - DEBUG=True
      - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - .:/app
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=saleor
      - POSTGRES_PASSWORD=saleor
      - POSTGRES_DB=saleor
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U saleor"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A saleor.celeryconf:app worker -E
    environment:
      - DATABASE_URL=postgres://saleor:saleor@db:5432/saleor
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

#### Step 3: Deploy with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

---

## 6. Staging Environment Deployment

### 6.1 Staging Infrastructure Setup

#### 6.1.1 Server Requirements

| Component | Specification |
|-----------|---------------|
| Server | 4 CPU, 8GB RAM, 50GB SSD |
| OS | Ubuntu 22.04 LTS |
| Docker | 24.0+ |
| Domain | staging.example.com |
| SSL | Let's Encrypt |

#### 6.1.2 Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Add user to docker group
sudo usermod -aG docker $USER

# Install required packages
sudo apt install -y git nginx certbot python3-certbot-nginx
```

### 6.2 Staging Deployment Steps

#### Step 1: Clone Repository on Staging Server

```bash
# SSH into staging server
ssh user@staging.example.com

# Clone repository
git clone https://github.com/your-org/SQE_Project_Saleor.git
cd SQE_Project_Saleor
```

#### Step 2: Configure Staging Environment

```bash
# Create staging environment file
cat > .env.staging << 'EOF'
# Staging Environment Configuration
DEBUG=False
SECRET_KEY=your-staging-secret-key-min-50-characters
ALLOWED_HOSTS=staging.example.com

# Database
DATABASE_URL=postgres://saleor:staging_password@db:5432/saleor

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

# Email
EMAIL_URL=smtp://user:pass@smtp.example.com:587/?tls=True

# Static/Media
STATIC_URL=/static/
MEDIA_URL=/media/
EOF
```

#### Step 3: Create Staging Docker Compose

**docker-compose.staging.yml**
```yaml
version: '3.8'

services:
  web:
    image: ${DOCKER_REGISTRY:-docker.io}/${DOCKER_USER:-saleor}/saleor-staging:${VERSION:-latest}
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env.staging
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py collectstatic --noinput &&
             uvicorn saleor.asgi:application --host 0.0.0.0 --port 8000"

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: saleor
      POSTGRES_PASSWORD: staging_password
      POSTGRES_DB: saleor
    volumes:
      - staging_postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U saleor"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - staging_redis_data:/data

  celery:
    image: ${DOCKER_REGISTRY:-docker.io}/${DOCKER_USER:-saleor}/saleor-staging:${VERSION:-latest}
    env_file:
      - .env.staging
    depends_on:
      - db
      - redis
    restart: unless-stopped
    command: celery -A saleor.celeryconf:app worker -E -l info

  celery-beat:
    image: ${DOCKER_REGISTRY:-docker.io}/${DOCKER_USER:-saleor}/saleor-staging:${VERSION:-latest}
    env_file:
      - .env.staging
    depends_on:
      - db
      - redis
    restart: unless-stopped
    command: celery -A saleor.celeryconf:app beat -l info

volumes:
  staging_postgres_data:
  staging_redis_data:
```

#### Step 4: Deploy to Staging

```bash
# Build and start staging environment
docker-compose -f docker-compose.staging.yml build
docker-compose -f docker-compose.staging.yml up -d

# Verify deployment
docker-compose -f docker-compose.staging.yml ps

# Check logs
docker-compose -f docker-compose.staging.yml logs -f web

# Run migrations (if not in command)
docker-compose -f docker-compose.staging.yml exec web python manage.py migrate

# Create admin user
docker-compose -f docker-compose.staging.yml exec web python manage.py createsuperuser
```

#### Step 5: Configure Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/saleor-staging
server {
    listen 80;
    server_name staging.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.example.com;

    ssl_certificate /etc/letsencrypt/live/staging.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.example.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/saleor-staging /etc/nginx/sites-enabled/

# Get SSL certificate
sudo certbot --nginx -d staging.example.com

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx
```

### 6.3 Staging Validation Checklist

| Check | Command/Action | Expected Result |
|-------|----------------|-----------------|
| Web server running | `docker-compose ps` | web: Up |
| Database connected | `docker-compose exec web python manage.py dbshell` | PostgreSQL prompt |
| Redis connected | `docker-compose exec web python -c "import redis; r=redis.Redis(); print(r.ping())"` | True |
| Migrations applied | Check admin panel | No errors |
| SSL working | Visit https://staging.example.com | Green lock |
| GraphQL accessible | Visit /graphql/ | Playground loads |

---

## 7. Production Environment Deployment

### 7.1 Production Infrastructure

#### 7.1.1 Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PRODUCTION ARCHITECTURE                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   CloudFlare    │
                              │   (CDN/WAF)     │
                              └────────┬────────┘
                                       │
                              ┌────────▼────────┐
                              │  Load Balancer  │
                              │   (Nginx/ALB)   │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐┌────────▼────────┐┌────────▼────────┐
           │   Web Server    ││   Web Server    ││   Web Server    │
           │   (Saleor)      ││   (Saleor)      ││   (Saleor)      │
           └────────┬────────┘└────────┬────────┘└────────┬────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
           ┌────────▼────────┐┌────────▼────────┐┌────────▼────────┐
           │   PostgreSQL    ││     Redis       ││   Celery        │
           │   (Primary +    ││   (Cluster)     ││   (Workers)     │
           │    Replica)     ││                 ││                 │
           └─────────────────┘└─────────────────┘└─────────────────┘
```

#### 7.1.2 Server Requirements

| Component | Specification | Quantity |
|-----------|---------------|----------|
| Web Servers | 8 CPU, 16GB RAM | 2-3 |
| Database | 4 CPU, 32GB RAM, SSD | 1 Primary + 1 Replica |
| Redis | 2 CPU, 8GB RAM | 1-3 (cluster) |
| Celery Workers | 4 CPU, 8GB RAM | 2+ |

### 7.2 Production Deployment Steps

#### Step 1: Prepare Production Environment

```bash
# Create production directory
mkdir -p /opt/saleor
cd /opt/saleor

# Clone repository
git clone https://github.com/your-org/SQE_Project_Saleor.git .
```

#### Step 2: Create Production Configuration

```bash
# Create production environment file
cat > .env.production << 'EOF'
# Production Environment Configuration
DEBUG=False
SECRET_KEY=${DJANGO_SECRET_KEY}
ALLOWED_HOSTS=example.com,www.example.com

# Database (Use managed database service)
DATABASE_URL=postgres://saleor:${DB_PASSWORD}@prod-db.example.com:5432/saleor

# Redis (Use managed Redis service)
REDIS_URL=redis://prod-redis.example.com:6379/0
CELERY_BROKER_URL=redis://prod-redis.example.com:6379/1

# Email
EMAIL_URL=smtp://${SMTP_USER}:${SMTP_PASS}@smtp.sendgrid.net:587/?tls=True
DEFAULT_FROM_EMAIL=noreply@example.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Static/Media (Use S3 or CDN)
AWS_ACCESS_KEY_ID=${AWS_KEY}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET}
AWS_STORAGE_BUCKET_NAME=saleor-media-prod
AWS_S3_CUSTOM_DOMAIN=cdn.example.com

# Monitoring
SENTRY_DSN=${SENTRY_DSN}

# Performance
CONN_MAX_AGE=60
EOF
```

#### Step 3: Create Production Docker Compose

**docker-compose.production.yml**
```yaml
version: '3.8'

services:
  web:
    image: ${DOCKER_REGISTRY}/saleor-prod:${VERSION:-latest}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    env_file:
      - .env.production
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py collectstatic --noinput &&
             gunicorn saleor.asgi:application -k uvicorn.workers.UvicornWorker 
             --bind 0.0.0.0:8000 --workers 4 --threads 2"

  celery:
    image: ${DOCKER_REGISTRY}/saleor-prod:${VERSION:-latest}
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 2G
    env_file:
      - .env.production
    command: celery -A saleor.celeryconf:app worker -E -l warning -c 4

  celery-beat:
    image: ${DOCKER_REGISTRY}/saleor-prod:${VERSION:-latest}
    deploy:
      replicas: 1
    env_file:
      - .env.production
    command: celery -A saleor.celeryconf:app beat -l warning
```

#### Step 4: Deploy to Production

```bash
# Pull latest images
docker-compose -f docker-compose.production.yml pull

# Deploy with zero downtime
docker-compose -f docker-compose.production.yml up -d --no-deps --scale web=3

# Verify deployment
docker-compose -f docker-compose.production.yml ps

# Check logs
docker-compose -f docker-compose.production.yml logs -f web
```

### 7.3 Production Validation Checklist

| Check | Action | Expected Result |
|-------|--------|-----------------|
| All containers running | `docker-compose ps` | All healthy |
| Database connection | Check logs for errors | No connection errors |
| SSL certificate valid | Check browser | Valid certificate |
| GraphQL endpoint | Visit /graphql/ | Returns schema |
| Static files loading | Check browser console | No 404 errors |
| Sentry integration | Trigger test error | Error appears in Sentry |
| Performance | Load test | Response < 500ms |

---

## 8. CI/CD Automated Deployment

### 8.1 GitHub Actions Deployment

The CI/CD pipeline automatically deploys to staging and production based on branch and conditions.

#### 8.1.1 Staging Deployment (Automatic)

```yaml
# Triggered automatically on push to main branch
staging:
  name: "🚀 Stage 4: Staging Deployment"
  runs-on: ubuntu-latest
  needs: [build, test]
  if: github.ref == 'refs/heads/main' && needs.test.result == 'success'
  environment:
    name: staging
    url: https://staging.example.com
  
  steps:
    - name: Deploy to Staging
      run: |
        # SSH and deploy
        ssh user@staging.example.com << 'EOF'
          cd /opt/saleor
          git pull origin main
          docker-compose -f docker-compose.staging.yml pull
          docker-compose -f docker-compose.staging.yml up -d
        EOF
```

#### 8.1.2 Production Deployment (With Approval)

```yaml
# Requires manual approval in GitHub
deploy:
  name: "🌐 Stage 5: Production Deployment"
  runs-on: ubuntu-latest
  needs: [staging]
  if: needs.staging.result == 'success'
  environment:
    name: production
    url: https://example.com
  
  steps:
    - name: Deploy to Production
      run: |
        # Blue-green deployment
        ssh user@production.example.com << 'EOF'
          cd /opt/saleor
          docker-compose -f docker-compose.production.yml pull
          docker-compose -f docker-compose.production.yml up -d --no-deps web
          # Health check
          sleep 30
          curl -f https://example.com/health/ || exit 1
        EOF
```

### 8.2 Deployment Triggers

| Event | Target | Automatic |
|-------|--------|-----------|
| Push to `main` | Staging | ✅ Yes |
| Staging success | Production | ⚠️ Requires approval |
| Manual trigger | Any | ✅ Yes |
| Tag created | Production | ✅ Yes |

### 8.3 Setting Up Environment Protection

1. Go to **Repository Settings** → **Environments**
2. Create `staging` and `production` environments
3. For `production`:
   - Enable **Required reviewers**
   - Add team members as reviewers
   - Optionally add **Wait timer** (e.g., 15 minutes)

---

## 9. Database Migration

### 9.1 Migration Commands

```bash
# Check for pending migrations
docker-compose exec web python manage.py showmigrations

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Apply specific app migrations
docker-compose exec web python manage.py migrate app_name

# Rollback migration
docker-compose exec web python manage.py migrate app_name 0001_previous
```

### 9.2 Migration Best Practices

| Practice | Description |
|----------|-------------|
| Test locally first | Run migrations on local DB before staging |
| Backup before migration | Always backup database before production migration |
| Use transactions | Django migrations are transactional by default |
| Avoid data migrations in deploy | Separate data migrations from schema changes |

### 9.3 Database Backup

```bash
# Backup database
docker-compose exec db pg_dump -U saleor saleor > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T db psql -U saleor saleor < backup_20241209_120000.sql
```

---

## 10. Monitoring and Logging

### 10.1 Logging Configuration

```python
# saleor/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### 10.2 Monitoring Tools

| Tool | Purpose | Setup |
|------|---------|-------|
| **Sentry** | Error tracking | Set `SENTRY_DSN` |
| **New Relic** | APM | Install newrelic package |
| **Prometheus** | Metrics | Add metrics endpoint |
| **Grafana** | Dashboards | Connect to Prometheus |

### 10.3 Health Check Endpoint

```python
# saleor/urls.py (add health check)
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'database': 'connected',
        'redis': 'connected'
    })

urlpatterns = [
    path('health/', health_check),
    # ... other urls
]
```

---

## 11. Rollback Procedures

### 11.1 Quick Rollback

```bash
# Rollback to previous Docker image
docker-compose -f docker-compose.production.yml stop web
docker-compose -f docker-compose.production.yml up -d web --force-recreate \
  -e VERSION=previous-tag

# Verify rollback
curl -f https://example.com/health/
```

### 11.2 Database Rollback

```bash
# Stop application
docker-compose stop web celery

# Restore database from backup
docker-compose exec -T db psql -U saleor saleor < backup_before_migration.sql

# Rollback migrations
docker-compose exec web python manage.py migrate app_name 0001_previous

# Restart application
docker-compose up -d web celery
```

### 11.3 Full Rollback Procedure

1. **Identify the issue** - Check logs and monitoring
2. **Stop traffic** - Update load balancer to maintenance mode
3. **Rollback code** - Deploy previous version
4. **Rollback database** (if needed) - Restore from backup
5. **Verify** - Run health checks
6. **Resume traffic** - Update load balancer

---

## 12. Troubleshooting

### 12.1 Common Issues

#### Issue: Container won't start

```bash
# Check container logs
docker-compose logs web

# Check container status
docker-compose ps

# Inspect container
docker inspect saleor-web
```

#### Issue: Database connection refused

```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()"
```

#### Issue: Static files not loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check static file directory
docker-compose exec web ls -la /app/staticfiles/
```

#### Issue: Celery tasks not running

```bash
# Check Celery logs
docker-compose logs celery

# Check Redis connection
docker-compose exec celery python -c "import redis; r=redis.Redis.from_url('redis://redis:6379/0'); print(r.ping())"
```

### 12.2 Debug Commands

```bash
# Enter container shell
docker-compose exec web bash

# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec web python manage.py dbshell

# Check environment variables
docker-compose exec web env | grep -E 'DATABASE|REDIS|SECRET'
```

---

## Appendix A: Deployment Checklist

### Pre-Deployment Checklist

- [ ] All tests passing in CI/CD
- [ ] Code reviewed and approved
- [ ] Database backup created
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented
- [ ] Team notified of deployment

### Post-Deployment Checklist

- [ ] Health check passing
- [ ] All services running
- [ ] Logs show no errors
- [ ] Smoke tests passing
- [ ] Monitoring shows normal metrics
- [ ] Team notified of successful deployment

---

## Appendix B: Quick Reference Commands

```bash
# ==================== DEVELOPMENT ====================
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop environment
docker-compose down

# ==================== STAGING ====================
# Deploy to staging
docker-compose -f docker-compose.staging.yml up -d

# Update staging
git pull && docker-compose -f docker-compose.staging.yml up -d --build

# ==================== PRODUCTION ====================
# Deploy to production
docker-compose -f docker-compose.production.yml up -d

# Scale web servers
docker-compose -f docker-compose.production.yml up -d --scale web=3

# Rolling update
docker-compose -f docker-compose.production.yml up -d --no-deps web

# ==================== MAINTENANCE ====================
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Database backup
docker-compose exec db pg_dump -U saleor saleor > backup.sql
```

---

**End of Deployment Instructions**

---

*Document Version: 1.0*
*Last Updated: December 9, 2024*
*Maintained By: SQE Project Team*

