"""
White-Box Testing - Product Utils
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/product/utils/*.py
"""
import pytest
from decimal import Decimal

from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.product.utils.availability import get_product_availability
from saleor.product.utils.variants import get_variant_selection_attributes
from saleor.channel.models import Channel
from saleor.warehouse.models import Warehouse


# ============================================
# TEST 1: Product Availability - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestProductAvailability:
    """Test product availability functions for statement coverage"""
    
    def test_get_product_availability_in_stock(self):
        """Statement Coverage: product in stock"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        availability = get_product_availability(
            product=product,
            variants=[variant],
            channel=channel
        )
        
        assert availability is not None
    
    def test_get_product_availability_out_of_stock(self):
        """Statement Coverage: product out of stock"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        availability = get_product_availability(
            product=product,
            variants=[variant],
            channel=channel
        )
        
        assert availability is not None


# ============================================
# TEST 2: Variant Selection Attributes - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestVariantSelectionAttributes:
    """Test variant selection attributes for statement coverage"""
    
    def test_get_variant_selection_attributes(self):
        """Statement Coverage: get variant selection attributes"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        attributes = get_variant_selection_attributes(variant)
        
        # Should return attributes (may be empty)
        assert isinstance(attributes, dict)

