# 🚀 Quick Start Guide - Access & Test Saleor

## Step 1: Start the Server

```bash
cd ~/SQE/SQE_Project_Saleor

# Start PostgreSQL (if not running)
sudo systemctl start postgresql

# Activate virtual environment
source .venv/bin/activate

# Start Saleor server
python manage.py runserver 0.0.0.0:8000
```

**You should see:**
```
Starting development server at http://0.0.0.0:8000/
```

---

## Step 2: Access the Interfaces

### **GraphQL Playground**
👉 **Open:** http://localhost:8000/graphql/

**Try this query:**
```graphql
query {
  shop {
    name
    version
    description
  }
}
```

### **Admin Dashboard**
👉 **Open:** http://localhost:8000/dashboard/

**Login:**
- Email: `admin@example.com`
- Password: `admin123`

---

## Step 3: Run Your First Tests

### **Option 1: Quick Test (Recommended First)**
```bash
cd ~/SQE/SQE_Project_Saleor
source .venv/bin/activate
./run_tests.sh basic
```

### **Option 2: Run All Tests**
```bash
./run_tests.sh all
```

### **Option 3: Run with Coverage**
```bash
./run_tests.sh coverage
```

### **Option 4: Run Specific Test Types**
```bash
./run_tests.sh unit        # White-box tests
./run_tests.sh integration # Black-box tests
```

---

## Step 4: Install Test Dependencies (If Needed)

If tests fail with "pytest not found":

```bash
source .venv/bin/activate
pip install pytest pytest-django pytest-cov
```

---

## 📋 What You Have Now:

✅ **Test Structure:**
- `tests/unit/test_models.py` - White-box tests (6 tests)
- `tests/integration/test_api.py` - Black-box tests (6 tests)
- `tests/test_basic.py` - Quick verification (2 tests)

✅ **CI/CD Pipeline:**
- `.github/workflows/ci.yml` - GitHub Actions workflow

✅ **Documentation:**
- `ACCESS_GUIDE.md` - How to access interfaces
- `PHASE2_START.md` - Phase 2 documentation
- `PROJECT_STATUS.md` - Overall project status

✅ **Scripts:**
- `run_tests.sh` - Easy test runner
- `setup_saleor.sh` - Automated setup
- `verify_setup.sh` - Verification script

---

## 🎯 Next Steps:

1. **Start server and verify access** (see Step 1 & 2 above)
2. **Run tests** (see Step 3 above)
3. **Check test results** - All tests should pass
4. **Add more tests** - Expand test coverage
5. **Push to GitHub** - Trigger CI/CD pipeline

---

## ❓ Troubleshooting

### **Tests fail with database error:**
```bash
# Make sure PostgreSQL is running
sudo systemctl start postgresql

# Run migrations
python manage.py migrate
```

### **pytest command not found:**
```bash
source .venv/bin/activate
pip install pytest pytest-django pytest-cov
```

### **Can't access GraphQL:**
- Make sure server is running on port 8000
- Check: http://localhost:8000/graphql/ (note trailing slash)

---

**Ready to test!** 🎉

