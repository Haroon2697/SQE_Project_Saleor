"""
Integration tests for Order module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model

from saleor.order.models import Order, OrderLine, OrderEvent, Fulfillment, FulfillmentLine
from saleor.order import OrderStatus, OrderOrigin, FulfillmentStatus
from saleor.channel.models import Channel
from saleor.product.models import (
    Product,
    ProductType,
    Category,
    ProductVariant,
)
from saleor.account.models import Address


User = get_user_model()


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Order Channel",
        slug="order-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="order@example.com",
        password="testpass123",
    )


@pytest.fixture
def address(db):
    """Create a test address."""
    return Address.objects.create(
        first_name="Order",
        last_name="User",
        street_address_1="456 Order St",
        city="Order City",
        postal_code="67890",
        country="US",
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name="Order Category",
        slug="order-category",
    )


@pytest.fixture
def product_type(db):
    """Create a test product type."""
    return ProductType.objects.create(
        name="Order Product Type",
        slug="order-product-type",
        is_shipping_required=True,
    )


@pytest.fixture
def product(db, product_type, category):
    """Create a test product."""
    return Product.objects.create(
        name="Order Product",
        slug="order-product",
        product_type=product_type,
        category=category,
    )


@pytest.fixture
def product_variant(db, product):
    """Create a test product variant."""
    return ProductVariant.objects.create(
        product=product,
        sku="ORDER-SKU-001",
        name="Order Variant",
    )


@pytest.fixture
def order(db, channel, user, address):
    """Create a test order."""
    return Order.objects.create(
        channel=channel,
        user=user,
        user_email=user.email,
        billing_address=address,
        shipping_address=address,
        status=OrderStatus.UNFULFILLED,
        origin=OrderOrigin.CHECKOUT,
        currency=channel.currency_code,
        total_net_amount=Decimal("100.00"),
        total_gross_amount=Decimal("120.00"),
        undiscounted_total_net_amount=Decimal("100.00"),
        undiscounted_total_gross_amount=Decimal("120.00"),
    )


@pytest.mark.django_db
class TestOrderCreation:
    """Test order creation."""

    def test_create_order(self, channel, user, address):
        """Test creating an order."""
        order = Order.objects.create(
            channel=channel,
            user=user,
            user_email=user.email,
            billing_address=address,
            status=OrderStatus.UNFULFILLED,
            origin=OrderOrigin.CHECKOUT,
            currency="USD",
            total_net_amount=Decimal("50.00"),
            total_gross_amount=Decimal("60.00"),
            undiscounted_total_net_amount=Decimal("50.00"),
            undiscounted_total_gross_amount=Decimal("60.00"),
        )
        assert order.id is not None
        assert order.status == OrderStatus.UNFULFILLED

    def test_create_draft_order(self, channel, user, address):
        """Test creating a draft order."""
        order = Order.objects.create(
            channel=channel,
            user=user,
            user_email=user.email,
            status=OrderStatus.DRAFT,
            origin=OrderOrigin.DRAFT,
            currency="USD",
            total_net_amount=Decimal("0.00"),
            total_gross_amount=Decimal("0.00"),
            undiscounted_total_net_amount=Decimal("0.00"),
            undiscounted_total_gross_amount=Decimal("0.00"),
        )
        assert order.status == OrderStatus.DRAFT
        assert order.origin == OrderOrigin.DRAFT


@pytest.mark.django_db
class TestOrderStatus:
    """Test order status changes."""

    def test_order_initial_status(self, order):
        """Test order initial status."""
        assert order.status == OrderStatus.UNFULFILLED

    def test_change_order_status(self, order):
        """Test changing order status."""
        order.status = OrderStatus.FULFILLED
        order.save()
        order.refresh_from_db()
        assert order.status == OrderStatus.FULFILLED

    def test_cancel_order(self, order):
        """Test canceling an order."""
        order.status = OrderStatus.CANCELED
        order.save()
        order.refresh_from_db()
        assert order.status == OrderStatus.CANCELED


@pytest.mark.django_db
class TestOrderLines:
    """Test order lines functionality."""

    def test_create_order_line(self, order, product_variant):
        """Test creating an order line."""
        line = OrderLine.objects.create(
            order=order,
            variant=product_variant,
            product_name=product_variant.product.name,
            variant_name=product_variant.name,
            product_sku=product_variant.sku,
            quantity=2,
            unit_price_net_amount=Decimal("50.00"),
            unit_price_gross_amount=Decimal("60.00"),
            total_price_net_amount=Decimal("100.00"),
            total_price_gross_amount=Decimal("120.00"),
            undiscounted_unit_price_net_amount=Decimal("50.00"),
            undiscounted_unit_price_gross_amount=Decimal("60.00"),
            undiscounted_total_price_net_amount=Decimal("100.00"),
            undiscounted_total_price_gross_amount=Decimal("120.00"),
            currency="USD",
        )
        assert line.id is not None
        assert line.order == order
        assert line.quantity == 2

    def test_multiple_order_lines(self, order, product):
        """Test multiple order lines."""
        variant1 = ProductVariant.objects.create(product=product, sku="LINE-001")
        variant2 = ProductVariant.objects.create(product=product, sku="LINE-002")
        
        OrderLine.objects.create(
            order=order,
            variant=variant1,
            product_name=product.name,
            variant_name="Var 1",
            product_sku="LINE-001",
            quantity=1,
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00"),
            total_price_net_amount=Decimal("10.00"),
            total_price_gross_amount=Decimal("12.00"),
            undiscounted_unit_price_net_amount=Decimal("10.00"),
            undiscounted_unit_price_gross_amount=Decimal("12.00"),
            undiscounted_total_price_net_amount=Decimal("10.00"),
            undiscounted_total_price_gross_amount=Decimal("12.00"),
            currency="USD",
        )
        OrderLine.objects.create(
            order=order,
            variant=variant2,
            product_name=product.name,
            variant_name="Var 2",
            product_sku="LINE-002",
            quantity=2,
            unit_price_net_amount=Decimal("20.00"),
            unit_price_gross_amount=Decimal("24.00"),
            total_price_net_amount=Decimal("40.00"),
            total_price_gross_amount=Decimal("48.00"),
            undiscounted_unit_price_net_amount=Decimal("20.00"),
            undiscounted_unit_price_gross_amount=Decimal("24.00"),
            undiscounted_total_price_net_amount=Decimal("40.00"),
            undiscounted_total_price_gross_amount=Decimal("48.00"),
            currency="USD",
        )
        
        assert order.lines.count() == 2


@pytest.mark.django_db
class TestOrderEvents:
    """Test order events functionality."""

    def test_create_order_event(self, order, user):
        """Test creating an order event."""
        event = OrderEvent.objects.create(
            order=order,
            type="placed",
            user=user,
        )
        assert event.id is not None
        assert event.order == order
        assert event.type == "placed"

    def test_multiple_order_events(self, order, user):
        """Test multiple order events."""
        OrderEvent.objects.create(order=order, type="placed", user=user)
        OrderEvent.objects.create(order=order, type="confirmed", user=user)
        OrderEvent.objects.create(order=order, type="fulfillment_fulfilled_items", user=user)
        
        assert order.events.count() == 3


@pytest.mark.django_db
class TestFulfillment:
    """Test fulfillment functionality."""

    def test_create_fulfillment(self, order):
        """Test creating a fulfillment."""
        fulfillment = Fulfillment.objects.create(
            order=order,
            fulfillment_order=1,
            status=FulfillmentStatus.FULFILLED,
            tracking_number="TRACK123",
        )
        assert fulfillment.id is not None
        assert fulfillment.order == order
        assert fulfillment.status == FulfillmentStatus.FULFILLED

    def test_fulfillment_lines(self, order, product_variant):
        """Test fulfillment lines."""
        order_line = OrderLine.objects.create(
            order=order,
            variant=product_variant,
            product_name="Test",
            variant_name="Test Var",
            product_sku="TEST",
            quantity=3,
            unit_price_net_amount=Decimal("10.00"),
            unit_price_gross_amount=Decimal("12.00"),
            total_price_net_amount=Decimal("30.00"),
            total_price_gross_amount=Decimal("36.00"),
            undiscounted_unit_price_net_amount=Decimal("10.00"),
            undiscounted_unit_price_gross_amount=Decimal("12.00"),
            undiscounted_total_price_net_amount=Decimal("30.00"),
            undiscounted_total_price_gross_amount=Decimal("36.00"),
            currency="USD",
        )
        
        fulfillment = Fulfillment.objects.create(
            order=order,
            fulfillment_order=1,
            status=FulfillmentStatus.FULFILLED,
        )
        
        fulfillment_line = FulfillmentLine.objects.create(
            fulfillment=fulfillment,
            order_line=order_line,
            quantity=2,
        )
        
        assert fulfillment_line.id is not None
        assert fulfillment_line.quantity == 2


@pytest.mark.django_db
class TestOrderQueries:
    """Test order query functionality."""

    def test_filter_orders_by_status(self, order):
        """Test filtering orders by status."""
        orders = Order.objects.filter(status=OrderStatus.UNFULFILLED)
        assert order in orders

    def test_filter_orders_by_channel(self, order, channel):
        """Test filtering orders by channel."""
        orders = Order.objects.filter(channel=channel)
        assert order in orders

    def test_filter_orders_by_user(self, order, user):
        """Test filtering orders by user."""
        orders = Order.objects.filter(user=user)
        assert order in orders


@pytest.mark.django_db
class TestOrderMetadata:
    """Test order metadata functionality."""

    def test_order_metadata(self, order):
        """Test order metadata."""
        order.metadata = {"order_key": "order_value"}
        order.save()
        order.refresh_from_db()
        assert order.metadata.get("order_key") == "order_value"

    def test_order_private_metadata(self, order):
        """Test order private metadata."""
        order.private_metadata = {"private": "secret"}
        order.save()
        order.refresh_from_db()
        assert order.private_metadata.get("private") == "secret"

