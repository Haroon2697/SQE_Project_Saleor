# 🚀 CI/CD Pipeline Setup Guide

**Quick Start Guide for Setting Up Your CI/CD Pipeline**

---

## ✅ What's Already Done

1. ✅ **Pipeline files created:**
   - `.github/workflows/cicd-pipeline.yml` - Complete 5-stage pipeline
   - `.github/workflows/ci.yml` - Simplified CI pipeline

2. ✅ **Test files ready:**
   - 14 tests written and passing
   - Coverage reports configured

3. ✅ **Documentation created:**
   - `CICD_PIPELINE_DOCUMENTATION.md` - Full documentation

---

## 🎯 Step-by-Step Setup

### **Step 1: Push Your Code to GitHub**

```bash
cd ~/SQE/SQE_Project_Saleor

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Saleor SQE project with CI/CD pipeline"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR_USERNAME` - Your GitHub username
- `YOUR_REPO` - Your repository name

---

### **Step 2: Configure GitHub Secrets (Optional but Recommended)**

1. Go to your GitHub repository
2. Click: **Settings → Secrets and variables → Actions**
3. Click: **New repository secret**

**Add these secrets:**

#### **Secret 1: `DJANGO_SECRET_KEY`**
- **Name:** `DJANGO_SECRET_KEY`
- **Value:** Your secret key (from `.env` file)
- **Example:** `PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA`

#### **Secret 2: `DATABASE_URL`** (Optional - for staging/production)
- **Name:** `DATABASE_URL`
- **Value:** Your production database URL
- **Example:** `postgres://user:pass@host:5432/dbname`

---

### **Step 3: Trigger the Pipeline**

**Option A: Automatic (Recommended)**
- Just push code to `main` branch:
  ```bash
  git add .
  git commit -m "Update tests"
  git push origin main
  ```

**Option B: Manual Trigger**
1. Go to: **GitHub → Actions tab**
2. Select: **"Saleor CI/CD Pipeline - Complete"**
3. Click: **"Run workflow"**
4. Select branch: **main**
5. Click: **"Run workflow"**

---

### **Step 4: View Pipeline Execution**

1. Go to: **GitHub → Actions tab**
2. Click on the running workflow
3. Watch each stage execute:
   - 🔨 Build Stage
   - 🧪 Test Stage
   - 🚀 Staging Stage
   - 🌐 Deploy Stage

---

### **Step 5: Check Results**

#### **Test Results:**
- **Location:** Actions tab → Workflow run → Test Stage
- **Coverage:** Download artifacts → `htmlcov/index.html`

#### **Pipeline Status:**
- ✅ Green checkmark = Success
- ❌ Red X = Failure (check logs)

---

## 🔧 Customization

### **Update Staging/Production URLs:**

Edit `.github/workflows/cicd-pipeline.yml`:

```yaml
environment:
  name: staging
  url: https://your-staging-url.com  # ← Change this
```

```yaml
environment:
  name: production
  url: https://your-production-url.com  # ← Change this
```

---

## 📊 Expected Pipeline Output

### **Successful Pipeline Run:**

```
✅ Source Stage: Code checked out
✅ Build Stage: Dependencies installed
✅ Test Stage: 14 tests passed
✅ Staging Stage: Deployed to staging
✅ Deploy Stage: Production deployment
```

### **Test Results:**

```
============================= test session starts ==============================
collected 14 items

tests/integration/test_api.py ....                                       [ 28%]
tests/unit/test_models.py ......                                         [ 71%]
tests/integration/test_api.py ..                                         [ 85%]
tests/test_basic.py ..                                                   [100%]

================== 14 passed, 3 warnings in 243.40s ==================
```

---

## ⚠️ Troubleshooting

### **Pipeline Fails at Build Stage:**

**Problem:** Dependencies not installing

**Solution:**
- Check Python version compatibility
- Verify `pyproject.toml` is correct
- Check build logs for specific errors

### **Pipeline Fails at Test Stage:**

**Problem:** Tests failing

**Solution:**
- Run tests locally first: `pytest tests/ -v`
- Check database connection
- Verify environment variables

### **Pipeline Fails at Staging/Deploy:**

**Problem:** Deployment failing

**Solution:**
- Update URLs in workflow file
- Configure Docker if needed
- Check deployment permissions

---

## 🎯 Quick Commands

### **Test Pipeline Locally (Before Pushing):**

```bash
# Run tests locally
cd ~/SQE/SQE_Project_Saleor
source .venv/bin/activate
pytest tests/ -v

# Check coverage
pytest tests/ --cov=saleor --cov-report=html
```

### **View Pipeline in GitHub:**

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Click on latest workflow run
3. View each stage

---

## 📝 Next Steps

1. **Push code to GitHub** ✅
2. **Configure secrets** (optional)
3. **Trigger pipeline** ✅
4. **Review results** ✅
5. **Add UI tests** (Cypress) - Next phase
6. **Configure staging environment** - If needed
7. **Configure production environment** - If needed

---

## 🎉 Success Criteria

Your pipeline is working when:

- ✅ Pipeline runs automatically on push
- ✅ All tests pass (14/14)
- ✅ Coverage report generated
- ✅ Artifacts uploaded
- ✅ Pipeline completes in ~15-20 minutes

---

**Ready to push and test!** 🚀

