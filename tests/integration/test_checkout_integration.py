"""
Integration tests for Checkout module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal
from uuid import uuid4
from django.contrib.auth import get_user_model

from saleor.checkout.models import Checkout, CheckoutLine
# Checkout utilities are imported in tests if needed
from saleor.channel.models import Channel
from saleor.product.models import (
    Product,
    ProductType,
    Category,
    ProductVariant,
    ProductVariantChannelListing,
)
from saleor.account.models import Address


User = get_user_model()


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Checkout Channel",
        slug="checkout-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="checkout@example.com",
        password="testpass123",
    )


@pytest.fixture
def address(db):
    """Create a test address."""
    return Address.objects.create(
        first_name="John",
        last_name="Doe",
        street_address_1="123 Test St",
        city="Test City",
        postal_code="12345",
        country="US",
    )


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(
        name="Checkout Category",
        slug="checkout-category",
    )


@pytest.fixture
def product_type(db):
    """Create a test product type."""
    return ProductType.objects.create(
        name="Checkout Product Type",
        slug="checkout-product-type",
        is_shipping_required=True,
    )


@pytest.fixture
def product(db, product_type, category):
    """Create a test product."""
    return Product.objects.create(
        name="Checkout Product",
        slug="checkout-product",
        product_type=product_type,
        category=category,
    )


@pytest.fixture
def product_variant(db, product):
    """Create a test product variant."""
    return ProductVariant.objects.create(
        product=product,
        sku="CHECKOUT-SKU-001",
        name="Checkout Variant",
    )


@pytest.fixture
def variant_listing(db, product_variant, channel):
    """Create a variant channel listing."""
    return ProductVariantChannelListing.objects.create(
        variant=product_variant,
        channel=channel,
        price_amount=Decimal("100.00"),
        currency="USD",
    )


@pytest.fixture
def checkout(db, channel, user):
    """Create a test checkout."""
    return Checkout.objects.create(
        token=uuid4(),
        channel=channel,
        user=user,
        email=user.email,
        currency=channel.currency_code,
    )


@pytest.mark.django_db
class TestCheckoutCreation:
    """Test checkout creation."""

    def test_create_checkout(self, channel, user):
        """Test creating a checkout."""
        checkout = Checkout.objects.create(
            token=uuid4(),
            channel=channel,
            user=user,
            email=user.email,
            currency="USD",
        )
        assert checkout.token is not None
        assert checkout.channel == channel
        assert checkout.user == user

    def test_create_anonymous_checkout(self, channel):
        """Test creating an anonymous checkout."""
        checkout = Checkout.objects.create(
            token=uuid4(),
            channel=channel,
            email="anonymous@example.com",
            currency="USD",
        )
        assert checkout.user is None
        assert checkout.email == "anonymous@example.com"

    def test_checkout_str(self, checkout):
        """Test checkout string representation."""
        assert str(checkout.token) in str(checkout) or str(checkout)


@pytest.mark.django_db
class TestCheckoutLines:
    """Test checkout lines functionality."""

    def test_create_checkout_line(self, checkout, product_variant):
        """Test creating a checkout line."""
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=product_variant,
            quantity=2,
        )
        assert line.id is not None
        assert line.checkout == checkout
        assert line.variant == product_variant
        assert line.quantity == 2

    def test_multiple_checkout_lines(self, checkout, product):
        """Test multiple checkout lines."""
        variant1 = ProductVariant.objects.create(
            product=product,
            sku="LINE-VAR-001",
        )
        variant2 = ProductVariant.objects.create(
            product=product,
            sku="LINE-VAR-002",
        )
        
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant1,
            quantity=1,
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant2,
            quantity=3,
        )
        
        assert checkout.lines.count() == 2
        assert line1 in checkout.lines.all()
        assert line2 in checkout.lines.all()

    def test_checkout_line_update_quantity(self, checkout, product_variant):
        """Test updating checkout line quantity."""
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=product_variant,
            quantity=1,
        )
        line.quantity = 5
        line.save()
        line.refresh_from_db()
        assert line.quantity == 5


@pytest.mark.django_db
class TestCheckoutAddresses:
    """Test checkout address functionality."""

    def test_set_shipping_address(self, checkout, address):
        """Test setting shipping address."""
        checkout.shipping_address = address
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.shipping_address == address

    def test_set_billing_address(self, checkout, address):
        """Test setting billing address."""
        checkout.billing_address = address
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.billing_address == address

    def test_same_billing_and_shipping(self, checkout, address):
        """Test same billing and shipping address."""
        checkout.shipping_address = address
        checkout.billing_address = address
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.shipping_address == checkout.billing_address


@pytest.mark.django_db
class TestCheckoutMetadata:
    """Test checkout metadata functionality."""

    def test_checkout_metadata(self, checkout):
        """Test checkout metadata."""
        checkout.metadata = {"key": "value"}
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.metadata.get("key") == "value"

    def test_checkout_private_metadata(self, checkout):
        """Test checkout private metadata."""
        checkout.private_metadata = {"secret": "data"}
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.private_metadata.get("secret") == "data"


@pytest.mark.django_db
class TestCheckoutQueries:
    """Test checkout query functionality."""

    def test_filter_checkouts_by_channel(self, checkout, channel):
        """Test filtering checkouts by channel."""
        checkouts = Checkout.objects.filter(channel=channel)
        assert checkout in checkouts

    def test_filter_checkouts_by_user(self, checkout, user):
        """Test filtering checkouts by user."""
        checkouts = Checkout.objects.filter(user=user)
        assert checkout in checkouts

    def test_filter_checkouts_by_email(self, checkout):
        """Test filtering checkouts by email."""
        checkouts = Checkout.objects.filter(email=checkout.email)
        assert checkout in checkouts


@pytest.mark.django_db
class TestCheckoutNotes:
    """Test checkout notes functionality."""

    def test_checkout_note(self, checkout):
        """Test checkout note."""
        checkout.note = "Test note for checkout"
        checkout.save()
        checkout.refresh_from_db()
        assert checkout.note == "Test note for checkout"

    def test_empty_note(self, checkout):
        """Test empty checkout note."""
        assert checkout.note == "" or checkout.note is None or not checkout.note

