"""
White-Box Testing - Order Base Calculations
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/order/base_calculations.py
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.order.models import Order, OrderLine, OrderStatus
from saleor.order.base_calculations import (
    base_order_shipping,
    base_order_subtotal,
    base_order_total,
    base_order_line_total,
    propagate_order_discount_on_order_prices,
    calculate_prices
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.discount.models import OrderDiscount, DiscountType
from prices import Money, TaxedMoney


# ============================================
# TEST 1: base_order_shipping - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseOrderShipping:
    """Test base_order_shipping() for statement coverage"""
    
    def test_base_order_shipping(self):
        """Statement Coverage: return order.base_shipping_price"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("10.00")
        )
        
        shipping = base_order_shipping(order)
        assert shipping.amount == Decimal("10.00")
        assert shipping.currency == "USD"


# ============================================
# TEST 2: base_order_subtotal - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseOrderSubtotal:
    """Test base_order_subtotal() for statement coverage"""
    
    def test_base_order_subtotal_single_line(self):
        """Statement Coverage: single order line"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
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
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU-001",
            quantity=2,
            base_unit_price_amount=Decimal("50.00"),
            currency="USD"
        )
        
        subtotal = base_order_subtotal(order, [line])
        assert subtotal.amount == Decimal("100.00")  # 2 * 50.00
        assert subtotal.currency == "USD"
    
    def test_base_order_subtotal_multiple_lines(self):
        """Statement Coverage: multiple order lines"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
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
        
        variant1 = ProductVariant.objects.create(product=product, sku="SKU-001")
        variant2 = ProductVariant.objects.create(product=product, sku="SKU-002")
        
        line1 = OrderLine.objects.create(
            order=order,
            variant=variant1,
            product_name="Product 1",
            variant_name="Variant 1",
            product_sku="SKU-001",
            quantity=2,
            base_unit_price_amount=Decimal("50.00"),
            currency="USD"
        )
        
        line2 = OrderLine.objects.create(
            order=order,
            variant=variant2,
            product_name="Product 2",
            variant_name="Variant 2",
            product_sku="SKU-002",
            quantity=3,
            base_unit_price_amount=Decimal("30.00"),
            currency="USD"
        )
        
        subtotal = base_order_subtotal(order, [line1, line2])
        assert subtotal.amount == Decimal("190.00")  # (2 * 50) + (3 * 30)
        assert subtotal.currency == "USD"
    
    def test_base_order_subtotal_empty_lines(self):
        """Statement Coverage: empty lines list"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        subtotal = base_order_subtotal(order, [])
        assert subtotal.amount == Decimal("0.00")
        assert subtotal.currency == "USD"


# ============================================
# TEST 3: base_order_line_total - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseOrderLineTotal:
    """Test base_order_line_total() for statement coverage"""
    
    def test_base_order_line_total(self):
        """Statement Coverage: calculate line total with discounts"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
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
        
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU-001",
            quantity=3,
            base_unit_price_amount=Decimal("100.00"),
            undiscounted_base_unit_price_amount=Decimal("120.00"),
            currency="USD"
        )
        
        result = base_order_line_total(line)
        
        # price_with_discounts = 100.00 * 3 = 300.00
        assert result.price_with_discounts.gross.amount == Decimal("300.00")
        assert result.price_with_discounts.net.amount == Decimal("300.00")
        
        # undiscounted_price = 120.00 * 3 = 360.00
        assert result.undiscounted_price.gross.amount == Decimal("360.00")
        assert result.undiscounted_price.net.amount == Decimal("360.00")


# ============================================
# TEST 4: base_order_total - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestBaseOrderTotal:
    """Test base_order_total() for statement coverage"""
    
    def test_base_order_total(self):
        """Statement Coverage: calculate total with prices"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
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
        
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU-001",
            quantity=2,
            base_unit_price_amount=Decimal("50.00"),
            currency="USD"
        )
        
        with patch('saleor.order.base_calculations.calculate_prices') as mock_calc:
            mock_calc.return_value = (
                Money(Decimal("100.00"), "USD"),  # subtotal
                Money(Decimal("10.00"), "USD")    # shipping
            )
            
            total = base_order_total(order, [line])
            
            assert total.amount == Decimal("110.00")  # 100 + 10
            assert total.currency == "USD"
            mock_calc.assert_called_once()


# ============================================
# TEST 5: propagate_order_discount_on_order_prices - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestPropagateOrderDiscountOnOrderPrices:
    """Test propagate_order_discount_on_order_prices() for statement coverage"""
    
    def test_propagate_discount_no_discounts(self):
        """Statement Coverage: no order discounts"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("10.00")
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
        
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU-001",
            quantity=1,
            base_unit_price_amount=Decimal("100.00"),
            currency="USD"
        )
        
        subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
        
        assert subtotal.amount == Decimal("100.00")
        assert shipping.amount == Decimal("10.00")
    
    def test_propagate_discount_with_entire_order_voucher(self):
        """Statement Coverage: with entire order voucher discount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("10.00")
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
        
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU-001",
            quantity=1,
            base_unit_price_amount=Decimal("100.00"),
            currency="USD"
        )
        
        # Create order discount
        discount = OrderDiscount.objects.create(
            order=order,
            type=DiscountType.VOUCHER,
            value_type="FIXED",
            value=Decimal("20.00"),
            amount_value=Decimal("20.00"),
            currency="USD"
        )
        
        subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
        
        # Discount should be applied
        assert subtotal.amount < Decimal("100.00")
        assert shipping.amount == Decimal("10.00")

