"""
Tests for saleor/shipping/interface.py
These tests actually execute the real code to increase coverage.
"""
import pytest
from decimal import Decimal
from measurement.measures import Weight
from prices import Money

from saleor.shipping.interface import ShippingMethodData


class TestShippingMethodData:
    """Test ShippingMethodData dataclass - actual execution, no mocking."""

    def test_create_basic_shipping_method(self):
        """Test creating a basic shipping method."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
        )
        assert method.id == "1"
        assert method.price.amount == Decimal("10.00")
        assert method.price.currency == "USD"

    def test_create_shipping_method_with_all_fields(self):
        """Test creating a shipping method with all fields."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("15.00"), "EUR"),
            name="Express Shipping",
            description="Fast delivery within 1-2 days",
            type="price",
            maximum_order_price=Money(Decimal("1000.00"), "EUR"),
            minimum_order_price=Money(Decimal("10.00"), "EUR"),
            minimum_order_weight=Weight(kg=0),
            maximum_order_weight=Weight(kg=30),
            maximum_delivery_days=2,
            minimum_delivery_days=1,
            metadata={"key": "value"},
            private_metadata={"secret": "data"},
            active=True,
            message="",
        )
        assert method.name == "Express Shipping"
        assert method.description == "Fast delivery within 1-2 days"
        assert method.type == "price"
        assert method.maximum_delivery_days == 2
        assert method.minimum_delivery_days == 1

    def test_default_values(self):
        """Test default values of shipping method."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("5.00"), "USD"),
        )
        assert method.name is None
        assert method.description is None
        assert method.type is None
        assert method.maximum_order_price is None
        assert method.minimum_order_price is None
        assert method.maximum_delivery_days is None
        assert method.minimum_delivery_days is None
        assert method.metadata == {}
        assert method.private_metadata == {}
        assert method.active is True
        assert method.message == ""

    def test_is_external_with_numeric_id(self):
        """Test is_external property with numeric ID."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
        )
        # Numeric IDs are not external
        assert method.is_external is False

    def test_is_external_with_invalid_global_id(self):
        """Test is_external property with invalid global ID."""
        method = ShippingMethodData(
            id="invalid-id-format",
            price=Money(Decimal("10.00"), "USD"),
        )
        # Invalid format should return False
        assert method.is_external is False

    def test_metadata_can_be_updated(self):
        """Test that metadata can be updated."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
            metadata={"initial": "value"},
        )
        method.metadata["new_key"] = "new_value"
        assert method.metadata["new_key"] == "new_value"
        assert method.metadata["initial"] == "value"

    def test_active_status(self):
        """Test active status of shipping method."""
        active_method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
            active=True,
        )
        inactive_method = ShippingMethodData(
            id="2",
            price=Money(Decimal("10.00"), "USD"),
            active=False,
        )
        assert active_method.active is True
        assert inactive_method.active is False

    def test_message_field(self):
        """Test message field."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
            message="This shipping method is temporarily unavailable",
        )
        assert method.message == "This shipping method is temporarily unavailable"

    def test_weight_fields(self):
        """Test weight fields."""
        method = ShippingMethodData(
            id="1",
            price=Money(Decimal("10.00"), "USD"),
            minimum_order_weight=Weight(kg=1),
            maximum_order_weight=Weight(kg=50),
        )
        assert method.minimum_order_weight.kg == 1
        assert method.maximum_order_weight.kg == 50

