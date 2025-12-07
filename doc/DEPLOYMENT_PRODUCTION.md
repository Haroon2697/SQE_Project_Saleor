# Production Deployment Guide

**Version:** 1.0  
**Date:** December 7, 2025  
**Environment:** Production  
**Classification:** CONFIDENTIAL

---

## ⚠️ WARNING

**This document contains production deployment procedures. Handle with extreme care.**
- Never deploy during business hours without approval
- Always have rollback plan ready
- Test all procedures in staging first
- Maintain deployment logs

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Production Environment Setup](#production-environment-setup)
3. [Configuration Management](#configuration-management)
4. [Deployment Procedure](#deployment-procedure)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Monitoring Setup](#monitoring-setup)
7. [Rollback Procedures](#rollback-procedures)
8. [Disaster Recovery](#disaster-recovery)

---

## Pre-Deployment Checklist

### 1.1 Mandatory Requirements

**Before ANY production deployment, verify:**

- [ ] All tests passing in CI/CD (100% pass rate)
- [ ] Code review approved by 2+ senior developers
- [ ] Security scan passed (no critical vulnerabilities)
- [ ] Performance testing completed
- [ ] Staging deployment successful and verified
- [ ] Database backup created and verified
- [ ] Rollback plan documented and tested
- [ ] Deployment window scheduled and approved
- [ ] Stakeholders notified
- [ ] On-call engineer available
- [ ] Monitoring dashboards ready
- [ ] Incident response plan ready

### 1.2 Deployment Window

**Recommended Times:**
- **Low Traffic:** 2:00 AM - 4:00 AM (Local Time)
- **Weekend:** Saturday 1:00 AM - 3:00 AM
- **Emergency:** Only with CTO approval

**Duration:** 2-4 hours (including verification)

---

## Production Environment Setup

### 2.1 Infrastructure Requirements

**Minimum Specifications:**
- **Application Servers:** 2+ (Load Balanced)
  - CPU: 8 cores
  - RAM: 16GB
  - Storage: 100GB SSD
  
- **Database Server:**
  - CPU: 8 cores
  - RAM: 32GB
  - Storage: 500GB SSD (with backups)
  
- **Redis Server:**
  - CPU: 4 cores
  - RAM: 8GB
  - Storage: 50GB SSD

**High Availability:**
- Load balancer (HAProxy/Nginx)
- Database replication (Master-Slave)
- Redis cluster
- CDN for static assets

### 2.2 Security Requirements

- [ ] SSL/TLS certificates installed
- [ ] Firewall rules configured
- [ ] DDoS protection enabled
- [ ] WAF (Web Application Firewall) configured
- [ ] Secrets management system (HashiCorp Vault/AWS Secrets Manager)
- [ ] Access control (SSH keys, no passwords)
- [ ] Audit logging enabled

---

## Configuration Management

### 3.1 Environment Variables

**⚠️ NEVER commit production secrets to version control**

Use secrets management system:

```bash
# Example: Using AWS Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id saleor/production/config \
  --query SecretString \
  --output text > .env.production
```

**Required Variables:**
```bash
# Database (Production)
DATABASE_URL=postgresql://user:password@prod-db:5432/saleor_prod
POSTGRES_DB=saleor_prod

# Redis (Production)
REDIS_URL=redis://prod-redis:6379/0

# Application
SECRET_KEY=<strong-secret-key-256-bits>
ALLOWED_HOSTS=example.com,api.example.com,www.example.com
DEBUG=False

# Email (Production SMTP)
EMAIL_HOST=smtp.production.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Payment Gateway (Production)
PAYMENT_GATEWAY_API_KEY=<production-api-key>
PAYMENT_GATEWAY_MODE=production

# Monitoring
SENTRY_DSN=<sentry-dsn>
DATADOG_API_KEY=<datadog-key>

# CDN
STATIC_URL=https://cdn.example.com/static/
MEDIA_URL=https://cdn.example.com/media/
```

### 3.2 Docker Configuration

**Production docker-compose.yml:**

```yaml
version: '3.8'

services:
  web:
    image: ${DOCKERHUB_USERNAME}/saleor:production-${VERSION}
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## Deployment Procedure

### 4.1 Phase 1: Preparation (30 minutes)

```bash
# 1. Create deployment branch
git checkout -b production-deploy-$(date +%Y%m%d)

# 2. Tag release
git tag -a v$(date +%Y%m%d) -m "Production release $(date +%Y%m%d)"

# 3. Push tag
git push origin v$(date +%Y%m%d)

# 4. Verify CI/CD pipeline completed successfully
# Check GitHub Actions: https://github.com/your-repo/actions
```

### 4.2 Phase 2: Database Migration (15 minutes)

```bash
# 1. Create database backup
pg_dump -h prod-db -U saleor -d saleor_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Verify backup
ls -lh backup_*.sql

# 3. Run migrations in dry-run mode first
docker run --rm \
  --env-file .env.production \
  --network saleor-prod_default \
  ${DOCKERHUB_USERNAME}/saleor:production-${VERSION} \
  python manage.py migrate --plan

# 4. Execute migrations
docker run --rm \
  --env-file .env.production \
  --network saleor-prod_default \
  ${DOCKERHUB_USERNAME}/saleor:production-${VERSION} \
  python manage.py migrate
```

### 4.3 Phase 3: Blue-Green Deployment (45 minutes)

**Strategy:** Deploy to new environment, verify, then switch traffic

```bash
# 1. Deploy to green environment
docker compose -f docker-compose.prod-green.yml up -d

# 2. Wait for health checks
sleep 60

# 3. Verify green environment
curl https://green.example.com/health/
# Run smoke tests

# 4. Switch load balancer to green
# Update load balancer configuration
# Gradually shift traffic: 10% → 50% → 100%

# 5. Monitor for 30 minutes
# Check error rates, response times, user reports

# 6. If stable, keep green. If issues, rollback to blue
```

### 4.4 Phase 4: Post-Deployment (30 minutes)

```bash
# 1. Verify all services
docker compose -f docker-compose.prod.yml ps

# 2. Check application logs
docker compose -f docker-compose.prod.yml logs --tail=100 web

# 3. Run health checks
./scripts/health-check.sh

# 4. Verify monitoring
# Check Sentry, DataDog, application metrics
```

---

## Post-Deployment Verification

### 5.1 Automated Health Checks

```bash
#!/bin/bash
# health-check.sh

ENDPOINTS=(
  "https://example.com/health/"
  "https://api.example.com/graphql/"
  "https://example.com/api/status/"
)

for endpoint in "${ENDPOINTS[@]}"; do
  response=$(curl -s -o /dev/null -w "%{http_code}" "$endpoint")
  if [ "$response" -eq 200 ]; then
    echo "✅ $endpoint - OK"
  else
    echo "❌ $endpoint - FAILED ($response)"
    exit 1
  fi
done
```

### 5.2 Functional Verification

**Critical Paths:**
- [ ] User registration works
- [ ] User login works
- [ ] Product browsing works
- [ ] Add to cart works
- [ ] Checkout process works
- [ ] Payment processing works
- [ ] Order confirmation sent
- [ ] Admin panel accessible

### 5.3 Performance Verification

**Metrics to Monitor:**
- Response time: < 200ms (p95)
- Error rate: < 0.1%
- CPU usage: < 70%
- Memory usage: < 80%
- Database connections: < 80% of max

### 5.4 Security Verification

- [ ] SSL certificates valid
- [ ] No exposed sensitive data
- [ ] Authentication working
- [ ] Authorization enforced
- [ ] Security headers present

---

## Monitoring Setup

### 6.1 Application Monitoring

**Tools:**
- **Sentry:** Error tracking
- **DataDog/New Relic:** APM and metrics
- **Prometheus + Grafana:** Custom metrics

**Key Metrics:**
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Database query performance
- Cache hit rate

### 6.2 Infrastructure Monitoring

**Tools:**
- **CloudWatch/DataDog:** Infrastructure metrics
- **Pingdom/UptimeRobot:** Uptime monitoring

**Key Metrics:**
- Server CPU/Memory/Disk
- Network traffic
- Database performance
- Redis performance

### 6.3 Alert Configuration

**Critical Alerts:**
- Error rate > 1%
- Response time > 1s (p95)
- Server CPU > 90%
- Database connections > 90%
- Disk space < 20%

**Alert Channels:**
- PagerDuty for critical
- Slack for warnings
- Email for info

---

## Rollback Procedures

### 7.1 Immediate Rollback (< 5 minutes)

**Trigger:** Critical bug affecting users

```bash
# 1. Switch load balancer back to blue
# Update load balancer config immediately

# 2. Stop green environment
docker compose -f docker-compose.prod-green.yml down

# 3. Verify blue is serving traffic
curl https://example.com/health/

# 4. Notify team
# Send alert to team channel
```

### 7.2 Database Rollback

**If database migration caused issues:**

```bash
# 1. Stop application
docker compose -f docker-compose.prod.yml stop web

# 2. Restore database
psql -h prod-db -U saleor -d saleor_prod < backup_YYYYMMDD_HHMMSS.sql

# 3. Verify database
psql -h prod-db -U saleor -d saleor_prod -c "SELECT COUNT(*) FROM orders;"

# 4. Restart with previous version
# Update docker-compose to use previous image tag
docker compose -f docker-compose.prod.yml up -d
```

### 7.3 Complete Rollback

**If entire deployment needs rollback:**

```bash
# 1. Revert to previous Git tag
git checkout v<previous-version>

# 2. Pull previous Docker image
docker pull ${DOCKERHUB_USERNAME}/saleor:production-<previous-version>

# 3. Update docker-compose
# Change image tag to previous version

# 4. Restart services
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d

# 5. Verify
./scripts/health-check.sh
```

---

## Disaster Recovery

### 8.1 Backup Strategy

**Database Backups:**
- **Frequency:** Every 6 hours
- **Retention:** 30 days
- **Location:** S3/Cloud Storage
- **Verification:** Weekly restore tests

**Application Backups:**
- **Docker Images:** Tagged and stored in registry
- **Configuration:** Version controlled
- **Static Files:** CDN with versioning

### 8.2 Recovery Procedures

**Complete System Failure:**

1. **Assess Damage:** Determine scope of failure
2. **Activate DR Site:** If available
3. **Restore Database:** From latest backup
4. **Deploy Application:** Latest stable version
5. **Verify Functionality:** Run health checks
6. **Gradual Traffic:** Ramp up gradually

**Data Corruption:**

1. **Stop Application:** Prevent further corruption
2. **Identify Corruption:** Analyze logs
3. **Restore from Backup:** Latest clean backup
4. **Verify Data Integrity:** Run data validation
5. **Resume Operations:** With monitoring

---

## Post-Deployment Checklist

### 9.1 Immediate (First Hour)

- [ ] All health checks passing
- [ ] No critical errors in logs
- [ ] Performance metrics normal
- [ ] User reports: No issues
- [ ] Monitoring dashboards updated

### 9.2 Short Term (First 24 Hours)

- [ ] Monitor error rates
- [ ] Review performance metrics
- [ ] Check user feedback
- [ ] Verify all integrations
- [ ] Update deployment log

### 9.3 Long Term (First Week)

- [ ] Performance stable
- [ ] No recurring issues
- [ ] User satisfaction maintained
- [ ] Cost analysis (if applicable)
- [ ] Lessons learned documented

---

## Emergency Contacts

**On-Call Engineer:** [Phone]  
**DevOps Lead:** [Phone]  
**CTO:** [Phone]  
**Incident Response:** [Slack Channel]

---

**⚠️ REMEMBER:**
- Never deploy without approval
- Always have rollback ready
- Monitor continuously
- Document everything

---

**Last Updated:** December 7, 2025  
**Classification:** CONFIDENTIAL  
**Next Review:** [TBD]

