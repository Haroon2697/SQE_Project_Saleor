# SQE Project Demo Guide - Saleor E-Commerce Platform

## Complete Demo Instructions & Demonstration Guide

---

## Table of Contents

1. [Pre-Demo Setup](#pre-demo-setup)
2. [Demo Flow Overview](#demo-flow-overview)
3. [Rubric-Based Demonstration](#rubric-based-demonstration)
4. [Commands Reference](#commands-reference)
5. [Troubleshooting](#troubleshooting)

---

## Pre-Demo Setup

### Step 1: Navigate to Project Directory

```bash
cd /home/haroon/SQE/SQE_Project_Saleor
```

### Step 2: Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Step 3: Verify Setup

```bash
# Check Python version
python --version

# Check pytest is installed
pytest --version

# Check coverage is installed
coverage --version
```

---

## Demo Flow Overview

| Time | Section | Rubric Points |
|------|---------|---------------|
| 0-5 min | Test Plan Overview | 20 pts |
| 5-12 min | Test Coverage Demo | 20 pts |
| 12-17 min | CI/CD Pipeline | 15 pts |
| 17-22 min | Test Execution | 15 pts |
| 22-27 min | Documentation | 10 pts |
| 27-32 min | Deployment | 10 pts |
| 32-35 min | Team Collaboration | 10 pts |

---

## Rubric-Based Demonstration

---

## 1. Test Plan Quality (20 Points)

### What to Show:

#### A. Show Test Plan Document

```bash
# Open the test plan document
cat doc/01_TEST_PLAN_DOCUMENT.md
```

#### B. Explain Test Strategy

**White-Box Testing Strategy:**
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- Decision Coverage

**Black-Box Testing Strategy:**
- API Endpoint Testing
- GraphQL Query/Mutation Testing
- Boundary Value Testing
- Error Handling Testing

#### C. Show Test Files Structure

```bash
# Show whitebox test files
ls -la tests/whitebox/

# Count total test files
find tests/ -name "test_*.py" | wc -l

# Show blackbox test files
ls -la tests/blackbox/
```

#### D. Demonstrate Test Categories

```bash
# Show different coverage types
ls tests/whitebox/test_*_coverage.py

# Show statement coverage tests
head -50 tests/whitebox/test_statement_coverage.py

# Show branch coverage tests
head -50 tests/whitebox/test_branch_coverage.py

# Show MC/DC coverage tests
head -50 tests/whitebox/test_mcdc_coverage.py
```

**Key Points to Mention:**
- IEEE 829 Test Plan Standard followed
- Comprehensive coverage criteria defined
- Test cases mapped to requirements
- Risk-based testing approach

---

## 2. Test Coverage (20 Points)

### What to Show:

#### A. Run White-Box Tests with Coverage

```bash
# Run all whitebox tests with coverage report
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate

python -m pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=term \
    --override-ini="addopts=" \
    -v --tb=short 2>&1 | head -100
```

#### B. Show Coverage Summary

```bash
# Run with summary output
python -m pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=term \
    --override-ini="addopts=" \
    -q --tb=no 2>&1 | tail -20
```

#### C. Generate HTML Coverage Report

```bash
# Generate detailed HTML report
python -m pytest tests/whitebox/ \
    --cov=saleor \
    --cov-report=html:htmlcov \
    --override-ini="addopts=" \
    -q --tb=no

# Open in browser (if GUI available)
# firefox htmlcov/index.html
```

#### D. Show Coverage by Module

```bash
# Show coverage for specific modules
python -m pytest tests/whitebox/ \
    --cov=saleor.core \
    --cov=saleor.order \
    --cov=saleor.payment \
    --cov-report=term \
    --override-ini="addopts=" \
    -q --tb=no 2>&1 | tail -30
```

**Key Points to Mention:**
- Current coverage: ~48% of 82,619 lines
- 1,000+ test cases written
- Coverage includes core utilities, GraphQL, payments, orders
- Explain why some modules have lower coverage (require database, external APIs)

---

## 3. Tool Integration - CI/CD (15 Points)

### What to Show:

#### A. Show GitHub Actions Workflow

```bash
# Show CI/CD configuration
cat .github/workflows/test.yml
```

#### B. Explain Pipeline Stages

```bash
# Show pipeline documentation
cat doc/02_CI_CD_PIPELINE_CONFIGURATION.md
```

#### C. Show Pipeline Structure

**Pipeline Stages:**
1. **Source** - Code checkout from repository
2. **Build** - Install dependencies
3. **Test** - Run pytest with coverage
4. **Report** - Generate coverage reports
5. **Deploy** - Deploy to staging/production

#### D. Show Docker Configuration

```bash
# Show Dockerfile
cat Dockerfile

# Show docker-compose
cat docker-compose.yml
```

**Key Points to Mention:**
- Automated testing on every push
- Coverage thresholds enforced
- Docker containerization for consistency
- Parallel test execution support

---

## 4. Test Execution (15 Points)

### What to Show:

#### A. Run Quick Test Suite

```bash
# Run a quick subset of tests
python -m pytest tests/whitebox/test_statement_coverage.py \
    tests/whitebox/test_branch_coverage.py \
    --override-ini="addopts=" \
    -v --tb=short
```

#### B. Run Full White-Box Test Suite

```bash
# Run all whitebox tests
python -m pytest tests/whitebox/ \
    --override-ini="addopts=" \
    -v --tb=short 2>&1 | head -50
```

#### C. Run Black-Box Tests

```bash
# Run blackbox tests
python -m pytest tests/blackbox/ \
    --override-ini="addopts=" \
    -v --tb=short
```

#### D. Run Specific Test Categories

```bash
# Run statement coverage tests only
python -m pytest tests/whitebox/test_statement_coverage.py -v

# Run integration tests
python -m pytest tests/whitebox/test_integration_coverage.py -v

# Run MC/DC tests
python -m pytest tests/whitebox/test_mcdc_coverage.py -v
```

#### E. Show Test Results Summary

```bash
# Run with summary
python -m pytest tests/whitebox/ tests/blackbox/ \
    --override-ini="addopts=" \
    -q --tb=no 2>&1 | tail -10
```

**Key Points to Mention:**
- All tests passing (1,000+ tests)
- Test execution time reasonable
- Clear pass/fail reporting
- Detailed error messages on failures

---

## 5. Documentation & Deliverables (10 Points)

### What to Show:

#### A. Show Documentation Structure

```bash
# List all documentation files
ls -la doc/

# Show main documents
cat doc/01_TEST_PLAN_DOCUMENT.md | head -100
cat doc/02_CI_CD_PIPELINE_CONFIGURATION.md | head -50
cat doc/03_TEST_RESULTS_AND_REPORTS.md | head -50
cat doc/04_DEPLOYMENT_INSTRUCTIONS.md | head -50
```

#### B. Show Test Report

```bash
# Show test results document
cat doc/03_TEST_RESULTS_AND_REPORTS.md
```

#### C. Show LaTeX Report (if compiled)

```bash
# Show LaTeX files
ls doc/*.tex

# Show main report structure
cat doc/PROJECT_REPORT_MAIN.tex | head -50
```

#### D. Show README

```bash
# Show project README
cat README.md | head -100
```

**Key Points to Mention:**
- Complete documentation for all deliverables
- Test Plan (IEEE 829 format)
- CI/CD Configuration documented
- Test Results with metrics
- Deployment Instructions

---

## 6. Deployment & Monitoring (10 Points)

### What to Show:

#### A. Show Deployment Documentation

```bash
cat doc/04_DEPLOYMENT_INSTRUCTIONS.md
```

#### B. Show Docker Deployment

```bash
# Show Docker configuration
cat Dockerfile
cat docker-compose.yml

# Explain deployment steps:
# 1. Build Docker image
# docker build -t saleor-app .

# 2. Run with docker-compose
# docker-compose up -d

# 3. Check status
# docker-compose ps
```

#### C. Show Environment Configuration

```bash
# Show environment variables
cat .env.example 2>/dev/null || echo "Environment configuration in docker-compose.yml"
```

#### D. Explain Monitoring Approach

**Monitoring Points:**
- Application logs via Docker
- Test coverage reports
- CI/CD pipeline status
- Error tracking

**Key Points to Mention:**
- Docker-based deployment
- Staging and production environments
- Environment variable configuration
- Health check endpoints

---

## 7. Team Collaboration & Progress (10 Points)

### What to Show:

#### A. Show Git History

```bash
# Show recent commits
git log --oneline -20

# Show commit statistics
git shortlog -sn

# Show branches
git branch -a
```

#### B. Show Progress Documentation

```bash
# Show progress tracking
cat doc/PROJECT_STATUS_REPORT.md 2>/dev/null || echo "See documentation folder"
```

#### C. Show Test Evolution

```bash
# Count test files
echo "Total test files:"
find tests/ -name "test_*.py" | wc -l

# Count test functions
echo "Total test functions:"
grep -r "def test_" tests/ | wc -l
```

**Key Points to Mention:**
- Regular commits and progress
- Clear task distribution
- Version control best practices
- Incremental development approach

---

## Commands Reference

### Quick Demo Commands

```bash
# 1. Setup
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate

# 2. Run all tests with coverage
python -m pytest tests/whitebox/ --cov=saleor --cov-report=term --override-ini="addopts=" -q --tb=no

# 3. Run specific coverage type tests
python -m pytest tests/whitebox/test_statement_coverage.py -v
python -m pytest tests/whitebox/test_branch_coverage.py -v
python -m pytest tests/whitebox/test_mcdc_coverage.py -v

# 4. Run blackbox tests
python -m pytest tests/blackbox/ -v --override-ini="addopts="

# 5. Generate HTML report
python -m pytest tests/whitebox/ --cov=saleor --cov-report=html:htmlcov --override-ini="addopts=" -q --tb=no

# 6. Show test count
find tests/ -name "test_*.py" | wc -l
grep -r "def test_" tests/ | wc -l
```

### Coverage Commands

```bash
# Full coverage report
python -m pytest tests/whitebox/ tests/unit/ --cov=saleor --cov-report=term --override-ini="addopts=" -q --tb=no

# Coverage for specific module
python -m pytest tests/whitebox/ --cov=saleor.core --cov-report=term --override-ini="addopts=" -q --tb=no

# HTML report
python -m pytest tests/whitebox/ --cov=saleor --cov-report=html:htmlcov --override-ini="addopts=" -q --tb=no
```

---

## Troubleshooting

### Common Issues

#### 1. Virtual Environment Not Activated

```bash
source .venv/bin/activate
```

#### 2. Import Errors

```bash
# Ensure you're in the right directory
cd /home/haroon/SQE/SQE_Project_Saleor
```

#### 3. Pytest Configuration Conflicts

```bash
# Use override-ini to bypass config issues
python -m pytest tests/whitebox/ --override-ini="addopts=" -v
```

#### 4. Coverage Not Found

```bash
pip install pytest-cov coverage
```

---

## Demo Script (5-Minute Quick Demo)

```bash
# STEP 1: Setup (30 seconds)
cd /home/haroon/SQE/SQE_Project_Saleor
source .venv/bin/activate

# STEP 2: Show test structure (30 seconds)
echo "=== Test Structure ==="
ls tests/
ls tests/whitebox/ | head -10

# STEP 3: Run tests with coverage (2 minutes)
echo "=== Running Tests with Coverage ==="
python -m pytest tests/whitebox/ --cov=saleor --cov-report=term --override-ini="addopts=" -q --tb=no 2>&1 | tail -20

# STEP 4: Show documentation (1 minute)
echo "=== Documentation ==="
ls doc/

# STEP 5: Show test count (30 seconds)
echo "=== Test Statistics ==="
echo "Test files: $(find tests/ -name 'test_*.py' | wc -l)"
echo "Test functions: $(grep -r 'def test_' tests/ | wc -l)"
```

---

## Expected Demo Output

### Test Execution Output

```
=================== test session starts ===================
collected 1076 items

tests/whitebox/test_statement_coverage.py ......
tests/whitebox/test_branch_coverage.py ........
tests/whitebox/test_mcdc_coverage.py ......
...

=================== 1076 passed in 20.69s ===================
```

### Coverage Output

```
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
saleor/core/utils/__init__.py            150     30    80%
saleor/core/prices.py                     45     10    78%
saleor/payment/interface.py              272      2    99%
...
-----------------------------------------------------------
TOTAL                                  82619  42570    48%
```

---

## Key Talking Points for Each Rubric Item

### 1. Test Plan Quality (20 pts)
- "We followed IEEE 829 standard for test planning"
- "Our test plan covers both white-box and black-box testing"
- "We have defined coverage criteria: Statement, Branch, MC/DC, Decision"

### 2. Test Coverage (20 pts)
- "We achieved 48% coverage on 82,619 lines of code"
- "We have 1,076+ test cases covering core functionality"
- "Coverage includes utilities, payments, orders, shipping"

### 3. CI/CD Integration (15 pts)
- "GitHub Actions automates our test pipeline"
- "Docker ensures consistent deployment environments"
- "Pipeline includes build, test, and deploy stages"

### 4. Test Execution (15 pts)
- "All 1,076 tests pass successfully"
- "Tests run in ~20 seconds"
- "We have organized tests by coverage type"

### 5. Documentation (10 pts)
- "Complete documentation for all deliverables"
- "Test plan, CI/CD config, results, deployment docs"
- "LaTeX report for professional presentation"

### 6. Deployment (10 pts)
- "Docker-based deployment strategy"
- "Staging and production environment support"
- "Environment configuration documented"

### 7. Team Collaboration (10 pts)
- "Regular commits showing incremental progress"
- "Clear version control practices"
- "Comprehensive test evolution"

---

## Good Luck with Your Demo!

