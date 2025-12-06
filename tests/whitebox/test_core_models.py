"""
White-Box Testing - Core Models
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/core/models.py (SortableModel, PublishableModel)
"""
import pytest
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta

from saleor.core.models import SortableModel, PublishableModel
from saleor.product.models import ProductType, Category, Product, ProductVariant
from saleor.channel.models import Channel
from saleor.product.models import ProductVariantChannelListing
from prices import Money


# ============================================
# TEST 1: SortableModel - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestSortableModelStatementCoverage:
    """Test SortableModel.save() and delete() for statement coverage"""
    
    def test_save_new_object_no_existing_max(self):
        """Statement Coverage: Test save() when pk is None and existing_max is None"""
        # Create a concrete implementation of SortableModel
        category = Category.objects.create(name="Test Category", slug="test-category")
        
        # Verify sort_order is set to 0 (since existing_max is None)
        assert category.sort_order == 0
    
    def test_save_new_object_with_existing_max(self):
        """Statement Coverage: Test save() when pk is None and existing_max exists"""
        # Use CollectionProduct which inherits from SortableModel
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            product_type=product_type,
            category=category
        )
        
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        # Create first CollectionProduct
        cp1 = CollectionProduct.objects.create(collection=collection, product=product1)
        assert cp1.sort_order == 0
        
        # Create second CollectionProduct (existing_max exists)
        cp2 = CollectionProduct.objects.create(collection=collection, product=product2)
        assert cp2.sort_order == 1
    
    def test_save_existing_object(self):
        """Statement Coverage: Test save() when pk is not None (skip sort_order logic)"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        original_sort_order = collection_product.sort_order
        
        # Update existing object (pk is not None)
        collection_product.save()
        
        # sort_order should remain unchanged
        assert collection_product.sort_order == original_sort_order
    
    def test_delete_with_sort_order(self):
        """Statement Coverage: Test delete() when sort_order is not None"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            product_type=product_type,
            category=category
        )
        
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            product_type=product_type,
            category=category
        )
        
        product3 = Product.objects.create(
            name="Product 3",
            slug="product-3",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        # Create multiple CollectionProducts
        cp1 = CollectionProduct.objects.create(collection=collection, product=product1)
        cp2 = CollectionProduct.objects.create(collection=collection, product=product2)
        cp3 = CollectionProduct.objects.create(collection=collection, product=product3)
        
        assert cp1.sort_order == 0
        assert cp2.sort_order == 1
        assert cp3.sort_order == 2
        
        # Delete middle one
        cp2.delete()
        
        # Verify cp3's sort_order decreased
        cp3.refresh_from_db()
        assert cp3.sort_order == 1
    
    def test_delete_without_sort_order(self):
        """Statement Coverage: Test delete() when sort_order is None"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        collection_product.sort_order = None
        collection_product.save()
        
        # Should not raise error
        collection_product.delete()
        assert not CollectionProduct.objects.filter(pk=collection_product.pk).exists()


# ============================================
# TEST 2: SortableModel - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestSortableModelDecisionCoverage:
    """Test all decision branches in SortableModel"""
    
    def test_decision_coverage_save_pk_none_true(self):
        """Decision Coverage: if self.pk is None -> TRUE branch"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        # Create new (pk is None during save)
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        assert collection_product.sort_order is not None
    
    def test_decision_coverage_save_pk_none_false(self):
        """Decision Coverage: if self.pk is None -> FALSE branch"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        original_sort = collection_product.sort_order
        
        # Update existing (pk is not None)
        collection_product.save()
        assert collection_product.sort_order == original_sort
    
    def test_decision_coverage_delete_sort_order_not_none_true(self):
        """Decision Coverage: if self.sort_order is not None -> TRUE branch"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            product_type=product_type,
            category=category
        )
        
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        cp1 = CollectionProduct.objects.create(collection=collection, product=product1)
        cp2 = CollectionProduct.objects.create(collection=collection, product=product2)
        
        cp1.delete()  # sort_order is not None
        cp2.refresh_from_db()
        assert cp2.sort_order == 0  # Decreased from 1 to 0
    
    def test_decision_coverage_delete_sort_order_not_none_false(self):
        """Decision Coverage: if self.sort_order is not None -> FALSE branch"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        collection_product.sort_order = None
        collection_product.save()
        
        # Delete should work without updating other sort_orders
        collection_product.delete()


# ============================================
# TEST 3: SortableModel - MC/DC Coverage
# ============================================
@pytest.mark.django_db
class TestSortableModelMCDC:
    """Modified Condition/Decision Coverage for SortableModel"""
    
    def test_mcdc_get_max_sort_order_none(self):
        """MC/DC: existing_max is None -> return 0"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Product",
            slug="product",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        collection_product = CollectionProduct.objects.create(
            collection=collection,
            product=product
        )
        assert collection_product.sort_order == 0
    
    def test_mcdc_get_max_sort_order_exists(self):
        """MC/DC: existing_max exists -> return existing_max + 1"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product1 = Product.objects.create(
            name="Product 1",
            slug="product-1",
            product_type=product_type,
            category=category
        )
        
        product2 = Product.objects.create(
            name="Product 2",
            slug="product-2",
            product_type=product_type,
            category=category
        )
        
        collection = Collection.objects.create(
            name="Collection",
            slug="collection"
        )
        
        cp1 = CollectionProduct.objects.create(collection=collection, product=product1)
        cp2 = CollectionProduct.objects.create(collection=collection, product=product2)
        assert cp2.sort_order == cp1.sort_order + 1


# ============================================
# TEST 4: PublishableModel - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestPublishableModelStatementCoverage:
    """Test PublishableModel.published() queryset for statement coverage"""
    
    def test_published_with_published_at_in_past(self):
        """Statement Coverage: published_at <= today AND is_published = True"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Published Product",
            slug="published-product",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() - timedelta(days=1)  # Past date
        )
        
        published = Product.objects.published()
        assert product in published
    
    def test_published_with_published_at_null(self):
        """Statement Coverage: published_at is null AND is_published = True"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Published No Date",
            slug="published-no-date",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=None
        )
        
        published = Product.objects.published()
        assert product in published
    
    def test_published_with_published_at_future(self):
        """Statement Coverage: published_at > today -> NOT published"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Future Product",
            slug="future-product",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1)  # Future date
        )
        
        published = Product.objects.published()
        assert product not in published
    
    def test_published_with_is_published_false(self):
        """Statement Coverage: is_published = False -> NOT published"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Unpublished Product",
            slug="unpublished-product",
            product_type=product_type,
            category=category,
            is_published=False,
            published_at=timezone.now() - timedelta(days=1)
        )
        
        published = Product.objects.published()
        assert product not in published


# ============================================
# TEST 5: PublishableModel - Decision Coverage
# ============================================
@pytest.mark.django_db
class TestPublishableModelDecisionCoverage:
    """Test all decision branches in PublishableModel.published()"""
    
    def test_decision_published_at_lte_today_true(self):
        """Decision: published_at <= today -> TRUE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Past Date",
            slug="past-date",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() - timedelta(hours=1)
        )
        
        assert product in Product.objects.published()
    
    def test_decision_published_at_lte_today_false(self):
        """Decision: published_at <= today -> FALSE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Future Date",
            slug="future-date",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1)
        )
        
        assert product not in Product.objects.published()
    
    def test_decision_published_at_isnull_true(self):
        """Decision: published_at is null -> TRUE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Null Date",
            slug="null-date",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=None
        )
        
        assert product in Product.objects.published()
    
    def test_decision_is_published_true(self):
        """Decision: is_published = True -> TRUE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Published",
            slug="published",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() - timedelta(days=1)
        )
        
        assert product in Product.objects.published()
    
    def test_decision_is_published_false(self):
        """Decision: is_published = False -> FALSE"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="Unpublished",
            slug="unpublished",
            product_type=product_type,
            category=category,
            is_published=False,
            published_at=timezone.now() - timedelta(days=1)
        )
        
        assert product not in Product.objects.published()


# ============================================
# TEST 6: PublishableModel - MC/DC Coverage
# ============================================
@pytest.mark.django_db
class TestPublishableModelMCDC:
    """Modified Condition/Decision Coverage for PublishableModel"""
    
    def test_mcdc_condition_a_true_b_true(self):
        """MC/DC: (published_at <= today OR published_at is null) AND is_published = True"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="MC/DC Test 1",
            slug="mcdc-1",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() - timedelta(days=1)
        )
        
        assert product in Product.objects.published()
    
    def test_mcdc_condition_a_false_b_true(self):
        """MC/DC: (published_at > today AND published_at is not null) AND is_published = True"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="MC/DC Test 2",
            slug="mcdc-2",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=timezone.now() + timedelta(days=1)
        )
        
        assert product not in Product.objects.published()
    
    def test_mcdc_condition_a_true_b_false(self):
        """MC/DC: (published_at <= today OR published_at is null) AND is_published = False"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="MC/DC Test 3",
            slug="mcdc-3",
            product_type=product_type,
            category=category,
            is_published=False,
            published_at=timezone.now() - timedelta(days=1)
        )
        
        assert product not in Product.objects.published()
    
    def test_mcdc_condition_null_date(self):
        """MC/DC: published_at is null -> TRUE (OR condition)"""
        product_type = ProductType.objects.create(name="Type", slug="type")
        category = Category.objects.create(name="Cat", slug="cat")
        
        product = Product.objects.create(
            name="MC/DC Test 4",
            slug="mcdc-4",
            product_type=product_type,
            category=category,
            is_published=True,
            published_at=None
        )
        
        assert product in Product.objects.published()

