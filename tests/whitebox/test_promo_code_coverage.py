"""
Tests for saleor/core/utils/promo_code.py
These tests actually execute the real code to increase coverage.
"""
import pytest
import re

from saleor.core.utils.promo_code import (
    InvalidPromoCode,
    generate_random_code,
)


class TestGenerateRandomCode:
    """Test generate_random_code() function - actual execution, no mocking."""

    def test_generate_random_code_format(self):
        """Test that generated code matches XXXX-XXXX-XXXX format."""
        code = generate_random_code()
        # Format: XXXX-XXXX-XXXX (hex characters, uppercase)
        pattern = r'^[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$'
        assert re.match(pattern, code)

    def test_generate_random_code_length(self):
        """Test that generated code has correct length."""
        code = generate_random_code()
        # 4 + 1 + 4 + 1 + 4 = 14 characters
        assert len(code) == 14

    def test_generate_random_code_is_uppercase(self):
        """Test that generated code is uppercase."""
        code = generate_random_code()
        assert code == code.upper()

    def test_generate_random_code_uniqueness(self):
        """Test that multiple generated codes are different."""
        codes = [generate_random_code() for _ in range(100)]
        unique_codes = set(codes)
        # All 100 codes should be unique
        assert len(unique_codes) == 100

    def test_generate_random_code_contains_dashes(self):
        """Test that code contains exactly 2 dashes."""
        code = generate_random_code()
        assert code.count('-') == 2


class TestInvalidPromoCode:
    """Test InvalidPromoCode exception class."""

    def test_invalid_promo_code_raises(self):
        with pytest.raises(InvalidPromoCode):
            raise InvalidPromoCode()

    def test_invalid_promo_code_default_message(self):
        try:
            raise InvalidPromoCode()
        except InvalidPromoCode as e:
            # InvalidPromoCode inherits from ValidationError
            assert hasattr(e, 'message_dict') or hasattr(e, 'messages')

    def test_invalid_promo_code_custom_message(self):
        custom_msg = "Custom error message"
        try:
            raise InvalidPromoCode(message=custom_msg)
        except InvalidPromoCode as e:
            # The message is wrapped in a list by ValidationError
            assert custom_msg in str(e)

