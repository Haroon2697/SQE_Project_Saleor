"""
Pytest configuration for Saleor tests
This file is automatically loaded by pytest
"""
import pytest
import os
import django

# Ensure Django is set up
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings')
django.setup()

# Note: pytest-django handles database setup automatically
# The database configuration comes from your .env file or DATABASE_URL
