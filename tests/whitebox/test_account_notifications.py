"""
Extensive White-Box Tests for saleor/account/notifications.py

Target: Increase account notifications coverage from 21% to 80%+
Covers: 57 uncovered statements
"""
import pytest
from unittest.mock import Mock, patch, MagicMock

from saleor.account.notifications import (
    get_default_user_payload,
    get_user_custom_payload,
    send_password_reset_notification,
    send_account_confirmation,
)
from saleor.account.models import User
from saleor.core.notify import NotifyEventType


@pytest.mark.django_db
class TestGetDefaultUserPayload:
    """Test get_default_user_payload()"""

    def test_get_default_user_payload_returns_correct_data(self):
        """Statement: Return user payload with all fields"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            is_staff=False,
            is_active=True,
            language_code="en"
        )
        user.private_metadata = {"key": "value"}
        user.metadata = {"public": "data"}
        user.save()
        
        with patch('saleor.account.notifications.to_global_id_or_none') as mock_id:
            mock_id.return_value = "gid://user/1"
            payload = get_default_user_payload(user)
            
            assert payload["email"] == "test@example.com"
            assert payload["first_name"] == "Test"
            assert payload["last_name"] == "User"
            assert payload["is_staff"] is False
            assert payload["is_active"] is True
            assert payload["private_metadata"] == {}  # Overridden to empty dict
            assert payload["metadata"] == {"public": "data"}
            assert payload["language_code"] == "en"

    def test_get_default_user_payload_overrides_private_metadata(self):
        """Statement: Override private_metadata with empty dict"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        user.private_metadata = {"secret": "data"}
        user.save()
        
        with patch('saleor.account.notifications.to_global_id_or_none') as mock_id:
            mock_id.return_value = "gid://user/1"
            payload = get_default_user_payload(user)
            
            assert payload["private_metadata"] == {}


@pytest.mark.django_db
class TestGetUserCustomPayload:
    """Test get_user_custom_payload()"""

    def test_get_user_custom_payload_includes_site_context(self):
        """Statement: Include site context in payload"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        
        with patch('saleor.account.notifications.to_global_id_or_none') as mock_id:
            with patch('saleor.account.notifications.get_site_context') as mock_site:
                mock_id.return_value = "gid://user/1"
                mock_site.return_value = {"site_name": "Test Site"}
                payload = get_user_custom_payload(user)
                
                assert "user" in payload
                assert "recipient_email" in payload
                assert payload["site_name"] == "Test Site"


@pytest.mark.django_db
class TestSendPasswordResetNotification:
    """Test send_password_reset_notification()"""

    @patch('saleor.account.notifications.token_generator.make_token')
    @patch('saleor.account.notifications.urlencode')
    @patch('saleor.account.notifications.prepare_url')
    @patch('saleor.account.notifications.get_site_context')
    def test_send_password_reset_notification_for_customer(
        self, mock_site, mock_prepare, mock_encode, mock_token, mock_manager
    ):
        """Statement: Send password reset for customer"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        manager = Mock()
        mock_token.return_value = "test-token"
        mock_encode.return_value = "email=test%40example.com&token=test-token"
        mock_prepare.return_value = "https://example.com/reset?email=test%40example.com&token=test-token"
        mock_site.return_value = {}
        
        with patch('saleor.account.notifications.get_default_user_payload') as mock_payload:
            mock_payload.return_value = {"id": "1", "email": "test@example.com"}
            send_password_reset_notification(
                "https://example.com/reset",
                user,
                manager,
                "channel-slug",
                staff=False
            )
            
            manager.notify.assert_called_once()
            call_args = manager.notify.call_args
            assert call_args[0][0] == NotifyEventType.ACCOUNT_PASSWORD_RESET

    @patch('saleor.account.notifications.token_generator.make_token')
    @patch('saleor.account.notifications.urlencode')
    @patch('saleor.account.notifications.prepare_url')
    @patch('saleor.account.notifications.get_site_context')
    def test_send_password_reset_notification_for_staff(
        self, mock_site, mock_prepare, mock_encode, mock_token, mock_manager
    ):
        """Statement: Send password reset for staff"""
        user = User.objects.create(
            email="staff@example.com",
            first_name="Staff",
            last_name="User",
            is_staff=True
        )
        manager = Mock()
        mock_token.return_value = "staff-token"
        mock_encode.return_value = "email=staff%40example.com&token=staff-token"
        mock_prepare.return_value = "https://example.com/reset?email=staff%40example.com&token=staff-token"
        mock_site.return_value = {}
        
        with patch('saleor.account.notifications.get_default_user_payload') as mock_payload:
            mock_payload.return_value = {"id": "1", "email": "staff@example.com"}
            send_password_reset_notification(
                "https://example.com/reset",
                user,
                manager,
                "channel-slug",
                staff=True
            )
            
            manager.notify.assert_called_once()
            call_args = manager.notify.call_args
            assert call_args[0][0] == NotifyEventType.ACCOUNT_STAFF_RESET_PASSWORD


@pytest.mark.django_db
class TestSendAccountConfirmation:
    """Test send_account_confirmation()"""

    @patch('saleor.account.notifications.token_generator.make_token')
    @patch('saleor.account.notifications.urlencode')
    @patch('saleor.account.notifications.prepare_url')
    @patch('saleor.account.notifications.get_site_context')
    def test_send_account_confirmation_without_token(
        self, mock_site, mock_prepare, mock_encode, mock_token, mock_manager
    ):
        """Statement: Generate token when not provided"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        manager = Mock()
        mock_token.return_value = "generated-token"
        mock_encode.return_value = "email=test%40example.com&token=generated-token"
        mock_prepare.return_value = "https://example.com/confirm?email=test%40example.com&token=generated-token"
        mock_site.return_value = {}
        
        with patch('saleor.account.notifications.get_default_user_payload') as mock_payload:
            mock_payload.return_value = {"id": "1", "email": "test@example.com"}
            send_account_confirmation(
                user,
                "https://example.com/confirm",
                manager,
                "channel-slug",
                token=None
            )
            
            mock_token.assert_called_once_with(user)
            manager.notify.assert_called_once()

    @patch('saleor.account.notifications.urlencode')
    @patch('saleor.account.notifications.prepare_url')
    @patch('saleor.account.notifications.get_site_context')
    def test_send_account_confirmation_with_token(
        self, mock_site, mock_prepare, mock_encode, mock_manager
    ):
        """Statement: Use provided token"""
        user = User.objects.create(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        manager = Mock()
        mock_encode.return_value = "email=test%40example.com&token=provided-token"
        mock_prepare.return_value = "https://example.com/confirm?email=test%40example.com&token=provided-token"
        mock_site.return_value = {}
        
        with patch('saleor.account.notifications.get_default_user_payload') as mock_payload:
            with patch('saleor.account.notifications.token_generator.make_token') as mock_token:
                mock_payload.return_value = {"id": "1", "email": "test@example.com"}
                send_account_confirmation(
                    user,
                    "https://example.com/confirm",
                    manager,
                    "channel-slug",
                    token="provided-token"
                )
                
                mock_token.assert_not_called()
                manager.notify.assert_called_once()

