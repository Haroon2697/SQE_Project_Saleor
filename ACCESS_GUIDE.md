# 🚀 How to Access Saleor Interfaces

## Quick Start

### 1. Start PostgreSQL (if not running)
```bash
sudo systemctl start postgresql
```

### 2. Start Saleor Server
```bash
cd ~/SQE/SQE_Project_Saleor
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

You should see:
```
Starting development server at http://0.0.0.0:8000/
```

---

## 📊 Access URLs

### **1. GraphQL API Interface**

**URL:** http://localhost:8000/graphql/

**What it is:**
- Interactive GraphQL playground
- Test queries and mutations
- Explore the API schema

**How to use:**
1. Open http://localhost:8000/graphql/ in your browser
2. You'll see a GraphQL interface
3. Try this query in the left panel:
   ```graphql
   query {
     shop {
       name
       version
       description
     }
   }
   ```
4. Click the "Play" button or press `Ctrl+Enter`
5. See results in the right panel

**Example Queries:**
```graphql
# Get shop information
query {
  shop {
    name
    version
    description
  }
}

# Get products
query {
  products(first: 5) {
    edges {
      node {
        name
        slug
        description
      }
    }
  }
}

# Get categories
query {
  categories(first: 5) {
    edges {
      node {
        name
        slug
      }
    }
  }
}
```

---

### **2. Admin Dashboard**

**URL:** http://localhost:8000/dashboard/

**What it is:**
- Full admin interface for managing Saleor
- Manage products, orders, customers
- Configure settings

**Login Credentials:**
- **Email:** `admin@example.com`
- **Password:** `admin123`

**How to use:**
1. Open http://localhost:8000/dashboard/ in your browser
2. You'll see a login page
3. Enter credentials:
   - Email: `admin@example.com`
   - Password: `admin123`
4. Click "Sign In"
5. You'll be redirected to the dashboard

**What you can do:**
- **Products:** Add, edit, delete products
- **Orders:** View and manage orders
- **Customers:** Manage customer accounts
- **Settings:** Configure store settings
- **Analytics:** View sales and statistics

---

### **3. Health Check Endpoint**

**URL:** http://localhost:8000/health/

**What it is:**
- Simple health check endpoint
- Returns server status
- Useful for monitoring

**How to test:**
```bash
curl http://localhost:8000/health/
```

Or open in browser: http://localhost:8000/health/

---

## 🔍 Troubleshooting

### **Server won't start:**
```bash
# Check if port 8000 is in use
sudo lsof -i :8000

# Kill process if needed
sudo kill -9 <PID>

# Check PostgreSQL is running
sudo systemctl status postgresql
```

### **Can't access GraphQL:**
- Make sure server is running
- Check URL: http://localhost:8000/graphql/ (note the trailing slash)
- Try: http://127.0.0.1:8000/graphql/

### **Can't login to Dashboard:**
- Verify admin user exists:
  ```bash
  python manage.py shell
  >>> from django.contrib.auth import get_user_model
  >>> User = get_user_model()
  >>> User.objects.filter(email='admin@example.com').exists()
  ```
- If user doesn't exist, create it:
  ```bash
  python manage.py createsuperuser
  ```

### **Database errors:**
```bash
# Run migrations
python manage.py migrate

# Check database connection
python manage.py dbshell
```

---

## 📝 Quick Verification

Run this to verify everything is working:

```bash
cd ~/SQE/SQE_Project_Saleor
source .venv/bin/activate
./verify_setup.sh
```

---

## 🎯 For Your SQE Project

### **Testing GraphQL API:**
- Use http://localhost:8000/graphql/ for manual testing
- Use `tests/integration/test_api.py` for automated testing
- Test various queries and mutations

### **Testing Admin Dashboard:**
- Use http://localhost:8000/dashboard/ for manual testing
- Use Cypress/Selenium for automated UI testing
- Test login, navigation, CRUD operations

### **API Testing Examples:**
See `tests/integration/test_api.py` for examples of:
- Health endpoint testing
- GraphQL query testing
- Authentication testing

---

**Last Updated:** 2025-12-02

