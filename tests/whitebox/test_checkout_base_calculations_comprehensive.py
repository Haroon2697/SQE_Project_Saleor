"""
Comprehensive White-Box Tests for saleor/checkout/base_calculations.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- calculate_base_line_unit_price
- calculate_base_line_total_price
- calculate_undiscounted_base_line_total_price
- calculate_undiscounted_base_line_unit_price
- base_checkout_delivery_price
- base_checkout_undiscounted_delivery_price
- calculate_base_price_for_shipping_method
- base_checkout_total
- base_checkout_subtotal
- checkout_total
- get_line_total_price_with_propagated_checkout_discount
- _propagate_checkout_discount_on_checkout_lines_prices
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money, TaxedMoney

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.base_calculations import (
    calculate_base_line_unit_price,
    calculate_base_line_total_price,
    calculate_undiscounted_base_line_total_price,
    calculate_undiscounted_base_line_unit_price,
    base_checkout_delivery_price,
    base_checkout_undiscounted_delivery_price,
    calculate_base_price_for_shipping_method,
    base_checkout_total,
    base_checkout_subtotal,
    checkout_total,
    get_line_total_price_with_propagated_checkout_discount,
    _propagate_checkout_discount_on_checkout_lines_prices,
)
from saleor.checkout.fetch import CheckoutInfo, CheckoutLineInfo, ShippingMethodInfo
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.shipping.models import ShippingMethod, ShippingMethodChannelListing
from saleor.discount.models import Voucher, VoucherType
from saleor.discount.utils.voucher import calculate_line_discount_amount_from_voucher


@pytest.mark.django_db
class TestCalculateBaseLineUnitPrice:
    """Test calculate_base_line_unit_price() - Statement Coverage"""
    
    def test_calculate_base_line_unit_price_divides_total_by_quantity(self):
        """Statement: total_line_price / quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3,
            currency="USD"
        )
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        with patch('saleor.checkout.base_calculations.calculate_base_line_total_price') as mock_total:
            mock_total.return_value = Money(Decimal("27.00"), "USD")
            result = calculate_base_line_unit_price(line_info)
            assert result == Money(Decimal("9.00"), "USD")  # 27 / 3


@pytest.mark.django_db
class TestCalculateBaseLineTotalPrice:
    """Test calculate_base_line_total_price() - Statement, Decision, MC/DC Coverage"""
    
    def test_calculate_base_line_total_price_no_discounts_no_voucher(self):
        """Statement: variant_price * quantity with no discounts"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            currency="USD"
        )
        
        line.undiscounted_unit_price_amount = Decimal("10.00")
        line.save()
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            rules_info=[],
            channel=channel,
            voucher=None,
            voucher_code=None,
            tax_class=None
        )
        
        result = calculate_base_line_total_price(line_info)
        assert result == Money(Decimal("20.00"), "USD")  # 10 * 2
    
    def test_calculate_base_line_total_price_with_discounts(self):
        """Statement: Subtract discount amounts from total_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            currency="USD"
        )
        
        discount1 = Mock()
        discount1.amount_value = Decimal("2.00")
        discount2 = Mock()
        discount2.amount_value = Decimal("1.00")
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[discount1, discount2],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        result = calculate_base_line_total_price(line_info, include_voucher=True)
        assert result == Money(Decimal("17.00"), "USD")  # 20 - 2 - 1
    
    def test_calculate_base_line_total_price_with_voucher_include_true(self):
        """Decision: include_voucher=True and voucher exists -> subtract voucher discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            currency="USD"
        )
        
        voucher = Mock()
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=voucher,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        with patch('saleor.checkout.base_calculations.calculate_line_discount_amount_from_voucher') as mock_voucher:
            mock_voucher.return_value = Money(Decimal("3.00"), "USD")
            result = calculate_base_line_total_price(line_info, include_voucher=True)
            assert result == Money(Decimal("17.00"), "USD")  # 20 - 3
            mock_voucher.assert_called_once()
    
    def test_calculate_base_line_total_price_with_voucher_include_false(self):
        """Decision: include_voucher=False -> don't subtract voucher discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            currency="USD"
        )
        
        voucher = Mock()
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=voucher,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        with patch('saleor.checkout.base_calculations.calculate_line_discount_amount_from_voucher') as mock_voucher:
            result = calculate_base_line_total_price(line_info, include_voucher=False)
            assert result == Money(Decimal("20.00"), "USD")  # No voucher discount
            mock_voucher.assert_not_called()


@pytest.mark.django_db
class TestCalculateUndiscountedBaseLineTotalPrice:
    """Test calculate_undiscounted_base_line_total_price() - Statement Coverage"""
    
    def test_calculate_undiscounted_base_line_total_price(self):
        """Statement: unit_price * quantity"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=3,
            currency="USD"
        )
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        with patch('saleor.checkout.base_calculations.calculate_undiscounted_base_line_unit_price') as mock_unit:
            mock_unit.return_value = Money(Decimal("10.00"), "USD")
            result = calculate_undiscounted_base_line_total_price(line_info, channel)
            assert result == Money(Decimal("30.00"), "USD")  # 10 * 3


@pytest.mark.django_db
class TestCalculateUndiscountedBaseLineUnitPrice:
    """Test calculate_undiscounted_base_line_unit_price() - Statement Coverage"""
    
    def test_calculate_undiscounted_base_line_unit_price(self):
        """Statement: Return quantized variant_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.50"), "USD")
        )
        
        result = calculate_undiscounted_base_line_unit_price(line_info, channel)
        assert result == Money(Decimal("10.50"), "USD")


@pytest.mark.django_db
class TestBaseCheckoutDeliveryPrice:
    """Test base_checkout_delivery_price() - Statement, Decision, MC/DC Coverage"""
    
    def test_base_checkout_delivery_price_no_shipping_voucher(self):
        """Decision: No shipping voucher -> return undiscounted_delivery_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = None
        
        with patch('saleor.checkout.base_calculations.base_checkout_undiscounted_delivery_price') as mock_undiscounted:
            mock_undiscounted.return_value = Money(Decimal("10.00"), "USD")
            result = base_checkout_delivery_price(checkout_info, lines=None, include_voucher=True)
            assert result == Money(Decimal("10.00"), "USD")
    
    def test_base_checkout_delivery_price_shipping_voucher_include_true(self):
        """Decision: Shipping voucher + include_voucher=True -> subtract discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("2.00")
        )
        
        voucher = Mock()
        voucher.type = VoucherType.SHIPPING
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = voucher
        
        with patch('saleor.checkout.base_calculations.base_checkout_undiscounted_delivery_price') as mock_undiscounted:
            mock_undiscounted.return_value = Money(Decimal("10.00"), "USD")
            result = base_checkout_delivery_price(checkout_info, lines=None, include_voucher=True)
            assert result == Money(Decimal("8.00"), "USD")  # 10 - 2
    
    def test_base_checkout_delivery_price_shipping_voucher_include_false(self):
        """Decision: Shipping voucher + include_voucher=False -> don't subtract discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("2.00")
        )
        
        voucher = Mock()
        voucher.type = VoucherType.SHIPPING
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = voucher
        
        with patch('saleor.checkout.base_calculations.base_checkout_undiscounted_delivery_price') as mock_undiscounted:
            mock_undiscounted.return_value = Money(Decimal("10.00"), "USD")
            result = base_checkout_delivery_price(checkout_info, lines=None, include_voucher=False)
            assert result == Money(Decimal("10.00"), "USD")  # No discount applied
    
    def test_base_checkout_delivery_price_shipping_voucher_discount_exceeds_price(self):
        """Decision: Discount > shipping_price -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            discount_amount=Decimal("15.00")
        )
        
        voucher = Mock()
        voucher.type = VoucherType.SHIPPING
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = voucher
        
        with patch('saleor.checkout.base_calculations.base_checkout_undiscounted_delivery_price') as mock_undiscounted:
            mock_undiscounted.return_value = Money(Decimal("10.00"), "USD")
            result = base_checkout_delivery_price(checkout_info, lines=None, include_voucher=True)
            assert result == Money(Decimal("0.00"), "USD")  # max(0, 10 - 15)


@pytest.mark.django_db
class TestBaseCheckoutUndiscountedDeliveryPrice:
    """Test base_checkout_undiscounted_delivery_price() - Statement, Decision Coverage"""
    
    def test_base_checkout_undiscounted_delivery_price_not_shipping_method_info(self):
        """Decision: Not ShippingMethodInfo -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.get_delivery_method_info.return_value = None  # Not ShippingMethodInfo
        
        result = base_checkout_undiscounted_delivery_price(checkout_info, lines=None)
        assert result == Money(Decimal("0.00"), "USD")
    
    def test_base_checkout_undiscounted_delivery_price_shipping_method_info(self):
        """Decision: ShippingMethodInfo -> call calculate_base_price_for_shipping_method"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        shipping_method_info = Mock(spec=ShippingMethodInfo)
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.get_delivery_method_info.return_value = shipping_method_info
        
        with patch('saleor.checkout.base_calculations.calculate_base_price_for_shipping_method') as mock_calc:
            mock_calc.return_value = Money(Decimal("10.00"), "USD")
            result = base_checkout_undiscounted_delivery_price(checkout_info, lines=None)
            assert result == Money(Decimal("10.00"), "USD")
            mock_calc.assert_called_once()


@pytest.mark.django_db
class TestCalculateBasePriceForShippingMethod:
    """Test calculate_base_price_for_shipping_method() - Statement, Decision, MC/DC Coverage"""
    
    def test_calculate_base_price_no_shipping_method(self):
        """Decision: shipping_method is None -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        shipping_method_info = Mock(spec=ShippingMethodInfo)
        shipping_method_info.delivery_method = None
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        result = calculate_base_price_for_shipping_method(
            checkout_info, shipping_method_info, lines=None
        )
        assert result == Money(Decimal("0.00"), "USD")
    
    def test_calculate_base_price_shipping_not_required(self):
        """Decision: shipping_required=False -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        shipping_method = ShippingMethod.objects.create(name="Standard")
        shipping_method_info = Mock(spec=ShippingMethodInfo)
        shipping_method_info.delivery_method = shipping_method
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.base_calculations.is_shipping_required', return_value=False):
            result = calculate_base_price_for_shipping_method(
                checkout_info, shipping_method_info, lines=None
            )
            assert result == Money(Decimal("0.00"), "USD")
    
    def test_calculate_base_price_shipping_required_with_method(self):
        """Decision: shipping_method exists + shipping_required=True -> return method price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        shipping_method = ShippingMethod.objects.create(name="Standard")
        shipping_method.price = Money(Decimal("10.00"), "USD")
        shipping_method_info = Mock(spec=ShippingMethodInfo)
        shipping_method_info.delivery_method = shipping_method
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        with patch('saleor.checkout.base_calculations.is_shipping_required', return_value=True):
            result = calculate_base_price_for_shipping_method(
                checkout_info, shipping_method_info, lines=None
            )
            assert result == Money(Decimal("10.00"), "USD")
    
    def test_calculate_base_price_uses_lines_for_shipping_required(self):
        """Decision: lines provided -> use is_shipping_required(lines)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        shipping_method = ShippingMethod.objects.create(name="Standard")
        shipping_method.price = Money(Decimal("10.00"), "USD")
        shipping_method_info = Mock(spec=ShippingMethodInfo)
        shipping_method_info.delivery_method = shipping_method
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.base_calculations.is_shipping_required', return_value=True) as mock_check:
            result = calculate_base_price_for_shipping_method(
                checkout_info, shipping_method_info, lines=lines
            )
            assert result == Money(Decimal("10.00"), "USD")
            mock_check.assert_called_once_with(lines)


@pytest.mark.django_db
class TestBaseCheckoutTotal:
    """Test base_checkout_total() - Statement Coverage"""
    
    def test_base_checkout_total_sums_subtotal_and_shipping(self):
        """Statement: Return subtotal + shipping_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.base_calculations.base_checkout_subtotal') as mock_subtotal:
            with patch('saleor.checkout.base_calculations.base_checkout_delivery_price') as mock_delivery:
                mock_subtotal.return_value = Money(Decimal("20.00"), "USD")
                mock_delivery.return_value = Money(Decimal("5.00"), "USD")
                
                result = base_checkout_total(checkout_info, lines)
                assert result == Money(Decimal("25.00"), "USD")  # 20 + 5


@pytest.mark.django_db
class TestBaseCheckoutSubtotal:
    """Test base_checkout_subtotal() - Statement, Decision Coverage"""
    
    def test_base_checkout_subtotal_empty_lines(self):
        """Statement: Empty lines -> return zero_money"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        
        result = base_checkout_subtotal([], channel, "USD", include_voucher=True)
        assert result == Money(Decimal("0.00"), "USD")
    
    def test_base_checkout_subtotal_multiple_lines(self):
        """Statement: Sum all line totals"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2,
            currency="USD"
        )
        
        line_info1 = CheckoutLineInfo(
            line=line1,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        line_info2 = CheckoutLineInfo(
            line=line2,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("5.00"), "USD")
        )
        
        with patch('saleor.checkout.base_calculations.calculate_base_line_total_price') as mock_total:
            mock_total.side_effect = [
                Money(Decimal("10.00"), "USD"),  # line1
                Money(Decimal("10.00"), "USD")   # line2
            ]
            result = base_checkout_subtotal([line_info1, line_info2], channel, "USD", include_voucher=True)
            assert result == Money(Decimal("20.00"), "USD")
            assert mock_total.call_count == 2


@pytest.mark.django_db
class TestCheckoutTotal:
    """Test checkout_total() - Statement Coverage"""
    
    def test_checkout_total_calculates_with_gift_cards(self):
        """Statement: Call calculate_checkout_total_with_gift_cards"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.base_calculations.calculate_checkout_total_with_gift_cards') as mock_calc:
            mock_calc.return_value = TaxedMoney(
                net=Money(Decimal("20.00"), "USD"),
                gross=Money(Decimal("20.00"), "USD")
            )
            result = checkout_total(checkout_info, lines)
            assert result.net == Money(Decimal("20.00"), "USD")
            mock_calc.assert_called_once()


@pytest.mark.django_db
class TestGetLineTotalPriceWithPropagatedCheckoutDiscount:
    """Test get_line_total_price_with_propagated_checkout_discount() - Statement Coverage"""
    
    def test_get_line_total_price_finds_line(self):
        """Statement: Find line by id -> return total_price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        checkout_discount = Money(Decimal("2.00"), "USD")
        
        with patch('saleor.checkout.base_calculations._propagate_checkout_discount_on_checkout_lines_prices') as mock_propagate:
            mock_propagate.return_value = [
                (line, Money(Decimal("8.00"), "USD"))
            ]
            result = get_line_total_price_with_propagated_checkout_discount(
                line_info, [line_info], checkout_discount
            )
            assert result == Money(Decimal("8.00"), "USD")
    
    def test_get_line_total_price_line_not_found(self):
        """Statement: Line not found -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        
        line_info1 = CheckoutLineInfo(
            line=line1,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        line_info2 = CheckoutLineInfo(
            line=line2,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("5.00"), "USD")
        )
        
        checkout_discount = Money(Decimal("2.00"), "USD")
        
        with patch('saleor.checkout.base_calculations._propagate_checkout_discount_on_checkout_lines_prices') as mock_propagate:
            mock_propagate.return_value = [
                (line2, Money(Decimal("3.00"), "USD"))
            ]
            # Search for line1 but only line2 is in results
            result = get_line_total_price_with_propagated_checkout_discount(
                line_info1, [line_info2], checkout_discount
            )
            assert result is None


@pytest.mark.django_db
class TestPropagateCheckoutDiscountOnCheckoutLinesPrices:
    """Test _propagate_checkout_discount_on_checkout_lines_prices() - Statement, Decision, MC/DC"""
    
    def test_propagate_checkout_discount_single_line(self):
        """Decision: lines_count == 1 -> apply whole discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        checkout_discount = Money(Decimal("2.00"), "USD")
        
        with patch('saleor.checkout.base_calculations.get_line_total_price_with_propagated_checkout_discount') as mock_get:
            mock_get.return_value = Money(Decimal("8.00"), "USD")
            results = list(_propagate_checkout_discount_on_checkout_lines_prices(
                [line_info], checkout_discount
            ))
            assert len(results) == 1
            assert results[0][0] == line_info
            assert results[0][1] == Money(Decimal("8.00"), "USD")
    
    def test_propagate_checkout_discount_multiple_lines(self):
        """Decision: lines_count > 1 -> propagate proportionally"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=1,
            currency="USD"
        )
        
        line_info1 = CheckoutLineInfo(
            line=line1,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        line_info2 = CheckoutLineInfo(
            line=line2,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=variant.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("5.00"), "USD")
        )
        
        checkout_discount = Money(Decimal("3.00"), "USD")
        
        with patch('saleor.checkout.base_calculations.get_line_total_price_with_propagated_checkout_discount') as mock_get:
            mock_get.side_effect = [
                Money(Decimal("8.00"), "USD"),  # line1
                Money(Decimal("2.00"), "USD")   # line2
            ]
            results = list(_propagate_checkout_discount_on_checkout_lines_prices(
                [line_info1, line_info2], checkout_discount
            ))
            assert len(results) == 2

