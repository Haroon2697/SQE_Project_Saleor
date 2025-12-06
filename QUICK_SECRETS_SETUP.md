# 🔐 Quick GitHub Secrets Setup

## ✅ Do You Need Secrets?

**Short Answer:** **NO, but RECOMMENDED**

Your pipeline has **fallback values**, so it will work without secrets. However, adding `DJANGO_SECRET_KEY` is recommended for better security.

---

## 🎯 Required Secret (Recommended)

### **Secret Name:** `DJANGO_SECRET_KEY`

**Why:** Better security, consistent values across pipeline runs

**Status:** ✅ Recommended (not required - has fallback)

---

## 📝 How to Create Secret (Step-by-Step)

### **Step 1: Get Your Secret Key Value**

Run this command:

```bash
cd ~/SQE/SQE_Project_Saleor
cat .env | grep SECRET_KEY
```

**You'll see something like:**
```
SECRET_KEY=PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA
```

**Copy the part AFTER `SECRET_KEY=`** (the long random string)

---

### **Step 2: Go to GitHub Secrets Page**

1. Open your GitHub repository in browser
2. Click **"Settings"** tab (top menu)
3. Click **"Secrets and variables"** (left sidebar)
4. Click **"Actions"**
5. Click **"New repository secret"** button

**Direct URL:**
```
https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions
```

---

### **Step 3: Add the Secret**

1. **Name:** Type exactly: `DJANGO_SECRET_KEY`
   - ⚠️ **Case-sensitive!** Must be exactly as shown

2. **Secret:** Paste your secret key value
   - Example: `PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA`

3. Click **"Add secret"**

---

### **Step 4: Verify**

You should see:
- ✅ `DJANGO_SECRET_KEY` appears in the secrets list
- ✅ Shows "Updated X minutes ago"
- ⚠️ Value is hidden (for security)

---

## 🎯 Visual Guide

```
GitHub Repository
  └── Settings (top menu)
      └── Secrets and variables (left sidebar)
          └── Actions
              └── Repository secrets
                  └── [New repository secret] ← Click here
                      
                      Form appears:
                      ┌─────────────────────────────┐
                      │ Name: DJANGO_SECRET_KEY      │
                      │ Secret: [paste value here]   │
                      │ [Add secret]                │
                      └─────────────────────────────┘
```

---

## ✅ Quick Checklist

- [ ] Opened GitHub repository
- [ ] Went to Settings → Secrets and variables → Actions
- [ ] Clicked "New repository secret"
- [ ] Entered name: `DJANGO_SECRET_KEY`
- [ ] Pasted secret value from `.env` file
- [ ] Clicked "Add secret"
- [ ] Verified secret appears in list

---

## 🔍 How to Verify Secret is Working

### **After Creating Secret:**

1. **Push code to trigger pipeline:**
   ```bash
   git add .
   git commit -m "Test pipeline with secrets"
   git push origin main
   ```

2. **Check pipeline logs:**
   - Go to: **Actions tab** → Click on workflow run
   - Look at "Run migrations" step
   - Should use your secret (not the fallback)

3. **In logs, you'll see:**
   ```
   SECRET_KEY=*** (hidden)
   ```
   Not: `SECRET_KEY=test-secret-key-for-ci`

---

## 📋 Complete Secret List (For Reference)

### **For Your SQE Project (Required):**

| Secret Name | Required? | Value | Purpose |
|------------|-----------|-------|---------|
| `CYPRESS_RECORD_KEY` | ✅ **Required** | `8d5f0fe8-0c32-4259-8073-86ef9b7ac337` | Cypress test recording |
| `DOCKER_HUB_TOKEN` | ✅ **Required** | `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY` | Docker Hub authentication |

### **Optional Secrets:**

| Secret Name | Required? | How to Get Value |
|------------|-----------|------------------|
| `DJANGO_SECRET_KEY` | ⚠️ Optional | From your `.env` file (has fallback) |

### **For Advanced Deployment (Future):**

| Secret Name | When Needed |
|------------|-------------|
| `DATABASE_URL` | If deploying to staging/production |
| `REDIS_URL` | If deploying to staging/production |
| `AWS_ACCESS_KEY_ID` | If deploying to AWS |
| `AWS_SECRET_ACCESS_KEY` | If deploying to AWS |

**For your SQE project, you only need `DJANGO_SECRET_KEY`!**

---

## 🚀 Quick Command to Get Your Secret Key

```bash
cd ~/SQE/SQE_Project_Saleor
cat .env | grep SECRET_KEY | cut -d'=' -f2
```

This will output just the secret key value (copy this).

---

## ❓ FAQ

### **Q: What if I don't create the secret?**
**A:** Pipeline will still work! It uses fallback: `test-secret-key-for-ci`

### **Q: Can I see the secret after saving?**
**A:** No, GitHub hides it for security. You can only update or delete it.

### **Q: What if I make a typo in the secret name?**
**A:** Pipeline will use fallback value. Check spelling: `DJANGO_SECRET_KEY` (exact match)

### **Q: Can I update the secret later?**
**A:** Yes! Click on secret name → Click "Update" → Enter new value

---

## 🎉 Summary

**For your SQE project:**

1. ✅ **Create ONE secret:** `DJANGO_SECRET_KEY`
2. ✅ **Get value from:** Your `.env` file
3. ✅ **Add in GitHub:** Settings → Secrets → Actions
4. ✅ **Done!** Pipeline will use it automatically

**The pipeline works without secrets** (uses defaults), but adding this one secret is recommended! ✅

---

**Need help?** Check `GITHUB_SECRETS_GUIDE.md` for detailed instructions.

