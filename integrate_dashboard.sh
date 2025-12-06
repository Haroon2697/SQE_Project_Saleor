#!/bin/bash

# Dashboard Integration Script
# This script integrates saleor-dashboard into the main SQE_Project_Saleor repository

set -e

echo "🚀 Starting Dashboard Integration..."
echo ""

# Check if dashboard directory exists
if [ ! -d "../saleor-dashboard" ]; then
    echo "❌ Error: saleor-dashboard directory not found at ../saleor-dashboard"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run from SQE_Project_Saleor directory"
    exit 1
fi

echo "📋 Step 1: Removing .git from dashboard (to avoid nested repos)..."
cd ../saleor-dashboard
if [ -d ".git" ]; then
    rm -rf .git
    echo "✅ Removed .git from dashboard"
else
    echo "ℹ️  No .git found in dashboard (already removed or not a git repo)"
fi

echo ""
echo "📋 Step 2: Copying dashboard to main repo..."
cd ..
if [ -d "SQE_Project_Saleor/dashboard" ]; then
    echo "⚠️  Warning: dashboard/ already exists in SQE_Project_Saleor"
    read -p "Do you want to remove it and copy fresh? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf SQE_Project_Saleor/dashboard
        echo "✅ Removed existing dashboard directory"
    else
        echo "❌ Aborted. Please manually handle the existing dashboard directory"
        exit 1
    fi
fi

# Copy dashboard (excluding node_modules and other build artifacts)
echo "📦 Copying dashboard files (excluding node_modules)..."
rsync -av --exclude='node_modules' \
         --exclude='.next' \
         --exclude='dist' \
         --exclude='build' \
         --exclude='.git' \
         --exclude='.pnpm-store' \
         --exclude='.cache' \
         saleor-dashboard/ SQE_Project_Saleor/dashboard/

echo "✅ Dashboard copied successfully"
echo ""

cd SQE_Project_Saleor

echo "📋 Step 3: Verifying .gitignore..."
if grep -q "dashboard/node_modules/" .gitignore; then
    echo "✅ .gitignore already configured for dashboard"
else
    echo "⚠️  Warning: dashboard entries not found in .gitignore"
    echo "   (They should have been added, but please verify)"
fi

echo ""
echo "📋 Step 4: Checking git status..."
git status dashboard/ 2>&1 | head -20

echo ""
echo "✅ Integration complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Review the changes: git status"
echo "   2. Add dashboard: git add dashboard/"
echo "   3. Commit: git commit -m 'Add saleor-dashboard for UI testing in CI/CD pipeline'"
echo "   4. Push: git push origin main"
echo ""
echo "⚠️  Note: node_modules/ is excluded and will be installed in CI/CD pipeline"
echo ""

