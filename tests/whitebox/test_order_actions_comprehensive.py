"""
Comprehensive White-Box Tests for saleor/order/actions.py

Target: Drastically increase coverage from 34.8% to 70%+
This file contains extensive tests for critical order action functions.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from uuid import uuid4
from prices import Money, TaxedMoney

from saleor.order.models import Order, OrderLine, Fulfillment, FulfillmentLine, OrderStatus, FulfillmentStatus
from saleor.order.actions import (
    clean_mark_order_as_paid,
    _increase_order_line_quantity,
    fulfill_order_lines,
    automatically_fulfill_digital_lines,
    _create_fulfillment_lines,
    create_fulfillments,
    _get_fulfillment_line_if_exists,
    _get_fulfillment_line,
    _move_order_lines_to_target_fulfillment,
    _move_fulfillment_lines_to_target_fulfillment,
    __get_shipping_refund_amount,
    create_refund_fulfillment,
    _populate_replace_order_fields,
    create_replace_order,
    _move_lines_to_return_fulfillment,
    _move_lines_to_replace_fulfillment,
    create_return_fulfillment,
    process_replace,
    create_fulfillments_for_returned_products,
    _calculate_refund_amount,
    decrease_fulfilled_quantity,
    cancel_fulfillment,
    approve_fulfillment,
    FulfillmentLineData,
)
from saleor.order.fetch import OrderLineInfo, OrderInfo
from saleor.channel.models import Channel
from saleor.payment.models import Payment, Transaction, TransactionItem, ChargeStatus, TransactionKind
from saleor.payment import CustomPaymentChoices, PaymentError
from saleor.core.exceptions import InsufficientStock, InsufficientStockData
from saleor.warehouse.models import Stock, Warehouse, Allocation
from saleor.product.models import Product, ProductVariant, ProductType, Category, DigitalContent
from saleor.account.models import User
from saleor.giftcard import GiftCardLineData
from saleor.plugins.manager import PluginsManager


@pytest.mark.django_db
class TestCleanMarkOrderAsPaid:
    """Test clean_mark_order_as_paid()"""

    def test_clean_mark_order_as_paid_raises_when_payments_exist(self):
        """Statement: Raise PaymentError when payments exist"""
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
        Payment.objects.create(
            order=order,
            gateway="test",
            currency="USD",
            total=Decimal("100.00"),
            charge_status=ChargeStatus.NOT_CHARGED
        )
        
        with pytest.raises(PaymentError, match="Orders with payments"):
            clean_mark_order_as_paid(order)

    def test_clean_mark_order_as_paid_raises_when_transactions_exist(self):
        """Statement: Raise PaymentError when transactions exist"""
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
        TransactionItem.objects.create(
            order=order,
            name="Test Transaction",
            currency="USD"
        )
        
        with pytest.raises(PaymentError, match="Orders with transactions"):
            clean_mark_order_as_paid(order)

    def test_clean_mark_order_as_paid_passes_when_no_payments_or_transactions(self):
        """Statement: Pass when no payments or transactions"""
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
        
        # Should not raise
        clean_mark_order_as_paid(order)


@pytest.mark.django_db
class TestIncreaseOrderLineQuantity:
    """Test _increase_order_line_quantity()"""

    def test_increase_order_line_quantity_updates_fulfilled_quantity(self):
        """Statement: Update quantity_fulfilled for order lines"""
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            quantity_fulfilled=2
        )
        line_info = OrderLineInfo(
            line=line,
            quantity=3,
            variant=None,
            warehouse_pk=None
        )
        
        _increase_order_line_quantity([line_info])
        
        line.refresh_from_db()
        assert line.quantity_fulfilled == 5


@pytest.mark.django_db
class TestFulfillOrderLines:
    """Test fulfill_order_lines()"""

    def test_fulfill_order_lines_decreases_stock_and_increases_quantity(self):
        """Statement: Decrease stock and increase fulfilled quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        warehouse.channels.add(channel)
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        stock = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant,
            quantity_fulfilled=0
        )
        Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        line_info = OrderLineInfo(
            line=line,
            quantity=3,
            variant=variant,
            warehouse_pk=warehouse.pk
        )
        manager = Mock()
        
        fulfill_order_lines([line_info], manager, allow_stock_to_be_exceeded=False)
        
        stock.refresh_from_db()
        line.refresh_from_db()
        assert stock.quantity == 7  # 10 - 3
        assert line.quantity_fulfilled == 3


@pytest.mark.django_db
class TestGetFulfillmentLineIfExists:
    """Test _get_fulfillment_line_if_exists()"""

    def test_get_fulfillment_line_if_exists_returns_line_when_found(self):
        """Statement: Return fulfillment line when found"""
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
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00")
        )
        fulfillment = Fulfillment.objects.create(order=order)
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=line,
            quantity=1
        )
        
        result = _get_fulfillment_line_if_exists(
            [fulfillment_line],
            line.id,
            None
        )
        
        assert result == fulfillment_line

    def test_get_fulfillment_line_if_exists_returns_none_when_not_found(self):
        """Statement: Return None when not found"""
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
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00")
        )
        fulfillment = Fulfillment.objects.create(order=order)
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=line,
            quantity=1
        )
        
        result = _get_fulfillment_line_if_exists(
            [fulfillment_line],
            uuid4(),  # Different line ID
            None
        )
        
        assert result is None


@pytest.mark.django_db
class TestGetFulfillmentLine:
    """Test _get_fulfillment_line()"""

    def test_get_fulfillment_line_returns_existing_line(self):
        """Statement: Return existing fulfillment line"""
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
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00")
        )
        target_fulfillment = Fulfillment.objects.create(order=order)
        existing_line = FulfillmentLine.objects.create(
            fulfillment=target_fulfillment,
            order_line=line,
            quantity=1
        )
        
        result_line, existed = _get_fulfillment_line(
            target_fulfillment,
            [existing_line],
            line.id,
            None
        )
        
        assert result_line == existing_line
        assert existed is True

    def test_get_fulfillment_line_creates_new_line_when_not_exists(self):
        """Statement: Create new fulfillment line when not exists"""
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
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00")
        )
        target_fulfillment = Fulfillment.objects.create(order=order)
        
        result_line, existed = _get_fulfillment_line(
            target_fulfillment,
            [],
            line.id,
            None
        )
        
        assert result_line.order_line_id == line.id
        assert result_line.quantity == 0
        assert existed is False


@pytest.mark.django_db
class TestGetShippingRefundAmount:
    """Test __get_shipping_refund_amount()"""

    def test_get_shipping_refund_amount_returns_shipping_when_refund_shipping_and_no_amount(self):
        """Statement: Return shipping price when refund_shipping_costs=True and amount=None"""
        shipping_price = Decimal("10.00")
        result = __get_shipping_refund_amount(True, None, shipping_price)
        assert result == shipping_price

    def test_get_shipping_refund_amount_returns_none_when_refund_shipping_false(self):
        """Statement: Return None when refund_shipping_costs=False"""
        shipping_price = Decimal("10.00")
        result = __get_shipping_refund_amount(False, None, shipping_price)
        assert result is None

    def test_get_shipping_refund_amount_returns_none_when_amount_provided(self):
        """Statement: Return None when amount is provided"""
        shipping_price = Decimal("10.00")
        result = __get_shipping_refund_amount(True, Decimal("50.00"), shipping_price)
        assert result is None


@pytest.mark.django_db
class TestPopulateReplaceOrderFields:
    """Test _populate_replace_order_fields()"""

    def test_populate_replace_order_fields_copies_order_fields(self):
        """Statement: Copy order fields to replace order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        user = User.objects.create_user(email="test@example.com", password="password")
        original_order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.CONFIRMED,
            lines_count=0,
            user=user,
            user_email="test@example.com",
            language_code="en"
        )
        
        replace_order = _populate_replace_order_fields(original_order, 2)
        
        assert replace_order.status == OrderStatus.DRAFT
        assert replace_order.user_id == original_order.user_id
        assert replace_order.language_code == original_order.language_code
        assert replace_order.user_email == original_order.user_email
        assert replace_order.currency == original_order.currency
        assert replace_order.channel == original_order.channel
        assert replace_order.lines_count == 2
        assert replace_order.original == original_order


@pytest.mark.django_db
class TestDecreaseFulfilledQuantity:
    """Test decrease_fulfilled_quantity()"""

    def test_decrease_fulfilled_quantity_decreases_quantity(self):
        """Statement: Decrease quantity_fulfilled for fulfillment lines"""
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            quantity_fulfilled=3
        )
        fulfillment = Fulfillment.objects.create(order=order)
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=line,
            quantity=2
        )
        
        decrease_fulfilled_quantity(fulfillment)
        
        line.refresh_from_db()
        assert line.quantity_fulfilled == 1  # 3 - 2


@pytest.mark.django_db
class TestCalculateRefundAmount:
    """Test _calculate_refund_amount()"""

    def test_calculate_refund_amount_calculates_from_order_lines(self):
        """Statement: Calculate refund amount from order lines"""
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
        line1 = OrderLine.objects.create(
            order=order,
            product_name="Product 1",
            variant_name="Variant 1",
            product_sku="SKU1",
            quantity=2,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00")
        )
        line2 = OrderLine.objects.create(
            order=order,
            product_name="Product 2",
            variant_name="Variant 2",
            product_sku="SKU2",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("20.00"),
            unit_price_gross_amount=Decimal("24.00")
        )
        line_info1 = OrderLineInfo(line=line1, quantity=2, variant=None, warehouse_pk=None)
        line_info2 = OrderLineInfo(line=line2, quantity=1, variant=None, warehouse_pk=None)
        lines_to_refund = {}
        
        refund_amount = _calculate_refund_amount(
            [line_info1, line_info2],
            [],
            lines_to_refund
        )
        
        # 2 * 12.00 + 1 * 24.00 = 48.00
        assert refund_amount == Decimal("48.00")
        assert len(lines_to_refund) == 2

    def test_calculate_refund_amount_includes_fulfillment_lines(self):
        """Statement: Include fulfillment lines in calculation"""
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00")
        )
        fulfillment = Fulfillment.objects.create(order=order, status=FulfillmentStatus.FULFILLED)
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=line,
            quantity=2
        )
        fulfillment_line_data = FulfillmentLineData(line=fulfillment_line, quantity=2)
        lines_to_refund = {}
        
        refund_amount = _calculate_refund_amount(
            [],
            [fulfillment_line_data],
            lines_to_refund
        )
        
        # 2 * 12.00 = 24.00
        assert refund_amount == Decimal("24.00")
        assert len(lines_to_refund) == 1

    def test_calculate_refund_amount_skips_already_refunded_lines(self):
        """Statement: Skip fulfillment lines already refunded"""
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00")
        )
        refunded_fulfillment = Fulfillment.objects.create(
            order=order,
            status=FulfillmentStatus.REFUNDED
        )
        fulfillment = Fulfillment.objects.create(order=order, status=FulfillmentStatus.FULFILLED)
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=refunded_fulfillment,
            order_line=line,
            quantity=2
        )
        fulfillment_line_data = FulfillmentLineData(line=fulfillment_line, quantity=2)
        lines_to_refund = {}
        
        refund_amount = _calculate_refund_amount(
            [],
            [fulfillment_line_data],
            lines_to_refund
        )
        
        # Should be 0 because line is already refunded
        assert refund_amount == Decimal("0.00")
        assert len(lines_to_refund) == 0

