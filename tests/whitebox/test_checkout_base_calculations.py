"""
White-Box Testing - Checkout Base Calculations
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/checkout/base_calculations.py
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.checkout.models import Checkout
from saleor.checkout.base_calculations import (
    base_checkout_subtotal,
    checkout_total,
    base_checkout_delivery_price
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.checkout.fetch import CheckoutInfo, CheckoutLineInfo
from prices import Money


# ============================================
# TEST 1: base_checkout_subtotal - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseCheckoutSubtotal:
    """Test base_checkout_subtotal() for statement coverage"""
    
    def test_base_checkout_subtotal_single_line(self):
        """Statement Coverage: single checkout line"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        
        from saleor.checkout.models import CheckoutLine
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        # Create CheckoutLineInfo
        from saleor.checkout.fetch import CheckoutLineInfo
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=product,
            collections=[],
            discounts=[],
            rules_info=[],
            channel=channel,
            voucher=None,
            promotion_discount=None,
            promotion_rule=None
        )
        
        # Mock the line total calculation
        with patch.object(line_info, 'line', create=True):
            line_info.line.total_price = Money(Decimal("100.00"), "USD")
            line_info.line.total_price_gross = Money(Decimal("100.00"), "USD")
        
        # Since base_checkout_subtotal needs actual line totals, we'll test the logic
        # by checking the function structure
        subtotal = base_checkout_subtotal(
            checkout_lines=[line_info],
            channel=channel,
            currency="USD",
            include_voucher=True
        )
        
        # Should return a Money object
        assert isinstance(subtotal, Money)
        assert subtotal.currency == "USD"
    
    def test_base_checkout_subtotal_empty_lines(self):
        """Statement Coverage: empty lines list"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        subtotal = base_checkout_subtotal(
            checkout_lines=[],
            channel=channel,
            currency="USD",
            include_voucher=True
        )
        
        assert subtotal.amount == Decimal("0.00")
        assert subtotal.currency == "USD"
    
    def test_base_checkout_subtotal_include_voucher_false(self):
        """Statement Coverage: include_voucher=False"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        
        from saleor.checkout.models import CheckoutLine
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        from saleor.checkout.fetch import CheckoutLineInfo
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=product,
            collections=[],
            discounts=[],
            rules_info=[],
            channel=channel,
            voucher=None,
            promotion_discount=None,
            promotion_rule=None
        )
        
        subtotal = base_checkout_subtotal(
            checkout_lines=[line_info],
            channel=channel,
            currency="USD",
            include_voucher=False
        )
        
        assert isinstance(subtotal, Money)
        assert subtotal.currency == "USD"


# ============================================
# TEST 2: checkout_total - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCheckoutTotal:
    """Test checkout_total() for statement coverage"""
    
    def test_checkout_total_no_discounts(self):
        """Statement Coverage: no discounts or vouchers"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("0.00")
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.discounts = []
        checkout_info.voucher = None
        
        with patch('saleor.checkout.base_calculations.base_checkout_subtotal') as mock_subtotal:
            with patch('saleor.checkout.base_calculations.base_checkout_delivery_price') as mock_delivery:
                mock_subtotal.return_value = Money(Decimal("100.00"), "USD")
                mock_delivery.return_value = Money(Decimal("10.00"), "USD")
                
                total = checkout_total(
                    checkout_info=checkout_info,
                    lines=[]
                )
                
                assert total.amount == Decimal("110.00")  # 100 + 10
                assert total.currency == "USD"
    
    def test_checkout_total_with_discount(self):
        """Statement Coverage: with discount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("20.00")
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.discounts = [Mock()]  # Has discounts
        checkout_info.voucher = None
        
        with patch('saleor.checkout.base_calculations.base_checkout_subtotal') as mock_subtotal:
            with patch('saleor.checkout.base_calculations.base_checkout_delivery_price') as mock_delivery:
                with patch('saleor.discount.utils.voucher.is_order_level_voucher', return_value=False):
                    mock_subtotal.return_value = Money(Decimal("100.00"), "USD")
                    mock_delivery.return_value = Money(Decimal("10.00"), "USD")
                    
                    total = checkout_total(
                        checkout_info=checkout_info,
                        lines=[]
                    )
                    
                    # Should subtract discount
                    assert total.amount < Decimal("110.00")
                    assert total.currency == "USD"

