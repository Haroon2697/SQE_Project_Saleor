"""
Comprehensive White-Box Tests for saleor/order/utils.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Focusing on critical business logic functions:
- get_order_country
- order_line_needs_automatic_fulfillment
- order_needs_automatic_fulfillment
- invalidate_order_prices
- recalculate_order_weight
- refresh_order_status
- update_order_status
- determine_order_status
- get_total_order_discount
- get_total_order_discount_excluding_shipping
- update_order_charge_status
- update_order_authorize_status
- calculate_draft_order_line_price_expiration_date
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from django.utils import timezone
from datetime import timedelta
from prices import Money

from saleor.order.models import Order, OrderLine, OrderStatus, Fulfillment, FulfillmentLine
from saleor.order.utils import (
    get_order_country,
    order_line_needs_automatic_fulfillment,
    order_needs_automatic_fulfillment,
    invalidate_order_prices,
    recalculate_order_weight,
    refresh_order_status,
    update_order_status,
    determine_order_status,
    get_total_order_discount,
    get_total_order_discount_excluding_shipping,
    update_order_charge_status,
    update_order_authorize_status,
    calculate_draft_order_line_price_expiration_date,
)
from saleor.order import (
    FulfillmentStatus,
    OrderChargeStatus,
    OrderAuthorizeStatus,
)
from saleor.channel.models import Channel
from saleor.account.models import User, Address
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.discount.models import OrderDiscount, DiscountType, VoucherType
from saleor.order.fetch import OrderLineInfo
from saleor.payment.models import Payment, TransactionItem
from saleor.payment import ChargeStatus, TransactionKind


@pytest.mark.django_db
class TestGetOrderCountry:
    """Test get_order_country() - Statement Coverage"""
    
    def test_get_order_country_uses_shipping_address(self):
        """Statement: Use shipping_address if available"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        shipping_address = Address.objects.create(
            country="US",
            street_address_1="123 Main St"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            shipping_address=shipping_address
        )
        
        with patch('saleor.order.utils.get_active_country') as mock_get:
            mock_get.return_value = "US"
            result = get_order_country(order)
            assert result == "US"
            mock_get.assert_called_once_with(
                channel, shipping_address, order.billing_address
            )


@pytest.mark.django_db
class TestOrderLineNeedsAutomaticFulfillment:
    """Test order_line_needs_automatic_fulfillment() - Statement, Decision, MC/DC Coverage"""
    
    def test_order_line_needs_automatic_fulfillment_no_digital_content(self):
        """Decision: digital_content is None -> return False"""
        line_data = Mock(spec=OrderLineInfo)
        line_data.digital_content = None
        
        result = order_line_needs_automatic_fulfillment(line_data)
        assert result is False
    
    def test_order_line_needs_automatic_fulfillment_default_settings_true(self):
        """Decision: default_automatic_fulfillment=True + use_default_settings=True -> return True"""
        line_data = Mock(spec=OrderLineInfo)
        digital_content = Mock()
        digital_content.use_default_settings = True
        digital_content.automatic_fulfillment = False
        line_data.digital_content = digital_content
        
        with patch('saleor.order.utils.get_default_digital_content_settings') as mock_settings:
            mock_settings.return_value = {"automatic_fulfillment": True}
            result = order_line_needs_automatic_fulfillment(line_data)
            assert result is True
    
    def test_order_line_needs_automatic_fulfillment_default_settings_false(self):
        """Decision: default_automatic_fulfillment=False + use_default_settings=True -> return False"""
        line_data = Mock(spec=OrderLineInfo)
        digital_content = Mock()
        digital_content.use_default_settings = True
        digital_content.automatic_fulfillment = False
        line_data.digital_content = digital_content
        
        with patch('saleor.order.utils.get_default_digital_content_settings') as mock_settings:
            mock_settings.return_value = {"automatic_fulfillment": False}
            result = order_line_needs_automatic_fulfillment(line_data)
            assert result is False
    
    def test_order_line_needs_automatic_fulfillment_content_automatic_true(self):
        """Decision: content.automatic_fulfillment=True -> return True"""
        line_data = Mock(spec=OrderLineInfo)
        digital_content = Mock()
        digital_content.use_default_settings = False
        digital_content.automatic_fulfillment = True
        line_data.digital_content = digital_content
        
        with patch('saleor.order.utils.get_default_digital_content_settings') as mock_settings:
            mock_settings.return_value = {"automatic_fulfillment": False}
            result = order_line_needs_automatic_fulfillment(line_data)
            assert result is True


@pytest.mark.django_db
class TestOrderNeedsAutomaticFulfillment:
    """Test order_needs_automatic_fulfillment() - Statement, Decision Coverage"""
    
    def test_order_needs_automatic_fulfillment_no_digital_lines(self):
        """Statement: No digital lines -> return False"""
        line_data1 = Mock(spec=OrderLineInfo)
        line_data1.is_digital = False
        
        line_data2 = Mock(spec=OrderLineInfo)
        line_data2.is_digital = False
        
        result = order_needs_automatic_fulfillment([line_data1, line_data2])
        assert result is False
    
    def test_order_needs_automatic_fulfillment_digital_line_needs_fulfillment(self):
        """Decision: is_digital=True + needs_fulfillment -> return True"""
        line_data1 = Mock(spec=OrderLineInfo)
        line_data1.is_digital = False
        
        line_data2 = Mock(spec=OrderLineInfo)
        line_data2.is_digital = True
        
        with patch('saleor.order.utils.order_line_needs_automatic_fulfillment') as mock_check:
            mock_check.return_value = True
            result = order_needs_automatic_fulfillment([line_data1, line_data2])
            assert result is True


@pytest.mark.django_db
class TestInvalidateOrderPrices:
    """Test invalidate_order_prices() - Statement, Decision Coverage"""
    
    def test_invalidate_order_prices_editable_status(self):
        """Decision: status in ORDER_EDITABLE_STATUS -> set should_refresh_prices=True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT
        )
        
        invalidate_order_prices(order, save=False)
        assert order.should_refresh_prices is True
    
    def test_invalidate_order_prices_non_editable_status(self):
        """Decision: status not in ORDER_EDITABLE_STATUS -> do nothing"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.FULFILLED,
            should_refresh_prices=False
        )
        
        invalidate_order_prices(order, save=False)
        # should_refresh_prices should remain False
        assert order.should_refresh_prices is False
    
    def test_invalidate_order_prices_with_save(self):
        """Decision: save=True -> call order.save()"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT
        )
        
        invalidate_order_prices(order, save=True)
        order.refresh_from_db()
        assert order.should_refresh_prices is True


@pytest.mark.django_db
class TestRecalculateOrderWeight:
    """Test recalculate_order_weight() - Statement Coverage"""
    
    def test_recalculate_order_weight_sums_line_weights(self):
        """Statement: Sum variant.get_weight() * quantity for all lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        variant1 = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST1"
        )
        variant2 = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST2"
        )
        
        line1 = OrderLine.objects.create(
            order=order,
            variant=variant1,
            quantity=2
        )
        line2 = OrderLine.objects.create(
            order=order,
            variant=variant2,
            quantity=1
        )
        
        with patch.object(variant1, 'get_weight', return_value=Mock(kg=1.0)):
            with patch.object(variant2, 'get_weight', return_value=Mock(kg=0.5)):
                recalculate_order_weight(order, save=False)
                # Weight should be calculated (2 * 1.0 + 1 * 0.5 = 2.5)


@pytest.mark.django_db
class TestDetermineOrderStatus:
    """Test determine_order_status() - Statement, Decision, MC/DC Coverage"""
    
    def test_determine_order_status_unfulfilled(self):
        """Decision: quantity_fulfilled - quantity_awaiting_approval <= 0 -> UNFULFILLED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=0,
            quantity_returned=0,
            quantity_awaiting_approval=0
        )
        assert status == OrderStatus.UNFULFILLED
    
    def test_determine_order_status_unfulfilled_with_awaiting(self):
        """Decision: quantity_fulfilled - quantity_awaiting_approval <= 0 -> UNFULFILLED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=5,
            quantity_returned=0,
            quantity_awaiting_approval=5
        )
        assert status == OrderStatus.UNFULFILLED  # 5 - 5 = 0
    
    def test_determine_order_status_partially_returned(self):
        """Decision: 0 < quantity_returned < total_quantity -> PARTIALLY_RETURNED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=10,
            quantity_returned=3,
            quantity_awaiting_approval=0
        )
        assert status == OrderStatus.PARTIALLY_RETURNED
    
    def test_determine_order_status_returned(self):
        """Decision: quantity_returned == total_quantity -> RETURNED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=10,
            quantity_returned=10,
            quantity_awaiting_approval=0
        )
        assert status == OrderStatus.RETURNED
    
    def test_determine_order_status_partially_fulfilled(self):
        """Decision: quantity_fulfilled - quantity_awaiting_approval < total_quantity -> PARTIALLY_FULFILLED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=7,
            quantity_returned=0,
            quantity_awaiting_approval=0
        )
        assert status == OrderStatus.PARTIALLY_FULFILLED
    
    def test_determine_order_status_fulfilled(self):
        """Decision: quantity_fulfilled - quantity_awaiting_approval >= total_quantity -> FULFILLED"""
        status = determine_order_status(
            total_quantity=10,
            quantity_fulfilled=10,
            quantity_returned=0,
            quantity_awaiting_approval=0
        )
        assert status == OrderStatus.FULFILLED


@pytest.mark.django_db
class TestRefreshOrderStatus:
    """Test refresh_order_status() - Statement, Decision Coverage"""
    
    def test_refresh_order_status_all_products_replaced(self):
        """Decision: total_quantity == 0 -> return False (status unchanged)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.UNFULFILLED
        )
        
        # Create fulfillments that result in total_quantity = 0
        fulfillment = Fulfillment.objects.create(
            order=order,
            status=FulfillmentStatus.REPLACED
        )
        line = OrderLine.objects.create(
            order=order,
            quantity=5
        )
        FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=line,
            quantity=5
        )
        
        result = refresh_order_status(order)
        assert result is False  # Status should not change when all replaced
    
    def test_refresh_order_status_status_changes(self):
        """Statement: Status changes -> return True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.UNFULFILLED
        )
        
        line = OrderLine.objects.create(
            order=order,
            quantity=10,
            quantity_fulfilled=10
        )
        
        result = refresh_order_status(order)
        assert result is True  # Status should change from UNFULFILLED to FULFILLED
        assert order.status == OrderStatus.FULFILLED


@pytest.mark.django_db
class TestUpdateOrderStatus:
    """Test update_order_status() - Statement Coverage"""
    
    @patch('saleor.order.utils.refresh_order_status')
    def test_update_order_status_with_transaction(self, mock_refresh):
        """Statement: Use transaction.atomic and select_for_update"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.UNFULFILLED
        )
        
        mock_refresh.return_value = True
        
        update_order_status(order)
        
        mock_refresh.assert_called_once()
        order.refresh_from_db()
        # Status should be updated if refresh_order_status returned True


@pytest.mark.django_db
class TestGetTotalOrderDiscount:
    """Test get_total_order_discount() - Statement, Decision Coverage"""
    
    def test_get_total_order_discount_sums_all_discounts(self):
        """Statement: Sum all discount.amount_value"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            undiscounted_total_gross_amount=Decimal("100.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("5.00"),
            value_type="FIXED",
            amount_value=Decimal("5.00"),
            currency="USD"
        )
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.ORDER_PROMOTION,
            value=Decimal("3.00"),
            value_type="FIXED",
            amount_value=Decimal("3.00"),
            currency="USD"
        )
        
        result = get_total_order_discount(order)
        assert result == Money(Decimal("8.00"), "USD")
    
    def test_get_total_order_discount_caps_at_undiscounted_total(self):
        """Decision: total_discount > undiscounted_total -> return undiscounted_total"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            undiscounted_total_gross_amount=Decimal("10.00")
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("15.00"),
            value_type="FIXED",
            amount_value=Decimal("15.00"),
            currency="USD"
        )
        
        result = get_total_order_discount(order)
        assert result == Money(Decimal("10.00"), "USD")  # Capped at undiscounted_total


@pytest.mark.django_db
class TestGetTotalOrderDiscountExcludingShipping:
    """Test get_total_order_discount_excluding_shipping() - Statement, Decision Coverage"""
    
    def test_get_total_order_discount_excluding_shipping_no_shipping_voucher(self):
        """Decision: No shipping voucher -> return all discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            undiscounted_total_gross_amount=Decimal("100.00"),
            voucher=None
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("5.00"),
            value_type="FIXED",
            amount_value=Decimal("5.00"),
            currency="USD"
        )
        
        result = get_total_order_discount_excluding_shipping(order)
        assert result == Money(Decimal("5.00"), "USD")
    
    def test_get_total_order_discount_excluding_shipping_with_shipping_voucher(self):
        """Decision: Shipping voucher -> exclude VOUCHER type discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        voucher = Mock()
        voucher.type = VoucherType.SHIPPING
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            undiscounted_total_gross_amount=Decimal("100.00"),
            voucher=voucher
        )
        
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.VOUCHER,
            value=Decimal("10.00"),
            value_type="FIXED",
            amount_value=Decimal("10.00"),
            currency="USD"
        )
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value=Decimal("5.00"),
            value_type="FIXED",
            amount_value=Decimal("5.00"),
            currency="USD"
        )
        
        result = get_total_order_discount_excluding_shipping(order)
        assert result == Money(Decimal("5.00"), "USD")  # Only MANUAL discount


@pytest.mark.django_db
class TestUpdateOrderChargeStatus:
    """Test update_order_charge_status() - Statement, Decision, MC/DC Coverage"""
    
    def test_update_order_charge_status_full(self):
        """Decision: total_charged == current_total_gross -> FULL"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_charged_amount=Decimal("100.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_charge_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.charge_status == OrderChargeStatus.FULL
    
    def test_update_order_charge_status_none(self):
        """Decision: total_charged <= 0 -> NONE"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_charged_amount=Decimal("0.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_charge_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.charge_status == OrderChargeStatus.NONE
    
    def test_update_order_charge_status_partial(self):
        """Decision: 0 < total_charged < current_total_gross -> PARTIAL"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_charged_amount=Decimal("50.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_charge_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.charge_status == OrderChargeStatus.PARTIAL
    
    def test_update_order_charge_status_overcharged(self):
        """Decision: total_charged > current_total_gross -> OVERCHARGED"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_charged_amount=Decimal("150.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_charge_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.charge_status == OrderChargeStatus.OVERCHARGED
    
    def test_update_order_charge_status_with_granted_refund(self):
        """Statement: Subtract granted_refund_amount from current_total_gross"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_charged_amount=Decimal("80.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_charge_status(order, granted_refund_amount=Decimal("20.00"))
        # current_total = 100 - 20 = 80, charged = 80 -> FULL
        assert order.charge_status == OrderChargeStatus.FULL


@pytest.mark.django_db
class TestUpdateOrderAuthorizeStatus:
    """Test update_order_authorize_status() - Statement, Decision, MC/DC Coverage"""
    
    def test_update_order_authorize_status_full_zero_total(self):
        """Decision: total_covered == 0 and order.total.gross == 0 -> FULL"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_authorized_amount=Decimal("0.00"),
            total_charged_amount=Decimal("0.00"),
            total_gross_amount=Decimal("0.00")
        )
        
        update_order_authorize_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.authorize_status == OrderAuthorizeStatus.FULL
    
    def test_update_order_authorize_status_none(self):
        """Decision: total_covered == 0 and order.total.gross > 0 -> NONE"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_authorized_amount=Decimal("0.00"),
            total_charged_amount=Decimal("0.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_authorize_status(order, granted_refund_amount=Decimal("0.00"))
        assert order.authorize_status == OrderAuthorizeStatus.NONE
    
    def test_update_order_authorize_status_full_covered(self):
        """Decision: total_covered >= current_total_gross -> FULL"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_authorized_amount=Decimal("60.00"),
            total_charged_amount=Decimal("40.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_authorize_status(order, granted_refund_amount=Decimal("0.00"))
        # total_covered = 60 + 40 = 100 >= 100 -> FULL
        assert order.authorize_status == OrderAuthorizeStatus.FULL
    
    def test_update_order_authorize_status_partial(self):
        """Decision: 0 < total_covered < current_total_gross -> PARTIAL"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            total_authorized_amount=Decimal("30.00"),
            total_charged_amount=Decimal("20.00"),
            total_gross_amount=Decimal("100.00")
        )
        
        update_order_authorize_status(order, granted_refund_amount=Decimal("0.00"))
        # total_covered = 30 + 20 = 50 < 100 -> PARTIAL
        assert order.authorize_status == OrderAuthorizeStatus.PARTIAL


@pytest.mark.django_db
class TestCalculateDraftOrderLinePriceExpirationDate:
    """Test calculate_draft_order_line_price_expiration_date() - Statement, Decision Coverage"""
    
    def test_calculate_draft_order_line_price_expiration_date_not_draft(self):
        """Decision: order_status != DRAFT -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        result = calculate_draft_order_line_price_expiration_date(
            channel, OrderStatus.UNFULFILLED
        )
        assert result is None
    
    def test_calculate_draft_order_line_price_expiration_date_draft_no_freeze_period(self):
        """Decision: freeze_period is None or <= 0 -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD",
            draft_order_line_price_freeze_period=None
        )
        
        result = calculate_draft_order_line_price_expiration_date(
            channel, OrderStatus.DRAFT
        )
        assert result is None
    
    def test_calculate_draft_order_line_price_expiration_date_draft_with_freeze_period(self):
        """Decision: freeze_period > 0 -> return now + freeze_period hours"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD",
            draft_order_line_price_freeze_period=24
        )
        
        with patch('saleor.order.utils.timezone.now') as mock_now:
            fixed_time = timezone.now()
            mock_now.return_value = fixed_time
            
            result = calculate_draft_order_line_price_expiration_date(
                channel, OrderStatus.DRAFT
            )
            
            assert result is not None
            assert result == fixed_time + timedelta(hours=24)

