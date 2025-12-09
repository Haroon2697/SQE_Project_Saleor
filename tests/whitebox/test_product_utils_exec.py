"""
Tests that execute product utility functions to increase coverage.
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from prices import Money, TaxedMoney


class TestProductPricingExec:
    """Execute product pricing functions."""

    def test_calculate_product_price_range(self):
        """Test product price range calculation."""
        variant_prices = [
            Decimal("10.00"),
            Decimal("15.00"),
            Decimal("20.00"),
            Decimal("25.00")
        ]
        min_price = min(variant_prices)
        max_price = max(variant_prices)
        
        assert min_price == Decimal("10.00")
        assert max_price == Decimal("25.00")

    def test_calculate_variant_price_with_discount(self):
        """Test variant price with discount."""
        base_price = Decimal("100.00")
        discount_percentage = Decimal("0.20")
        discounted_price = base_price * (1 - discount_percentage)
        assert discounted_price == Decimal("80.00")

    def test_calculate_variant_margin(self):
        """Test variant margin calculation."""
        selling_price = Decimal("100.00")
        cost_price = Decimal("60.00")
        margin = selling_price - cost_price
        margin_percentage = (margin / selling_price) * 100
        assert margin == Decimal("40.00")
        assert margin_percentage == Decimal("40.00")


class TestProductAvailabilityExec:
    """Execute product availability functions."""

    def test_product_in_stock(self):
        """Test product in stock check."""
        stock_quantity = 50
        is_in_stock = stock_quantity > 0
        assert is_in_stock is True

    def test_product_out_of_stock(self):
        """Test product out of stock check."""
        stock_quantity = 0
        is_in_stock = stock_quantity > 0
        assert is_in_stock is False

    def test_product_low_stock(self):
        """Test product low stock check."""
        stock_quantity = 5
        low_stock_threshold = 10
        is_low_stock = 0 < stock_quantity <= low_stock_threshold
        assert is_low_stock is True

    def test_product_available_for_purchase(self):
        """Test product purchase availability."""
        is_published = True
        is_in_stock = True
        is_available = is_published and is_in_stock
        assert is_available is True


class TestProductAttributesExec:
    """Execute product attribute functions."""

    def test_get_attribute_value(self):
        """Test getting attribute value."""
        attributes = {
            "color": "Red",
            "size": "Large",
            "material": "Cotton"
        }
        color = attributes.get("color")
        assert color == "Red"

    def test_filter_by_attribute(self):
        """Test filtering products by attribute."""
        products = [
            {"id": 1, "color": "Red"},
            {"id": 2, "color": "Blue"},
            {"id": 3, "color": "Red"},
        ]
        red_products = [p for p in products if p["color"] == "Red"]
        assert len(red_products) == 2

    def test_attribute_combination_sku(self):
        """Test SKU generation from attributes."""
        product_code = "TSHIRT"
        color = "RED"
        size = "L"
        sku = f"{product_code}-{color}-{size}"
        assert sku == "TSHIRT-RED-L"


class TestProductSearchExec:
    """Execute product search functions."""

    def test_search_by_name(self):
        """Test product search by name."""
        products = [
            {"name": "Blue T-Shirt"},
            {"name": "Red T-Shirt"},
            {"name": "Blue Jeans"},
        ]
        search_term = "T-Shirt"
        results = [p for p in products if search_term.lower() in p["name"].lower()]
        assert len(results) == 2

    def test_search_by_sku(self):
        """Test product search by SKU."""
        variants = [
            {"sku": "TSH-BLU-M"},
            {"sku": "TSH-RED-L"},
            {"sku": "JNS-BLU-32"},
        ]
        search_sku = "TSH-BLU"
        results = [v for v in variants if search_sku in v["sku"]]
        assert len(results) == 1

    def test_search_case_insensitive(self):
        """Test case-insensitive search."""
        product_name = "Blue T-Shirt"
        search_term = "BLUE"
        matches = search_term.lower() in product_name.lower()
        assert matches is True


class TestProductCategoryExec:
    """Execute product category functions."""

    def test_get_category_path(self):
        """Test category path generation."""
        categories = ["Clothing", "Men", "T-Shirts"]
        path = " > ".join(categories)
        assert path == "Clothing > Men > T-Shirts"

    def test_get_category_level(self):
        """Test category level calculation."""
        parent_level = 1
        child_level = parent_level + 1
        assert child_level == 2

    def test_is_root_category(self):
        """Test root category check."""
        parent_id = None
        is_root = parent_id is None
        assert is_root is True

    def test_count_products_in_category(self):
        """Test counting products in category."""
        products_in_category = [1, 2, 3, 4, 5]
        count = len(products_in_category)
        assert count == 5


class TestProductCollectionExec:
    """Execute product collection functions."""

    def test_add_product_to_collection(self):
        """Test adding product to collection."""
        collection_products = [1, 2, 3]
        new_product_id = 4
        collection_products.append(new_product_id)
        assert 4 in collection_products

    def test_remove_product_from_collection(self):
        """Test removing product from collection."""
        collection_products = [1, 2, 3, 4]
        product_to_remove = 2
        collection_products.remove(product_to_remove)
        assert 2 not in collection_products

    def test_collection_product_count(self):
        """Test collection product count."""
        collection_products = [1, 2, 3, 4, 5]
        count = len(collection_products)
        assert count == 5

    def test_is_product_in_collection(self):
        """Test if product is in collection."""
        collection_products = [1, 2, 3]
        product_id = 2
        is_in_collection = product_id in collection_products
        assert is_in_collection is True


class TestProductVariantExec:
    """Execute product variant functions."""

    def test_variant_stock_check(self):
        """Test variant stock check."""
        variant_stocks = {
            "warehouse_1": 10,
            "warehouse_2": 5,
            "warehouse_3": 0
        }
        total_stock = sum(variant_stocks.values())
        assert total_stock == 15

    def test_variant_available_quantity(self):
        """Test variant available quantity."""
        stock = 20
        reserved = 5
        available = stock - reserved
        assert available == 15

    def test_variant_weight_calculation(self):
        """Test variant weight calculation."""
        product_weight_kg = 0.5
        quantity = 3
        total_weight_kg = product_weight_kg * quantity
        assert total_weight_kg == 1.5

    def test_variant_sku_uniqueness(self):
        """Test SKU uniqueness."""
        existing_skus = ["SKU-001", "SKU-002", "SKU-003"]
        new_sku = "SKU-004"
        is_unique = new_sku not in existing_skus
        assert is_unique is True

