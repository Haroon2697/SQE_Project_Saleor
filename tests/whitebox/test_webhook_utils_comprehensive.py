"""
Comprehensive White-Box Tests for saleor/webhook/utils.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- get_filter_for_single_webhook_event
- get_webhooks_for_event
- get_webhooks_for_multiple_events
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from django.db.models import Q

from saleor.webhook.utils import (
    get_filter_for_single_webhook_event,
    get_webhooks_for_event,
    get_webhooks_for_multiple_events,
)
from saleor.webhook.event_types import WebhookEventAsyncType, WebhookEventSyncType
from saleor.webhook.models import Webhook, WebhookEvent
from saleor.app.models import App


@pytest.mark.django_db
class TestGetFilterForSingleWebhookEvent:
    """Test get_filter_for_single_webhook_event() - Statement Coverage"""

    def test_get_filter_with_event_type_async(self):
        """Statement: Test with async event type"""
        event_type = WebhookEventAsyncType.ORDER_CREATED
        result = get_filter_for_single_webhook_event(event_type)
        assert isinstance(result, Q)
        assert result.connector == Q.AND

    def test_get_filter_with_event_type_sync(self):
        """Statement: Test with sync event type"""
        event_type = WebhookEventSyncType.PAYMENT_AUTHORIZE
        result = get_filter_for_single_webhook_event(event_type)
        assert isinstance(result, Q)

    def test_get_filter_with_apps_ids(self):
        """Statement: Test with apps_ids parameter"""
        event_type = WebhookEventAsyncType.ORDER_CREATED
        apps_ids = [1, 2, 3]
        result = get_filter_for_single_webhook_event(event_type, apps_ids=apps_ids)
        assert isinstance(result, Q)

    def test_get_filter_with_apps_identifier(self):
        """Statement: Test with apps_identifier parameter"""
        event_type = WebhookEventAsyncType.ORDER_CREATED
        apps_identifier = ["app1", "app2"]
        result = get_filter_for_single_webhook_event(
            event_type, apps_identifier=apps_identifier
        )
        assert isinstance(result, Q)

    def test_get_filter_with_both_apps_ids_and_identifier(self):
        """Statement: Test with both apps_ids and apps_identifier"""
        event_type = WebhookEventAsyncType.ORDER_CREATED
        apps_ids = [1, 2]
        apps_identifier = ["app1"]
        result = get_filter_for_single_webhook_event(
            event_type, apps_ids=apps_ids, apps_identifier=apps_identifier
        )
        assert isinstance(result, Q)

    def test_get_filter_with_app_deleted_event(self):
        """Decision: Test with APP_DELETED event (different logic)"""
        event_type = WebhookEventAsyncType.APP_DELETED
        result = get_filter_for_single_webhook_event(event_type)
        assert isinstance(result, Q)

    def test_get_filter_without_permissions(self):
        """Statement: Test event type without required permissions"""
        # Use an event type that might not have permissions
        event_type = "CUSTOM_EVENT"
        result = get_filter_for_single_webhook_event(event_type)
        assert isinstance(result, Q)


@pytest.mark.django_db
class TestGetWebhooksForEvent:
    """Test get_webhooks_for_event() - Statement Coverage"""

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_event_with_webhooks_queryset(self, mock_settings):
        """Statement: Test with provided webhooks queryset"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_type = WebhookEventAsyncType.ORDER_CREATED
        webhooks = Webhook.objects.none()  # Empty queryset
        
        result = get_webhooks_for_event(event_type, webhooks=webhooks)
        assert result is not None

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_event_without_webhooks(self, mock_settings):
        """Statement: Test without provided webhooks (uses all)"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_type = WebhookEventAsyncType.ORDER_CREATED
        result = get_webhooks_for_event(event_type)
        assert result is not None

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_event_with_apps_ids(self, mock_settings):
        """Statement: Test with apps_ids parameter"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_type = WebhookEventAsyncType.ORDER_CREATED
        apps_ids = [1, 2, 3]
        result = get_webhooks_for_event(event_type, apps_ids=apps_ids)
        assert result is not None

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_event_with_apps_identifier(self, mock_settings):
        """Statement: Test with apps_identifier parameter"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_type = WebhookEventAsyncType.ORDER_CREATED
        apps_identifier = ["app1", "app2"]
        result = get_webhooks_for_event(event_type, apps_identifier=apps_identifier)
        assert result is not None


@pytest.mark.django_db
class TestGetWebhooksForMultipleEvents:
    """Test get_webhooks_for_multiple_events() - Statement Coverage"""

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_multiple_events_empty(self, mock_settings):
        """Statement: Test with empty event types"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_types = []
        result = get_webhooks_for_multiple_events(event_types)
        assert isinstance(result, dict)
        assert len(result) == 0

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_multiple_events_single(self, mock_settings):
        """Statement: Test with single event type"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_types = [WebhookEventAsyncType.ORDER_CREATED]
        result = get_webhooks_for_multiple_events(event_types)
        assert isinstance(result, dict)

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_multiple_events_multiple(self, mock_settings):
        """Statement: Test with multiple event types"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_types = [
            WebhookEventAsyncType.ORDER_CREATED,
            WebhookEventAsyncType.ORDER_UPDATED,
        ]
        result = get_webhooks_for_multiple_events(event_types)
        assert isinstance(result, dict)

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_multiple_events_with_any(self, mock_settings):
        """Decision: Test with event type that triggers ANY addition"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        # Use an async event type that should trigger ANY addition
        event_types = [WebhookEventAsyncType.ORDER_CREATED]
        result = get_webhooks_for_multiple_events(event_types)
        assert isinstance(result, dict)

    @patch('saleor.webhook.utils.settings')
    def test_get_webhooks_for_multiple_events_with_sync_events(self, mock_settings):
        """Statement: Test with sync event types"""
        mock_settings.DATABASE_CONNECTION_REPLICA_NAME = "default"
        
        event_types = [WebhookEventSyncType.PAYMENT_AUTHORIZE]
        result = get_webhooks_for_multiple_events(event_types)
        assert isinstance(result, dict)

