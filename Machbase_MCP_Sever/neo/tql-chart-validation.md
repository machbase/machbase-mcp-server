# TQL Chart Validation Guide

## Overview

When creating charts with TQL, several common issues can cause blank charts, runtime errors, or incorrect visualizations. This guide explains how to validate TQL chart scripts to detect and fix these issues before execution.

**Key Concept**: HTTP 200 response with a `chartID` does **not** guarantee that a chart renders correctly. The chart may still be blank due to data mismatches or invalid column references.

---

## Common TQL Chart Issues

### Issue Types and Status Codes

| Issue Type | Description | Status Code |
|------------|-------------|-------------|
| **No Data** | SQL query returns 0 rows | `NO_DATA` |
| **Invalid Column** | `column(N)` where N ≥ actual column count | `INVALID_COLUMN` |
| **Negative Index** | Using `column(-1)` or other negative indices | `NEGATIVE_INDEX` |
| **Empty Chart** | `chartOption({})` or missing series definition | `EMPTY_CHART` |
| **Valid** | All checks pass | `OK` |
| **Error** | Execution or parsing error | `ERROR` |

---

## 4-Step Validation Process

### Step 1: Data Existence Check

**Purpose**: Verify that the data source returns actual records.

**What to Check**:
- SQL queries must return at least 1 row
- FAKE data must have valid dimensions
- Column count must be determinable

**SQL Data Sources**:

```js
// Extract and execute the SQL query
SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)

// Validation checks:
// 1. Execute: SELECT COUNT(*) FROM (original query)
// 2. If count = 0 → STATUS: NO_DATA
// 3. Execute: SELECT * FROM (original query) LIMIT 1
// 4. Count columns in result set
```

**FAKE Data Sources**:

```js
// Validation analyzes the FAKE() patterns
FAKE(arrange(0, 100, 1))
MAPVALUE(1, sin(value(0)))
MAPVALUE(2, cos(value(0)))

// Detection patterns:
// - arrange(start, end, step) → rows = (end-start)/step
// - linspace(start, end, count) → rows = count
// - MAPVALUE(N, ...) → columns include index N+1
```

**Result**:
- ✓ Query data: 100 rows × 3 columns
- ✗ Query returned no data (STATUS: NO_DATA)

---

### Step 2: Column Reference Validation

**Purpose**: Validate that all `column(N)` references are within valid range.

**What to Check**:
- Find all `column(N)` calls in `CHART()` sections
- Verify `0 ≤ N < column_count`
- Detect negative indices like `column(-1)`

**Valid Column References**:

```js
SQL(`SELECT time, value FROM example LIMIT 10`)
// Returns: 2 columns (time, value)
// Valid range: column(0) to column(1)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },  // ✓ Valid
        series: [{ data: column(1) }]              // ✓ Valid
    })
)
```

**Invalid Column References**:

```js
SQL(`SELECT time, value FROM example LIMIT 10`)
// Returns: 2 columns (time, value)
// Valid range: column(0) to column(1)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(2) }]              // ✗ Invalid: column(2) doesn't exist
    })
)
```

**Negative Index Detection**:

```js
FAKE(linspace(0, 10, 5))
CHART(
    chartOption({
        series: [{ data: column(-1) }]             // ✗ Invalid: negative index
    })
)
```

**Result**:
- ✓ All column references valid: [0, 1]
- ✗ Invalid column references found: [2, 5]
- ✗ Negative column indices found: [-1]

---

### Step 3: Empty Chart Option Check

**Purpose**: Detect empty or incomplete chart configurations.

**Empty Patterns**:

```js
// Pattern 1: Completely empty chartOption
CHART(
    chartOption({})                                // ✗ Empty
)

// Pattern 2: No series defined
CHART(
    chartOption({
        xAxis: { type: "category" },
        yAxis: {}
        // Missing: series
    })
)
```

**Valid Chart Option**:

```js
CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [                                   // ✓ Series defined
            { type: "line", data: column(1) }
        ]
    })
)
```

**Result**:
- ✓ Chart options present
- ✗ Empty chartOption detected

---

### Step 4: Auto-Fix Capability

**Purpose**: Automatically generate corrected TQL scripts.

**Fix 1: Negative Indices → 0**

```js
// Original (INVALID)
CHART(
    chartOption({
        series: [{ data: column(-1) }]
    })
)

// Fixed
CHART(
    chartOption({
        series: [{ data: column(0) }]  // Fixed: was column(-1)
    })
)
```

**Fix 2: Out of Range → Nearest Valid Column**

```js
// Data: 3 columns (0, 1, 2)

// Original (INVALID)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(5) }  // Out of range
        ]
    })
)

// Fixed
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(2) }  // Fixed: was column(5)
        ]
    })
)
```

**Fix 3: Empty Chart → Default Time-Series Template**

```js
// Data: 2 columns (time, value)

// Original (EMPTY)
CHART(chartOption({}))

// Fixed: Complete time-series chart with data transformation
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)

CHART(
    chartOption({
        title: { text: "Time Series Chart" },
        xAxis: { 
            type: "time",
            name: "Time"
        },
        yAxis: { 
            type: "value",
            name: "Value"
        },
        tooltip: { trigger: "axis" },
        series: [{ 
            type: "line", 
            data: column(0),
            smooth: true
        }]
    })
)
```

**Fix 4: Add Data Transformation (when needed)**

For 3-column data `[name, time, value]`:

```js
// Added transformation
MAPVALUE(0, list(value(1), value(2)))
POPVALUE(1, 2)

CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(0) }]
    })
)
```

---

## Validation Report Format

### Report Structure

```
=== TQL CHART VALIDATION REPORT ===

[STEP 1] DATA EXISTENCE CHECK
✓ Query data: 100 rows × 2 columns

[STEP 2] COLUMN REFERENCE VALIDATION
✓ All column references valid: [0, 1]
  Valid range: column(0) to column(1)

[STEP 3] EMPTY CHART OPTION CHECK
✓ Chart options present

=== VALIDATION RESULT ===
STATUS: OK
DATA: 100 rows × 2 columns

=== ORIGINAL TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { type: "time", data: column(0) },
        series: [{ data: column(1) }]
    })
)
```
```

### Report with Issues

```
=== TQL CHART VALIDATION REPORT ===

[STEP 1] DATA EXISTENCE CHECK
✓ Query data: 100 rows × 2 columns

[STEP 2] COLUMN REFERENCE VALIDATION
✗ Invalid column references found: [3]
  Valid range: column(0) to column(1)

[STEP 3] EMPTY CHART OPTION CHECK
✓ Chart options present

=== VALIDATION RESULT ===
STATUS: INVALID_COLUMN
DATA: 100 rows × 2 columns
ISSUES: Out of range: [3]
FIXED: Yes

=== ORIGINAL TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(3) }
        ]
    })
)
```

=== FIXED TQL ===
```tql
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(1) }  // Fixed: was column(3)
        ]
    })
)
```

✓ Use the fixed TQL above to avoid chart errors
```

---

## Runtime Validation Script

When runtime validation is enabled, validation code is prepended to the TQL:

```js
// === Auto-generated validation script ===
SCRIPT({
    console.log("Validating chart data dimensions...");
    console.log("Expected columns: 3");
}, {
    if ($.values.length < 3) {
        console.warn("Data has only " + $.values.length + " columns, expected 3");
    }
    $.yield.apply($, $.values);
})

SQL(`SELECT name, time, value FROM example`)
CHART(
    chartOption({
        xAxis: { data: column(1) },
        series: [{ data: column(2) }]
    })
)
```

This helps debug production issues where data dimensions change unexpectedly.

---

## Best Practices

### 1. Always Validate Before Execution

**Workflow**:

```
1. Write TQL script
2. Validate script (check for issues)
3. If issues found:
   - Use auto-fixed version
   - Or manually correct the script
4. Execute validated TQL
5. Verify chart renders correctly
```

### 2. Understanding column() vs value()

**Critical Difference**:

| Function | Usage | Returns | Example |
|----------|-------|---------|---------|
| `value(N)` | Pipeline middle | Single value from current record | `value(0)` = `10` |
| `column(N)` | Inside CHART() only | Array of all values from column N | `column(0)` = `[1,2,3,4,5]` |

**Example**:

```js
SQL(`SELECT time, value FROM example`)
// During pipeline: each record has 2 values
// value(0) = time of current record
// value(1) = value of current record

MAPVALUE(1, value(1) * 100)  // ✓ Correct: transforms each record

CHART(
    chartOption({
        xAxis: { data: column(0) },  // ✓ Correct: collects all time values
        series: [{ data: column(1) }]  // ✓ Correct: collects all value values
    })
)
```

### 3. Check Data Structure First

Before writing `CHART()`, verify your data structure:

```js
SQL(`SELECT time, value FROM example LIMIT 10`)
CSV()  // Preview: see actual columns and values
```

Output:
```csv
1699920000000000000,10.5
1699920001000000000,11.3
1699920002000000000,9.8
...
```

Now you know:
- Column 0: time (timestamp)
- Column 1: value (number)
- Valid range: `column(0)` to `column(1)`

### 4. Handle Multi-Column Data Properly

**For 3-column data** `[name, time, value]`:

```js
SQL(`SELECT name, time, value FROM example`)
// 3 columns: column(0)=name, column(1)=time, column(2)=value

// Option 1: Transform to [time, value] pairs
MAPVALUE(0, list(value(1), value(2)))
POPVALUE(1, 2)
CHART(
    chartOption({
        xAxis: { type: "time" },
        series: [{ data: column(0) }]  // Now column(0) = [time, value]
    })
)

// Option 2: Use separate columns
CHART(
    chartOption({
        xAxis: { type: "time", data: column(1) },
        series: [{ data: column(2) }]
    })
)
```

### 5. Avoid Common Mistakes

**❌ Wrong: Using column() outside CHART()**

```js
SQL(`SELECT time, value FROM example`)
MAPVALUE(1, column(1) * 100)  // ERROR: column() not available here
```

**✓ Correct: Use value() in pipeline**

```js
SQL(`SELECT time, value FROM example`)
MAPVALUE(1, value(1) * 100)   // ✓ Correct
```

**❌ Wrong: Forbidden syntax - column(N, M)**

```js
CHART(
    chartOption({
        series: [{ data: column(0, 1) }]  // ERROR: column(N, M) doesn't exist
    })
)
```

**✓ Correct: Use list() in pipeline**

```js
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    chartOption({
        series: [{ data: column(0) }]  // ✓ column(0) now contains [time, value] pairs
    })
)
```

**❌ Wrong: Assuming data structure**

```js
// Assuming 3 columns without verification
SQL(`SELECT * FROM example`)
CHART(
    chartOption({
        series: [
            { data: column(1) },
            { data: column(2) }
        ]
    })
)
```

**✓ Correct: Verify first, then use**

```js
// Step 1: Check structure
SQL(`SELECT * FROM example LIMIT 1`)
CSV()  // See actual columns

// Step 2: Validate before CHART()
// Use validation to confirm column count

// Step 3: Use confirmed indices
SQL(`SELECT * FROM example`)
CHART(
    chartOption({
        series: [
            { data: column(1) },  // ✓ Verified safe
            { data: column(2) }   // ✓ Verified safe
        ]
    })
)
```

---

## Debugging Blank Charts

### Common Causes and Solutions

**1. HTTP 200 + chartID but blank chart**

**Problem**: Response looks successful but chart doesn't render.

**Diagnosis**:
- Run validation to check column references
- Most common cause: `column(N)` where N ≥ actual columns

**Solution**:
```js
// Check validation report for INVALID_COLUMN status
// Use auto-fixed version or correct manually
```

**2. Data exists but chart shows nothing**

**Problem**: SQL returns data but series is empty.

**Diagnosis**:
- Check if data transformation is needed
- Verify xAxis type matches data format

**Solution**:
```js
// For time-series data
MAPVALUE(0, list(value(0), value(1)))  // Create [time, value] pairs
POPVALUE(1)
CHART(
    chartOption({
        xAxis: { type: "time" },       // Match data type
        series: [{ data: column(0) }]
    })
)
```

**3. Empty chartOption**

**Problem**: `chartOption({})` or missing series.

**Diagnosis**:
- Validation report shows EMPTY_CHART status

**Solution**:
```js
// Use auto-fixed version with default template
// Or manually add complete chart configuration
CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [{ type: "line", data: column(1) }]
    })
)
```

---

## Examples

### Example 1: Valid Simple Chart

**TQL Script**:

```js
FAKE(linspace(0, 10, 11))
MAPVALUE(1, value(0) * value(0))

CHART(
    chartOption({
        xAxis: { data: column(0) },
        yAxis: {},
        series: [
            { type: "line", data: column(1) }
        ]
    })
)
```

**Validation Result**:

```
STATUS: OK
DATA: 11 rows × 2 columns
```

---

### Example 2: Invalid Column Reference

**TQL Script**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(2) },  // Invalid!
            { data: column(3) }   // Invalid!
        ]
    })
)
```

**Validation Result**:

```
STATUS: INVALID_COLUMN
DATA: 100 rows × 2 columns
ISSUES: Out of range: [2, 3]
```

**Fixed Version**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [
            { data: column(1) },
            { data: column(1) },  // Fixed: was column(2)
            { data: column(1) }   // Fixed: was column(3)
        ]
    })
)
```

---

### Example 3: Empty Chart Option

**TQL Script**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)
CHART(chartOption({}))
```

**Validation Result**:

```
STATUS: EMPTY_CHART
DATA: 100 rows × 2 columns
ISSUES: Empty chartOption (no series or completely empty)
```

**Fixed Version**:

```js
SQL(`SELECT time, value FROM example LIMIT 100`)

MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)

CHART(
    chartOption({
        title: { text: "Time Series Chart" },
        xAxis: { 
            type: "time",
            name: "Time"
        },
        yAxis: { 
            type: "value",
            name: "Value"
        },
        tooltip: { trigger: "axis" },
        series: [{ 
            type: "line", 
            data: column(0),
            smooth: true
        }]
    })
)
```

---

### Example 4: No Data Returned

**TQL Script**:

```js
SQL(`SELECT time, value FROM example WHERE name = 'nonexistent'`)

CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

**Validation Result**:

```
STATUS: NO_DATA
REASON: SQL query returned 0 rows
SQL: SELECT time, value FROM example WHERE name = 'nonexistent'
```

**Solution**: Fix the WHERE clause or data insertion.

---

### Example 5: Negative Column Index

**TQL Script**:

```js
FAKE(linspace(0, 10, 5))

CHART(
    chartOption({
        series: [{ data: column(-1) }]
    })
)
```

**Validation Result**:

```
STATUS: NEGATIVE_INDEX
DATA: 5 rows × 1 columns
ISSUES: Negative indices: [-1]
```

**Fixed Version**:

```js
FAKE(linspace(0, 10, 5))

CHART(
    chartOption({
        series: [{ data: column(0) }]  // Fixed: was column(-1)
    })
)
```

---

## Validation Workflow in Practice

### Complete Development Cycle

**Step 1: Write initial TQL**

```js
SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

**Step 2: Validate the script**

```
Request validation check
→ Receives validation report
→ Check STATUS field
```

**Step 3: Handle validation result**

**If STATUS: OK**
```
→ Execute TQL directly
→ Verify chart renders
```

**If STATUS: INVALID_COLUMN, NEGATIVE_INDEX, or EMPTY_CHART**
```
→ Review FIXED TQL section
→ Use fixed version
→ Execute fixed TQL
→ Verify chart renders
```

**If STATUS: NO_DATA**
```
→ Check SQL query
→ Verify table name and WHERE conditions
→ Check if data exists in database
→ Fix query and revalidate
```

**If STATUS: ERROR**
```
→ Review error message
→ Check TQL syntax
→ Fix errors and revalidate
```

**Step 4: Production deployment**

```js
// Optional: Add runtime validation for debugging
// This logs warnings if data dimensions change

// === Auto-generated validation script ===
SCRIPT({
    console.log("Validating chart data dimensions...");
    console.log("Expected columns: 2");
}, {
    if ($.values.length < 2) {
        console.warn("Data has only " + $.values.length + " columns, expected 2");
    }
    $.yield.apply($, $.values);
})

SQL(`SELECT time, value FROM example WHERE name = 'sensor01'`)
CHART(
    chartOption({
        xAxis: { data: column(0) },
        series: [{ data: column(1) }]
    })
)
```

---

## Summary

### Key Takeaways

1. **Always validate TQL chart scripts** before execution to prevent blank charts and runtime errors

2. **HTTP 200 + chartID ≠ successful chart** - validation is needed to ensure correct rendering

3. **Understand the validation process**:
   - Step 1: Data existence (rows and columns)
   - Step 2: Column references (valid indices)
   - Step 3: Empty chart options (missing series)
   - Step 4: Auto-fix (corrected TQL)

4. **Know the difference**:
   - `value(N)`: Single value in pipeline processing
   - `column(N)`: Array of values in CHART() only

5. **Common fixes**:
   - Negative indices → `column(0)`
   - Out of range → nearest valid column
   - Empty chartOption → default time-series template

6. **Best practice workflow**:
   - Write TQL → Validate → Fix if needed → Execute → Verify

7. **Use runtime validation** in production for debugging dimension mismatches

---

## Related Documentation

- [TQL Guide](tql-guide.md) - Complete TQL language reference
- [TQL Reference](tql-reference.md) - TQL syntax and operators  
- [Line Chart Examples](chart/line-chart.md) - Practical chart examples
- [CHART() Function](tql-sink.md) - Detailed CHART() function documentation
- [SCRIPT() Function](tql-script.md) - JavaScript processing in TQL
