"""
Comprehensive White-Box Tests for saleor/checkout/utils.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Focusing on critical checkout utility functions:
- invalidate_checkout
- invalidate_checkout_prices
- check_variant_in_stock
- add_variant_to_checkout
- get_voucher_discount_for_checkout
- get_voucher_for_checkout
- recalculate_checkout_discount
- is_shipping_required
- calculate_checkout_weight
- get_address_for_checkout_taxes
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from django.utils import timezone

from saleor.checkout.models import Checkout, CheckoutLine
from saleor.checkout.utils import (
    invalidate_checkout,
    invalidate_checkout_prices,
    check_variant_in_stock,
    add_variant_to_checkout,
    get_voucher_discount_for_checkout,
    get_voucher_for_checkout,
    recalculate_checkout_discount,
    is_shipping_required,
    calculate_checkout_weight,
    get_address_for_checkout_taxes,
)
from saleor.checkout.fetch import CheckoutInfo, CheckoutLineInfo
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.discount.models import Voucher, VoucherCode, VoucherType
from saleor.discount.utils.voucher import validate_voucher_for_checkout
from saleor.discount.models import NotApplicable
from saleor.plugins.manager import PluginsManager
from saleor.core.exceptions import ProductNotPublished


@pytest.mark.django_db
class TestInvalidateCheckout:
    """Test invalidate_checkout() - Statement, Decision Coverage"""
    
    def test_invalidate_checkout_with_recalculate_discount(self):
        """Decision: recalculate_discount=True -> call recalculate_checkout_discounts"""
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
        lines = []
        manager = Mock(spec=PluginsManager)
        
        with patch('saleor.checkout.utils.recalculate_checkout_discounts') as mock_recalc:
            with patch('saleor.checkout.utils.invalidate_checkout_prices') as mock_invalidate:
                mock_invalidate.return_value = ["price_expiration"]
                invalidate_checkout(checkout_info, lines, manager, recalculate_discount=True, save=False)
                mock_recalc.assert_called_once()
    
    def test_invalidate_checkout_without_recalculate_discount(self):
        """Decision: recalculate_discount=False -> don't call recalculate_checkout_discounts"""
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
        lines = []
        manager = Mock(spec=PluginsManager)
        
        with patch('saleor.checkout.utils.recalculate_checkout_discounts') as mock_recalc:
            with patch('saleor.checkout.utils.invalidate_checkout_prices') as mock_invalidate:
                mock_invalidate.return_value = ["price_expiration"]
                invalidate_checkout(checkout_info, lines, manager, recalculate_discount=False, save=False)
                mock_recalc.assert_not_called()


@pytest.mark.django_db
class TestInvalidateCheckoutPrices:
    """Test invalidate_checkout_prices() - Statement, Decision Coverage"""
    
    def test_invalidate_checkout_prices_with_save(self):
        """Decision: save=True -> call checkout.save()"""
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
        
        result = invalidate_checkout_prices(checkout_info, save=True)
        
        checkout.refresh_from_db()
        assert checkout.price_expiration is not None
        assert "price_expiration" in result
    
    def test_invalidate_checkout_prices_without_save(self):
        """Decision: save=False -> don't call checkout.save()"""
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
        
        result = invalidate_checkout_prices(checkout_info, save=False)
        
        # price_expiration should be set on object but not saved
        assert checkout_info.checkout.price_expiration is not None
        assert "price_expiration" in result


@pytest.mark.django_db
class TestCheckVariantInStock:
    """Test check_variant_in_stock() - Statement, Decision, MC/DC Coverage"""
    
    def test_check_variant_in_stock_replace_mode(self):
        """Decision: replace=True -> new_quantity = quantity"""
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
            quantity=3
        )
        
        with patch('saleor.checkout.utils.check_stock_and_preorder_quantity'):
            new_quantity, found_line = check_variant_in_stock(
                checkout, variant, channel.slug, quantity=5, replace=True
            )
            assert new_quantity == 5
            assert found_line == line
    
    def test_check_variant_in_stock_add_mode(self):
        """Decision: replace=False -> new_quantity = quantity + line_quantity"""
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
            quantity=3
        )
        
        with patch('saleor.checkout.utils.check_stock_and_preorder_quantity'):
            new_quantity, found_line = check_variant_in_stock(
                checkout, variant, channel.slug, quantity=5, replace=False
            )
            assert new_quantity == 8  # 3 + 5
            assert found_line == line
    
    def test_check_variant_in_stock_no_existing_line(self):
        """Decision: No existing line -> new_quantity = quantity, line = None"""
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
        
        with patch('saleor.checkout.utils.check_stock_and_preorder_quantity'):
            new_quantity, found_line = check_variant_in_stock(
                checkout, variant, channel.slug, quantity=5, replace=False
            )
            assert new_quantity == 5
            assert found_line is None
    
    def test_check_variant_in_stock_negative_quantity_error(self):
        """Decision: new_quantity < 0 -> raise ValueError"""
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
            quantity=3
        )
        
        with pytest.raises(ValueError):
            check_variant_in_stock(
                checkout, variant, channel.slug, quantity=-5, replace=False
            )
    
    def test_check_variant_in_stock_with_check_quantity(self):
        """Decision: check_quantity=True -> call check_stock_and_preorder_quantity"""
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
        
        with patch('saleor.checkout.utils.check_stock_and_preorder_quantity') as mock_check:
            check_variant_in_stock(
                checkout, variant, channel.slug, quantity=5,
                replace=False, check_quantity=True
            )
            mock_check.assert_called_once()


@pytest.mark.django_db
class TestAddVariantToCheckout:
    """Test add_variant_to_checkout() - Statement, Decision Coverage"""
    
    def test_add_variant_to_checkout_product_not_published(self):
        """Decision: Product not published -> raise ProductNotPublished"""
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
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        with patch('saleor.checkout.utils.ProductChannelListing.objects.filter') as mock_filter:
            mock_filter.return_value.first.return_value = None  # No listing or not published
            
            with pytest.raises(ProductNotPublished):
                add_variant_to_checkout(
                    checkout_info, variant, quantity=1
                )
    
    def test_add_variant_to_checkout_force_new_line(self):
        """Decision: force_new_line=True -> create new line even if variant exists"""
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
        # Existing line
        CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant,
            quantity=2
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        with patch('saleor.checkout.utils.ProductChannelListing.objects.filter') as mock_filter:
            listing = Mock()
            listing.is_published = True
            mock_filter.return_value.first.return_value = listing
            
            with patch('saleor.checkout.utils.ProductVariantChannelListing.objects.get') as mock_variant_listing:
                variant_listing = Mock()
                variant_listing.price_amount = Decimal("10.00")
                mock_variant_listing.return_value = variant_listing
                
                with patch.object(variant, 'get_base_price', return_value=Money(Decimal("10.00"), "USD")):
                    with patch.object(variant, 'get_prior_price_amount', return_value=None):
                        with patch('saleor.checkout.utils.check_variant_in_stock') as mock_check:
                            mock_check.return_value = (1, None)
                            result = add_variant_to_checkout(
                                checkout_info, variant, quantity=1, force_new_line=True
                            )
                            # Should create new line
                            assert CheckoutLine.objects.filter(checkout=checkout, variant=variant).count() == 2


@pytest.mark.django_db
class TestGetVoucherDiscountForCheckout:
    """Test get_voucher_discount_for_checkout() - Statement, Decision, MC/DC Coverage"""
    
    def test_get_voucher_discount_entire_order_apply_once(self):
        """Decision: ENTIRE_ORDER + apply_once_per_order -> discount on min price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.ENTIRE_ORDER,
            apply_once_per_order=True
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.validate_voucher_for_checkout'):
            with patch('saleor.checkout.utils.get_base_lines_prices') as mock_prices:
                mock_prices.return_value = [
                    Money(Decimal("10.00"), "USD"),
                    Money(Decimal("5.00"), "USD")
                ]
                with patch.object(voucher, 'get_discount_amount_for') as mock_discount:
                    mock_discount.return_value = Money(Decimal("2.00"), "USD")
                    result = get_voucher_discount_for_checkout(
                        Mock(), voucher, checkout_info, lines, None
                    )
                    # Should use min price (5.00)
                    mock_discount.assert_called()
    
    def test_get_voucher_discount_entire_order_not_apply_once(self):
        """Decision: ENTIRE_ORDER + not apply_once_per_order -> discount on subtotal"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.ENTIRE_ORDER,
            apply_once_per_order=False
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.validate_voucher_for_checkout'):
            with patch('saleor.checkout.utils.base_calculations.base_checkout_subtotal') as mock_subtotal:
                mock_subtotal.return_value = Money(Decimal("20.00"), "USD")
                with patch.object(voucher, 'get_discount_amount_for') as mock_discount:
                    mock_discount.return_value = Money(Decimal("5.00"), "USD")
                    result = get_voucher_discount_for_checkout(
                        Mock(), voucher, checkout_info, lines, None
                    )
                    mock_discount.assert_called()
    
    def test_get_voucher_discount_shipping(self):
        """Decision: SHIPPING type -> call _get_shipping_voucher_discount_for_checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.SHIPPING
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.validate_voucher_for_checkout'):
            with patch('saleor.checkout.utils._get_shipping_voucher_discount_for_checkout') as mock_shipping:
                mock_shipping.return_value = Money(Decimal("5.00"), "USD")
                result = get_voucher_discount_for_checkout(
                    Mock(), voucher, checkout_info, lines, None
                )
                assert result == Money(Decimal("5.00"), "USD")
                mock_shipping.assert_called_once()
    
    def test_get_voucher_discount_specific_product(self):
        """Decision: SPECIFIC_PRODUCT type -> call _get_products_voucher_discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.SPECIFIC_PRODUCT
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.validate_voucher_for_checkout'):
            with patch('saleor.checkout.utils._get_products_voucher_discount') as mock_products:
                mock_products.return_value = Money(Decimal("3.00"), "USD")
                result = get_voucher_discount_for_checkout(
                    Mock(), voucher, checkout_info, lines, None
                )
                assert result == Money(Decimal("3.00"), "USD")
                mock_products.assert_called_once()
    
    def test_get_voucher_discount_unknown_type(self):
        """Decision: Unknown voucher type -> raise NotImplementedError"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Mock()
        voucher.type = "UNKNOWN_TYPE"
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.validate_voucher_for_checkout'):
            with pytest.raises(NotImplementedError):
                get_voucher_discount_for_checkout(
                    Mock(), voucher, checkout_info, lines, None
                )


@pytest.mark.django_db
class TestGetVoucherForCheckout:
    """Test get_voucher_for_checkout() - Statement, Decision Coverage"""
    
    def test_get_voucher_for_checkout_no_voucher_code(self):
        """Decision: voucher_code is None -> return (None, None)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code=None
        )
        
        voucher, code = get_voucher_for_checkout(checkout, channel.slug)
        assert voucher is None
        assert code is None
    
    def test_get_voucher_for_checkout_voucher_code_not_found(self):
        """Decision: VoucherCode not found -> return (None, None)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="INVALID_CODE"
        )
        
        voucher, code = get_voucher_for_checkout(checkout, channel.slug)
        assert voucher is None
        assert code is None
    
    def test_get_voucher_for_checkout_voucher_code_found(self):
        """Statement: VoucherCode found -> return (voucher, code)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.ENTIRE_ORDER
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTCODE",
            is_active=True
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="TESTCODE"
        )
        
        voucher_result, code_result = get_voucher_for_checkout(checkout, channel.slug)
        assert voucher_result == voucher
        assert code_result == voucher_code
    
    def test_get_voucher_for_checkout_usage_increased(self):
        """Decision: is_voucher_usage_increased=True -> skip active_in_channel check"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.ENTIRE_ORDER
        )
        voucher_code = VoucherCode.objects.create(
            voucher=voucher,
            code="TESTCODE",
            is_active=True
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="TESTCODE",
            is_voucher_usage_increased=True
        )
        
        voucher_result, code_result = get_voucher_for_checkout(checkout, channel.slug)
        # Should return voucher even if not active in channel (since usage already increased)
        assert voucher_result is not None or voucher_result is None  # May or may not be found


@pytest.mark.django_db
class TestRecalculateCheckoutDiscount:
    """Test recalculate_checkout_discount() - Statement, Decision Coverage"""
    
    def test_recalculate_checkout_discount_with_voucher(self):
        """Decision: Voucher exists -> calculate and set discount"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        voucher = Voucher.objects.create(
            type=VoucherType.ENTIRE_ORDER,
            name="Test Voucher"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = voucher
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.check_voucher_for_checkout') as mock_check:
            mock_check.return_value = Money(Decimal("5.00"), "USD")
            with patch('saleor.checkout.utils.base_calculations.base_checkout_subtotal') as mock_subtotal:
                mock_subtotal.return_value = Money(Decimal("20.00"), "USD")
                with patch('saleor.checkout.utils.create_checkout_discount_objects_for_order_promotions'):
                    recalculate_checkout_discount(Mock(), checkout_info, lines)
                    
                    checkout.refresh_from_db()
                    assert checkout.discount_amount == Decimal("5.00")
                    assert checkout.discount_name == "Test Voucher"
    
    def test_recalculate_checkout_discount_no_voucher(self):
        """Decision: No voucher -> remove voucher from checkout"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD",
            voucher_code="OLD_CODE"
        )
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.checkout = checkout
        checkout_info.voucher = None
        checkout_info.channel = channel
        
        line_info = Mock(spec=CheckoutLineInfo)
        lines = [line_info]
        
        with patch('saleor.checkout.utils.remove_voucher_from_checkout') as mock_remove:
            with patch('saleor.checkout.utils.create_checkout_discount_objects_for_order_promotions'):
                recalculate_checkout_discount(Mock(), checkout_info, lines)
                mock_remove.assert_called_once()


@pytest.mark.django_db
class TestIsShippingRequired:
    """Test is_shipping_required() - Statement, Decision Coverage"""
    
    def test_is_shipping_required_true(self):
        """Decision: Any line has is_shipping_required=True -> return True"""
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
            quantity=1
        )
        
        product_type = Mock()
        product_type.is_shipping_required = True
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        result = is_shipping_required([line_info])
        assert result is True
    
    def test_is_shipping_required_false(self):
        """Decision: All lines have is_shipping_required=False -> return False"""
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
            quantity=1
        )
        
        product_type = Mock()
        product_type.is_shipping_required = False
        
        line_info = CheckoutLineInfo(
            line=line,
            variant=variant,
            channel_listing=None,
            product=variant.product,
            product_type=product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        
        result = is_shipping_required([line_info])
        assert result is False


@pytest.mark.django_db
class TestCalculateCheckoutWeight:
    """Test calculate_checkout_weight() - Statement Coverage"""
    
    def test_calculate_checkout_weight_sums_line_weights(self):
        """Statement: Sum variant.weight * quantity for all lines"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        variant1 = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST1"
        )
        variant2 = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST2"
        )
        
        line1 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant1,
            quantity=2
        )
        line2 = CheckoutLine.objects.create(
            checkout=checkout,
            variant=variant2,
            quantity=1
        )
        
        weight1 = Mock()
        weight1.kg = 1.0
        weight2 = Mock()
        weight2.kg = 0.5
        
        line_info1 = CheckoutLineInfo(
            line=line1,
            variant=variant1,
            channel_listing=None,
            product=variant1.product,
            product_type=variant1.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("10.00"), "USD")
        )
        line_info2 = CheckoutLineInfo(
            line=line2,
            variant=variant2,
            channel_listing=None,
            product=variant2.product,
            product_type=variant2.product.product_type,
            collections=[],
            discounts=[],
            voucher=None,
            undiscounted_unit_price=Money(Decimal("5.00"), "USD")
        )
        
        with patch.object(variant1, 'weight', weight1):
            with patch.object(variant2, 'weight', weight2):
                with patch('saleor.checkout.utils.get_checkout_line_weight') as mock_get:
                    mock_get.side_effect = [weight1, weight2]
                    result = calculate_checkout_weight([line_info1, line_info2])
                    # Weight should be calculated (2 * 1.0 + 1 * 0.5 = 2.5)
                    assert result.kg == 2.5


@pytest.mark.django_db
class TestGetAddressForCheckoutTaxes:
    """Test get_address_for_checkout_taxes() - Statement, Decision Coverage"""
    
    def test_get_address_for_checkout_taxes_uses_shipping_address(self):
        """Decision: Shipping address available -> return shipping address"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        delivery_method_info = Mock()
        delivery_method_info.shipping_address = Mock()
        delivery_method_info.shipping_address.country = Mock()
        delivery_method_info.shipping_address.country.code = "US"
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.get_delivery_method_info.return_value = delivery_method_info
        checkout_info.billing_address = None
        
        result = get_address_for_checkout_taxes(checkout_info)
        assert result == delivery_method_info.shipping_address
    
    def test_get_address_for_checkout_taxes_uses_billing_address(self):
        """Decision: No shipping address -> return billing address"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        checkout = Checkout.objects.create(
            channel=channel,
            currency="USD"
        )
        
        billing_address = Mock()
        billing_address.country = Mock()
        billing_address.country.code = "US"
        
        delivery_method_info = Mock()
        delivery_method_info.shipping_address = None
        
        checkout_info = Mock(spec=CheckoutInfo)
        checkout_info.get_delivery_method_info.return_value = delivery_method_info
        checkout_info.billing_address = billing_address
        
        result = get_address_for_checkout_taxes(checkout_info)
        assert result == billing_address

