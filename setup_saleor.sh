#!/bin/bash

# Saleor Setup Script for SQE Project
# This script sets up Saleor for manual testing (no Docker)

set -e

echo "=========================================="
echo "🚀 SALEOR SETUP FOR SQE PROJECT"
echo "=========================================="
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check PostgreSQL
echo "📊 Step 1: Checking PostgreSQL..."
if sudo systemctl is-active --quiet postgresql; then
    echo -e "${GREEN}✅ PostgreSQL is running${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL is not running. Starting it...${NC}"
    sudo systemctl start postgresql
    sleep 2
    if sudo systemctl is-active --quiet postgresql; then
        echo -e "${GREEN}✅ PostgreSQL started${NC}"
    else
        echo -e "${RED}❌ Failed to start PostgreSQL. Please run: sudo systemctl start postgresql${NC}"
        exit 1
    fi
fi

# Step 2: Activate virtual environment
echo
echo "📦 Step 2: Activating virtual environment..."
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating it...${NC}"
    python3 -m venv .venv
fi
source .venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Step 3: Check .env file
echo
echo "⚙️  Step 3: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating it...${NC}"
    cat > .env << 'ENVEOF'
DEBUG=True
SECRET_KEY=PQDhYBvuP-Sab79BrgxHAwOXO19VROSaceNGstvnszX3_ZXK0y8pIMXB4SU2jQ8DSWA
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://saleor:saleor@localhost:5432/saleor
REDIS_URL=redis://localhost:6379/0
EMAIL_URL=console://
DEFAULT_FROM_EMAIL=noreply@example.com
ENABLE_ACCOUNT_CONFIRMATION_BY_EMAIL=False
ENVEOF
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Step 4: Run migrations
echo
echo "🗄️  Step 4: Running database migrations..."
python manage.py migrate --noinput
echo -e "${GREEN}✅ Migrations completed${NC}"

# Step 5: Create superuser (if doesn't exist)
echo
echo "👤 Step 5: Checking admin user..."
python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print("✅ Admin user created: admin@example.com / admin123")
else:
    print("✅ Admin user already exists")
PYEOF

# Step 6: Collect static files
echo
echo "📁 Step 6: Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1 || echo "⚠️  Static files collection skipped (not critical)"

echo
echo "=========================================="
echo -e "${GREEN}🎉 SETUP COMPLETE!${NC}"
echo "=========================================="
echo
echo "📊 Access URLs:"
echo "   GraphQL API:    http://localhost:8000/graphql"
echo "   Admin Panel:    http://localhost:8000/dashboard"
echo "   Health Check:   http://localhost:8000/health/"
echo
echo "🔑 Admin Credentials:"
echo "   Email:    admin@example.com"
echo "   Password: admin123"
echo
echo "▶️  To start the server, run:"
echo "   source .venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo
echo "=========================================="

