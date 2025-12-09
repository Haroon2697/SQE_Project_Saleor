"""
Tests for saleor/core/exceptions.py
These tests actually execute the real code to increase coverage.
"""
import pytest
from uuid import uuid4

from saleor.core.exceptions import (
    InsufficientStockData,
    UnsupportedMediaProviderException,
    NonExistingCheckoutLines,
    NonExistingCheckout,
    InsufficientStock,
    AllocationError,
    PreorderAllocationError,
    ProductNotPublished,
    PermissionDenied,
    GiftCardNotApplicable,
    CircularSubscriptionSyncEvent,
    SyncEventError,
)


class TestInsufficientStockData:
    """Test InsufficientStockData dataclass."""

    def test_create_basic_data(self):
        data = InsufficientStockData(available_quantity=5)
        assert data.available_quantity == 5
        assert data.variant is None
        assert data.checkout_line is None
        assert data.order_line is None
        assert data.warehouse_pk is None

    def test_create_data_with_warehouse(self):
        warehouse_pk = uuid4()
        data = InsufficientStockData(
            available_quantity=0,
            warehouse_pk=warehouse_pk,
        )
        assert data.warehouse_pk == warehouse_pk


class TestUnsupportedMediaProviderException:
    """Test UnsupportedMediaProviderException."""

    def test_default_message(self):
        exc = UnsupportedMediaProviderException()
        assert exc.message == "Unsupported media provider or incorrect URL."

    def test_custom_message(self):
        exc = UnsupportedMediaProviderException("Custom error message")
        assert exc.message == "Custom error message"

    def test_raises(self):
        with pytest.raises(UnsupportedMediaProviderException):
            raise UnsupportedMediaProviderException()


class TestNonExistingCheckoutLines:
    """Test NonExistingCheckoutLines exception."""

    def test_raises_with_line_pks(self):
        line_pks = {uuid4(), uuid4()}
        exc = NonExistingCheckoutLines(line_pks)
        assert exc.line_pks == line_pks

    def test_message(self):
        line_pks = {uuid4()}
        exc = NonExistingCheckoutLines(line_pks)
        assert str(exc) == "Checkout lines don't exist."


class TestNonExistingCheckout:
    """Test NonExistingCheckout exception."""

    def test_raises_with_token(self):
        token = uuid4()
        exc = NonExistingCheckout(token)
        assert exc.checkout_token == token

    def test_message(self):
        token = uuid4()
        exc = NonExistingCheckout(token)
        assert str(token) in str(exc)


class TestInsufficientStock:
    """Test InsufficientStock exception."""

    def test_raises_with_items(self):
        items = [InsufficientStockData(available_quantity=0)]
        exc = InsufficientStock(items)
        assert exc.items == items

    def test_has_code(self):
        items = [InsufficientStockData(available_quantity=0)]
        exc = InsufficientStock(items)
        from saleor.checkout.error_codes import CheckoutErrorCode
        assert exc.code == CheckoutErrorCode.INSUFFICIENT_STOCK


class TestAllocationError:
    """Test AllocationError exception."""

    def test_raises_with_order_lines(self):
        order_lines = ["line1", "line2"]
        exc = AllocationError(order_lines)
        assert exc.order_lines == order_lines

    def test_message_contains_lines(self):
        order_lines = ["line1", "line2"]
        exc = AllocationError(order_lines)
        assert "line1" in str(exc)
        assert "line2" in str(exc)


class TestPreorderAllocationError:
    """Test PreorderAllocationError exception."""

    def test_raises_with_order_line(self):
        order_line = "test_line"
        exc = PreorderAllocationError(order_line)
        assert exc.order_line == order_line

    def test_message_contains_line(self):
        order_line = "test_line"
        exc = PreorderAllocationError(order_line)
        assert "test_line" in str(exc)


class TestProductNotPublished:
    """Test ProductNotPublished exception."""

    def test_default_message(self):
        exc = ProductNotPublished()
        assert "unpublished product" in str(exc)

    def test_context(self):
        context = {"product_id": 123}
        exc = ProductNotPublished(context=context)
        assert exc.context == context

    def test_has_code(self):
        exc = ProductNotPublished()
        from saleor.checkout.error_codes import CheckoutErrorCode
        assert exc.code == CheckoutErrorCode.PRODUCT_NOT_PUBLISHED


class TestPermissionDenied:
    """Test PermissionDenied exception."""

    def test_default_message(self):
        exc = PermissionDenied()
        assert "permission" in str(exc).lower()

    def test_custom_message(self):
        exc = PermissionDenied("Custom permission error")
        assert str(exc) == "Custom permission error"

    def test_with_permissions(self):
        from enum import Enum
        class TestPermission(Enum):
            MANAGE_PRODUCTS = "manage_products"
            MANAGE_ORDERS = "manage_orders"
        
        exc = PermissionDenied(permissions=[TestPermission.MANAGE_PRODUCTS])
        assert "MANAGE_PRODUCTS" in str(exc)
        assert exc.permissions == [TestPermission.MANAGE_PRODUCTS]


class TestGiftCardNotApplicable:
    """Test GiftCardNotApplicable exception."""

    def test_message(self):
        exc = GiftCardNotApplicable("Gift card not valid")
        assert exc.message == "Gift card not valid"

    def test_has_code(self):
        exc = GiftCardNotApplicable("Error")
        from saleor.checkout.error_codes import CheckoutErrorCode
        assert exc.code == CheckoutErrorCode.GIFT_CARD_NOT_APPLICABLE.value


class TestCircularSubscriptionSyncEvent:
    """Test CircularSubscriptionSyncEvent exception."""

    def test_is_graphql_error(self):
        from graphql import GraphQLError
        exc = CircularSubscriptionSyncEvent("Circular event detected")
        assert isinstance(exc, GraphQLError)


class TestSyncEventError:
    """Test SyncEventError exception."""

    def test_message_and_code(self):
        exc = SyncEventError("Sync failed", code="SYNC_ERROR")
        assert exc.message == "Sync failed"
        assert exc.code == "SYNC_ERROR"

    def test_str(self):
        exc = SyncEventError("Test error", code="TEST")
        assert str(exc) == "Test error"

    def test_without_code(self):
        exc = SyncEventError("Error without code")
        assert exc.message == "Error without code"
        assert exc.code is None

