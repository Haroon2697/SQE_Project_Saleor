#!/bin/bash

# Quick verification script for Saleor setup

echo "=========================================="
echo "🔍 VERIFYING SALEOR SETUP"
echo "=========================================="
echo

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check PostgreSQL
echo "1. PostgreSQL:"
if sudo systemctl is-active --quiet postgresql 2>/dev/null; then
    echo -e "   ${GREEN}✅ Running${NC}"
else
    echo -e "   ${RED}❌ Not running (run: sudo systemctl start postgresql)${NC}"
fi

# Check Redis
echo "2. Redis:"
if sudo systemctl is-active --quiet redis-server 2>/dev/null || pgrep -x redis-server > /dev/null; then
    echo -e "   ${GREEN}✅ Running${NC}"
else
    echo -e "   ${YELLOW}⚠️  Not running (optional)${NC}"
fi

# Check .env file
echo "3. Environment file:"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✅ .env exists${NC}"
    if grep -q "SECRET_KEY=" .env && ! grep -q "SECRET_KEY=changeme" .env; then
        echo -e "   ${GREEN}✅ SECRET_KEY configured${NC}"
    else
        echo -e "   ${YELLOW}⚠️  SECRET_KEY needs to be set${NC}"
    fi
else
    echo -e "   ${RED}❌ .env file missing${NC}"
fi

# Check virtual environment
echo "4. Virtual environment:"
if [ -d ".venv" ]; then
    echo -e "   ${GREEN}✅ Virtual environment exists${NC}"
else
    echo -e "   ${RED}❌ Virtual environment missing${NC}"
fi

# Check if server is running
echo "5. Saleor server:"
if curl -s http://localhost:8000/health/ > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Server is running on port 8000${NC}"
elif curl -s http://localhost:8000/graphql/ > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Server is running on port 8000${NC}"
else
    echo -e "   ${YELLOW}⚠️  Server not running (start with: python manage.py runserver)${NC}"
fi

echo
echo "=========================================="

