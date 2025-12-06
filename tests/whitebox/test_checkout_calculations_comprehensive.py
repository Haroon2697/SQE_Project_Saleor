"""
Comprehensive White-Box Testing - Checkout Base Calculations
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/checkout/base_calculations.py (all functions)
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.checkout.base_calculations import (
    calculate_base_line_unit_price,
    calculate_base_line_total_price,
    calculate_undiscounted_base_line_total_price,
    calculate_undiscounted_base_line_unit_price,
    base_checkout_delivery_price,
    base_checkout_undiscounted_delivery_price,
)
from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.fetch import CheckoutLineInfo, CheckoutInfo
from saleor.product.models import Product, ProductType, Category, ProductVariant, ProductVariantChannelListing
from saleor.channel.models import Channel
from saleor.shipping.models import ShippingZone, ShippingMethod, ShippingMethodChannelListing
from saleor.discount.models import Voucher, VoucherType
from prices import Money


# ============================================
# TEST 1: calculate_base_line_unit_price - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCalculateBaseLineUnitPrice:
    """Test calculate_base_line_unit_price() for statement coverage"""
    
    def test_calculate_base_line_unit_price_basic(self):
        """Statement Coverage: Basic calculation without discounts"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        # Create CheckoutLineInfo
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        unit_price = calculate_base_line_unit_price(line_info)
        
        assert unit_price.amount == Decimal("10.00")
        assert unit_price.currency == "USD"
    
    def test_calculate_base_line_unit_price_with_discounts(self):
        """Statement Coverage: Calculation with discounts"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        # Mock discount
        discount = Mock()
        discount.amount_value = Decimal("2.00")
        
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[discount],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        unit_price = calculate_base_line_unit_price(line_info)
        
        # Should be (10 * 2 - 2) / 2 = 9.00
        assert unit_price.amount == Decimal("9.00")
        assert unit_price.currency == "USD"


# ============================================
# TEST 2: calculate_base_line_total_price - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCalculateBaseLineTotalPrice:
    """Test calculate_base_line_total_price() for statement coverage"""
    
    def test_calculate_base_line_total_price_no_discounts(self):
        """Statement Coverage: No discounts, no voucher"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        total_price = calculate_base_line_total_price(line_info)
        
        assert total_price.amount == Decimal("20.00")
        assert total_price.currency == "USD"
    
    def test_calculate_base_line_total_price_with_discounts(self):
        """Statement Coverage: With discounts"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        discount = Mock()
        discount.amount_value = Decimal("2.00")
        
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[discount],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        total_price = calculate_base_line_total_price(line_info)
        
        # 10 * 2 - 2 = 18.00
        assert total_price.amount == Decimal("18.00")
        assert total_price.currency == "USD"
    
    def test_calculate_base_line_total_price_include_voucher_false(self):
        """Statement Coverage: include_voucher=False"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        voucher = Voucher.objects.create(
            code="TEST",
            type=VoucherType.SPECIFIC_PRODUCT
        )
        
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=voucher,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        # include_voucher=False should skip voucher calculation
        total_price = calculate_base_line_total_price(line_info, include_voucher=False)
        
        assert total_price.amount == Decimal("20.00")
        assert total_price.currency == "USD"


# ============================================
# TEST 3: calculate_undiscounted_base_line_total_price - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCalculateUndiscountedBaseLineTotalPrice:
    """Test calculate_undiscounted_base_line_total_price() for statement coverage"""
    
    def test_calculate_undiscounted_base_line_total_price(self):
        """Statement Coverage: Calculate undiscounted total"""
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
        
        ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3
        )
        
        line_info = CheckoutLineInfo(
            line=checkout_line,
            variant=variant,
            channel_listing=variant.channel_listings.first(),
            product=product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        total_price = calculate_undiscounted_base_line_total_price(line_info, channel)
        
        assert total_price.amount == Decimal("30.00")
        assert total_price.currency == "USD"


# ============================================
# TEST 4: base_checkout_delivery_price - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseCheckoutDeliveryPrice:
    """Test base_checkout_delivery_price() for statement coverage"""
    
    def test_base_checkout_delivery_price_no_voucher(self):
        """Statement Coverage: No voucher -> return shipping price"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        zone = ShippingZone.objects.create(
            name="Zone",
            countries=["US"]
        )
        
        shipping_method = ShippingMethod.objects.create(
            name="Standard",
            type="PRICE_BASED",
            shipping_zone=zone
        )
        
        ShippingMethodChannelListing.objects.create(
            shipping_method=shipping_method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency=channel.currency_code
        )
        
        # Create CheckoutInfo mock
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.voucher = None
        checkout_info.shipping_method_info = Mock()
        checkout_info.shipping_method_info.price = Money(Decimal("10.00"), "USD")
        
        delivery_price = base_checkout_delivery_price(checkout_info)
        
        assert delivery_price.amount == Decimal("10.00")
        assert delivery_price.currency == "USD"

