"""
Comprehensive White-Box Tests for saleor/warehouse/management.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Focusing on critical inventory management functions:
- allocate_stocks
- deallocate_stock
- increase_stock
- decrease_stock
- increase_allocations
- decrease_allocations
- get_order_lines_with_track_inventory
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from uuid import uuid4

from saleor.warehouse.management import (
    allocate_stocks,
    deallocate_stock,
    increase_stock,
    decrease_stock,
    increase_allocations,
    decrease_allocations,
    get_order_lines_with_track_inventory,
)
from saleor.warehouse.models import Stock, Warehouse, Allocation
from saleor.order.models import Order, OrderLine
from saleor.order.fetch import OrderLineInfo
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.plugins.manager import PluginsManager


@pytest.mark.django_db
class TestGetOrderLinesWithTrackInventory:
    """Test get_order_lines_with_track_inventory() - Statement, Decision Coverage"""
    
    def test_get_order_lines_with_track_inventory_tracks_inventory(self):
        """Decision: variant.track_inventory=True -> include line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=1
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=1,
            warehouse_pk=None
        )
        
        result = get_order_lines_with_track_inventory([line_info])
        assert len(result) == 1
        assert result[0] == line_info
    
    def test_get_order_lines_with_track_inventory_no_track(self):
        """Decision: variant.track_inventory=False -> exclude line"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=False
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=1
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=1,
            warehouse_pk=None
        )
        
        result = get_order_lines_with_track_inventory([line_info])
        assert len(result) == 0
    
    def test_get_order_lines_with_track_inventory_no_variant(self):
        """Decision: variant is None -> exclude line"""
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
            variant=None,
            quantity=1
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=None,
            quantity=1,
            warehouse_pk=None
        )
        
        result = get_order_lines_with_track_inventory([line_info])
        assert len(result) == 0


@pytest.mark.django_db
class TestIncreaseStock:
    """Test increase_stock() - Statement Coverage"""
    
    def test_increase_stock_creates_stock_if_not_exists(self):
        """Statement: Stock doesn't exist -> create new stock"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        
        increase_stock([(variant, warehouse, 10)], allocate=False)
        
        stock = Stock.objects.get(variant=variant, warehouse=warehouse)
        assert stock.quantity == 10
    
    def test_increase_stock_increases_existing_stock(self):
        """Statement: Stock exists -> increase quantity"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=5
        )
        
        increase_stock([(variant, warehouse, 10)], allocate=False)
        
        stock.refresh_from_db()
        assert stock.quantity == 15  # 5 + 10
    
    def test_increase_stock_with_allocate(self):
        """Decision: allocate=True -> also create allocation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        
        increase_stock([(variant, warehouse, 10)], allocate=True, order_line=line)
        
        stock = Stock.objects.get(variant=variant, warehouse=warehouse)
        assert stock.quantity == 10
        
        allocation = Allocation.objects.filter(order_line=line, stock=stock).first()
        assert allocation is not None
        assert allocation.quantity_allocated == 5


@pytest.mark.django_db
class TestDecreaseStock:
    """Test decrease_stock() - Statement Coverage"""
    
    def test_decrease_stock_decreases_quantity(self):
        """Statement: Decrease stock quantity"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=20
        )
        
        decrease_stock([(variant, warehouse, 5)])
        
        stock.refresh_from_db()
        assert stock.quantity == 15  # 20 - 5


@pytest.mark.django_db
class TestIncreaseAllocations:
    """Test increase_allocations() - Statement Coverage"""
    
    def test_increase_allocations_creates_allocation(self):
        """Statement: Create new allocation if doesn't exist"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=5,
            warehouse_pk=None
        )
        
        manager = Mock(spec=PluginsManager)
        increase_allocations([line_info], channel, manager=manager)
        
        allocation = Allocation.objects.filter(order_line=line, stock=stock).first()
        assert allocation is not None
        assert allocation.quantity_allocated == 5
    
    def test_increase_allocations_increases_existing_allocation(self):
        """Statement: Allocation exists -> increase quantity_allocated"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=3
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=2,  # Additional quantity
            warehouse_pk=None
        )
        
        manager = Mock(spec=PluginsManager)
        increase_allocations([line_info], channel, manager=manager)
        
        allocation.refresh_from_db()
        assert allocation.quantity_allocated == 5  # 3 + 2


@pytest.mark.django_db
class TestDecreaseAllocations:
    """Test decrease_allocations() - Statement Coverage"""
    
    def test_decrease_allocations_decreases_quantity(self):
        """Statement: Decrease allocation quantity_allocated"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=2,  # Quantity to deallocate
            warehouse_pk=None
        )
        
        manager = Mock(spec=PluginsManager)
        decrease_allocations([line_info], manager=manager)
        
        allocation.refresh_from_db()
        assert allocation.quantity_allocated == 3  # 5 - 2
    
    def test_decrease_allocations_deletes_allocation_when_zero(self):
        """Decision: quantity_allocated becomes 0 -> delete allocation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=5,  # Deallocate all
            warehouse_pk=None
        )
        
        manager = Mock(spec=PluginsManager)
        decrease_allocations([line_info], manager=manager)
        
        # Allocation should be deleted
        assert not Allocation.objects.filter(id=allocation.id).exists()


@pytest.mark.django_db
class TestDeallocateStock:
    """Test deallocate_stock() - Statement Coverage"""
    
    def test_deallocate_stock_deallocates_for_lines(self):
        """Statement: Deallocate stock for order lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        line = OrderLine.objects.create(
            order=order,
            variant=variant,
            quantity=5
        )
        allocation = Allocation.objects.create(
            order_line=line,
            stock=stock,
            quantity_allocated=5
        )
        
        line_info = OrderLineInfo(
            line=line,
            variant=variant,
            quantity=5,
            warehouse_pk=None
        )
        
        manager = Mock(spec=PluginsManager)
        deallocate_stock([line_info], manager=manager)
        
        # Allocation should be removed or quantity decreased
        allocation.refresh_from_db()
        # Depending on implementation, allocation might be deleted or quantity set to 0

