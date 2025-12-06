"""
White-Box Testing - Discount Utils
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/discount/utils/promotion.py
- saleor/discount/utils/voucher.py
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.discount.utils.promotion import (
    calculate_discounted_price_for_rules,
    prepare_promotion_discount_reason,
    get_sale_id
)
from saleor.discount.utils.voucher import (
    is_order_level_voucher,
    is_shipping_voucher,
    get_the_cheapest_line
)
from saleor.discount.models import Promotion, PromotionRule, Voucher, VoucherType
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category
from prices import Money


# ============================================
# TEST 1: calculate_discounted_price_for_rules - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCalculateDiscountedPriceForRules:
    """Test calculate_discounted_price_for_rules() for statement coverage"""
    
    def test_calculate_discounted_price_no_rules(self):
        """Statement Coverage: empty rules list -> return original price"""
        price = Money(Decimal("100.00"), "USD")
        rules = []
        
        result = calculate_discounted_price_for_rules(
            price=price,
            rules=rules,
            currency="USD"
        )
        
        assert result == price
        assert result.amount == Decimal("100.00")
    
    def test_calculate_discounted_price_with_rules(self):
        """Statement Coverage: rules with discounts"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE"
        )
        
        rule = PromotionRule.objects.create(
            promotion=promotion,
            name="Rule 1",
            reward_value_type="FIXED",
            reward_value=Decimal("10.00")
        )
        
        price = Money(Decimal("100.00"), "USD")
        
        result = calculate_discounted_price_for_rules(
            price=price,
            rules=[rule],
            currency="USD"
        )
        
        # Should apply discount
        assert result.amount < price.amount
        assert result.currency == "USD"
    
    def test_calculate_discounted_price_multiple_rules(self):
        """Statement Coverage: multiple rules -> sum discounts"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE"
        )
        
        rule1 = PromotionRule.objects.create(
            promotion=promotion,
            name="Rule 1",
            reward_value_type="FIXED",
            reward_value=Decimal("10.00")
        )
        
        rule2 = PromotionRule.objects.create(
            promotion=promotion,
            name="Rule 2",
            reward_value_type="FIXED",
            reward_value=Decimal("5.00")
        )
        
        price = Money(Decimal("100.00"), "USD")
        
        result = calculate_discounted_price_for_rules(
            price=price,
            rules=[rule1, rule2],
            currency="USD"
        )
        
        # Should apply both discounts
        assert result.amount < price.amount
        assert result.currency == "USD"
    
    def test_calculate_discounted_price_result_negative(self):
        """Statement Coverage: discount > price -> return zero_money"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE"
        )
        
        rule = PromotionRule.objects.create(
            promotion=promotion,
            name="Rule 1",
            reward_value_type="FIXED",
            reward_value=Decimal("150.00")  # More than price
        )
        
        price = Money(Decimal("100.00"), "USD")
        
        result = calculate_discounted_price_for_rules(
            price=price,
            rules=[rule],
            currency="USD"
        )
        
        # Should return zero (not negative)
        assert result.amount >= Decimal("0.00")
        assert result.currency == "USD"


# ============================================
# TEST 2: prepare_promotion_discount_reason - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestPreparePromotionDiscountReason:
    """Test prepare_promotion_discount_reason() for statement coverage"""
    
    def test_prepare_reason_with_old_sale_id(self):
        """Statement Coverage: promotion.old_sale_id exists"""
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE",
            old_sale_id=123
        )
        
        reason = prepare_promotion_discount_reason(promotion)
        
        assert "Sale:" in reason
        assert str(promotion.old_sale_id) in reason
    
    def test_prepare_reason_without_old_sale_id(self):
        """Statement Coverage: promotion.old_sale_id is None"""
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE",
            old_sale_id=None
        )
        
        reason = prepare_promotion_discount_reason(promotion)
        
        assert "Promotion:" in reason
        assert str(promotion.id) in reason


# ============================================
# TEST 3: get_sale_id - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetSaleId:
    """Test get_sale_id() for statement coverage"""
    
    def test_get_sale_id_with_old_sale_id(self):
        """Statement Coverage: old_sale_id exists"""
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE",
            old_sale_id=456
        )
        
        sale_id = get_sale_id(promotion)
        
        assert "Sale" in sale_id
        assert str(promotion.old_sale_id) in sale_id
    
    def test_get_sale_id_without_old_sale_id(self):
        """Statement Coverage: old_sale_id is None"""
        promotion = Promotion.objects.create(
            name="Test Promotion",
            type="CATALOGUE",
            old_sale_id=None
        )
        
        sale_id = get_sale_id(promotion)
        
        assert "Promotion" in sale_id
        assert str(promotion.id) in sale_id


# ============================================
# TEST 4: is_order_level_voucher - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestIsOrderLevelVoucher:
    """Test is_order_level_voucher() for statement coverage"""
    
    def test_is_order_level_voucher_entire_order(self):
        """Statement Coverage: voucher type is ENTIRE_ORDER"""
        voucher = Voucher.objects.create(
            code="TEST123",
            type=VoucherType.ENTIRE_ORDER
        )
        
        result = is_order_level_voucher(voucher)
        assert result is True
    
    def test_is_order_level_voucher_shipping(self):
        """Statement Coverage: voucher type is SHIPPING"""
        voucher = Voucher.objects.create(
            code="TEST123",
            type=VoucherType.SHIPPING
        )
        
        result = is_order_level_voucher(voucher)
        assert result is True
    
    def test_is_order_level_voucher_specific_product(self):
        """Statement Coverage: voucher type is SPECIFIC_PRODUCT"""
        voucher = Voucher.objects.create(
            code="TEST123",
            type=VoucherType.SPECIFIC_PRODUCT
        )
        
        result = is_order_level_voucher(voucher)
        assert result is False
    
    def test_is_order_level_voucher_none(self):
        """Statement Coverage: voucher is None"""
        result = is_order_level_voucher(None)
        assert result is False


# ============================================
# TEST 5: is_shipping_voucher - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestIsShippingVoucher:
    """Test is_shipping_voucher() for statement coverage"""
    
    def test_is_shipping_voucher_true(self):
        """Statement Coverage: voucher type is SHIPPING"""
        voucher = Voucher.objects.create(
            code="TEST123",
            type=VoucherType.SHIPPING
        )
        
        result = is_shipping_voucher(voucher)
        assert result is True
    
    def test_is_shipping_voucher_false(self):
        """Statement Coverage: voucher type is not SHIPPING"""
        voucher = Voucher.objects.create(
            code="TEST123",
            type=VoucherType.ENTIRE_ORDER
        )
        
        result = is_shipping_voucher(voucher)
        assert result is False
    
    def test_is_shipping_voucher_none(self):
        """Statement Coverage: voucher is None"""
        result = is_shipping_voucher(None)
        assert result is False

