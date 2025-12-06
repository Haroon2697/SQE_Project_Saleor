"""
White-Box Testing - Core Metadata Models
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/core/models.py (ModelWithMetadata)
"""
import pytest
from decimal import Decimal

from saleor.core.models import ModelWithMetadata
from saleor.product.models import Product, ProductType, Category


# ============================================
# TEST 1: ModelWithMetadata - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestModelWithMetadataStatementCoverage:
    """Test ModelWithMetadata methods for statement coverage"""
    
    def test_get_value_from_private_metadata_key_exists(self):
        """Statement Coverage: key exists in private_metadata -> return value"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1", "key2": "value2"}
        product.save()
        
        value = product.get_value_from_private_metadata("key1")
        assert value == "value1"
    
    def test_get_value_from_private_metadata_key_not_exists(self):
        """Statement Coverage: key not exists -> return default"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1"}
        product.save()
        
        value = product.get_value_from_private_metadata("key2", default="default_value")
        assert value == "default_value"
    
    def test_store_value_in_private_metadata_metadata_exists(self):
        """Statement Coverage: private_metadata exists -> update"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1"}
        product.save()
        
        product.store_value_in_private_metadata({"key2": "value2"})
        assert product.private_metadata["key1"] == "value1"
        assert product.private_metadata["key2"] == "value2"
    
    def test_store_value_in_private_metadata_metadata_none(self):
        """Statement Coverage: private_metadata is None -> create dict"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        # private_metadata defaults to {} not None, so we need to test the if not condition
        product.private_metadata = {}
        product.save()
        
        # Test when private_metadata is empty dict (falsy)
        product.store_value_in_private_metadata({"key1": "value1"})
        assert product.private_metadata["key1"] == "value1"
    
    def test_clear_private_metadata(self):
        """Statement Coverage: clear_private_metadata -> set to empty dict"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1", "key2": "value2"}
        product.save()
        
        product.clear_private_metadata()
        assert product.private_metadata == {}
    
    def test_delete_value_from_private_metadata_key_exists(self):
        """Statement Coverage: key exists -> delete and return True"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1", "key2": "value2"}
        product.save()
        
        result = product.delete_value_from_private_metadata("key1")
        assert result is True
        assert "key1" not in product.private_metadata
        assert "key2" in product.private_metadata
    
    def test_delete_value_from_private_metadata_key_not_exists(self):
        """Statement Coverage: key not exists -> return False"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1"}
        product.save()
        
        result = product.delete_value_from_private_metadata("key2")
        assert result is False
        assert "key1" in product.private_metadata
    
    def test_get_value_from_metadata_key_exists(self):
        """Statement Coverage: key exists in metadata -> return value"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1"}
        product.save()
        
        value = product.get_value_from_metadata("key1")
        assert value == "value1"
    
    def test_get_value_from_metadata_key_not_exists(self):
        """Statement Coverage: key not exists -> return default"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1"}
        product.save()
        
        value = product.get_value_from_metadata("key2", default="default")
        assert value == "default"
    
    def test_store_value_in_metadata_metadata_exists(self):
        """Statement Coverage: metadata exists -> update"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1"}
        product.save()
        
        product.store_value_in_metadata({"key2": "value2"})
        assert product.metadata["key1"] == "value1"
        assert product.metadata["key2"] == "value2"
    
    def test_store_value_in_metadata_metadata_none(self):
        """Statement Coverage: metadata is None -> create dict"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        # metadata defaults to {} not None, so we need to test the if not condition
        product.metadata = {}
        product.save()
        
        # Test when metadata is empty dict (falsy)
        product.store_value_in_metadata({"key1": "value1"})
        assert product.metadata["key1"] == "value1"
    
    def test_clear_metadata(self):
        """Statement Coverage: clear_metadata -> set to empty dict"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1", "key2": "value2"}
        product.save()
        
        product.clear_metadata()
        assert product.metadata == {}
    
    def test_delete_value_from_metadata_key_exists(self):
        """Statement Coverage: key exists -> delete"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1", "key2": "value2"}
        product.save()
        
        product.delete_value_from_metadata("key1")
        assert "key1" not in product.metadata
        assert "key2" in product.metadata
    
    def test_delete_value_from_metadata_key_not_exists(self):
        """Statement Coverage: key not exists -> no error"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1"}
        product.save()
        
        # Should not raise error
        product.delete_value_from_metadata("key2")
        assert "key1" in product.metadata


# ============================================
# TEST 2: ModelWithMetadata - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestModelWithMetadataDecisionCoverage:
    """Test all decision branches in ModelWithMetadata"""
    
    def test_decision_private_metadata_key_in_true(self):
        """Decision: key in private_metadata -> TRUE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key": "value"}
        product.save()
        
        result = product.delete_value_from_private_metadata("key")
        assert result is True
    
    def test_decision_private_metadata_key_in_false(self):
        """Decision: key not in private_metadata -> FALSE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        product.private_metadata = {"key1": "value1"}
        product.save()
        
        result = product.delete_value_from_private_metadata("key2")
        assert result is False
    
    def test_decision_metadata_key_in_true(self):
        """Decision: key in metadata -> TRUE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key": "value"}
        product.save()
        
        product.delete_value_from_metadata("key")
        assert "key" not in product.metadata
    
    def test_decision_metadata_key_in_false(self):
        """Decision: key not in metadata -> FALSE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        product.metadata = {"key1": "value1"}
        product.save()
        
        product.delete_value_from_metadata("key2")
        assert "key1" in product.metadata


# ============================================
# TEST 3: PublishableModel.is_visible - Statement & Decision Coverage
# ============================================
@pytest.mark.django_db
class TestPublishableModelIsVisible:
    """Test PublishableModel.is_visible property"""
    
    def test_is_visible_published_true_published_at_none(self):
        """Statement Coverage: is_published=True, published_at=None -> True"""
        import datetime
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=None
        )
        
        assert product.is_visible is True
    
    def test_is_visible_published_true_published_at_past(self):
        """Statement Coverage: is_published=True, published_at <= now -> True"""
        import datetime
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=1)
        )
        
        assert product.is_visible is True
    
    def test_is_visible_published_true_published_at_future(self):
        """Statement Coverage: is_published=True, published_at > now -> False"""
        import datetime
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=1)
        )
        
        assert product.is_visible is False
    
    def test_is_visible_published_false(self):
        """Statement Coverage: is_published=False -> False"""
        import datetime
        
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category,
            is_published=False,
            published_at=datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=1)
        )
        
        assert product.is_visible is False

