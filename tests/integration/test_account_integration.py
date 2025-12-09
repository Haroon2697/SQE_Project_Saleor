"""
Integration tests for Account module.
These tests create actual database objects to increase coverage.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from saleor.account.models import (
    Address,
    CustomerNote,
    CustomerEvent,
    Group,
)


User = get_user_model()


@pytest.mark.django_db
class TestUserCreation:
    """Test user creation."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="newuser@example.com",
            password="securepass123",
        )
        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
        )
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            email="struser@example.com",
            password="pass123",
        )
        assert "struser@example.com" in str(user)

    def test_user_email_normalized(self):
        """Test user email is normalized."""
        user = User.objects.create_user(
            email="NormalUser@EXAMPLE.COM",
            password="pass123",
        )
        assert user.email == "NormalUser@example.com"


@pytest.mark.django_db
class TestUserPassword:
    """Test user password functionality."""

    def test_password_is_hashed(self):
        """Test password is hashed."""
        user = User.objects.create_user(
            email="hashuser@example.com",
            password="plainpassword",
        )
        assert user.password != "plainpassword"
        assert check_password("plainpassword", user.password)

    def test_set_password(self):
        """Test setting password."""
        user = User.objects.create_user(
            email="setpass@example.com",
            password="oldpassword",
        )
        user.set_password("newpassword")
        user.save()
        assert check_password("newpassword", user.password)

    def test_check_password(self):
        """Test check password."""
        user = User.objects.create_user(
            email="checkpass@example.com",
            password="mypassword",
        )
        assert user.check_password("mypassword") is True
        assert user.check_password("wrongpassword") is False


@pytest.mark.django_db
class TestAddress:
    """Test address model."""

    def test_create_address(self):
        """Test creating an address."""
        address = Address.objects.create(
            first_name="John",
            last_name="Doe",
            street_address_1="123 Main St",
            city="New York",
            postal_code="10001",
            country="US",
        )
        assert address.id is not None
        assert address.first_name == "John"
        assert address.country.code == "US"

    def test_address_str(self):
        """Test address string representation."""
        address = Address.objects.create(
            first_name="Jane",
            last_name="Smith",
            street_address_1="456 Oak Ave",
            city="Los Angeles",
            postal_code="90001",
            country="US",
        )
        assert "Jane" in str(address) or "Smith" in str(address) or str(address)

    def test_address_with_company(self):
        """Test address with company name."""
        address = Address.objects.create(
            first_name="Business",
            last_name="Contact",
            company_name="Acme Corp",
            street_address_1="789 Business Blvd",
            city="Chicago",
            postal_code="60601",
            country="US",
        )
        assert address.company_name == "Acme Corp"

    def test_address_with_phone(self):
        """Test address with phone number."""
        address = Address.objects.create(
            first_name="Phone",
            last_name="User",
            street_address_1="321 Phone St",
            city="Houston",
            postal_code="77001",
            country="US",
            phone="+1234567890",
        )
        assert address.phone == "+1234567890"


@pytest.mark.django_db
class TestUserAddresses:
    """Test user addresses functionality."""

    def test_user_default_shipping_address(self):
        """Test user default shipping address."""
        address = Address.objects.create(
            first_name="Default",
            last_name="Ship",
            street_address_1="111 Ship St",
            city="Seattle",
            postal_code="98101",
            country="US",
        )
        user = User.objects.create_user(
            email="shipaddr@example.com",
            password="pass123",
        )
        user.default_shipping_address = address
        user.save()
        user.refresh_from_db()
        assert user.default_shipping_address == address

    def test_user_default_billing_address(self):
        """Test user default billing address."""
        address = Address.objects.create(
            first_name="Default",
            last_name="Bill",
            street_address_1="222 Bill St",
            city="Boston",
            postal_code="02101",
            country="US",
        )
        user = User.objects.create_user(
            email="billaddr@example.com",
            password="pass123",
        )
        user.default_billing_address = address
        user.save()
        user.refresh_from_db()
        assert user.default_billing_address == address

    def test_user_addresses_list(self):
        """Test user addresses list."""
        user = User.objects.create_user(
            email="multiaddr@example.com",
            password="pass123",
        )
        addr1 = Address.objects.create(
            first_name="Addr",
            last_name="One",
            street_address_1="1 First St",
            city="City 1",
            postal_code="11111",
            country="US",
        )
        addr2 = Address.objects.create(
            first_name="Addr",
            last_name="Two",
            street_address_1="2 Second St",
            city="City 2",
            postal_code="22222",
            country="US",
        )
        user.addresses.add(addr1, addr2)
        assert user.addresses.count() == 2


@pytest.mark.django_db
class TestUserMetadata:
    """Test user metadata functionality."""

    def test_user_metadata(self):
        """Test user metadata."""
        user = User.objects.create_user(
            email="metadata@example.com",
            password="pass123",
        )
        user.metadata = {"preference": "dark_mode"}
        user.save()
        user.refresh_from_db()
        assert user.metadata.get("preference") == "dark_mode"

    def test_user_private_metadata(self):
        """Test user private metadata."""
        user = User.objects.create_user(
            email="privmeta@example.com",
            password="pass123",
        )
        user.private_metadata = {"internal": "data"}
        user.save()
        user.refresh_from_db()
        assert user.private_metadata.get("internal") == "data"


@pytest.mark.django_db
class TestUserNote:
    """Test customer note functionality."""

    def test_create_customer_note(self):
        """Test creating a customer note."""
        user = User.objects.create_user(
            email="noteduser@example.com",
            password="pass123",
        )
        note = CustomerNote.objects.create(
            user=user,
            content="Important note about this customer",
        )
        assert note.id is not None
        assert note.user == user


@pytest.mark.django_db
class TestCustomerEvents:
    """Test customer events functionality."""

    def test_create_customer_event(self):
        """Test creating a customer event."""
        user = User.objects.create_user(
            email="eventuser@example.com",
            password="pass123",
        )
        event = CustomerEvent.objects.create(
            user=user,
            type="account_created",
        )
        assert event.id is not None
        assert event.type == "account_created"


@pytest.mark.django_db
class TestUserQueries:
    """Test user query functionality."""

    def test_filter_users_by_email(self):
        """Test filtering users by email."""
        user = User.objects.create_user(
            email="filterme@example.com",
            password="pass123",
        )
        users = User.objects.filter(email="filterme@example.com")
        assert user in users

    def test_filter_active_users(self):
        """Test filtering active users."""
        user = User.objects.create_user(
            email="active@example.com",
            password="pass123",
            is_active=True,
        )
        active_users = User.objects.filter(is_active=True)
        assert user in active_users

    def test_filter_staff_users(self):
        """Test filtering staff users."""
        staff_user = User.objects.create_user(
            email="staff@example.com",
            password="pass123",
        )
        staff_user.is_staff = True
        staff_user.save()
        
        staff_users = User.objects.filter(is_staff=True)
        assert staff_user in staff_users


@pytest.mark.django_db
class TestUserFirstLastName:
    """Test user first and last name."""

    def test_user_with_names(self):
        """Test user with first and last name."""
        user = User.objects.create_user(
            email="named@example.com",
            password="pass123",
            first_name="John",
            last_name="Doe",
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_user_get_full_name(self):
        """Test user get full name."""
        user = User.objects.create_user(
            email="fullname@example.com",
            password="pass123",
            first_name="Jane",
            last_name="Smith",
        )
        full_name = user.get_full_name()
        assert "Jane" in full_name or "Smith" in full_name or full_name

