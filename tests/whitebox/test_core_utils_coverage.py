"""
Tests for saleor/core/utils and related modules.
These tests actually execute the real code to increase coverage.
"""
import pytest
from decimal import Decimal
from prices import Money, TaxedMoney

from saleor.core.utils import (
    is_valid_ipv4,
    is_valid_ipv6,
    prepare_unique_slug,
)
from saleor.core.taxes import (
    zero_money,
    zero_taxed_money,
    TaxError,
    TaxDataError,
    TaxType,
    TaxLineData,
    TaxData,
)
from saleor.core.prices import quantize_price, MAXIMUM_PRICE


# =============================================================================
# Tests for saleor/core/utils/__init__.py
# =============================================================================

class TestIsValidIPv4:
    """Test is_valid_ipv4() function - actual execution, no mocking."""

    def test_valid_ipv4_address(self):
        assert is_valid_ipv4("192.168.1.1") is True
        assert is_valid_ipv4("127.0.0.1") is True
        assert is_valid_ipv4("0.0.0.0") is True
        assert is_valid_ipv4("255.255.255.255") is True
        assert is_valid_ipv4("10.0.0.1") is True

    def test_invalid_ipv4_address(self):
        assert is_valid_ipv4("256.256.256.256") is False
        assert is_valid_ipv4("invalid") is False
        assert is_valid_ipv4("") is False
        assert is_valid_ipv4("192.168.1") is False
        assert is_valid_ipv4("192.168.1.1.1") is False
        assert is_valid_ipv4("::1") is False  # IPv6 address


class TestIsValidIPv6:
    """Test is_valid_ipv6() function - actual execution, no mocking."""

    def test_valid_ipv6_address(self):
        assert is_valid_ipv6("::1") is True
        assert is_valid_ipv6("fe80::1") is True
        assert is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
        assert is_valid_ipv6("::") is True

    def test_invalid_ipv6_address(self):
        assert is_valid_ipv6("192.168.1.1") is False
        assert is_valid_ipv6("invalid") is False
        assert is_valid_ipv6("") is False
        assert is_valid_ipv6(":::1") is False


class TestPrepareUniqueSlug:
    """Test prepare_unique_slug() function - actual execution, no mocking."""

    def test_unique_slug_no_collision(self):
        result = prepare_unique_slug("test-slug", [])
        assert result == "test-slug"

    def test_unique_slug_with_collision(self):
        existing = ["test-slug"]
        result = prepare_unique_slug("test-slug", existing)
        assert result == "test-slug-2"

    def test_unique_slug_multiple_collisions(self):
        existing = ["test-slug", "test-slug-2", "test-slug-3"]
        result = prepare_unique_slug("test-slug", existing)
        assert result == "test-slug-4"

    def test_unique_slug_with_generator(self):
        existing = iter(["slug", "slug-2"])
        result = prepare_unique_slug("slug", existing)
        assert result == "slug-3"


# =============================================================================
# Tests for saleor/core/taxes.py
# =============================================================================

class TestZeroMoney:
    """Test zero_money() function - actual execution, no mocking."""

    def test_zero_money_usd(self):
        result = zero_money("USD")
        assert isinstance(result, Money)
        assert result.amount == 0
        assert result.currency == "USD"

    def test_zero_money_eur(self):
        result = zero_money("EUR")
        assert isinstance(result, Money)
        assert result.amount == 0
        assert result.currency == "EUR"

    def test_zero_money_gbp(self):
        result = zero_money("GBP")
        assert isinstance(result, Money)
        assert result.amount == 0
        assert result.currency == "GBP"


class TestZeroTaxedMoney:
    """Test zero_taxed_money() function - actual execution, no mocking."""

    def test_zero_taxed_money_usd(self):
        result = zero_taxed_money("USD")
        assert isinstance(result, TaxedMoney)
        assert result.net.amount == 0
        assert result.gross.amount == 0
        assert result.net.currency == "USD"
        assert result.gross.currency == "USD"

    def test_zero_taxed_money_eur(self):
        result = zero_taxed_money("EUR")
        assert isinstance(result, TaxedMoney)
        assert result.net.amount == 0
        assert result.gross.amount == 0
        assert result.currency == "EUR"


class TestTaxError:
    """Test TaxError exception class."""

    def test_tax_error_raises(self):
        with pytest.raises(TaxError):
            raise TaxError("Test error")

    def test_tax_error_message(self):
        try:
            raise TaxError("Custom tax error message")
        except TaxError as e:
            assert str(e) == "Custom tax error message"


class TestTaxDataError:
    """Test TaxDataError exception class."""

    def test_tax_data_error_raises(self):
        with pytest.raises(TaxDataError):
            raise TaxDataError("Test error")

    def test_tax_data_error_with_errors_list(self):
        errors = ["error1", "error2"]
        try:
            raise TaxDataError("Tax data error", errors=errors)
        except TaxDataError as e:
            assert str(e) == "Tax data error"
            assert e.errors == errors

    def test_tax_data_error_default_empty_errors(self):
        try:
            raise TaxDataError("Error without errors list")
        except TaxDataError as e:
            assert e.errors == []


class TestTaxType:
    """Test TaxType dataclass."""

    def test_tax_type_creation(self):
        tax_type = TaxType(code="VAT", description="Value Added Tax")
        assert tax_type.code == "VAT"
        assert tax_type.description == "Value Added Tax"

    def test_tax_type_frozen(self):
        tax_type = TaxType(code="VAT", description="VAT")
        with pytest.raises(Exception):  # FrozenInstanceError
            tax_type.code = "SALES"


class TestTaxLineData:
    """Test TaxLineData dataclass."""

    def test_tax_line_data_creation(self):
        line_data = TaxLineData(
            tax_rate=Decimal("0.20"),
            total_gross_amount=Decimal("120.00"),
            total_net_amount=Decimal("100.00"),
        )
        assert line_data.tax_rate == Decimal("0.20")
        assert line_data.total_gross_amount == Decimal("120.00")
        assert line_data.total_net_amount == Decimal("100.00")


class TestTaxData:
    """Test TaxData dataclass."""

    def test_tax_data_creation(self):
        line = TaxLineData(
            tax_rate=Decimal("0.20"),
            total_gross_amount=Decimal("120.00"),
            total_net_amount=Decimal("100.00"),
        )
        tax_data = TaxData(
            shipping_price_gross_amount=Decimal("12.00"),
            shipping_price_net_amount=Decimal("10.00"),
            shipping_tax_rate=Decimal("0.20"),
            lines=[line],
        )
        assert tax_data.shipping_price_gross_amount == Decimal("12.00")
        assert tax_data.shipping_price_net_amount == Decimal("10.00")
        assert tax_data.shipping_tax_rate == Decimal("0.20")
        assert len(tax_data.lines) == 1


# =============================================================================
# Tests for saleor/core/prices.py
# =============================================================================

class TestQuantizePrice:
    """Test quantize_price() function - actual execution, no mocking."""

    def test_quantize_decimal_usd(self):
        price = Decimal("10.12345")
        result = quantize_price(price, "USD")
        assert result == Decimal("10.12")

    def test_quantize_decimal_jpy(self):
        # JPY has 0 decimal places
        price = Decimal("100.75")
        result = quantize_price(price, "JPY")
        assert result == Decimal("101")

    def test_quantize_money_usd(self):
        price = Money(Decimal("10.12345"), "USD")
        result = quantize_price(price, "USD")
        assert result.amount == Decimal("10.12")

    def test_quantize_taxed_money(self):
        price = TaxedMoney(
            net=Money(Decimal("10.12345"), "USD"),
            gross=Money(Decimal("12.14876"), "USD"),
        )
        result = quantize_price(price, "USD")
        assert result.net.amount == Decimal("10.12")
        assert result.gross.amount == Decimal("12.15")


class TestMaximumPrice:
    """Test MAXIMUM_PRICE constant."""

    def test_maximum_price_is_positive(self):
        assert MAXIMUM_PRICE > 0

    def test_maximum_price_is_integer(self):
        assert isinstance(MAXIMUM_PRICE, int)

