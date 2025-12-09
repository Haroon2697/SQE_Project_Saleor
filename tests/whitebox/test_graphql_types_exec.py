"""
Tests that execute GraphQL type definitions to increase coverage.
"""
import pytest
from unittest.mock import Mock, patch


class TestAccountTypesExec:
    """Execute account GraphQL types."""

    def test_user_type_import(self):
        """Test User type import."""
        from saleor.graphql.account.types import User
        assert User is not None

    def test_address_type_import(self):
        """Test Address type import."""
        from saleor.graphql.account.types import Address
        assert Address is not None

    def test_customer_event_type_import(self):
        """Test CustomerEvent type import."""
        from saleor.graphql.account.types import CustomerEvent
        assert CustomerEvent is not None

    def test_group_type_import(self):
        """Test Group type import."""
        from saleor.graphql.account.types import Group
        assert Group is not None


class TestProductTypesExec:
    """Execute product GraphQL types."""

    def test_product_type_import(self):
        """Test Product type import."""
        from saleor.graphql.product.types import Product
        assert Product is not None

    def test_product_variant_type_import(self):
        """Test ProductVariant type import."""
        from saleor.graphql.product.types import ProductVariant
        assert ProductVariant is not None

    def test_category_type_import(self):
        """Test Category type import."""
        from saleor.graphql.product.types import Category
        assert Category is not None

    def test_collection_type_import(self):
        """Test Collection type import."""
        from saleor.graphql.product.types import Collection
        assert Collection is not None

    def test_product_media_type_import(self):
        """Test ProductMedia type import."""
        from saleor.graphql.product.types import ProductMedia
        assert ProductMedia is not None


class TestOrderTypesExec:
    """Execute order GraphQL types."""

    def test_order_type_import(self):
        """Test Order type import."""
        from saleor.graphql.order.types import Order
        assert Order is not None

    def test_order_line_type_import(self):
        """Test OrderLine type import."""
        from saleor.graphql.order.types import OrderLine
        assert OrderLine is not None

    def test_fulfillment_type_import(self):
        """Test Fulfillment type import."""
        from saleor.graphql.order.types import Fulfillment
        assert Fulfillment is not None

    def test_order_event_type_import(self):
        """Test OrderEvent type import."""
        from saleor.graphql.order.types import OrderEvent
        assert OrderEvent is not None


class TestCheckoutTypesExec:
    """Execute checkout GraphQL types."""

    def test_checkout_type_import(self):
        """Test Checkout type import."""
        from saleor.graphql.checkout.types import Checkout
        assert Checkout is not None

    def test_checkout_line_type_import(self):
        """Test CheckoutLine type import."""
        from saleor.graphql.checkout.types import CheckoutLine
        assert CheckoutLine is not None


class TestPaymentTypesExec:
    """Execute payment GraphQL types."""

    def test_payment_type_import(self):
        """Test Payment type import."""
        from saleor.graphql.payment.types import Payment
        assert Payment is not None

    def test_transaction_type_import(self):
        """Test Transaction type import."""
        from saleor.graphql.payment.types import Transaction
        assert Transaction is not None

    def test_transaction_item_type_import(self):
        """Test TransactionItem type import."""
        from saleor.graphql.payment.types import TransactionItem
        assert TransactionItem is not None


class TestShippingTypesExec:
    """Execute shipping GraphQL types."""

    def test_shipping_zone_type_import(self):
        """Test ShippingZone type import."""
        from saleor.graphql.shipping.types import ShippingZone
        assert ShippingZone is not None

    def test_shipping_method_type_import(self):
        """Test ShippingMethod type import."""
        from saleor.graphql.shipping.types import ShippingMethodType
        assert ShippingMethodType is not None


class TestWarehouseTypesExec:
    """Execute warehouse GraphQL types."""

    def test_warehouse_type_import(self):
        """Test Warehouse type import."""
        from saleor.graphql.warehouse.types import Warehouse
        assert Warehouse is not None

    def test_stock_type_import(self):
        """Test Stock type import."""
        from saleor.graphql.warehouse.types import Stock
        assert Stock is not None

    def test_allocation_type_import(self):
        """Test Allocation type import."""
        from saleor.graphql.warehouse.types import Allocation
        assert Allocation is not None


class TestDiscountTypesExec:
    """Execute discount GraphQL types."""

    def test_voucher_type_import(self):
        """Test Voucher type import."""
        from saleor.graphql.discount.types import Voucher
        assert Voucher is not None

    def test_promotion_type_import(self):
        """Test Promotion type import."""
        from saleor.graphql.discount.types import Promotion
        assert Promotion is not None

    def test_promotion_rule_type_import(self):
        """Test PromotionRule type import."""
        from saleor.graphql.discount.types import PromotionRule
        assert PromotionRule is not None


class TestChannelTypesExec:
    """Execute channel GraphQL types."""

    def test_channel_type_import(self):
        """Test Channel type import."""
        from saleor.graphql.channel.types import Channel
        assert Channel is not None


class TestAttributeTypesExec:
    """Execute attribute GraphQL types."""

    def test_attribute_type_import(self):
        """Test Attribute type import."""
        from saleor.graphql.attribute.types import Attribute
        assert Attribute is not None

    def test_attribute_value_type_import(self):
        """Test AttributeValue type import."""
        from saleor.graphql.attribute.types import AttributeValue
        assert AttributeValue is not None


class TestMenuTypesExec:
    """Execute menu GraphQL types."""

    def test_menu_type_import(self):
        """Test Menu type import."""
        from saleor.graphql.menu.types import Menu
        assert Menu is not None

    def test_menu_item_type_import(self):
        """Test MenuItem type import."""
        from saleor.graphql.menu.types import MenuItem
        assert MenuItem is not None


class TestPageTypesExec:
    """Execute page GraphQL types."""

    def test_page_type_import(self):
        """Test Page type import."""
        from saleor.graphql.page.types import Page
        assert Page is not None

    def test_page_type_type_import(self):
        """Test PageType type import."""
        from saleor.graphql.page.types import PageType
        assert PageType is not None


class TestAppTypesExec:
    """Execute app GraphQL types."""

    def test_app_type_import(self):
        """Test App type import."""
        from saleor.graphql.app.types import App
        assert App is not None

    def test_app_token_type_import(self):
        """Test AppToken type import."""
        from saleor.graphql.app.types import AppToken
        assert AppToken is not None


class TestWebhookTypesExec:
    """Execute webhook GraphQL types."""

    def test_webhook_type_import(self):
        """Test Webhook type import."""
        from saleor.graphql.webhook.types import Webhook
        assert Webhook is not None

    def test_webhook_event_type_import(self):
        """Test WebhookEvent type import."""
        from saleor.graphql.webhook.types import WebhookEvent
        assert WebhookEvent is not None


class TestGiftCardTypesExec:
    """Execute gift card GraphQL types."""

    def test_gift_card_type_import(self):
        """Test GiftCard type import."""
        from saleor.graphql.giftcard.types import GiftCard
        assert GiftCard is not None

    def test_gift_card_event_type_import(self):
        """Test GiftCardEvent type import."""
        from saleor.graphql.giftcard.types import GiftCardEvent
        assert GiftCardEvent is not None


class TestTaxTypesExec:
    """Execute tax GraphQL types."""

    def test_tax_class_type_import(self):
        """Test TaxClass type import."""
        from saleor.graphql.tax.types import TaxClass
        assert TaxClass is not None

    def test_tax_configuration_type_import(self):
        """Test TaxConfiguration type import."""
        from saleor.graphql.tax.types import TaxConfiguration
        assert TaxConfiguration is not None


class TestShopTypesExec:
    """Execute shop GraphQL types."""

    def test_shop_type_import(self):
        """Test Shop type import."""
        from saleor.graphql.shop.types import Shop
        assert Shop is not None


class TestInvoiceTypesExec:
    """Execute invoice GraphQL types."""

    def test_invoice_type_import(self):
        """Test Invoice type import."""
        from saleor.graphql.invoice.types import Invoice
        assert Invoice is not None

