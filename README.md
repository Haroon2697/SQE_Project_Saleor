# Saleor E-Commerce Platform - SQE Project

A comprehensive quality engineering project for the Saleor e-commerce platform, including automated testing, CI/CD pipeline, and deployment automation.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Setup & Configuration](#setup--configuration)
- [Documentation](#documentation)

## 🎯 Project Overview

This project implements a complete quality engineering solution for Saleor, including:

- **White-box Testing**: Comprehensive unit tests with Statement, Decision, and MC/DC coverage
- **Black-box Testing**: API integration tests and Cypress UI tests
- **CI/CD Pipeline**: 5-stage automated pipeline (Source, Build, Test, Staging, Deploy)
- **Test Coverage**: 80%+ coverage for business logic modules

## 🚀 Quick Start

### Prerequisites

- Ubuntu 20.04+
- Python 3.12
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Haroon2697/SQE_Project_Saleor.git
   cd SQE_Project_Saleor
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install .
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
SQE_Project_Saleor/
├── saleor/              # Saleor backend application
├── tests/               # Test suites
│   ├── unit/           # Unit tests (white-box)
│   ├── integration/    # Integration tests (black-box)
│   └── whitebox/       # Comprehensive white-box tests
├── cypress/             # Cypress UI tests
├── .github/workflows/   # CI/CD pipeline configurations
├── scripts/             # Deployment scripts
└── docs/                # Documentation
```

## 🧪 Testing

### Running Tests

**White-box Tests:**
```bash
./run_whitebox_tests.sh
# or
pytest tests/whitebox/ --cov=saleor --cov-report=html
```

**Integration Tests:**
```bash
pytest tests/integration/ -v
```

**UI Tests (Cypress):**
```bash
npm run cypress:open      # Interactive mode
npm run cypress:run      # Headless mode
```

### Test Coverage

- **HTML Coverage Report**: `htmlcov/whitebox/index.html`
- **XML Coverage Report**: `coverage-whitebox.xml`
- **Coverage Target**: 80%+ for business logic modules

## 🔄 CI/CD Pipeline

The project includes a 5-stage CI/CD pipeline:

1. **Source Stage**: Code validation and change detection
2. **Build Stage**: Dependency installation and artifact creation
3. **Test Stage**: Automated testing (Pytest + Cypress)
4. **Staging Stage**: Deployment to staging environment
5. **Deploy Stage**: Production deployment

**Pipeline File**: `.github/workflows/complete-cicd-pipeline.yml`

**View Pipeline**: Go to [GitHub Actions](https://github.com/Haroon2697/SQE_Project_Saleor/actions) → "🚀 Complete CI/CD Pipeline - 5 Stages"

## ⚙️ Setup & Configuration

### Environment Variables

Create a `.env` file with:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://saleor:saleor@localhost:5432/saleor
REDIS_URL=redis://localhost:6379/0
EMAIL_URL=console://
DEFAULT_FROM_EMAIL=noreply@example.com
```

### GitHub Secrets

For CI/CD pipeline, configure these secrets in GitHub:

- `DJANGO_SECRET_KEY`: Django secret key
- `DOCKER_HUB_USERNAME`: Docker Hub username
- `DOCKER_HUB_TOKEN`: Docker Hub personal access token
- `CYPRESS_RECORD_KEY`: Cypress record key (optional)

See `QUICK_SECRETS_SETUP.md` for detailed setup instructions.

## 📚 Documentation

### Essential Documentation

- **`PROJECT_STATUS.md`**: Current project status and completion tracking
- **`QA_TEST_REPORT.md`**: Comprehensive test report with coverage analysis
- **`COMPREHENSIVE_WHITEBOX_TESTING.md`**: Detailed white-box testing documentation
- **`COMPLETE_CICD_IMPLEMENTATION.md`**: Complete CI/CD pipeline documentation
- **`QUICK_SECRETS_SETUP.md`**: Quick guide for setting up GitHub Secrets

### Testing Documentation

- **White-box Tests**: Located in `tests/whitebox/`
  - Core models, utilities, calculations
  - Statement, Decision, and MC/DC coverage
  - 80%+ coverage for business logic

- **Black-box Tests**: Located in `tests/integration/`
  - API endpoint testing
  - GraphQL query validation
  - Response verification

- **UI Tests**: Located in `cypress/e2e/`
  - Login functionality
  - Navigation tests
  - Dashboard interactions

## 🛠️ Development

### Running Locally

1. **Start PostgreSQL:**
   ```bash
   sudo systemctl start postgresql
   ```

2. **Start Redis:**
   ```bash
   sudo systemctl start redis
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - GraphQL Playground: http://localhost:8000/graphql/
   - Admin Panel: http://localhost:8000/admin/

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=saleor --cov-report=html

# Specific test suite
pytest tests/whitebox/
pytest tests/integration/
```

## 📊 Test Coverage

Current coverage includes:

- **Core Models**: SortableModel, PublishableModel, Metadata
- **Product Models**: ProductVariant methods
- **Order Calculations**: Price calculations, discounts
- **Checkout Calculations**: Subtotal, total, delivery
- **Discount Utils**: Voucher and promotion logic
- **Account Utils**: User address management
- **Payment Utils**: Payment and transaction handling
- **Shipping Utils**: Shipping method calculations

## 🚢 Deployment

### Staging

```bash
./scripts/deploy-staging.sh
```

### Production

```bash
./scripts/deploy-production.sh
```

### Docker

```bash
docker build -t saleor:latest .
docker run -p 8000:8000 saleor:latest
```

## 📝 License

This project is licensed under the BSD-3-Clause License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## 🔒 Security

See [SECURITY.md](SECURITY.md) for security policies and reporting.

## 📞 Support

For issues and questions:
- GitHub Issues: https://github.com/Haroon2697/SQE_Project_Saleor/issues
- Documentation: See `docs/` directory

---

**Project Status**: ✅ Active Development  
**Last Updated**: 2025  
**Version**: 3.23.0-a.0
