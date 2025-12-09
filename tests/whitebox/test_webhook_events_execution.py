"""
Tests for webhook event types to increase coverage.
"""
import pytest

from saleor.webhook.event_types import (
    WebhookEventSyncType,
    WebhookEventAsyncType,
)
from saleor.webhook.deprecated_event_types import (
    WebhookEventType,
)


class TestWebhookEventSyncType:
    """Test all WebhookEventSyncType values."""

    def test_payment_list_gateways(self):
        assert WebhookEventSyncType.PAYMENT_LIST_GATEWAYS == "payment_list_gateways"

    def test_payment_authorize(self):
        assert WebhookEventSyncType.PAYMENT_AUTHORIZE == "payment_authorize"

    def test_payment_capture(self):
        assert WebhookEventSyncType.PAYMENT_CAPTURE == "payment_capture"

    def test_payment_refund(self):
        assert WebhookEventSyncType.PAYMENT_REFUND == "payment_refund"

    def test_payment_void(self):
        assert WebhookEventSyncType.PAYMENT_VOID == "payment_void"

    def test_payment_confirm(self):
        assert WebhookEventSyncType.PAYMENT_CONFIRM == "payment_confirm"

    def test_payment_process(self):
        assert WebhookEventSyncType.PAYMENT_PROCESS == "payment_process"

    def test_checkout_calculate_taxes(self):
        assert WebhookEventSyncType.CHECKOUT_CALCULATE_TAXES == "checkout_calculate_taxes"

    def test_order_calculate_taxes(self):
        assert WebhookEventSyncType.ORDER_CALCULATE_TAXES == "order_calculate_taxes"

    def test_shipping_list_methods_for_checkout(self):
        assert WebhookEventSyncType.SHIPPING_LIST_METHODS_FOR_CHECKOUT == "shipping_list_methods_for_checkout"

    def test_checkout_filter_shipping_methods(self):
        assert WebhookEventSyncType.CHECKOUT_FILTER_SHIPPING_METHODS == "checkout_filter_shipping_methods"

    def test_order_filter_shipping_methods(self):
        assert WebhookEventSyncType.ORDER_FILTER_SHIPPING_METHODS == "order_filter_shipping_methods"


class TestWebhookEventAsyncType:
    """Test WebhookEventAsyncType values."""

    def test_account_confirmation_requested(self):
        assert WebhookEventAsyncType.ACCOUNT_CONFIRMATION_REQUESTED == "account_confirmation_requested"

    def test_account_change_email_requested(self):
        assert WebhookEventAsyncType.ACCOUNT_CHANGE_EMAIL_REQUESTED == "account_change_email_requested"

    def test_account_email_changed(self):
        assert WebhookEventAsyncType.ACCOUNT_EMAIL_CHANGED == "account_email_changed"

    def test_account_set_password_requested(self):
        assert WebhookEventAsyncType.ACCOUNT_SET_PASSWORD_REQUESTED == "account_set_password_requested"

    def test_account_confirmed(self):
        assert WebhookEventAsyncType.ACCOUNT_CONFIRMED == "account_confirmed"

    def test_account_delete_requested(self):
        assert WebhookEventAsyncType.ACCOUNT_DELETE_REQUESTED == "account_delete_requested"

    def test_account_deleted(self):
        assert WebhookEventAsyncType.ACCOUNT_DELETED == "account_deleted"

    def test_address_created(self):
        assert WebhookEventAsyncType.ADDRESS_CREATED == "address_created"

    def test_address_updated(self):
        assert WebhookEventAsyncType.ADDRESS_UPDATED == "address_updated"

    def test_address_deleted(self):
        assert WebhookEventAsyncType.ADDRESS_DELETED == "address_deleted"

    def test_app_installed(self):
        assert WebhookEventAsyncType.APP_INSTALLED == "app_installed"

    def test_app_updated(self):
        assert WebhookEventAsyncType.APP_UPDATED == "app_updated"

    def test_app_deleted(self):
        assert WebhookEventAsyncType.APP_DELETED == "app_deleted"

    def test_app_status_changed(self):
        assert WebhookEventAsyncType.APP_STATUS_CHANGED == "app_status_changed"

    def test_attribute_created(self):
        assert WebhookEventAsyncType.ATTRIBUTE_CREATED == "attribute_created"

    def test_attribute_updated(self):
        assert WebhookEventAsyncType.ATTRIBUTE_UPDATED == "attribute_updated"

    def test_attribute_deleted(self):
        assert WebhookEventAsyncType.ATTRIBUTE_DELETED == "attribute_deleted"

    def test_attribute_value_created(self):
        assert WebhookEventAsyncType.ATTRIBUTE_VALUE_CREATED == "attribute_value_created"

    def test_attribute_value_updated(self):
        assert WebhookEventAsyncType.ATTRIBUTE_VALUE_UPDATED == "attribute_value_updated"

    def test_attribute_value_deleted(self):
        assert WebhookEventAsyncType.ATTRIBUTE_VALUE_DELETED == "attribute_value_deleted"

    def test_category_created(self):
        assert WebhookEventAsyncType.CATEGORY_CREATED == "category_created"

    def test_category_updated(self):
        assert WebhookEventAsyncType.CATEGORY_UPDATED == "category_updated"

    def test_category_deleted(self):
        assert WebhookEventAsyncType.CATEGORY_DELETED == "category_deleted"

    def test_channel_created(self):
        assert WebhookEventAsyncType.CHANNEL_CREATED == "channel_created"

    def test_channel_updated(self):
        assert WebhookEventAsyncType.CHANNEL_UPDATED == "channel_updated"

    def test_channel_deleted(self):
        assert WebhookEventAsyncType.CHANNEL_DELETED == "channel_deleted"

    def test_channel_status_changed(self):
        assert WebhookEventAsyncType.CHANNEL_STATUS_CHANGED == "channel_status_changed"

    def test_checkout_created(self):
        assert WebhookEventAsyncType.CHECKOUT_CREATED == "checkout_created"

    def test_checkout_updated(self):
        assert WebhookEventAsyncType.CHECKOUT_UPDATED == "checkout_updated"

    def test_checkout_fully_paid(self):
        assert WebhookEventAsyncType.CHECKOUT_FULLY_PAID == "checkout_fully_paid"

    def test_collection_created(self):
        assert WebhookEventAsyncType.COLLECTION_CREATED == "collection_created"

    def test_collection_updated(self):
        assert WebhookEventAsyncType.COLLECTION_UPDATED == "collection_updated"

    def test_collection_deleted(self):
        assert WebhookEventAsyncType.COLLECTION_DELETED == "collection_deleted"

    def test_customer_created(self):
        assert WebhookEventAsyncType.CUSTOMER_CREATED == "customer_created"

    def test_customer_updated(self):
        assert WebhookEventAsyncType.CUSTOMER_UPDATED == "customer_updated"

    def test_customer_deleted(self):
        assert WebhookEventAsyncType.CUSTOMER_DELETED == "customer_deleted"

    def test_customer_metadata_updated(self):
        assert WebhookEventAsyncType.CUSTOMER_METADATA_UPDATED == "customer_metadata_updated"

    def test_draft_order_created(self):
        assert WebhookEventAsyncType.DRAFT_ORDER_CREATED == "draft_order_created"

    def test_draft_order_updated(self):
        assert WebhookEventAsyncType.DRAFT_ORDER_UPDATED == "draft_order_updated"

    def test_draft_order_deleted(self):
        assert WebhookEventAsyncType.DRAFT_ORDER_DELETED == "draft_order_deleted"

    def test_fulfillment_created(self):
        assert WebhookEventAsyncType.FULFILLMENT_CREATED == "fulfillment_created"

    def test_fulfillment_canceled(self):
        assert WebhookEventAsyncType.FULFILLMENT_CANCELED == "fulfillment_canceled"

    def test_fulfillment_approved(self):
        assert WebhookEventAsyncType.FULFILLMENT_APPROVED == "fulfillment_approved"

    def test_gift_card_created(self):
        assert WebhookEventAsyncType.GIFT_CARD_CREATED == "gift_card_created"

    def test_gift_card_updated(self):
        assert WebhookEventAsyncType.GIFT_CARD_UPDATED == "gift_card_updated"

    def test_gift_card_deleted(self):
        assert WebhookEventAsyncType.GIFT_CARD_DELETED == "gift_card_deleted"

    def test_gift_card_sent(self):
        assert WebhookEventAsyncType.GIFT_CARD_SENT == "gift_card_sent"

    def test_gift_card_status_changed(self):
        assert WebhookEventAsyncType.GIFT_CARD_STATUS_CHANGED == "gift_card_status_changed"

    def test_gift_card_metadata_updated(self):
        assert WebhookEventAsyncType.GIFT_CARD_METADATA_UPDATED == "gift_card_metadata_updated"

    def test_invoice_requested(self):
        assert WebhookEventAsyncType.INVOICE_REQUESTED == "invoice_requested"

    def test_invoice_deleted(self):
        assert WebhookEventAsyncType.INVOICE_DELETED == "invoice_deleted"

    def test_invoice_sent(self):
        assert WebhookEventAsyncType.INVOICE_SENT == "invoice_sent"

    def test_menu_created(self):
        assert WebhookEventAsyncType.MENU_CREATED == "menu_created"

    def test_menu_updated(self):
        assert WebhookEventAsyncType.MENU_UPDATED == "menu_updated"

    def test_menu_deleted(self):
        assert WebhookEventAsyncType.MENU_DELETED == "menu_deleted"

    def test_menu_item_created(self):
        assert WebhookEventAsyncType.MENU_ITEM_CREATED == "menu_item_created"

    def test_menu_item_updated(self):
        assert WebhookEventAsyncType.MENU_ITEM_UPDATED == "menu_item_updated"

    def test_menu_item_deleted(self):
        assert WebhookEventAsyncType.MENU_ITEM_DELETED == "menu_item_deleted"

    def test_order_created(self):
        assert WebhookEventAsyncType.ORDER_CREATED == "order_created"

    def test_order_confirmed(self):
        assert WebhookEventAsyncType.ORDER_CONFIRMED == "order_confirmed"

    def test_order_paid(self):
        assert WebhookEventAsyncType.ORDER_PAID == "order_paid"

    def test_order_fully_paid(self):
        assert WebhookEventAsyncType.ORDER_FULLY_PAID == "order_fully_paid"

    def test_order_refunded(self):
        assert WebhookEventAsyncType.ORDER_REFUNDED == "order_refunded"

    def test_order_fully_refunded(self):
        assert WebhookEventAsyncType.ORDER_FULLY_REFUNDED == "order_fully_refunded"

    def test_order_updated(self):
        assert WebhookEventAsyncType.ORDER_UPDATED == "order_updated"

    def test_order_cancelled(self):
        assert WebhookEventAsyncType.ORDER_CANCELLED == "order_cancelled"

    def test_order_expired(self):
        assert WebhookEventAsyncType.ORDER_EXPIRED == "order_expired"

    def test_order_fulfilled(self):
        assert WebhookEventAsyncType.ORDER_FULFILLED == "order_fulfilled"

    def test_order_metadata_updated(self):
        assert WebhookEventAsyncType.ORDER_METADATA_UPDATED == "order_metadata_updated"

    def test_page_created(self):
        assert WebhookEventAsyncType.PAGE_CREATED == "page_created"

    def test_page_updated(self):
        assert WebhookEventAsyncType.PAGE_UPDATED == "page_updated"

    def test_page_deleted(self):
        assert WebhookEventAsyncType.PAGE_DELETED == "page_deleted"

    def test_page_type_created(self):
        assert WebhookEventAsyncType.PAGE_TYPE_CREATED == "page_type_created"

    def test_page_type_updated(self):
        assert WebhookEventAsyncType.PAGE_TYPE_UPDATED == "page_type_updated"

    def test_page_type_deleted(self):
        assert WebhookEventAsyncType.PAGE_TYPE_DELETED == "page_type_deleted"

    def test_permission_group_created(self):
        assert WebhookEventAsyncType.PERMISSION_GROUP_CREATED == "permission_group_created"

    def test_permission_group_updated(self):
        assert WebhookEventAsyncType.PERMISSION_GROUP_UPDATED == "permission_group_updated"

    def test_permission_group_deleted(self):
        assert WebhookEventAsyncType.PERMISSION_GROUP_DELETED == "permission_group_deleted"

    def test_product_created(self):
        assert WebhookEventAsyncType.PRODUCT_CREATED == "product_created"

    def test_product_updated(self):
        assert WebhookEventAsyncType.PRODUCT_UPDATED == "product_updated"

    def test_product_deleted(self):
        assert WebhookEventAsyncType.PRODUCT_DELETED == "product_deleted"

    def test_product_media_created(self):
        assert WebhookEventAsyncType.PRODUCT_MEDIA_CREATED == "product_media_created"

    def test_product_media_updated(self):
        assert WebhookEventAsyncType.PRODUCT_MEDIA_UPDATED == "product_media_updated"

    def test_product_media_deleted(self):
        assert WebhookEventAsyncType.PRODUCT_MEDIA_DELETED == "product_media_deleted"

    def test_product_metadata_updated(self):
        assert WebhookEventAsyncType.PRODUCT_METADATA_UPDATED == "product_metadata_updated"

    def test_product_variant_created(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_CREATED == "product_variant_created"

    def test_product_variant_updated(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_UPDATED == "product_variant_updated"

    def test_product_variant_deleted(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_DELETED == "product_variant_deleted"

    def test_product_variant_back_in_stock(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_BACK_IN_STOCK == "product_variant_back_in_stock"

    def test_product_variant_out_of_stock(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_OUT_OF_STOCK == "product_variant_out_of_stock"

    def test_product_variant_stock_updated(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_STOCK_UPDATED == "product_variant_stock_updated"

    def test_product_variant_metadata_updated(self):
        assert WebhookEventAsyncType.PRODUCT_VARIANT_METADATA_UPDATED == "product_variant_metadata_updated"


class TestDeprecatedWebhookEventType:
    """Test deprecated webhook event type."""

    def test_deprecated_event_type_exists(self):
        assert WebhookEventType is not None

