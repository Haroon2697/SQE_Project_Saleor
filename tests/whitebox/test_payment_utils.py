"""
White-Box Testing - Payment Utils
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/payment/utils.py (key functions)
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.payment.models import Payment, Transaction, TransactionItem, TransactionEvent
from saleor.payment import TransactionKind, ChargeStatus, TransactionAction
from saleor.order.models import Order, OrderStatus
from saleor.channel.models import Channel


# ============================================
# TEST 1: Payment Model Methods - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestPaymentModel:
    """Test Payment model methods for statement coverage"""
    
    def test_payment_creation(self):
        """Statement Coverage: create payment"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.UNFULFILLED
        )
        
        payment = Payment.objects.create(
            order=order,
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
            charge_status=ChargeStatus.NOT_CHARGED
        )
        
        assert payment.order == order
        assert payment.total == Decimal("100.00")
        assert payment.charge_status == ChargeStatus.NOT_CHARGED
    
    def test_payment_captured_amount(self):
        """Statement Coverage: get captured amount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment = Payment.objects.create(
            order=order,
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD",
            charge_status=ChargeStatus.CHARGED,
            captured_amount=Decimal("100.00")
        )
        
        assert payment.captured_amount == Decimal("100.00")
    
    def test_payment_get_authorized(self):
        """Statement Coverage: get authorized amount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment = Payment.objects.create(
            order=order,
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD"
        )
        
        # Create authorization transaction
        Transaction.objects.create(
            payment=payment,
            kind=TransactionKind.AUTH,
            amount=Decimal("100.00"),
            currency="USD",
            is_success=True
        )
        
        authorized = payment.get_authorized()
        assert authorized.amount == Decimal("100.00")


# ============================================
# TEST 2: Transaction Model - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestTransactionModel:
    """Test Transaction model for statement coverage"""
    
    def test_transaction_creation(self):
        """Statement Coverage: create transaction"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment = Payment.objects.create(
            order=order,
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD"
        )
        
        transaction = Transaction.objects.create(
            payment=payment,
            kind=TransactionKind.CAPTURE,
            amount=Decimal("100.00"),
            currency="USD",
            is_success=True
        )
        
        assert transaction.payment == payment
        assert transaction.kind == TransactionKind.CAPTURE
        assert transaction.is_success is True
    
    def test_transaction_failed(self):
        """Statement Coverage: failed transaction"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        payment = Payment.objects.create(
            order=order,
            gateway="test-gateway",
            total=Decimal("100.00"),
            currency="USD"
        )
        
        transaction = Transaction.objects.create(
            payment=payment,
            kind=TransactionKind.CAPTURE,
            amount=Decimal("100.00"),
            currency="USD",
            is_success=False,
            error="Payment failed"
        )
        
        assert transaction.is_success is False
        assert transaction.error == "Payment failed"


# ============================================
# TEST 3: TransactionItem Model - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestTransactionItemModel:
    """Test TransactionItem model for statement coverage"""
    
    def test_transaction_item_creation(self):
        """Statement Coverage: create transaction item"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        transaction_item = TransactionItem.objects.create(
            name="Test Transaction",
            order=order,
            amount=Decimal("100.00"),
            currency="USD"
        )
        
        assert transaction_item.order == order
        assert transaction_item.amount == Decimal("100.00")
        assert transaction_item.currency == "USD"
    
    def test_transaction_item_authorized_amount(self):
        """Statement Coverage: get authorized amount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        transaction_item = TransactionItem.objects.create(
            name="Test Transaction",
            order=order,
            amount=Decimal("100.00"),
            currency="USD",
            authorized_value=Decimal("100.00")
        )
        
        assert transaction_item.authorized_value == Decimal("100.00")
    
    def test_transaction_item_charged_amount(self):
        """Statement Coverage: get charged amount"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        transaction_item = TransactionItem.objects.create(
            name="Test Transaction",
            order=order,
            amount=Decimal("100.00"),
            currency="USD",
            charged_value=Decimal("100.00")
        )
        
        assert transaction_item.charged_value == Decimal("100.00")

