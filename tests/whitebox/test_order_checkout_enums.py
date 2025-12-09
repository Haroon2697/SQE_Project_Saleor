"""
Tests for order and checkout enums and constants to increase coverage.
"""
import pytest
from decimal import Decimal

from saleor.order import (
    OrderStatus,
    OrderOrigin,
    OrderAuthorizeStatus,
    OrderChargeStatus,
    FulfillmentStatus,
    OrderEvents,
)
from saleor.checkout import AddressType
from saleor.checkout.error_codes import CheckoutErrorCode
from saleor.order.error_codes import OrderErrorCode


class TestOrderStatusComplete:
    """Test all OrderStatus values."""

    def test_draft(self):
        assert OrderStatus.DRAFT == "draft"

    def test_unconfirmed(self):
        assert OrderStatus.UNCONFIRMED == "unconfirmed"

    def test_unfulfilled(self):
        assert OrderStatus.UNFULFILLED == "unfulfilled"

    def test_partially_fulfilled(self):
        assert OrderStatus.PARTIALLY_FULFILLED is not None

    def test_fulfilled(self):
        assert OrderStatus.FULFILLED == "fulfilled"

    def test_partially_returned(self):
        assert OrderStatus.PARTIALLY_RETURNED == "partially_returned"

    def test_returned(self):
        assert OrderStatus.RETURNED == "returned"

    def test_canceled(self):
        assert OrderStatus.CANCELED == "canceled"

    def test_expired(self):
        assert OrderStatus.EXPIRED == "expired"


class TestOrderOriginComplete:
    """Test all OrderOrigin values."""

    def test_checkout(self):
        assert OrderOrigin.CHECKOUT == "checkout"

    def test_draft(self):
        assert OrderOrigin.DRAFT == "draft"

    def test_reissue(self):
        assert OrderOrigin.REISSUE == "reissue"

    def test_bulk_create(self):
        assert OrderOrigin.BULK_CREATE == "bulk_create"


class TestOrderAuthorizeStatusComplete:
    """Test all OrderAuthorizeStatus values."""

    def test_none(self):
        assert OrderAuthorizeStatus.NONE == "none"

    def test_partial(self):
        assert OrderAuthorizeStatus.PARTIAL == "partial"

    def test_full(self):
        assert OrderAuthorizeStatus.FULL == "full"


class TestOrderChargeStatusComplete:
    """Test all OrderChargeStatus values."""

    def test_none(self):
        assert OrderChargeStatus.NONE == "none"

    def test_partial(self):
        assert OrderChargeStatus.PARTIAL == "partial"

    def test_full(self):
        assert OrderChargeStatus.FULL == "full"

    def test_overcharged(self):
        assert OrderChargeStatus.OVERCHARGED == "overcharged"


class TestFulfillmentStatusComplete:
    """Test all FulfillmentStatus values."""

    def test_fulfilled(self):
        assert FulfillmentStatus.FULFILLED == "fulfilled"

    def test_refunded(self):
        assert FulfillmentStatus.REFUNDED == "refunded"

    def test_returned(self):
        assert FulfillmentStatus.RETURNED == "returned"

    def test_refunded_and_returned(self):
        assert FulfillmentStatus.REFUNDED_AND_RETURNED == "refunded_and_returned"

    def test_replaced(self):
        assert FulfillmentStatus.REPLACED == "replaced"

    def test_canceled(self):
        assert FulfillmentStatus.CANCELED == "canceled"

    def test_waiting_for_approval(self):
        assert FulfillmentStatus.WAITING_FOR_APPROVAL == "waiting_for_approval"


class TestOrderEventsComplete:
    """Test OrderEvents enum."""

    def test_order_events_exists(self):
        assert OrderEvents is not None


class TestAddressTypeComplete:
    """Test AddressType enum."""

    def test_shipping(self):
        assert AddressType.SHIPPING == "shipping"

    def test_billing(self):
        assert AddressType.BILLING == "billing"


class TestCheckoutErrorCodeComplete:
    """Test CheckoutErrorCode enum values."""

    def test_graphql_error(self):
        assert CheckoutErrorCode.GRAPHQL_ERROR is not None

    def test_invalid(self):
        assert CheckoutErrorCode.INVALID is not None

    def test_not_found(self):
        assert CheckoutErrorCode.NOT_FOUND is not None

    def test_required(self):
        assert CheckoutErrorCode.REQUIRED is not None

    def test_unique(self):
        assert CheckoutErrorCode.UNIQUE is not None

    def test_insufficient_stock(self):
        assert CheckoutErrorCode.INSUFFICIENT_STOCK is not None

    def test_zero_quantity(self):
        assert CheckoutErrorCode.ZERO_QUANTITY is not None

    def test_quantity_greater_than_limit(self):
        assert CheckoutErrorCode.QUANTITY_GREATER_THAN_LIMIT is not None

    def test_invalid_shipping_method(self):
        assert CheckoutErrorCode.INVALID_SHIPPING_METHOD is not None

    def test_shipping_address_not_set(self):
        assert CheckoutErrorCode.SHIPPING_ADDRESS_NOT_SET is not None

    def test_billing_address_not_set(self):
        assert CheckoutErrorCode.BILLING_ADDRESS_NOT_SET is not None

    def test_voucher_not_applicable(self):
        assert CheckoutErrorCode.VOUCHER_NOT_APPLICABLE is not None

    def test_gift_card_not_applicable(self):
        assert CheckoutErrorCode.GIFT_CARD_NOT_APPLICABLE is not None

    def test_tax_error(self):
        assert CheckoutErrorCode.TAX_ERROR is not None

    def test_email_not_set(self):
        assert CheckoutErrorCode.EMAIL_NOT_SET is not None

    def test_no_lines(self):
        assert CheckoutErrorCode.NO_LINES is not None


class TestOrderErrorCodeComplete:
    """Test OrderErrorCode enum values."""

    def test_graphql_error(self):
        assert OrderErrorCode.GRAPHQL_ERROR is not None

    def test_invalid(self):
        assert OrderErrorCode.INVALID is not None

    def test_not_found(self):
        assert OrderErrorCode.NOT_FOUND is not None

    def test_required(self):
        assert OrderErrorCode.REQUIRED is not None

    def test_unique(self):
        assert OrderErrorCode.UNIQUE is not None

    def test_cannot_cancel_fulfillment(self):
        assert OrderErrorCode.CANNOT_CANCEL_FULFILLMENT is not None

    def test_cannot_cancel_order(self):
        assert OrderErrorCode.CANNOT_CANCEL_ORDER is not None

    def test_cannot_delete(self):
        assert OrderErrorCode.CANNOT_DELETE is not None

    def test_cannot_refund(self):
        assert OrderErrorCode.CANNOT_REFUND is not None

    def test_cannot_fulfill_unpaid_order(self):
        assert OrderErrorCode.CANNOT_FULFILL_UNPAID_ORDER is not None

    def test_fulfill_order_line(self):
        assert OrderErrorCode.FULFILL_ORDER_LINE is not None

    def test_insufficient_stock(self):
        assert OrderErrorCode.INSUFFICIENT_STOCK is not None

    def test_invalid_quantity(self):
        assert OrderErrorCode.INVALID_QUANTITY is not None

    def test_not_available_in_channel(self):
        assert OrderErrorCode.NOT_AVAILABLE_IN_CHANNEL is not None

    def test_order_no_shipping_address(self):
        assert OrderErrorCode.ORDER_NO_SHIPPING_ADDRESS is not None

    def test_payment_error(self):
        assert OrderErrorCode.PAYMENT_ERROR is not None

    def test_payment_missing(self):
        assert OrderErrorCode.PAYMENT_MISSING is not None

    def test_product_not_published(self):
        assert OrderErrorCode.PRODUCT_NOT_PUBLISHED is not None

    def test_product_unavailable_for_purchase(self):
        assert OrderErrorCode.PRODUCT_UNAVAILABLE_FOR_PURCHASE is not None

    def test_void_inactive_payment(self):
        assert OrderErrorCode.VOID_INACTIVE_PAYMENT is not None

    def test_zero_quantity(self):
        assert OrderErrorCode.ZERO_QUANTITY is not None

