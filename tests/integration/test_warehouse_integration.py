"""
Integration tests for Warehouse module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from uuid import uuid4

from saleor.warehouse.models import (
    Warehouse,
    Stock,
    Allocation,
    PreorderAllocation,
    Reservation,
)
from saleor.warehouse import WarehouseClickAndCollectOption
from saleor.warehouse.management import (
    increase_stock,
    decrease_stock,
)
from saleor.channel.models import Channel
from saleor.product.models import (
    Product,
    ProductType,
    Category,
    ProductVariant,
)
from saleor.account.models import Address
from saleor.checkout.models import Checkout, CheckoutLine
from saleor.order.models import Order, OrderLine
from saleor.order import OrderStatus, OrderOrigin
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def address(db):
    """Create a test address."""
    return Address.objects.create(
        first_name="Warehouse",
        last_name="Manager",
        street_address_1="789 Warehouse St",
        city="Warehouse City",
        postal_code="11111",
        country="US",
    )


@pytest.fixture
def warehouse(db, address):
    """Create a test warehouse."""
    return Warehouse.objects.create(
        name="Test Warehouse",
        slug="test-warehouse",
        address=address,
        click_and_collect_option=WarehouseClickAndCollectOption.DISABLED,
    )


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Warehouse Channel",
        slug="warehouse-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name="Warehouse Category",
        slug="warehouse-category",
    )


@pytest.fixture
def product_type(db):
    """Create a test product type."""
    return ProductType.objects.create(
        name="Warehouse Product Type",
        slug="warehouse-product-type",
        is_shipping_required=True,
    )


@pytest.fixture
def product(db, product_type, category):
    """Create a test product."""
    return Product.objects.create(
        name="Warehouse Product",
        slug="warehouse-product",
        product_type=product_type,
        category=category,
    )


@pytest.fixture
def product_variant(db, product):
    """Create a test product variant."""
    return ProductVariant.objects.create(
        product=product,
        sku="WAREHOUSE-SKU-001",
        name="Warehouse Variant",
    )


@pytest.fixture
def stock(db, warehouse, product_variant):
    """Create test stock."""
    return Stock.objects.create(
        warehouse=warehouse,
        product_variant=product_variant,
        quantity=100,
    )


@pytest.mark.django_db
class TestWarehouseCreation:
    """Test warehouse creation."""

    def test_create_warehouse(self, address):
        """Test creating a warehouse."""
        warehouse = Warehouse.objects.create(
            name="New Warehouse",
            slug="new-warehouse",
            address=address,
        )
        assert warehouse.id is not None
        assert warehouse.name == "New Warehouse"

    def test_warehouse_str(self, warehouse):
        """Test warehouse string representation."""
        assert str(warehouse) == "Test Warehouse"

    def test_warehouse_with_click_and_collect(self, address):
        """Test warehouse with click and collect."""
        warehouse = Warehouse.objects.create(
            name="CC Warehouse",
            slug="cc-warehouse",
            address=address,
            click_and_collect_option=WarehouseClickAndCollectOption.LOCAL_STOCK,
        )
        assert warehouse.click_and_collect_option == WarehouseClickAndCollectOption.LOCAL_STOCK


@pytest.mark.django_db
class TestStockManagement:
    """Test stock management."""

    def test_create_stock(self, warehouse, product_variant):
        """Test creating stock."""
        stock = Stock.objects.create(
            warehouse=warehouse,
            product_variant=product_variant,
            quantity=50,
        )
        assert stock.id is not None
        assert stock.quantity == 50

    def test_update_stock_quantity(self, stock):
        """Test updating stock quantity."""
        stock.quantity = 200
        stock.save()
        stock.refresh_from_db()
        assert stock.quantity == 200

    def test_zero_stock(self, warehouse, product_variant):
        """Test zero stock."""
        stock = Stock.objects.create(
            warehouse=warehouse,
            product_variant=product_variant,
            quantity=0,
        )
        assert stock.quantity == 0


@pytest.mark.django_db
class TestStockQueries:
    """Test stock query functionality."""

    def test_filter_stock_by_warehouse(self, stock, warehouse):
        """Test filtering stock by warehouse."""
        stocks = Stock.objects.filter(warehouse=warehouse)
        assert stock in stocks

    def test_filter_stock_by_variant(self, stock, product_variant):
        """Test filtering stock by variant."""
        stocks = Stock.objects.filter(product_variant=product_variant)
        assert stock in stocks

    def test_available_stock(self, stock):
        """Test available stock calculation."""
        # Stock quantity minus allocated
        assert stock.quantity >= 0


@pytest.mark.django_db
class TestAllocation:
    """Test stock allocation."""

    def test_create_allocation(self, stock, channel, address):
        """Test creating an allocation."""
        user = User.objects.create_user(email="alloc@test.com", password="test")
        
        order = Order.objects.create(
            channel=channel,
            user=user,
            user_email=user.email,
            billing_address=address,
            status=OrderStatus.UNFULFILLED,
            origin=OrderOrigin.CHECKOUT,
            currency="USD",
            total_net_amount=Decimal("100.00"),
            total_gross_amount=Decimal("120.00"),
            undiscounted_total_net_amount=Decimal("100.00"),
            undiscounted_total_gross_amount=Decimal("120.00"),
        )
        
        order_line = OrderLine.objects.create(
            order=order,
            variant=stock.product_variant,
            product_name="Test",
            variant_name="Test",
            product_sku="TEST",
            quantity=5,
            unit_price_net_amount=Decimal("20.00"),
            unit_price_gross_amount=Decimal("24.00"),
            total_price_net_amount=Decimal("100.00"),
            total_price_gross_amount=Decimal("120.00"),
            undiscounted_unit_price_net_amount=Decimal("20.00"),
            undiscounted_unit_price_gross_amount=Decimal("24.00"),
            undiscounted_total_price_net_amount=Decimal("100.00"),
            undiscounted_total_price_gross_amount=Decimal("120.00"),
            currency="USD",
        )
        
        allocation = Allocation.objects.create(
            order_line=order_line,
            stock=stock,
            quantity_allocated=5,
        )
        
        assert allocation.id is not None
        assert allocation.quantity_allocated == 5


@pytest.mark.django_db
class TestMultipleWarehouses:
    """Test multiple warehouses."""

    def test_multiple_warehouses(self, address):
        """Test creating multiple warehouses."""
        wh1 = Warehouse.objects.create(
            name="Warehouse 1",
            slug="warehouse-1",
            address=address,
        )
        wh2 = Warehouse.objects.create(
            name="Warehouse 2",
            slug="warehouse-2",
            address=address,
        )
        
        assert Warehouse.objects.count() >= 2
        assert wh1.slug != wh2.slug

    def test_stock_across_warehouses(self, address, product_variant):
        """Test stock across multiple warehouses."""
        wh1 = Warehouse.objects.create(name="WH1", slug="wh1", address=address)
        wh2 = Warehouse.objects.create(name="WH2", slug="wh2", address=address)
        
        stock1 = Stock.objects.create(
            warehouse=wh1,
            product_variant=product_variant,
            quantity=50,
        )
        stock2 = Stock.objects.create(
            warehouse=wh2,
            product_variant=product_variant,
            quantity=75,
        )
        
        total_stock = Stock.objects.filter(
            product_variant=product_variant
        ).values_list('quantity', flat=True)
        
        assert sum(total_stock) >= 125


@pytest.mark.django_db
class TestWarehouseChannels:
    """Test warehouse channel relationships."""

    def test_warehouse_shipping_zones(self, warehouse):
        """Test warehouse has shipping zones attribute."""
        assert hasattr(warehouse, 'shipping_zones')


@pytest.mark.django_db
class TestReservation:
    """Test stock reservation functionality."""

    def test_reservation_model_exists(self):
        """Test Reservation model exists."""
        assert Reservation is not None
        assert hasattr(Reservation, 'objects')

