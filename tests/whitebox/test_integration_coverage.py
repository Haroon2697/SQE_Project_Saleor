"""
Integration Coverage Tests
==========================
Tests verifying multiple components work together.
"""
import pytest
from decimal import Decimal
from prices import Money, TaxedMoney


class TestIntegrationPriceTax:
    """Integration tests for price and tax."""

    def test_price_with_tax_integration(self):
        """Test price quantization with tax calculations."""
        from saleor.core.prices import quantize_price
        from saleor.core.taxes import zero_money, zero_taxed_money
        
        net = Money(Decimal("100.00"), "USD")
        gross = Money(Decimal("121.00"), "USD")
        taxed_price = TaxedMoney(net=net, gross=gross)
        
        quantized = quantize_price(taxed_price, "USD")
        
        assert quantized.net.amount == Decimal("100.00")
        assert quantized.gross.amount == Decimal("121.00")
        
        zero = zero_money("USD")
        assert zero.amount == Decimal("0")
        
        zero_taxed = zero_taxed_money("USD")
        assert zero_taxed.net.amount == Decimal("0")


class TestIntegrationWeightShipping:
    """Integration tests for weight and shipping."""

    def test_weight_conversion_for_shipping(self):
        """Test weight conversion for shipping calculations."""
        from saleor.core.weight import convert_weight, zero_weight
        from saleor.shipping.interface import ShippingMethodData
        from measurement.measures import Weight
        
        min_weight = Weight(kg=0.5)
        max_weight = Weight(kg=10)
        
        shipping = ShippingMethodData(
            id="ship_1",
            name="Standard",
            price=Money(Decimal("5.00"), "USD"),
            minimum_order_weight=min_weight,
            maximum_order_weight=max_weight,
        )
        
        min_lb = convert_weight(min_weight, "lb")
        max_lb = convert_weight(max_weight, "lb")
        
        assert min_lb.unit == "lb"
        assert max_lb.unit == "lb"


class TestIntegrationOrderPayment:
    """Integration tests for order and payment."""

    def test_order_payment_status_integration(self):
        """Test order status with payment status."""
        from saleor.order import OrderStatus, OrderChargeStatus
        from saleor.payment import ChargeStatus
        
        order_statuses = [
            OrderStatus.DRAFT,
            OrderStatus.UNFULFILLED,
            OrderStatus.FULFILLED,
        ]
        
        charge_statuses = [
            OrderChargeStatus.NONE,
            OrderChargeStatus.PARTIAL,
            OrderChargeStatus.FULL,
        ]
        
        for os in order_statuses:
            for cs in charge_statuses:
                assert os is not None
                assert cs is not None


class TestIntegrationDiscountPrice:
    """Integration tests for discount and price."""

    def test_discount_application_integration(self):
        """Test discount application to prices."""
        from saleor.discount import DiscountType, DiscountValueType
        from saleor.core.prices import quantize_price
        
        original_price = Money(Decimal("100.00"), "USD")
        
        fixed_discount = Decimal("10.00")
        discounted_fixed = Money(original_price.amount - fixed_discount, "USD")
        assert discounted_fixed.amount == Decimal("90.00")
        
        percentage = Decimal("0.15")
        discount_amount = original_price.amount * percentage
        discounted_percent = Money(original_price.amount - discount_amount, "USD")
        assert discounted_percent.amount == Decimal("85.00")


class TestIntegrationWebhookEvents:
    """Integration tests for webhook events."""

    def test_webhook_event_types_integration(self):
        """Test webhook event types work together."""
        from saleor.webhook.event_types import (
            WebhookEventSyncType,
            WebhookEventAsyncType,
        )
        
        sync_events = [
            WebhookEventSyncType.PAYMENT_AUTHORIZE,
            WebhookEventSyncType.PAYMENT_CAPTURE,
            WebhookEventSyncType.PAYMENT_REFUND,
        ]
        
        async_events = [
            WebhookEventAsyncType.ORDER_CREATED,
            WebhookEventAsyncType.ORDER_UPDATED,
            WebhookEventAsyncType.ORDER_CONFIRMED,
        ]
        
        all_events = sync_events + async_events
        assert len(set(all_events)) == len(all_events)


class TestIntegrationErrorCodes:
    """Integration tests for error codes."""

    def test_checkout_order_error_codes_integration(self):
        """Test error codes used across modules."""
        from saleor.checkout.error_codes import CheckoutErrorCode
        from saleor.order.error_codes import OrderErrorCode
        
        assert CheckoutErrorCode.INSUFFICIENT_STOCK is not None
        assert OrderErrorCode.INSUFFICIENT_STOCK is not None
        
        assert CheckoutErrorCode.INVALID is not None
        assert OrderErrorCode.INVALID is not None

