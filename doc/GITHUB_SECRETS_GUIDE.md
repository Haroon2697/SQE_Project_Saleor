# 🔐 GitHub Secrets Setup Guide

**Complete guide for configuring GitHub Secrets for your CI/CD pipeline**

---

## 📋 Required vs Optional Secrets

### **✅ REQUIRED Secrets (Recommended):**

1. **`DJANGO_SECRET_KEY`** - For secure Django operations
   - **Status:** Recommended (has fallback)
   - **Why:** Better security, consistent across runs

### **⚠️ OPTIONAL Secrets (For Advanced Deployment):**

2. **`DATABASE_URL`** - Production database (if deploying)
3. **`REDIS_URL`** - Production Redis (if deploying)
4. **`AWS_ACCESS_KEY_ID`** - For AWS deployment
5. **`AWS_SECRET_ACCESS_KEY`** - For AWS deployment
6. **`DOCKER_HUB_USERNAME`** - For Docker Hub
7. **`DOCKER_HUB_TOKEN`** - For Docker Hub

---

## 🎯 For Your SQE Project (Minimum Required)

**You only NEED to create ONE secret:**
- **`DJANGO_SECRET_KEY`** (recommended but not required - has fallback)

**The pipeline will work WITHOUT any secrets** (uses default test values), but adding `DJANGO_SECRET_KEY` is recommended for better security.

---

## 📝 Step-by-Step: How to Create GitHub Secrets

### **Method 1: Via GitHub Web Interface (Recommended)**

#### **Step 1: Go to Your Repository**
1. Open your GitHub repository in browser
2. URL: `https://github.com/YOUR_USERNAME/YOUR_REPO`

#### **Step 2: Navigate to Secrets**
1. Click on **"Settings"** tab (top menu)
2. In left sidebar, click: **"Secrets and variables"**
3. Click: **"Actions"**
4. You'll see: **"Repository secrets"** section

#### **Step 3: Add Secret**
1. Click: **"New repository secret"** button
2. Fill in:
   - **Name:** `DJANGO_SECRET_KEY`
   - **Secret:** (paste your secret key - see below)
3. Click: **"Add secret"**

#### **Step 4: Verify**
- You should see `DJANGO_SECRET_KEY` in the list
- Note: You can't see the value after saving (for security)

---

## 🔑 Secret Values to Use

### **Secret 1: `DJANGO_SECRET_KEY`**

**How to Get the Value:**

**Option A: Use Your Existing Key (Recommended)**
```bash
cd ~/SQE/SQE_Project_Saleor
cat .env | grep SECRET_KEY
```

**Option B: Generate a New One**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Example Value:**
```
PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA
```

**In GitHub:**
- **Name:** `DJANGO_SECRET_KEY`
- **Value:** `PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA`

---

## 📸 Visual Guide

### **GitHub Secrets Page Location:**

```
Your Repository
  └── Settings (top menu)
      └── Secrets and variables (left sidebar)
          └── Actions
              └── Repository secrets
                  └── New repository secret (button)
```

### **What You'll See:**

```
┌─────────────────────────────────────┐
│ Repository secrets                   │
├─────────────────────────────────────┤
│ [New repository secret]  ← Click    │
│                                     │
│ Name: DJANGO_SECRET_KEY              │
│ Secret: [hidden value]              │
│ [Add secret]                        │
└─────────────────────────────────────┘
```

---

## ✅ Verification Checklist

After creating secrets:

- [ ] Secret `DJANGO_SECRET_KEY` appears in list
- [ ] Secret name is exactly: `DJANGO_SECRET_KEY` (case-sensitive)
- [ ] Value is 50+ characters long
- [ ] Secret is marked as "Repository secret" (not "Environment secret")

---

## 🚀 Testing Secrets in Pipeline

### **After Creating Secrets:**

1. **Push code to trigger pipeline:**
   ```bash
   git add .
   git commit -m "Test pipeline with secrets"
   git push origin main
   ```

2. **Check pipeline logs:**
   - Go to: **Actions tab**
   - Click on running workflow
   - Check "Run migrations" step
   - Should use your secret (not fallback)

3. **Verify Secret is Used:**
   - In pipeline logs, you should see:
     ```
     SECRET_KEY=*** (hidden for security)
     ```
   - Not: `SECRET_KEY=test-secret-key-for-ci`

---

## 🔒 Security Best Practices

### **DO:**
- ✅ Use strong, random secret keys
- ✅ Keep secrets in GitHub Secrets (not in code)
- ✅ Rotate secrets periodically
- ✅ Use different secrets for staging/production

### **DON'T:**
- ❌ Commit secrets to git
- ❌ Share secrets in chat/email
- ❌ Use simple passwords as secrets
- ❌ Reuse same secret everywhere

---

## 📋 Complete Secret List (For Reference)

### **For Basic CI/CD (Your SQE Project):**

| Secret Name | Required? | Purpose | Example |
|------------|-----------|---------|---------|
| `DJANGO_SECRET_KEY` | Recommended | Django security | `PQDhYBvuP-Sab79...` |

### **For Staging/Production Deployment:**

| Secret Name | Required? | Purpose | Example |
|------------|-----------|---------|---------|
| `DATABASE_URL` | Optional | Production DB | `postgres://user:pass@host:5432/db` |
| `REDIS_URL` | Optional | Production Redis | `redis://host:6379/0` |
| `AWS_ACCESS_KEY_ID` | Optional | AWS deployment | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | Optional | AWS deployment | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |

---

## 🎯 Quick Setup (Copy-Paste Ready)

### **1. Get Your Secret Key:**
```bash
cd ~/SQE/SQE_Project_Saleor
cat .env | grep SECRET_KEY
```

### **2. Create Secret in GitHub:**
1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`
2. Click: **"New repository secret"**
3. **Name:** `DJANGO_SECRET_KEY`
4. **Value:** (paste from step 1)
5. Click: **"Add secret"**

### **3. Done!** ✅

---

## ❓ FAQ

### **Q: Do I need secrets for the pipeline to work?**
**A:** No! The pipeline has fallback values. But using secrets is recommended for security.

### **Q: Can I see the secret value after saving?**
**A:** No, GitHub hides it for security. You can only update or delete it.

### **Q: What if I forget the secret value?**
**A:** Generate a new one and update it in GitHub Secrets.

### **Q: Can I use the same secret for staging and production?**
**A:** Technically yes, but it's better to use different secrets for each environment.

### **Q: How do I update a secret?**
**A:** Go to Secrets page → Click on secret name → Click "Update" → Enter new value.

---

## 🎉 Summary

**For your SQE project, you need:**

1. ✅ **Create ONE secret:** `DJANGO_SECRET_KEY`
2. ✅ **Get value from:** Your `.env` file
3. ✅ **Add in GitHub:** Settings → Secrets → Actions → New secret
4. ✅ **Done!** Pipeline will use it automatically

**The pipeline will work without secrets** (uses defaults), but adding `DJANGO_SECRET_KEY` is the recommended minimum.

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Ready to Configure

