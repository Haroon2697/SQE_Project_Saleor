"""
Comprehensive White-Box Tests for saleor/order/base_calculations.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- base_order_shipping
- base_order_subtotal
- base_order_total
- base_order_line_total
- propagate_order_discount_on_order_prices
- calculate_prices
- _get_total_price_with_subtotal_discount_for_order_line
- propagate_order_discount_on_order_lines_prices
- get_total_price_with_subtotal_discount_for_order_line
- apply_subtotal_discount_to_order_lines
- assign_order_line_prices
- assign_order_prices
- undiscounted_order_shipping
- undiscounted_order_subtotal
- undiscounted_order_total
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money, TaxedMoney

from saleor.order.models import Order, OrderLine, OrderStatus
from saleor.order.base_calculations import (
    base_order_shipping,
    base_order_subtotal,
    base_order_total,
    base_order_line_total,
    propagate_order_discount_on_order_prices,
    calculate_prices,
    _get_total_price_with_subtotal_discount_for_order_line,
    propagate_order_discount_on_order_lines_prices,
    get_total_price_with_subtotal_discount_for_order_line,
    apply_subtotal_discount_to_order_lines,
    assign_order_line_prices,
    assign_order_prices,
    undiscounted_order_shipping,
    undiscounted_order_subtotal,
    undiscounted_order_total,
)
from saleor.discount.models import OrderDiscount, DiscountType, DiscountValueType
from saleor.discount.utils.voucher import is_order_level_voucher, is_shipping_voucher
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category
from saleor.shipping.models import ShippingMethod, ShippingMethodChannelListing


@pytest.mark.django_db
class TestBaseOrderShipping:
    """Test base_order_shipping() - Statement Coverage"""
    
    def test_base_order_shipping_returns_base_shipping_price(self):
        """Statement: Return order.base_shipping_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("10.00")
        )
        
        result = base_order_shipping(order)
        assert result == Money(Decimal("10.00"), "USD")
        assert result.amount == Decimal("10.00")


@pytest.mark.django_db
class TestBaseOrderSubtotal:
    """Test base_order_subtotal() - Statement, Decision, MC/DC Coverage"""
    
    def test_base_order_subtotal_empty_lines(self):
        """Statement: Empty lines -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        result = base_order_subtotal(order, [])
        assert result == Money(Decimal("0.00"), "USD")
    
    def test_base_order_subtotal_single_line(self):
        """Statement: Single line with quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=2,
            base_unit_price_amount=Decimal("10.00")
        )
        
        result = base_order_subtotal(order, [line])
        assert result == Money(Decimal("20.00"), "USD")
    
    def test_base_order_subtotal_multiple_lines(self):
        """Statement: Multiple lines -> sum all"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line1 = OrderLine.objects.create(
            order=order,
            quantity=2,
            base_unit_price_amount=Decimal("10.00")
        )
        line2 = OrderLine.objects.create(
            order=order,
            quantity=3,
            base_unit_price_amount=Decimal("5.00")
        )
        
        result = base_order_subtotal(order, [line1, line2])
        assert result == Money(Decimal("35.00"), "USD")  # 20 + 15


@pytest.mark.django_db
class TestBaseOrderTotal:
    """Test base_order_total() - Statement Coverage"""
    
    @patch('saleor.order.base_calculations.calculate_prices')
    def test_base_order_total_calls_calculate_prices(self, mock_calculate):
        """Statement: Call calculate_prices and return subtotal + shipping"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        mock_calculate.return_value = (
            Money(Decimal("10.00"), "USD"),
            Money(Decimal("5.00"), "USD")
        )
        
        result = base_order_total(order, [line])
        assert result == Money(Decimal("15.00"), "USD")
        mock_calculate.assert_called_once()


@pytest.mark.django_db
class TestBaseOrderLineTotal:
    """Test base_order_line_total() - Statement Coverage"""
    
    def test_base_order_line_total_calculates_correctly(self):
        """Statement: Calculate price_with_discounts and undiscounted_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=3,
            base_unit_price_amount=Decimal("10.00"),
            undiscounted_base_unit_price_amount=Decimal("12.00")
        )
        
        result = base_order_line_total(line)
        assert result.price_with_discounts.net == Money(Decimal("30.00"), "USD")
        assert result.undiscounted_price.net == Money(Decimal("36.00"), "USD")


@pytest.mark.django_db
class TestPropagateOrderDiscountOnOrderPrices:
    """Test propagate_order_discount_on_order_prices() - Statement, Decision, MC/DC"""
    
    def test_propagate_order_discount_no_discounts(self):
        """Statement: No discounts -> return base_subtotal and base_shipping_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
        assert subtotal == Money(Decimal("10.00"), "USD")
        assert shipping == Money(Decimal("5.00"), "USD")
    
    def test_propagate_order_discount_voucher_order_level(self):
        """Decision: Voucher type + is_order_level_voucher -> apply to subtotal"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        voucher = Mock()
        voucher.type = None  # Will be set via OrderDiscount
        order_discount = OrderDiscount.objects.create(
            order=order,
            type=DiscountType.VOUCHER,
            value=Decimal("2.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("2.00"),
            currency="USD"
        )
        order_discount.voucher = voucher
        
        with patch('saleor.order.base_calculations.is_order_level_voucher', return_value=True):
            with patch('saleor.order.base_calculations.is_shipping_voucher', return_value=False):
                with patch('saleor.order.base_calculations.apply_discount_to_value') as mock_apply:
                    mock_apply.return_value = Money(Decimal("8.00"), "USD")
                    subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
                    assert mock_apply.called
    
    def test_propagate_order_discount_voucher_shipping(self):
        """Decision: Voucher type + is_shipping_voucher -> continue (skip)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        voucher = Mock()
        order_discount = OrderDiscount.objects.create(
            order=order,
            type=DiscountType.VOUCHER,
            value=Decimal("2.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("2.00"),
            currency="USD"
        )
        order_discount.voucher = voucher
        
        with patch('saleor.order.base_calculations.is_order_level_voucher', return_value=False):
            with patch('saleor.order.base_calculations.is_shipping_voucher', return_value=True):
                subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
                # Shipping voucher should be skipped
                assert subtotal == Money(Decimal("10.00"), "USD")
    
    def test_propagate_order_discount_order_promotion(self):
        """Decision: ORDER_PROMOTION type -> apply to subtotal"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.ORDER_PROMOTION,
            value=Decimal("1.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("1.00"),
            currency="USD"
        )
        
        with patch('saleor.order.base_calculations.apply_discount_to_value') as mock_apply:
            mock_apply.return_value = Money(Decimal("9.00"), "USD")
            subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
            assert mock_apply.called
    
    def test_propagate_order_discount_manual_percentage(self):
        """Decision: MANUAL type + PERCENTAGE -> apply to subtotal and shipping"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("10.00"),
            value_type=DiscountValueType.PERCENTAGE,
            amount_value=Decimal("1.50"),
            currency="USD"
        )
        
        with patch('saleor.order.base_calculations.apply_discount_to_value') as mock_apply:
            mock_apply.side_effect = [
                Money(Decimal("9.00"), "USD"),  # subtotal
                Money(Decimal("4.50"), "USD")  # shipping
            ]
            subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
            assert mock_apply.call_count == 2
    
    def test_propagate_order_discount_manual_fixed_positive_total(self):
        """Decision: MANUAL type + FIXED + positive total -> calculate proportional discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("3.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("3.00"),
            currency="USD"
        )
        
        with patch('saleor.order.base_calculations.apply_discount_to_value') as mock_apply:
            mock_apply.return_value = Money(Decimal("12.00"), "USD")  # 15 - 3
            subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
            # Should calculate proportional discount
            assert mock_apply.called
    
    def test_propagate_order_discount_manual_fixed_zero_total(self):
        """Decision: MANUAL type + FIXED + zero total -> skip discount calculation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("0.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("0.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("3.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("3.00"),
            currency="USD"
        )
        
        subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
        # With zero total, discount should not be applied
        assert subtotal == Money(Decimal("0.00"), "USD")
        assert shipping == Money(Decimal("0.00"), "USD")
    
    def test_propagate_order_discount_updates_amount(self):
        """Statement: If amount changed -> update order_discount.amount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            base_shipping_price_amount=Decimal("5.00")
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        order_discount = OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("2.00"),
            value_type=DiscountValueType.FIXED,
            amount_value=Decimal("1.00"),  # Different from calculated
            currency="USD"
        )
        
        with patch('saleor.order.base_calculations.apply_discount_to_value') as mock_apply:
            mock_apply.return_value = Money(Decimal("13.00"), "USD")
            subtotal, shipping = propagate_order_discount_on_order_prices(order, [line])
            # Should update order_discount.amount
            order_discount.refresh_from_db()
            # Amount should be updated (bulk_update is called)


@pytest.mark.django_db
class TestCalculatePrices:
    """Test calculate_prices() - Statement, Decision Coverage"""
    
    @patch('saleor.order.base_calculations.assign_order_prices')
    @patch('saleor.order.base_calculations.apply_subtotal_discount_to_order_lines')
    @patch('saleor.order.base_calculations.propagate_order_discount_on_order_prices')
    @patch('saleor.order.base_calculations.base_order_subtotal')
    def test_calculate_prices_with_assign_prices_true(self, mock_subtotal, mock_propagate, mock_apply, mock_assign):
        """Decision: assign_prices=True -> call assign_order_prices and apply_subtotal_discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        mock_subtotal.return_value = Money(Decimal("10.00"), "USD")
        mock_propagate.return_value = (Money(Decimal("9.00"), "USD"), Money(Decimal("5.00"), "USD"))
        
        subtotal, shipping = calculate_prices(order, [line], assign_prices=True)
        
        assert mock_assign.called
        assert mock_apply.called
        assert subtotal == Money(Decimal("9.00"), "USD")
        assert shipping == Money(Decimal("5.00"), "USD")
    
    @patch('saleor.order.base_calculations.propagate_order_discount_on_order_prices')
    @patch('saleor.order.base_calculations.base_order_subtotal')
    def test_calculate_prices_with_assign_prices_false(self, mock_subtotal, mock_propagate):
        """Decision: assign_prices=False -> don't call assign_order_prices"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        mock_subtotal.return_value = Money(Decimal("10.00"), "USD")
        mock_propagate.return_value = (Money(Decimal("9.00"), "USD"), Money(Decimal("5.00"), "USD"))
        
        subtotal, shipping = calculate_prices(order, [line], assign_prices=False)
        
        assert subtotal == Money(Decimal("9.00"), "USD")
        assert shipping == Money(Decimal("5.00"), "USD")


@pytest.mark.django_db
class TestGetTotalPriceWithSubtotalDiscountForOrderLine:
    """Test _get_total_price_with_subtotal_discount_for_order_line() - Statement, Decision"""
    
    def test_get_total_price_positive_discount(self):
        """Statement: discount < base_line_total -> return base_line_total - discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=2,
            base_unit_price_amount=Decimal("10.00")
        )
        
        discount = Money(Decimal("5.00"), "USD")
        result = _get_total_price_with_subtotal_discount_for_order_line(line, discount)
        assert result == Money(Decimal("15.00"), "USD")  # 20 - 5
    
    def test_get_total_price_discount_exceeds_total(self):
        """Decision: discount >= base_line_total -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        discount = Money(Decimal("15.00"), "USD")
        result = _get_total_price_with_subtotal_discount_for_order_line(line, discount)
        assert result == Money(Decimal("0.00"), "USD")


@pytest.mark.django_db
class TestPropagateOrderDiscountOnOrderLinesPrices:
    """Test propagate_order_discount_on_order_lines_prices() - Statement, Decision, MC/DC"""
    
    def test_propagate_discount_single_line(self):
        """Decision: lines_count == 1 -> apply whole discount to single line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        base_subtotal = Money(Decimal("10.00"), "USD")
        subtotal_discount = Money(Decimal("2.00"), "USD")
        
        results = list(propagate_order_discount_on_order_lines_prices(
            [line], base_subtotal, subtotal_discount
        ))
        
        assert len(results) == 1
        assert results[0][0] == line
        assert results[0][1] == Money(Decimal("8.00"), "USD")
    
    def test_propagate_discount_multiple_lines(self):
        """Decision: lines_count > 1 -> propagate proportionally"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line1 = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        line2 = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("5.00")
        )
        
        base_subtotal = Money(Decimal("15.00"), "USD")
        subtotal_discount = Money(Decimal("3.00"), "USD")
        
        results = list(propagate_order_discount_on_order_lines_prices(
            [line1, line2], base_subtotal, subtotal_discount
        ))
        
        assert len(results) == 2
        # First line gets proportional discount
        assert results[0][0] == line1
        # Second line gets remaining discount
        assert results[1][0] == line2
    
    def test_propagate_discount_zero_base_subtotal(self):
        """Decision: base_subtotal.amount == 0 -> return zero_money for all lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("0.00")
        )
        
        base_subtotal = Money(Decimal("0.00"), "USD")
        subtotal_discount = Money(Decimal("2.00"), "USD")
        
        results = list(propagate_order_discount_on_order_lines_prices(
            [line], base_subtotal, subtotal_discount
        ))
        
        assert len(results) == 1
        assert results[0][1] == Money(Decimal("0.00"), "USD")


@pytest.mark.django_db
class TestGetTotalPriceWithSubtotalDiscountForOrderLineFunction:
    """Test get_total_price_with_subtotal_discount_for_order_line() - Statement Coverage"""
    
    def test_get_total_price_finds_line(self):
        """Statement: Find line by id -> return total_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        base_subtotal = Money(Decimal("10.00"), "USD")
        subtotal_discount = Money(Decimal("2.00"), "USD")
        
        result = get_total_price_with_subtotal_discount_for_order_line(
            line, [line], base_subtotal, subtotal_discount
        )
        
        assert result == Money(Decimal("8.00"), "USD")
    
    def test_get_total_price_line_not_found(self):
        """Statement: Line not found -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line1 = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        line2 = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("5.00")
        )
        
        base_subtotal = Money(Decimal("15.00"), "USD")
        subtotal_discount = Money(Decimal("2.00"), "USD")
        
        # Search for line1 but only pass line2
        result = get_total_price_with_subtotal_discount_for_order_line(
            line1, [line2], base_subtotal, subtotal_discount
        )
        
        assert result is None


@pytest.mark.django_db
class TestApplySubtotalDiscountToOrderLines:
    """Test apply_subtotal_discount_to_order_lines() - Statement Coverage"""
    
    @patch('saleor.order.base_calculations.assign_order_line_prices')
    def test_apply_subtotal_discount_calls_assign(self, mock_assign):
        """Statement: Call assign_order_line_prices for each line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        base_subtotal = Money(Decimal("10.00"), "USD")
        subtotal_discount = Money(Decimal("2.00"), "USD")
        
        apply_subtotal_discount_to_order_lines([line], base_subtotal, subtotal_discount)
        
        assert mock_assign.called


@pytest.mark.django_db
class TestAssignOrderLinePrices:
    """Test assign_order_line_prices() - Statement, Decision Coverage"""
    
    def test_assign_order_line_prices_positive_quantity(self):
        """Decision: quantity > 0 -> calculate unit_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=2,
            base_unit_price_amount=Decimal("10.00"),
            undiscounted_base_unit_price_amount=Decimal("12.00")
        )
        
        total_price = Money(Decimal("18.00"), "USD")
        assign_order_line_prices(line, total_price)
        
        assert line.total_price_net_amount == Decimal("18.00")
        assert line.total_price_gross_amount == Decimal("18.00")
        assert line.unit_price_net_amount == Decimal("9.00")  # 18 / 2
        assert line.unit_price_gross_amount == Decimal("9.00")
    
    def test_assign_order_line_prices_zero_quantity(self):
        """Decision: quantity == 0 -> don't calculate unit_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=0,
            base_unit_price_amount=Decimal("10.00"),
            undiscounted_base_unit_price_amount=Decimal("12.00")
        )
        
        total_price = Money(Decimal("0.00"), "USD")
        assign_order_line_prices(line, total_price)
        
        assert line.total_price_net_amount == Decimal("0.00")
        # Unit price should not be set when quantity is 0


@pytest.mark.django_db
class TestAssignOrderPrices:
    """Test assign_order_prices() - Statement Coverage"""
    
    @patch('saleor.order.base_calculations.undiscounted_order_total')
    def test_assign_order_prices_sets_all_fields(self, mock_undiscounted):
        """Statement: Set all order price fields"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            base_unit_price_amount=Decimal("10.00")
        )
        
        mock_undiscounted.return_value = Money(Decimal("15.00"), "USD")
        subtotal = Money(Decimal("10.00"), "USD")
        shipping = Money(Decimal("5.00"), "USD")
        
        assign_order_prices(order, [line], subtotal, shipping)
        
        assert order.shipping_price_net_amount == Decimal("5.00")
        assert order.total_net_amount == Decimal("15.00")  # 10 + 5
        assert order.subtotal_net_amount == Decimal("10.00")
        assert order.undiscounted_total_net_amount == Decimal("15.00")


@pytest.mark.django_db
class TestUndiscountedOrderShipping:
    """Test undiscounted_order_shipping() - Statement, Decision Coverage"""
    
    def test_undiscounted_order_shipping_with_shipping_method(self):
        """Decision: shipping_method exists -> return listing price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        shipping_method = ShippingMethod.objects.create(name="Standard")
        listing = ShippingMethodChannelListing.objects.create(
            channel=channel,
            shipping_method=shipping_method,
            price_amount=Decimal("10.00")
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            shipping_method=shipping_method
        )
        
        result = undiscounted_order_shipping(order)
        assert result == Money(Decimal("10.00"), "USD")
    
    def test_undiscounted_order_shipping_no_shipping_method(self):
        """Decision: shipping_method is None -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            shipping_method=None
        )
        
        result = undiscounted_order_shipping(order)
        assert result == Money(Decimal("0.00"), "USD")
    
    def test_undiscounted_order_shipping_no_listing(self):
        """Decision: No listing found -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        shipping_method = ShippingMethod.objects.create(name="Standard")
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            shipping_method=shipping_method
        )
        
        result = undiscounted_order_shipping(order)
        assert result == Money(Decimal("0.00"), "USD")


@pytest.mark.django_db
class TestUndiscountedOrderSubtotal:
    """Test undiscounted_order_subtotal() - Statement Coverage"""
    
    def test_undiscounted_order_subtotal_calculates_correctly(self):
        """Statement: Sum undiscounted_unit_price * quantity for all lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=2,
            undiscounted_base_unit_price_amount=Decimal("12.00")
        )
        
        result = undiscounted_order_subtotal(order, [line])
        assert result == Money(Decimal("24.00"), "USD")  # 12 * 2


@pytest.mark.django_db
class TestUndiscountedOrderTotal:
    """Test undiscounted_order_total() - Statement Coverage"""
    
    @patch('saleor.order.base_calculations.undiscounted_order_shipping')
    def test_undiscounted_order_total_sums_subtotal_and_shipping(self, mock_shipping):
        """Statement: Return undiscounted_subtotal + undiscounted_shipping"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=1,
            undiscounted_base_unit_price_amount=Decimal("10.00")
        )
        
        mock_shipping.return_value = Money(Decimal("5.00"), "USD")
        
        result = undiscounted_order_total(order, [line])
        assert result == Money(Decimal("15.00"), "USD")  # 10 + 5

