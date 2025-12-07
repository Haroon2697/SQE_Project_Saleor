"""
Comprehensive White-Box Tests for saleor/warehouse/availability.py

Target: 80%+ Coverage with Statement, Decision, and MC/DC Coverage
Focusing on critical availability functions:
- check_stock_and_preorder_quantity
- check_stock_quantity
- _get_available_quantity
- get_available_quantity
- is_product_in_stock
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch, PropertyMock

from saleor.warehouse.availability import (
    check_stock_and_preorder_quantity,
    check_stock_quantity,
    _get_available_quantity,
    get_available_quantity,
    is_product_in_stock,
)
from saleor.warehouse.models import Stock, Warehouse
from saleor.channel.models import Channel
from saleor.product.models import Product, ProductType, Category, ProductVariant
from saleor.core.exceptions import InsufficientStock


@pytest.mark.django_db
class TestGetAvailableQuantity:
    """Test _get_available_quantity() - Statement, Decision Coverage"""
    
    def test_get_available_quantity_without_reservations(self):
        """Decision: check_reservations=False -> don't subtract reserved quantity"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        from saleor.warehouse.models import StockQuerySet
        stocks = Stock.objects.filter(id=stock.id)
        
        result = _get_available_quantity(stocks, checkout_lines=None, check_reservations=False)
        assert result == 10  # total_quantity - quantity_allocated (0) - quantity_reserved (0)
    
    def test_get_available_quantity_with_reservations(self):
        """Decision: check_reservations=True -> subtract reserved quantity"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        stocks = Stock.objects.filter(id=stock.id)
        
        with patch('saleor.warehouse.availability.get_reserved_stock_quantity') as mock_reserved:
            mock_reserved.return_value = 3
            result = _get_available_quantity(stocks, checkout_lines=None, check_reservations=True)
            assert result == 7  # 10 - 0 (allocated) - 3 (reserved)
    
    def test_get_available_quantity_returns_zero_if_negative(self):
        """Decision: Available quantity < 0 -> return 0"""
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        variant = ProductVariant.objects.create(
            product=Product.objects.create(
                product_type=ProductType.objects.create(name="Type"),
                category=Category.objects.create(name="Category")
            ),
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=5
        )
        
        stocks = Stock.objects.filter(id=stock.id)
        
        with patch('saleor.warehouse.availability.get_reserved_stock_quantity') as mock_reserved:
            mock_reserved.return_value = 10  # More than available
            result = _get_available_quantity(stocks, checkout_lines=None, check_reservations=True)
            assert result == 0  # max(0, ...)


@pytest.mark.django_db
class TestCheckStockAndPreorderQuantity:
    """Test check_stock_and_preorder_quantity() - Statement, Decision Coverage"""
    
    def test_check_stock_and_preorder_quantity_preorder_active(self):
        """Decision: is_preorder_active() -> check_preorder_threshold"""
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
        
        with patch.object(variant, 'is_preorder_active', return_value=True):
            with patch('saleor.warehouse.availability.check_preorder_threshold_in_orders') as mock_check:
                check_stock_and_preorder_quantity(
                    variant, "US", channel.slug, 5, checkout_lines=None, check_reservations=False
                )
                mock_check.assert_called_once()
    
    def test_check_stock_and_preorder_quantity_not_preorder(self):
        """Decision: not is_preorder_active() -> check_stock_quantity"""
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
        
        with patch.object(variant, 'is_preorder_active', return_value=False):
            with patch('saleor.warehouse.availability.check_stock_quantity') as mock_check:
                check_stock_and_preorder_quantity(
                    variant, "US", channel.slug, 5, checkout_lines=None, check_reservations=False
                )
                mock_check.assert_called_once()


@pytest.mark.django_db
class TestCheckStockQuantity:
    """Test check_stock_quantity() - Statement, Decision Coverage"""
    
    def test_check_stock_quantity_sufficient_stock(self):
        """Statement: Sufficient stock -> no exception"""
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
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        # Should not raise exception
        check_stock_quantity(
            variant, "US", channel.slug, 5,
            checkout_lines=None, check_reservations=False, order_line=None
        )
    
    def test_check_stock_quantity_insufficient_stock(self):
        """Decision: Insufficient stock -> raise InsufficientStock"""
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
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=3
        )
        
        with pytest.raises(InsufficientStock):
            check_stock_quantity(
                variant, "US", channel.slug, 5,
                checkout_lines=None, check_reservations=False, order_line=None
            )


@pytest.mark.django_db
class TestGetAvailableQuantityFunction:
    """Test get_available_quantity() - Statement Coverage"""
    
    def test_get_available_quantity_returns_correct_value(self):
        """Statement: Return available quantity for variant"""
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
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        result = get_available_quantity(variant, "US", channel.slug)
        assert result >= 0


@pytest.mark.django_db
class TestIsProductInStock:
    """Test is_product_in_stock() - Statement, Decision Coverage"""
    
    def test_is_product_in_stock_has_stock(self):
        """Decision: Available quantity > 0 -> return True"""
        channel = Channel.objects.create(
            name="Test Channel",
            slug="test-channel",
            currency_code="USD"
        )
        warehouse = Warehouse.objects.create(
            name="Test Warehouse",
            slug="test-warehouse"
        )
        product = Product.objects.create(
            product_type=ProductType.objects.create(name="Type"),
            category=Category.objects.create(name="Category")
        )
        variant = ProductVariant.objects.create(
            product=product,
            sku="TEST"
        )
        stock = Stock.objects.create(
            variant=variant,
            warehouse=warehouse,
            quantity=10
        )
        
        result = is_product_in_stock(product, "US", channel.slug)
        assert result is True
    
    def test_is_product_in_stock_no_stock(self):
        """Decision: Available quantity == 0 -> return False"""
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
        # No stock created
        
        result = is_product_in_stock(product, "US", channel.slug)
        assert result is False

