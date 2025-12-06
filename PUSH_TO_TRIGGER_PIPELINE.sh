#!/bin/bash
# Quick script to commit and push the 5-stage pipeline fix

echo "🚀 Committing and pushing 5-stage pipeline fix..."
echo ""

cd /home/haroon/SQE/SQE_Project_Saleor

# Add the workflow file
git add .github/workflows/complete-cicd-pipeline.yml \
        HOW_TO_SEE_5_STAGE_PIPELINE.md \
        TRIGGER_PIPELINE_NOW.md

# Commit
git commit -m "fix: Enable 5-stage CI/CD pipeline on all pushes" || echo "⚠️ Nothing to commit or already committed"

# Show status
echo ""
echo "📊 Current status:"
git status --short

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Ready to push!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run this command to push and trigger the pipeline:"
echo ""
echo "   git push origin main"
echo ""
echo "After pushing, go to:"
echo "   https://github.com/Haroon2697/SQE_Project_Saleor/actions"
echo ""
echo "You should see: '🚀 Complete CI/CD Pipeline - 5 Stages' running!"
echo ""

