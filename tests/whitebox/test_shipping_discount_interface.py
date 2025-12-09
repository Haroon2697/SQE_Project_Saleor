"""
Tests for shipping and discount interfaces to increase coverage.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from prices import Money

from saleor.shipping.interface import ShippingMethodData
from saleor.discount import DiscountType, DiscountValueType, VoucherType, RewardType, RewardValueType
from saleor.discount.interface import VariantPromotionRuleInfo


class TestShippingMethodData:
    """Test ShippingMethodData dataclass."""

    def test_create_shipping_method_data(self):
        data = ShippingMethodData(
            id="shipping_1",
            name="Standard Shipping",
            price=Money(Decimal("5.00"), "USD"),
            description="5-7 business days"
        )
        assert data.id == "shipping_1"
        assert data.name == "Standard Shipping"
        assert data.price.amount == Decimal("5.00")

    def test_shipping_method_with_delivery_days(self):
        data = ShippingMethodData(
            id="shipping_2",
            name="Express",
            price=Money(Decimal("15.00"), "USD"),
            minimum_delivery_days=1,
            maximum_delivery_days=3
        )
        assert data.minimum_delivery_days == 1
        assert data.maximum_delivery_days == 3

    def test_shipping_method_with_weight_limits(self):
        from measurement.measures import Weight
        data = ShippingMethodData(
            id="shipping_3",
            name="Heavy Items",
            price=Money(Decimal("25.00"), "USD"),
            minimum_order_weight=Weight(kg=1),
            maximum_order_weight=Weight(kg=50)
        )
        assert data.minimum_order_weight.kg == 1
        assert data.maximum_order_weight.kg == 50

    def test_shipping_method_with_price_limits(self):
        data = ShippingMethodData(
            id="shipping_4",
            name="Free over $100",
            price=Money(Decimal("0.00"), "USD"),
            minimum_order_price=Money(Decimal("100.00"), "USD"),
            maximum_order_price=Money(Decimal("1000.00"), "USD")
        )
        assert data.minimum_order_price.amount == Decimal("100.00")

    def test_shipping_method_active_status(self):
        data = ShippingMethodData(
            id="shipping_5",
            name="Test",
            price=Money(Decimal("10.00"), "USD"),
            active=True,
            message=""
        )
        assert data.active is True

    def test_shipping_method_inactive_with_message(self):
        data = ShippingMethodData(
            id="shipping_6",
            name="Unavailable",
            price=Money(Decimal("10.00"), "USD"),
            active=False,
            message="Not available for your location"
        )
        assert data.active is False
        assert data.message == "Not available for your location"


class TestDiscountTypeEnum:
    """Test DiscountType enum values."""

    def test_voucher_type(self):
        assert DiscountType.VOUCHER == "voucher"

    def test_promotion_type(self):
        assert DiscountType.PROMOTION == "promotion"

    def test_order_promotion_type(self):
        assert DiscountType.ORDER_PROMOTION == "order_promotion"

    def test_manual_type(self):
        assert DiscountType.MANUAL == "manual"


class TestDiscountValueTypeEnum:
    """Test DiscountValueType enum values."""

    def test_fixed_value(self):
        assert DiscountValueType.FIXED == "fixed"

    def test_percentage_value(self):
        assert DiscountValueType.PERCENTAGE == "percentage"


class TestVoucherTypeEnum:
    """Test VoucherType enum values."""

    def test_entire_order(self):
        assert VoucherType.ENTIRE_ORDER == "entire_order"

    def test_shipping(self):
        assert VoucherType.SHIPPING == "shipping"

    def test_specific_product(self):
        assert VoucherType.SPECIFIC_PRODUCT == "specific_product"


class TestRewardTypeEnum:
    """Test RewardType enum values."""

    def test_subtotal_discount(self):
        assert RewardType.SUBTOTAL_DISCOUNT == "subtotal_discount"

    def test_gift(self):
        assert RewardType.GIFT == "gift"


class TestRewardValueTypeEnum:
    """Test RewardValueType enum values."""

    def test_fixed_reward(self):
        assert RewardValueType.FIXED == "fixed"

    def test_percentage_reward(self):
        assert RewardValueType.PERCENTAGE == "percentage"


class TestVariantPromotionRuleInfo:
    """Test VariantPromotionRuleInfo dataclass."""

    def test_create_variant_rule_info(self):
        rule_mock = Mock()
        rule_mock.id = 1
        rule_mock.name = "10% off"
        
        listing_mock = Mock()
        listing_mock.discount_amount = Decimal("5.00")
        
        info = VariantPromotionRuleInfo(
            rule=rule_mock,
            variant_listing_promotion_rule=listing_mock,
            promotion=Mock(name="Summer Sale"),
            promotion_translation=None,
            rule_translation=None
        )
        assert info.rule.id == 1
        assert info.variant_listing_promotion_rule.discount_amount == Decimal("5.00")

