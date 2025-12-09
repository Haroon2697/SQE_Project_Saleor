"""
Tests for saleor/core/utils/validators.py
These tests actually execute the real code to increase coverage.
"""
import pytest
import datetime

from saleor.core.utils.validators import is_date_in_future


class TestIsDateInFuture:
    """Test is_date_in_future() function - actual execution, no mocking."""

    def test_future_date_returns_true(self):
        future_date = datetime.date.today() + datetime.timedelta(days=30)
        assert is_date_in_future(future_date) is True

    def test_past_date_returns_false(self):
        past_date = datetime.date.today() - datetime.timedelta(days=30)
        assert is_date_in_future(past_date) is False

    def test_today_returns_false(self):
        today = datetime.date.today()
        assert is_date_in_future(today) is False

    def test_yesterday_returns_false(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        assert is_date_in_future(yesterday) is False

    def test_tomorrow_returns_true(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        assert is_date_in_future(tomorrow) is True

    def test_far_future_date_returns_true(self):
        far_future = datetime.date.today() + datetime.timedelta(days=3650)
        assert is_date_in_future(far_future) is True

