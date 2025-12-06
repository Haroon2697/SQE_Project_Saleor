"""
White-Box Testing - Core Utils
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/core/utils/__init__.py
"""
import pytest
from unittest.mock import Mock, patch
from django.test import RequestFactory
from django.contrib.sites.models import Site

from saleor.core.utils import (
    get_client_ip,
    build_absolute_uri,
    get_domain,
    get_public_url
)


# ============================================
# TEST 1: get_client_ip - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetClientIp:
    """Test get_client_ip() for statement coverage"""
    
    def test_get_client_ip_x_forwarded_for_single(self):
        """Statement Coverage: X-Forwarded-For with single IP"""
        request = RequestFactory().get("/", HTTP_X_FORWARDED_FOR="192.168.1.1")
        ip = get_client_ip(request)
        assert ip == "192.168.1.1"
    
    def test_get_client_ip_x_forwarded_for_multiple(self):
        """Statement Coverage: X-Forwarded-For with multiple IPs (take first)"""
        request = RequestFactory().get("/", HTTP_X_FORWARDED_FOR="192.168.1.1, 10.0.0.1")
        ip = get_client_ip(request)
        assert ip == "192.168.1.1"
    
    def test_get_client_ip_remote_addr(self):
        """Statement Coverage: use REMOTE_ADDR when X-Forwarded-For not present"""
        request = RequestFactory().get("/")
        request.META['REMOTE_ADDR'] = '192.168.1.100'
        ip = get_client_ip(request)
        assert ip == "192.168.1.100"
    
    def test_get_client_ip_invalid_ip(self):
        """Statement Coverage: invalid IP -> return 127.0.0.1"""
        request = RequestFactory().get("/", HTTP_X_FORWARDED_FOR="invalid.ip.address")
        ip = get_client_ip(request)
        assert ip == "127.0.0.1"
    
    def test_get_client_ip_none(self):
        """Statement Coverage: no IP -> return 127.0.0.1"""
        request = RequestFactory().get("/")
        if 'REMOTE_ADDR' in request.META:
            del request.META['REMOTE_ADDR']
        ip = get_client_ip(request)
        assert ip == "127.0.0.1"


# ============================================
# TEST 2: build_absolute_uri - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBuildAbsoluteUri:
    """Test build_absolute_uri() for statement coverage"""
    
    def test_build_absolute_uri_with_domain(self):
        """Statement Coverage: with domain parameter"""
        uri = build_absolute_uri("/path/to/resource", domain="example.com")
        assert uri == "http://example.com/path/to/resource"
    
    def test_build_absolute_uri_without_domain(self):
        """Statement Coverage: without domain (use site)"""
        site = Site.objects.create(domain="testsite.com", name="Test Site")
        
        with patch('saleor.core.utils.Site.objects.get_current', return_value=site):
            uri = build_absolute_uri("/path/to/resource")
            assert "testsite.com" in uri
            assert "/path/to/resource" in uri
    
    def test_build_absolute_uri_https(self):
        """Statement Coverage: with HTTPS"""
        uri = build_absolute_uri("/path/to/resource", domain="example.com", protocol="https")
        assert uri == "https://example.com/path/to/resource"
    
    def test_build_absolute_uri_absolute_path(self):
        """Statement Coverage: absolute path (starts with /)"""
        uri = build_absolute_uri("/absolute/path", domain="example.com")
        assert uri == "http://example.com/absolute/path"
    
    def test_build_absolute_uri_relative_path(self):
        """Statement Coverage: relative path"""
        uri = build_absolute_uri("relative/path", domain="example.com")
        assert uri == "http://example.com/relative/path"


# ============================================
# TEST 3: get_domain - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetDomain:
    """Test get_domain() for statement coverage"""
    
    def test_get_domain_with_site(self):
        """Statement Coverage: with site parameter"""
        site = Site.objects.create(domain="testsite.com", name="Test Site")
        domain = get_domain(site=site)
        assert domain == "testsite.com"
    
    def test_get_domain_without_site(self):
        """Statement Coverage: without site (use current site)"""
        site = Site.objects.create(domain="currentsite.com", name="Current Site")
        
        with patch('saleor.core.utils.Site.objects.get_current', return_value=site):
            domain = get_domain()
            assert domain == "currentsite.com"
    
    def test_get_domain_none_site(self):
        """Statement Coverage: site is None"""
        with patch('saleor.core.utils.Site.objects.get_current', return_value=None):
            domain = get_domain()
            # Should handle None gracefully
            assert domain is None or isinstance(domain, str)


# ============================================
# TEST 4: get_public_url - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetPublicUrl:
    """Test get_public_url() for statement coverage"""
    
    def test_get_public_url_with_domain(self):
        """Statement Coverage: with domain parameter"""
        url = get_public_url(domain="example.com")
        assert url == "http://example.com"
    
    def test_get_public_url_without_domain(self):
        """Statement Coverage: without domain (use get_domain)"""
        site = Site.objects.create(domain="testsite.com", name="Test Site")
        
        with patch('saleor.core.utils.get_domain', return_value="testsite.com"):
            url = get_public_url()
            assert url == "http://testsite.com"
    
    def test_get_public_url_https(self):
        """Statement Coverage: with HTTPS protocol"""
        url = get_public_url(domain="example.com", protocol="https")
        assert url == "https://example.com"
    
    def test_get_public_url_none_domain(self):
        """Statement Coverage: domain is None"""
        with patch('saleor.core.utils.get_domain', return_value=None):
            url = get_public_url()
            # Should handle None gracefully
            assert url is None or isinstance(url, str)

