# 🔐 Secrets Quick Reference Card

**Copy-paste ready values for GitHub Secrets**

---

## ✅ Required Secrets (Add These 2)

### **Secret 1: CYPRESS_RECORD_KEY**

```
Name: CYPRESS_RECORD_KEY
Value: 8d5f0fe8-0c32-4259-8073-86ef9b7ac337
```

**Purpose:** Cypress test recording to Dashboard  
**Project ID:** `rpaahx`

---

### **Secret 2: DOCKER_HUB_TOKEN**

```
Name: DOCKER_HUB_TOKEN
Value: dckr_pat_9MKc91ToLqs5pq-m70bH-taozpY
```

**Purpose:** Docker Hub authentication for pushing images  
**Username:** `haroon5295`  
**Permissions:** Read & Write  
**Expires:** Jan 03, 2026

---

## 🚀 How to Add (3 Steps)

1. **Go to:** `https://github.com/Haroon2697/SQE_Project_Saleor/settings/secrets/actions`
2. **Click:** "New repository secret"
3. **Add both secrets** using the values above

---

## ✅ Verification

After adding, you should see:
- ✅ `CYPRESS_RECORD_KEY` in secrets list
- ✅ `DOCKER_HUB_TOKEN` in secrets list

---

**That's it!** Your pipeline will now use these secrets automatically.

