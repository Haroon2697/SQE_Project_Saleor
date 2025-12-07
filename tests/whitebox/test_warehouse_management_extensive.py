"""
Extensive White-Box Tests for saleor/warehouse/management.py

Target: Increase warehouse module coverage from 28.2% to 70%+
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from uuid import uuid4

from saleor.warehouse.models import Stock, Warehouse, Allocation, Reservation
from saleor.warehouse.management import (
    delete_stocks,
    stock_bulk_update,
    delete_allocations,
    allocate_stocks,
    deallocate_stock,
    increase_stock,
    increase_allocations,
    decrease_allocations,
    decrease_stock,
    deallocate_stock_for_orders,
    allocate_preorders,
    deactivate_preorder_for_variant,
)
from saleor.channel.models import Channel
from saleor.order.models import Order, OrderLine
from saleor.product.models import Product, ProductVariant, ProductType, Category
from saleor.order.fetch import OrderLineInfo
from saleor.plugins.manager import PluginsManager
from saleor.core.exceptions import InsufficientStock, AllocationError


@pytest.mark.django_db
class TestDeleteStocks:
    """Test delete_stocks()"""

    def test_delete_stocks_deletes_specified_stocks(self):
        """Statement: Delete stocks with specified PKs"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        stock1 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        stock2 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=20
        )
        
        delete_stocks([stock1.id])
        
        assert not Stock.objects.filter(id=stock1.id).exists()
        assert Stock.objects.filter(id=stock2.id).exists()


@pytest.mark.django_db
class TestStockBulkUpdate:
    """Test stock_bulk_update()"""

    def test_stock_bulk_update_updates_stocks(self):
        """Statement: Update multiple stocks"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        stock1 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        stock2 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=20
        )
        
        stock1.quantity = 15
        stock2.quantity = 25
        
        stock_bulk_update([stock1, stock2], ["quantity"])
        
        stock1.refresh_from_db()
        stock2.refresh_from_db()
        assert stock1.quantity == 15
        assert stock2.quantity == 25


@pytest.mark.django_db
class TestDeleteAllocations:
    """Test delete_allocations()"""

    def test_delete_allocations_deletes_specified_allocations(self):
        """Statement: Delete allocations with specified PKs"""
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
            status="DRAFT",
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
            variant=variant
        )
        allocation1 = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=3
        )
        allocation2 = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=2
        )
        
        delete_allocations([allocation1.id])
        
        assert not Allocation.objects.filter(id=allocation1.id).exists()
        assert Allocation.objects.filter(id=allocation2.id).exists()


@pytest.mark.django_db
class TestIncreaseStock:
    """Test increase_stock()"""

    def test_increase_stock_increases_quantity(self):
        """Statement: Increase stock quantity"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
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
        
        increase_stock([stock], 5)
        
        stock.refresh_from_db()
        assert stock.quantity == 15  # 10 + 5

    def test_increase_stock_handles_multiple_stocks(self):
        """Statement: Handle multiple stocks"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        stock1 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        stock2 = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=20
        )
        
        increase_stock([stock1, stock2], 5)
        
        stock1.refresh_from_db()
        stock2.refresh_from_db()
        assert stock1.quantity == 15
        assert stock2.quantity == 25


@pytest.mark.django_db
class TestIncreaseAllocations:
    """Test increase_allocations()"""

    def test_increase_allocations_increases_quantity_allocated(self):
        """Statement: Increase quantity_allocated for allocations"""
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
            quantity=10,
            quantity_allocated=3
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=3
        )
        
        increase_allocations([allocation], 2)
        
        allocation.refresh_from_db()
        stock.refresh_from_db()
        assert allocation.quantity_allocated == 5  # 3 + 2
        assert stock.quantity_allocated == 5  # 3 + 2


@pytest.mark.django_db
class TestDecreaseAllocations:
    """Test decrease_allocations()"""

    def test_decrease_allocations_decreases_quantity_allocated(self):
        """Statement: Decrease quantity_allocated for allocations"""
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
            quantity=10,
            quantity_allocated=5
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        line_info = OrderLineInfo(
            line=line,
            quantity=2,
            variant=variant,
            warehouse_pk=warehouse.pk
        )
        manager = Mock()
        
        decrease_allocations([line_info], manager)
        
        allocation.refresh_from_db()
        stock.refresh_from_db()
        assert allocation.quantity_allocated == 3  # 5 - 2
        assert stock.quantity_allocated == 3  # 5 - 2


@pytest.mark.django_db
class TestDecreaseStock:
    """Test decrease_stock()"""

    def test_decrease_stock_decreases_quantity(self):
        """Statement: Decrease stock quantity"""
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
            status="DRAFT",
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
            variant=variant
        )
        line_info = OrderLineInfo(
            line=line,
            quantity=3,
            variant=variant,
            warehouse_pk=warehouse.pk
        )
        manager = Mock()
        
        decrease_stock([line_info], manager, allow_stock_to_be_exceeded=False)
        
        stock.refresh_from_db()
        assert stock.quantity == 7  # 10 - 3

    def test_decrease_stock_raises_insufficient_stock_when_not_enough(self):
        """Statement: Raise InsufficientStock when not enough quantity"""
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
            quantity=5
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
            quantity=10,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant
        )
        line_info = OrderLineInfo(
            line=line,
            quantity=10,
            variant=variant,
            warehouse_pk=warehouse.pk
        )
        manager = Mock()
        
        with pytest.raises(InsufficientStock):
            decrease_stock([line_info], manager, allow_stock_to_be_exceeded=False)


@pytest.mark.django_db
class TestDeallocateStock:
    """Test deallocate_stock()"""

    def test_deallocate_stock_deallocates_quantities(self):
        """Statement: Deallocate stock quantities"""
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
            quantity=10,
            quantity_allocated=5
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant
        )
        allocation = Allocation.objects.create(
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
        
        deallocate_stock([line_info], manager)
        
        allocation.refresh_from_db()
        stock.refresh_from_db()
        assert allocation.quantity_allocated == 2  # 5 - 3
        assert stock.quantity_allocated == 2  # 5 - 3


@pytest.mark.django_db
class TestDeallocateStockForOrders:
    """Test deallocate_stock_for_orders()"""

    def test_deallocate_stock_for_orders_deallocates_all_order_lines(self):
        """Statement: Deallocate all order lines for given orders"""
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
            quantity=10,
            quantity_allocated=5
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
            quantity=5,
            currency="USD",
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("10.00"),
            variant=variant
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        manager = Mock()
        
        deallocate_stock_for_orders([order.id], manager)
        
        allocation.refresh_from_db()
        stock.refresh_from_db()
        assert allocation.quantity_allocated == 0
        assert stock.quantity_allocated == 0

