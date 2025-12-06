# 🔍 How to Find Your 5-Stage CI/CD Pipeline in GitHub Actions

**Issue:** You're seeing the default Saleor `publish-main.yml` workflow, but you need to find your custom **5-stage pipeline**.

---

## ✅ Your Custom Pipeline Name

**Workflow Name:** `Saleor CI/CD Pipeline - Complete`

**File:** `.github/workflows/cicd-pipeline.yml`

---

## 📍 Step-by-Step: Finding Your Pipeline

### **Step 1: Go to GitHub Actions**

1. Open your repository: `https://github.com/Haroon2697/SQE_Project_Saleor`
2. Click the **"Actions"** tab (top menu)

### **Step 2: Find Your Custom Workflow**

In the left sidebar, you'll see a list of workflows. Look for:

```
✅ Saleor CI/CD Pipeline - Complete
```

**OR** look for workflows that start with:
- `Saleor CI/CD Pipeline`
- `Saleor CI Pipeline`

### **Step 3: Click on Your Workflow**

Click on **"Saleor CI/CD Pipeline - Complete"** in the left sidebar.

### **Step 4: View Workflow Runs**

You'll see a list of workflow runs. Look for runs with:
- **Name:** "Saleor CI/CD Pipeline - Complete"
- **Trigger:** "push" or "workflow_dispatch"
- **Status:** ✅ Success or ⏳ Running

### **Step 5: Click on a Workflow Run**

Click on any run to see the **5 stages**:

```
┌─────────────────────────────────────┐
│  🔨 Build Stage                     │
│  ✅ Completed                        │
├─────────────────────────────────────┤
│  🧪 Test Stage                      │
│  ✅ Completed                        │
├─────────────────────────────────────┤
│  🚀 Staging Stage                   │
│  ✅ Completed                        │
├─────────────────────────────────────┤
│  🌐 Deploy Stage (Production)       │
│  ✅ Completed                        │
├─────────────────────────────────────┤
│  📋 Pipeline Summary                │
│  ✅ Completed                        │
└─────────────────────────────────────┘
```

---

## 🎯 Visual Guide: What You Should See

### **In GitHub Actions Tab:**

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions                                         │
├─────────────────────────────────────────────────────────┤
│  Left Sidebar:          │  Main Area:                   │
│                        │                               │
│  All workflows         │  [Workflow Runs List]         │
│  ├─ publish-main       │  ┌─────────────────────────┐ │
│  ├─ tests-and-linters  │  │ Saleor CI/CD Pipeline   │ │
│  ├─ ✅ Saleor CI/CD    │  │ - Complete #1            │ │
│  │   Pipeline          │  │ ✅ Success 4m 25s        │ │
│  │   - Complete        │  └─────────────────────────┘ │
│  └─ ...                │                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 If You Don't See Your Pipeline

### **Option 1: Trigger It Manually**

1. Go to: **Actions** tab
2. Click: **"Saleor CI/CD Pipeline - Complete"** (left sidebar)
3. Click: **"Run workflow"** button (top right)
4. Select branch: **main**
5. Click: **"Run workflow"**

### **Option 2: Push a New Commit**

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
git add .
git commit -m "Trigger 5-stage CI/CD pipeline"
git push origin main
```

### **Option 3: Check if Pipeline File Exists**

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
ls -la .github/workflows/cicd-pipeline.yml
```

If it doesn't exist, you need to commit and push it.

---

## ✅ Verify Your Pipeline Has All 5 Stages

When you click on a workflow run, you should see these **5 jobs**:

| Stage | Job Name | Status |
|-------|----------|--------|
| **Stage 1: Source** | (Automatic) | ✅ |
| **Stage 2: Build** | 🔨 Build Stage | ✅ |
| **Stage 3: Test** | 🧪 Test Stage | ✅ |
| **Stage 4: Staging** | 🚀 Staging Stage | ✅ |
| **Stage 5: Deploy** | 🌐 Deploy Stage (Production) | ✅ |
| **Summary** | 📋 Pipeline Summary | ✅ |

---

## 📊 What Each Stage Does

### **Stage 1: Source Stage** ✅
- **Tool:** GitHub Actions (automatic)
- **What it does:** Checks out code from repository
- **Visible as:** "📥 Source Stage - Checkout Code" step

### **Stage 2: Build Stage** ✅
- **Tool:** Python pip, build tools
- **What it does:**
  - Sets up Python 3.12
  - Installs dependencies
  - Creates build artifacts
- **Job:** `build`

### **Stage 3: Test Stage** ✅
- **Tools:** Pytest (backend), Cypress (UI)
- **What it does:**
  - Runs 14 backend tests
  - Runs UI tests (if configured)
  - Generates coverage reports
- **Job:** `test`
- **Services:** PostgreSQL 15, Redis 7

### **Stage 4: Staging Stage** ✅
- **Tool:** Docker
- **What it does:**
  - Builds Docker image
  - Deploys to staging (placeholder)
  - Validates deployment
- **Job:** `staging`
- **Condition:** Only runs on push to `main`/`master`

### **Stage 5: Deploy Stage** ✅
- **Tool:** Docker, monitoring tools
- **What it does:**
  - Builds production Docker image
  - Deploys to production (placeholder)
  - Sets up monitoring
  - Runs health checks
- **Job:** `deploy`
- **Condition:** Only runs after staging, on push to `main`

---

## 🎓 For Your SQE Project Submission

### **Screenshots to Take:**

1. **Pipeline Overview:**
   - Screenshot showing all 5 stages in GitHub Actions
   - Shows: Build → Test → Staging → Deploy → Summary

2. **Build Stage:**
   - Screenshot of Build Stage logs
   - Shows: Dependencies installed, artifacts created

3. **Test Stage:**
   - Screenshot of Test Stage results
   - Shows: 14 tests passed, coverage report

4. **Staging Stage:**
   - Screenshot of Staging Stage
   - Shows: Docker image built, deployment initiated

5. **Deploy Stage:**
   - Screenshot of Deploy Stage
   - Shows: Production deployment, monitoring setup

6. **Pipeline Summary:**
   - Screenshot of final summary
   - Shows: All stages completed successfully

---

## 🔍 Quick Checklist

- [ ] Opened GitHub Actions tab
- [ ] Found "Saleor CI/CD Pipeline - Complete" in left sidebar
- [ ] Clicked on workflow run
- [ ] Verified all 5 stages are visible:
  - [ ] 🔨 Build Stage
  - [ ] 🧪 Test Stage
  - [ ] 🚀 Staging Stage
  - [ ] 🌐 Deploy Stage
  - [ ] 📋 Pipeline Summary
- [ ] All stages show ✅ Success status

---

## ⚠️ Troubleshooting

### **Problem: Pipeline Not Showing in Actions Tab**

**Solution:**
1. Check if file exists: `.github/workflows/cicd-pipeline.yml`
2. Verify it's committed: `git log --oneline .github/workflows/cicd-pipeline.yml`
3. Push to GitHub: `git push origin main`
4. Wait 1-2 minutes for GitHub to detect the workflow

### **Problem: Pipeline Runs But Shows Wrong Stages**

**Solution:**
- Make sure you're looking at the correct workflow run
- The workflow name should be: "Saleor CI/CD Pipeline - Complete"
- Not: "Publish main" or "Tests & Linters"

### **Problem: Only 1-2 Stages Showing**

**Solution:**
- Check the workflow file syntax
- Verify all jobs are defined correctly
- Check if conditions are preventing stages from running
- Look at workflow logs for errors

---

## 📝 Summary

**Your custom 5-stage pipeline is:**
- ✅ File: `.github/workflows/cicd-pipeline.yml`
- ✅ Name: "Saleor CI/CD Pipeline - Complete"
- ✅ Location: GitHub Actions → Left sidebar → "Saleor CI/CD Pipeline - Complete"

**To see it:**
1. Go to Actions tab
2. Find "Saleor CI/CD Pipeline - Complete" in left sidebar
3. Click on it
4. Click on a workflow run
5. You'll see all 5 stages! 🎉

---

**Last Updated:** 2025-12-04

