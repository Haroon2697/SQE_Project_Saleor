# Deliverable 7: Configuration Files

## 📋 Overview

**Files:** `cypress.config.js`, `package.json`, `pyproject.toml`, `setup.cfg`  
**Type:** Application and Tool Configuration  
**Purpose:** Configure testing tools, dependencies, and project settings  
**Status:** ✅ All Configuration Files Present

---

## 📊 Configuration Files

### **1. cypress.config.js**
- **Location:** Root directory
- **Purpose:** Cypress E2E testing configuration

**Configuration:**
```javascript
{
  e2e: {
    baseUrl: 'http://localhost:9000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000
  },
  projectId: 'rpaahx'
}
```

**Key Settings:**
- **Base URL:** Dashboard URL (port 9000)
- **Viewport:** 1280x720
- **Video Recording:** Enabled
- **Screenshots:** On failure
- **Timeouts:** 10 seconds
- **Project ID:** Cypress Dashboard project ID

---

### **2. package.json**
- **Location:** Root directory
- **Purpose:** Node.js dependencies and scripts

**Dependencies:**
- `cypress: ^15.7.1` - E2E testing framework
- `@cypress/github-action: ^6.10.4` - GitHub Actions integration
- `release-it: ^19.0.4` - Release management

**Scripts:**
- `cypress:open` - Open Cypress in interactive mode
- `cypress:run` - Run Cypress in headless mode
- `cypress:run:record` - Run with recording
- `start:servers` - Start servers for Cypress

---

### **3. pyproject.toml**
- **Location:** Root directory
- **Purpose:** Python project configuration and dependencies

**Key Sections:**
- `[build-system]` - Build backend (hatchling)
- `[project]` - Project metadata
- `[project.dependencies]` - Python dependencies
- `[tool.pytest.ini_options]` - Pytest configuration

**Dependencies:**
- Django 5.2.8
- PostgreSQL adapter (psycopg)
- Testing frameworks (pytest, pytest-django)
- Coverage tools (pytest-cov, coverage)

---

### **4. setup.cfg**
- **Location:** Root directory
- **Purpose:** Additional Python tool configuration

**Sections:**
- `[pytest]` - Pytest settings
- `[coverage:run]` - Coverage settings
- `[coverage:report]` - Coverage reporting

---

### **5. .env (Example)**
- **Location:** Root directory (not committed)
- **Purpose:** Environment variables configuration

**Key Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Django secret key
- `REDIS_URL` - Redis connection string
- `DEBUG` - Debug mode flag
- `ALLOWED_HOSTS` - Allowed hostnames

---

## 🔧 Configuration Details

### **Cypress Configuration**
- **Base URL:** Points to dashboard (port 9000)
- **Timeouts:** Configured for slow networks
- **Recording:** Enabled for CI/CD
- **Project ID:** For Cypress Dashboard integration

### **Python Configuration**
- **Python Version:** 3.12
- **Dependencies:** Managed via pyproject.toml
- **Testing:** Pytest with Django plugin
- **Coverage:** pytest-cov for coverage reports

### **Node.js Configuration**
- **Node Version:** >=20 <22
- **Package Manager:** npm or pnpm
- **Testing:** Cypress for E2E tests

---

## 🚀 Usage

### **Install Python Dependencies**
```bash
pip install .
```

### **Install Node.js Dependencies**
```bash
npm install
```

### **Run Cypress**
```bash
npm run cypress:open
```

### **Run Pytest**
```bash
pytest tests/
```

---

## 📊 Configuration Statistics

- **Configuration Files:** 5
- **Cypress Settings:** 10+
- **Python Dependencies:** 100+
- **Node.js Dependencies:** 4

---

## 🔗 Related Documentation

- `CYPRESS_SETUP_GUIDE.md` - Cypress configuration guide
- `doc/COVERAGE_AND_TESTING_SETUP.md` - Coverage configuration
- `doc/DOCKER_HUB_SECRET_SETUP.md` - Secret configuration

