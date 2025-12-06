#!/bin/bash
# Generate Django SECRET_KEY
# This script generates a secure SECRET_KEY for Django

echo "🔐 Generating Django SECRET_KEY..."
echo ""

# Generate SECRET_KEY using Python
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null)

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Error: Python3 not found or failed to generate key"
    echo ""
    echo "Alternative method:"
    echo "Run this command manually:"
    echo "  python3 -c \"import secrets; print(secrets.token_urlsafe(50))\""
    exit 1
fi

echo "✅ SECRET_KEY generated successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Your Django SECRET_KEY:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "$SECRET_KEY"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Copy the SECRET_KEY above"
echo ""
echo "2. Add to GitHub Secrets:"
echo "   - Go to: https://github.com/Haroon2697/SQE_Project_Saleor/settings/secrets/actions"
echo "   - Click 'New repository secret'"
echo "   - Name: DJANGO_SECRET_KEY"
echo "   - Value: [paste the key above]"
echo "   - Click 'Add secret'"
echo ""
echo "3. (Optional) Update your local .env file:"
echo "   echo 'SECRET_KEY=$SECRET_KEY' >> .env"
echo ""
echo "✅ Done!"

