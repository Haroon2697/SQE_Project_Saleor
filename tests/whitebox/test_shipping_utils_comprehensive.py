"""
Comprehensive White-Box Tests for saleor/shipping/utils.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- default_shipping_zone_exists
- get_countries_without_shipping_zone
- convert_to_shipping_method_data
- convert_checkout_delivery_to_shipping_method_data
- convert_shipping_method_data_to_checkout_delivery
- initialize_shipping_method_active_status
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money

from saleor.shipping.models import ShippingZone, ShippingMethod, ShippingMethodChannelListing
from saleor.shipping.utils import (
    default_shipping_zone_exists,
    get_countries_without_shipping_zone,
    convert_to_shipping_method_data,
    convert_checkout_delivery_to_shipping_method_data,
    convert_shipping_method_data_to_checkout_delivery,
    initialize_shipping_method_active_status,
)
from saleor.shipping.interface import ShippingMethodData
from saleor.channel.models import Channel
from saleor.tax.models import TaxClass
from saleor.checkout.models import Checkout, CheckoutDelivery
from saleor.plugins.base_plugin import ExcludedShippingMethod


@pytest.mark.django_db
class TestDefaultShippingZoneExists:
    """Test default_shipping_zone_exists() - Statement Coverage"""

    def test_default_shipping_zone_exists_returns_queryset_when_zone_exists(self):
        """Statement: Return queryset with default zone"""
        zone = ShippingZone.objects.create(
            name="Default Zone",
            countries=["US"],
            default=True
        )

        result = default_shipping_zone_exists()
        assert result.count() == 1
        assert result.first() == zone

    def test_default_shipping_zone_exists_returns_empty_when_no_default(self):
        """Statement: Return empty queryset when no default zone"""
        ShippingZone.objects.create(
            name="Non-Default Zone",
            countries=["US"],
            default=False
        )

        result = default_shipping_zone_exists()
        assert result.count() == 0

    def test_default_shipping_zone_exists_excludes_specified_pk(self):
        """Statement: Exclude specified zone_pk from result"""
        zone1 = ShippingZone.objects.create(
            name="Default Zone 1",
            countries=["US"],
            default=True
        )
        zone2 = ShippingZone.objects.create(
            name="Default Zone 2",
            countries=["CA"],
            default=True
        )

        result = default_shipping_zone_exists(zone_pk=zone1.pk)
        assert result.count() == 1
        assert result.first() == zone2


@pytest.mark.django_db
class TestGetCountriesWithoutShippingZone:
    """Test get_countries_without_shipping_zone() - Statement Coverage"""

    def test_get_countries_without_shipping_zone_returns_uncovered_countries(self):
        """Statement: Return countries not in any zone"""
        ShippingZone.objects.create(
            name="US Zone",
            countries=["US"]
        )
        ShippingZone.objects.create(
            name="CA Zone",
            countries=["CA"]
        )

        uncovered = list(get_countries_without_shipping_zone())
        assert "US" not in uncovered
        assert "CA" not in uncovered
        assert "GB" in uncovered  # Should be uncovered
        assert "FR" in uncovered  # Should be uncovered

    def test_get_countries_without_shipping_zone_returns_all_when_no_zones(self):
        """Statement: Return all countries when no zones exist"""
        uncovered = list(get_countries_without_shipping_zone())
        assert len(uncovered) > 0
        assert "US" in uncovered
        assert "CA" in uncovered

    def test_get_countries_without_shipping_zone_handles_multiple_countries_in_zone(self):
        """Statement: Handle zones with multiple countries"""
        ShippingZone.objects.create(
            name="Multi Zone",
            countries=["US", "CA", "MX"]
        )

        uncovered = list(get_countries_without_shipping_zone())
        assert "US" not in uncovered
        assert "CA" not in uncovered
        assert "MX" not in uncovered
        assert "GB" in uncovered


@pytest.mark.django_db
class TestConvertToShippingMethodData:
    """Test convert_to_shipping_method_data() - Statement Coverage"""

    def test_convert_to_shipping_method_data_with_tax_class(self):
        """Statement: Convert with provided tax_class"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        tax_class = TaxClass.objects.create(name="Standard Tax")
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone,
            tax_class=tax_class
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency="USD",
            minimum_order_price_amount=Decimal("50.00"),
            maximum_order_price_amount=Decimal("1000.00")
        )

        result = convert_to_shipping_method_data(method, listing, tax_class)

        assert isinstance(result, ShippingMethodData)
        assert result.id == str(method.id)
        assert result.name == "Standard Shipping"
        assert result.price == Money(Decimal("10.00"), "USD")
        assert result.tax_class == tax_class
        assert result.minimum_order_price == Money(Decimal("50.00"), "USD")
        assert result.maximum_order_price == Money(Decimal("1000.00"), "USD")

    def test_convert_to_shipping_method_data_without_tax_class(self):
        """Statement: Convert without tax_class, fallback to method.tax_class"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        tax_class = TaxClass.objects.create(name="Standard Tax")
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone,
            tax_class=tax_class
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency="USD"
        )

        result = convert_to_shipping_method_data(method, listing, tax_class=None)

        assert isinstance(result, ShippingMethodData)
        assert result.tax_class == tax_class

    def test_convert_to_shipping_method_data_with_weight_based_method(self):
        """Statement: Convert weight-based shipping method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        from measurement.measures import Weight
        method = ShippingMethod.objects.create(
            name="Weight Shipping",
            type="WEIGHT_BASED",
            shipping_zone=zone,
            minimum_order_weight=Weight(kg=1),
            maximum_order_weight=Weight(kg=10)
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("15.00"),
            currency="USD"
        )

        result = convert_to_shipping_method_data(method, listing)

        assert result.type == "WEIGHT_BASED"
        assert result.minimum_order_weight == Weight(kg=1)
        assert result.maximum_order_weight == Weight(kg=10)

    def test_convert_to_shipping_method_data_with_metadata(self):
        """Statement: Convert with metadata and private_metadata"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone,
            metadata={"key": "value"},
            private_metadata={"private": "data"}
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency="USD"
        )

        result = convert_to_shipping_method_data(method, listing)

        assert result.metadata == {"key": "value"}
        assert result.private_metadata == {"private": "data"}

    def test_convert_to_shipping_method_data_with_delivery_days(self):
        """Statement: Convert with delivery days"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        zone = ShippingZone.objects.create(
            name="Test Zone",
            countries=["US"]
        )
        method = ShippingMethod.objects.create(
            name="Standard Shipping",
            type="PRICE_BASED",
            shipping_zone=zone,
            minimum_delivery_days=3,
            maximum_delivery_days=7
        )
        listing = ShippingMethodChannelListing.objects.create(
            shipping_method=method,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency="USD"
        )

        result = convert_to_shipping_method_data(method, listing)

        assert result.minimum_delivery_days == 3
        assert result.maximum_delivery_days == 7


@pytest.mark.django_db
class TestConvertCheckoutDeliveryToShippingMethodData:
    """Test convert_checkout_delivery_to_shipping_method_data() - Statement Coverage"""

    def test_convert_checkout_delivery_to_shipping_method_data(self):
        """Statement: Convert CheckoutDelivery to ShippingMethodData"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        tax_class = TaxClass.objects.create(name="Standard Tax")
        delivery = CheckoutDelivery.objects.create(
            checkout=checkout,
            shipping_method_id="123",
            name="Standard Shipping",
            description="Test description",
            price_amount=Decimal("10.00"),
            currency="USD",
            minimum_delivery_days=3,
            maximum_delivery_days=7,
            metadata={"key": "value"},
            private_metadata={"private": "data"},
            active=True,
            is_valid=True,
            tax_class_id=tax_class.id,
            tax_class_name="Standard Tax",
            tax_class_metadata={"tax": "meta"},
            tax_class_private_metadata={"tax": "private"}
        )

        result = convert_checkout_delivery_to_shipping_method_data(delivery)

        assert isinstance(result, ShippingMethodData)
        assert result.id == "123"
        assert result.name == "Standard Shipping"
        assert result.description == "Test description"
        assert result.price == Money(Decimal("10.00"), "USD")
        assert result.active is True
        assert result.minimum_delivery_days == 3
        assert result.maximum_delivery_days == 7
        assert result.metadata == {"key": "value"}
        assert result.private_metadata == {"private": "data"}
        assert result.tax_class.id == tax_class.id
        assert result.tax_class.name == "Standard Tax"

    def test_convert_checkout_delivery_with_message(self):
        """Statement: Convert with message"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        delivery = CheckoutDelivery.objects.create(
            checkout=checkout,
            shipping_method_id="123",
            name="Standard Shipping",
            price_amount=Decimal("10.00"),
            currency="USD",
            message="Shipping unavailable"
        )

        result = convert_checkout_delivery_to_shipping_method_data(delivery)

        assert result.message == "Shipping unavailable"

    def test_convert_checkout_delivery_with_inactive_status(self):
        """Statement: Convert with inactive status"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        delivery = CheckoutDelivery.objects.create(
            checkout=checkout,
            shipping_method_id="123",
            name="Standard Shipping",
            price_amount=Decimal("10.00"),
            currency="USD",
            active=False,
            is_valid=True
        )

        result = convert_checkout_delivery_to_shipping_method_data(delivery)

        assert result.active is False

    def test_convert_checkout_delivery_with_invalid_status(self):
        """Statement: Convert with invalid status"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        delivery = CheckoutDelivery.objects.create(
            checkout=checkout,
            shipping_method_id="123",
            name="Standard Shipping",
            price_amount=Decimal("10.00"),
            currency="USD",
            active=True,
            is_valid=False
        )

        result = convert_checkout_delivery_to_shipping_method_data(delivery)

        assert result.active is False  # Should be False because is_valid is False

    def test_convert_checkout_delivery_with_empty_message(self):
        """Statement: Convert with empty message"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        delivery = CheckoutDelivery.objects.create(
            checkout=checkout,
            shipping_method_id="123",
            name="Standard Shipping",
            price_amount=Decimal("10.00"),
            currency="USD",
            message=None
        )

        result = convert_checkout_delivery_to_shipping_method_data(delivery)

        assert result.message == ""


@pytest.mark.django_db
class TestConvertShippingMethodDataToCheckoutDelivery:
    """Test convert_shipping_method_data_to_checkout_delivery() - Statement Coverage"""

    def test_convert_shipping_method_data_to_checkout_delivery_built_in(self):
        """Statement: Convert built-in shipping method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        tax_class = TaxClass.objects.create(name="Standard Tax")
        shipping_data = ShippingMethodData(
            id="123",
            name="Standard Shipping",
            description="Test description",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD"),
            tax_class=tax_class,
            minimum_delivery_days=3,
            maximum_delivery_days=7,
            metadata={"key": "value"},
            private_metadata={"private": "data"},
            active=True,
            message="",
            is_external=False
        )

        result = convert_shipping_method_data_to_checkout_delivery(shipping_data, checkout)

        assert isinstance(result, CheckoutDelivery)
        assert result.checkout == checkout
        assert result.built_in_shipping_method_id == 123
        assert result.external_shipping_method_id is None
        assert result.name == "Standard Shipping"
        assert result.description == "Test description"
        assert result.price_amount == Decimal("10.00")
        assert result.currency == "USD"
        assert result.minimum_delivery_days == 3
        assert result.maximum_delivery_days == 7
        assert result.metadata == {"key": "value"}
        assert result.private_metadata == {"private": "data"}
        assert result.active is True
        assert result.is_valid is True
        assert result.is_external is False
        assert result.tax_class_id == tax_class.id
        assert result.tax_class_name == "Standard Tax"

    def test_convert_shipping_method_data_to_checkout_delivery_external(self):
        """Statement: Convert external shipping method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        shipping_data = ShippingMethodData(
            id="external-123",
            name="External Shipping",
            type="PRICE_BASED",
            price=Money(Decimal("15.00"), "USD"),
            is_external=True
        )

        result = convert_shipping_method_data_to_checkout_delivery(shipping_data, checkout)

        assert result.built_in_shipping_method_id is None
        assert result.external_shipping_method_id == "external-123"
        assert result.is_external is True

    def test_convert_shipping_method_data_to_checkout_delivery_without_tax_class(self):
        """Statement: Convert without tax_class"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        shipping_data = ShippingMethodData(
            id="123",
            name="Standard Shipping",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD"),
            tax_class=None,
            is_external=False
        )

        result = convert_shipping_method_data_to_checkout_delivery(shipping_data, checkout)

        assert result.tax_class_id is None
        assert result.tax_class_name is None

    def test_convert_shipping_method_data_to_checkout_delivery_with_message(self):
        """Statement: Convert with message"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        shipping_data = ShippingMethodData(
            id="123",
            name="Standard Shipping",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD"),
            message="Shipping unavailable",
            is_external=False
        )

        result = convert_shipping_method_data_to_checkout_delivery(shipping_data, checkout)

        assert result.message == "Shipping unavailable"

    def test_convert_shipping_method_data_to_checkout_delivery_with_empty_name(self):
        """Statement: Convert with empty name"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        shipping_data = ShippingMethodData(
            id="123",
            name=None,
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD"),
            is_external=False
        )

        result = convert_shipping_method_data_to_checkout_delivery(shipping_data, checkout)

        assert result.name == ""


@pytest.mark.django_db
class TestInitializeShippingMethodActiveStatus:
    """Test initialize_shipping_method_active_status() - Statement Coverage"""

    def test_initialize_shipping_method_active_status_all_active(self):
        """Statement: Initialize all methods as active when no exclusions"""
        method1 = ShippingMethodData(
            id="1",
            name="Method 1",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD")
        )
        method2 = ShippingMethodData(
            id="2",
            name="Method 2",
            type="PRICE_BASED",
            price=Money(Decimal("15.00"), "USD")
        )
        methods = [method1, method2]
        excluded_methods = []

        initialize_shipping_method_active_status(methods, excluded_methods)

        assert method1.active is True
        assert method1.message == ""
        assert method2.active is True
        assert method2.message == ""

    def test_initialize_shipping_method_active_status_with_exclusions(self):
        """Statement: Set excluded methods as inactive with reason"""
        method1 = ShippingMethodData(
            id="1",
            name="Method 1",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD")
        )
        method2 = ShippingMethodData(
            id="2",
            name="Method 2",
            type="PRICE_BASED",
            price=Money(Decimal("15.00"), "USD")
        )
        methods = [method1, method2]
        excluded_methods = [
            ExcludedShippingMethod(id="1", reason="Not available in your area")
        ]

        initialize_shipping_method_active_status(methods, excluded_methods)

        assert method1.active is False
        assert method1.message == "Not available in your area"
        assert method2.active is True
        assert method2.message == ""

    def test_initialize_shipping_method_active_status_partial_exclusions(self):
        """Statement: Handle partial exclusions"""
        method1 = ShippingMethodData(
            id="1",
            name="Method 1",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD")
        )
        method2 = ShippingMethodData(
            id="2",
            name="Method 2",
            type="PRICE_BASED",
            price=Money(Decimal("15.00"), "USD")
        )
        method3 = ShippingMethodData(
            id="3",
            name="Method 3",
            type="PRICE_BASED",
            price=Money(Decimal("20.00"), "USD")
        )
        methods = [method1, method2, method3]
        excluded_methods = [
            ExcludedShippingMethod(id="1", reason="Reason 1"),
            ExcludedShippingMethod(id="3", reason="Reason 3")
        ]

        initialize_shipping_method_active_status(methods, excluded_methods)

        assert method1.active is False
        assert method1.message == "Reason 1"
        assert method2.active is True
        assert method2.message == ""
        assert method3.active is False
        assert method3.message == "Reason 3"

    def test_initialize_shipping_method_active_status_resets_existing_status(self):
        """Statement: Reset existing inactive status to active if not excluded"""
        method1 = ShippingMethodData(
            id="1",
            name="Method 1",
            type="PRICE_BASED",
            price=Money(Decimal("10.00"), "USD"),
            active=False,
            message="Previous message"
        )
        methods = [method1]
        excluded_methods = []

        initialize_shipping_method_active_status(methods, excluded_methods)

        assert method1.active is True
        assert method1.message == ""

    def test_initialize_shipping_method_active_status_empty_list(self):
        """Statement: Handle empty methods list"""
        methods = []
        excluded_methods = []

        initialize_shipping_method_active_status(methods, excluded_methods)

        assert len(methods) == 0

