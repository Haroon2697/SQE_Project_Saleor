"""
Extensive White-Box Tests for saleor/checkout/utils.py

Target: Increase checkout module coverage from 31.5% to 70%+
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from uuid import uuid4

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.utils import (
    invalidate_checkout,
    recalculate_checkout_discounts,
    invalidate_checkout_prices,
    checkout_lines_bulk_update,
    checkout_lines_bulk_delete,
    delete_checkouts,
    get_user_checkout,
    check_variant_in_stock,
    add_variant_to_checkout,
    calculate_checkout_quantity,
    change_billing_address_in_checkout,
    change_shipping_address_in_checkout,
    get_voucher_discount_for_checkout,
    get_voucher_for_checkout,
    check_voucher_for_checkout,
    recalculate_checkout_discount,
    add_promo_code_to_checkout,
    add_voucher_code_to_checkout,
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType, Category
from saleor.account.models import User, Address
from saleor.discount.models import Voucher, VoucherType, DiscountValueType
from saleor.warehouse.models import Stock, Warehouse


@pytest.mark.django_db
class TestInvalidateCheckout:
    """Test invalidate_checkout()"""

    def test_invalidate_checkout_sets_should_refresh_prices(self):
        """Statement: Set should_refresh_prices to True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            should_refresh_prices=False
        )
        
        invalidate_checkout(checkout)
        
        checkout.refresh_from_db()
        assert checkout.should_refresh_prices is True


@pytest.mark.django_db
class TestInvalidateCheckoutPrices:
    """Test invalidate_checkout_prices()"""

    def test_invalidate_checkout_prices_sets_flag(self):
        """Statement: Set should_refresh_prices flag"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            should_refresh_prices=False
        )
        
        invalidate_checkout_prices(checkout, save=True)
        
        checkout.refresh_from_db()
        assert checkout.should_refresh_prices is True


@pytest.mark.django_db
class TestCheckoutLinesBulkUpdate:
    """Test checkout_lines_bulk_update()"""

    def test_checkout_lines_bulk_update_updates_lines(self):
        """Statement: Update multiple checkout lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        line1.quantity = 3
        line2.quantity = 4
        
        checkout_lines_bulk_update([line1, line2], ["quantity"])
        
        line1.refresh_from_db()
        line2.refresh_from_db()
        assert line1.quantity == 3
        assert line2.quantity == 4


@pytest.mark.django_db
class TestCheckoutLinesBulkDelete:
    """Test checkout_lines_bulk_delete()"""

    def test_checkout_lines_bulk_delete_deletes_lines(self):
        """Statement: Delete checkout lines with specified PKs"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        checkout_lines_bulk_delete([line1.id])
        
        assert not CheckoutLine.objects.filter(id=line1.id).exists()
        assert CheckoutLine.objects.filter(id=line2.id).exists()


@pytest.mark.django_db
class TestDeleteCheckouts:
    """Test delete_checkouts()"""

    def test_delete_checkouts_deletes_specified_checkouts(self):
        """Statement: Delete checkouts with specified PKs"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout1 = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout2 = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        deleted_count = delete_checkouts([checkout1.id])
        
        assert deleted_count == 1
        assert not Checkout.objects.filter(id=checkout1.id).exists()
        assert Checkout.objects.filter(id=checkout2.id).exists()


@pytest.mark.django_db
class TestGetUserCheckout:
    """Test get_user_checkout()"""

    def test_get_user_checkout_returns_user_checkout(self):
        """Statement: Return checkout for user"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        user = User.objects.create_user(email="test@example.com", password="password")
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            user=user
        )
        
        result = get_user_checkout(user, channel.slug)
        
        assert result == checkout

    def test_get_user_checkout_returns_none_when_no_checkout(self):
        """Statement: Return None when user has no checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        user = User.objects.create_user(email="test@example.com", password="password")
        
        result = get_user_checkout(user, channel.slug)
        
        assert result is None


@pytest.mark.django_db
class TestCheckVariantInStock:
    """Test check_variant_in_stock()"""

    def test_check_variant_in_stock_returns_true_when_available(self):
        """Statement: Return True when variant is in stock"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        warehouse.channels.add(channel)
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        result = check_variant_in_stock(variant, channel.slug, "US", quantity=5)
        
        assert result is True

    def test_check_variant_in_stock_returns_false_when_not_enough(self):
        """Statement: Return False when not enough stock"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        warehouse.channels.add(channel)
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=5
        )
        
        result = check_variant_in_stock(variant, channel.slug, "US", quantity=10)
        
        assert result is False


@pytest.mark.django_db
class TestAddVariantToCheckout:
    """Test add_variant_to_checkout()"""

    def test_add_variant_to_checkout_creates_new_line(self):
        """Statement: Create new checkout line when variant not in checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        
        line = add_variant_to_checkout(checkout, variant, 2, channel.slug, "US")
        
        assert line is not None
        assert line.quantity == 2
        assert line.variant == variant

    def test_add_variant_to_checkout_increases_existing_line(self):
        """Statement: Increase quantity when variant already in checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        existing_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        line = add_variant_to_checkout(checkout, variant, 3, channel.slug, "US", replace=False)
        
        assert line.id == existing_line.id
        assert line.quantity == 5  # 2 + 3


@pytest.mark.django_db
class TestCalculateCheckoutQuantity:
    """Test calculate_checkout_quantity()"""

    def test_calculate_checkout_quantity_sums_line_quantities(self):
        """Statement: Sum quantities of all lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3
        )
        line_info1 = Mock()
        line_info1.line = Mock()
        line_info1.line.quantity = 2
        line_info2 = Mock()
        line_info2.line = Mock()
        line_info2.line.quantity = 3
        
        result = calculate_checkout_quantity([line_info1, line_info2])
        
        assert result == 5  # 2 + 3


@pytest.mark.django_db
class TestChangeBillingAddressInCheckout:
    """Test change_billing_address_in_checkout()"""

    def test_change_billing_address_sets_billing_address(self):
        """Statement: Set billing address on checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        address = Address.objects.create(
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="New York",
            country="US"
        )
        
        change_billing_address_in_checkout(checkout, address, save=True)
        
        checkout.refresh_from_db()
        assert checkout.billing_address == address


@pytest.mark.django_db
class TestChangeShippingAddressInCheckout:
    """Test change_shipping_address_in_checkout()"""

    def test_change_shipping_address_sets_shipping_address(self):
        """Statement: Set shipping address on checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        address = Address.objects.create(
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="New York",
            country="US"
        )
        
        change_shipping_address_in_checkout(checkout, address, save=True)
        
        checkout.refresh_from_db()
        assert checkout.shipping_address == address


@pytest.mark.django_db
class TestGetVoucherForCheckout:
    """Test get_voucher_for_checkout()"""

    def test_get_voucher_for_checkout_returns_voucher_when_code_exists(self):
        """Statement: Return voucher when code exists"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        voucher = Voucher.objects.create(
            code="TEST_VOUCHER",
            type=VoucherType.ENTIRE_ORDER,
            discount_value_type=DiscountValueType.FIXED,
            discount_value=Decimal("10.00")
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="TEST_VOUCHER"
        )
        
        result = get_voucher_for_checkout(checkout)
        
        assert result == voucher

    def test_get_voucher_for_checkout_returns_none_when_no_code(self):
        """Statement: Return None when no voucher code"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        result = get_voucher_for_checkout(checkout)
        
        assert result is None

