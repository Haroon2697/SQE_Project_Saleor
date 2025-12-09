"""
Integration tests for Shipping module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from measurement.measures import Weight

from saleor.shipping.models import (
    ShippingZone,
    ShippingMethod,
    ShippingMethodChannelListing,
)
from saleor.channel.models import Channel
from saleor.warehouse.models import Warehouse
from saleor.account.models import Address


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Shipping Channel",
        slug="shipping-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def address(db):
    """Create a test address."""
    return Address.objects.create(
        first_name="Shipping",
        last_name="Test",
        street_address_1="100 Shipping Way",
        city="Ship City",
        postal_code="00000",
        country="US",
    )


@pytest.fixture
def warehouse(db, address):
    """Create a test warehouse."""
    return Warehouse.objects.create(
        name="Shipping Warehouse",
        slug="shipping-warehouse",
        address=address,
    )


@pytest.mark.django_db
class TestShippingZone:
    """Test shipping zone functionality."""

    def test_create_shipping_zone(self):
        """Test creating a shipping zone."""
        zone = ShippingZone.objects.create(
            name="US Shipping",
            default=False,
        )
        assert zone.id is not None
        assert zone.name == "US Shipping"

    def test_create_default_shipping_zone(self):
        """Test creating a default shipping zone."""
        zone = ShippingZone.objects.create(
            name="Default Zone",
            default=True,
        )
        assert zone.default is True

    def test_shipping_zone_str(self):
        """Test shipping zone string representation."""
        zone = ShippingZone.objects.create(
            name="Test Zone",
            default=False,
        )
        assert str(zone) == "Test Zone"

    def test_shipping_zone_countries(self):
        """Test shipping zone countries."""
        zone = ShippingZone.objects.create(
            name="Country Zone",
            default=False,
            countries=["US", "CA", "MX"],
        )
        assert "US" in zone.countries
        assert "CA" in zone.countries


@pytest.mark.django_db
class TestShippingMethod:
    """Test shipping method functionality."""

    def test_create_shipping_method(self):
        """Test creating a shipping method."""
        zone = ShippingZone.objects.create(name="Method Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            shipping_zone=zone,
            type="price",
        )
        assert method.id is not None
        assert method.name == "Standard Shipping"

    def test_create_weight_based_method(self):
        """Test creating a weight-based shipping method."""
        zone = ShippingZone.objects.create(name="Weight Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Weight Based Shipping",
            shipping_zone=zone,
            type="weight",
            minimum_order_weight=Weight(kg=0),
            maximum_order_weight=Weight(kg=10),
        )
        assert method.type == "weight"

    def test_shipping_method_str(self):
        """Test shipping method string representation."""
        zone = ShippingZone.objects.create(name="Str Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Express Shipping",
            shipping_zone=zone,
            type="price",
        )
        assert "Express" in str(method)


@pytest.mark.django_db
class TestShippingMethodChannelListing:
    """Test shipping method channel listing."""

    def test_create_channel_listing(self, channel):
        """Test creating a shipping method channel listing."""
        zone = ShippingZone.objects.create(name="Listing Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Listed Method",
            shipping_zone=zone,
            type="price",
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("9.99"),
            currency="USD",
        )
        assert listing.id is not None
        assert listing.price_amount == Decimal("9.99")

    def test_free_shipping_listing(self, channel):
        """Test free shipping channel listing."""
        zone = ShippingZone.objects.create(name="Free Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Free Shipping",
            shipping_zone=zone,
            type="price",
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("0.00"),
            currency="USD",
        )
        assert listing.price_amount == Decimal("0.00")

    def test_minimum_order_price(self, channel):
        """Test minimum order price for shipping."""
        zone = ShippingZone.objects.create(name="Min Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Min Order Method",
            shipping_zone=zone,
            type="price",
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("5.00"),
            minimum_order_price_amount=Decimal("50.00"),
            currency="USD",
        )
        assert listing.minimum_order_price_amount == Decimal("50.00")


@pytest.mark.django_db
class TestShippingZoneWarehouses:
    """Test shipping zone warehouse relationships."""

    def test_add_warehouse_to_zone(self, warehouse):
        """Test adding warehouse to shipping zone."""
        zone = ShippingZone.objects.create(name="Warehouse Zone", default=False)
        zone.warehouses.add(warehouse)
        
        assert warehouse in zone.warehouses.all()

    def test_multiple_warehouses(self, address):
        """Test multiple warehouses in zone."""
        wh1 = Warehouse.objects.create(name="WH1", slug="wh1", address=address)
        wh2 = Warehouse.objects.create(name="WH2", slug="wh2", address=address)
        
        zone = ShippingZone.objects.create(name="Multi WH Zone", default=False)
        zone.warehouses.add(wh1, wh2)
        
        assert zone.warehouses.count() == 2


@pytest.mark.django_db
class TestShippingZoneChannels:
    """Test shipping zone channel relationships."""

    def test_add_channel_to_zone(self, channel):
        """Test adding channel to shipping zone."""
        zone = ShippingZone.objects.create(name="Channel Zone", default=False)
        zone.channels.add(channel)
        
        assert channel in zone.channels.all()


@pytest.mark.django_db
class TestShippingMethodWeights:
    """Test shipping method weight constraints."""

    def test_method_with_min_weight(self):
        """Test method with minimum weight."""
        zone = ShippingZone.objects.create(name="Min Weight Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Heavy Items",
            shipping_zone=zone,
            type="weight",
            minimum_order_weight=Weight(kg=5),
        )
        assert method.minimum_order_weight == Weight(kg=5)

    def test_method_with_max_weight(self):
        """Test method with maximum weight."""
        zone = ShippingZone.objects.create(name="Max Weight Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Light Items",
            shipping_zone=zone,
            type="weight",
            maximum_order_weight=Weight(kg=2),
        )
        assert method.maximum_order_weight == Weight(kg=2)


@pytest.mark.django_db
class TestShippingMethodDeliveryTime:
    """Test shipping method delivery time."""

    def test_method_with_delivery_days(self):
        """Test method with delivery days."""
        zone = ShippingZone.objects.create(name="Delivery Zone", default=False)
        method = ShippingMethod.objects.create(
            name="3-5 Day Shipping",
            shipping_zone=zone,
            type="price",
            minimum_delivery_days=3,
            maximum_delivery_days=5,
        )
        assert method.minimum_delivery_days == 3
        assert method.maximum_delivery_days == 5


@pytest.mark.django_db
class TestShippingQueries:
    """Test shipping query functionality."""

    def test_filter_zones_by_default(self):
        """Test filtering zones by default flag."""
        default_zone = ShippingZone.objects.create(name="Default", default=True)
        ShippingZone.objects.create(name="Non-Default", default=False)
        
        default_zones = ShippingZone.objects.filter(default=True)
        assert default_zone in default_zones

    def test_filter_methods_by_zone(self):
        """Test filtering methods by zone."""
        zone = ShippingZone.objects.create(name="Query Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Query Method",
            shipping_zone=zone,
            type="price",
        )
        
        methods = ShippingMethod.objects.filter(shipping_zone=zone)
        assert method in methods


@pytest.mark.django_db
class TestShippingMethodMetadata:
    """Test shipping method metadata."""

    def test_method_metadata(self):
        """Test shipping method metadata."""
        zone = ShippingZone.objects.create(name="Meta Zone", default=False)
        method = ShippingMethod.objects.create(
            name="Meta Method",
            shipping_zone=zone,
            type="price",
        )
        method.metadata = {"carrier": "FedEx"}
        method.save()
        method.refresh_from_db()
        assert method.metadata.get("carrier") == "FedEx"

