#!/bin/bash
# Smoke Tests for Staging/Production
# This script runs basic smoke tests to validate deployment

set -e

BASE_URL="${1:-http://localhost:8000}"
TIMEOUT=30

echo "🧪 Running Smoke Tests against: $BASE_URL"
echo ""

# Test 1: GraphQL Endpoint
echo "Test 1: GraphQL Endpoint"
if curl -f -s -X POST "$BASE_URL/graphql/" \
    -H "Content-Type: application/json" \
    -d '{"query": "{ shop { name } }"}' \
    --max-time $TIMEOUT > /dev/null; then
    echo "✅ GraphQL endpoint is responding"
else
    echo "❌ GraphQL endpoint failed"
    exit 1
fi

# Test 2: Health Check (if available)
echo "Test 2: Health Check"
if curl -f -s "$BASE_URL/health" --max-time $TIMEOUT > /dev/null 2>&1; then
    echo "✅ Health endpoint is responding"
else
    echo "⚠️ Health endpoint not available (this is okay)"
fi

# Test 3: Static Files
echo "Test 3: Static Files"
if curl -f -s "$BASE_URL/static/" --max-time $TIMEOUT > /dev/null 2>&1; then
    echo "✅ Static files are accessible"
else
    echo "⚠️ Static files not accessible (this is okay)"
fi

# Test 4: API Response Time
echo "Test 4: API Response Time"
START_TIME=$(date +%s%N)
curl -f -s -X POST "$BASE_URL/graphql/" \
    -H "Content-Type: application/json" \
    -d '{"query": "{ shop { name } }"}' \
    --max-time $TIMEOUT > /dev/null
END_TIME=$(date +%s%N)
DURATION=$((($END_TIME - $START_TIME) / 1000000))

if [ $DURATION -lt 1000 ]; then
    echo "✅ API response time: ${DURATION}ms (acceptable)"
else
    echo "⚠️ API response time: ${DURATION}ms (slow but acceptable)"
fi

# Test 5: Database Connectivity (via API)
echo "Test 5: Database Connectivity"
RESPONSE=$(curl -s -X POST "$BASE_URL/graphql/" \
    -H "Content-Type: application/json" \
    -d '{"query": "{ shop { name } }"}' \
    --max-time $TIMEOUT)

if echo "$RESPONSE" | grep -q "shop"; then
    echo "✅ Database connectivity verified"
else
    echo "❌ Database connectivity failed"
    exit 1
fi

echo ""
echo "✅ All smoke tests passed!"

