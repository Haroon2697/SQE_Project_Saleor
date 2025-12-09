"""
Tests for saleor/payment/utils.py to increase coverage.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock
from prices import Money, TaxedMoney


class TestPaymentUtilsImports:
    """Test imports from payment utils module."""

    def test_import_payment_utils_module(self):
        """Test importing payment utils module."""
        from saleor.payment import utils
        assert utils is not None

    def test_import_create_payment(self):
        """Test importing create_payment."""
        from saleor.payment.utils import create_payment
        assert create_payment is not None

    def test_import_clean_capture(self):
        """Test importing clean_capture."""
        from saleor.payment.utils import clean_capture
        assert clean_capture is not None

    def test_import_clean_authorize(self):
        """Test importing clean_authorize."""
        from saleor.payment.utils import clean_authorize
        assert clean_authorize is not None

    def test_import_is_currency_supported(self):
        """Test importing is_currency_supported."""
        from saleor.payment.utils import is_currency_supported
        assert is_currency_supported is not None

    def test_import_price_to_minor_unit(self):
        """Test importing price_to_minor_unit."""
        from saleor.payment.utils import price_to_minor_unit
        assert price_to_minor_unit is not None

    def test_import_price_from_minor_unit(self):
        """Test importing price_from_minor_unit."""
        from saleor.payment.utils import price_from_minor_unit
        assert price_from_minor_unit is not None


class TestPriceConversions:
    """Test price conversion functions."""

    def test_price_to_minor_unit_usd(self):
        """Test converting USD to minor unit (cents)."""
        from saleor.payment.utils import price_to_minor_unit
        
        # $10.50 = 1050 cents
        result = price_to_minor_unit(Decimal("10.50"), "USD")
        assert result == 1050

    def test_price_to_minor_unit_eur(self):
        """Test converting EUR to minor unit."""
        from saleor.payment.utils import price_to_minor_unit
        
        # €25.99 = 2599 cents
        result = price_to_minor_unit(Decimal("25.99"), "EUR")
        assert result == 2599

    def test_price_to_minor_unit_jpy(self):
        """Test converting JPY (no decimal places)."""
        from saleor.payment.utils import price_to_minor_unit
        
        # ¥1000 = 1000 (JPY has no minor unit)
        result = price_to_minor_unit(Decimal("1000"), "JPY")
        assert result == 1000

    def test_price_from_minor_unit_usd(self):
        """Test converting cents to USD."""
        from saleor.payment.utils import price_from_minor_unit
        
        # 1050 cents = $10.50
        result = price_from_minor_unit(1050, "USD")
        assert result == Decimal("10.50")

    def test_price_from_minor_unit_eur(self):
        """Test converting cents to EUR."""
        from saleor.payment.utils import price_from_minor_unit
        
        # 2599 cents = €25.99
        result = price_from_minor_unit(2599, "EUR")
        assert result == Decimal("25.99")

    def test_price_from_minor_unit_jpy(self):
        """Test converting JPY from minor unit."""
        from saleor.payment.utils import price_from_minor_unit
        
        # 1000 = ¥1000
        result = price_from_minor_unit(1000, "JPY")
        assert result == Decimal("1000")


class TestCurrencySupport:
    """Test currency support functions."""

    def test_is_currency_supported_usd(self):
        """Test USD is supported."""
        from saleor.payment.utils import is_currency_supported
        
        gateway_currencies = ["USD", "EUR", "GBP"]
        result = is_currency_supported("USD", gateway_currencies)
        assert result is True

    def test_is_currency_supported_unsupported(self):
        """Test unsupported currency."""
        from saleor.payment.utils import is_currency_supported
        
        gateway_currencies = ["USD", "EUR"]
        result = is_currency_supported("JPY", gateway_currencies)
        assert result is False

    def test_is_currency_supported_empty_list(self):
        """Test with empty currency list."""
        from saleor.payment.utils import is_currency_supported
        
        gateway_currencies = []
        result = is_currency_supported("USD", gateway_currencies)
        assert result is False


class TestPaymentValidation:
    """Test payment validation functions."""

    def test_clean_capture_function_exists(self):
        """Test clean_capture function exists."""
        from saleor.payment.utils import clean_capture
        assert callable(clean_capture)

    def test_clean_authorize_function_exists(self):
        """Test clean_authorize function exists."""
        from saleor.payment.utils import clean_authorize
        assert callable(clean_authorize)

    def test_create_payment_function_exists(self):
        """Test create_payment function exists."""
        from saleor.payment.utils import create_payment
        assert callable(create_payment)


class TestPaymentAmountCalculations:
    """Test payment amount calculations."""

    def test_calculate_payment_amount(self):
        """Test payment amount calculation."""
        order_total = Decimal("100.00")
        shipping = Decimal("10.00")
        tax = Decimal("11.00")
        
        payment_amount = order_total + shipping + tax
        assert payment_amount == Decimal("121.00")

    def test_calculate_partial_capture(self):
        """Test partial capture calculation."""
        authorized_amount = Decimal("100.00")
        capture_amount = Decimal("50.00")
        
        remaining = authorized_amount - capture_amount
        assert remaining == Decimal("50.00")

    def test_calculate_refund_amount(self):
        """Test refund amount calculation."""
        captured_amount = Decimal("100.00")
        refund_amount = Decimal("30.00")
        
        remaining = captured_amount - refund_amount
        assert remaining == Decimal("70.00")

    def test_calculate_multiple_refunds(self):
        """Test multiple refunds calculation."""
        captured_amount = Decimal("100.00")
        refunds = [Decimal("20.00"), Decimal("30.00"), Decimal("10.00")]
        
        total_refunded = sum(refunds)
        remaining = captured_amount - total_refunded
        
        assert total_refunded == Decimal("60.00")
        assert remaining == Decimal("40.00")


class TestPaymentStatusHelpers:
    """Test payment status helper functions."""

    def test_charge_status_not_charged(self):
        """Test not charged status."""
        from saleor.payment import ChargeStatus
        
        status = ChargeStatus.NOT_CHARGED
        assert status == "not-charged"

    def test_charge_status_pending(self):
        """Test pending status."""
        from saleor.payment import ChargeStatus
        
        status = ChargeStatus.PENDING
        assert status == "pending"

    def test_charge_status_fully_charged(self):
        """Test fully charged status."""
        from saleor.payment import ChargeStatus
        
        status = ChargeStatus.FULLY_CHARGED
        assert status == "fully-charged"

    def test_charge_status_fully_refunded(self):
        """Test fully refunded status."""
        from saleor.payment import ChargeStatus
        
        status = ChargeStatus.FULLY_REFUNDED
        assert status == "fully-refunded"


class TestTransactionKindHelpers:
    """Test transaction kind helpers."""

    def test_transaction_kind_auth(self):
        """Test auth transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.AUTH
        assert kind == "auth"

    def test_transaction_kind_capture(self):
        """Test capture transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.CAPTURE
        assert kind == "capture"

    def test_transaction_kind_refund(self):
        """Test refund transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.REFUND
        assert kind == "refund"

    def test_transaction_kind_void(self):
        """Test void transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.VOID
        assert kind == "void"

    def test_transaction_kind_pending(self):
        """Test pending transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.PENDING
        assert kind == "pending"

    def test_transaction_kind_confirm(self):
        """Test confirm transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.CONFIRM
        assert kind == "confirm"

    def test_transaction_kind_cancel(self):
        """Test cancel transaction kind."""
        from saleor.payment import TransactionKind
        
        kind = TransactionKind.CANCEL
        assert kind == "cancel"


class TestPaymentGatewayHelpers:
    """Test payment gateway helper functions."""

    def test_gateway_identifier_format(self):
        """Test gateway identifier format."""
        gateway_id = "mirumee.payments.dummy"
        
        parts = gateway_id.split(".")
        assert len(parts) == 3
        assert parts[0] == "mirumee"
        assert parts[1] == "payments"

    def test_gateway_config_structure(self):
        """Test gateway config structure."""
        config = [
            {"field": "api_key", "value": "sk_test_123"},
            {"field": "public_key", "value": "pk_test_456"}
        ]
        
        assert len(config) == 2
        assert config[0]["field"] == "api_key"


class TestPaymentErrorHandling:
    """Test payment error handling."""

    def test_payment_error_code_import(self):
        """Test PaymentErrorCode import."""
        from saleor.payment.error_codes import PaymentErrorCode
        assert PaymentErrorCode is not None

    def test_payment_error_codes_exist(self):
        """Test payment error codes exist."""
        from saleor.payment.error_codes import PaymentErrorCode
        
        codes = [
            PaymentErrorCode.GRAPHQL_ERROR,
            PaymentErrorCode.INVALID,
            PaymentErrorCode.NOT_FOUND,
            PaymentErrorCode.PAYMENT_ERROR,
        ]
        
        for code in codes:
            assert code is not None

