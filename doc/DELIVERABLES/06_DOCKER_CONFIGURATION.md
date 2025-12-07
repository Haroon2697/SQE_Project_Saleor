# Deliverable 6: Docker Configuration

## 📋 Overview

**Files:** `Dockerfile`, `.dockerignore`, `docker-compose.*.yml`  
**Type:** Containerization Configuration  
**Purpose:** Dockerize Saleor application for deployment  
**Status:** ✅ Multi-stage Dockerfile, Docker Compose files

---

## 📊 Docker Files

### **1. Dockerfile**
- **Location:** Root directory
- **Type:** Multi-stage build
- **Purpose:** Build optimized Docker image for Saleor

#### **Stage 1: Builder**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
# Install build dependencies
# Copy project files
# Install Python dependencies
```

**Features:**
- Installs gcc, g++, libpq-dev for building Python packages
- Copies `pyproject.toml`, `README.md`, `saleor/`, `manage.py`
- Installs Python dependencies via `pip install .`

#### **Stage 2: Runtime**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
# Install runtime dependencies
# Copy dependencies from builder
# Copy application code
# Create non-root user
```

**Features:**
- Minimal runtime image
- Only runtime dependencies (libpq5, curl)
- Non-root user for security
- Health check configured
- Exposes port 8000

---

### **2. .dockerignore**
- **Location:** Root directory
- **Purpose:** Exclude files from Docker build context

**Excluded:**
- Git files (`.git`, `.gitignore`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`.venv/`, `venv/`)
- Test files (`tests/`, `*.test.py`)
- Documentation (`*.md`, `docs/`)
- CI/CD files (`.github/`)
- **Exception:** `README.md` is included (required by pyproject.toml)

---

### **3. docker-compose.staging.yml**
- **Location:** Root directory
- **Purpose:** Staging environment Docker Compose configuration

**Services:**
- `db` - PostgreSQL database
- `cache` - Redis cache
- `backend` - Saleor backend
- `dashboard` - Saleor dashboard
- `storefront` - Saleor storefront

---

### **4. docker-compose.production.yml**
- **Location:** Root directory
- **Purpose:** Production environment Docker Compose configuration

**Features:**
- Production-optimized configuration
- Resource limits
- Health checks
- Restart policies

---

## 🔧 Docker Build Process

### **Build Command**
```bash
docker build -t haroon5295/saleor:latest .
```

### **Build Steps**
1. **Stage 1 (Builder):**
   - Install system dependencies
   - Copy project files
   - Install Python dependencies
   - Build application

2. **Stage 2 (Runtime):**
   - Copy Python dependencies from builder
   - Copy application code
   - Create non-root user
   - Configure health check

### **Build Time:** ~5-10 minutes

---

## 🚀 Docker Usage

### **Build Image**
```bash
docker build -t haroon5295/saleor:latest .
```

### **Run Container**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgres://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  haroon5295/saleor:latest
```

### **Run with Docker Compose**
```bash
docker-compose -f docker-compose.staging.yml up
```

---

## 📊 Image Details

### **Base Image**
- `python:3.12-slim` - Minimal Python 3.12 image

### **Image Size**
- **Builder Stage:** ~500MB
- **Runtime Stage:** ~200MB (optimized)

### **Ports**
- `8000` - Saleor backend API

### **Health Check**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/graphql/ || exit 1
```

---

## 🔍 Key Features

1. **Multi-stage Build:** Reduces final image size
2. **Security:** Non-root user execution
3. **Health Checks:** Automatic container health monitoring
4. **Optimization:** Minimal dependencies in runtime image
5. **README.md Handling:** Properly included for metadata generation

---

## 🐛 Troubleshooting

### **Build Fails: README.md not found**
- **Fix:** Ensure `README.md` exists in root directory
- **Check:** `.dockerignore` should have `!README.md`

### **Build Fails: metadata-generation-failed**
- **Fix:** Ensure `saleor/` directory and `manage.py` are copied before `pip install .`

### **Image Too Large**
- **Solution:** Multi-stage build already optimizes size
- **Check:** Remove unnecessary files from build context

---

## 📈 Statistics

- **Dockerfile Lines:** 61
- **Build Stages:** 2
- **Docker Compose Files:** 2
- **Services Defined:** 5

---

## 🔗 Related Documentation

- `doc/DOCKER_HUB_SECRET_SETUP.md` - Docker Hub configuration
- `.github/workflows/complete-cicd-pipeline.yml` - CI/CD Docker build

