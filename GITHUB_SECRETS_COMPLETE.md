# 🔐 Complete GitHub Secrets Setup Guide

**Date:** 2025-12-04  
**Project:** SQE Project - Saleor CI/CD  
**Status:** ✅ **READY TO CONFIGURE**

---

## 📋 Required Secrets

You need to add **2 secrets** to your GitHub repository:

| Secret Name | Value | Purpose |
|------------|-------|---------|
| `CYPRESS_RECORD_KEY` | `8d5f0fe8-0c32-4259-8073-86ef9b7ac337` | Cypress test recording |
| `DOCKER_HUB_TOKEN` | `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY` | Docker Hub authentication |

---

## 🚀 Step-by-Step: Add Secrets to GitHub

### **Step 1: Go to GitHub Secrets Page**

1. Open your repository: `https://github.com/Haroon2697/SQE_Project_Saleor`
2. Click **"Settings"** (top menu)
3. Click **"Secrets and variables"** (left sidebar)
4. Click **"Actions"**
5. Click **"New repository secret"**

**Direct URL:**
```
https://github.com/Haroon2697/SQE_Project_Saleor/settings/secrets/actions
```

---

### **Step 2: Add CYPRESS_RECORD_KEY**

1. **Name:** `CYPRESS_RECORD_KEY`
2. **Secret:** `8d5f0fe8-0c32-4259-8073-86ef9b7ac337`
3. Click **"Add secret"**

---

### **Step 3: Add DOCKER_HUB_TOKEN**

1. Click **"New repository secret"** again
2. **Name:** `DOCKER_HUB_TOKEN`
3. **Secret:** `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY`
4. Click **"Add secret"**

---

## ✅ Verification

After adding both secrets, you should see:

```
Repository secrets
├── CYPRESS_RECORD_KEY        (Updated X minutes ago)
└── DOCKER_HUB_TOKEN          (Updated X minutes ago)
```

---

## 📊 What Each Secret Does

### **CYPRESS_RECORD_KEY**

**Purpose:** Allows Cypress to record test runs to Cypress Dashboard

**Used in:**
- Test Stage (UI Tests)
- Records test execution videos and results
- Project ID: `rpaahx`

**Where it's used:**
```yaml
# .github/workflows/cicd-pipeline.yml
env:
  CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
```

---

### **DOCKER_HUB_TOKEN**

**Purpose:** Authenticates with Docker Hub to push/pull Docker images

**Used in:**
- Staging Stage (Docker build & push)
- Deploy Stage (Production Docker build & push)

**Docker Hub Details:**
- Username: `haroon5295`
- Token: `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY`
- Permissions: Read & Write
- Expires: Jan 03, 2026

**Where it's used:**
```yaml
# .github/workflows/cicd-pipeline.yml
- name: "🐳 Login to Docker Hub"
  run: |
    echo "${{ secrets.DOCKER_HUB_TOKEN }}" | docker login -u haroon5295 --password-stdin
```

---

## 🎯 Quick Reference

### **Secret 1: CYPRESS_RECORD_KEY**

```
Name: CYPRESS_RECORD_KEY
Value: 8d5f0fe8-0c32-4259-8073-86ef9b7ac337
```

### **Secret 2: DOCKER_HUB_TOKEN**

```
Name: DOCKER_HUB_TOKEN
Value: dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY
```

---

## 🔧 Optional: Additional Secrets

### **DJANGO_SECRET_KEY (Optional but Recommended)**

If you want to use your own secret key instead of the fallback:

```
Name: DJANGO_SECRET_KEY
Value: [Your secret key from .env file]
```

**Current fallback:** `test-secret-key-for-ci` (works without this secret)

---

## 📝 Visual Guide

```
GitHub Repository
  └── Settings
      └── Secrets and variables
          └── Actions
              └── [New repository secret]
                  
                  Secret 1:
                  ┌─────────────────────────────────────┐
                  │ Name: CYPRESS_RECORD_KEY              │
                  │ Secret: 8d5f0fe8-0c32-4259-8073...   │
                  │ [Add secret]                         │
                  └─────────────────────────────────────┘
                  
                  Secret 2:
                  ┌─────────────────────────────────────┐
                  │ Name: DOCKER_HUB_TOKEN                │
                  │ Secret: dckr_pat_9MKc91ToLqs5pq...     │
                  │ [Add secret]                         │
                  └─────────────────────────────────────┘
```

---

## ✅ Checklist

- [ ] Opened GitHub repository settings
- [ ] Went to Secrets and variables → Actions
- [ ] Added `CYPRESS_RECORD_KEY` with value `8d5f0fe8-0c32-4259-8073-86ef9b7ac337`
- [ ] Added `DOCKER_HUB_TOKEN` with value `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY`
- [ ] Verified both secrets appear in the list
- [ ] (Optional) Added `DJANGO_SECRET_KEY` if desired

---

## 🚀 After Adding Secrets

### **1. Test the Pipeline**

Push a commit to trigger the pipeline:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
git add .
git commit -m "Add Cypress and Docker Hub secrets configuration"
git push origin main
```

### **2. Check GitHub Actions**

1. Go to: `https://github.com/Haroon2697/SQE_Project_Saleor/actions`
2. Click on the latest workflow run
3. Verify:
   - ✅ Cypress tests run with recording
   - ✅ Docker images build and push to Docker Hub

---

## 🔒 Security Notes

### **Token Security:**

1. **Never commit secrets to git** - They're stored securely in GitHub
2. **Tokens are masked in logs** - GitHub hides them automatically
3. **Docker token expires:** Jan 03, 2026 - Renew before expiration
4. **Cypress key is permanent** - No expiration

### **Token Permissions:**

- **DOCKER_HUB_TOKEN:** Read & Write (can push/pull images)
- **CYPRESS_RECORD_KEY:** Record test runs (read-only for dashboard)

---

## 📊 Expected Pipeline Behavior

### **With Secrets:**

✅ **Test Stage:**
- Cypress tests run with recording
- Results visible in Cypress Dashboard
- Videos and screenshots uploaded

✅ **Staging Stage:**
- Docker image built
- Image pushed to: `haroon5295/saleor-staging:latest`
- Available on Docker Hub

✅ **Deploy Stage:**
- Production Docker image built
- Image pushed to: `haroon5295/saleor-prod:latest`
- Available on Docker Hub

### **Without Secrets:**

⚠️ **Test Stage:**
- Cypress tests run without recording
- No dashboard upload

⚠️ **Staging/Deploy Stages:**
- Docker images built locally
- Not pushed to Docker Hub

---

## 🎉 Summary

**Required Secrets:**
1. ✅ `CYPRESS_RECORD_KEY` - For Cypress test recording
2. ✅ `DOCKER_HUB_TOKEN` - For Docker Hub authentication

**Optional Secrets:**
- `DJANGO_SECRET_KEY` - For custom Django secret (has fallback)

**Next Steps:**
1. Add both secrets to GitHub
2. Push code to trigger pipeline
3. Verify secrets are working in Actions logs

---

**Last Updated:** 2025-12-04  
**Status:** ✅ **READY TO CONFIGURE**

