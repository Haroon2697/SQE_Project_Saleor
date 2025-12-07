# Coverage Analysis and Improvement Plan

## 📊 Current Status

**Overall Coverage: 49%** (Target: 80%+)  
**Gap: 31%** (Need to cover ~25,000+ more statements)

---

## 🔍 Why Coverage is Only 49%

### 1. **Large Untested Modules**

The Saleor codebase has **82,616 total statements**, but many critical modules have **0% or very low coverage**:

#### **Zero Coverage Modules (0%)**:
- `saleor/asgi/` - **All files 0%** (asgi_handler, cors_handler, gzip_compression, health_check, telemetry)
  - **Impact:** High - ASGI is critical for production deployment
  - **Lines:** ~200+ statements
  - **Priority:** 🔴 **CRITICAL**

- `saleor/__main__.py` - 0% (4 statements)
- `saleor/channel/tasks/saleor3_22.py` - 0% (7 statements)

#### **Very Low Coverage (<20%)**:
- `saleor/checkout/complete_checkout.py` - **15%** (628 statements, only 97 covered)
  - **Impact:** 🔴 **CRITICAL** - Core checkout completion logic
  - **Gap:** 531 statements uncovered
  
- `saleor/checkout/calculations.py` - **18%** (262 statements, only 48 covered)
  - **Impact:** 🔴 **CRITICAL** - Checkout price calculations
  - **Gap:** 214 statements uncovered

- `saleor/checkout/actions.py` - **24%** (101 statements, only 24 covered)
  - **Impact:** 🔴 **CRITICAL** - Checkout actions
  - **Gap:** 77 statements uncovered

- `saleor/webhook/utils.py` - **18%** (155 statements, only 28 covered)
  - **Impact:** 🔴 **HIGH** - Webhook utilities
  - **Gap:** 127 statements uncovered

- `saleor/webhook/transport/synchronous/transport.py` - **26%**
- `saleor/webhook/transport/asynchronous/transport.py` - **22%**
- `saleor/webhook/response_schemas/transaction.py` - **11%**

- `saleor/app/installation_utils.py` - **27%** (169 statements, only 45 covered)
- `saleor/app/manifest_validations.py` - **18%** (247 statements, only 44 covered)
- `saleor/app/tasks.py` - **29%** (75 statements, only 22 covered)

- `saleor/attribute/utils.py` - **14%** (100 statements, only 14 covered)
- `saleor/checkout/payment_utils.py` - **21%** (67 statements, only 14 covered)

#### **Low Coverage (20-40%)**:
- `saleor/account/notifications.py` - **21%** (72 statements)
- `saleor/account/tasks.py` - **40%** (58 statements)
- `saleor/account/throttling.py` - **33%** (70 statements)
- `saleor/account/utils.py` - **45%** (119 statements)
- `saleor/checkout/fetch.py` - **38%** (325 statements)
- `saleor/checkout/problems.py` - **39%** (90 statements)
- `saleor/checkout/tasks.py` - **0%** (102 statements)

### 2. **GraphQL Module (Huge Codebase)**

The `saleor/graphql/` module has **10,743+ classes/functions** but likely has low overall coverage:
- Many GraphQL resolvers, mutations, and types
- Complex integration points
- Requires full Django/GraphQL setup

**Estimated Coverage:** ~40-50% (needs verification)

### 3. **Missing Test Categories**

1. **Integration Tests** - Testing modules together
2. **Error Handling Tests** - Edge cases and error conditions
3. **Async/Background Tasks** - Celery tasks, async operations
4. **API Endpoint Tests** - Full request/response cycles

---

## 🎯 Improvement Strategy

### **Phase 1: Critical Business Logic (Target: +15% coverage)**

**Priority 1: Checkout Module** (Highest Impact)
- `complete_checkout.py` - 531 statements uncovered
- `calculations.py` - 214 statements uncovered
- `actions.py` - 77 statements uncovered
- **Expected Impact:** +10% overall coverage

**Priority 2: Webhook Module** (High Impact)
- `webhook/utils.py` - 127 statements uncovered
- `webhook/transport/` - Both sync and async transports
- **Expected Impact:** +3% overall coverage

**Priority 3: ASGI Module** (Production Critical)
- All ASGI handlers - ~200 statements
- **Expected Impact:** +2% overall coverage

### **Phase 2: Supporting Modules (Target: +10% coverage)**

**Priority 4: App Module**
- `installation_utils.py` - 124 statements uncovered
- `manifest_validations.py` - 203 statements uncovered
- `tasks.py` - 53 statements uncovered

**Priority 5: Account Module**
- `notifications.py` - 57 statements uncovered
- `tasks.py` - 35 statements uncovered
- `throttling.py` - 47 statements uncovered

**Priority 6: Attribute Module**
- `utils.py` - 86 statements uncovered

### **Phase 3: GraphQL and Integration (Target: +6% coverage)**

**Priority 7: GraphQL Core**
- GraphQL mutations and resolvers
- Integration with business logic

**Priority 8: Integration Tests**
- End-to-end scenarios
- Multi-module interactions

---

## 📝 Action Plan

### **Step 1: Create Tests for Critical Checkout Module**

**Files to Create:**
1. `tests/whitebox/test_checkout_complete_checkout_comprehensive.py`
   - Test `complete_checkout()` function
   - Test all checkout completion paths
   - Test error handling
   - **Target:** 80%+ coverage for `complete_checkout.py`

2. `tests/whitebox/test_checkout_calculations_extensive.py`
   - Test all calculation functions
   - Test edge cases
   - **Target:** 80%+ coverage for `calculations.py`

3. `tests/whitebox/test_checkout_actions_extensive.py`
   - Test all action functions
   - **Target:** 80%+ coverage for `actions.py`

### **Step 2: Create Tests for Webhook Module**

**Files to Create:**
1. `tests/whitebox/test_webhook_utils_extensive.py`
   - Test all utility functions
   - Test webhook filtering and retrieval
   - **Target:** 80%+ coverage for `webhook/utils.py`

2. `tests/whitebox/test_webhook_transport_sync.py`
   - Test synchronous webhook delivery
   - **Target:** 80%+ coverage

3. `tests/whitebox/test_webhook_transport_async.py`
   - Test asynchronous webhook delivery
   - **Target:** 80%+ coverage

### **Step 3: Create Tests for ASGI Module**

**Files to Create:**
1. `tests/whitebox/test_asgi_handlers.py`
   - Test ASGI handler
   - Test CORS handler
   - Test gzip compression
   - Test health check
   - **Target:** 80%+ coverage for all ASGI files

### **Step 4: Create Tests for App Module**

**Files to Create:**
1. `tests/whitebox/test_app_installation_utils.py`
   - Test app installation utilities
   - **Target:** 80%+ coverage

2. `tests/whitebox/test_app_manifest_validations.py`
   - Test manifest validation
   - **Target:** 80%+ coverage

### **Step 5: Create Tests for Account Module**

**Files to Create:**
1. `tests/whitebox/test_account_notifications.py`
   - Test notification functions
   - **Target:** 80%+ coverage

2. `tests/whitebox/test_account_tasks.py`
   - Test background tasks
   - **Target:** 80%+ coverage

---

## 📈 Expected Coverage Improvements

| Module | Current | Target | Statements to Cover | Expected Impact |
|--------|---------|--------|---------------------|-----------------|
| **Checkout (complete_checkout)** | 15% | 80% | 531 | +6.4% overall |
| **Checkout (calculations)** | 18% | 80% | 214 | +2.6% overall |
| **Checkout (actions)** | 24% | 80% | 77 | +0.9% overall |
| **Webhook (utils)** | 18% | 80% | 127 | +1.5% overall |
| **Webhook (transport)** | 22-26% | 80% | ~100 | +1.2% overall |
| **ASGI (all)** | 0% | 80% | 200 | +2.4% overall |
| **App (installation)** | 27% | 80% | 124 | +1.5% overall |
| **App (manifest)** | 18% | 80% | 203 | +2.5% overall |
| **Account (notifications)** | 21% | 80% | 57 | +0.7% overall |
| **Account (tasks)** | 40% | 80% | 35 | +0.4% overall |
| **Attribute (utils)** | 14% | 80% | 86 | +1.0% overall |
| **TOTAL** | | | **~1,765** | **+20.1%** |

**Projected Final Coverage: 49% + 20% = 69%**

**To reach 80%:** Need additional ~9,000 statements covered (likely from GraphQL and integration tests)

---

## 🚀 Implementation Priority

### **Week 1: Critical Checkout Module**
1. ✅ `test_checkout_complete_checkout_comprehensive.py`
2. ✅ `test_checkout_calculations_extensive.py`
3. ✅ `test_checkout_actions_extensive.py`

### **Week 2: Webhook and ASGI**
1. ✅ `test_webhook_utils_extensive.py`
2. ✅ `test_webhook_transport_sync.py`
3. ✅ `test_webhook_transport_async.py`
4. ✅ `test_asgi_handlers.py`

### **Week 3: App and Account Modules**
1. ✅ `test_app_installation_utils.py`
2. ✅ `test_app_manifest_validations.py`
3. ✅ `test_account_notifications.py`
4. ✅ `test_account_tasks.py`

### **Week 4: Remaining Modules**
1. ✅ `test_attribute_utils_extensive.py`
2. ✅ GraphQL integration tests
3. ✅ End-to-end integration tests

---

## ✅ Success Criteria

1. **Coverage Target:** 80%+ overall
2. **Critical Modules:** 80%+ coverage for:
   - Checkout module
   - Webhook module
   - ASGI module
3. **Test Quality:** All tests passing, comprehensive edge case coverage
4. **CI/CD Integration:** All tests run in pipeline

---

## 📊 Monitoring Progress

After each test file is created:
1. Run coverage: `pytest tests/ --cov=saleor --cov-report=html`
2. Check coverage report: `htmlcov/index.html`
3. Verify target module coverage increased
4. Update this document with actual coverage numbers

---

## 🎯 Next Steps

1. **Start with Checkout Module** - Highest impact
2. **Create comprehensive test files** - One module at a time
3. **Run and verify coverage** - After each file
4. **Iterate** - Continue until 80%+ coverage achieved

