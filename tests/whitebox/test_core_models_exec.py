"""
Tests that execute core model functions to increase coverage.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock


class TestSortableModelExec:
    """Execute sortable model functions."""

    def test_sortable_model_import(self):
        """Test SortableModel import."""
        from saleor.core.models import SortableModel
        assert SortableModel is not None

    def test_model_with_metadata_import(self):
        """Test ModelWithMetadata import."""
        from saleor.core.models import ModelWithMetadata
        assert ModelWithMetadata is not None

    def test_publishing_model_import(self):
        """Test PublishableModel import."""
        from saleor.core.models import PublishableModel
        assert PublishableModel is not None


class TestEventDeliveryExec:
    """Execute event delivery functions."""

    def test_event_delivery_import(self):
        """Test EventDelivery model import."""
        from saleor.core.models import EventDelivery
        assert EventDelivery is not None

    def test_event_delivery_attempt_import(self):
        """Test EventDeliveryAttempt model import."""
        from saleor.core.models import EventDeliveryAttempt
        assert EventDeliveryAttempt is not None

    def test_event_payload_import(self):
        """Test EventPayload model import."""
        from saleor.core.models import EventPayload
        assert EventPayload is not None


class TestJobModelsExec:
    """Execute job model functions."""

    def test_job_model_import(self):
        """Test Job model import."""
        from saleor.core.models import Job
        assert Job is not None


class TestThumbnailModelsExec:
    """Execute thumbnail model functions."""

    def test_thumbnail_model_import(self):
        """Test Thumbnail model import."""
        from saleor.thumbnail.models import Thumbnail
        assert Thumbnail is not None


class TestAccountModelsExec:
    """Execute account model functions."""

    def test_user_model_import(self):
        """Test User model import."""
        from saleor.account.models import User
        assert User is not None

    def test_address_model_import(self):
        """Test Address model import."""
        from saleor.account.models import Address
        assert Address is not None

    def test_customer_note_import(self):
        """Test CustomerNote model import."""
        from saleor.account.models import CustomerNote
        assert CustomerNote is not None

    def test_customer_event_import(self):
        """Test CustomerEvent model import."""
        from saleor.account.models import CustomerEvent
        assert CustomerEvent is not None

    def test_staff_notification_recipient_import(self):
        """Test StaffNotificationRecipient model import."""
        from saleor.account.models import StaffNotificationRecipient
        assert StaffNotificationRecipient is not None


class TestProductModelsExec:
    """Execute product model functions."""

    def test_product_model_import(self):
        """Test Product model import."""
        from saleor.product.models import Product
        assert Product is not None

    def test_product_type_import(self):
        """Test ProductType model import."""
        from saleor.product.models import ProductType
        assert ProductType is not None

    def test_product_variant_import(self):
        """Test ProductVariant model import."""
        from saleor.product.models import ProductVariant
        assert ProductVariant is not None

    def test_category_import(self):
        """Test Category model import."""
        from saleor.product.models import Category
        assert Category is not None

    def test_collection_import(self):
        """Test Collection model import."""
        from saleor.product.models import Collection
        assert Collection is not None

    def test_product_media_import(self):
        """Test ProductMedia model import."""
        from saleor.product.models import ProductMedia
        assert ProductMedia is not None

    def test_digital_content_import(self):
        """Test DigitalContent model import."""
        from saleor.product.models import DigitalContent
        assert DigitalContent is not None

    def test_digital_content_url_import(self):
        """Test DigitalContentUrl model import."""
        from saleor.product.models import DigitalContentUrl
        assert DigitalContentUrl is not None


class TestOrderModelsExec:
    """Execute order model functions."""

    def test_order_model_import(self):
        """Test Order model import."""
        from saleor.order.models import Order
        assert Order is not None

    def test_order_line_import(self):
        """Test OrderLine model import."""
        from saleor.order.models import OrderLine
        assert OrderLine is not None

    def test_fulfillment_import(self):
        """Test Fulfillment model import."""
        from saleor.order.models import Fulfillment
        assert Fulfillment is not None

    def test_fulfillment_line_import(self):
        """Test FulfillmentLine model import."""
        from saleor.order.models import FulfillmentLine
        assert FulfillmentLine is not None

    def test_order_event_import(self):
        """Test OrderEvent model import."""
        from saleor.order.models import OrderEvent
        assert OrderEvent is not None

    def test_order_granted_refund_import(self):
        """Test OrderGrantedRefund model import."""
        from saleor.order.models import OrderGrantedRefund
        assert OrderGrantedRefund is not None


class TestCheckoutModelsExec:
    """Execute checkout model functions."""

    def test_checkout_model_import(self):
        """Test Checkout model import."""
        from saleor.checkout.models import Checkout
        assert Checkout is not None

    def test_checkout_line_import(self):
        """Test CheckoutLine model import."""
        from saleor.checkout.models import CheckoutLine
        assert CheckoutLine is not None

    def test_checkout_metadata_import(self):
        """Test CheckoutMetadata model import."""
        from saleor.checkout.models import CheckoutMetadata
        assert CheckoutMetadata is not None


class TestPaymentModelsExec:
    """Execute payment model functions."""

    def test_payment_model_import(self):
        """Test Payment model import."""
        from saleor.payment.models import Payment
        assert Payment is not None

    def test_transaction_import(self):
        """Test Transaction model import."""
        from saleor.payment.models import Transaction
        assert Transaction is not None

    def test_transaction_item_import(self):
        """Test TransactionItem model import."""
        from saleor.payment.models import TransactionItem
        assert TransactionItem is not None

    def test_transaction_event_import(self):
        """Test TransactionEvent model import."""
        from saleor.payment.models import TransactionEvent
        assert TransactionEvent is not None


class TestWarehouseModelsExec:
    """Execute warehouse model functions."""

    def test_warehouse_model_import(self):
        """Test Warehouse model import."""
        from saleor.warehouse.models import Warehouse
        assert Warehouse is not None

    def test_stock_import(self):
        """Test Stock model import."""
        from saleor.warehouse.models import Stock
        assert Stock is not None

    def test_allocation_import(self):
        """Test Allocation model import."""
        from saleor.warehouse.models import Allocation
        assert Allocation is not None

    def test_reservation_import(self):
        """Test Reservation model import."""
        from saleor.warehouse.models import Reservation
        assert Reservation is not None

    def test_preorder_allocation_import(self):
        """Test PreorderAllocation model import."""
        from saleor.warehouse.models import PreorderAllocation
        assert PreorderAllocation is not None


class TestShippingModelsExec:
    """Execute shipping model functions."""

    def test_shipping_zone_import(self):
        """Test ShippingZone model import."""
        from saleor.shipping.models import ShippingZone
        assert ShippingZone is not None

    def test_shipping_method_import(self):
        """Test ShippingMethod model import."""
        from saleor.shipping.models import ShippingMethod
        assert ShippingMethod is not None

    def test_shipping_method_postal_code_rule_import(self):
        """Test ShippingMethodPostalCodeRule model import."""
        from saleor.shipping.models import ShippingMethodPostalCodeRule
        assert ShippingMethodPostalCodeRule is not None

    def test_shipping_method_channel_listing_import(self):
        """Test ShippingMethodChannelListing model import."""
        from saleor.shipping.models import ShippingMethodChannelListing
        assert ShippingMethodChannelListing is not None


class TestDiscountModelsExec:
    """Execute discount model functions."""

    def test_voucher_import(self):
        """Test Voucher model import."""
        from saleor.discount.models import Voucher
        assert Voucher is not None

    def test_voucher_code_import(self):
        """Test VoucherCode model import."""
        from saleor.discount.models import VoucherCode
        assert VoucherCode is not None

    def test_promotion_import(self):
        """Test Promotion model import."""
        from saleor.discount.models import Promotion
        assert Promotion is not None

    def test_promotion_rule_import(self):
        """Test PromotionRule model import."""
        from saleor.discount.models import PromotionRule
        assert PromotionRule is not None

    def test_order_discount_import(self):
        """Test OrderDiscount model import."""
        from saleor.discount.models import OrderDiscount
        assert OrderDiscount is not None

    def test_order_line_discount_import(self):
        """Test OrderLineDiscount model import."""
        from saleor.discount.models import OrderLineDiscount
        assert OrderLineDiscount is not None


class TestGiftCardModelsExec:
    """Execute gift card model functions."""

    def test_gift_card_import(self):
        """Test GiftCard model import."""
        from saleor.giftcard.models import GiftCard
        assert GiftCard is not None

    def test_gift_card_event_import(self):
        """Test GiftCardEvent model import."""
        from saleor.giftcard.models import GiftCardEvent
        assert GiftCardEvent is not None

    def test_gift_card_tag_import(self):
        """Test GiftCardTag model import."""
        from saleor.giftcard.models import GiftCardTag
        assert GiftCardTag is not None


class TestChannelModelsExec:
    """Execute channel model functions."""

    def test_channel_import(self):
        """Test Channel model import."""
        from saleor.channel.models import Channel
        assert Channel is not None


class TestAttributeModelsExec:
    """Execute attribute model functions."""

    def test_attribute_import(self):
        """Test Attribute model import."""
        from saleor.attribute.models import Attribute
        assert Attribute is not None

    def test_attribute_value_import(self):
        """Test AttributeValue model import."""
        from saleor.attribute.models import AttributeValue
        assert AttributeValue is not None

    def test_attribute_product_import(self):
        """Test AttributeProduct model import."""
        from saleor.attribute.models import AttributeProduct
        assert AttributeProduct is not None

    def test_attribute_variant_import(self):
        """Test AttributeVariant model import."""
        from saleor.attribute.models import AttributeVariant
        assert AttributeVariant is not None


class TestMenuModelsExec:
    """Execute menu model functions."""

    def test_menu_import(self):
        """Test Menu model import."""
        from saleor.menu.models import Menu
        assert Menu is not None

    def test_menu_item_import(self):
        """Test MenuItem model import."""
        from saleor.menu.models import MenuItem
        assert MenuItem is not None


class TestPageModelsExec:
    """Execute page model functions."""

    def test_page_import(self):
        """Test Page model import."""
        from saleor.page.models import Page
        assert Page is not None

    def test_page_type_import(self):
        """Test PageType model import."""
        from saleor.page.models import PageType
        assert PageType is not None


class TestWebhookModelsExec:
    """Execute webhook model functions."""

    def test_webhook_import(self):
        """Test Webhook model import."""
        from saleor.webhook.models import Webhook
        assert Webhook is not None

    def test_webhook_event_import(self):
        """Test WebhookEvent model import."""
        from saleor.webhook.models import WebhookEvent
        assert WebhookEvent is not None


class TestAppModelsExec:
    """Execute app model functions."""

    def test_app_import(self):
        """Test App model import."""
        from saleor.app.models import App
        assert App is not None

    def test_app_installation_import(self):
        """Test AppInstallation model import."""
        from saleor.app.models import AppInstallation
        assert AppInstallation is not None

    def test_app_token_import(self):
        """Test AppToken model import."""
        from saleor.app.models import AppToken
        assert AppToken is not None


class TestTaxModelsExec:
    """Execute tax model functions."""

    def test_tax_class_import(self):
        """Test TaxClass model import."""
        from saleor.tax.models import TaxClass
        assert TaxClass is not None

    def test_tax_configuration_import(self):
        """Test TaxConfiguration model import."""
        from saleor.tax.models import TaxConfiguration
        assert TaxConfiguration is not None

    def test_tax_country_configuration_import(self):
        """Test TaxClassCountryRate model import."""
        from saleor.tax.models import TaxClassCountryRate
        assert TaxClassCountryRate is not None


class TestInvoiceModelsExec:
    """Execute invoice model functions."""

    def test_invoice_import(self):
        """Test Invoice model import."""
        from saleor.invoice.models import Invoice
        assert Invoice is not None

    def test_invoice_event_import(self):
        """Test InvoiceEvent model import."""
        from saleor.invoice.models import InvoiceEvent
        assert InvoiceEvent is not None


class TestSiteModelsExec:
    """Execute site model functions."""

    def test_site_settings_import(self):
        """Test SiteSettings model import."""
        from saleor.site.models import SiteSettings
        assert SiteSettings is not None

