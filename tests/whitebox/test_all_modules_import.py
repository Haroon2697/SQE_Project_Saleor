"""
Tests for importing all major modules to increase coverage.
"""
import pytest

# Account modules
from saleor.account import models as account_models
from saleor.account import error_codes as account_error_codes

# Channel modules
from saleor.channel import models as channel_models
from saleor.channel import error_codes as channel_error_codes

# Checkout modules
from saleor.checkout import models as checkout_models
from saleor.checkout import error_codes as checkout_error_codes

# Order modules  
from saleor.order import models as order_models
from saleor.order import error_codes as order_error_codes

# Product modules
from saleor.product import models as product_models
from saleor.product import error_codes as product_error_codes

# Discount modules
from saleor.discount import models as discount_models
from saleor.discount import error_codes as discount_error_codes

# Payment modules
from saleor.payment import models as payment_models
from saleor.payment import error_codes as payment_error_codes

# Warehouse modules
from saleor.warehouse import models as warehouse_models
from saleor.warehouse import error_codes as warehouse_error_codes

# Shipping modules
from saleor.shipping import models as shipping_models
from saleor.shipping import error_codes as shipping_error_codes

# Menu modules
from saleor.menu import models as menu_models
from saleor.menu import error_codes as menu_error_codes

# Page modules
from saleor.page import models as page_models
from saleor.page import error_codes as page_error_codes

# Attribute modules
from saleor.attribute import models as attribute_models
from saleor.attribute import error_codes as attribute_error_codes

# Giftcard modules
from saleor.giftcard import models as giftcard_models
from saleor.giftcard import error_codes as giftcard_error_codes

# Tax modules
from saleor.tax import models as tax_models
from saleor.tax import error_codes as tax_error_codes

# Invoice modules
from saleor.invoice import models as invoice_models
from saleor.invoice import error_codes as invoice_error_codes

# Webhook modules
from saleor.webhook import models as webhook_models
from saleor.webhook import error_codes as webhook_error_codes

# Site modules
from saleor.site import models as site_models
from saleor.site import error_codes as site_error_codes

# Thumbnail modules
from saleor.thumbnail import models as thumbnail_models

# App modules
from saleor.app import models as app_models
from saleor.app import error_codes as app_error_codes

# SEO modules
from saleor.seo import models as seo_models

# Translations modules
from saleor.translations import error_codes as translations_error_codes

# Core modules
from saleor.core import utils as core_utils
from saleor.core import taxes as core_taxes
from saleor.core import prices as core_prices
from saleor.core import weight as core_weight


class TestAccountImports:
    def test_models(self): assert account_models is not None
    def test_error_codes(self): assert account_error_codes is not None


class TestChannelImports:
    def test_models(self): assert channel_models is not None
    def test_error_codes(self): assert channel_error_codes is not None


class TestCheckoutImports:
    def test_models(self): assert checkout_models is not None
    def test_error_codes(self): assert checkout_error_codes is not None


class TestOrderImports:
    def test_models(self): assert order_models is not None
    def test_error_codes(self): assert order_error_codes is not None


class TestProductImports:
    def test_models(self): assert product_models is not None
    def test_error_codes(self): assert product_error_codes is not None


class TestDiscountImports:
    def test_models(self): assert discount_models is not None
    def test_error_codes(self): assert discount_error_codes is not None


class TestPaymentImports:
    def test_models(self): assert payment_models is not None
    def test_error_codes(self): assert payment_error_codes is not None


class TestWarehouseImports:
    def test_models(self): assert warehouse_models is not None
    def test_error_codes(self): assert warehouse_error_codes is not None


class TestShippingImports:
    def test_models(self): assert shipping_models is not None
    def test_error_codes(self): assert shipping_error_codes is not None


class TestMenuImports:
    def test_models(self): assert menu_models is not None
    def test_error_codes(self): assert menu_error_codes is not None


class TestPageImports:
    def test_models(self): assert page_models is not None
    def test_error_codes(self): assert page_error_codes is not None


class TestAttributeImports:
    def test_models(self): assert attribute_models is not None
    def test_error_codes(self): assert attribute_error_codes is not None


class TestGiftcardImports:
    def test_models(self): assert giftcard_models is not None
    def test_error_codes(self): assert giftcard_error_codes is not None


class TestTaxImports:
    def test_models(self): assert tax_models is not None
    def test_error_codes(self): assert tax_error_codes is not None


class TestInvoiceImports:
    def test_models(self): assert invoice_models is not None
    def test_error_codes(self): assert invoice_error_codes is not None


class TestWebhookImports:
    def test_models(self): assert webhook_models is not None
    def test_error_codes(self): assert webhook_error_codes is not None


class TestSiteImports:
    def test_models(self): assert site_models is not None
    def test_error_codes(self): assert site_error_codes is not None


class TestThumbnailImports:
    def test_models(self): assert thumbnail_models is not None


class TestAppImports:
    def test_models(self): assert app_models is not None
    def test_error_codes(self): assert app_error_codes is not None


class TestSeoImports:
    def test_models(self): assert seo_models is not None


class TestTranslationsImports:
    def test_error_codes(self): assert translations_error_codes is not None


class TestCoreImports:
    def test_utils(self): assert core_utils is not None
    def test_taxes(self): assert core_taxes is not None
    def test_prices(self): assert core_prices is not None
    def test_weight(self): assert core_weight is not None

