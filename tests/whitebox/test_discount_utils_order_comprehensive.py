"""
Comprehensive White-Box Tests for saleor/discount/utils/order.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money, TaxedMoney

from saleor.discount.models import OrderDiscount, OrderLineDiscount, DiscountType, DiscountValueType
from saleor.discount.utils.order import (
    create_order_line_discount_objects,
    update_catalogue_promotion_discount_amount_for_order,
    update_unit_discount_data_on_order_line,
    update_unit_discount_data_on_order_lines_info,
    handle_order_promotion,
    create_order_discount_objects_for_order_promotions,
    _set_order_base_prices,
    _clear_order_discount,
)
from saleor.order.models import Order, OrderLine
from saleor.channel.models import Channel


@pytest.mark.django_db
class TestCreateOrderLineDiscountObjects:
    """Test create_order_line_discount_objects()"""

    def test_create_order_line_discount_objects_returns_none_when_no_data(self):
        """Statement: Return None when discount_data is None"""
        lines_info = []
        result = create_order_line_discount_objects(lines_info, None)
        assert result is None

    def test_create_order_line_discount_objects_returns_none_when_no_lines(self):
        """Statement: Return None when lines_info is empty"""
        discount_data = ([], [], [], [])
        result = create_order_line_discount_objects([], discount_data)
        assert result is None

    def test_create_order_line_discount_objects_removes_discounts(self):
        """Statement: Remove discounts when in discount_to_remove"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
        discount = OrderLineDiscount.objects.create(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("5.00"),
            amount_value=Decimal("5.00"),
            currency="USD"
        )
        line_info = Mock()
        line_info.line = line
        lines_info = [line_info]
        
        discount_data = ([], [], [discount], [])
        
        result = create_order_line_discount_objects(lines_info, discount_data)
        
        assert not OrderLineDiscount.objects.filter(id=discount.id).exists()

    def test_create_order_line_discount_objects_creates_discounts(self):
        """Statement: Create new discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
        new_discount = OrderLineDiscount(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("5.00"),
            amount_value=Decimal("5.00"),
            currency="USD"
        )
        line_info = Mock()
        line_info.line = line
        lines_info = [line_info]
        
        discount_data = ([new_discount], [], [], [])
        
        result = create_order_line_discount_objects(lines_info, discount_data)
        
        assert OrderLineDiscount.objects.filter(line=line).exists()


@pytest.mark.django_db
class TestUpdateCataloguePromotionDiscountAmountForOrder:
    """Test update_catalogue_promotion_discount_amount_for_order()"""

    def test_update_catalogue_promotion_discount_amount_updates_amount(self):
        """Statement: Update discount amount based on quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
            unit_price_gross_amount=Decimal("10.00"),
            undiscounted_base_unit_price_amount=Decimal("10.00")
        )
        discount = OrderLineDiscount.objects.create(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.PERCENTAGE,
            value=Decimal("10.00"),
            amount_value=Decimal("1.00"),
            currency="USD"
        )
        
        update_catalogue_promotion_discount_amount_for_order(
            discount, line, 2, "USD"
        )
        
        discount.refresh_from_db()
        # Should update amount_value based on quantity
        assert discount.amount_value > Decimal("0")


@pytest.mark.django_db
class TestUpdateUnitDiscountDataOnOrderLine:
    """Test update_unit_discount_data_on_order_line()"""

    def test_update_unit_discount_data_sets_fields_when_no_discounts(self):
        """Statement: Set fields to zero/None when no discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
        
        update_unit_discount_data_on_order_line(line, [])
        
        assert line.unit_discount_amount == Decimal("0.0")
        assert line.unit_discount_type is None
        assert line.unit_discount_value == Decimal("0.0")
        assert line.unit_discount_reason is None

    def test_update_unit_discount_data_sets_fields_for_single_discount(self):
        """Statement: Set fields for single discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
            unit_price_gross_amount=Decimal("10.00")
        )
        discount = OrderLineDiscount(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("5.00"),
            amount_value=Decimal("10.00"),
            currency="USD",
            reason="Test reason"
        )
        
        update_unit_discount_data_on_order_line(line, [discount])
        
        assert line.unit_discount_amount == Decimal("5.00")  # 10.00 / 2
        assert line.unit_discount_type == DiscountValueType.FIXED
        assert line.unit_discount_value == Decimal("5.00")
        assert line.unit_discount_reason == "Test reason"

    def test_update_unit_discount_data_sets_fixed_type_for_multiple_discounts(self):
        """Statement: Set FIXED type when multiple discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
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
        discount1 = OrderLineDiscount(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.PERCENTAGE,
            value=Decimal("10.00"),
            amount_value=Decimal("1.00"),
            currency="USD"
        )
        discount2 = OrderLineDiscount(
            line=line,
            type=DiscountType.PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("2.00"),
            amount_value=Decimal("2.00"),
            currency="USD"
        )
        
        update_unit_discount_data_on_order_line(line, [discount1, discount2])
        
        assert line.unit_discount_type == DiscountValueType.FIXED
        assert line.unit_discount_value == Decimal("3.00")  # Sum of amounts


@pytest.mark.django_db
class TestHandleOrderPromotion:
    """Test handle_order_promotion()"""

    def test_handle_order_promotion_calls_create_discount_objects(self):
        """Statement: Call create_order_discount_objects_for_order_promotions"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0
        )
        lines_info = []
        
        with patch('saleor.discount.utils.order.create_order_discount_objects_for_order_promotions') as mock_create:
            with patch('saleor.discount.utils.order._clear_prefetched_order_discounts'):
                handle_order_promotion(order, lines_info)
                
                mock_create.assert_called_once()


@pytest.mark.django_db
class TestCreateOrderDiscountObjectsForOrderPromotions:
    """Test create_order_discount_objects_for_order_promotions()"""

    def test_create_order_discount_clears_when_voucher_code_exists(self):
        """Statement: Clear discount when voucher_code exists"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0,
            voucher_code="TEST_VOUCHER"
        )
        lines_info = []
        
        with patch('saleor.discount.utils.order._clear_order_discount') as mock_clear:
            create_order_discount_objects_for_order_promotions(order, lines_info)
            
            mock_clear.assert_called_once()

    def test_create_order_discount_clears_when_manual_discount_exists(self):
        """Statement: Clear discount when manual discount exists"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0
        )
        OrderDiscount.objects.create(
            order=order,
            type=DiscountType.MANUAL,
            value_type=DiscountValueType.FIXED,
            value=Decimal("10.00"),
            amount_value=Decimal("10.00"),
            currency="USD"
        )
        lines_info = []
        
        with patch('saleor.discount.utils.order._clear_order_discount') as mock_clear:
            create_order_discount_objects_for_order_promotions(order, lines_info)
            
            mock_clear.assert_called_once()


@pytest.mark.django_db
class TestSetOrderBasePrices:
    """Test _set_order_base_prices()"""

    def test_set_order_base_prices_updates_when_different(self):
        """Statement: Update order prices when different"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0,
            subtotal_net_amount=Decimal("100.00"),
            subtotal_gross_amount=Decimal("100.00"),
            total_net_amount=Decimal("110.00"),
            total_gross_amount=Decimal("110.00")
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("90.00"),
            unit_price_gross_amount=Decimal("90.00")
        )
        line_info = Mock()
        line_info.line = line
        lines_info = [line_info]
        
        with patch('saleor.discount.utils.order.base_order_subtotal', return_value=Money(Decimal("90.00"), "USD")):
            order.undiscounted_base_shipping_price = Money(Decimal("10.00"), "USD")
            _set_order_base_prices(order, lines_info)
            
            order.refresh_from_db()
            assert order.subtotal_net_amount == Decimal("90.00")
            assert order.total_net_amount == Decimal("100.00")

    def test_set_order_base_prices_skips_when_same(self):
        """Statement: Skip update when prices are same"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0,
            subtotal_net_amount=Decimal("100.00"),
            subtotal_gross_amount=Decimal("100.00"),
            total_net_amount=Decimal("110.00"),
            total_gross_amount=Decimal("110.00")
        )
        line = OrderLine.objects.create(
            order=order,
            product_name="Product",
            variant_name="Variant",
            product_sku="SKU",
            quantity=1,
            currency="USD",
            unit_price_net_amount=Decimal("100.00"),
            unit_price_gross_amount=Decimal("100.00")
        )
        line_info = Mock()
        line_info.line = line
        lines_info = [line_info]
        
        with patch('saleor.discount.utils.order.base_order_subtotal', return_value=Money(Decimal("100.00"), "USD")):
            order.undiscounted_base_shipping_price = Money(Decimal("10.00"), "USD")
            _set_order_base_prices(order, lines_info)
            
            # Should not update since values are same
            order.refresh_from_db()
            assert order.subtotal_net_amount == Decimal("100.00")
            assert order.total_net_amount == Decimal("110.00")


@pytest.mark.django_db
class TestClearOrderDiscount:
    """Test _clear_order_discount()"""

    def test_clear_order_discount_deletes_order_promotion_discounts(self):
        """Statement: Delete order promotion discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status="DRAFT",
            lines_count=0
        )
        discount = OrderDiscount.objects.create(
            order=order,
            type=DiscountType.ORDER_PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("10.00"),
            amount_value=Decimal("10.00"),
            currency="USD"
        )
        lines_info = []
        
        with patch('saleor.discount.utils.order.delete_gift_line'):
            _clear_order_discount(order, lines_info)
            
            assert not OrderDiscount.objects.filter(id=discount.id).exists()

