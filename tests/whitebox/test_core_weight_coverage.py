"""
Tests for saleor/core/weight.py
These tests actually execute the real code to increase coverage.
"""
import pytest
from measurement.measures import Weight

from saleor.core.weight import zero_weight, convert_weight


class TestZeroWeight:
    """Test zero_weight() function - actual execution, no mocking."""

    def test_zero_weight_returns_weight(self):
        result = zero_weight()
        assert isinstance(result, Weight)
        assert result.kg == 0

    def test_zero_weight_is_zero_in_all_units(self):
        result = zero_weight()
        assert result.kg == 0
        assert result.lb == 0
        assert result.g == 0
        assert result.oz == 0


class TestConvertWeight:
    """Test convert_weight() function - actual execution, no mocking."""

    def test_convert_kg_to_lb(self):
        weight = Weight(kg=1)
        result = convert_weight(weight, "lb")
        # 1 kg ≈ 2.205 lb
        assert abs(result.lb - 2.205) < 0.01

    def test_convert_lb_to_kg(self):
        weight = Weight(lb=2.205)
        result = convert_weight(weight, "kg")
        # 2.205 lb ≈ 1 kg
        assert abs(result.kg - 1.0) < 0.01

    def test_convert_kg_to_g(self):
        weight = Weight(kg=1)
        result = convert_weight(weight, "g")
        assert result.g == 1000

    def test_convert_g_to_kg(self):
        weight = Weight(g=1000)
        result = convert_weight(weight, "kg")
        assert result.kg == 1

    def test_convert_rounds_to_three_decimals(self):
        weight = Weight(kg=1.23456789)
        result = convert_weight(weight, "kg")
        # Value should be rounded to 3 decimal places
        assert result.value == round(1.23456789, 3)

    def test_convert_oz_to_lb(self):
        weight = Weight(oz=16)
        result = convert_weight(weight, "lb")
        assert result.lb == 1.0

