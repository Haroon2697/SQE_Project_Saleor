# Saleor E-Commerce Platform - SQE Project

A modular, high performance, headless e-commerce platform built with Python, GraphQL, Django, and React.

## Project Overview

This repository contains the Software Quality Engineering (SQE) project implementation for the Saleor e-commerce platform. The project focuses on comprehensive testing, CI/CD integration, and quality assurance practices.

## Features

- **GraphQL API**: Flexible and powerful API for frontend integration
- **Django Backend**: Robust Python-based backend framework
- **Headless Architecture**: Decoupled frontend and backend
- **Multi-channel Support**: Manage multiple sales channels
- **Extensive Plugin System**: Customizable functionality

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis (optional, for caching)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/SQE_Project_Saleor.git
cd SQE_Project_Saleor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or using uv:
uv sync
```

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all whitebox tests with coverage
python -m pytest tests/whitebox/ --cov=saleor --cov-report=term --override-ini="addopts=" -v

# Run blackbox tests
python -m pytest tests/blackbox/ --override-ini="addopts=" -v

# Generate HTML coverage report
python -m pytest tests/whitebox/ --cov=saleor --cov-report=html:htmlcov --override-ini="addopts="
```

## Project Structure

```
SQE_Project_Saleor/
├── saleor/                 # Main application code
│   ├── account/            # User account management
│   ├── checkout/           # Checkout process
│   ├── core/               # Core utilities
│   ├── discount/           # Discounts and promotions
│   ├── graphql/            # GraphQL API
│   ├── order/              # Order management
│   ├── payment/            # Payment processing
│   ├── plugins/            # Plugin system
│   ├── product/            # Product catalog
│   ├── shipping/           # Shipping methods
│   └── warehouse/          # Inventory management
├── tests/                  # Test suites
│   ├── whitebox/           # White-box tests (unit, coverage)
│   ├── blackbox/           # Black-box tests (API, integration)
│   └── unit/               # Unit tests
├── cypress/                # End-to-end tests
├── doc/                    # Documentation
│   ├── 01_TEST_PLAN_DOCUMENT.md
│   ├── 02_CI_CD_PIPELINE_CONFIGURATION.md
│   ├── 03_TEST_RESULTS_AND_REPORTS.md
│   └── 04_DEPLOYMENT_INSTRUCTIONS.md
└── .github/workflows/      # CI/CD configuration
```

## Testing Strategy

### White-Box Testing

- **Statement Coverage**: Testing all executable statements
- **Branch Coverage**: Testing all decision branches
- **MC/DC Coverage**: Modified Condition/Decision Coverage
- **Decision Coverage**: Testing all decision outcomes

### Black-Box Testing

- **API Testing**: GraphQL queries and mutations
- **Boundary Testing**: Edge case validation
- **Error Handling**: Exception and error scenarios

## Test Results

| Metric | Value |
|--------|-------|
| Total Tests | 1,076+ |
| Pass Rate | 100% |
| Code Coverage | 48% |
| Lines of Code | 82,619 |

## CI/CD Pipeline

The project includes a complete CI/CD pipeline using GitHub Actions:

1. **Source**: Code checkout from repository
2. **Build**: Install dependencies
3. **Test**: Run pytest with coverage
4. **Report**: Generate coverage reports
5. **Deploy**: Deploy to staging/production

## Documentation

- [Test Plan Document](doc/01_TEST_PLAN_DOCUMENT.md)
- [CI/CD Pipeline Configuration](doc/02_CI_CD_PIPELINE_CONFIGURATION.md)
- [Test Results and Reports](doc/03_TEST_RESULTS_AND_REPORTS.md)
- [Deployment Instructions](doc/04_DEPLOYMENT_INSTRUCTIONS.md)
- [Demo Guide](DEMO_GUIDE.md)

## Technology Stack

- **Backend**: Python 3.12, Django 5.x
- **API**: GraphQL with Graphene
- **Database**: PostgreSQL
- **Cache**: Redis
- **Testing**: pytest, pytest-cov, Cypress
- **CI/CD**: GitHub Actions, Docker

## License

BSD-3-Clause License

## Contributing

This is an academic project for Software Quality Engineering course.

## Contact

For questions regarding this SQE project, please contact the project team.

