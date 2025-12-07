# Why Files Are "Skipped" in Coverage Reports

## 📊 What "Skipped Due to Complete Coverage" Means

When you see:
```
233 files skipped due to complete coverage.
```

This is **GOOD NEWS**! It means:
- ✅ Those 233 files have **100% test coverage**
- ✅ They are excluded from the detailed report to reduce clutter
- ✅ The coverage tool only shows files that need attention

## 📈 Current Status

**Overall Coverage: 48%** (Target: 80%+)  
**Total Statements: 82,616**  
**Covered: 42,973**  
**Missing: 39,643**

## 🔍 Why Coverage is Only 48%

The remaining 48% gap comes from files that are **NOT skipped** because they have **less than 100% coverage**. These are the files shown in the detailed report.

### Biggest Gaps (Files Needing Tests):

1. **`saleor/checkout/complete_checkout.py`** - **15% coverage** (531 statements uncovered)
   - This is the **biggest single gap** in your codebase
   - Core checkout completion logic
   - **Priority: 🔴 CRITICAL**

2. **`saleor/checkout/calculations.py`** - **18% coverage** (214 statements uncovered)
   - Checkout price calculations
   - **Priority: 🔴 CRITICAL**

3. **`saleor/checkout/actions.py`** - **24% coverage** (77 statements uncovered)
   - Checkout actions
   - **Priority: 🔴 CRITICAL**

4. **`saleor/webhook/utils.py`** - **18% coverage** (127 statements uncovered)
   - Webhook utilities
   - **Priority: 🟡 HIGH**

5. **`saleor/asgi/`** - **0% coverage** (~200 statements)
   - ASGI handlers (production critical)
   - **Priority: 🔴 CRITICAL**

## 🎯 How to Increase Coverage

### Step 1: Focus on High-Impact Files

The files shown in the coverage report (not skipped) are the ones that need tests. Focus on:

1. **Checkout Module** (biggest impact)
   - `complete_checkout.py` - 531 statements uncovered
   - `calculations.py` - 214 statements uncovered
   - `actions.py` - 77 statements uncovered

2. **Webhook Module**
   - `webhook/utils.py` - 127 statements uncovered
   - `webhook/transport/` - Both sync and async

3. **ASGI Module**
   - All ASGI handlers - ~200 statements

### Step 2: View the HTML Report

Open the HTML coverage report to see exactly which lines need coverage:

```bash
# Open in browser:
file:///home/haroon/SQE/SQE_Project_Saleor/htmlcov/combined/index.html
```

The report shows:
- ✅ Green lines = Covered
- ❌ Red lines = Not covered
- Files with <100% coverage are shown in detail

### Step 3: Create Targeted Tests

For each file with low coverage:
1. Open the file in the HTML report
2. Identify red (uncovered) lines
3. Write tests that exercise those code paths
4. Re-run coverage to verify improvement

## 📊 Expected Impact

If you cover the top 5 modules:
- **Checkout complete_checkout.py**: +6.4% overall coverage
- **Checkout calculations.py**: +2.6% overall coverage
- **Checkout actions.py**: +0.9% overall coverage
- **Webhook utils.py**: +1.5% overall coverage
- **ASGI handlers**: +2.4% overall coverage

**Total Expected: 48% + 13.8% = ~62%**

To reach 80%, you'll need to cover additional modules (GraphQL, more integration tests, etc.)

## ✅ Summary

- **"Skipped" files = 100% covered** (good!)
- **Files shown in report = need tests** (focus here!)
- **Current coverage: 48%** (target: 80%+)
- **Biggest gap: checkout/complete_checkout.py** (531 statements)

Focus your testing efforts on the files shown in the coverage report, starting with the checkout module for maximum impact.

