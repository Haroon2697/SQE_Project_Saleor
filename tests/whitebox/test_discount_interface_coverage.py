"""
Tests for saleor/discount/interface.py
These tests actually execute the real code to increase coverage.
"""
import pytest
from decimal import Decimal

from saleor.discount.interface import DiscountInfo, VoucherInfo
from saleor.discount import DiscountType, DiscountValueType


class TestDiscountInfo:
    """Test DiscountInfo dataclass - actual execution, no mocking."""

    def test_create_basic_discount_info(self):
        """Test creating a basic discount info."""
        discount = DiscountInfo(currency="USD")
        assert discount.currency == "USD"
        assert discount.type == DiscountType.MANUAL
        assert discount.value_type == DiscountValueType.FIXED
        assert discount.value == Decimal("0.0")
        assert discount.amount_value == Decimal("0.0")

    def test_create_discount_info_with_all_fields(self):
        """Test creating a discount info with all fields."""
        discount = DiscountInfo(
            currency="EUR",
            type=DiscountType.VOUCHER,
            value_type=DiscountValueType.PERCENTAGE,
            value=Decimal("20.00"),
            amount_value=Decimal("15.00"),
            name="Summer Sale",
            translated_name="Solde d'été",
            reason="Promotional discount",
            voucher_code="SUMMER20",
        )
        assert discount.currency == "EUR"
        assert discount.type == DiscountType.VOUCHER
        assert discount.value_type == DiscountValueType.PERCENTAGE
        assert discount.value == Decimal("20.00")
        assert discount.amount_value == Decimal("15.00")
        assert discount.name == "Summer Sale"
        assert discount.translated_name == "Solde d'été"
        assert discount.reason == "Promotional discount"
        assert discount.voucher_code == "SUMMER20"

    def test_default_values(self):
        """Test default values of discount info."""
        discount = DiscountInfo(currency="USD")
        assert discount.name is None
        assert discount.translated_name is None
        assert discount.reason is None
        assert discount.promotion_rule is None
        assert discount.voucher is None
        assert discount.voucher_code is None

    def test_fixed_value_discount(self):
        """Test creating a fixed value discount."""
        discount = DiscountInfo(
            currency="USD",
            type=DiscountType.MANUAL,
            value_type=DiscountValueType.FIXED,
            value=Decimal("10.00"),
            amount_value=Decimal("10.00"),
        )
        assert discount.value_type == DiscountValueType.FIXED
        assert discount.value == Decimal("10.00")

    def test_percentage_discount(self):
        """Test creating a percentage discount."""
        discount = DiscountInfo(
            currency="USD",
            type=DiscountType.VOUCHER,
            value_type=DiscountValueType.PERCENTAGE,
            value=Decimal("25.00"),
        )
        assert discount.value_type == DiscountValueType.PERCENTAGE
        assert discount.value == Decimal("25.00")


class TestVoucherInfo:
    """Test VoucherInfo dataclass - actual execution, no mocking."""

    def test_create_empty_voucher_info(self):
        """Test creating a voucher info with empty lists."""
        from unittest.mock import Mock
        mock_voucher = Mock()
        
        info = VoucherInfo(
            voucher=mock_voucher,
            voucher_code="TEST123",
            product_pks=[],
            variant_pks=[],
            collection_pks=[],
            category_pks=[],
        )
        assert info.voucher == mock_voucher
        assert info.voucher_code == "TEST123"
        assert info.product_pks == []
        assert info.variant_pks == []
        assert info.collection_pks == []
        assert info.category_pks == []

    def test_create_voucher_info_with_pks(self):
        """Test creating a voucher info with PKs."""
        from unittest.mock import Mock
        mock_voucher = Mock()
        
        info = VoucherInfo(
            voucher=mock_voucher,
            voucher_code="DISCOUNT50",
            product_pks=[1, 2, 3],
            variant_pks=[10, 20],
            collection_pks=[100],
            category_pks=[1000, 2000],
        )
        assert info.product_pks == [1, 2, 3]
        assert info.variant_pks == [10, 20]
        assert info.collection_pks == [100]
        assert info.category_pks == [1000, 2000]

    def test_voucher_info_with_none_code(self):
        """Test creating a voucher info with None voucher code."""
        from unittest.mock import Mock
        mock_voucher = Mock()
        
        info = VoucherInfo(
            voucher=mock_voucher,
            voucher_code=None,
            product_pks=[],
            variant_pks=[],
            collection_pks=[],
            category_pks=[],
        )
        assert info.voucher_code is None

