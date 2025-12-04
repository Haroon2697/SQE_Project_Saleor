"""
Unit Tests (White-box Testing)
Tests for Saleor models and internal functionality
"""
import pytest
from django.contrib.auth import get_user_model
from saleor.product.models import Product, Category, ProductType
from saleor.site.models import SiteSettings


@pytest.mark.django_db
def test_create_user():
    """Test user creation (white-box)"""
    User = get_user_model()
    user = User.objects.create_user(
        email="test@example.com",
        password="test123"
    )
    assert user.email == "test@example.com"
    assert user.check_password("test123")
    assert not user.is_staff
    assert not user.is_superuser
    print("✅ User creation test passed")


@pytest.mark.django_db
def test_create_superuser():
    """Test superuser creation (white-box)"""
    User = get_user_model()
    superuser = User.objects.create_superuser(
        email="admin@test.com",
        password="admin123"
    )
    assert superuser.email == "admin@test.com"
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.check_password("admin123")
    print("✅ Superuser creation test passed")


@pytest.mark.django_db
def test_create_category():
    """Test category creation (white-box)"""
    category = Category.objects.create(
        name="Electronics",
        slug="electronics"
    )
    assert category.name == "Electronics"
    assert category.slug == "electronics"
    assert str(category) == "Electronics"
    print("✅ Category creation test passed")


@pytest.mark.django_db
def test_create_product_type():
    """Test product type creation (white-box)"""
    product_type = ProductType.objects.create(
        name="Digital",
        slug="digital"
    )
    assert product_type.name == "Digital"
    assert product_type.slug == "digital"
    print("✅ Product type creation test passed")


@pytest.mark.django_db
def test_create_product():
    """Test product creation (white-box)"""
    category = Category.objects.create(
        name="Electronics",
        slug="electronics"
    )
    
    product_type = ProductType.objects.create(
        name="Digital",
        slug="digital"
    )
    
    # Product description must be JSON format (EditorJS) or None
    product = Product.objects.create(
        name="Test Product",
        slug="test-product",
        product_type=product_type,
        category=category,  # Use category (singular) not categories
        description=None  # Use None instead of string
    )
    
    assert product.name == "Test Product"
    assert product.slug == "test-product"
    assert product.category == category
    assert product.product_type.name == "Digital"
    print("✅ Product creation test passed")


@pytest.mark.django_db
def test_site_settings():
    """Test site settings (white-box)"""
    site_settings = SiteSettings.objects.first()
    if site_settings:
        assert site_settings.site is not None
        print("✅ Site settings test passed")
    else:
        pytest.skip("Site settings not configured")

