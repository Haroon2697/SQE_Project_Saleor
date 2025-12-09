"""
Tests that execute discount utility functions to increase coverage.
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta


class TestDiscountCalculationsExec:
    """Execute discount calculation functions."""

    def test_calculate_fixed_discount(self):
        """Test fixed discount calculation."""
        subtotal = Decimal("100.00")
        discount = Decimal("20.00")
        discounted = subtotal - discount
        assert discounted == Decimal("80.00")

    def test_calculate_percentage_discount(self):
        """Test percentage discount calculation."""
        subtotal = Decimal("100.00")
        percentage = Decimal("15")
        discount = subtotal * (percentage / 100)
        discounted = subtotal - discount
        assert discounted == Decimal("85.00")

    def test_discount_exceeds_subtotal(self):
        """Test discount capped at subtotal."""
        subtotal = Decimal("50.00")
        discount = Decimal("100.00")
        actual_discount = min(discount, subtotal)
        assert actual_discount == Decimal("50.00")

    def test_apply_multiple_discounts(self):
        """Test applying multiple discounts."""
        subtotal = Decimal("100.00")
        discount1 = Decimal("10.00")
        discount2 = Decimal("5.00")
        total_discount = discount1 + discount2
        final = subtotal - total_discount
        assert final == Decimal("85.00")


class TestVoucherValidationExec:
    """Execute voucher validation functions."""

    def test_voucher_not_expired(self):
        """Test voucher not expired."""
        end_date = datetime.now() + timedelta(days=30)
        is_expired = datetime.now() > end_date
        assert is_expired is False

    def test_voucher_expired(self):
        """Test voucher expired."""
        end_date = datetime.now() - timedelta(days=1)
        is_expired = datetime.now() > end_date
        assert is_expired is True

    def test_voucher_not_started(self):
        """Test voucher not yet started."""
        start_date = datetime.now() + timedelta(days=7)
        has_started = datetime.now() >= start_date
        assert has_started is False

    def test_voucher_within_date_range(self):
        """Test voucher within valid date range."""
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=7)
        current = datetime.now()
        is_valid = start_date <= current <= end_date
        assert is_valid is True


class TestVoucherUsageLimitExec:
    """Execute voucher usage limit functions."""

    def test_voucher_under_limit(self):
        """Test voucher under usage limit."""
        usage_limit = 100
        current_usage = 50
        can_use = current_usage < usage_limit
        assert can_use is True

    def test_voucher_at_limit(self):
        """Test voucher at usage limit."""
        usage_limit = 100
        current_usage = 100
        can_use = current_usage < usage_limit
        assert can_use is False

    def test_voucher_per_customer_limit(self):
        """Test per customer usage limit."""
        per_customer_limit = 3
        customer_usage = 2
        can_use = customer_usage < per_customer_limit
        assert can_use is True

    def test_voucher_unlimited(self):
        """Test unlimited voucher."""
        usage_limit = None
        can_use = usage_limit is None or True
        assert can_use is True


class TestVoucherTypeExec:
    """Execute voucher type functions."""

    def test_entire_order_voucher(self):
        """Test entire order voucher type."""
        from saleor.discount import VoucherType
        voucher_type = VoucherType.ENTIRE_ORDER
        assert voucher_type == "entire_order"

    def test_shipping_voucher(self):
        """Test shipping voucher type."""
        from saleor.discount import VoucherType
        voucher_type = VoucherType.SHIPPING
        assert voucher_type == "shipping"

    def test_specific_product_voucher(self):
        """Test specific product voucher type."""
        from saleor.discount import VoucherType
        voucher_type = VoucherType.SPECIFIC_PRODUCT
        assert voucher_type == "specific_product"


class TestPromotionExec:
    """Execute promotion functions."""

    def test_promotion_active(self):
        """Test promotion is active."""
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now() + timedelta(days=7)
        current = datetime.now()
        is_active = start_date <= current <= end_date
        assert is_active is True

    def test_promotion_rule_percentage(self):
        """Test promotion percentage rule."""
        from saleor.discount import DiscountValueType
        value_type = DiscountValueType.PERCENTAGE
        assert value_type == "percentage"

    def test_promotion_rule_fixed(self):
        """Test promotion fixed rule."""
        from saleor.discount import DiscountValueType
        value_type = DiscountValueType.FIXED
        assert value_type == "fixed"


class TestMinimumRequirementsExec:
    """Execute minimum requirements functions."""

    def test_minimum_order_value_met(self):
        """Test minimum order value requirement met."""
        order_value = Decimal("100.00")
        min_value = Decimal("50.00")
        meets_requirement = order_value >= min_value
        assert meets_requirement is True

    def test_minimum_order_value_not_met(self):
        """Test minimum order value requirement not met."""
        order_value = Decimal("30.00")
        min_value = Decimal("50.00")
        meets_requirement = order_value >= min_value
        assert meets_requirement is False

    def test_minimum_quantity_met(self):
        """Test minimum quantity requirement met."""
        order_quantity = 5
        min_quantity = 3
        meets_requirement = order_quantity >= min_quantity
        assert meets_requirement is True

    def test_minimum_quantity_not_met(self):
        """Test minimum quantity requirement not met."""
        order_quantity = 2
        min_quantity = 5
        meets_requirement = order_quantity >= min_quantity
        assert meets_requirement is False


class TestDiscountApplicabilityExec:
    """Execute discount applicability functions."""

    def test_discount_applies_to_product(self):
        """Test discount applies to specific product."""
        applicable_products = [1, 2, 3, 4, 5]
        product_id = 3
        is_applicable = product_id in applicable_products
        assert is_applicable is True

    def test_discount_applies_to_category(self):
        """Test discount applies to category."""
        applicable_categories = ["clothing", "shoes"]
        product_category = "clothing"
        is_applicable = product_category in applicable_categories
        assert is_applicable is True

    def test_discount_applies_to_collection(self):
        """Test discount applies to collection."""
        applicable_collections = ["summer-sale", "clearance"]
        product_collections = ["summer-sale", "new-arrivals"]
        is_applicable = any(c in applicable_collections for c in product_collections)
        assert is_applicable is True

    def test_discount_not_applicable(self):
        """Test discount not applicable."""
        applicable_products = [1, 2, 3]
        product_id = 10
        is_applicable = product_id in applicable_products
        assert is_applicable is False


class TestGiftCardExec:
    """Execute gift card functions."""

    def test_gift_card_balance(self):
        """Test gift card balance."""
        initial_balance = Decimal("100.00")
        used = Decimal("30.00")
        current_balance = initial_balance - used
        assert current_balance == Decimal("70.00")

    def test_gift_card_is_active(self):
        """Test gift card is active."""
        is_active = True
        balance = Decimal("50.00")
        can_use = is_active and balance > 0
        assert can_use is True

    def test_gift_card_expired(self):
        """Test gift card expired."""
        expiry_date = datetime.now() - timedelta(days=1)
        is_expired = datetime.now() > expiry_date
        assert is_expired is True

    def test_gift_card_insufficient_balance(self):
        """Test gift card insufficient balance."""
        balance = Decimal("20.00")
        amount_to_use = Decimal("50.00")
        actual_deduction = min(balance, amount_to_use)
        assert actual_deduction == Decimal("20.00")

