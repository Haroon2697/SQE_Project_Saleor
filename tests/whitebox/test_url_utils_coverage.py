"""
Tests for saleor/core/utils/url.py
These tests actually execute the real code to increase coverage.
"""
import pytest
from urllib.parse import urlparse

from saleor.core.utils.url import prepare_url, sanitize_url_for_logging


class TestPrepareUrl:
    """Test prepare_url() function - actual execution, no mocking."""

    def test_prepare_url_adds_params_to_empty_query(self):
        result = prepare_url("token=abc123", "https://example.com/redirect")
        assert result == "https://example.com/redirect?token=abc123"

    def test_prepare_url_appends_to_existing_query(self):
        result = prepare_url("new=value", "https://example.com/redirect?existing=param")
        assert result == "https://example.com/redirect?existing=param&new=value"

    def test_prepare_url_with_path(self):
        result = prepare_url("token=xyz", "https://example.com/path/to/page")
        assert result == "https://example.com/path/to/page?token=xyz"

    def test_prepare_url_with_fragment(self):
        result = prepare_url("token=abc", "https://example.com/page#section")
        assert "token=abc" in result

    def test_prepare_url_preserves_scheme(self):
        result = prepare_url("param=value", "http://example.com/page")
        assert result.startswith("http://")


class TestSanitizeUrlForLogging:
    """Test sanitize_url_for_logging() function - actual execution, no mocking."""

    def test_sanitize_url_without_credentials(self):
        url = "https://example.com/api/endpoint"
        result = sanitize_url_for_logging(url)
        assert result == url

    def test_sanitize_url_with_username_and_password(self):
        url = "https://user:password@example.com/api"
        result = sanitize_url_for_logging(url)
        assert "user" not in result
        assert "password" not in result
        assert "***:***@" in result
        assert "example.com" in result

    def test_sanitize_url_with_port(self):
        url = "https://user:pass@example.com:8080/api"
        result = sanitize_url_for_logging(url)
        assert "user" not in result
        assert "pass" not in result
        assert "8080" in result
        assert "***:***@" in result

    def test_sanitize_url_preserves_path_and_query(self):
        url = "https://user:pass@example.com/api/v1?key=value"
        result = sanitize_url_for_logging(url)
        assert "/api/v1" in result
        assert "key=value" in result

    def test_sanitize_url_simple_url(self):
        url = "https://api.example.com/webhook"
        result = sanitize_url_for_logging(url)
        assert result == url

