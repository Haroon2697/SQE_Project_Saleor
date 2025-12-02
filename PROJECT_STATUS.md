# Software Quality Engineering Project - Status

## Saleor E-commerce Platform Setup

**Date:** 2025-12-02  
**Project:** SQE Testing & CI/CD Implementation  
**Platform:** Saleor 3.23.0

---

## 🎯 PHASE 1: SYSTEM SETUP - COMPLETE ✅

### 1. Environment Setup

- ✅ Python 3.12.3 installed
- ✅ Virtual environment created: `.venv/`
- ✅ All dependencies installed via `pip install .`
- ✅ PostgreSQL database configured
- ✅ Environment variables configured in `.env`

### 2. Saleor Application Status

- **Status:** Ready to run on localhost:8000
- **Database:** PostgreSQL (saleor database)
- **Admin User:** admin@example.com / admin123
- **API:** GraphQL available at `/graphql/`
- **Dashboard:** Available at `/dashboard/`
- **Health Check:** Available at `/health/`

### 3. Issues Resolved

1. ✅ Docker port conflicts (Redis port 6379)
2. ✅ Simplified to manual setup for project needs
3. ✅ Database configured (PostgreSQL)
4. ✅ Environment variables properly loaded via `python-dotenv`
5. ✅ `SECRET_KEY` configured and working
6. ✅ `manage.py` updated to auto-load `.env` file

### 4. Access Information

**Application URL:** http://localhost:8000

**Endpoints:**
- GraphQL API: http://localhost:8000/graphql
- Admin Panel: http://localhost:8000/dashboard
- Health Check: http://localhost:8000/health/

**Admin Credentials:**
- Email: `admin@example.com`
- Password: `admin123`

---

## 🚀 QUICK START COMMANDS

### Start Services (Run these before starting Saleor):

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Start Redis (optional, but recommended)
sudo systemctl start redis-server
```

### Start Saleor:

```bash
cd ~/SQE/SQE_Project_Saleor
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Or use the setup script:

```bash
cd ~/SQE/SQE_Project_Saleor
chmod +x setup_saleor.sh
./setup_saleor.sh
```

---

## 📝 CONFIGURATION FILES

### `.env` File Location:
`/home/haroon/SQE/SQE_Project_Saleor/.env`

### Key Environment Variables:
- `DEBUG=True` - Development mode
- `SECRET_KEY` - Django secret key (configured)
- `DATABASE_URL=postgres://saleor:saleor@localhost:5432/saleor`
- `REDIS_URL=redis://localhost:6379/0`
- `EMAIL_URL=console://` - Console email backend for testing

---

## 🧪 NEXT STEPS FOR TESTING

### Phase 2: Write Tests

1. **Backend Tests (White-box)**
   - Location: `saleor/tests/` or create new test files
   - Framework: pytest
   - Examples:
     - GraphQL API tests
     - Authentication tests
     - Product CRUD tests

2. **Frontend Tests (Black-box)**
   - Framework: Cypress
   - Location: To be determined (dashboard/storefront repos)
   - Examples:
     - Login page tests
     - Navigation tests
     - Product browsing tests

### Phase 3: CI/CD Setup

1. **GitHub Actions**
   - Create `.github/workflows/ci.yml`
   - Run pytest tests
   - Run Cypress tests
   - Deploy to staging (optional)

2. **Secrets Configuration**
   - `DJANGO_SECRET_KEY` - Add to GitHub Secrets
   - `DATABASE_URL` - Add to GitHub Secrets (for CI)
   - `REDIS_URL` - Add to GitHub Secrets (if needed)

---

## 📊 SYSTEM REQUIREMENTS

- **OS:** Ubuntu (Linux)
- **Python:** 3.12.3
- **Database:** PostgreSQL 12+
- **Cache:** Redis (optional but recommended)
- **Node.js:** Not required for backend (needed for frontend testing)

---

## ⚠️ KNOWN WARNINGS (Non-Critical)

1. **RSA_PRIVATE_KEY missing** - Using temporary key (OK for development)
2. **pkg_resources deprecation** - From razorpay package (doesn't affect functionality)

---

## 📚 DOCUMENTATION

- **Project Guide:** `/home/haroon/SQE/SQE_PROJECT_GUIDE.md`
- **Saleor Docs:** https://docs.saleor.io/
- **Setup Script:** `setup_saleor.sh`

---

**Last Updated:** 2025-12-02  
**Status:** ✅ Ready for Testing Phase

