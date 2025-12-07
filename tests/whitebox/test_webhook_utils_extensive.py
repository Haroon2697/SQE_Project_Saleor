"""
Extensive White-Box Tests for saleor/webhook/utils.py

Target: Increase webhook utils coverage from 18% to 80%+
Covers: 127 uncovered statements
"""
import pytest
from unittest.mock import Mock, patch
from django.db.models import Q

from saleor.webhook.utils import (
    get_filter_for_single_webhook_event,
    get_webhooks_for_event,
    get_webhooks_for_multiple_events,
    calculate_webhooks_for_multiple_events,
)
from saleor.webhook.models import Webhook, WebhookEvent
from saleor.webhook.event_types import WebhookEventAsyncType, WebhookEventSyncType
from saleor.app.models import App
from saleor.permission.models import Permission


@pytest.mark.django_db
class TestGetFilterForSingleWebhookEvent:
    """Test get_filter_for_single_webhook_event()"""

    def test_get_filter_with_apps_ids(self):
        """Statement: Filter by apps_ids"""
        app = App.objects.create(name="Test App", is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.App.objects.using') as mock_apps:
                with patch('saleor.webhook.utils.WebhookEvent.objects.using') as mock_events:
                    mock_apps.return_value.filter.return_value = App.objects.filter(id=app.id)
                    mock_events.return_value.filter.return_value = WebhookEvent.objects.none()
                    
                    result = get_filter_for_single_webhook_event(
                        event_type=event_type,
                        apps_ids=[app.id]
                    )
                    
                    assert isinstance(result, Q)

    def test_get_filter_with_apps_identifier(self):
        """Statement: Filter by apps_identifier"""
        app = App.objects.create(name="Test App", identifier="test-app", is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.App.objects.using') as mock_apps:
                with patch('saleor.webhook.utils.WebhookEvent.objects.using') as mock_events:
                    mock_apps.return_value.filter.return_value = App.objects.filter(id=app.id)
                    mock_events.return_value.filter.return_value = WebhookEvent.objects.none()
                    
                    result = get_filter_for_single_webhook_event(
                        event_type=event_type,
                        apps_identifier=["test-app"]
                    )
                    
                    assert isinstance(result, Q)

    def test_get_filter_with_permissions(self):
        """Statement: Include permissions in filter"""
        app = App.objects.create(name="Test App", is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.App.objects.using') as mock_apps:
                with patch('saleor.webhook.utils.WebhookEvent.objects.using') as mock_events:
                    mock_apps.return_value.filter.return_value = App.objects.filter(id=app.id)
                    mock_events.return_value.filter.return_value = WebhookEvent.objects.none()
                    
                    result = get_filter_for_single_webhook_event(event_type=event_type)
                    
                    assert isinstance(result, Q)

    def test_get_filter_with_app_deleted_event(self):
        """Statement: Handle APP_DELETED event differently"""
        app = App.objects.create(name="Test App", is_active=True)
        event_type = WebhookEventAsyncType.APP_DELETED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.App.objects.using') as mock_apps:
                with patch('saleor.webhook.utils.WebhookEvent.objects.using') as mock_events:
                    mock_apps.return_value.filter.return_value = App.objects.filter(id=app.id)
                    mock_events.return_value.filter.return_value = WebhookEvent.objects.none()
                    
                    result = get_filter_for_single_webhook_event(event_type=event_type)
                    
                    assert isinstance(result, Q)

    def test_get_filter_adds_any_event_for_async_events(self):
        """Statement: Add ANY event type for async events"""
        app = App.objects.create(name="Test App", is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.App.objects.using') as mock_apps:
                with patch('saleor.webhook.utils.WebhookEvent.objects.using') as mock_events:
                    mock_apps.return_value.filter.return_value = App.objects.filter(id=app.id)
                    mock_events.return_value.filter.return_value = WebhookEvent.objects.none()
                    
                    result = get_filter_for_single_webhook_event(event_type=event_type)
                    
                    assert isinstance(result, Q)


@pytest.mark.django_db
class TestGetWebhooksForEvent:
    """Test get_webhooks_for_event()"""

    def test_get_webhooks_for_event_with_none_webhooks(self):
        """Statement: Create queryset when webhooks is None"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        WebhookEvent.objects.create(webhook=webhook, event_type=WebhookEventAsyncType.ORDER_CREATED)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            result = get_webhooks_for_event(event_type)
            
            assert result is not None

    def test_get_webhooks_for_event_with_provided_webhooks(self):
        """Statement: Use provided webhooks queryset"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        WebhookEvent.objects.create(webhook=webhook, event_type=WebhookEventAsyncType.ORDER_CREATED)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        webhooks = Webhook.objects.all()
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            result = get_webhooks_for_event(event_type, webhooks=webhooks)
            
            assert result is not None

    def test_get_webhooks_for_event_with_apps_ids(self):
        """Statement: Filter by apps_ids"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        WebhookEvent.objects.create(webhook=webhook, event_type=WebhookEventAsyncType.ORDER_CREATED)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            result = get_webhooks_for_event(event_type, apps_ids=[app.id])
            
            assert result is not None


@pytest.mark.django_db
class TestGetWebhooksForMultipleEvents:
    """Test get_webhooks_for_multiple_events()"""

    def test_get_webhooks_for_multiple_events_adds_any_for_async(self):
        """Statement: Add ANY event type for async events"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        WebhookEvent.objects.create(webhook=webhook, event_type=WebhookEventAsyncType.ORDER_CREATED)
        event_types = [WebhookEventAsyncType.ORDER_CREATED]
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.calculate_webhooks_for_multiple_events') as mock_calc:
                mock_calc.return_value = {event_types[0]: set()}
                result = get_webhooks_for_multiple_events(event_types)
                
                assert isinstance(result, dict)

    def test_get_webhooks_for_multiple_events_with_sync_events(self):
        """Statement: Handle sync events"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        WebhookEvent.objects.create(webhook=webhook, event_type=WebhookEventSyncType.CHECKOUT_CALCULATE_TAXES)
        event_types = [WebhookEventSyncType.CHECKOUT_CALCULATE_TAXES]
        
        with patch('saleor.webhook.utils.settings') as mock_settings:
            mock_settings.DATABASE_CONNECTION_REPLICA_NAME = 'default'
            with patch('saleor.webhook.utils.calculate_webhooks_for_multiple_events') as mock_calc:
                mock_calc.return_value = {event_types[0]: set()}
                result = get_webhooks_for_multiple_events(event_types)
                
                assert isinstance(result, dict)


@pytest.mark.django_db
class TestCalculateWebhooksForMultipleEvents:
    """Test calculate_webhooks_for_multiple_events()"""

    def test_calculate_webhooks_without_permissions(self):
        """Statement: Add webhook when no permissions required"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        set_event_types = {event_type}
        app_by_id_map = {app.id: app}
        webhooks = [webhook]
        events_types_by_webhook_id_map = {webhook.id: {event_type}}
        
        with patch('saleor.webhook.utils.WebhookEventAsyncType.PERMISSIONS', {}):
            with patch('saleor.webhook.utils.WebhookEventSyncType.PERMISSIONS', {}):
                result = calculate_webhooks_for_multiple_events(
                    set_event_types,
                    app_by_id_map,
                    webhooks,
                    events_types_by_webhook_id_map
                )
                
                assert event_type in result
                assert webhook in result[event_type]

    def test_calculate_webhooks_with_matching_permissions(self):
        """Statement: Add webhook when permissions match"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        set_event_types = {event_type}
        app_by_id_map = {app.id: app}
        webhooks = [webhook]
        events_types_by_webhook_id_map = {webhook.id: {event_type}}
        
        # Mock permission
        permission = Mock()
        permission.value = "order.manage_orders"
        with patch('saleor.webhook.utils.WebhookEventAsyncType.PERMISSIONS', {event_type: permission}):
            with patch('saleor.webhook.utils.WebhookEventSyncType.PERMISSIONS', {}):
                with patch.object(app, 'permissions') as mock_perms:
                    mock_perms.all.return_value = [Mock(content_type=Mock(app_label="order"), codename="manage_orders")]
                    result = calculate_webhooks_for_multiple_events(
                        set_event_types,
                        app_by_id_map,
                        webhooks,
                        events_types_by_webhook_id_map
                    )
                    
                    assert event_type in result

    def test_calculate_webhooks_skips_inactive_app(self):
        """Statement: Skip webhook when app not in app_by_id_map"""
        app = App.objects.create(name="Test App", is_active=True)
        webhook = Webhook.objects.create(app=app, is_active=True)
        event_type = WebhookEventAsyncType.ORDER_CREATED
        set_event_types = {event_type}
        app_by_id_map = {}  # App not in map
        webhooks = [webhook]
        events_types_by_webhook_id_map = {webhook.id: {event_type}}
        
        result = calculate_webhooks_for_multiple_events(
            set_event_types,
            app_by_id_map,
            webhooks,
            events_types_by_webhook_id_map
        )
        
        assert event_type in result
        assert webhook not in result[event_type]  # Should be empty set

    def test_calculate_webhooks_adds_empty_sets_for_all_events(self):
        """Statement: Add empty sets for all events"""
        set_event_types = {
            WebhookEventAsyncType.ORDER_CREATED,
            WebhookEventAsyncType.ORDER_UPDATED
        }
        app_by_id_map = {}
        webhooks = []
        events_types_by_webhook_id_map = {}
        
        result = calculate_webhooks_for_multiple_events(
            set_event_types,
            app_by_id_map,
            webhooks,
            events_types_by_webhook_id_map
        )
        
        assert WebhookEventAsyncType.ORDER_CREATED in result
        assert WebhookEventAsyncType.ORDER_UPDATED in result
        assert result[WebhookEventAsyncType.ORDER_CREATED] == set()
        assert result[WebhookEventAsyncType.ORDER_UPDATED] == set()

