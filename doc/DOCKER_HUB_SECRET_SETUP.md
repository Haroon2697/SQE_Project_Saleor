# Docker Hub Secret Setup Guide

## 🔑 Your Docker Hub Credentials

**Username:** `haroon5295`  
**Access Token:** `YOUR_DOCKER_HUB_TOKEN_HERE` (⚠️ Never commit tokens to code!)  
**Token Description:** `SQE_Project_Saleor`  
**Expires:** `Jan 06, 2026 at 23:59:59`  
**Permissions:** `Read & Write`

## 📝 Steps to Add to GitHub Secrets

### Step 1: Go to GitHub Repository Settings
1. Navigate to your repository: `https://github.com/YOUR_USERNAME/YOUR_REPO`
2. Click on **Settings** (top navigation bar)
3. In the left sidebar, click **Secrets and variables** → **Actions**

### Step 2: Add DOCKER_HUB_USERNAME Secret
1. Click **New repository secret**
2. **Name:** `DOCKER_HUB_USERNAME`
3. **Secret:** `haroon5295`
4. Click **Add secret**

### Step 3: Add DOCKER_HUB_TOKEN Secret
1. Click **New repository secret** again
2. **Name:** `DOCKERHUB_TOKEN` or `DOCKER_HUB_TOKEN` (⚠️ Workflow supports both)
3. **Secret:** `YOUR_DOCKER_HUB_ACCESS_TOKEN` (⚠️ Use your actual token from Docker Hub)
4. Click **Add secret**

## ✅ Verify Secrets Are Added

You should see both secrets in the list:
- ✅ `DOCKER_HUB_USERNAME`
- ✅ `DOCKER_HUB_TOKEN`

## 🧪 Test the Setup

After adding the secrets, the next workflow run should:
1. ✅ Detect the `DOCKER_HUB_TOKEN` secret
2. ✅ Login to Docker Hub successfully
3. ✅ Push Docker images to `haroon5295/saleor-staging` and `haroon5295/saleor-prod`

## 🔒 Security Notes

- ⚠️ **Never commit tokens to code**
- ⚠️ **Never share tokens publicly**
- ✅ Tokens are encrypted in GitHub Secrets
- ✅ Only accessible to workflows in your repository
- ✅ Token expires: Jan 06, 2026 (renew before then)

## 🐛 Troubleshooting

### If workflow still shows "DOCKER_HUB_TOKEN not set":
1. Check secret name is exactly: `DOCKER_HUB_TOKEN` (case-sensitive)
2. Verify secret was added to the correct repository
3. Check if workflow has access to secrets (some events may not have access)
4. Wait a few minutes after adding secret (GitHub may need to sync)

### If Docker login fails:
1. Verify token hasn't expired
2. Check token has "Read & Write" permissions
3. Verify username is correct: `haroon5295`
4. Test token manually: `docker login -u haroon5295` (use token as password)

## 📚 Related Documentation

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)

