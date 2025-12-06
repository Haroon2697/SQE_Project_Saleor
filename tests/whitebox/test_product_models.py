"""
White-Box Testing - Product Models
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/product/models.py (ProductVariant methods)
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock

from saleor.product.models import (
    Product, ProductType, Category, ProductVariant, ProductVariantChannelListing,
    ProductTypeKind
)
from saleor.channel.models import Channel
from prices import Money


# ============================================
# TEST 1: ProductVariant.get_base_price() - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetBasePrice:
    """Test ProductVariant.get_base_price() for statement coverage"""
    
    def test_get_base_price_price_override_none(self):
        """Statement Coverage: price_override is None -> return channel_listing.price"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-001"
        )
        
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("99.99"),
            currency=channel.currency_code
        )
        
        # Test with price_override = None
        base_price = variant.get_base_price(listing, price_override=None)
        assert base_price == listing.price
        assert base_price.amount == Decimal("99.99")
    
    def test_get_base_price_price_override_provided(self):
        """Statement Coverage: price_override is provided -> return Money(price_override)"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST-001"
        )
        
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("99.99"),
            currency=channel.currency_code
        )
        
        # Test with price_override provided
        override_price = Decimal("149.99")
        base_price = variant.get_base_price(listing, price_override=override_price)
        assert base_price.amount == override_price
        assert base_price.currency == channel.currency_code


# ============================================
# TEST 2: ProductVariant.get_base_price() - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetBasePriceDecision:
    """Test all decision branches in get_base_price()"""
    
    def test_decision_price_override_none_true(self):
        """Decision: price_override is None -> TRUE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("50.00"),
            currency="USD"
        )
        
        price = variant.get_base_price(listing, price_override=None)
        assert price == listing.price
    
    def test_decision_price_override_none_false(self):
        """Decision: price_override is None -> FALSE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("50.00"),
            currency="USD"
        )
        
        override = Decimal("75.00")
        price = variant.get_base_price(listing, price_override=override)
        assert price.amount == override
        assert price != listing.price


# ============================================
# TEST 3: ProductVariant.get_price() - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetPrice:
    """Test ProductVariant.get_price() for statement coverage"""
    
    def test_get_price_price_override_none_with_discounted_price(self):
        """Statement Coverage: price_override is None, discounted_price exists"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            discounted_price_amount=Decimal("80.00"),
            currency="USD"
        )
        
        price = variant.get_price(listing, price_override=None)
        assert price.amount == Decimal("80.00")  # Should return discounted_price
    
    def test_get_price_price_override_none_without_discounted_price(self):
        """Statement Coverage: price_override is None, discounted_price is None"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            discounted_price_amount=None,
            currency="USD"
        )
        
        price = variant.get_price(listing, price_override=None)
        assert price.amount == Decimal("100.00")  # Should return price
    
    def test_get_price_price_override_provided(self):
        """Statement Coverage: price_override is provided -> calculate with promotions"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            currency="USD"
        )
        
        # Test with price_override (will call calculate_discounted_price_for_rules)
        override = Decimal("120.00")
        price = variant.get_price(listing, price_override=override, promotion_rules=[])
        # Should use base_price with override and apply promotions (empty rules = no discount)
        assert price.amount == override


# ============================================
# TEST 4: ProductVariant.get_price() - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetPriceDecision:
    """Test all decision branches in get_price()"""
    
    def test_decision_price_override_none_true(self):
        """Decision: price_override is None -> TRUE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            discounted_price_amount=Decimal("90.00"),
            currency="USD"
        )
        
        price = variant.get_price(listing, price_override=None)
        assert price.amount == Decimal("90.00")
    
    def test_decision_price_override_none_false(self):
        """Decision: price_override is None -> FALSE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            currency="USD"
        )
        
        override = Decimal("150.00")
        price = variant.get_price(listing, price_override=override)
        assert price.amount == override
    
    def test_decision_discounted_price_exists_true(self):
        """Decision: discounted_price exists -> TRUE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            discounted_price_amount=Decimal("85.00"),
            currency="USD"
        )
        
        price = variant.get_price(listing)
        assert price.amount == Decimal("85.00")
    
    def test_decision_discounted_price_exists_false(self):
        """Decision: discounted_price is None -> FALSE branch"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            discounted_price_amount=None,
            currency="USD"
        )
        
        price = variant.get_price(listing)
        assert price.amount == Decimal("100.00")


# ============================================
# TEST 5: ProductVariant.get_prior_price_amount() - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetPriorPriceAmount:
    """Test ProductVariant.get_prior_price_amount() for statement coverage"""
    
    def test_get_prior_price_channel_listing_none(self):
        """Statement Coverage: channel_listing is None -> return None"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        
        prior_price = variant.get_prior_price_amount(None)
        assert prior_price is None
    
    def test_get_prior_price_prior_price_none(self):
        """Statement Coverage: channel_listing.prior_price is None -> return None"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            currency="USD"
        )
        # prior_price is None by default
        
        prior_price = variant.get_prior_price_amount(listing)
        assert prior_price is None
    
    def test_get_prior_price_with_prior_price(self):
        """Statement Coverage: channel_listing.prior_price exists -> return amount"""
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
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        listing = ProductVariantChannelListing.objects.create(
            variant=variant,
            channel=channel,
            price_amount=Decimal("100.00"),
            currency="USD"
        )
        
        # Create a prior price
        from saleor.core.prices import Money
        listing.prior_price = Money(Decimal("120.00"), "USD")
        listing.save()
        
        prior_price = variant.get_prior_price_amount(listing)
        assert prior_price == Decimal("120.00")


# ============================================
# TEST 6: ProductVariant.get_weight() - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantGetWeight:
    """Test ProductVariant.get_weight() for statement coverage"""
    
    def test_get_weight_variant_weight_exists(self):
        """Statement Coverage: self.weight exists -> return self.weight"""
        from saleor.core.weight import Weight
        
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
            sku="SKU-001",
            weight=Weight(kg=2.5)
        )
        
        weight = variant.get_weight()
        assert weight.kg == 2.5
    
    def test_get_weight_product_weight_exists(self):
        """Statement Coverage: self.weight is None, product.weight exists"""
        from saleor.core.weight import Weight
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            weight=Weight(kg=1.5)
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001",
            weight=None
        )
        
        weight = variant.get_weight()
        assert weight.kg == 1.5
    
    def test_get_weight_product_type_weight_exists(self):
        """Statement Coverage: variant and product weight are None, product_type.weight exists"""
        from saleor.core.weight import Weight
        
        product_type = ProductType.objects.create(
            name="Type",
            slug="type",
            weight=Weight(kg=0.5)
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            weight=None
        )
        
        variant = ProductVariant.objects.create(
            product=product,
            sku="SKU-001",
            weight=None
        )
        
        weight = variant.get_weight()
        assert weight.kg == 0.5


# ============================================
# TEST 7: ProductVariant.is_digital() - Statement Coverage & Decision Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantIsDigital:
    """Test ProductVariant.is_digital() for statement and decision coverage"""
    
    def test_is_digital_shipping_required_false_and_is_digital_true(self):
        """Statement Coverage: not shipping_required AND is_digital -> True"""
        product_type = ProductType.objects.create(
            name="Digital Type",
            slug="digital-type",
            is_shipping_required=False,
            is_digital=True
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Digital Product",
            slug="digital-product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="DIG-001")
        assert variant.is_digital() is True
    
    def test_is_digital_shipping_required_true(self):
        """Statement Coverage: shipping_required -> False"""
        product_type = ProductType.objects.create(
            name="Physical Type",
            slug="physical-type",
            is_shipping_required=True,
            is_digital=False
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Physical Product",
            slug="physical-product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="PHY-001")
        assert variant.is_digital() is False
    
    def test_is_digital_is_digital_false(self):
        """Statement Coverage: not shipping_required BUT is_digital = False -> False"""
        product_type = ProductType.objects.create(
            name="Type",
            slug="type",
            is_shipping_required=False,
            is_digital=False
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        assert variant.is_digital() is False


# ============================================
# TEST 8: ProductVariant.is_digital() - MC/DC Coverage
# ============================================
@pytest.mark.django_db
class TestProductVariantIsDigitalMCDC:
    """Modified Condition/Decision Coverage for is_digital()"""
    
    def test_mcdc_not_shipping_required_true_is_digital_true(self):
        """MC/DC: not shipping_required = True AND is_digital = True -> True"""
        product_type = ProductType.objects.create(
            name="Type",
            slug="type",
            is_shipping_required=False,
            is_digital=True
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        assert variant.is_digital() is True
    
    def test_mcdc_not_shipping_required_false(self):
        """MC/DC: not shipping_required = False -> False (regardless of is_digital)"""
        product_type = ProductType.objects.create(
            name="Type",
            slug="type",
            is_shipping_required=True,
            is_digital=True  # Even if digital, shipping required makes it False
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        assert variant.is_digital() is False
    
    def test_mcdc_is_digital_false(self):
        """MC/DC: is_digital = False -> False (regardless of shipping)"""
        product_type = ProductType.objects.create(
            name="Type",
            slug="type",
            is_shipping_required=False,
            is_digital=False
        )
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        variant = ProductVariant.objects.create(product=product, sku="SKU-001")
        assert variant.is_digital() is False

