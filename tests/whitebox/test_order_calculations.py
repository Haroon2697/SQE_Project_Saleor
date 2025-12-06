"""
White-Box Testing - Order Calculations
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/order/calculations.py (fetch_order_prices_if_expired)
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from django.utils import timezone

from saleor.order.models import Order, OrderLine, OrderStatus
from saleor.order import ORDER_EDITABLE_STATUS
from saleor.order.calculations import fetch_order_prices_if_expired
from saleor.tax import TaxCalculationStrategy
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category


# ============================================
# TEST 1: fetch_order_prices_if_expired - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestFetchOrderPricesIfExpiredStatementCoverage:
    """Test fetch_order_prices_if_expired() for statement coverage"""
    
    def test_order_status_not_editable(self):
        """Statement Coverage: order.status not in ORDER_EDITABLE_STATUS -> return early"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.FULFILLED  # Not editable
        )
        
        manager = Mock()
        result_order, result_lines = fetch_order_prices_if_expired(
            order, manager, lines=None, force_update=False
        )
        
        assert result_order == order
        assert result_lines is None
    
    def test_no_force_update_no_refresh_no_expired(self):
        """Statement Coverage: force_update=False, should_refresh=False, no expired -> return early"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,  # Editable
            should_refresh_prices=False
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            result_order, result_lines = fetch_order_prices_if_expired(
                order, manager, lines=None, force_update=False
            )
        
        assert result_order == order
    
    def test_tax_strategy_tax_app_no_sync_webhooks(self):
        """Statement Coverage: tax_strategy == TAX_APP and allow_sync_webhooks=False -> return early"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=True
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order', 
                      return_value=TaxCalculationStrategy.TAX_APP):
                result_order, result_lines = fetch_order_prices_if_expired(
                    order, manager, lines=None, force_update=False, allow_sync_webhooks=False
                )
        
        assert result_order == order
    
    def test_expired_line_ids_exists(self):
        """Statement Coverage: expired_line_ids exists -> refresh_order_base_prices_and_discounts"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        expired_ids = [1, 2]
        
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=expired_ids):
            with patch('saleor.order.calculations.refresh_order_base_prices_and_discounts') as mock_refresh:
                with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                          return_value=TaxCalculationStrategy.FLAT_RATES):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                fetch_order_prices_if_expired(
                                    order, manager, lines=None, force_update=False
                                )
                
                # Verify refresh_order_base_prices_and_discounts was called
                mock_refresh.assert_called_once()
    
    def test_no_expired_line_ids(self):
        """Statement Coverage: expired_line_ids is empty -> fetch_draft_order_lines_info"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=True
        )
        
        manager = Mock()
        
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.fetch_draft_order_lines_info') as mock_fetch:
                with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                          return_value=TaxCalculationStrategy.FLAT_RATES):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                fetch_order_prices_if_expired(
                                    order, manager, lines=None, force_update=False
                                )
                
                # Verify fetch_draft_order_lines_info was called
                mock_fetch.assert_called_once()


# ============================================
# TEST 2: fetch_order_prices_if_expired - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestFetchOrderPricesIfExpiredDecisionCoverage:
    """Test all decision branches in fetch_order_prices_if_expired()"""
    
    def test_decision_order_status_editable_true(self):
        """Decision: order.status in ORDER_EDITABLE_STATUS -> TRUE"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT  # Editable
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                      return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations.fetch_draft_order_lines_info'):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                result_order, _ = fetch_order_prices_if_expired(
                                    order, manager, force_update=True
                                )
                                # Should process, not return early
                                assert result_order.should_refresh_prices is False
    
    def test_decision_order_status_editable_false(self):
        """Decision: order.status not in ORDER_EDITABLE_STATUS -> FALSE (return early)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.CANCELED  # Not editable
        )
        
        manager = Mock()
        result_order, result_lines = fetch_order_prices_if_expired(
            order, manager, force_update=False
        )
        
        # Should return early without processing
        assert result_order == order
        assert result_lines is None
    
    def test_decision_force_update_true(self):
        """Decision: force_update = True -> TRUE (process)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                      return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations.fetch_draft_order_lines_info'):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                result_order, _ = fetch_order_prices_if_expired(
                                    order, manager, force_update=True
                                )
                                # Should process even if should_refresh_prices is False
                                assert result_order.should_refresh_prices is False
    
    def test_decision_force_update_false_should_refresh_true(self):
        """Decision: force_update = False, should_refresh = True -> TRUE (process)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=True
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                      return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations.fetch_draft_order_lines_info'):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                result_order, _ = fetch_order_prices_if_expired(
                                    order, manager, force_update=False
                                )
                                # Should process
                                assert result_order.should_refresh_prices is False
    
    def test_decision_expired_line_ids_exists_true(self):
        """Decision: expired_line_ids exists -> TRUE (refresh_order_base_prices_and_discounts)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        expired_ids = [1]
        
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=expired_ids):
            with patch('saleor.order.calculations.refresh_order_base_prices_and_discounts') as mock_refresh:
                with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                          return_value=TaxCalculationStrategy.FLAT_RATES):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                fetch_order_prices_if_expired(
                                    order, manager, force_update=False
                                )
                
                mock_refresh.assert_called_once()
    
    def test_decision_expired_line_ids_exists_false(self):
        """Decision: expired_line_ids is empty -> FALSE (fetch_draft_order_lines_info)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=True
        )
        
        manager = Mock()
        
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.fetch_draft_order_lines_info') as mock_fetch:
                with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                          return_value=TaxCalculationStrategy.FLAT_RATES):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                fetch_order_prices_if_expired(
                                    order, manager, force_update=False
                                )
                
                mock_fetch.assert_called_once()


# ============================================
# TEST 3: fetch_order_prices_if_expired - MC/DC Coverage
# ============================================
@pytest.mark.django_db
class TestFetchOrderPricesIfExpiredMCDC:
    """Modified Condition/Decision Coverage for fetch_order_prices_if_expired()"""
    
    def test_mcdc_condition_force_update_true(self):
        """MC/DC: force_update = True -> Process (regardless of other conditions)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                      return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations.fetch_draft_order_lines_info'):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                result_order, _ = fetch_order_prices_if_expired(
                                    order, manager, force_update=True
                                )
                                # force_update=True should trigger processing
                                assert result_order.should_refresh_prices is False
    
    def test_mcdc_condition_should_refresh_true(self):
        """MC/DC: should_refresh_prices = True -> Process (when force_update=False)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=True
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                      return_value=TaxCalculationStrategy.FLAT_RATES):
                with patch('saleor.order.calculations.fetch_draft_order_lines_info'):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                result_order, _ = fetch_order_prices_if_expired(
                                    order, manager, force_update=False
                                )
                                # should_refresh_prices=True should trigger processing
                                assert result_order.should_refresh_prices is False
    
    def test_mcdc_condition_expired_line_ids_true(self):
        """MC/DC: expired_line_ids exists -> Process (when force_update=False, should_refresh=False)"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        expired_ids = [1]
        
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=expired_ids):
            with patch('saleor.order.calculations.refresh_order_base_prices_and_discounts') as mock_refresh:
                with patch('saleor.order.calculations.get_tax_calculation_strategy_for_order',
                          return_value=TaxCalculationStrategy.FLAT_RATES):
                    with patch('saleor.order.calculations.handle_order_promotion'):
                        with patch('saleor.order.calculations.calculate_prices'):
                            with patch('saleor.order.calculations.calculate_taxes'):
                                fetch_order_prices_if_expired(
                                    order, manager, force_update=False
                                )
                                # expired_line_ids should trigger processing
                                mock_refresh.assert_called_once()
    
    def test_mcdc_condition_all_false(self):
        """MC/DC: force_update=False, should_refresh=False, expired_line_ids=[] -> Don't process"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        order = Order.objects.create(
            channel=channel,
            currency="USD",
            status=OrderStatus.DRAFT,
            should_refresh_prices=False
        )
        
        manager = Mock()
        with patch('saleor.order.calculations.get_expired_line_ids', return_value=[]):
            result_order, result_lines = fetch_order_prices_if_expired(
                order, manager, force_update=False
            )
            # All conditions False -> return early
            assert result_order == order

