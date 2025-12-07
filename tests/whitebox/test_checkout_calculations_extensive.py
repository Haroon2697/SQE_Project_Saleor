"""
Extensive White-Box Tests for saleor/checkout/calculations.py

Target: Increase checkout calculations coverage from 18% to 80%+
Covers: 214 uncovered statements
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from django.utils import timezone
from datetime import timedelta
from prices import Money, TaxedMoney

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.calculations import (
    checkout_shipping_price,
    checkout_shipping_tax_rate,
    checkout_subtotal,
    calculate_checkout_total,
    calculate_checkout_total_with_gift_cards,
    checkout_line_total,
    checkout_line_unit_price,
    checkout_line_tax_rate,
    checkout_line_undiscounted_unit_price,
    checkout_line_undiscounted_total_price,
    update_undiscounted_unit_price_for_lines,
    update_prior_unit_price_for_lines,
    fetch_checkout_data,
    recalculate_discounts,
)
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductVariant, ProductType, Category
from saleor.account.models import Address
from saleor.checkout.fetch import CheckoutInfo, CheckoutLineInfo
from saleor.core.taxes import zero_taxed_money, zero_money
from saleor.tax import TaxCalculationStrategy


@pytest.mark.django_db
class TestCheckoutShippingPrice:
    """Test checkout_shipping_price()"""

    def test_checkout_shipping_price_with_valid_checkout(self):
        """Statement: Return shipping price with valid checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            shipping_price=TaxedMoney(Money("10.00", "USD"), Money("10.00", "USD")),
            price_expiration=timezone.now() + timedelta(hours=1)
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        address = None
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_shipping_price(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=address
            )
            
            assert result.currency == "USD"
            mock_fetch.assert_called_once()

    def test_checkout_shipping_price_with_pregenerated_payloads(self):
        """Statement: Handle pregenerated subscription payloads"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            shipping_price=TaxedMoney(Money("10.00", "USD"), Money("10.00", "USD"))
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        payloads = {"test": "data"}
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            checkout_shipping_price(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=None,
                pregenerated_subscription_payloads=payloads
            )
            
            assert mock_fetch.called
            call_kwargs = mock_fetch.call_args[1]
            assert call_kwargs.get('pregenerated_subscription_payloads') == payloads


@pytest.mark.django_db
class TestCheckoutShippingTaxRate:
    """Test checkout_shipping_tax_rate()"""

    def test_checkout_shipping_tax_rate_returns_tax_rate(self):
        """Statement: Return shipping tax rate"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            shipping_tax_rate=Decimal("0.20")
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_shipping_tax_rate(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=None
            )
            
            assert result == Decimal("0.20")


@pytest.mark.django_db
class TestCheckoutSubtotal:
    """Test checkout_subtotal()"""

    def test_checkout_subtotal_returns_subtotal(self):
        """Statement: Return checkout subtotal"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            subtotal=TaxedMoney(Money("100.00", "USD"), Money("100.00", "USD"))
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_subtotal(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=None
            )
            
            assert result.currency == "USD"
            assert result.gross == Money("100.00", "USD")


@pytest.mark.django_db
class TestCalculateCheckoutTotal:
    """Test calculate_checkout_total()"""

    def test_calculate_checkout_total_returns_total(self):
        """Statement: Return checkout total"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            total=TaxedMoney(Money("150.00", "USD"), Money("150.00", "USD"))
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = calculate_checkout_total(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=None
            )
            
            assert result.currency == "USD"
            assert result.gross == Money("150.00", "USD")

    def test_calculate_checkout_total_with_force_update(self):
        """Statement: Force update when force_update=True"""
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
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            calculate_checkout_total(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                address=None,
                force_update=True
            )
            
            call_kwargs = mock_fetch.call_args[1]
            assert call_kwargs.get('force_update') is True


@pytest.mark.django_db
class TestCalculateCheckoutTotalWithGiftCards:
    """Test calculate_checkout_total_with_gift_cards()"""

    def test_calculate_checkout_total_with_gift_cards_zero_total(self):
        """Statement: Return zero when total is zero"""
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
        checkout_info = Mock()
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.calculations.calculate_checkout_total') as mock_calc:
            mock_calc.return_value = zero_taxed_money("USD")
            result = calculate_checkout_total_with_gift_cards(
                manager=manager,
                checkout_info=checkout_info,
                lines=[],
                address=None
            )
            
            assert result == zero_taxed_money("USD")

    def test_calculate_checkout_total_with_gift_cards_subtracts_balance(self):
        """Statement: Subtract gift card balance from total"""
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
        checkout_info = Mock()
        checkout_info.checkout = checkout
        
        def mock_get_total_gift_cards_balance(db_name):
            return Money("20.00", "USD")
        
        checkout.get_total_gift_cards_balance = mock_get_total_gift_cards_balance
        
        with patch('saleor.checkout.calculations.calculate_checkout_total') as mock_calc:
            total = TaxedMoney(Money("100.00", "USD"), Money("100.00", "USD"))
            mock_calc.return_value = total
            
            result = calculate_checkout_total_with_gift_cards(
                manager=manager,
                checkout_info=checkout_info,
                lines=[],
                address=None
            )
            
            assert result.gross == Money("80.00", "USD")

    def test_calculate_checkout_total_with_gift_cards_prevents_negative(self):
        """Statement: Prevent negative gross value"""
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
        checkout_info = Mock()
        checkout_info.checkout = checkout
        
        def mock_get_total_gift_cards_balance(db_name):
            return Money("150.00", "USD")
        
        checkout.get_total_gift_cards_balance = mock_get_total_gift_cards_balance
        
        with patch('saleor.checkout.calculations.calculate_checkout_total') as mock_calc:
            total = TaxedMoney(Money("100.00", "USD"), Money("100.00", "USD"))
            mock_calc.return_value = total
            
            result = calculate_checkout_total_with_gift_cards(
                manager=manager,
                checkout_info=checkout_info,
                lines=[],
                address=None
            )
            
            assert result.gross == zero_money("USD")


@pytest.mark.django_db
class TestCheckoutLineTotal:
    """Test checkout_line_total()"""

    def test_checkout_line_total_returns_line_total(self):
        """Statement: Return line total price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            total_price=TaxedMoney(Money("20.00", "USD"), Money("20.00", "USD"))
        )
        
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        line_info = Mock()
        line_info.line = line
        lines = [line_info]
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_line_total(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                checkout_line_info=line_info
            )
            
            assert result.currency == "USD"
            assert result.gross == Money("20.00", "USD")


@pytest.mark.django_db
class TestCheckoutLineUnitPrice:
    """Test checkout_line_unit_price()"""

    def test_checkout_line_unit_price_calculates_from_total(self):
        """Statement: Calculate unit price from total"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            total_price=TaxedMoney(Money("20.00", "USD"), Money("20.00", "USD"))
        )
        
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        line_info = Mock()
        line_info.line = line
        lines = [line_info]
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_line_unit_price(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                checkout_line_info=line_info
            )
            
            assert result.currency == "USD"
            assert result.gross == Money("10.00", "USD")  # 20.00 / 2


@pytest.mark.django_db
class TestCheckoutLineTaxRate:
    """Test checkout_line_tax_rate()"""

    def test_checkout_line_tax_rate_returns_tax_rate(self):
        """Statement: Return line tax rate"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            tax_rate=Decimal("0.20")
        )
        
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        line_info = Mock()
        line_info.line = line
        lines = [line_info]
        
        with patch('saleor.checkout.calculations.fetch_checkout_data') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = checkout_line_tax_rate(
                manager=manager,
                checkout_info=checkout_info,
                lines=lines,
                checkout_line_info=line_info
            )
            
            assert result == Decimal("0.20")


@pytest.mark.django_db
class TestCheckoutLineUndiscountedPrices:
    """Test undiscounted price functions"""

    def test_checkout_line_undiscounted_unit_price_from_expired_prices(self):
        """Statement: Calculate from base when prices expired"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            price_expiration=timezone.now() - timedelta(hours=1)
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        checkout_info = Mock()
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        line_info = Mock()
        line_info.line = line
        
        with patch('saleor.checkout.base_calculations.calculate_undiscounted_base_line_unit_price') as mock_calc:
            mock_calc.return_value = Money("15.00", "USD")
            result = checkout_line_undiscounted_unit_price(
                checkout_info=checkout_info,
                checkout_line_info=line_info
            )
            
            mock_calc.assert_called_once()
            assert result == Money("15.00", "USD")

    def test_checkout_line_undiscounted_unit_price_from_valid_prices(self):
        """Statement: Return from line when prices valid"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            price_expiration=timezone.now() + timedelta(hours=1)
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            undiscounted_unit_price=TaxedMoney(Money("12.00", "USD"), Money("12.00", "USD"))
        )
        
        checkout_info = Mock()
        checkout_info.checkout = checkout
        line_info = Mock()
        line_info.line = line
        
        result = checkout_line_undiscounted_unit_price(
            checkout_info=checkout_info,
            checkout_line_info=line_info
        )
        
        assert result.gross == Money("12.00", "USD")

    def test_checkout_line_undiscounted_total_price_calculates_total(self):
        """Statement: Calculate total from unit price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3
        )
        
        checkout_info = Mock()
        checkout_info.checkout = checkout
        line_info = Mock()
        line_info.line = line
        
        with patch('saleor.checkout.calculations.checkout_line_undiscounted_unit_price') as mock_unit:
            mock_unit.return_value = TaxedMoney(Money("10.00", "USD"), Money("10.00", "USD"))
            result = checkout_line_undiscounted_total_price(
                checkout_info=checkout_info,
                checkout_line_info=line_info
            )
            
            assert result.gross == Money("30.00", "USD")  # 10.00 * 3


@pytest.mark.django_db
class TestUpdateUndiscountedPriceForLines:
    """Test update_undiscounted_unit_price_for_lines()"""

    def test_update_undiscounted_unit_price_for_lines_updates_all_lines(self):
        """Statement: Update all lines with channel listing"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        line_info = Mock()
        line_info.line = line
        channel_listing = Mock()
        channel_listing.price = Money("10.00", "USD")
        line_info.channel_listing = channel_listing
        line_info.undiscounted_unit_price = TaxedMoney(Money("10.00", "USD"), Money("10.00", "USD"))
        
        update_undiscounted_unit_price_for_lines([line_info])
        
        assert line.undiscounted_unit_price.gross == Money("10.00", "USD")

    def test_update_undiscounted_unit_price_for_lines_skips_missing_listing(self):
        """Statement: Skip lines without channel listing"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = None
        
        # Should not raise error
        update_undiscounted_unit_price_for_lines([line_info])


@pytest.mark.django_db
class TestUpdatePriorPriceForLines:
    """Test update_prior_unit_price_for_lines()"""

    def test_update_prior_unit_price_for_lines_with_prior_price(self):
        """Statement: Update prior price when listing has prior price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        line_info = Mock()
        line_info.line = line
        channel_listing = Mock()
        channel_listing.prior_price_amount = Decimal("15.00")
        line_info.channel_listing = channel_listing
        line_info.prior_unit_price_amount = Decimal("15.00")
        
        update_prior_unit_price_for_lines([line_info])
        
        assert line.prior_unit_price_amount == Decimal("15.00")

    def test_update_prior_unit_price_for_lines_without_prior_price(self):
        """Statement: Set to None when no prior price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        line_info = Mock()
        line_info.line = line
        channel_listing = Mock()
        channel_listing.prior_price_amount = None
        line_info.channel_listing = channel_listing
        
        update_prior_unit_price_for_lines([line_info])
        
        assert line.prior_unit_price_amount is None

    def test_update_prior_unit_price_for_lines_skips_missing_listing(self):
        """Statement: Skip lines without channel listing"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        product_type = ProductType.objects.create(name="Test Type")
        product = Product.objects.create(
            name="Test Product",
            product_type=product_type
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-SKU"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1
        )
        
        line_info = Mock()
        line_info.line = line
        line_info.channel_listing = None
        
        # Should not raise error
        update_prior_unit_price_for_lines([line_info])


@pytest.mark.django_db
class TestFetchCheckoutData:
    """Test fetch_checkout_data() - Main function"""

    def test_fetch_checkout_data_with_force_update(self):
        """Statement: Force update when force_update=True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            price_expiration=timezone.now() + timedelta(hours=1)
        )
        manager = Mock()
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations._fetch_checkout_prices_if_expired') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            result = fetch_checkout_data(
                checkout_info=checkout_info,
                manager=manager,
                lines=lines,
                force_update=True
            )
            
            call_kwargs = mock_fetch.call_args[1]
            assert call_kwargs.get('force_update') is True

    def test_fetch_checkout_data_with_database_connection(self):
        """Statement: Use specified database connection"""
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
        checkout_info = Mock()
        checkout_info.checkout = checkout
        lines = []
        
        with patch('saleor.checkout.calculations._fetch_checkout_prices_if_expired') as mock_fetch:
            mock_fetch.return_value = (checkout_info, lines)
            fetch_checkout_data(
                checkout_info=checkout_info,
                manager=manager,
                lines=lines,
                database_connection_name="replica"
            )
            
            call_kwargs = mock_fetch.call_args[1]
            assert call_kwargs.get('database_connection_name') == "replica"

