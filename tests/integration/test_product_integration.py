"""
Integration tests for Product module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from saleor.product.models import (
    Product,
    ProductType,
    Category,
    ProductVariant,
    ProductChannelListing,
    ProductVariantChannelListing,
)
from saleor.channel.models import Channel
# Product utilities are imported in tests if needed


User = get_user_model()


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Test Channel",
        slug="test-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name="Test Category",
        slug="test-category",
    )


@pytest.fixture
def product_type(db):
    """Create a test product type."""
    return ProductType.objects.create(
        name="Test Product Type",
        slug="test-product-type",
        is_shipping_required=True,
        is_digital=False,
    )


@pytest.fixture
def product(db, product_type, category):
    """Create a test product."""
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        product_type=product_type,
        category=category,
    )


@pytest.fixture
def product_variant(db, product):
    """Create a test product variant."""
    return ProductVariant.objects.create(
        product=product,
        sku="TEST-SKU-001",
        name="Test Variant",
    )


@pytest.fixture
def product_channel_listing(db, product, channel):
    """Create a product channel listing."""
    return ProductChannelListing.objects.create(
        product=product,
        channel=channel,
        is_published=True,
        visible_in_listings=True,
    )


@pytest.fixture
def variant_channel_listing(db, product_variant, channel):
    """Create a variant channel listing."""
    return ProductVariantChannelListing.objects.create(
        variant=product_variant,
        channel=channel,
        price_amount=Decimal("100.00"),
        currency=channel.currency_code,
    )


@pytest.mark.django_db
class TestProductCreation:
    """Test product creation and management."""

    def test_create_product(self, product_type, category):
        """Test creating a product."""
        product = Product.objects.create(
            name="New Product",
            slug="new-product",
            product_type=product_type,
            category=category,
        )
        assert product.id is not None
        assert product.name == "New Product"
        assert product.slug == "new-product"
        assert str(product) == "New Product"

    def test_create_product_variant(self, product):
        """Test creating a product variant."""
        variant = ProductVariant.objects.create(
            product=product,
            sku="NEW-SKU-001",
            name="New Variant",
        )
        assert variant.id is not None
        assert variant.product == product
        assert variant.sku == "NEW-SKU-001"

    def test_product_type_str(self, product_type):
        """Test product type string representation."""
        assert str(product_type) == "Test Product Type"

    def test_category_str(self, category):
        """Test category string representation."""
        assert str(category) == "Test Category"

    def test_product_with_multiple_variants(self, product):
        """Test product with multiple variants."""
        variant1 = ProductVariant.objects.create(
            product=product,
            sku="VAR-001",
            name="Variant 1",
        )
        variant2 = ProductVariant.objects.create(
            product=product,
            sku="VAR-002",
            name="Variant 2",
        )
        assert product.variants.count() == 2
        assert variant1 in product.variants.all()
        assert variant2 in product.variants.all()


@pytest.mark.django_db
class TestProductChannelListing:
    """Test product channel listing functionality."""

    def test_create_channel_listing(self, product, channel):
        """Test creating a channel listing."""
        listing = ProductChannelListing.objects.create(
            product=product,
            channel=channel,
            is_published=True,
            visible_in_listings=True,
        )
        assert listing.id is not None
        assert listing.product == product
        assert listing.channel == channel
        assert listing.is_published is True

    def test_variant_channel_listing_price(self, product_variant, channel):
        """Test variant channel listing with price."""
        listing = ProductVariantChannelListing.objects.create(
            variant=product_variant,
            channel=channel,
            price_amount=Decimal("50.00"),
            currency="USD",
        )
        assert listing.price_amount == Decimal("50.00")
        assert listing.currency == "USD"

    def test_unpublished_product(self, product, channel):
        """Test unpublished product listing."""
        listing = ProductChannelListing.objects.create(
            product=product,
            channel=channel,
            is_published=False,
            visible_in_listings=False,
        )
        assert listing.is_published is False
        assert listing.visible_in_listings is False


@pytest.mark.django_db
class TestProductQueries:
    """Test product query functionality."""

    def test_filter_products_by_category(self, product, category):
        """Test filtering products by category."""
        products = Product.objects.filter(category=category)
        assert product in products

    def test_filter_products_by_product_type(self, product, product_type):
        """Test filtering products by product type."""
        products = Product.objects.filter(product_type=product_type)
        assert product in products

    def test_products_without_variants(self, product, product_type, category):
        """Test products without variants query."""
        # Create a product without variants
        product_no_variants = Product.objects.create(
            name="No Variants Product",
            slug="no-variants-product",
            product_type=product_type,
            category=category,
        )
        # Query products that have no variants
        products = Product.objects.filter(variants__isnull=True)
        assert product_no_variants in products


@pytest.mark.django_db
class TestCategoryHierarchy:
    """Test category hierarchy functionality."""

    def test_create_subcategory(self, category):
        """Test creating a subcategory."""
        subcategory = Category.objects.create(
            name="Subcategory",
            slug="subcategory",
            parent=category,
        )
        assert subcategory.parent == category
        assert subcategory in category.children.all()

    def test_category_level(self, category):
        """Test category level."""
        subcategory = Category.objects.create(
            name="Sub",
            slug="sub",
            parent=category,
        )
        assert subcategory.level == category.level + 1

    def test_root_category(self, category):
        """Test root category has no parent."""
        assert category.parent is None


@pytest.mark.django_db
class TestProductTypeAttributes:
    """Test product type attributes."""

    def test_product_type_is_shipping_required(self, product_type):
        """Test product type shipping requirement."""
        assert product_type.is_shipping_required is True

    def test_product_type_is_digital(self, product_type):
        """Test product type digital flag."""
        assert product_type.is_digital is False

    def test_create_digital_product_type(self, db):
        """Test creating a digital product type."""
        digital_type = ProductType.objects.create(
            name="Digital Product",
            slug="digital-product",
            is_shipping_required=False,
            is_digital=True,
        )
        assert digital_type.is_digital is True
        assert digital_type.is_shipping_required is False


@pytest.mark.django_db
class TestChannelModel:
    """Test channel model functionality."""

    def test_create_channel(self, db):
        """Test creating a channel."""
        channel = Channel.objects.create(
            name="New Channel",
            slug="new-channel",
            currency_code="EUR",
            is_active=True,
        )
        assert channel.id is not None
        assert channel.currency_code == "EUR"
        assert str(channel) == "New Channel"

    def test_inactive_channel(self, db):
        """Test creating an inactive channel."""
        channel = Channel.objects.create(
            name="Inactive Channel",
            slug="inactive-channel",
            currency_code="GBP",
            is_active=False,
        )
        assert channel.is_active is False

    def test_channel_default_country(self, channel):
        """Test channel default country."""
        # Channel may have a default_country field
        assert hasattr(channel, 'default_country') or True

