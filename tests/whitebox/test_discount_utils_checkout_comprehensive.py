"""
Comprehensive White-Box Tests for saleor/discount/utils/checkout.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from datetime import datetime, timedelta
from prices import Money

from saleor.discount.models import CheckoutDiscount, CheckoutLineDiscount, DiscountType, DiscountValueType
from saleor.discount.utils.checkout import (
    create_or_update_discount_objects_from_promotion_for_checkout,
    create_checkout_line_discount_objects_for_catalogue_promotions,
    prepare_checkout_line_discount_objects_for_catalogue_promotions,
    create_checkout_discount_objects_for_order_promotions,
    _set_checkout_base_prices,
    _clear_checkout_discount,
)
from saleor.checkout.models import Checkout
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType, Category


@pytest.mark.django_db
class TestCreateOrUpdateDiscountObjectsFromPromotionForCheckout:
    """Test create_or_update_discount_objects_from_promotion_for_checkout()"""

    def test_create_or_update_discount_objects_returns_soonest_end_date(self):
        """Statement: Return soonest end date when both dates exist"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.get_country.return_value = "US"
        
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.create_checkout_line_discount_objects_for_catalogue_promotions') as mock_catalogue:
            with patch('saleor.discount.utils.checkout.create_checkout_discount_objects_for_order_promotions') as mock_order:
                mock_catalogue.return_value = datetime.now() + timedelta(days=5)
                mock_order.return_value = datetime.now() + timedelta(days=3)
                
                result = create_or_update_discount_objects_from_promotion_for_checkout(
                    checkout_info, lines_info
                )
                
                assert result == datetime.now() + timedelta(days=3)

    def test_create_or_update_discount_objects_returns_catalogue_date_only(self):
        """Statement: Return catalogue date when order date is None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.get_country.return_value = "US"
        
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.create_checkout_line_discount_objects_for_catalogue_promotions') as mock_catalogue:
            with patch('saleor.discount.utils.checkout.create_checkout_discount_objects_for_order_promotions') as mock_order:
                mock_catalogue.return_value = datetime.now() + timedelta(days=5)
                mock_order.return_value = None
                
                result = create_or_update_discount_objects_from_promotion_for_checkout(
                    checkout_info, lines_info
                )
                
                assert result == datetime.now() + timedelta(days=5)

    def test_create_or_update_discount_objects_returns_order_date_only(self):
        """Statement: Return order date when catalogue date is None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.get_country.return_value = "US"
        
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.create_checkout_line_discount_objects_for_catalogue_promotions') as mock_catalogue:
            with patch('saleor.discount.utils.checkout.create_checkout_discount_objects_for_order_promotions') as mock_order:
                mock_catalogue.return_value = None
                mock_order.return_value = datetime.now() + timedelta(days=3)
                
                result = create_or_update_discount_objects_from_promotion_for_checkout(
                    checkout_info, lines_info
                )
                
                assert result == datetime.now() + timedelta(days=3)

    def test_create_or_update_discount_objects_returns_none_when_both_none(self):
        """Statement: Return None when both dates are None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.get_country.return_value = "US"
        
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.create_checkout_line_discount_objects_for_catalogue_promotions') as mock_catalogue:
            with patch('saleor.discount.utils.checkout.create_checkout_discount_objects_for_order_promotions') as mock_order:
                mock_catalogue.return_value = None
                mock_order.return_value = None
                
                result = create_or_update_discount_objects_from_promotion_for_checkout(
                    checkout_info, lines_info
                )
                
                assert result is None


@pytest.mark.django_db
class TestPrepareCheckoutLineDiscountObjectsForCataloguePromotions:
    """Test prepare_checkout_line_discount_objects_for_catalogue_promotions()"""

    def test_prepare_checkout_line_discount_returns_none_when_no_lines(self):
        """Statement: Return None when lines_info is empty"""
        result = prepare_checkout_line_discount_objects_for_catalogue_promotions([])
        assert result is None

    def test_prepare_checkout_line_discount_skips_line_without_channel_listing(self):
        """Statement: Skip line when channel_listing is None"""
        line_info = Mock()
        line_info.line = Mock()
        line_info.line.is_gift = False
        line_info.channel_listing = None
        line_info.get_catalogue_discounts.return_value = []
        line_info.discounts = []
        line_info.rules_info = []
        
        result = prepare_checkout_line_discount_objects_for_catalogue_promotions([line_info])
        
        assert result is not None
        assert len(result[0]) == 0  # No discounts to create

    def test_prepare_checkout_line_discount_removes_when_manual_discount_exists(self):
        """Statement: Remove existing discounts when manual discount exists"""
        line_info = Mock()
        line_info.line = Mock()
        line_info.line.is_gift = False
        line_info.channel_listing = Mock()
        existing_discount = Mock()
        line_info.get_catalogue_discounts.return_value = [existing_discount]
        manual_discount = Mock()
        manual_discount.type = DiscountType.MANUAL
        line_info.discounts = [manual_discount]
        line_info.rules_info = []
        
        result = prepare_checkout_line_discount_objects_for_catalogue_promotions([line_info])
        
        assert result is not None
        assert existing_discount in result[2]  # Should be in discounts_to_remove

    def test_prepare_checkout_line_discount_removes_when_not_discounted(self):
        """Statement: Remove discounts when line is not discounted"""
        line_info = Mock()
        line_info.line = Mock()
        line_info.line.is_gift = False
        line_info.channel_listing = Mock()
        existing_discount = Mock()
        line_info.get_catalogue_discounts.return_value = [existing_discount]
        line_info.discounts = []
        
        with patch('saleor.discount.utils.checkout.is_discounted_line_by_catalogue_promotion', return_value=False):
            result = prepare_checkout_line_discount_objects_for_catalogue_promotions([line_info])
            
            assert result is not None
            assert existing_discount in result[2]  # Should be in discounts_to_remove

    def test_prepare_checkout_line_discount_removes_when_gift(self):
        """Statement: Remove discounts when line is gift"""
        line_info = Mock()
        line_info.line = Mock()
        line_info.line.is_gift = True
        line_info.channel_listing = Mock()
        existing_discount = Mock()
        line_info.get_catalogue_discounts.return_value = [existing_discount]
        line_info.discounts = []
        
        with patch('saleor.discount.utils.checkout.is_discounted_line_by_catalogue_promotion', return_value=True):
            result = prepare_checkout_line_discount_objects_for_catalogue_promotions([line_info])
            
            assert result is not None
            assert existing_discount in result[2]  # Should be in discounts_to_remove


@pytest.mark.django_db
class TestCreateCheckoutDiscountObjectsForOrderPromotions:
    """Test create_checkout_discount_objects_for_order_promotions()"""

    def test_create_checkout_discount_clears_when_voucher_code_exists(self):
        """Statement: Clear discount when voucher_code exists"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="TEST_VOUCHER"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.discounts = []
        lines_info = []
        
        with patch('saleor.discount.utils.checkout._clear_checkout_discount') as mock_clear:
            result = create_checkout_discount_objects_for_order_promotions(
                checkout_info, lines_info
            )
            
            mock_clear.assert_called_once()
            assert result is None

    def test_create_checkout_discount_clears_when_no_promotion_applied(self):
        """Statement: Clear discount when no promotion applied"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        checkout_info.discounts = []
        checkout_info.get_country.return_value = "US"
        lines_info = []
        
        with patch('saleor.discount.utils.checkout._set_checkout_base_prices'):
            with patch('saleor.discount.utils.checkout.create_discount_objects_for_order_promotions', return_value=(False, None, None)):
                with patch('saleor.discount.utils.checkout._clear_checkout_discount') as mock_clear:
                    result = create_checkout_discount_objects_for_order_promotions(
                        checkout_info, lines_info
                    )
                    
                    mock_clear.assert_called_once()
                    assert result is None


@pytest.mark.django_db
class TestSetCheckoutBasePrices:
    """Test _set_checkout_base_prices()"""

    def test_set_checkout_base_prices_updates_when_different(self):
        """Statement: Update checkout base prices when different"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            base_subtotal_amount=Decimal("100.00"),
            base_total_amount=Decimal("110.00")
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.base_checkout_subtotal', return_value=Money(Decimal("90.00"), "USD")):
            with patch('saleor.discount.utils.checkout.base_checkout_delivery_price', return_value=Money(Decimal("10.00"), "USD")):
                _set_checkout_base_prices(checkout_info, lines_info)
                
                checkout.refresh_from_db()
                assert checkout.base_subtotal_amount == Decimal("90.00")
                assert checkout.base_total_amount == Decimal("100.00")

    def test_set_checkout_base_prices_skips_when_same(self):
        """Statement: Skip update when prices are same"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            base_subtotal_amount=Decimal("100.00"),
            base_total_amount=Decimal("110.00")
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.base_checkout_subtotal', return_value=Money(Decimal("100.00"), "USD")):
            with patch('saleor.discount.utils.checkout.base_checkout_delivery_price', return_value=Money(Decimal("10.00"), "USD")):
                _set_checkout_base_prices(checkout_info, lines_info)
                
                # Should not update since values are same
                checkout.refresh_from_db()
                assert checkout.base_subtotal_amount == Decimal("100.00")
                assert checkout.base_total_amount == Decimal("110.00")


@pytest.mark.django_db
class TestClearCheckoutDiscount:
    """Test _clear_checkout_discount()"""

    def test_clear_checkout_discount_deletes_order_promotion_discounts(self):
        """Statement: Delete order promotion discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        discount = CheckoutDiscount.objects.create(
            checkout=checkout,
            type=DiscountType.ORDER_PROMOTION,
            value_type=DiscountValueType.FIXED,
            value=Decimal("10.00"),
            amount_value=Decimal("10.00"),
            currency="USD"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.discounts = [discount]
        checkout_info.voucher_code = None
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.delete_gift_line'):
            _clear_checkout_discount(checkout_info, lines_info, save=False)
            
            assert not CheckoutDiscount.objects.filter(id=discount.id).exists()

    def test_clear_checkout_discount_clears_voucher_fields(self):
        """Statement: Clear voucher fields when no voucher code"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("10.00"),
            discount_name="Test Discount"
        )
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.discounts = []
        checkout_info.voucher_code = None
        lines_info = []
        
        with patch('saleor.discount.utils.checkout.delete_gift_line'):
            _clear_checkout_discount(checkout_info, lines_info, save=True)
            
            checkout.refresh_from_db()
            assert checkout.discount_amount == Decimal("0.00")
            assert checkout.discount_name == ""

