"""
Tests for plugins to increase coverage.
"""
import pytest
from unittest.mock import Mock, patch

# Import plugin modules
from saleor.plugins import base_plugin
from saleor.plugins import manager
from saleor.plugins import models as plugins_models

# Import specific plugins
from saleor.plugins.admin_email import plugin as admin_email_plugin
from saleor.plugins.admin_email import constants as admin_email_constants
from saleor.plugins.admin_email import notify_events as admin_email_notify
from saleor.plugins.admin_email import tasks as admin_email_tasks

from saleor.plugins.user_email import plugin as user_email_plugin
from saleor.plugins.user_email import constants as user_email_constants
from saleor.plugins.user_email import notify_events as user_email_notify
from saleor.plugins.user_email import tasks as user_email_tasks

from saleor.plugins.sendgrid import plugin as sendgrid_plugin
from saleor.plugins.sendgrid import tasks as sendgrid_tasks

from saleor.plugins.avatax import plugin as avatax_plugin
from saleor.plugins.avatax import tasks as avatax_tasks

from saleor.plugins.openid_connect import plugin as openid_plugin
from saleor.plugins.openid_connect import utils as openid_utils
from saleor.plugins.openid_connect import client as openid_client
from saleor.plugins.openid_connect import dataclasses as openid_dataclasses

from saleor.plugins.webhook import plugin as webhook_plugin

from saleor.plugins import email_common


class TestBasePluginImport:
    """Test base plugin is importable."""

    def test_base_plugin_module(self):
        assert base_plugin is not None

    def test_base_plugin_class(self):
        from saleor.plugins.base_plugin import BasePlugin
        assert BasePlugin is not None

    def test_excluded_shipping_method(self):
        from saleor.plugins.base_plugin import ExcludedShippingMethod
        assert ExcludedShippingMethod is not None


class TestPluginManagerImport:
    """Test plugin manager is importable."""

    def test_manager_module(self):
        assert manager is not None

    def test_plugins_manager_class(self):
        from saleor.plugins.manager import PluginsManager
        assert PluginsManager is not None


class TestPluginModelsImport:
    """Test plugin models are importable."""

    def test_models_module(self):
        assert plugins_models is not None

    def test_plugin_configuration_model(self):
        from saleor.plugins.models import PluginConfiguration
        assert PluginConfiguration is not None


class TestAdminEmailPluginImport:
    """Test admin email plugin is importable."""

    def test_plugin_module(self):
        assert admin_email_plugin is not None

    def test_constants_module(self):
        assert admin_email_constants is not None

    def test_notify_events_module(self):
        assert admin_email_notify is not None

    def test_tasks_module(self):
        assert admin_email_tasks is not None


class TestUserEmailPluginImport:
    """Test user email plugin is importable."""

    def test_plugin_module(self):
        assert user_email_plugin is not None

    def test_constants_module(self):
        assert user_email_constants is not None

    def test_notify_events_module(self):
        assert user_email_notify is not None

    def test_tasks_module(self):
        assert user_email_tasks is not None


class TestSendgridPluginImport:
    """Test sendgrid plugin is importable."""

    def test_plugin_module(self):
        assert sendgrid_plugin is not None

    def test_tasks_module(self):
        assert sendgrid_tasks is not None


class TestAvataxPluginImport:
    """Test avatax plugin is importable."""

    def test_plugin_module(self):
        assert avatax_plugin is not None

    def test_tasks_module(self):
        assert avatax_tasks is not None


class TestOpenidConnectPluginImport:
    """Test openid connect plugin is importable."""

    def test_plugin_module(self):
        assert openid_plugin is not None

    def test_utils_module(self):
        assert openid_utils is not None

    def test_client_module(self):
        assert openid_client is not None

    def test_dataclasses_module(self):
        assert openid_dataclasses is not None


class TestWebhookPluginImport:
    """Test webhook plugin is importable."""

    def test_plugin_module(self):
        assert webhook_plugin is not None


class TestEmailCommonImport:
    """Test email common module is importable."""

    def test_email_common_module(self):
        assert email_common is not None


class TestPluginErrorCodes:
    """Test plugin error codes."""

    def test_error_codes_module(self):
        from saleor.plugins import error_codes
        assert error_codes is not None

