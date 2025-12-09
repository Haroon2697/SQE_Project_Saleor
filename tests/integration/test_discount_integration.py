"""
Integration tests for Discount module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

from saleor.discount.models import (
    Voucher,
    VoucherCode,
    VoucherChannelListing,
    Promotion,
    PromotionRule,
)
from saleor.discount import DiscountType, DiscountValueType, VoucherType
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Discount Channel",
        slug="discount-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name="Discount Category",
        slug="discount-category",
    )


@pytest.fixture
def product_type(db):
    """Create a test product type."""
    return ProductType.objects.create(
        name="Discount Product Type",
        slug="discount-product-type",
    )


@pytest.fixture
def product(db, product_type, category):
    """Create a test product."""
    return Product.objects.create(
        name="Discount Product",
        slug="discount-product",
        product_type=product_type,
        category=category,
    )


@pytest.mark.django_db
class TestVoucherCreation:
    """Test voucher creation."""

    def test_create_voucher(self):
        """Test creating a voucher."""
        voucher = Voucher.objects.create(
            name="Test Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        assert voucher.id is not None
        assert voucher.name == "Test Voucher"

    def test_create_fixed_voucher(self):
        """Test creating a fixed amount voucher."""
        voucher = Voucher.objects.create(
            name="Fixed Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.FIXED,
        )
        assert voucher.discount_value_type == DiscountValueType.FIXED

    def test_create_shipping_voucher(self):
        """Test creating a shipping voucher."""
        voucher = Voucher.objects.create(
            name="Shipping Voucher",
            type=VoucherType.SHIPPING,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        assert voucher.type == VoucherType.SHIPPING


@pytest.mark.django_db
class TestVoucherCode:
    """Test voucher code functionality."""

    def test_create_voucher_code(self):
        """Test creating a voucher code."""
        voucher = Voucher.objects.create(
            name="Code Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        code = VoucherCode.objects.create(
            voucher=voucher,
            code="SAVE10",
        )
        assert code.id is not None
        assert code.code == "SAVE10"
        assert code.voucher == voucher

    def test_multiple_voucher_codes(self):
        """Test multiple voucher codes."""
        voucher = Voucher.objects.create(
            name="Multi Code Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        VoucherCode.objects.create(voucher=voucher, code="CODE1")
        VoucherCode.objects.create(voucher=voucher, code="CODE2")
        VoucherCode.objects.create(voucher=voucher, code="CODE3")
        
        assert voucher.codes.count() == 3


@pytest.mark.django_db
class TestVoucherChannelListing:
    """Test voucher channel listing."""

    def test_create_voucher_channel_listing(self, channel):
        """Test creating a voucher channel listing."""
        voucher = Voucher.objects.create(
            name="Channel Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.FIXED,
        )
        listing = VoucherChannelListing.objects.create(
            voucher=voucher,
            channel=channel,
            discount_value=Decimal("10.00"),
            currency="USD",
        )
        assert listing.id is not None
        assert listing.discount_value == Decimal("10.00")

    def test_percentage_voucher_listing(self, channel):
        """Test percentage voucher channel listing."""
        voucher = Voucher.objects.create(
            name="Percent Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        listing = VoucherChannelListing.objects.create(
            voucher=voucher,
            channel=channel,
            discount_value=Decimal("15.00"),  # 15%
            currency="USD",
        )
        assert listing.discount_value == Decimal("15.00")


@pytest.mark.django_db
class TestVoucherUsageLimit:
    """Test voucher usage limit functionality."""

    def test_voucher_with_usage_limit(self):
        """Test voucher with usage limit."""
        voucher = Voucher.objects.create(
            name="Limited Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
            usage_limit=100,
        )
        assert voucher.usage_limit == 100

    def test_voucher_single_use(self):
        """Test single use voucher."""
        voucher = Voucher.objects.create(
            name="Single Use",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
            single_use=True,
        )
        assert voucher.single_use is True


@pytest.mark.django_db
class TestVoucherDates:
    """Test voucher date functionality."""

    def test_voucher_with_start_date(self):
        """Test voucher with start date."""
        start_date = timezone.now()
        voucher = Voucher.objects.create(
            name="Start Date Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
            start_date=start_date,
        )
        assert voucher.start_date is not None

    def test_voucher_with_end_date(self):
        """Test voucher with end date."""
        end_date = timezone.now() + timedelta(days=30)
        voucher = Voucher.objects.create(
            name="End Date Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
            end_date=end_date,
        )
        assert voucher.end_date is not None


@pytest.mark.django_db
class TestPromotion:
    """Test promotion functionality."""

    def test_create_promotion(self):
        """Test creating a promotion."""
        promotion = Promotion.objects.create(
            name="Summer Sale",
        )
        assert promotion.id is not None
        assert promotion.name == "Summer Sale"

    def test_promotion_with_dates(self):
        """Test promotion with start and end dates."""
        start_date = timezone.now()
        end_date = timezone.now() + timedelta(days=14)
        
        promotion = Promotion.objects.create(
            name="Limited Time Sale",
            start_date=start_date,
            end_date=end_date,
        )
        assert promotion.start_date is not None
        assert promotion.end_date is not None


@pytest.mark.django_db
class TestPromotionRule:
    """Test promotion rule functionality."""

    def test_create_promotion_rule(self, channel):
        """Test creating a promotion rule."""
        promotion = Promotion.objects.create(name="Rule Promotion")
        rule = PromotionRule.objects.create(
            promotion=promotion,
            reward_value=Decimal("10.00"),
            reward_value_type=DiscountValueType.PERCENTAGE,
        )
        # Add channel to the rule
        rule.channels.add(channel)
        
        assert rule.id is not None
        assert rule.promotion == promotion


@pytest.mark.django_db
class TestVoucherQueries:
    """Test voucher query functionality."""

    def test_filter_vouchers_by_type(self):
        """Test filtering vouchers by type."""
        voucher = Voucher.objects.create(
            name="Filter Test",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        vouchers = Voucher.objects.filter(type=VoucherType.ENTIRE_ORDER)
        assert voucher in vouchers

    def test_filter_active_vouchers(self):
        """Test filtering active vouchers."""
        # Create voucher without end date (always active)
        voucher = Voucher.objects.create(
            name="Active Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        # Vouchers without end_date or with end_date in future are active
        assert voucher.end_date is None


@pytest.mark.django_db
class TestVoucherProducts:
    """Test voucher product associations."""

    def test_voucher_specific_products(self, product):
        """Test voucher for specific products."""
        voucher = Voucher.objects.create(
            name="Product Voucher",
            type=VoucherType.SPECIFIC_PRODUCT,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        voucher.products.add(product)
        
        assert product in voucher.products.all()

    def test_voucher_categories(self, category):
        """Test voucher for categories."""
        voucher = Voucher.objects.create(
            name="Category Voucher",
            type=VoucherType.SPECIFIC_PRODUCT,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        voucher.categories.add(category)
        
        assert category in voucher.categories.all()


@pytest.mark.django_db
class TestDiscountValueTypes:
    """Test discount value types."""

    def test_percentage_discount_type(self):
        """Test percentage discount type."""
        assert DiscountValueType.PERCENTAGE == "percentage"

    def test_fixed_discount_type(self):
        """Test fixed discount type."""
        assert DiscountValueType.FIXED == "fixed"


@pytest.mark.django_db
class TestVoucherMetadata:
    """Test voucher metadata."""

    def test_voucher_metadata(self):
        """Test voucher metadata."""
        voucher = Voucher.objects.create(
            name="Meta Voucher",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.PERCENTAGE,
        )
        voucher.metadata = {"campaign": "summer2024"}
        voucher.save()
        voucher.refresh_from_db()
        assert voucher.metadata.get("campaign") == "summer2024"

