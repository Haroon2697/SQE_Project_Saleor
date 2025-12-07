"""
Extensive White-Box Tests for saleor/checkout/base_calculations.py

Target: Increase checkout module coverage from 31.5% to 70%+
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from prices import Money, TaxedMoney

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.base_calculations import (
    calculate_base_line_unit_price,
    calculate_base_line_total_price,
    calculate_undiscounted_base_line_total_price,
    calculate_undiscounted_base_line_unit_price,
    base_checkout_delivery_price,
    base_checkout_undiscounted_delivery_price,
    calculate_base_price_for_shipping_method,
    base_checkout_total,
    base_checkout_subtotal,
    checkout_total,
    get_line_total_price_with_propagated_checkout_discount,
    _propagate_checkout_discount_on_checkout_lines_prices,
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType, Category
from saleor.shipping.models import ShippingMethod, ShippingZone, ShippingMethodChannelListing
from saleor.discount.models import CheckoutDiscount, DiscountType, DiscountValueType


@pytest.mark.django_db
class TestCalculateBaseLineUnitPrice:
    """Test calculate_base_line_unit_price()"""

    def test_calculate_base_line_unit_price_returns_channel_listing_price(self):
        """Statement: Return channel listing price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        channel_listing = Mock()
        channel_listing.price = Money(Decimal("10.00"), "USD")
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = channel_listing
        
        result = calculate_base_line_unit_price(line_info, channel, "USD")
        
        assert result == Money(Decimal("10.00"), "USD")

    def test_calculate_base_line_unit_price_handles_custom_price(self):
        """Statement: Handle custom price override"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            price_override_amount=Decimal("15.00")
        )
        channel_listing = Mock()
        channel_listing.price = Money(Decimal("10.00"), "USD")
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = channel_listing
        
        result = calculate_base_line_unit_price(line_info, channel, "USD")
        
        assert result == Money(Decimal("15.00"), "USD")


@pytest.mark.django_db
class TestCalculateBaseLineTotalPrice:
    """Test calculate_base_line_total_price()"""

    def test_calculate_base_line_total_price_multiplies_by_quantity(self):
        """Statement: Multiply unit price by quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3
        )
        channel_listing = Mock()
        channel_listing.price = Money(Decimal("10.00"), "USD")
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = channel_listing
        
        with patch('saleor.checkout.base_calculations.calculate_base_line_unit_price', return_value=Money(Decimal("10.00"), "USD")):
            result = calculate_base_line_total_price(line_info, channel, "USD")
            
            assert result == Money(Decimal("30.00"), "USD")  # 10.00 * 3


@pytest.mark.django_db
class TestBaseCheckoutDeliveryPrice:
    """Test base_checkout_delivery_price()"""

    def test_base_checkout_delivery_price_returns_zero_when_no_shipping_method(self):
        """Statement: Return zero when no shipping method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.shipping_method = None
        lines_info = []
        
        result = base_checkout_delivery_price(checkout_info, lines_info, include_voucher=False)
        
        assert result == Money(Decimal("0.00"), "USD")

    def test_base_checkout_delivery_price_returns_shipping_method_price(self):
        """Statement: Return shipping method price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        zone.channels.add(channel)
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency="USD"
        )
        shipping_method_data = Mock()
        shipping_method_data.price = Money(Decimal("10.00"), "USD")
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.shipping_method = shipping_method_data
        lines_info = []
        
        result = base_checkout_delivery_price(checkout_info, lines_info, include_voucher=False)
        
        assert result == Money(Decimal("10.00"), "USD")


@pytest.mark.django_db
class TestBaseCheckoutSubtotal:
    """Test base_checkout_subtotal()"""

    def test_base_checkout_subtotal_sums_line_totals(self):
        """Statement: Sum all line totals"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        line_info1 = Mock()
        line_info1.line = line1
        line_info1.channel_listing = Mock()
        line_info1.channel_listing.price = Money(Decimal("10.00"), "USD")
        line_info2 = Mock()
        line_info2.line = line2
        line_info2.channel_listing = Mock()
        line_info2.channel_listing.price = Money(Decimal("20.00"), "USD")
        
        with patch('saleor.checkout.base_calculations.calculate_base_line_total_price') as mock_calc:
            mock_calc.side_effect = [
                Money(Decimal("20.00"), "USD"),  # 10.00 * 2
                Money(Decimal("20.00"), "USD")   # 20.00 * 1
            ]
            result = base_checkout_subtotal([line_info1, line_info2], channel, "USD", include_voucher=False)
            
            assert result == Money(Decimal("40.00"), "USD")  # 20.00 + 20.00


@pytest.mark.django_db
class TestBaseCheckoutTotal:
    """Test base_checkout_total()"""

    def test_base_checkout_total_adds_subtotal_and_shipping(self):
        """Statement: Add subtotal and shipping price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines_info = []
        
        with patch('saleor.checkout.base_calculations.base_checkout_subtotal', return_value=Money(Decimal("100.00"), "USD")):
            with patch('saleor.checkout.base_calculations.base_checkout_delivery_price', return_value=Money(Decimal("10.00"), "USD")):
                result = base_checkout_total(checkout_info, lines_info, include_voucher=False)
                
                assert result == Money(Decimal("110.00"), "USD")  # 100.00 + 10.00


@pytest.mark.django_db
class TestCheckoutTotal:
    """Test checkout_total()"""

    def test_checkout_total_includes_discounts(self):
        """Statement: Include discounts in total calculation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("5.00")
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.base_calculations.base_checkout_total', return_value=Money(Decimal("100.00"), "USD")):
            result = checkout_total(checkout_info, [], include_voucher=False)
            
            # Should subtract discount: 100.00 - 5.00 = 95.00
            assert result == Money(Decimal("95.00"), "USD")


@pytest.mark.django_db
class TestGetLineTotalPriceWithPropagatedCheckoutDiscount:
    """Test get_line_total_price_with_propagated_checkout_discount()"""

    def test_get_line_total_price_with_propagated_discount_applies_discount(self):
        """Statement: Apply propagated discount to line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = Mock()
        line_info.channel_listing.price = Money(Decimal("10.00"), "USD")
        
        # Mock base total price
        base_total = Money(Decimal("20.00"), "USD")  # 10.00 * 2
        checkout_discount = Money(Decimal("5.00"), "USD")
        checkout_subtotal = Money(Decimal("100.00"), "USD")
        
        result = get_line_total_price_with_propagated_checkout_discount(
            line_info,
            channel,
            "USD",
            base_total,
            checkout_discount,
            checkout_subtotal
        )
        
        # Discount should be proportional: (20.00 / 100.00) * 5.00 = 1.00
        # So result should be: 20.00 - 1.00 = 19.00
        assert result == Money(Decimal("19.00"), "USD")

    def test_get_line_total_price_with_propagated_discount_handles_zero_subtotal(self):
        """Statement: Handle zero subtotal gracefully"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = Mock()
        line_info.channel_listing.price = Money(Decimal("10.00"), "USD")
        
        base_total = Money(Decimal("20.00"), "USD")
        checkout_discount = Money(Decimal("5.00"), "USD")
        checkout_subtotal = Money(Decimal("0.00"), "USD")
        
        result = get_line_total_price_with_propagated_checkout_discount(
            line_info,
            channel,
            "USD",
            base_total,
            checkout_discount,
            checkout_subtotal
        )
        
        # Should return base_total when subtotal is zero
        assert result == base_total


@pytest.mark.django_db
class TestCalculateBasePriceForShippingMethod:
    """Test calculate_base_price_for_shipping_method()"""

    def test_calculate_base_price_returns_shipping_method_price(self):
        """Statement: Return shipping method price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        zone.channels.add(channel)
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("15.00"),
            currency="USD"
        )
        shipping_method_data = Mock()
        shipping_method_data.price = Money(Decimal("15.00"), "USD")
        
        result = calculate_base_price_for_shipping_method(
            shipping_method_data,
            channel,
            "USD"
        )
        
        assert result == Money(Decimal("15.00"), "USD")

    def test_calculate_base_price_returns_zero_when_no_method(self):
        """Statement: Return zero when no shipping method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        result = calculate_base_price_for_shipping_method(
            None,
            channel,
            "USD"
        )
        
        assert result == Money(Decimal("0.00"), "USD")

