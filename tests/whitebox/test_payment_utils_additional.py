"""
Additional Comprehensive Tests for saleor/payment/utils.py

Target: Increase coverage for payment utility functions
Functions to Test:
- create_payment_lines_information
- create_checkout_payment_lines_information
- create_order_payment_lines_information
- generate_transactions_data
- create_payment_information
- create_payment
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money, TaxedMoney

from saleor.payment.utils import (
    create_payment_lines_information,
    create_checkout_payment_lines_information,
    create_order_payment_lines_information,
    generate_transactions_data,
    create_payment_information,
    create_payment,
)
from saleor.payment.models import Payment, TransactionItem
from saleor.checkout.models import Checkout, CheckoutLine
from saleor.order.models import Order, OrderLine
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant
from saleor.account.models import User


@pytest.mark.django_db
class TestCreatePaymentLinesInformation:
    """Test create_payment_lines_information()"""

    def test_create_payment_lines_information_empty_lines(self):
        """Statement: Test with empty lines list"""
        lines = []
        result = create_payment_lines_information(lines)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_create_payment_lines_information_with_lines(self):
        """Statement: Test with lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        # Create mock line objects
        line1 = Mock()
        line1.product_name = "Product 1"
        line1.variant_name = "Variant 1"
        line1.product_sku = "SKU1"
        line1.variant_id = 1
        line1.quantity = 2
        line1.unit_price = Money(Decimal("10.00"), "USD")
        line1.total_price = Money(Decimal("20.00"), "USD")
        
        lines = [line1]
        result = create_payment_lines_information(lines)
        assert isinstance(result, list)
        assert len(result) == 1


@pytest.mark.django_db
class TestCreateCheckoutPaymentLinesInformation:
    """Test create_checkout_payment_lines_information()"""

    def test_create_checkout_payment_lines_information(self):
        """Statement: Test with checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        result = create_checkout_payment_lines_information(checkout)
        assert isinstance(result, list)


@pytest.mark.django_db
class TestCreateOrderPaymentLinesInformation:
    """Test create_order_payment_lines_information()"""

    def test_create_order_payment_lines_information(self):
        """Statement: Test with order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            lines_count=0
        )
        
        result = create_order_payment_lines_information(order)
        assert isinstance(result, list)


@pytest.mark.django_db
class TestGenerateTransactionsData:
    """Test generate_transactions_data()"""

    def test_generate_transactions_data_empty(self):
        """Statement: Test with payment that has no transactions"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        payment = Payment.objects.create(
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
        )
        
        result = generate_transactions_data(payment)
        assert isinstance(result, list)

    def test_generate_transactions_data_with_transactions(self):
        """Statement: Test with payment that has transactions"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        payment = Payment.objects.create(
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
        )
        
        # Create transaction item
        transaction = TransactionItem.objects.create(
            payment=payment,
            name="Test Transaction",
            psp_reference="PSP123",
            amount_value=Decimal("100.00"),
            currency="USD",
        )
        
        result = generate_transactions_data(payment)
        assert isinstance(result, list)


@pytest.mark.django_db
class TestCreatePaymentInformation:
    """Test create_payment_information()"""

    def test_create_payment_information_with_payment(self):
        """Statement: Test with payment object"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        payment = Payment.objects.create(
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
        )
        
        result = create_payment_information(
            payment=payment,
            manager=Mock()
        )
        assert result is not None
        assert hasattr(result, 'gateway')

    def test_create_payment_information_with_checkout(self):
        """Statement: Test with checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment = Payment.objects.create(
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
        )
        
        result = create_payment_information(
            payment=payment,
            manager=Mock(),
            customer_ip_address="127.0.0.1",
            checkout=checkout
        )
        assert result is not None

    def test_create_payment_information_with_order(self):
        """Statement: Test with order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            lines_count=0
        )
        
        payment = Payment.objects.create(
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
        )
        
        result = create_payment_information(
            payment=payment,
            manager=Mock(),
            customer_ip_address="127.0.0.1",
            order=order
        )
        assert result is not None


@pytest.mark.django_db
class TestCreatePayment:
    """Test create_payment()"""

    def test_create_payment_basic(self):
        """Statement: Test basic payment creation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        payment_data = Mock()
        payment_data.gateway = "test-gateway"
        payment_data.amount = Decimal("100.00")
        payment_data.currency = "USD"
        payment_data.payment_method_info = Mock()
        payment_data.payment_method_info.type = "card"
        payment_data.payment_method_info.brand = "visa"
        payment_data.payment_method_info.last_4 = "1234"
        payment_data.payment_method_info.exp_month = 12
        payment_data.payment_method_info.exp_year = 2025
        
        result = create_payment(
            gateway=payment_data.gateway,
            total=payment_data.amount,
            currency=payment_data.currency,
            email="test@example.com",
            payment_method_info=payment_data.payment_method_info,
            customer_ip_address="127.0.0.1",
        )
        assert result is not None
        assert result.gateway == "test-gateway"
        assert result.total == Decimal("100.00")
        assert result.currency == "USD"

    def test_create_payment_with_checkout(self):
        """Statement: Test payment creation with checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment_data = Mock()
        payment_data.gateway = "test-gateway"
        payment_data.amount = Decimal("100.00")
        payment_data.currency = "USD"
        payment_data.payment_method_info = Mock()
        payment_data.payment_method_info.type = "card"
        
        result = create_payment(
            gateway=payment_data.gateway,
            total=payment_data.amount,
            currency=payment_data.currency,
            email="test@example.com",
            payment_method_info=payment_data.payment_method_info,
            checkout=checkout,
        )
        assert result is not None
        assert result.checkout == checkout

    def test_create_payment_with_order(self):
        """Statement: Test payment creation with order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            lines_count=0
        )
        
        payment_data = Mock()
        payment_data.gateway = "test-gateway"
        payment_data.amount = Decimal("100.00")
        payment_data.currency = "USD"
        payment_data.payment_method_info = Mock()
        payment_data.payment_method_info.type = "card"
        
        result = create_payment(
            gateway=payment_data.gateway,
            total=payment_data.amount,
            currency=payment_data.currency,
            email="test@example.com",
            payment_method_info=payment_data.payment_method_info,
            order=order,
        )
        assert result is not None
        assert result.order == order

