"""
Comprehensive White-Box Testing - Product Availability
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/product/utils/availability.py (all functions)
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from saleor.product.utils.availability import (
    get_product_availability,
    get_variant_availability,
    _get_total_discount,
    _get_total_discount_from_range,
    get_product_price_range,
    _calculate_product_price_with_taxes,
    _calculate_product_price_with_taxes_range,
)
from saleor.product.models import Product, ProductType, Category, ProductVariant, ProductVariantChannelListing, ProductChannelListing
from saleor.channel.models import Channel
from saleor.tax.models import TaxClass
from prices import Money, TaxedMoney, MoneyRange, TaxedMoneyRange


# ============================================
# TEST 1: _get_total_discount - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetTotalDiscount:
    """Test _get_total_discount() for statement coverage"""
    
    def test_get_total_discount_undiscounted_greater(self):
        """Statement Coverage: undiscounted > discounted -> return difference"""
        undiscounted = TaxedMoney(Money(Decimal("100.00"), "USD"), Money(Decimal("100.00"), "USD"))
        discounted = TaxedMoney(Money(Decimal("80.00"), "USD"), Money(Decimal("80.00"), "USD"))
        
        discount = _get_total_discount(undiscounted, discounted)
        
        assert discount is not None
        assert discount.net.amount == Decimal("20.00")
        assert discount.gross.amount == Decimal("20.00")
    
    def test_get_total_discount_undiscounted_equal(self):
        """Statement Coverage: undiscounted == discounted -> return None"""
        price = TaxedMoney(Money(Decimal("100.00"), "USD"), Money(Decimal("100.00"), "USD"))
        
        discount = _get_total_discount(price, price)
        
        assert discount is None
    
    def test_get_total_discount_undiscounted_less(self):
        """Statement Coverage: undiscounted < discounted -> return None"""
        undiscounted = TaxedMoney(Money(Decimal("80.00"), "USD"), Money(Decimal("80.00"), "USD"))
        discounted = TaxedMoney(Money(Decimal("100.00"), "USD"), Money(Decimal("100.00"), "USD"))
        
        discount = _get_total_discount(undiscounted, discounted)
        
        assert discount is None


# ============================================
# TEST 2: _get_total_discount_from_range - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetTotalDiscountFromRange:
    """Test _get_total_discount_from_range() for statement coverage"""
    
    def test_get_total_discount_from_range(self):
        """Statement Coverage: Calculate discount from ranges"""
        undiscounted = TaxedMoneyRange(
            start=TaxedMoney(Money(Decimal("100.00"), "USD"), Money(Decimal("100.00"), "USD")),
            stop=TaxedMoney(Money(Decimal("200.00"), "USD"), Money(Decimal("200.00"), "USD"))
        )
        discounted = TaxedMoneyRange(
            start=TaxedMoney(Money(Decimal("80.00"), "USD"), Money(Decimal("80.00"), "USD")),
            stop=TaxedMoney(Money(Decimal("160.00"), "USD"), Money(Decimal("160.00"), "USD"))
        )
        
        discount = _get_total_discount_from_range(undiscounted, discounted)
        
        assert discount is not None
        assert discount.net.amount == Decimal("20.00")


# ============================================
# TEST 3: get_product_price_range - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestGetProductPriceRange:
    """Test get_product_price_range() for statement coverage"""
    
    def test_get_product_price_range_price_field(self):
        """Statement Coverage: Get price range for 'price' field"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant1 = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        variant2 = ProductVariant.objects.create(
            product=product,
            sku="SKU-002"
        )
        
        listing1 = ProductVariantChannelListing.objects.create(
            variant=variant1,
            channel=channel,
            price_amount=Decimal("10.00"),
            currency=channel.currency_code
        )
        
        listing2 = ProductVariantChannelListing.objects.create(
            variant=variant2,
            channel=channel,
            price_amount=Decimal("20.00"),
            currency=channel.currency_code
        )
        
        listings = [listing1, listing2]
        
        price_range = get_product_price_range(
            variants_channel_listing=listings,
            field="price"
        )
        
        assert price_range is not None
        assert price_range.start.amount == Decimal("10.00")
        assert price_range.stop.amount == Decimal("20.00")
    
    def test_get_product_price_range_discounted_price_field(self):
        """Statement Coverage: Get price range for 'discounted_price' field"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant1 = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        variant2 = ProductVariant.objects.create(
            product=product,
            sku="SKU-002"
        )
        
        listing1 = ProductVariantChannelListing.objects.create(
            variant=variant1,
            channel=channel,
            price_amount=Decimal("10.00"),
            discounted_price_amount=Decimal("8.00"),
            currency=channel.currency_code
        )
        
        listing2 = ProductVariantChannelListing.objects.create(
            variant=variant2,
            channel=channel,
            price_amount=Decimal("20.00"),
            discounted_price_amount=Decimal("15.00"),
            currency=channel.currency_code
        )
        
        listings = [listing1, listing2]
        
        price_range = get_product_price_range(
            variants_channel_listing=listings,
            field="discounted_price"
        )
        
        assert price_range is not None
        assert price_range.start.amount == Decimal("8.00")
        assert price_range.stop.amount == Decimal("15.00")
    
    def test_get_product_price_range_prior_price_field(self):
        """Statement Coverage: Get price range for 'prior_price' field"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant1 = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        variant2 = ProductVariant.objects.create(
            product=product,
            sku="SKU-002"
        )
        
        listing1 = ProductVariantChannelListing.objects.create(
            variant=variant1,
            channel=channel,
            price_amount=Decimal("10.00"),
            prior_price_amount=Decimal("12.00"),
            currency=channel.currency_code
        )
        
        listing2 = ProductVariantChannelListing.objects.create(
            variant=variant2,
            channel=channel,
            price_amount=Decimal("20.00"),
            prior_price_amount=Decimal("25.00"),
            currency=channel.currency_code
        )
        
        listings = [listing1, listing2]
        
        price_range = get_product_price_range(
            variants_channel_listing=listings,
            field="prior_price"
        )
        
        assert price_range is not None
        assert price_range.start.amount == Decimal("12.00")
        assert price_range.stop.amount == Decimal("25.00")
    
    def test_get_product_price_range_none_prices(self):
        """Statement Coverage: All prices are None -> return None"""
        channel = Channel.objects.create(
            name="Channel",
            slug="channel",
            currency_code="USD"
        )
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001"
        )
        
        # Create listing without price
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=None,
            currency=channel.currency_code
        )
        
        listings = [listing]
        
        price_range = get_product_price_range(
            variants_channel_listing=listings,
            field="price"
        )
        
        assert price_range is None


# ============================================
# TEST 4: _calculate_product_price_with_taxes - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestCalculateProductPriceWithTaxes:
    """Test _calculate_product_price_with_taxes() for statement coverage"""
    
    def test_calculate_product_price_with_taxes_flat_rates(self):
        """Statement Coverage: FLAT_RATES strategy"""
        from saleor.tax import TaxCalculationStrategy
        
        price = Money(Decimal("100.00"), "USD")
        tax_rate = Decimal("0.10")
        tax_calculation_strategy = TaxCalculationStrategy.FLAT_RATES
        prices_entered_with_tax = False
        
        taxed_price = _calculate_product_price_with_taxes(
            price=price,
            tax_rate=tax_rate,
            tax_calculation_strategy=tax_calculation_strategy,
            prices_entered_with_tax=prices_entered_with_tax
        )
        
        assert taxed_price is not None
        assert taxed_price.net.amount == Decimal("100.00")
    
    def test_calculate_product_price_with_taxes_other_strategy(self):
        """Statement Coverage: Other strategy -> return TaxedMoney(price, price)"""
        from saleor.tax import TaxCalculationStrategy
        
        price = Money(Decimal("100.00"), "USD")
        tax_rate = Decimal("0.10")
        tax_calculation_strategy = "OTHER_STRATEGY"
        prices_entered_with_tax = False
        
        taxed_price = _calculate_product_price_with_taxes(
            price=price,
            tax_rate=tax_rate,
            tax_calculation_strategy=tax_calculation_strategy,
            prices_entered_with_tax=prices_entered_with_tax
        )
        
        assert taxed_price is not None
        assert taxed_price.net.amount == Decimal("100.00")
        assert taxed_price.gross.amount == Decimal("100.00")

