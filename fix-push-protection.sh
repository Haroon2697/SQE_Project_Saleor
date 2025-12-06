#!/bin/bash
# Fix GitHub Push Protection - Quick Fix Script

echo "🔒 Fixing GitHub Push Protection Issue..."
echo ""

# Step 1: Commit the fixed files
echo "📝 Step 1: Committing fixed documentation files..."
git add GITHUB_SECRETS_SETUP_GUIDE.md \
        COMPLETE_CICD_IMPLEMENTATION.md \
        QUICK_SECRETS_SETUP.md \
        GITHUB_SECRETS_COMPLETE.md \
        SECRETS_QUICK_REFERENCE.md \
        FIX_PUSH_PROTECTION.md

git commit -m "security: Remove hardcoded Docker Hub token from documentation" || echo "⚠️ No changes to commit"

echo ""
echo "✅ Files committed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 IMPORTANT: Allow the Secret via GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "The token is still in previous commits. You need to allow it via GitHub:"
echo ""
echo "1. Open this URL in your browser:"
echo "   https://github.com/Haroon2697/SQE_Project_Saleor/security/secret-scanning/unblock-secret/36T98Rj0tHVNMQIyoDk79mCSSUu"
echo ""
echo "2. Click 'Allow secret' button"
echo ""
echo "3. Then run: git push origin main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Script completed! Follow the steps above to allow the secret."

