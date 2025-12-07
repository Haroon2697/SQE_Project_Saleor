# Cypress Setup Guide

## 🚨 Issue: Cypress Cannot Connect to Server

If you see the error:
```
Cypress could not verify that this server is running:
> http://localhost:9000
```

This means the **Saleor Dashboard** is not running on port 9000.

## ✅ Solution: Start Servers Before Running Cypress

### Option 1: Use the Helper Script (Recommended)

```bash
cd /home/haroon/SQE/SQE_Project_Saleor

# Start both backend and dashboard servers
./start_servers_for_cypress.sh
```

This script will:
1. ✅ Start the Saleor backend on port 8000
2. ✅ Start the Saleor dashboard on port 9000
3. ✅ Wait for both servers to be ready
4. ✅ Keep them running until you press Ctrl+C

**Then in another terminal:**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
npm run cypress:open    # Interactive mode
# OR
npm run cypress:run     # Headless mode
```

### Option 2: Manual Setup

#### Step 1: Start Backend Server

**Terminal 1:**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate  # or venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

Wait until you see:
```
Starting development server at http://0.0.0.0:8000/
```

#### Step 2: Start Dashboard Server

**Terminal 2:**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor/dashboard

# Install dependencies (first time only)
pnpm install  # or npm install if pnpm not available

# Start dashboard on port 9000
pnpm dev --port 9000  # or npm run dev -- --port 9000
```

Wait until you see the dashboard is running.

#### Step 3: Run Cypress

**Terminal 3:**
```bash
cd /home/haroon/SQE/SQE_Project_Saleor
npm run cypress:open    # Interactive mode
# OR
npm run cypress:run     # Headless mode
```

## 🔍 Verify Servers Are Running

Before running Cypress, verify both servers are accessible:

```bash
# Check backend (port 8000)
curl http://localhost:8000/graphql/
# Should return HTML or GraphQL response

# Check dashboard (port 9000)
curl http://localhost:9000/
# Should return HTML
```

## 📝 Configuration

### Cypress Configuration
- **File:** `cypress.config.js`
- **Base URL:** `http://localhost:9000` (dashboard)
- **Backend API:** `http://localhost:8000/graphql/` (used by dashboard)

### Dashboard Configuration
The dashboard needs to know where the backend API is. Check:
- `dashboard/.env` or environment variables
- `API_URL` should point to `http://localhost:8000/graphql/`

## 🐛 Troubleshooting

### Dashboard Won't Start

1. **Check if port 9000 is already in use:**
   ```bash
   lsof -i :9000
   # If something is using it, kill it or use a different port
   ```

2. **Check dashboard dependencies:**
   ```bash
   cd dashboard
   pnpm install  # or npm install
   ```

3. **Check for errors in dashboard.log:**
   ```bash
   cat dashboard.log
   ```

### Backend Won't Start

1. **Check if PostgreSQL is running:**
   ```bash
   sudo systemctl status postgresql
   sudo systemctl start postgresql  # if not running
   ```

2. **Check if port 8000 is already in use:**
   ```bash
   lsof -i :8000
   ```

3. **Check backend logs:**
   ```bash
   cat backend.log
   ```

### Cypress Still Can't Connect

1. **Wait longer:** The servers might need more time to start
2. **Check firewall:** Ensure ports 8000 and 9000 are not blocked
3. **Try different ports:** Update `cypress.config.js` if needed
4. **Check Cypress logs:** Look for more detailed error messages

## 🎯 Quick Start Checklist

- [ ] PostgreSQL is running
- [ ] Backend server is running on port 8000
- [ ] Dashboard server is running on port 9000
- [ ] Both servers respond to curl requests
- [ ] Cypress can connect to http://localhost:9000

## 📚 Related Files

- `cypress.config.js` - Cypress configuration
- `start_servers_for_cypress.sh` - Helper script to start servers
- `dashboard/package.json` - Dashboard scripts
- `.github/workflows/complete-cicd-pipeline.yml` - CI/CD Cypress setup

