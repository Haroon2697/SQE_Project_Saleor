"""
Integration tests for Tax module.
These tests create actual database objects to increase coverage.
"""
import pytest
from decimal import Decimal

from saleor.tax.models import (
    TaxClass,
    TaxClassCountryRate,
    TaxConfiguration,
    TaxConfigurationPerCountry,
)
from saleor.channel.models import Channel


@pytest.fixture
def channel(db):
    """Create a test channel."""
    return Channel.objects.create(
        name="Tax Channel",
        slug="tax-channel",
        currency_code="USD",
        is_active=True,
    )


@pytest.mark.django_db
class TestTaxClass:
    """Test tax class functionality."""

    def test_create_tax_class(self):
        """Test creating a tax class."""
        tax_class = TaxClass.objects.create(
            name="Standard Rate",
        )
        assert tax_class.id is not None
        assert tax_class.name == "Standard Rate"

    def test_tax_class_str(self):
        """Test tax class string representation."""
        tax_class = TaxClass.objects.create(name="Reduced Rate")
        assert str(tax_class) == "Reduced Rate"

    def test_multiple_tax_classes(self):
        """Test multiple tax classes."""
        TaxClass.objects.create(name="Standard")
        TaxClass.objects.create(name="Reduced")
        TaxClass.objects.create(name="Zero")
        
        assert TaxClass.objects.count() >= 3


@pytest.mark.django_db
class TestTaxClassCountryRate:
    """Test tax class country rate functionality."""

    def test_create_country_rate(self):
        """Test creating a country rate."""
        tax_class = TaxClass.objects.create(name="VAT")
        rate = TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="US",
            rate=Decimal("7.00"),
        )
        assert rate.id is not None
        assert rate.rate == Decimal("7.00")

    def test_multiple_country_rates(self):
        """Test multiple country rates for one tax class."""
        tax_class = TaxClass.objects.create(name="Multi Rate")
        TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="US",
            rate=Decimal("7.00"),
        )
        TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="CA",
            rate=Decimal("13.00"),
        )
        TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="GB",
            rate=Decimal("20.00"),
        )
        
        assert tax_class.country_rates.count() == 3

    def test_zero_rate(self):
        """Test zero rate."""
        tax_class = TaxClass.objects.create(name="Zero Rate")
        rate = TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="US",
            rate=Decimal("0.00"),
        )
        assert rate.rate == Decimal("0.00")


@pytest.mark.django_db
class TestTaxConfiguration:
    """Test tax configuration functionality."""

    def test_create_tax_configuration(self, channel):
        """Test creating a tax configuration."""
        config = TaxConfiguration.objects.create(
            channel=channel,
            charge_taxes=True,
            display_gross_prices=True,
        )
        assert config.id is not None
        assert config.charge_taxes is True

    def test_tax_configuration_no_charge(self, channel):
        """Test tax configuration without charging taxes."""
        config = TaxConfiguration.objects.create(
            channel=channel,
            charge_taxes=False,
            display_gross_prices=False,
        )
        assert config.charge_taxes is False

    def test_tax_configuration_prices_entered_with_tax(self, channel):
        """Test tax configuration with prices entered with tax."""
        config = TaxConfiguration.objects.create(
            channel=channel,
            charge_taxes=True,
            prices_entered_with_tax=True,
        )
        assert config.prices_entered_with_tax is True


@pytest.mark.django_db
class TestTaxConfigurationPerCountry:
    """Test tax configuration per country functionality."""

    def test_create_country_config(self, channel):
        """Test creating a country-specific tax configuration."""
        config = TaxConfiguration.objects.create(
            channel=channel,
            charge_taxes=True,
        )
        country_config = TaxConfigurationPerCountry.objects.create(
            tax_configuration=config,
            country="US",
            charge_taxes=True,
        )
        assert country_config.id is not None
        assert country_config.country.code == "US"

    def test_multiple_country_configs(self, channel):
        """Test multiple country configurations."""
        config = TaxConfiguration.objects.create(
            channel=channel,
            charge_taxes=True,
        )
        TaxConfigurationPerCountry.objects.create(
            tax_configuration=config,
            country="US",
            charge_taxes=True,
        )
        TaxConfigurationPerCountry.objects.create(
            tax_configuration=config,
            country="CA",
            charge_taxes=True,
        )
        
        assert config.country_exceptions.count() == 2


@pytest.mark.django_db
class TestTaxClassMetadata:
    """Test tax class metadata."""

    def test_tax_class_metadata(self):
        """Test tax class metadata."""
        tax_class = TaxClass.objects.create(name="Meta Tax")
        tax_class.metadata = {"tax_authority": "IRS"}
        tax_class.save()
        tax_class.refresh_from_db()
        assert tax_class.metadata.get("tax_authority") == "IRS"


@pytest.mark.django_db
class TestTaxQueries:
    """Test tax query functionality."""

    def test_filter_tax_classes_by_name(self):
        """Test filtering tax classes by name."""
        tax_class = TaxClass.objects.create(name="Filter Test")
        tax_classes = TaxClass.objects.filter(name="Filter Test")
        assert tax_class in tax_classes

    def test_filter_country_rates_by_country(self):
        """Test filtering country rates by country."""
        tax_class = TaxClass.objects.create(name="Country Filter")
        rate = TaxClassCountryRate.objects.create(
            tax_class=tax_class,
            country="DE",
            rate=Decimal("19.00"),
        )
        rates = TaxClassCountryRate.objects.filter(country="DE")
        assert rate in rates

