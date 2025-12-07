"""
Comprehensive White-Box Tests for saleor/checkout/complete_checkout.py

Target: Increase coverage from 15% to 80%+
Focusing on critical checkout completion functions:
- complete_checkout
- complete_checkout_with_payment
- complete_checkout_with_transaction
- create_order_from_checkout
- assign_checkout_user
- _process_voucher_data_for_order
- _create_order_from_checkout
- _create_lines_for_order
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from uuid import uuid4

from saleor.checkout.complete_checkout import (
    complete_checkout,
    complete_checkout_with_payment,
    complete_checkout_with_transaction,
    create_order_from_checkout,
    assign_checkout_user,
    _process_voucher_data_for_order,
    _increase_checkout_voucher_usage,
    _release_checkout_voucher_usage,
    _process_shipping_data_for_order,
    _process_user_data_for_order,
    _create_lines_for_order,
    _prepare_order_data,
    _create_order,
    _get_order_data,
    _create_order_discount,
    _post_create_order_actions,
)
from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.fetch import CheckoutInfo, CheckoutLineInfo
from saleor.order.models import Order, OrderLine
from saleor.order.fetch import OrderInfo, OrderLineInfo
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.plugins.manager import PluginsManager, get_plugins_manager
from saleor.account.models import User, Address
from saleor.payment.models import Payment, Transaction
from saleor.discount.models import Voucher, VoucherCode
from saleor.warehouse.models import Warehouse, Stock
from saleor.core.exceptions import GiftCardNotApplicable, InsufficientStock
from django.core.exceptions import ValidationError
from prices import Money, TaxedMoney


@pytest.mark.django_db
class TestProcessVoucherDataForOrder:
    """Test _process_voucher_data_for_order()"""
    
    def test_process_voucher_data_with_valid_voucher(self):
        """Statement: Process valid voucher data"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        voucher = Voucher.objects.create(
            code="TESTVOUCHER",
            discount_value_type="PERCENTAGE",
            discount_value=10
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTVOUCHER"
        )
        checkout.voucher_code = voucher_code.code
        checkout.save()
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.complete_checkout.get_voucher_for_checkout_info') as mock_get:
            with patch('saleor.checkout.complete_checkout._increase_checkout_voucher_usage') as mock_increase:
                with patch('saleor.checkout.complete_checkout.get_customer_email_for_voucher_usage') as mock_email:
                    mock_get.return_value = (voucher, voucher_code)
                    mock_email.return_value = "test@example.com"
                    
                    result = _process_voucher_data_for_order(checkout_info)
                    
                    assert "voucher" in result
                    assert "voucher_code" in result
                    assert result["voucher"] == voucher
                    assert result["voucher_code"] == voucher_code.code
    
    def test_process_voucher_data_without_voucher(self):
        """Statement: Return empty dict when no voucher"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.complete_checkout.get_voucher_for_checkout_info') as mock_get:
            mock_get.return_value = (None, None)
            
            result = _process_voucher_data_for_order(checkout_info)
            
            assert result == {}


@pytest.mark.django_db
class TestAssignCheckoutUser:
    """Test assign_checkout_user()"""
    
    def test_assign_checkout_user_with_existing_user(self):
        """Statement: Assign checkout to existing user"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        user = User.objects.create_user(
            email="test@example.com",
            password="password"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.complete_checkout.retrieve_user_by_email') as mock_retrieve:
            mock_retrieve.return_value = user
            
            assign_checkout_user(user, checkout_info)
            
            assert checkout_info.checkout.user == user
    
    def test_assign_checkout_user_with_no_user(self):
        """Statement: Handle None user"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        assign_checkout_user(None, checkout_info)
        
        # Should not raise error
        assert True


@pytest.mark.django_db
class TestCreateOrderFromCheckout:
    """Test create_order_from_checkout()"""
    
    def test_create_order_from_checkout_basic(self):
        """Statement: Create order from checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST",
            track_inventory=True
        )
        stock = Stock.objects.create(
            product_variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        checkout_line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        manager = get_plugins_manager(allow_replica=False)
        
        with patch('saleor.checkout.complete_checkout.fetch_checkout_lines') as mock_fetch_lines:
            with patch('saleor.checkout.complete_checkout.fetch_checkout_info') as mock_fetch_info:
                with patch('saleor.checkout.complete_checkout._create_order_from_checkout') as mock_create:
                    checkout_lines = [Mock(spec=CheckoutLineInfo)]
                    checkout_info = Mock(spec=CheckoutInfo)
                    checkout_info.checkout = checkout
                    checkout_info.channel = channel
                    
                    mock_fetch_lines.return_value = (checkout_lines, [])
                    mock_fetch_info.return_value = checkout_info
                    
                    order = Order.objects.create(
                        channel=channel,
                        currency="USD",
                        status="DRAFT"
                    )
                    mock_create.return_value = order
                    
                    result = create_order_from_checkout(
                        checkout_info=checkout_info,
                        manager=manager,
                        user=None,
                        app=None,
                        delete_checkout=False
                    )
                    
                    assert result == order


@pytest.mark.django_db
class TestCompleteCheckout:
    """Test complete_checkout()"""
    
    def test_complete_checkout_zero_amount(self):
        """Statement: Complete checkout with zero amount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com",
            authorize_status="FULL"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        lines = []
        manager = get_plugins_manager(allow_replica=False)
        
        with patch('saleor.checkout.complete_checkout.fetch_checkout_data') as mock_fetch:
            with patch('saleor.checkout.complete_checkout.create_order_from_checkout') as mock_create:
                mock_create.return_value = Order.objects.create(
                    channel=channel,
                    currency="USD"
                )
                
                # Mock checkout.total to return zero
                with patch.object(checkout, 'total', new_callable=PropertyMock) as mock_total:
                    mock_total.return_value = TaxedMoney(
                        net=Money(Decimal('0'), 'USD'),
                        gross=Money(Decimal('0'), 'USD')
                    )
                    
                    result = complete_checkout(
                        manager=manager,
                        checkout_info=checkout_info,
                        lines=lines,
                        payment_data={},
                        store_source=False,
                        user=None,
                        app=None
                    )
                    
                    assert result[0] is not None  # Order created


@pytest.mark.django_db
class TestCompleteCheckoutWithPayment:
    """Test complete_checkout_with_payment()"""
    
    def test_complete_checkout_with_payment_checkout_not_found(self):
        """Statement: Handle checkout not found - return existing order"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout_pk = uuid4()
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        manager = get_plugins_manager(allow_replica=False)
        
        with patch('saleor.checkout.complete_checkout.Checkout.objects.select_for_update') as mock_select:
            mock_select.return_value.filter.return_value.first.return_value = None
            
            with patch('saleor.checkout.complete_checkout.Order.objects.get_by_checkout_token') as mock_get:
                mock_get.return_value = order
                
                result = complete_checkout_with_payment(
                    manager=manager,
                    checkout_pk=checkout_pk,
                    payment_data={},
                    store_source=False,
                    user=None,
                    app=None
                )
                
                assert result[0] == order
                assert result[1] == False  # action_required
                assert result[2] == {}  # action_data


@pytest.mark.django_db
class TestProcessShippingDataForOrder:
    """Test _process_shipping_data_for_order()"""
    
    def test_process_shipping_data_with_shipping_method(self):
        """Statement: Process shipping method data"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.shipping_method = Mock()
        checkout_info.shipping_method.name = "Test Shipping"
        
        manager = get_plugins_manager(allow_replica=False)
        
        result = _process_shipping_data_for_order(checkout_info, manager)
        
        assert "shipping_method_name" in result
        assert result["shipping_method_name"] == "Test Shipping"


@pytest.mark.django_db
class TestProcessUserDataForOrder:
    """Test _process_user_data_for_order()"""
    
    def test_process_user_data_with_user(self):
        """Statement: Process user data"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        user = User.objects.create_user(
            email="test@example.com",
            password="password"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com",
            user=user
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        manager = get_plugins_manager(allow_replica=False)
        
        with patch('saleor.checkout.complete_checkout.store_user_address') as mock_store:
            result = _process_user_data_for_order(checkout_info, manager)
            
            assert "user_email" in result
            assert result["user_email"] == "test@example.com"


@pytest.mark.django_db
class TestCreateOrderDiscount:
    """Test _create_order_discount()"""
    
    def test_create_order_discount_with_voucher(self):
        """Statement: Create order discount from voucher"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            code="TESTVOUCHER",
            discount_value_type="PERCENTAGE",
            discount_value=10
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.voucher = voucher
        checkout_info.checkout = Mock()
        checkout_info.checkout.discount_amount = Decimal('10.00')
        
        result = _create_order_discount(order, checkout_info)
        
        assert result is not None
        assert result.order == order
        assert result.voucher == voucher


@pytest.mark.django_db
class TestPostCreateOrderActions:
    """Test _post_create_order_actions()"""
    
    def test_post_create_order_actions(self):
        """Statement: Execute post-create order actions"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        order = Order.objects.create(
            channel=channel,
            currency="USD"
        )
        
        manager = get_plugins_manager(allow_replica=False)
        
        with patch('saleor.checkout.complete_checkout.order_created') as mock_order_created:
            with patch('saleor.checkout.complete_checkout.send_order_confirmation') as mock_send:
                _post_create_order_actions(
                    order=order,
                    manager=manager,
                    user=None,
                    app=None,
                    site_settings=None
                )
                
                mock_order_created.assert_called_once()


@pytest.mark.django_db
class TestIncreaseCheckoutVoucherUsage:
    """Test _increase_checkout_voucher_usage()"""
    
    def test_increase_voucher_usage_already_increased(self):
        """Statement: Skip if voucher usage already increased"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com",
            is_voucher_usage_increased=True
        )
        voucher = Voucher.objects.create(
            code="TESTVOUCHER",
            discount_value_type="PERCENTAGE",
            discount_value=10
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTVOUCHER"
        )
        
        with patch('saleor.checkout.complete_checkout.increase_voucher_usage') as mock_increase:
            _increase_checkout_voucher_usage(
                checkout=checkout,
                voucher_code=voucher_code,
                voucher=voucher,
                customer_email="test@example.com"
            )
            
            # Should not call increase_voucher_usage if already increased
            mock_increase.assert_not_called()
    
    def test_increase_voucher_usage_first_time(self):
        """Statement: Increase voucher usage first time"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com",
            is_voucher_usage_increased=False
        )
        voucher = Voucher.objects.create(
            code="TESTVOUCHER",
            discount_value_type="PERCENTAGE",
            discount_value=10
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTVOUCHER"
        )
        
        with patch('saleor.checkout.complete_checkout.increase_voucher_usage') as mock_increase:
            _increase_checkout_voucher_usage(
                checkout=checkout,
                voucher_code=voucher_code,
                voucher=voucher,
                customer_email="test@example.com"
            )
            
            mock_increase.assert_called_once()
            checkout.refresh_from_db()
            assert checkout.is_voucher_usage_increased == True


@pytest.mark.django_db
class TestReleaseCheckoutVoucherUsage:
    """Test _release_checkout_voucher_usage()"""
    
    def test_release_voucher_usage(self):
        """Statement: Release voucher usage"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            email="test@example.com",
            is_voucher_usage_increased=True
        )
        voucher = Voucher.objects.create(
            code="TESTVOUCHER",
            discount_value_type="PERCENTAGE",
            discount_value=10
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTVOUCHER"
        )
        
        with patch('saleor.checkout.complete_checkout.release_voucher_code_usage') as mock_release:
            _release_checkout_voucher_usage(
                checkout=checkout,
                voucher_code=voucher_code,
                voucher=voucher,
                customer_email="test@example.com"
            )
            
            mock_release.assert_called_once()
            checkout.refresh_from_db()
            assert checkout.is_voucher_usage_increased == False

