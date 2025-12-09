"""
Integration API tests for Saleor.
These tests use Django test client instead of requiring a running server.
"""
import pytest
from django.test import Client


@pytest.mark.django_db
class TestHealthEndpoint:
    """Test basic server responses."""
    
    def test_graphql_endpoint_exists(self):
        """Test GraphQL endpoint exists."""
        client = Client()
        response = client.get('/graphql/')
        # Should return 405 (Method Not Allowed for GET) or 200
        assert response.status_code in [200, 400, 405]
    
    def test_graphql_post_request(self):
        """Test GraphQL POST request."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ shop { name } }"}',
            content_type='application/json'
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestGraphQLQueries:
    """Test GraphQL query functionality."""
    
    def test_shop_query(self):
        """Test shop query returns data."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ shop { name description } }"}',
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert 'data' in data or 'errors' in data
    
    def test_channels_query(self):
        """Test channels query."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ channels { id name slug } }"}',
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_products_query(self):
        """Test products query."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ products(first: 5, channel: \\"default-channel\\") { edges { node { id name } } } }"}',
            content_type='application/json'
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestGraphQLInvalidQueries:
    """Test GraphQL handles invalid queries."""
    
    def test_invalid_query(self):
        """Test invalid query returns error."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ invalidField { name } }"}',
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert 'errors' in data
    
    def test_syntax_error_query(self):
        """Test syntax error in query."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "{ unclosed { name }"}',
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert 'errors' in data


@pytest.mark.django_db
class TestGraphQLMutations:
    """Test GraphQL mutation functionality."""
    
    def test_mutation_without_auth(self):
        """Test mutation without authentication."""
        client = Client()
        response = client.post(
            '/graphql/',
            data='{"query": "mutation { tokenCreate(email: \\"test@test.com\\", password: \\"test\\") { token } }"}',
            content_type='application/json'
        )
        # Should return 200 with error about authentication
        assert response.status_code == 200
