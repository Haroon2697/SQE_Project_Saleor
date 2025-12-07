"""
Comprehensive White-Box Tests for saleor/product/utils/availability.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Functions to Test:
- _get_total_discount_from_range
- _get_total_discount
- get_product_price_range
- _calculate_product_price_with_taxes
- _calculate_product_price_with_taxes_range
- get_product_availability
- get_variant_availability
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from prices import Money, MoneyRange, TaxedMoney, TaxedMoneyRange

from saleor.product.utils.availability import (
    _get_total_discount_from_range,
    _get_total_discount,
    get_product_price_range,
    _calculate_product_price_with_taxes,
    _calculate_product_price_with_taxes_range,
    get_product_availability,
    get_variant_availability,
)
from saleor.product.models import (
    Product, ProductType, Category, ProductVariant,
    ProductChannelListing, ProductVariantChannelListing
)
from saleor.channel.models import Channel
from saleor.tax import TaxCalculationStrategy


@pytest.mark.django_db
class TestGetTotalDiscount:
    """Test _get_total_discount() - Statement, Decision Coverage"""
    
    def test_get_total_discount_undiscounted_greater(self):
        """Decision: undiscounted > discounted -> return difference"""
        undiscounted = TaxedMoney(
            net=Money(Decimal("10.00"), "USD"),
            gross=Money(Decimal("10.00"), "USD")
        )
        discounted = TaxedMoney(
            net=Money(Decimal("8.00"), "USD"),
            gross=Money(Decimal("8.00"), "USD")
        )
        
        result = _get_total_discount(undiscounted, discounted)
        assert result is not None
        assert result.net == Money(Decimal("2.00"), "USD")
    
    def test_get_total_discount_undiscounted_equal(self):
        """Decision: undiscounted == discounted -> return None"""
        price = TaxedMoney(
            net=Money(Decimal("10.00"), "USD"),
            gross=Money(Decimal("10.00"), "USD")
        )
        
        result = _get_total_discount(price, price)
        assert result is None
    
    def test_get_total_discount_undiscounted_less(self):
        """Decision: undiscounted < discounted -> return None"""
        undiscounted = TaxedMoney(
            net=Money(Decimal("8.00"), "USD"),
            gross=Money(Decimal("8.00"), "USD")
        )
        discounted = TaxedMoney(
            net=Money(Decimal("10.00"), "USD"),
            gross=Money(Decimal("10.00"), "USD")
        )
        
        result = _get_total_discount(undiscounted, discounted)
        assert result is None


@pytest.mark.django_db
class TestGetTotalDiscountFromRange:
    """Test _get_total_discount_from_range() - Statement Coverage"""
    
    def test_get_total_discount_from_range_calculates_correctly(self):
        """Statement: Call _get_total_discount with range.start values"""
        undiscounted_range = TaxedMoneyRange(
            start=TaxedMoney(
                net=Money(Decimal("10.00"), "USD"),
                gross=Money(Decimal("10.00"), "USD")
            ),
            stop=TaxedMoney(
                net=Money(Decimal("20.00"), "USD"),
                gross=Money(Decimal("20.00"), "USD")
            )
        )
        discounted_range = TaxedMoneyRange(
            start=TaxedMoney(
                net=Money(Decimal("8.00"), "USD"),
                gross=Money(Decimal("8.00"), "USD")
            ),
            stop=TaxedMoney(
                net=Money(Decimal("18.00"), "USD"),
                gross=Money(Decimal("18.00"), "USD")
            )
        )
        
        result = _get_total_discount_from_range(undiscounted_range, discounted_range)
        assert result is not None
        assert result.net == Money(Decimal("2.00"), "USD")


@pytest.mark.django_db
class TestGetProductPriceRange:
    """Test get_product_price_range() - Statement, Decision Coverage"""
    
    def test_get_product_price_range_with_prices(self):
        """Statement: Extract prices from listings -> return MoneyRange"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
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
        
        listing1 = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant1,
            price_amount=Decimal("10.00"),
            currency="USD"
        )
        listing2 = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant2,
            price_amount=Decimal("20.00"),
            currency="USD"
        )
        
        result = get_product_price_range(
            variants_channel_listing=[listing1, listing2],
            field="price"
        )
        
        assert result is not None
        assert result.start == Money(Decimal("10.00"), "USD")
        assert result.stop == Money(Decimal("20.00"), "USD")
    
    def test_get_product_price_range_with_none_prices(self):
        """Decision: All prices are None -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        
        listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=None,
            currency="USD"
        )
        
        result = get_product_price_range(
            variants_channel_listing=[listing],
            field="price"
        )
        
        assert result is None
    
    def test_get_product_price_range_empty_list(self):
        """Statement: Empty list -> return None"""
        result = get_product_price_range(
            variants_channel_listing=[],
            field="price"
        )
        assert result is None


@pytest.mark.django_db
class TestCalculateProductPriceWithTaxes:
    """Test _calculate_product_price_with_taxes() - Statement, Decision Coverage"""
    
    def test_calculate_product_price_with_taxes_flat_rates(self):
        """Decision: tax_calculation_strategy == FLAT_RATES -> call calculate_flat_rate_tax"""
        price = Money(Decimal("10.00"), "USD")
        tax_rate = Decimal("0.20")
        
        with patch('saleor.product.utils.availability.calculate_flat_rate_tax') as mock_calc:
            mock_calc.return_value = TaxedMoney(
                net=Money(Decimal("8.33"), "USD"),
                gross=Money(Decimal("10.00"), "USD")
            )
            result = _calculate_product_price_with_taxes(
                price, tax_rate, TaxCalculationStrategy.FLAT_RATES, prices_entered_with_tax=True
            )
            assert mock_calc.called
            assert result.gross == Money(Decimal("10.00"), "USD")
    
    def test_calculate_product_price_with_taxes_other_strategy(self):
        """Decision: tax_calculation_strategy != FLAT_RATES -> return TaxedMoney(price, price)"""
        price = Money(Decimal("10.00"), "USD")
        tax_rate = Decimal("0.20")
        
        result = _calculate_product_price_with_taxes(
            price, tax_rate, TaxCalculationStrategy.TAX_APP, prices_entered_with_tax=True
        )
        assert result.net == price
        assert result.gross == price


@pytest.mark.django_db
class TestCalculateProductPriceWithTaxesRange:
    """Test _calculate_product_price_with_taxes_range() - Statement, Decision Coverage"""
    
    def test_calculate_product_price_with_taxes_range_with_prices(self):
        """Decision: price_net_range is not None -> calculate taxed range"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=Decimal("10.00"),
            currency="USD"
        )
        
        with patch('saleor.product.utils.availability._calculate_product_price_with_taxes') as mock_calc:
            mock_calc.return_value = TaxedMoney(
                net=Money(Decimal("10.00"), "USD"),
                gross=Money(Decimal("10.00"), "USD")
            )
            result = _calculate_product_price_with_taxes_range(
                "price", [listing], Decimal("0.20"),
                TaxCalculationStrategy.FLAT_RATES, True
            )
            assert result is not None
            assert mock_calc.call_count == 2  # Called for start and stop
    
    def test_calculate_product_price_with_taxes_range_no_prices(self):
        """Decision: price_net_range is None -> return None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=None,
            currency="USD"
        )
        
        result = _calculate_product_price_with_taxes_range(
            "price", [listing], Decimal("0.20"),
            TaxCalculationStrategy.FLAT_RATES, True
        )
        assert result is None


@pytest.mark.django_db
class TestGetProductAvailability:
    """Test get_product_availability() - Statement, Decision Coverage"""
    
    def test_get_product_availability_with_discounts(self):
        """Statement: Calculate availability with discounts and prior prices"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        product = Product.objects.create(
            product_type=ProductType.objects.create(name="Type"),
            category=Category.objects.create(name="Category")
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST"
        )
        product_listing = ProductChannelListing.objects.create(
            channel=channel,
            product=product
        )
        variant_listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=Decimal("10.00"),
            discounted_price_amount=Decimal("8.00"),
            prior_price_amount=Decimal("12.00"),
            currency="USD"
        )
        
        result = get_product_availability(
            product_channel_listing=product_listing,
            variants_channel_listing=[variant_listing],
            prices_entered_with_tax=True,
            tax_calculation_strategy=TaxCalculationStrategy.FLAT_RATES,
            tax_rate=Decimal("0.20")
        )
        
        assert result.on_sale is True
        assert result.price_range is not None
        assert result.price_range_undiscounted is not None
    
    def test_get_product_availability_no_undiscounted(self):
        """Decision: undiscounted is None -> discounted and prior are None"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        product = Product.objects.create(
            product_type=ProductType.objects.create(name="Type"),
            category=Category.objects.create(name="Category")
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST"
        )
        product_listing = ProductChannelListing.objects.create(
            channel=channel,
            product=product
        )
        variant_listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=None,
            currency="USD"
        )
        
        result = get_product_availability(
            product_channel_listing=product_listing,
            variants_channel_listing=[variant_listing],
            prices_entered_with_tax=True,
            tax_calculation_strategy=TaxCalculationStrategy.FLAT_RATES,
            tax_rate=Decimal("0.20")
        )
        
        assert result.price_range is None
        assert result.price_range_undiscounted is None


@pytest.mark.django_db
class TestGetVariantAvailability:
    """Test get_variant_availability() - Statement Coverage"""
    
    def test_get_variant_availability_calculates_correctly(self):
        """Statement: Calculate variant availability with prices"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        variant_listing = ProductVariantChannelListing.objects.create(
            channel=channel,
            variant=variant,
            price_amount=Decimal("10.00"),
            discounted_price_amount=Decimal("8.00"),
            prior_price_amount=Decimal("12.00"),
            currency="USD"
        )
        
        result = get_variant_availability(
            variant_channel_listing=variant_listing,
            prices_entered_with_tax=True,
            tax_calculation_strategy=TaxCalculationStrategy.FLAT_RATES,
            tax_rate=Decimal("0.20")
        )
        
        assert result.on_sale is True
        assert result.price is not None
        assert result.price_undiscounted is not None
        assert result.discount is not None

