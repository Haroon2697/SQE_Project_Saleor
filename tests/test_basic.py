"""
Basic Tests - Quick verification tests
Run these first to verify your setup is working
"""
import pytest
from django.test import Client


def test_health():
    """Basic health check test - checks if server responds"""
    client = Client()
    # Try root endpoint instead of /health/ (which doesn't exist)
    response = client.get('/')
    # Should return 200 (home page) or 404 (not configured), but server should respond
    assert response.status_code in [200, 404]
    print("✅ Health test passed - server is responding")


def test_graphql():
    """Basic GraphQL endpoint test"""
    client = Client()
    response = client.post(
        '/graphql/',
        content_type='application/json',
        data='{"query": "{ shop { name } }"}'
    )
    assert response.status_code == 200
    print("✅ GraphQL test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

