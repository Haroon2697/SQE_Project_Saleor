"""
Extensive White-Box Tests for saleor/checkout/actions.py

Target: Increase checkout actions coverage from 24% to 80%+
Covers: 77 uncovered statements
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
from django.utils import timezone
from datetime import timedelta

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.actions import (
    call_checkout_event,
    call_checkout_events,
    call_checkout_info_event,
    update_last_transaction_modified_at_for_checkout,
    transaction_amounts_for_checkout_updated,
    transaction_amounts_for_checkout_updated_without_price_recalculation,
    _transaction_amounts_for_checkout_updated,
    _trigger_checkout_sync_webhooks,
)
from saleor.checkout import CheckoutAuthorizeStatus, CheckoutChargeStatus
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType
from saleor.payment.models import TransactionItem
from saleor.webhook.event_types import WebhookEventAsyncType, WebhookEventSyncType
from saleor.core.taxes import zero_money


@pytest.mark.django_db
class TestCallCheckoutEvent:
    """Test call_checkout_event()"""

    def test_call_checkout_event_raises_for_invalid_event(self):
        """Statement: Raise ValueError for invalid event"""
        manager = Mock()
        checkout = Mock()
        
        with pytest.raises(ValueError, match="not found in CHECKOUT_WEBHOOK_EVENT_MAP"):
            call_checkout_event(manager, "INVALID_EVENT", checkout)

    def test_call_checkout_event_without_sync_webhooks(self):
        """Statement: Call event without sync webhooks"""
        manager = Mock()
        checkout = Mock()
        event_name = WebhookEventAsyncType.CHECKOUT_CREATED
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_name: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = False
                with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                    call_checkout_event(manager, event_name, checkout)
                    
                    mock_call.assert_called_once()

    def test_call_checkout_event_with_sync_webhooks(self):
        """Statement: Call event with sync webhooks"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        manager = Mock()
        event_name = WebhookEventAsyncType.CHECKOUT_CREATED
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_name: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = True
                with patch('saleor.checkout.actions.fetch_checkout_lines') as mock_fetch_lines:
                    with patch('saleor.checkout.actions.fetch_checkout_info') as mock_fetch_info:
                        with patch('saleor.checkout.actions.call_checkout_info_event') as mock_call:
                            mock_fetch_lines.return_value = ([], None)
                            mock_fetch_info.return_value = Mock()
                            call_checkout_event(manager, event_name, checkout)
                            
                            mock_call.assert_called_once()


@pytest.mark.django_db
class TestCallCheckoutEvents:
    """Test call_checkout_events()"""

    def test_call_checkout_events_raises_for_invalid_events(self):
        """Statement: Raise ValueError for invalid events"""
        manager = Mock()
        checkout = Mock()
        event_names = ["INVALID_EVENT", "ANOTHER_INVALID"]
        
        with pytest.raises(ValueError, match="not found in CHECKOUT_WEBHOOK_EVENT_MAP"):
            call_checkout_events(manager, event_names, checkout)

    def test_call_checkout_events_with_sync_webhooks(self):
        """Statement: Trigger sync webhooks when required"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        manager = Mock()
        event_names = [WebhookEventAsyncType.CHECKOUT_CREATED]
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_names[0]: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = True
                with patch('saleor.checkout.actions.fetch_checkout_lines') as mock_fetch_lines:
                    with patch('saleor.checkout.actions.fetch_checkout_info') as mock_fetch_info:
                        with patch('saleor.checkout.actions._trigger_checkout_sync_webhooks') as mock_trigger:
                            with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                                mock_fetch_lines.return_value = ([], None)
                                mock_fetch_info.return_value = Mock()
                                call_checkout_events(manager, event_names, checkout)
                                
                                mock_trigger.assert_called_once()
                                mock_call.assert_called()

    def test_call_checkout_events_without_sync_webhooks(self):
        """Statement: Call events without sync webhooks"""
        manager = Mock()
        checkout = Mock()
        event_names = [WebhookEventAsyncType.CHECKOUT_CREATED]
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_names[0]: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = False
                with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                    call_checkout_events(manager, event_names, checkout)
                    
                    mock_call.assert_called()


@pytest.mark.django_db
class TestCallCheckoutInfoEvent:
    """Test call_checkout_info_event()"""

    def test_call_checkout_info_event_raises_for_invalid_event(self):
        """Statement: Raise ValueError for invalid event"""
        manager = Mock()
        checkout_info = Mock()
        lines = []
        
        with pytest.raises(ValueError, match="not found in CHECKOUT_WEBHOOK_EVENT_MAP"):
            call_checkout_info_event(manager, "INVALID_EVENT", checkout_info, lines)

    def test_call_checkout_info_event_without_sync_webhooks(self):
        """Statement: Call event without sync webhooks"""
        manager = Mock()
        checkout = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        event_name = WebhookEventAsyncType.CHECKOUT_CREATED
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_name: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = False
                with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                    call_checkout_info_event(manager, event_name, checkout_info, lines)
                    
                    mock_call.assert_called_once()

    def test_call_checkout_info_event_with_sync_webhooks(self):
        """Statement: Trigger sync webhooks when required"""
        manager = Mock()
        checkout = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        event_name = WebhookEventAsyncType.CHECKOUT_CREATED
        
        with patch('saleor.checkout.actions.get_webhooks_for_multiple_events') as mock_webhooks:
            mock_webhooks.return_value = {event_name: set()}
            with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
                mock_requires.return_value = True
                with patch('saleor.checkout.actions._trigger_checkout_sync_webhooks') as mock_trigger:
                    with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                        call_checkout_info_event(manager, event_name, checkout_info, lines)
                        
                        mock_trigger.assert_called_once()
                        mock_call.assert_called_once()

    def test_call_checkout_info_event_with_provided_webhook_map(self):
        """Statement: Use provided webhook_event_map"""
        manager = Mock()
        checkout = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        event_name = WebhookEventAsyncType.CHECKOUT_CREATED
        webhook_map = {event_name: set()}
        
        with patch('saleor.checkout.actions.webhook_async_event_requires_sync_webhooks_to_trigger') as mock_requires:
            mock_requires.return_value = False
            with patch('saleor.checkout.actions.call_event_including_protected_events') as mock_call:
                call_checkout_info_event(
                    manager, event_name, checkout_info, lines,
                    webhook_event_map=webhook_map
                )
                
                mock_call.assert_called_once()


@pytest.mark.django_db
class TestTriggerCheckoutSyncWebhooks:
    """Test _trigger_checkout_sync_webhooks()"""

    def test_trigger_checkout_sync_webhooks_with_expired_prices(self):
        """Statement: Fetch checkout data when prices expired"""
        manager = Mock()
        checkout = Mock()
        checkout.price_expiration = timezone.now() - timedelta(seconds=20)
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        webhook_map = {WebhookEventSyncType.CHECKOUT_CALCULATE_TAXES: set()}
        
        with patch('saleor.checkout.actions.get_or_fetch_checkout_deliveries') as mock_deliveries:
            with patch('saleor.checkout.actions.fetch_checkout_data') as mock_fetch:
                _trigger_checkout_sync_webhooks(manager, checkout_info, lines, webhook_map)
                
                mock_deliveries.assert_called_once()
                mock_fetch.assert_called_once_with(
                    checkout_info=checkout_info,
                    manager=manager,
                    lines=lines,
                    force_update=True
                )

    def test_trigger_checkout_sync_webhooks_with_valid_prices(self):
        """Statement: Skip fetch when prices valid"""
        manager = Mock()
        checkout = Mock()
        checkout.price_expiration = timezone.now() + timedelta(seconds=20)
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        webhook_map = {WebhookEventSyncType.CHECKOUT_CALCULATE_TAXES: set()}
        
        with patch('saleor.checkout.actions.get_or_fetch_checkout_deliveries') as mock_deliveries:
            with patch('saleor.checkout.actions.fetch_checkout_data') as mock_fetch:
                _trigger_checkout_sync_webhooks(manager, checkout_info, lines, webhook_map)
                
                mock_deliveries.assert_called_once()
                mock_fetch.assert_not_called()

    def test_trigger_checkout_sync_webhooks_without_tax_webhook(self):
        """Statement: Skip when no tax webhook"""
        manager = Mock()
        checkout = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        webhook_map = {}
        
        with patch('saleor.checkout.actions.get_or_fetch_checkout_deliveries') as mock_deliveries:
            with patch('saleor.checkout.actions.fetch_checkout_data') as mock_fetch:
                _trigger_checkout_sync_webhooks(manager, checkout_info, lines, webhook_map)
                
                mock_deliveries.assert_called_once()
                mock_fetch.assert_not_called()


@pytest.mark.django_db
class TestUpdateLastTransactionModifiedAt:
    """Test update_last_transaction_modified_at_for_checkout()"""

    def test_update_last_transaction_modified_at_when_none(self):
        """Statement: Update when last_transaction_modified_at is None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            last_transaction_modified_at=None
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            modified_at=timezone.now()
        )
        
        update_last_transaction_modified_at_for_checkout(checkout, transaction)
        
        checkout.refresh_from_db()
        assert checkout.last_transaction_modified_at == transaction.modified_at

    def test_update_last_transaction_modified_at_when_older(self):
        """Statement: Update when transaction is newer"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        old_time = timezone.now() - timedelta(hours=1)
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            last_transaction_modified_at=old_time
        )
        new_time = timezone.now()
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            modified_at=new_time
        )
        
        update_last_transaction_modified_at_for_checkout(checkout, transaction)
        
        checkout.refresh_from_db()
        assert checkout.last_transaction_modified_at == new_time

    def test_update_last_transaction_modified_at_when_newer_exists(self):
        """Statement: Skip when existing is newer"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        new_time = timezone.now()
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            last_transaction_modified_at=new_time
        )
        old_time = timezone.now() - timedelta(hours=1)
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            modified_at=old_time
        )
        
        update_last_transaction_modified_at_for_checkout(checkout, transaction)
        
        checkout.refresh_from_db()
        assert checkout.last_transaction_modified_at == new_time


@pytest.mark.django_db
class TestTransactionAmountsForCheckoutUpdated:
    """Test transaction_amounts_for_checkout_updated()"""

    def test_transaction_amounts_for_checkout_updated_without_checkout(self):
        """Statement: Return early when no checkout_id"""
        transaction = TransactionItem.objects.create()
        manager = Mock()
        
        # Should not raise error
        transaction_amounts_for_checkout_updated(transaction, manager, None, None)

    def test_transaction_amounts_for_checkout_updated_with_checkout(self):
        """Statement: Process checkout when checkout_id exists"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout
        )
        manager = Mock()
        
        with patch('saleor.checkout.actions.fetch_checkout_lines') as mock_fetch_lines:
            with patch('saleor.checkout.actions.fetch_checkout_info') as mock_fetch_info:
                with patch('saleor.checkout.actions.fetch_checkout_data') as mock_fetch_data:
                    with patch('saleor.checkout.actions._transaction_amounts_for_checkout_updated') as mock_internal:
                        mock_fetch_lines.return_value = ([], None)
                        mock_fetch_info.return_value = Mock()
                        mock_fetch_info.return_value.checkout = checkout
                        
                        transaction_amounts_for_checkout_updated(transaction, manager, None, None)
                        
                        mock_internal.assert_called_once()


@pytest.mark.django_db
class TestTransactionAmountsForCheckoutUpdatedWithoutPriceRecalculation:
    """Test transaction_amounts_for_checkout_updated_without_price_recalculation()"""

    def test_transaction_amounts_without_recalculation_updates_status(self):
        """Statement: Update payment status without price recalculation"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout
        )
        manager = Mock()
        
        def mock_get_total_gift_cards_balance(db_name):
            return zero_money("USD")
        
        checkout.get_total_gift_cards_balance = mock_get_total_gift_cards_balance
        checkout.total = Mock()
        checkout.total.gross = zero_money("USD")
        
        with patch('saleor.checkout.actions.fetch_checkout_lines') as mock_fetch_lines:
            with patch('saleor.checkout.actions.fetch_checkout_info') as mock_fetch_info:
                with patch('saleor.checkout.actions.update_checkout_payment_statuses') as mock_update_status:
                    with patch('saleor.checkout.actions._transaction_amounts_for_checkout_updated') as mock_internal:
                        mock_fetch_lines.return_value = ([], None)
                        checkout_info = Mock()
                        checkout_info.checkout = checkout
                        mock_fetch_info.return_value = checkout_info
                        
                        transaction_amounts_for_checkout_updated_without_price_recalculation(
                            transaction, checkout, manager, None, None
                        )
                        
                        mock_update_status.assert_called_once()
                        mock_internal.assert_called_once()


@pytest.mark.django_db
class TestTransactionAmountsForCheckoutUpdatedInternal:
    """Test _transaction_amounts_for_checkout_updated()"""

    def test_transaction_amounts_internal_triggers_fully_paid_event(self):
        """Statement: Trigger CHECKOUT_FULLY_PAID event when status changes"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            charge_status=CheckoutChargeStatus.PARTIAL
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            last_refund_success=False
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.checkout.charge_status = CheckoutChargeStatus.FULL
        lines = []
        
        with patch('saleor.checkout.actions.update_last_transaction_modified_at_for_checkout') as mock_update:
            with patch('saleor.checkout.actions.update_refundable_for_checkout') as mock_refund:
                with patch('saleor.checkout.actions.call_checkout_info_event') as mock_call:
                    _transaction_amounts_for_checkout_updated(
                        transaction,
                        CheckoutChargeStatus.PARTIAL,
                        CheckoutAuthorizeStatus.NONE,
                        checkout_info,
                        lines,
                        manager,
                        None,
                        None
                    )
                    
                    mock_call.assert_called_once_with(
                        manager,
                        WebhookEventAsyncType.CHECKOUT_FULLY_PAID,
                        checkout_info,
                        lines
                    )

    def test_transaction_amounts_internal_triggers_fully_authorized_event(self):
        """Statement: Trigger CHECKOUT_FULLY_AUTHORIZED event when status changes"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            authorize_status=CheckoutAuthorizeStatus.PARTIAL
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            last_refund_success=False
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.checkout.authorize_status = CheckoutAuthorizeStatus.FULL
        lines = []
        
        with patch('saleor.checkout.actions.update_last_transaction_modified_at_for_checkout') as mock_update:
            with patch('saleor.checkout.actions.update_refundable_for_checkout') as mock_refund:
                with patch('saleor.checkout.actions.call_checkout_info_event') as mock_call:
                    _transaction_amounts_for_checkout_updated(
                        transaction,
                        CheckoutChargeStatus.NONE,
                        CheckoutAuthorizeStatus.PARTIAL,
                        checkout_info,
                        lines,
                        manager,
                        None,
                        None
                    )
                    
                    mock_call.assert_called_once_with(
                        manager,
                        WebhookEventAsyncType.CHECKOUT_FULLY_AUTHORIZED,
                        checkout_info,
                        lines
                    )

    def test_transaction_amounts_internal_updates_refundable(self):
        """Statement: Update refundable when different"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            automatically_refundable=False
        )
        transaction = TransactionItem.objects.create(
            checkout=checkout,
            last_refund_success=True,
            authorized_value=Decimal("10.00")
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.actions.update_last_transaction_modified_at_for_checkout') as mock_update:
            with patch('saleor.checkout.actions.update_refundable_for_checkout') as mock_refund:
                _transaction_amounts_for_checkout_updated(
                    transaction,
                    CheckoutChargeStatus.NONE,
                    CheckoutAuthorizeStatus.NONE,
                    checkout_info,
                    lines,
                    manager,
                    None,
                    None
                )
                
                mock_refund.assert_called_once_with(checkout.pk)

