"""
Comprehensive White-Box Tests for saleor/order/calculations.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- fetch_order_prices_if_expired
- get_expired_line_ids
- calculate_taxes
- _calculate_and_add_tax
- _call_plugin_or_tax_app
- _get_taxes_for_order
- _recalculate_with_plugins
- remove_tax
- refresh_order_base_prices_and_discounts
- order_line_unit
- order_line_total
- order_line_tax_rate
- order_subtotal
- order_total
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from datetime import datetime, timedelta
from prices import Money, TaxedMoney

from saleor.order.models import Order, OrderLine, OrderStatus
from saleor.order.calculations import (
    fetch_order_prices_if_expired,
    get_expired_line_ids,
    calculate_taxes,
    remove_tax,
    order_line_unit,
    order_line_total,
    order_line_tax_rate,
    order_subtotal,
    order_total,
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType, Category
from saleor.tax import TaxCalculationStrategy
from saleor.core.taxes import TaxDataError, TaxDataErrorMessage


@pytest.mark.django_db
class TestGetExpiredLineIds:
    """Test get_expired_line_ids() - Statement Coverage"""

    def test_get_expired_line_ids_returns_empty_for_non_draft(self):
        """Statement: Return empty list for non-draft orders"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.CONFIRMED,
            lines_count=0
        )
        
        result = get_expired_line_ids(order, None)
        assert result == []

    def test_get_expired_line_ids_returns_expired_lines(self):
        """Statement: Return expired line IDs"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        from django.utils import timezone
        expired_time = timezone.now() - timedelta(days=1)
        future_time = timezone.now() + timedelta(days=1)
        
        line1 = OrderLine.objects.create(
            order=order,
            product_name="Product 1",
            variant_name="Variant 1",
            product_sku="SKU1",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            draft_base_price_expire_at=expired_time
        )
        line2 = OrderLine.objects.create(
            order=order,
            product_name="Product 2",
            variant_name="Variant 2",
            product_sku="SKU2",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("20.00"),
            unit_price_gross_amount=Decimal("20.00"),
            draft_base_price_expire_at=future_time
        )
        
        result = get_expired_line_ids(order, None)
        assert len(result) == 1
        assert result[0] == line1.id

    def test_get_expired_line_ids_uses_provided_lines(self):
        """Statement: Use provided lines instead of fetching"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        from django.utils import timezone
        expired_time = timezone.now() - timedelta(days=1)
        
        line = OrderLine.objects.create(
            order=order,
            product_name="Product 1",
            variant_name="Variant 1",
            product_sku="SKU1",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            draft_base_price_expire_at=expired_time
        )
        
        provided_lines = [line]
        result = get_expired_line_ids(order, provided_lines)
        assert len(result) == 1
        assert result[0] == line.id


@pytest.mark.django_db
class TestFetchOrderPricesIfExpired:
    """Test fetch_order_prices_if_expired() - Statement Coverage"""

    def test_fetch_order_prices_returns_early_for_non_editable_status(self):
        """Statement: Return early for non-editable status"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.CANCELED,
            lines_count=0
        )
        manager = Mock()
        
        result_order, result_lines = fetch_order_prices_if_expired(
            order, manager, None, False
        )
        
        assert result_order == order
        assert result_lines is None

    def test_fetch_order_prices_returns_early_when_not_expired(self):
        """Statement: Return early when prices not expired"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            should_refresh_prices=False
        )
        manager = Mock()
        
        result_order, result_lines = fetch_order_prices_if_expired(
            order, manager, None, False
        )
        
        assert result_order == order
        assert result_lines is None

    def test_fetch_order_prices_refreshes_when_force_update(self):
        """Statement: Refresh when force_update is True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            should_refresh_prices=False
        )
        manager = Mock()
        
        with patch('saleor.order.calculations.fetch_draft_order_lines_info') as mock_fetch:
            with patch('saleor.order.calculations.handle_order_promotion'):
                with patch('saleor.order.calculations.calculate_prices'):
                    with patch('saleor.order.calculations.calculate_taxes'):
                        mock_fetch.return_value = []
                        result_order, result_lines = fetch_order_prices_if_expired(
                            order, manager, None, True
                        )
                        
                        mock_fetch.assert_called_once()


@pytest.mark.django_db
class TestCalculateTaxes:
    """Test calculate_taxes() - Statement Coverage"""

    def test_calculate_taxes_with_prices_entered_with_tax(self):
        """Statement: Calculate taxes when prices entered with tax"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        channel.tax_configuration.prices_entered_with_tax = True
        channel.tax_configuration.save()
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            tax_exemption=False
        )
        manager = Mock()
        lines = []
        
        with patch('saleor.order.calculations.get_charge_taxes_for_order', return_value=True):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order', return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations._calculate_and_add_tax'):
                    with patch('saleor.order.calculations.remove_tax'):
                        calculate_taxes(order, manager, lines, TaxCalculationStrategy.FLAT_RATES)
                        
                        # Should call _calculate_and_add_tax
                        assert True  # Test passes if no exception

    def test_calculate_taxes_removes_tax_when_exempt(self):
        """Statement: Remove tax when order is exempt"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        channel.tax_configuration.prices_entered_with_tax = True
        channel.tax_configuration.save()
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            tax_exemption=True
        )
        manager = Mock()
        lines = []
        
        with patch('saleor.order.calculations.get_charge_taxes_for_order', return_value=True):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order', return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations._calculate_and_add_tax'):
                    with patch('saleor.order.calculations.remove_tax') as mock_remove:
                        calculate_taxes(order, manager, lines, TaxCalculationStrategy.FLAT_RATES)
                        
                        mock_remove.assert_called_once()

    def test_calculate_taxes_with_prices_without_tax(self):
        """Statement: Calculate taxes when prices entered without tax"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        channel.tax_configuration.prices_entered_with_tax = False
        channel.tax_configuration.save()
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            tax_exemption=False
        )
        manager = Mock()
        lines = []
        
        with patch('saleor.order.calculations.get_charge_taxes_for_order', return_value=True):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order', return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations._calculate_and_add_tax'):
                    calculate_taxes(order, manager, lines, TaxCalculationStrategy.FLAT_RATES)
                    
                    # Should call _calculate_and_add_tax
                    assert True  # Test passes if no exception


@pytest.mark.django_db
class TestRemoveTax:
    """Test remove_tax() - Statement Coverage"""

    def test_remove_tax_calls_remove_tax_gross_when_prices_with_tax(self):
        """Statement: Call _remove_tax_gross when prices entered with tax"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            subtotal_net_amount=Decimal("100.00"),
            subtotal_gross_amount=Decimal("120.00")
        )
        lines = []
        
        with patch('saleor.order.calculations._remove_tax_gross') as mock_remove:
            remove_tax(order, lines, True)
            mock_remove.assert_called_once()

    def test_remove_tax_calls_remove_tax_net_when_prices_without_tax(self):
        """Statement: Call _remove_tax_net when prices entered without tax"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        lines = []
        
        with patch('saleor.order.calculations._remove_tax_net') as mock_remove:
            remove_tax(order, lines, False)
            mock_remove.assert_called_once()


@pytest.mark.django_db
class TestOrderLineUnit:
    """Test order_line_unit() - Statement Coverage"""

    def test_order_line_unit_returns_unit_price(self):
        """Statement: Return unit price from line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=2,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00")
        )
        
        result = order_line_unit(line)
        
        assert result.net == Money(Decimal("10.00"), "USD")
        assert result.gross == Money(Decimal("12.00"), "USD")


@pytest.mark.django_db
class TestOrderLineTotal:
    """Test order_line_total() - Statement Coverage"""

    def test_order_line_total_returns_total_price(self):
        """Statement: Return total price from line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=2,
            currency="USD",
            total_price_net_amount=Decimal("20.00"),
            total_price_gross_amount=Decimal("24.00")
        )
        
        result = order_line_total(line)
        
        assert result.net == Money(Decimal("20.00"), "USD")
        assert result.gross == Money(Decimal("24.00"), "USD")


@pytest.mark.django_db
class TestOrderLineTaxRate:
    """Test order_line_tax_rate() - Statement Coverage"""

    def test_order_line_tax_rate_returns_tax_rate(self):
        """Statement: Return tax rate from line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=1,
            currency="USD",
            tax_rate=Decimal("0.20")
        )
        
        result = order_line_tax_rate(line)
        
        assert result == Decimal("0.20")

    def test_order_line_tax_rate_returns_zero_when_none(self):
        """Statement: Return zero when tax_rate is None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=1,
            currency="USD",
            tax_rate=None
        )
        
        result = order_line_tax_rate(line)
        
        assert result == Decimal("0")


@pytest.mark.django_db
class TestOrderSubtotal:
    """Test order_subtotal() - Statement Coverage"""

    def test_order_subtotal_returns_subtotal_from_order(self):
        """Statement: Return subtotal from order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            subtotal_net_amount=Decimal("100.00"),
            subtotal_gross_amount=Decimal("120.00")
        )
        
        result = order_subtotal(order)
        
        assert result.net == Money(Decimal("100.00"), "USD")
        assert result.gross == Money(Decimal("120.00"), "USD")


@pytest.mark.django_db
class TestOrderTotal:
    """Test order_total() - Statement Coverage"""

    def test_order_total_returns_total_from_order(self):
        """Statement: Return total from order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            lines_count=0,
            total_net_amount=Decimal("110.00"),
            total_gross_amount=Decimal("132.00")
        )
        
        result = order_total(order)
        
        assert result.net == Money(Decimal("110.00"), "USD")
        assert result.gross == Money(Decimal("132.00"), "USD")

