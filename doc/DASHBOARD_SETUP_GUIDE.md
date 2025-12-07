# Dashboard Setup Guide

## 📋 Current Status

**Dashboard Location:**
- ✅ Dashboard already exists in: `/home/haroon/SQE/SQE_Project_Saleor/dashboard`
- Separate dashboard directory: `/home/haroon/SQE/saleor-dashboard`

## 🤔 Do You Need to Push the Dashboard?

### **Answer: It depends on your setup**

1. **If dashboard is already in your repo:**
   - ✅ No need to push separately
   - The dashboard is part of your main project
   - It will be pushed automatically with your main project

2. **If you want to update/sync the dashboard:**
   - You may want to copy the latest from `saleor-dashboard` to `dashboard`
   - Or keep them separate if they serve different purposes

## 🔍 How to Check

### Check if dashboard is tracked in git:
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
git status dashboard/
```

### Check if dashboard is committed:
```bash
git ls-files dashboard/ | head -10
```

## 📦 How to Add/Update Dashboard in Your Repo

### Option 1: Dashboard Already Exists (Current Situation)
If `dashboard/` already exists in your project:
- ✅ **No action needed** - it's already part of your repo
- Just commit and push your main project:
  ```bash
  cd /home/haroon/SQE/SQE_Project_Saleor
  git add dashboard/
  git commit -m "Update dashboard"
  git push
  ```

### Option 2: Copy from Separate Dashboard Directory
If you want to update the dashboard from the separate directory:

```bash
# Navigate to main project
cd /home/haroon/SQE/SQE_Project_Saleor

# Backup existing dashboard (optional)
mv dashboard dashboard.backup

# Copy from separate dashboard directory
cp -r ../saleor-dashboard ./dashboard

# Remove node_modules and other build artifacts (they'll be regenerated)
cd dashboard
rm -rf node_modules dist build .next

# Add to git
cd ..
git add dashboard/
git commit -m "Add/update dashboard from saleor-dashboard"
git push
```

### Option 3: Use Git Submodule (Advanced)
If you want to keep them as separate repos:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor

# Remove existing dashboard if it's not a submodule
rm -rf dashboard

# Add as submodule (if saleor-dashboard is a git repo)
git submodule add <your-dashboard-repo-url> dashboard

# Commit submodule
git commit -m "Add dashboard as submodule"
git push
```

## 🚀 Recommended Approach

**For your current setup, I recommend:**

1. **Check if dashboard is already committed:**
   ```bash
   cd /home/haroon/SQE/SQE_Project_Saleor
   git ls-files dashboard/ | wc -l
   ```

2. **If dashboard files are tracked:**
   - ✅ Just push normally - dashboard is already in your repo
   - No separate push needed

3. **If dashboard is not tracked:**
   - Add it to your repo:
     ```bash
     git add dashboard/
     git commit -m "Add dashboard directory"
     git push
     ```

## ⚠️ Important Notes

1. **Size Consideration:**
   - Dashboard with `node_modules` is ~1.6GB
   - **DO NOT commit `node_modules/`** - it's in `.gitignore`
   - Only commit source files, not dependencies

2. **What to Commit:**
   - ✅ Source files (`src/`, `package.json`, etc.)
   - ✅ Configuration files
   - ❌ `node_modules/` (excluded by `.gitignore`)
   - ❌ `dist/`, `build/` (build artifacts)
   - ❌ `.next/`, `.cache/` (cache files)

3. **CI/CD Pipeline:**
   - Your pipeline already handles dashboard:
     - Installs dependencies in CI
     - Builds dashboard if needed
     - Starts dashboard for Cypress tests
   - No special setup needed if dashboard is in repo

## 🔧 Quick Check Commands

```bash
# Check if dashboard is in repo
cd /home/haroon/SQE/SQE_Project_Saleor
git ls-files dashboard/ | head -5

# Check dashboard size (excluding node_modules)
du -sh dashboard --exclude=node_modules

# Check what's ignored
git check-ignore -v dashboard/node_modules
```

## ✅ Summary

**Most Likely:** Your dashboard is already in the repo and will be pushed automatically with your main project. Just run:

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
git add .
git commit -m "Update project with new tests and fixes"
git push
```

The dashboard will be included automatically if it's part of your project structure!

