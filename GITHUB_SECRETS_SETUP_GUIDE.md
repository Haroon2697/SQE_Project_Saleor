# 🔐 GitHub Secrets Setup Guide

**Complete step-by-step instructions for setting up all required GitHub Secrets for the CI/CD pipeline.**

---

## 📋 Required GitHub Secrets

Your CI/CD pipeline needs these secrets:

1. **`DJANGO_SECRET_KEY`** - Django secret key (REQUIRED)
2. **`DOCKER_HUB_USERNAME`** - Docker Hub username (REQUIRED)
3. **`DOCKER_HUB_TOKEN`** - Docker Hub personal access token (REQUIRED)
4. **`CYPRESS_RECORD_KEY`** - Cypress recording key (OPTIONAL)

---

## 🔑 Step 1: Get Django SECRET_KEY

### **Option A: Generate a New SECRET_KEY**

Run this command in your terminal:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Example output:**
```
PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA
```

**Copy this value** - you'll need it for GitHub Secrets.

---

### **Option B: Find Existing SECRET_KEY**

If you already have a SECRET_KEY in your `.env` file:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
cat .env | grep SECRET_KEY
```

**Or check your `.env` file:**
```bash
nano .env
# Look for: SECRET_KEY=...
```

**If you find it, copy the value after `SECRET_KEY=`**

---

### **Option C: Generate Using Python Script**

Create a simple script to generate it:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
python3 << EOF
import secrets
key = secrets.token_urlsafe(50)
print(f"SECRET_KEY={key}")
EOF
```

---

## 🐳 Step 2: Get Docker Hub Credentials

### **DOCKER_HUB_USERNAME**

Your Docker Hub username is: **`haroon5295`**

(You already provided this earlier)

---

### **DOCKER_HUB_TOKEN**

Your Docker Hub personal access token is: **`dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY`**

(You already provided this earlier)

**⚠️ Important:** If you need to generate a new token:

1. Go to: https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Give it a name (e.g., "GitHub Actions")
4. Set permissions: **Read & Write**
5. Click "Generate"
6. **Copy the token immediately** (you won't see it again!)

---

## 🎨 Step 3: Get Cypress Record Key (Optional)

Your Cypress record key is: **`8d5f0fe8-0c32-4259-8073-86ef9b7ac337`**

(You already provided this earlier)

**Project ID:** `rpaahx`

---

## 📝 Step 4: Add Secrets to GitHub

### **Method 1: Using GitHub Web Interface (Recommended)**

1. **Go to your repository:**
   - Open: https://github.com/Haroon2697/SQE_Project_Saleor

2. **Navigate to Settings:**
   - Click on **"Settings"** tab (top menu)
   - In the left sidebar, click **"Secrets and variables"**
   - Click **"Actions"**

3. **Add each secret:**
   - Click **"New repository secret"** button
   - Enter the secret name and value
   - Click **"Add secret"**

4. **Add these secrets one by one:**

   **Secret 1: DJANGO_SECRET_KEY**
   - Name: `DJANGO_SECRET_KEY`
   - Value: `[Your generated SECRET_KEY from Step 1]`
   - Click "Add secret"

   **Secret 2: DOCKER_HUB_USERNAME**
   - Name: `DOCKER_HUB_USERNAME`
   - Value: `haroon5295`
   - Click "Add secret"

   **Secret 3: DOCKER_HUB_TOKEN**
   - Name: `DOCKER_HUB_TOKEN`
   - Value: `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY`
   - Click "Add secret"

   **Secret 4: CYPRESS_RECORD_KEY (Optional)**
   - Name: `CYPRESS_RECORD_KEY`
   - Value: `8d5f0fe8-0c32-4259-8073-86ef9b7ac337`
   - Click "Add secret"

---

### **Method 2: Using GitHub CLI (Advanced)**

If you have GitHub CLI installed:

```bash
# Set secrets via CLI
gh secret set DJANGO_SECRET_KEY --body "YOUR_SECRET_KEY_HERE"
gh secret set DOCKER_HUB_USERNAME --body "haroon5295"
gh secret set DOCKER_HUB_TOKEN --body "dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY"
gh secret set CYPRESS_RECORD_KEY --body "8d5f0fe8-0c32-4259-8073-86ef9b7ac337"
```

---

## ✅ Step 5: Verify Secrets Are Added

1. Go to: https://github.com/Haroon2697/SQE_Project_Saleor/settings/secrets/actions
2. You should see all 4 secrets listed:
   - ✅ `DJANGO_SECRET_KEY`
   - ✅ `DOCKER_HUB_USERNAME`
   - ✅ `DOCKER_HUB_TOKEN`
   - ✅ `CYPRESS_RECORD_KEY` (optional)

**Note:** You won't be able to see the values (they're hidden for security), but you'll see the names.

---

## 🚀 Step 6: Test the Pipeline

After adding secrets, trigger the pipeline:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
git add .
git commit -m "feat: Add CI/CD pipeline configuration"
git push origin main
```

Then check:
- Go to: https://github.com/Haroon2697/SQE_Project_Saleor/actions
- Click on the latest workflow run
- Verify all stages execute successfully

---

## 📸 Visual Guide

### **Step-by-Step Screenshots Guide:**

1. **Go to Repository Settings:**
   ```
   Repository → Settings → Secrets and variables → Actions
   ```

2. **Click "New repository secret":**
   - Button is on the right side

3. **Enter Secret Name and Value:**
   ```
   Name: DJANGO_SECRET_KEY
   Secret: [paste your generated key]
   ```

4. **Click "Add secret"**

5. **Repeat for all secrets**

---

## 🔍 Quick Reference

### **All Secrets Summary:**

| Secret Name | Value | Required | Source |
|------------|-------|----------|--------|
| `DJANGO_SECRET_KEY` | Generate with Python | ✅ Yes | See Step 1 |
| `DOCKER_HUB_USERNAME` | `haroon5295` | ✅ Yes | You provided |
| `DOCKER_HUB_TOKEN` | `dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY` | ✅ Yes | You provided |
| `CYPRESS_RECORD_KEY` | `8d5f0fe8-0c32-4259-8073-86ef9b7ac337` | ⚠️ Optional | You provided |

---

## 🛠️ Troubleshooting

### **Problem: Can't find SECRET_KEY in .env**

**Solution:**
1. Generate a new one using Option A above
2. Add it to your `.env` file:
   ```bash
   echo "SECRET_KEY=YOUR_GENERATED_KEY" >> .env
   ```

### **Problem: GitHub Secrets page not showing**

**Solution:**
- Make sure you're logged into GitHub
- Check you have admin/write access to the repository
- Try refreshing the page

### **Problem: Pipeline fails with "Secret not found"**

**Solution:**
- Double-check secret names (case-sensitive!)
- Make sure secrets are added to the correct repository
- Verify you clicked "Add secret" after entering values

---

## 📚 Additional Resources

- **GitHub Secrets Documentation:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Docker Hub Tokens:** https://docs.docker.com/docker-hub/access-tokens/
- **Cypress Dashboard:** https://dashboard.cypress.io/

---

## ✅ Checklist

Before running the pipeline, make sure:

- [ ] Generated or found `DJANGO_SECRET_KEY`
- [ ] Added `DJANGO_SECRET_KEY` to GitHub Secrets
- [ ] Added `DOCKER_HUB_USERNAME` to GitHub Secrets
- [ ] Added `DOCKER_HUB_TOKEN` to GitHub Secrets
- [ ] Added `CYPRESS_RECORD_KEY` to GitHub Secrets (optional)
- [ ] Verified all secrets are listed in GitHub
- [ ] Ready to push code and trigger pipeline

---

**Status:** ✅ **Ready to setup GitHub Secrets!**

**Next Step:** Generate SECRET_KEY and add all secrets to GitHub.

