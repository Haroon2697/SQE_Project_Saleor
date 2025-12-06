"""
White-Box Testing - Account Utils
Tests for Statement Coverage, Decision Coverage, and MC/DC Coverage

Target Files:
- saleor/account/utils.py
"""
import pytest
from unittest.mock import Mock, patch
from django.conf import settings

from saleor.account.models import User, Address
from saleor.account.utils import (
    store_user_address,
    is_user_address_limit_reached,
    remove_the_oldest_user_address_if_address_limit_is_reached,
    remove_the_oldest_user_address
)
from saleor.checkout import AddressType


# ============================================
# TEST 1: is_user_address_limit_reached - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestIsUserAddressLimitReached:
    """Test is_user_address_limit_reached() for statement coverage"""
    
    def test_address_limit_not_reached(self):
        """Statement Coverage: count < MAX_USER_ADDRESSES"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        # Create addresses below limit
        Address.objects.create(
            user=user,
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="City",
            country="US"
        )
        
        result = is_user_address_limit_reached(user)
        assert result is False
    
    def test_address_limit_reached(self):
        """Statement Coverage: count >= MAX_USER_ADDRESSES"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        # Create addresses up to limit
        max_addresses = getattr(settings, 'MAX_USER_ADDRESSES', 5)
        for i in range(max_addresses):
            Address.objects.create(
                user=user,
                first_name=f"John{i}",
                last_name="Doe",
                street_address_1=f"{i} Main St",
                city="City",
                country="US"
            )
        
        result = is_user_address_limit_reached(user)
        assert result is True


# ============================================
# TEST 2: store_user_address - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestStoreUserAddress:
    """Test store_user_address() for statement coverage"""
    
    def test_store_address_limit_reached(self):
        """Statement Coverage: address limit reached -> return early"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        # Create addresses up to limit
        max_addresses = getattr(settings, 'MAX_USER_ADDRESSES', 5)
        for i in range(max_addresses):
            Address.objects.create(
                user=user,
                first_name=f"John{i}",
                last_name="Doe",
                street_address_1=f"{i} Main St",
                city="City",
                country="US"
            )
        
        address = Address(
            first_name="New",
            last_name="User",
            street_address_1="999 New St",
            city="City",
            country="US"
        )
        
        manager = Mock()
        store_user_address(user, address, AddressType.BILLING, manager)
        
        # Should not create new address
        assert user.addresses.count() == max_addresses
    
    def test_store_address_existing_address(self):
        """Statement Coverage: address already exists"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        address = Address.objects.create(
            user=user,
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="City",
            country="US"
        )
        
        manager = Mock()
        store_user_address(user, address, AddressType.BILLING, manager)
        
        # Should not create duplicate
        assert user.addresses.count() == 1
    
    def test_store_address_new_address_billing(self):
        """Statement Coverage: new address, billing type, no default"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        address = Address(
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="City",
            country="US"
        )
        
        manager = Mock()
        store_user_address(user, address, AddressType.BILLING, manager)
        
        # Should create address and set as default billing
        assert user.addresses.count() == 1
        assert user.default_billing_address is not None
    
    def test_store_address_new_address_shipping(self):
        """Statement Coverage: new address, shipping type, no default"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        address = Address(
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="City",
            country="US"
        )
        
        manager = Mock()
        store_user_address(user, address, AddressType.SHIPPING, manager)
        
        # Should create address and set as default shipping
        assert user.addresses.count() == 1
        assert user.default_shipping_address is not None
    
    def test_store_address_billing_with_existing_default(self):
        """Statement Coverage: billing type, default already exists"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        # Create existing default billing address
        existing = Address.objects.create(
            user=user,
            first_name="Existing",
            last_name="User",
            street_address_1="123 Old St",
            city="City",
            country="US"
        )
        user.default_billing_address = existing
        user.save()
        
        address = Address(
            first_name="New",
            last_name="User",
            street_address_1="999 New St",
            city="City",
            country="US"
        )
        
        manager = Mock()
        store_user_address(user, address, AddressType.BILLING, manager)
        
        # Should create address but not change default
        assert user.addresses.count() == 2
        assert user.default_billing_address == existing


# ============================================
# TEST 3: remove_the_oldest_user_address_if_address_limit_is_reached - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestRemoveOldestAddressIfLimitReached:
    """Test remove_the_oldest_user_address_if_address_limit_is_reached()"""
    
    def test_remove_if_limit_reached(self):
        """Statement Coverage: limit reached -> remove oldest"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        max_addresses = getattr(settings, 'MAX_USER_ADDRESSES', 5)
        
        # Create addresses up to limit
        addresses = []
        for i in range(max_addresses):
            addr = Address.objects.create(
                user=user,
                first_name=f"John{i}",
                last_name="Doe",
                street_address_1=f"{i} Main St",
                city="City",
                country="US"
            )
            addresses.append(addr)
        
        oldest_id = addresses[0].id
        
        remove_the_oldest_user_address_if_address_limit_is_reached(user)
        
        # Oldest should be removed
        assert not Address.objects.filter(id=oldest_id).exists()
        assert user.addresses.count() == max_addresses - 1
    
    def test_remove_if_limit_not_reached(self):
        """Statement Coverage: limit not reached -> do nothing"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        Address.objects.create(
            user=user,
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="City",
            country="US"
        )
        
        initial_count = user.addresses.count()
        remove_the_oldest_user_address_if_address_limit_is_reached(user)
        
        # Should not remove anything
        assert user.addresses.count() == initial_count


# ============================================
# TEST 4: remove_the_oldest_user_address - Statement Coverage
# ============================================
@pytest.mark.django_db
class TestRemoveOldestUserAddress:
    """Test remove_the_oldest_user_address() for statement coverage"""
    
    def test_remove_oldest_not_default(self):
        """Statement Coverage: oldest is not default -> remove"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        oldest = Address.objects.create(
            user=user,
            first_name="Oldest",
            last_name="User",
            street_address_1="1 Old St",
            city="City",
            country="US"
        )
        
        newer = Address.objects.create(
            user=user,
            first_name="Newer",
            last_name="User",
            street_address_1="2 New St",
            city="City",
            country="US"
        )
        
        user.default_billing_address = newer
        user.save()
        
        remove_the_oldest_user_address(user)
        
        # Oldest should be removed
        assert not Address.objects.filter(id=oldest.id).exists()
        assert Address.objects.filter(id=newer.id).exists()
    
    def test_remove_oldest_is_default(self):
        """Statement Coverage: oldest is default -> skip and remove next"""
        user = User.objects.create_user(
            email="test@example.com",
            password="test123"
        )
        
        oldest = Address.objects.create(
            user=user,
            first_name="Oldest",
            last_name="User",
            street_address_1="1 Old St",
            city="City",
            country="US"
        )
        
        newer = Address.objects.create(
            user=user,
            first_name="Newer",
            last_name="User",
            street_address_1="2 New St",
            city="City",
            country="US"
        )
        
        user.default_billing_address = oldest
        user.default_shipping_address = oldest
        user.save()
        
        remove_the_oldest_user_address(user)
        
        # Oldest should remain (it's default)
        assert Address.objects.filter(id=oldest.id).exists()
        # Newer should be removed instead
        assert not Address.objects.filter(id=newer.id).exists()

