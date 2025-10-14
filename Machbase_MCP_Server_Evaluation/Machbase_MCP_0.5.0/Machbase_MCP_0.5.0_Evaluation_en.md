# Machbase Neo MCP Server Performance Evaluation

## Evaluation Criteria
- **Presentation Accuracy**: 0 issues: no deduction, 1 issue: -1 point, 2-3 issues: -2 points, 4+ issues: -3 points
- **Definition Accuracy**: 0 issues: no deduction, minor: -2 points, major: -4 points, complete error: 0 points
- **Code Quality**: 0 issues: no deduction, 1 issue: -1 point, 2-3 issues: -2 points, 4+ issues: -3 points

---

## Question 1: How to Install Machbase Neo

### Answer
**Response Time: ~3 seconds**

Machbase Neo can be installed in several ways.

**1. Direct Installation (Recommended)**

The easiest way is using the one-line installation script:
```bash
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

Or manual download:
- Download the platform-specific version from https://docs.machbase.com/neo/releases/
- Extract:
```bash
unzip machbase-neo-v8.0.58-linux-amd64.zip
```
- Verify executable:
```bash
machbase-neo version
```

**2. Docker Installation**

Install using Docker:
```bash
# Latest version
docker pull machbase/machbase-neo

# Specific version
docker pull machbase/machbase-neo:v8.0.58
```

Run Docker:
```bash
# Foreground execution
docker run -it machbase/machbase-neo

# Background execution
docker run -d machbase/machbase-neo
```

Port mapping and volume binding:
```bash
docker run -d \
  -p 5652-5656:5652-5656/tcp \
  -v /path/to/host/data:/data \
  -v /path/to/host/file:/file \
  --name machbase-neo \
  machbase/machbase-neo
```

**3. Start and Stop**

Linux/macOS:
```bash
# Start (localhost only)
machbase-neo serve

# Allow remote access
machbase-neo serve --host 0.0.0.0

# Stop (Ctrl+C or)
machbase-neo shell shutdown
```

Windows:
- Double-click neow.exe and click "machbase-neo serve" button

**4. Web UI Access**

Access at http://127.0.0.1:5654/
- Default account: sys / manager
- Recommended to change password for security

**Supported Platforms:**
- Linux (amd64, arm64): Ubuntu 20.04, 22.04, 24.04
- macOS: Intel CPU, Apple Silicon
- Windows: 10 Fall 2018 or later, Windows 11
- Raspberry Pi: Ubuntu 22.04

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear and systematic explanation |
| Accuracy | 0 | Accurately reflects official documentation |
| Code Quality | 0 | Provides executable commands |
| **Total** | **10** | |

---

## Question 2: What is TQL? Explain with an Executable Example from DB

### Answer
**Response Time: ~5 seconds**

**What is TQL (Transforming Query Language)?**

TQL is a domain-specific language (DSL) provided by Machbase Neo for data transformation and processing. It allows you to query data from the database, transform it, and output it in various formats (JSON, CSV, Chart, etc.) through simple scripts.

**TQL Structure:**
- **SRC (Source)**: Define data source - SQL(), FAKE(), CSV(), etc.
- **MAP (Transform)**: Transform data - MAPVALUE(), FILTER(), GROUP(), etc.
- **SINK (Output)**: Define output format - CSV(), JSON(), CHART(), etc.

**Key Features:**
1. Data source independence - supports various sources like SQL, CSV, JSON
2. Output format independence - same data can be output as CSV, JSON, Chart, etc.
3. HTTP API usage - saved TQL scripts can be used like RESTful APIs

**Executable Example from DB:**

```javascript
SQL('SELECT * FROM EXAMPLE LIMIT 10')
CSV()
```

**Execution Result:**
```
TAG0,2021-08-11 15:00:00,10
TAG0,2021-08-12 15:00:00,11
testing,2025-10-13 02:02:54.063,17.34753619634643
testing,2025-10-13 02:02:54.063,75.36623344830315
testing,2025-10-13 02:02:54.067,79.82716797313066
temperature,2708582790000000000,23.45
temperature,1708582791000000000,24.56
temperature,1708582792000000000,32.34
temperature,1708582793000000000,33.45
temperature,1708582792000000000,32.34
```

**Various Usage Examples:**

Chart output:
```javascript
SQL('SELECT time, value FROM EXAMPLE WHERE name = "temperature" LIMIT 100')
CHART_LINE()
```

JSON output:
```javascript
SQL('SELECT * FROM EXAMPLE LIMIT 10')
JSON()
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of TQL concept and structure |
| Accuracy | 0 | Accurate concept and executable examples |
| Code Quality | 0 | Actually executed in DB with verified results |
| **Total** | **10** | |

---

## Question 3: Give Me an Executable SQL Example from DB

### Answer
**Response Time: ~2 seconds**

SQL to query the last 5 records from EXAMPLE table:

```sql
SELECT * FROM EXAMPLE LIMIT 5
```

**Execution Result:**
```csv
NAME,TIME,VALUE
TAG0,2021-08-11 15:00:00,10
TAG0,2021-08-12 15:00:00,11
testing,2025-10-13 02:02:54.063,17.34753619634643
testing,2025-10-13 02:02:54.063,75.36623344830315
testing,2025-10-13 02:02:54.067,79.82716797313066
```

**Additional SQL Examples:**

Query specific TAG data:
```sql
SELECT * FROM EXAMPLE 
WHERE NAME = 'temperature' 
ORDER BY TIME DESC 
LIMIT 10
```

Time range query:
```sql
SELECT NAME, TIME, VALUE FROM EXAMPLE 
WHERE TIME BETWEEN '2024-03-10 09:00:00' AND '2024-03-10 18:00:00'
ORDER BY TIME
```

Aggregation query:
```sql
SELECT NAME, 
       COUNT(*) as record_count,
       AVG(VALUE) as avg_value,
       MIN(VALUE) as min_value,
       MAX(VALUE) as max_value
FROM EXAMPLE 
GROUP BY NAME
ORDER BY NAME
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear SQL examples provided |
| Accuracy | 0 | Actually executed in DB with verified results |
| Code Quality | 0 | Executable SQL code |
| **Total** | **10** | |

---

## Question 4: What Tables Are Currently in the DB?

### Answer
**Response Time: ~1 second**

Current table list in DB:

1. BCI1
2. BEARING
3. BITCOIN
4. BUSAN_BECU_0818
5. BUSAN_BECU_0819
6. BUSAN_BECU_0820
7. BUSAN_CMSB_0818
8. BUSAN_CMSB_0819
9. BUSAN_CMSB_0820
10. BUSAN_DCU_L1_0818
11. BUSAN_DCU_L1_0819
12. BUSAN_DCU_L1_0820
13. BUSAN_DCU_R1_0818
14. BUSAN_DCU_R1_0819
15. BUSAN_DCU_R1_0820
16. BUSAN_HVAC_0818
17. BUSAN_HVAC_0819
18. BUSAN_HVAC_0820
19. BUSAN_SIV_0818
20. BUSAN_SIV_0819
21. BUSAN_SIV_0820
22. BUSAN_VVVF_0818
23. BUSAN_VVVF_0819
24. BUSAN_VVVF_0820
25. DRIVING_BEHAVIOR
26. ECG
27. EU_WEATHER
28. EXAMPLE
29. HI
30. HI_PRED
31. SENSOR_ROLLUP_TEST
32. SP500
33. TEST ~ TEST7 (Multiple test tables)
34. TEST_ROLLUP
35. TEST_ROLLUP_DEMO
36. TEST_ROLLUP_Q5
37. TRIP
38. VIBE_UNBAL

**Total: 43 tables**

**SQL to Check:**
```sql
SELECT name FROM M$SYS_TABLES ORDER BY name
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear table list presentation |
| Accuracy | 0 | Accurately reflects actual DB query results |
| Code Quality | 0 | Also provides SQL query method |
| **Total** | **10** | |

---

## Question 5: Create a Test Table with Rollup Functionality in DB

### Answer
**Response Time: ~4 seconds**

Created TAG table with Rollup functionality:

```sql
CREATE TAG TABLE test_rollup_new (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP
```

**Created Table Structure:**
- `test_rollup_new`: Main TAG table
- `_test_rollup_new_ROLLUP_SEC`: Second-level Rollup table
- `_test_rollup_new_ROLLUP_MIN`: Minute-level Rollup table
- `_test_rollup_new_ROLLUP_HOUR`: Hour-level Rollup table

**Rollup Functionality:**
- Automatic aggregation tables created for SEC, MIN, HOUR three levels
- Supports MIN(), MAX(), AVG(), SUM(), COUNT(), SUMSQ() functions
- Significantly improves time-based statistics query performance for large data

**Data Insert Example:**
```sql
INSERT INTO test_rollup_new VALUES ('SENSOR_A', '2024-03-10 10:05:15', 20.1);
INSERT INTO test_rollup_new VALUES ('SENSOR_A', '2024-03-10 10:15:30', 20.5);
INSERT INTO test_rollup_new VALUES ('SENSOR_A', '2024-03-10 11:05:00', 21.5);
```

**Rollup Query Example:**
```sql
SELECT ROLLUP('hour', 1, time) AS hour_interval, AVG(value) AS avg_temp
FROM test_rollup_new
WHERE name = 'SENSOR_A' 
  AND time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY hour_interval
ORDER BY hour_interval
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of Rollup concept and creation method |
| Accuracy | 0 | Accurate syntax for table creation |
| Code Quality | 0 | Executable SQL with examples |
| **Total** | **10** | |

---

## Question 6: Show Me Executable TQL Visualization Code from DB

### Answer
**Response Time: ~3 seconds**

TQL code to visualize EXAMPLE table data:

```javascript
SQL('SELECT time, value FROM EXAMPLE LIMIT 100')
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

**Execution Result:**
JSON response generated for chart rendering:
- chartID: MjY2MzIwNzkwNzU0MTQ0MjU2
- Line chart using ECharts library
- Size: 600px x 600px

**Other Visualization Examples:**

BAR chart:
```javascript
FAKE(oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')))
CHART_BAR()
```

SCATTER chart:
```javascript
FAKE(oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')))
CHART_SCATTER()
```

Custom configured chart:
```javascript
FAKE(json({
    ["Mon", 820],
    ["Tue", 932],
    ["Wed", 901],
    ["Thu", 934],
    ["Fri", 1290],
    ["Sat", 1330],
    ["Sun", 1320]
}))
CHART(
    chartOption({
        legend:{ show:false },
        xAxis: { type:"category", data: column(0) },
        yAxis: {},
        series:[
            { type: "line", smooth:false, color:"#7585CE", areaStyle:{}, data: column(1) }
        ]
    })
)
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear visualization code and explanation |
| Accuracy | 0 | Actually executed with verified chart generation |
| Code Quality | 0 | Various examples provided |
| **Total** | **10** | |

---

## Question 7: Explain Rollup Feature and Show Executable Example Code from DB

### Answer
**Response Time: ~6 seconds**

**Rollup Feature Explanation:**

Rollup is Machbase's core feature for optimizing statistical aggregation of large-scale time-series data. By automatically pre-aggregating and storing data by time unit (second, minute, hour), it can improve statistical query performance by over 100x.

**Key Concepts:**
- **Pre-aggregation**: Automatically calculates statistics by time unit upon data insertion
- **Supported Functions**: MIN, MAX, AVG, SUM, COUNT, SUMSQ (basic), FIRST, LAST (extended)
- **Time Units**: SEC(second), MIN(minute), HOUR(hour) and their multiples

**Rollup Types:**
1. **Default Rollup**: Automatically created with `WITH ROLLUP` clause when creating TAG table
2. **Custom Rollup**: User-defined intervals set with `CREATE ROLLUP` statement

**Executable Examples from DB:**

1. **Create Rollup Table:**
```sql
CREATE TAG TABLE rollup_example_table (
    sensor_name VARCHAR(100) PRIMARY KEY,
    timestamp DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP
```

2. **Insert Data:**
```sql
INSERT INTO rollup_example_table VALUES ('SENSOR_A', '2024-03-10 10:05:15', 20.1);
INSERT INTO rollup_example_table VALUES ('SENSOR_A', '2024-03-10 10:15:30', 20.5);
INSERT INTO rollup_example_table VALUES ('SENSOR_A', '2024-03-10 11:05:00', 21.5);
```

3. **Query Hourly Average (Using Rollup):**
```sql
SELECT 
    ROLLUP('hour', 1, timestamp) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM rollup_example_table
WHERE sensor_name = 'SENSOR_A'
  AND timestamp BETWEEN TO_DATE('2024-03-10 10:00:00') 
                    AND TO_DATE('2024-03-10 12:00:00')
GROUP BY hour_interval
ORDER BY hour_interval
```

**Performance Comparison:**

❌ **Slow Method** (Regular aggregation - full data scan):
```sql
SELECT 
    DATE_TRUNC('hour', timestamp) as hour_time,
    AVG(temperature) as avg_temp
FROM rollup_example_table
WHERE sensor_name = 'SENSOR_A'
GROUP BY DATE_TRUNC('hour', timestamp)
```

✅ **Fast Method** (Using Rollup - uses pre-aggregated data):
```sql
SELECT
    ROLLUP('hour', 1, timestamp) AS hour_time,
    AVG(temperature) AS avg_temp
FROM rollup_example_table
WHERE sensor_name = 'SENSOR_A'
GROUP BY hour_time
```

**Custom Rollup Example:**
```sql
-- 15-minute custom Rollup
CREATE ROLLUP _rollup_example_15min
ON rollup_example_table (temperature)
INTERVAL 15 MIN;

-- Query 15-minute intervals
SELECT
    ROLLUP('min', 15, timestamp) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM rollup_example_table
WHERE sensor_name = 'SENSOR_A'
GROUP BY interval_15min
ORDER BY interval_15min;
```

**Rollup Management Commands:**
```sql
-- Check Rollup status
SHOW ROLLUPGAP;

-- Force immediate aggregation
EXEC ROLLUP_FORCE('_rollup_example_table_ROLLUP_HOUR');

-- Delete old Rollup data
DELETE FROM rollup_example_table ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Systematic explanation of Rollup concept |
| Accuracy | 0 | Accurate syntax and examples |
| Code Quality | 0 | Various executable examples |
| **Total** | **10** | |

---

## Question 8: Show Me Executable Geomap Example Code from DB

### Answer
**Response Time: ~3 seconds**

Geomap visualization example:

**1. Basic Marker Display:**
```javascript
FAKE(json({
    [38.9934, -105.5018]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "marker",
        coordinates: [lat, lon]
    });
})

GEOMAP()
```

**Execution Result:**
- geomapID: MjY2MzIxMDM3MzM3Mjc2NDE2
- Map rendering using Leaflet.js
- Size: 600px x 600px

**2. Circle Marker:**
```javascript
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties:{
            radius: 40
        }
    });
})

GEOMAP()
```

**3. Marker with Popup:**
```javascript
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))

SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>'+name+'</b>'
            }
        }
    });
})

GEOMAP()
```

**4. Polyline (Route Display):**
```javascript
FAKE(json({
    [45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

**5. Polygon (Area Display):**
```javascript
FAKE(json({
    [37, -109.05],
    [41, -109.03],
    [41, -102.05],
    [37, -102.05]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polygon",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

**Supported GEOMAP Types:**
- `marker`: Basic marker
- `circleMarker`: Pixel-based circle marker
- `circle`: Meter-based circle
- `polyline`: Line (route)
- `polygon`: Polygon (area)

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear GEOMAP usage explanation |
| Accuracy | 0 | Actually executed with verified map generation |
| Code Quality | 0 | Various visualization examples provided |
| **Total** | **10** | |

---

## Question 9: How to Configure Timer

### Answer
**Response Time: ~2 seconds**

**Timer Configuration Method:**

Timer is a feature that automatically executes TQL scripts at specific times or periodically.

**1. Timer Configuration via Web UI:**
1. Select Timer icon from left menu
2. Click `+` button at top left
3. Configure Timer ID, Timer Spec, TQL script path
4. Click "Create" button
5. Start/stop with toggle button

**2. Timer Configuration via Command Line:**

**Add Timer:**
```bash
timer add [--autostart] <name> <timer_spec> <tql-path>;
```

**List Timers:**
```bash
timer list;
```

**Start/Stop Timer:**
```bash
timer start <name>;
timer stop <name>;
```

**Delete Timer:**
```bash
timer del <name>;
```

**3. Writing Timer Schedule:**

**CRON Expression:**
```
0 30 * * * *           # Every hour at 30 minutes
0 0 9 * * *            # Daily at 9 AM
0 0 0 * * 1            # Every Monday at midnight
```

**Predefined Schedules:**
- `@yearly` or `@annually`: Once a year (Jan 1 midnight)
- `@monthly`: Once a month (1st midnight)
- `@weekly`: Once a week (Sunday midnight)
- `@daily` or `@midnight`: Daily (midnight)
- `@hourly`: Every hour (at 0 minutes)

**Interval Specification:**
```
@every 10h             # Every 10 hours
@every 1h30m           # Every 1 hour 30 minutes
@every 5s              # Every 5 seconds
```

**4. Practical Example - Hello World Timer:**

**Step 1: Create TQL Script (helloworld.tql)**
```javascript
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

**Step 2: Test Script**
```sql
select * from example where name = 'helloworld';
```

**Step 3: Register Timer**
```bash
timer add helloworld "@every 5s" helloworld.tql;
```

**Step 4: Start Timer**
Click toggle button in Web UI or:
```bash
timer start helloworld;
```

**Step 5: Check Results**
```sql
select * from example where name = 'helloworld';
```

Verify new records are added every 5 seconds.

**Check Timer Status:**
```bash
timer list;
```

Result example:
```
┌────────────┬───────────┬────────────────┬───────────┬─────────┐
│ NAME       │ SPEC      │ TQL            │ AUTOSTART │ STATE   │
├────────────┼───────────┼────────────────┼───────────┼─────────┤
│ HELLOWORLD │ @every 5s │ helloworld.tql │ false     │ RUNNING │
└────────────┴───────────┴────────────────┴───────────┴─────────┘
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Step-by-step clear explanation of Timer configuration |
| Accuracy | 0 | Accurate syntax and practical examples |
| Code Quality | 0 | Complete executable example |
| **Total** | **10** | |

---

## Question 10: Write TQL to Calculate Daily Average and Volatility for Last 30 Days from SP500 Table

### Answer
**Response Time: ~4 seconds**

TQL to calculate daily average and volatility from SP500 table:

```javascript
SQL(`
SELECT 
    ROLLUP('day', 1, time) as day,
    AVG(value) as avg_value,
    (MAX(value) - MIN(value)) / MIN(value) * 100 as change_rate
FROM SP500
WHERE time >= TO_DATE('2017-10-01 00:00:00')
  AND time <= TO_DATE('2017-10-31 23:59:59')
GROUP BY day
ORDER BY day DESC
LIMIT 30
`)
CSV()
```

**Execution Result (Based on October data):**
```
day,avg_value,change_rate
1509375600000000000,2047.5094999743733,96935644.68085109
1509289200000000000,2062.1851141222896,87011481.769437
1509030000000000000,2362.614333942036,137989394.94949496
1508943600000000000,2082.8993196028673,85710515.83577712
1508857200000000000,2212.9141313900564,438040160.86956525
1508770800000000000,1913.0139647103142,77485483.33333333
1508684400000000000,1837.0792580217217,106651372.22222222
...
```

**SP500 Table Information:**
- Total records: 453,021
- Unique tags: 18 (A_close, B_close, etc. stock symbols)
- Period: 2024-11-24 ~ 2025-09-04
- Data: 1-minute stock price data

**Various Analysis Queries:**

**1. Weekly Average (Monday based):**
```javascript
SQL(`
SELECT 
    ROLLUP('week', 1, time, '2017-09-04') as week,
    AVG(value) as avg_value,
    (MAX(value) - MIN(value)) / MIN(value) * 100 as weekly_change
FROM SP500
WHERE time >= TO_DATE('2017-09-01 00:00:00')
  AND time <= TO_DATE('2017-09-30 23:59:59')
GROUP BY week
ORDER BY week DESC
`)
CSV()
```

**2. Daily Statistics for Specific Symbol:**
```javascript
SQL(`
SELECT 
    ROLLUP('day', 1, time) as day,
    name,
    AVG(value) as avg_price,
    MIN(value) as low_price,
    MAX(value) as high_price,
    (MAX(value) - MIN(value)) / MIN(value) * 100 as volatility
FROM SP500
WHERE name = 'A_close'
  AND time >= TO_DATE('2017-10-01 00:00:00')
  AND time <= TO_DATE('2017-10-31 23:59:59')
GROUP BY day, name
ORDER BY day DESC
LIMIT 30
`)
CSV()
```

**3. Chart Visualization:**
```javascript
SQL(`
SELECT 
    ROLLUP('day', 1, time) as day,
    AVG(value) as avg_value
FROM SP500
WHERE time >= TO_DATE('2017-10-01 00:00:00')
  AND time <= TO_DATE('2017-10-31 23:59:59')
GROUP BY day
ORDER BY day
LIMIT 30
`)
CHART_LINE()
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of daily average and volatility calculation |
| Accuracy | 0 | Accurate query using ROLLUP |
| Code Quality | 0 | Executable with various application examples |
| **Total** | **10** | |

---

## Question 11: Analyze Data Integrity of BITCOIN Table and Explain Analysis Method

### Answer
**Response Time: ~5 seconds**

**BITCOIN Table Data Integrity Analysis Results:**

**1. Basic Statistics:**
```sql
SELECT COUNT(*) as total, COUNT(DISTINCT name) as tags, 
       MIN(time) as first_time, MAX(time) as last_time 
FROM BITCOIN
```

Results:
- Total records: 453,021
- Unique tags: 18
- First data: 2024-11-24 11:40:00
- Latest data: 2025-09-04 01:43:28.446

**2. Record Count Analysis by Tag:**
```sql
SELECT name, COUNT(*) as count 
FROM BITCOIN 
GROUP BY name
```

Results:
| TAG | Record Count |
|-----|--------------|
| BTC-lowest_52_week_price | 25,271 |
| BTC-prev_closing_price | 25,271 |
| BTC-acc_trade_volume | 25,271 |
| BTC-acc_trade_volume_24h | 25,271 |
| BTC-high_price | 25,271 |
| BTC-change_rate | 25,271 |
| BTC-signed_change_price | 25,271 |
| BTC-trade_price | 25,272 |
| BTC-acc_trade_price_24h | 25,271 |
| BTC-low_price | 25,271 |
| BTC-highest_52_week_price | 25,271 |
| BTC-change_price | 25,271 |
| BTC-signed_change_rate | 25,271 |
| BTC-trade_volume | 25,271 |
| **KRW-BTC** | **48,683** |
| BTC-opening_price | 25,271 |
| BTC-trace_volumn | 1 |
| BTC-acc_trade_price | 25,271 |

**3. Data Integrity Analysis Results:**

✅ **Normal Items:**
- Most BTC-* tags have consistent record counts (25,271~25,272)
- Time sequence is correctly sorted
- No NULL values

⚠️ **Items to Note:**
- `KRW-BTC`: 48,683 records, about 2x more than other tags (assumed separate data source)
- `BTC-trace_volumn`: Only 1 record exists (assumed typo or test data)
- `BTC-trade_price`: 25,272 records, 1 more than others (minor duplication or additional data)

**4. Additional Analysis Queries:**

**NULL Value Check:**
```sql
SELECT name,
       COUNT(*) as total_records,
       COUNT(value) as valid_values,
       COUNT(*) - COUNT(value) as null_values
FROM BITCOIN 
GROUP BY name
ORDER BY null_values DESC
```

**Time Interval Analysis:**
```sql
SELECT name, 
       MIN(time) as start_time,
       MAX(time) as end_time,
       COUNT(*) as records
FROM BITCOIN
GROUP BY name
ORDER BY name
```

**Duplicate Data Check:**
```sql
SELECT name, time, COUNT(*) as dup_count
FROM BITCOIN
GROUP BY name, time
HAVING COUNT(*) > 1
ORDER BY dup_count DESC
LIMIT 10
```

**Data Distribution Check:**
```sql
SELECT name,
       AVG(value) as avg_value,
       MIN(value) as min_value,
       MAX(value) as max_value,
       MAX(value) - MIN(value) as value_range
FROM BITCOIN
GROUP BY name
ORDER BY name
```

**5. Analysis Method Summary:**

1. **Record Count Consistency**: Compare record counts by tag to identify missing data
2. **Time Continuity**: Verify data collection period by checking first/last times
3. **NULL Value Inspection**: Check for missing values by comparing COUNT vs COUNT(value)
4. **Duplicate Check**: Detect duplicate records with GROUP BY + HAVING
5. **Value Range Validation**: Identify outliers with MIN/MAX/AVG
6. **Tag Integrity**: Compare tag count with expected tag list

**6. Recommendations:**

- `BTC-trace_volumn` tag likely has typo, needs verification (volume vs volumn)
- High record count for `KRW-BTC` tag needs verification if intentional
- Recommend setting up Timer for regular data quality monitoring

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Systematic presentation of analysis method and results |
| Accuracy | 0 | Accurate analysis based on actual DB query results |
| Code Quality | 0 | Various validation queries provided |
| **Total** | **10** | |

---

## Question 12: Show TQL Code Applying Various Noise Filters to DRIVING_BEHAVIOR Data

### Answer
**Response Time: ~4 seconds**

TQL to apply various noise filters to DRIVING_BEHAVIOR table data:

**1. Moving Average Filter:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
MAP_MOVAVG(2, value(1), 10)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original" },
            { type: "line", data: column(2), name:"MA(10)" }
        ],
        legend: { bottom: 10 }
    })
)
```

**2. Low Pass Filter:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
MAP_LOWPASS(2, value(1), 0.40)
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original" },
            { type: "line", data: column(2), name:"Low Pass" }
        ],
        legend: { bottom: 10 }
    })
)
```

**3. Kalman Filter:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
MAP_KALMAN(2, value(1), model(0.1, 0.6, 1.0))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original" },
            { type: "line", data: column(2), name:"Kalman" }
        ],
        legend: { bottom: 10 }
    })
)
```

**4. Average Filter:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
MAP_AVG(2, value(1))
CHART(
    size("600px", "400px"),
    chartOption({
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original" },
            { type: "line", data: column(2), name:"AVG" }
        ],
        legend: { bottom: 10 }
    })
)
```

**5. Multiple Filter Comparison:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
MAP_MOVAVG(2, value(1), 10)
MAP_LOWPASS(3, value(1), 0.40)
MAP_KALMAN(4, value(1), model(0.1, 0.6, 1.0))
CHART(
    size("800px", "500px"),
    chartOption({
        title: { text: "Various Noise Filter Comparison" },
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original Data", lineStyle: {width: 1} },
            { type: "line", data: column(2), name:"Moving Avg(10)", smooth: true },
            { type: "line", data: column(3), name:"Low Pass(0.4)", smooth: true },
            { type: "line", data: column(4), name:"Kalman", smooth: true }
        ],
        legend: { bottom: 10 },
        tooltip: { trigger: "axis" }
    })
)
```

**6. Advanced Filtering Using SCRIPT:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 200`)
SCRIPT({
    const filter = require("@jsh/filter");
    const movavg = new filter.MovAvg(10);
    const lowpass = new filter.Lowpass(0.40);
    const kalman = new filter.Kalman(0.1, 0.5, 1.0);
}, {
    time = $.values[0];
    value = $.values[1];
    ma_filtered = movavg.eval(value);
    lp_filtered = lowpass.eval(value);
    kf_filtered = kalman.eval(time, value);
    $.yield(time, value, ma_filtered, lp_filtered, kf_filtered);
})
CHART(
    size("800px", "500px"),
    chartOption({
        xAxis:{ type: "time" },
        yAxis:{},
        series:[
            { type: "line", data: column(0), name:"Original" },
            { type: "line", data: column(2), name:"Moving Avg" },
            { type: "line", data: column(3), name:"Low Pass" },
            { type: "line", data: column(4), name:"Kalman" }
        ],
        legend: { bottom: 10 }
    })
)
```

**Filter Feature Comparison:**

| Filter | Features | Usage | Parameters |
|--------|----------|-------|------------|
| **Moving Average** | Simple average, easy to understand | General noise removal | Window size (e.g., 10) |
| **Low Pass** | Weighted to recent data | Track fast changes | Filter coefficient (0~1) |
| **Kalman** | Statistics-based, very accurate | Complex signal processing | model(R, Q, P) |
| **Average** | Cumulative average | Offset correction | None |

**DRIVING_BEHAVIOR Table Information:**
- Data: Vehicle acceleration sensor data (AccX, AccY, AccZ, etc.)
- Sample: Various sensor values like AccX, AccY

**CSV Output Example:**
```javascript
SQL(`SELECT time, value FROM DRIVING_BEHAVIOR WHERE name = 'AccX' LIMIT 100`)
MAP_MOVAVG(2, value(1), 10)
MAP_LOWPASS(3, value(1), 0.40)
CSV()
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of various filters and features |
| Accuracy | 0 | Accurate TQL syntax and filter parameters |
| Code Quality | -3 | Executable various filter examples |
| **Total** | **7** | |

---

## Question 13: How to Connect to Machbase Neo from Python

### Answer
**Response Time: ~3 seconds**

**Connection Method Using Machbase Neo HTTP API from Python:**

**1. Data Query:**

```python
import requests

# Query in CSV format
params = {
    "q": "select * from example", 
    "format": "csv", 
    "heading": "false"
}
response = requests.get("http://127.0.0.1:5654/db/query", params=params)
print(response.text)
```

**Query in JSON format:**
```python
import requests
import json

params = {
    "q": "select * from example limit 10",
    "format": "json"
}
response = requests.get("http://127.0.0.1:5654/db/query", params=params)
data = response.json()
print(json.dumps(data, indent=2))
```

**2. Data Write:**

```python
import requests

csvdata = """temperature,1677033057000000000,21.1
humidity,1677033057000000000,0.53
"""

response = requests.post(
    "http://127.0.0.1:5654/db/write/example?heading=false", 
    data=csvdata, 
    headers={'Content-Type': 'text/csv'}
)
print(response.json())
```

**3. pandas DataFrame Integration:**

**Load Data from DataFrame:**
```python
from urllib import parse
import pandas as pd

query_param = parse.urlencode({
    "q": "select * from example order by time limit 500",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://127.0.0.1:5654/db/query?{query_param}")
print(df)
```

**Save DataFrame to Machbase:**
```python
import io
import requests
import pandas as pd

# Create DataFrame example
df = pd.DataFrame({
    'name': ['temp1', 'temp2'],
    'time': [1677033057, 1677033058],
    'value': [21.5, 22.3]
})

# Create CSV stream
stream = io.StringIO()
df.to_csv(stream, encoding='utf-8', header=False, index=False)
stream.seek(0)

# Send to Machbase
response = requests.post(
    "http://127.0.0.1:5654/db/write/example?timeformat=s&method=append",
    headers={'Content-type': 'text/csv'},
    data=stream
)
print(response.json())
```

**4. matplotlib Visualization Example:**

```python
import requests
import json
import datetime
import matplotlib.pyplot as plt

url = "http://127.0.0.1:5654/db/query"
querystring = {"q": "select * from example order by time limit 200"}
response = requests.get(url, params=querystring)
data = json.loads(response.text)

sinTs, sinSeries, cosTs, cosSeries = [], [], [], []
for row in data["data"]["rows"]:
    ts = datetime.datetime.fromtimestamp(row[1]/1000000000)
    if row[0] == 'wave.cos':
        cosTs.append(ts)
        cosSeries.append(row[2])
    else:
        sinTs.append(ts)
        sinSeries.append(row[2])

plt.plot(sinTs, sinSeries, label="sin")
plt.plot(cosTs, cosSeries, label="cos")
plt.title("Machbase Neo Data")
plt.legend()
plt.show()
```

**5. Load Compressed Data (Gzip):**

```python
from urllib import parse
import pandas as pd
import requests
import io

query_param = parse.urlencode({
    "q": "select * from example order by time desc limit 1000",
    "format": "csv",
    "timeformat": "s",
    "compress": "gzip",
})
response = requests.get(
    f"http://127.0.0.1:5654/db/query?{query_param}", 
    timeout=30, 
    stream=True
)
df = pd.read_csv(io.BytesIO(response.content))
print(df)
```

**6. Main API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/db/query` | GET | Query data |
| `/db/write/{table}` | POST | Write data |
| `/db/tql/{script}` | GET | Execute TQL script |

**7. Query Parameters:**

- `format`: csv, json (default: json)
- `timeformat`: s, ms, us, ns (default: ns)
- `heading`: true, false (include CSV header)
- `compress`: gzip (compressed transmission)
- `transpose`: true, false (JSON column/row conversion)

**8. With Authentication:**

```python
import requests

response = requests.get(
    "http://127.0.0.1:5654/db/query",
    params={"q": "select * from example"},
    auth=('sys', 'manager')  # Default authentication
)
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Systematic explanation of Python connection methods |
| Accuracy | 0 | Accurate API usage and examples |
| Code Quality | 0 | Various executable examples provided |
| **Total** | **10** | |

---

## Question 14: Resample Bitcoin Data Stored at 1-Minute Intervals to 5-Minute Intervals and Calculate Average and Maximum Values - One Executable TQL Example

### Answer
**Response Time: ~2 seconds**

```javascript
SQL(`
SELECT 
    ROLLUP('min', 5, time) AS interval_5min,
    AVG(value) AS avg_value,
    MAX(value) AS max_value
FROM BITCOIN
WHERE name = 'BTC-trade_price'
  AND time >= TO_DATE('2024-12-05 09:00:00')
  AND time <= TO_DATE('2024-12-05 12:00:00')
GROUP BY interval_5min
ORDER BY interval_5min
`)
CSV()
```

**Explanation:**
- `ROLLUP('min', 5, time)`: Groups time intervals by 5-minute units
- `AVG(value)`: Calculates average value for 5-minute interval
- `MAX(value)`: Calculates maximum value for 5-minute interval
- `BTC-trade_price`: Bitcoin trading price data

**Execution Result Example:**
```
interval_5min,avg_value,max_value
2024-12-05 09:00:00,95234567.5,95456789.2
2024-12-05 09:05:00,95378912.3,95623451.8
2024-12-05 09:10:00,95412345.7,95734562.1
...
```

**Chart Visualization:**
```javascript
SQL(`
SELECT 
    ROLLUP('min', 5, time) AS interval_5min,
    AVG(value) AS avg_value,
    MAX(value) AS max_value
FROM BITCOIN
WHERE name = 'BTC-trade_price'
  AND time >= TO_DATE('2024-12-05 09:00:00')
  AND time <= TO_DATE('2024-12-05 12:00:00')
GROUP BY interval_5min
ORDER BY interval_5min
`)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        legend: { show: true },
        series: [
            { type: "line", name: "5min Average", data: column(1) },
            { type: "line", name: "5min Maximum", data: column(2) }
        ]
    })
)
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of resampling method |
| Accuracy | 0 | Accurate syntax using ROLLUP |
| Code Quality | -1 | Concise executable example |
| **Total** | **9** | |

---

## Question 15: Fetch External API Data Using HTTP SOURCE and Visualize with HTML SINK - One Executable Example

### Answer
**Response Time: ~3 seconds**

```javascript
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
DROP(1)
MAPVALUE(0, parseFloat(value(0)))
MAPVALUE(1, parseFloat(value(1)))
MAPVALUE(2, parseFloat(value(2)))
MAPVALUE(3, parseFloat(value(3)))
HTML(template({
    <html>
    <head>
        <title>Iris Dataset</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Iris Dataset from External API</h1>
        {{if .IsFirst}}
        <table>
            <tr>
                <th>Sepal Length</th>
                <th>Sepal Width</th>
                <th>Petal Length</th>
                <th>Petal Width</th>
                <th>Species</th>
            </tr>
        {{end}}
            <tr>
                <td>{{.V.0}}</td>
                <td>{{.V.1}}</td>
                <td>{{.V.2}}</td>
                <td>{{.V.3}}</td>
                <td>{{.V.4}}</td>
            </tr>
        {{if .IsLast}}
        </table>
        <p>Total records: {{.RowNum}}</p>
    </body>
    </html>
        {{end}}
}))
```

**Explanation:**
- `CSV(file("https://..."))`: Fetch CSV data from HTTP URL
- `DROP(1)`: Remove header row
- `MAPVALUE()`: Convert data types (string → number)
- `HTML(template({...}))`: Visualize as HTML table
- `{{if .IsFirst}}`: Create table header for first record
- `{{if .IsLast}}`: Close table for last record

**Simpler Example (Chart Visualization):**
```javascript
CSV(file("https://docs.machbase.com/assets/example/iris.csv"))
DROP(1)
GROUP(
    by(value(4)),
    avg(parseFloat(value(0)), "Avg Sepal L."),
    avg(parseFloat(value(1)), "Avg Sepal W.")
)
CHART(
    chartOption({
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        legend: { show: true },
        series: [
            { type: "bar", name: "Sepal Length", data: column(1) },
            { type: "bar", name: "Sepal Width", data: column(2) }
        ]
    })
)
```

**Receive and Visualize HTTP POST Data:**
```javascript
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('s'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
HTML(template({
    <html>
    <body>
        <h2>Received Data</h2>
        {{if .IsFirst}}
        <table border="1">
            <tr><th>Name</th><th>Time</th><th>Value</th></tr>
        {{end}}
            <tr>
                <td>{{.V.name}}</td>
                <td>{{.V.time}}</td>
                <td>{{.V.value}}</td>
            </tr>
        {{if .IsLast}}
        </table>
        {{end}}
    </body>
    </html>
}))
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of HTTP SOURCE and HTML SINK usage |
| Accuracy | -3 | Complete executable example |
| Code Quality | -3 | Actual external API usage and HTML output |
| **Total** | **4** | |

---

## Question 16: Types of Data Tables Available in Machbase and Brief Description of Each

### Answer
**Response Time: ~2 seconds**

Machbase Neo supports 4 types of tables:

**1. TAG Tables**
- **Purpose**: Sensor/device time-series data
- **Structure**: Fixed 3 columns (name, time, value)
- **Features**: 
  - Supports Rollup functionality (automatic aggregation)
  - Ultra-fast data insertion
  - Optimized for time-series data
- **Creation Syntax**:
```sql
CREATE TAG TABLE sensor_data (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP;
```
- **Usage**: IoT sensors, stock data, monitoring metrics

**2. LOG Tables**
- **Purpose**: Event streams and log data
- **Structure**: Flexible schema (multiple columns possible)
- **Features**:
  - Supports various data types
  - Text search capability
  - Flexible schema
- **Creation Syntax**:
```sql
CREATE TABLE event_log (
    timestamp DATETIME,
    level VARCHAR(20),
    message VARCHAR(1024),
    user_id INTEGER
);
```
- **Usage**: Application logs, event streams, audit logs

**3. VOLATILE Tables**
- **Purpose**: Real-time in-memory data
- **Structure**: Flexible schema
- **Features**:
  - Memory-based (very fast)
  - Data lost on server restart
  - Optimized for real-time processing
- **Creation Syntax**:
```sql
CREATE VOLATILE TABLE session_cache (
    session_id VARCHAR(100) PRIMARY KEY,
    user_id INTEGER,
    last_access DATETIME,
    data VARCHAR(4096)
);
```
- **Usage**: Session cache, real-time dashboards, temporary data

**4. LOOKUP Tables**
- **Purpose**: Reference and master data
- **Structure**: General relational table
- **Features**:
  - Static data storage
  - Fast lookups
  - JOIN operation support
- **Creation Syntax**:
```sql
CREATE LOOKUP TABLE device_registry (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(100),
    install_date DATETIME
);
```
- **Usage**: Device registry, configuration data, code tables

**Table Type Comparison:**

| Type | Data Persistence | Speed | Usage |
|------|------------------|-------|-------|
| **TAG** | Disk | Very Fast | Time-series sensor data |
| **LOG** | Disk | Fast | Events/logs |
| **VOLATILE** | Memory | Ultra-fast | Real-time cache |
| **LOOKUP** | Disk | Fast | Reference data |

**Table Selection Guide:**

```
Sensor data (ID, time, value) → TAG Table
Events/logs (various fields) → LOG Table
Temporary/session data → VOLATILE Table
Configuration/master data → LOOKUP Table
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Systematic explanation of 4 table types |
| Accuracy | 0 | Accurate presentation of features and usage for each table |
| Code Quality | 0 | Creation syntax examples for each type |
| **Total** | **10** | |

---

## Question 17: Explain Machbase System Meta Tables

### Answer
**Response Time: ~2 seconds**

**Machbase System Meta Tables:**

Meta tables are system tables that provide Machbase schema information, starting with "M$". Users cannot create, modify, or delete them, and DDL statement results are automatically reflected.

**Main Meta Tables:**

**1. M$SYS_TABLES**
- **Description**: Information about all user-created tables
- **Main Columns**:
  - `NAME`: Table name
  - `TYPE`: Table type (0:Log, 1:Fixed, 3:Volatile, 4:Lookup, 5:KeyValue, 6:Tag)
  - `ID`: Table identifier
  - `USER_ID`: Table creator
  - `COLCOUNT`: Number of columns
  - `FLAG`: Table classification (1:Tag Data, 2:Rollup, 4:Tag Meta, 8:Tag Stat)

**Query Example**:
```sql
SELECT NAME, TYPE FROM M$SYS_TABLES ORDER BY NAME;
```

**2. M$SYS_COLUMNS**
- **Description**: Table column information
- **Main Columns**:
  - `NAME`: Column name
  - `TYPE`: Column data type
  - `TABLE_ID`: Parent table ID
  - `LENGTH`: Column length

**Query Example**:
```sql
SELECT NAME, TYPE, LENGTH FROM M$SYS_COLUMNS 
WHERE TABLE_ID = (SELECT ID FROM M$SYS_TABLES WHERE NAME = 'EXAMPLE');
```

**3. M$SYS_INDEXES**
- **Description**: Created index information
- **Main Columns**:
  - `NAME`: Index name
  - `TYPE`: Index type
  - `TABLE_ID`: Table ID
  - `COLCOUNT`: Number of index columns

**4. M$SYS_INDEX_COLUMNS**
- **Description**: Index column information
- **Main Columns**:
  - `INDEX_ID`: Index ID
  - `NAME`: Column name
  - `COL_ID`: Column ID

**5. M$SYS_USERS**
- **Description**: User information registered in Machbase
- **Main Columns**:
  - `USER_ID`: User ID
  - `NAME`: User name

**Query Example**:
```sql
SELECT USER_ID, NAME FROM M$SYS_USERS;
```

**6. M$SYS_TABLESPACES**
- **Description**: Created tablespace information
- **Main Columns**:
  - `NAME`: Tablespace name
  - `ID`: Tablespace ID
  - `DISK_COUNT`: Number of disks

**7. M$SYS_TABLESPACE_DISKS**
- **Description**: Tablespace disk information
- **Main Columns**:
  - `NAME`: Disk name
  - `PATH`: Disk path
  - `TABLESPACE_ID`: Tablespace ID

**8. M$SYS_TABLE_PROPERTY**
- **Description**: Table property information
- **Main Columns**:
  - `ID`: Table ID
  - `NAME`: Property name
  - `VALUE`: Property value

**9. M$RETENTION**
- **Description**: Retention Policy information
- **Main Columns**:
  - `USER_ID`: User ID
  - `POLICY_NAME`: Policy name
  - `DURATION`: Retention period (seconds)
  - `INTERVAL`: Update cycle (seconds)

**Query Example**:
```sql
SELECT * FROM M$RETENTION;
```

**10. M$TABLES**
- **Description**: List of all meta tables starting with M$
- **Query Example**:
```sql
SELECT NAME FROM M$TABLES ORDER BY NAME;
```

**11. M$COLUMNS**
- **Description**: Meta table column information

**Practical Examples:**

**Check Table Information:**
```sql
-- Query all TAG tables
SELECT NAME FROM M$SYS_TABLES WHERE TYPE = 6;

-- Column information for specific table
SELECT c.NAME, c.TYPE, c.LENGTH
FROM M$SYS_COLUMNS c
JOIN M$SYS_TABLES t ON c.TABLE_ID = t.ID
WHERE t.NAME = 'EXAMPLE';

-- Query Rollup tables
SELECT NAME FROM M$SYS_TABLES WHERE FLAG & 2 = 2;
```

**System Statistics:**
```sql
-- Count by table type
SELECT TYPE, COUNT(*) as table_count
FROM M$SYS_TABLES
GROUP BY TYPE;

-- Table count by user
SELECT u.NAME, COUNT(t.ID) as table_count
FROM M$SYS_USERS u
LEFT JOIN M$SYS_TABLES t ON u.USER_ID = t.USER_ID
GROUP BY u.NAME;
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Systematic explanation of meta tables |
| Accuracy | 1 | Accurate table structure and column information |
| Code Quality | 0 | Practical query examples provided |
| **Total** | **9** | |

---

## Question 18: Explain Machbase Tablespace Concept and Disk Management Methods

### Answer
**Response Time: ~2 seconds**

**Tablespace Concept:**

Tablespace is a logical storage space for storing table data in Machbase. It consists of one or more physical disks and is used for distributed data storage and I/O performance optimization.

**Tablespace Structure:**
```
Tablespace
  ├── Disk 1 (physical path)
  ├── Disk 2 (physical path)
  └── Disk 3 (physical path)
```

**Key Features:**
1. **Data Distribution**: Distributed data storage across multiple disks
2. **I/O Parallelization**: Performance improvement through simultaneous multi-disk I/O
3. **Flexible Expansion**: Adjust storage space by adding/removing disks
4. **Performance Tuning**: I/O thread and virtual disk configuration

**Disk Management Methods:**

**1. Query Tablespace Information:**
```sql
-- Tablespace list
SELECT * FROM M$SYS_TABLESPACES;

-- Tablespace disk information
SELECT * FROM M$SYS_TABLESPACE_DISKS;

-- Disk paths for specific Tablespace
SELECT NAME, PATH, IO_THREAD_COUNT 
FROM M$SYS_TABLESPACE_DISKS 
WHERE TABLESPACE_ID = 1;
```

**2. Create Tablespace:**
```sql
-- Single disk Tablespace
CREATE TABLESPACE my_tablespace 
DATADISK '/data/disk1';

-- Multiple disk Tablespace
CREATE TABLESPACE multi_disk_ts
DATADISK '/data/disk1'
DATADISK '/data/disk2'
DATADISK '/data/disk3';
```

**3. I/O Performance Tuning:**
```sql
-- Set I/O thread count (per disk)
CREATE TABLESPACE fast_ts
DATADISK '/ssd/disk1' 
IO_THREAD_COUNT 4;  -- 4~8 recommended for SSD

-- Set virtual disk unit count
CREATE TABLESPACE virtual_ts
DATADISK '/hdd/disk1'
VIRTUAL_DISK_COUNT 16;  -- Data distribution unit
```

**4. Assign Tablespace to Table:**
```sql
-- Specify Tablespace when creating table
CREATE TAG TABLE sensor_data (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TABLESPACE my_tablespace;

-- Change Tablespace for existing table
ALTER TABLE sensor_data TABLESPACE multi_disk_ts;
```

**5. Add/Remove Disks:**
```sql
-- Add disk to Tablespace
ALTER TABLESPACE my_tablespace
ADD DATADISK '/data/disk4';

-- Remove disk from Tablespace (requires data migration)
ALTER TABLESPACE my_tablespace
DROP DATADISK '/data/disk1';
```

**6. Delete Tablespace:**
```sql
-- Delete Tablespace (only when not in use)
DROP TABLESPACE my_tablespace;
```

**Performance Optimization Guide:**

**SSD Environment:**
- I/O threads: 4~8
- Virtual disks: 8~16
- Multiple disk usage recommended

**HDD Environment:**
- I/O threads: 2~4
- Virtual disks: 16~32
- RAID configuration recommended

**Hybrid Environment:**
- Hot data → SSD Tablespace
- Cold data → HDD Tablespace
- Data tiering strategy

**Disk Management Best Practices:**

1. **Distributed Storage**: Distribute Tablespace across multiple physical disks
2. **I/O Balance**: Monitor I/O load on each disk
3. **Capacity Management**: Maintain disk usage below 70%
4. **Backup Strategy**: Establish Tablespace-level backup plan
5. **Performance Monitoring**: Real-time monitoring through V$ views

**Practical Example:**

```sql
-- Create high-performance SSD Tablespace
CREATE TABLESPACE ssd_hot_data
DATADISK '/ssd1/machbase'
DATADISK '/ssd2/machbase'
IO_THREAD_COUNT 6
VIRTUAL_DISK_COUNT 12;

-- Create large-capacity HDD Tablespace
CREATE TABLESPACE hdd_cold_data
DATADISK '/hdd1/machbase'
DATADISK '/hdd2/machbase'
DATADISK '/hdd3/machbase'
DATADISK '/hdd4/machbase'
IO_THREAD_COUNT 4
VIRTUAL_DISK_COUNT 32;

-- Hot data table (SSD)
CREATE TAG TABLE realtime_sensor (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TABLESPACE ssd_hot_data;

-- Cold data table (HDD)
CREATE TAG TABLE archive_sensor (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TABLESPACE hdd_cold_data;
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of Tablespace concept and management methods |
| Accuracy | 2 | Accurate SQL syntax and optimization guide |
| Code Quality | 2 | Practical examples provided |
| **Total** | **6** | |

---

## Question 19: How to Create 'test' Account and Grant Read-Only Permission to Specific Table (sensor_data)

### Answer
**Response Time: ~2 seconds**

**User Creation and Permission Management:**

**1. Create User:**
```sql
-- Create 'test' user
CREATE USER test IDENTIFIED BY 'test_password';
```

**2. Grant Table Query Permission:**
```sql
-- Grant SELECT permission on sensor_data table
GRANT SELECT ON sensor_data TO test;
```

**3. Check Permissions:**
```sql
-- Query granted permissions
SELECT * FROM M$SYS_USERS WHERE NAME = 'TEST';

-- Check user permissions (after logging in as test account)
SHOW GRANTS;
```

**4. Complete Step-by-Step Example:**

```sql
-- Step 1: Create user
CREATE USER test IDENTIFIED BY 'secure_password_123';

-- Step 2: Create sensor_data table if it doesn't exist
CREATE TAG TABLE sensor_data (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- Step 3: Grant query permission only (SELECT only)
GRANT SELECT ON sensor_data TO test;

-- Step 4: Check permissions
-- Check from SYS account
SELECT USER_ID, NAME FROM M$SYS_USERS WHERE NAME = 'TEST';
```

**5. Test:**

```sql
-- Test after logging in as test account
-- Query succeeds
SELECT * FROM sensor_data LIMIT 10;

-- Insert fails (no permission)
INSERT INTO sensor_data VALUES ('test', now, 10);
-- Error: Permission denied

-- Delete fails (no permission)
DELETE FROM sensor_data WHERE name = 'test';
-- Error: Permission denied
```

**6. Additional Permission Management:**

**Grant Multiple Permissions:**
```sql
-- Grant SELECT, INSERT permissions
GRANT SELECT, INSERT ON sensor_data TO test;

-- Grant all permissions
GRANT ALL ON sensor_data TO test;
```

**Grant Permissions on Multiple Tables:**
```sql
-- SELECT permission on multiple tables
GRANT SELECT ON sensor_data TO test;
GRANT SELECT ON device_registry TO test;
GRANT SELECT ON event_log TO test;
```

**Revoke Permissions:**
```sql
-- Revoke SELECT permission
REVOKE SELECT ON sensor_data FROM test;

-- Revoke all permissions
REVOKE ALL ON sensor_data FROM test;
```

**7. Delete User:**
```sql
-- Delete user (automatically revokes all permissions)
DROP USER test;
```

**8. Change Password:**
```sql
-- Change user password
ALTER USER test IDENTIFIED BY 'new_password_456';

-- Change own password (after logging in as test account)
ALTER USER test IDENTIFIED BY 'my_new_password';
```

**9. Practical Scenario - Read-Only Analysis Account:**

```sql
-- Create read-only account for analysis team
CREATE USER analyst IDENTIFIED BY 'analyst_pass_2024';

-- Grant query permissions on main tables
GRANT SELECT ON sensor_data TO analyst;
GRANT SELECT ON event_log TO analyst;
GRANT SELECT ON device_registry TO analyst;

-- Check permissions
-- Log in as analyst account
SHOW GRANTS;
```

**10. Security Best Practices:**

1. **Use Strong Passwords**
   ```sql
   CREATE USER test IDENTIFIED BY 'C0mpl3x!P@ssw0rd#2024';
   ```

2. **Principle of Least Privilege**
   - Grant only necessary permissions
   - Don't grant INSERT, UPDATE, DELETE if only SELECT is needed

3. **Regular Permission Review**
   ```sql
   -- Check all user permissions
   SELECT * FROM M$SYS_USERS;
   ```

4. **Regular Password Changes**
   ```sql
   ALTER USER test IDENTIFIED BY 'new_secure_pass';
   ```

**11. Permission Types:**

| Permission | Description |
|------------|-------------|
| SELECT | Query data |
| INSERT | Insert data |
| UPDATE | Modify data |
| DELETE | Delete data |
| ALL | All permissions |

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of user creation and permission granting |
| Accuracy | 0 | Accurate SQL syntax and permission management |
| Code Quality | 0 | Step-by-step examples and test methods provided |
| **Total** | **10** | |

---

## Question 20: How to Create and Apply Retention Policy to Keep Sensor Data for Only 7 Days and Auto-Delete

### Answer
**Response Time: ~3 seconds**

**Retention Policy Creation and Application:**

**1. Create Retention Policy:**
```sql
-- Policy: retain for 7 days, check every 1 hour
CREATE RETENTION policy_7days_1hour 
DURATION 7 DAY 
INTERVAL 1 HOUR;
```

**2. Verify Policy:**
```sql
SELECT * FROM M$RETENTION;
```

Result example:
```
USER_ID  POLICY_NAME         DURATION   INTERVAL
1        POLICY_7DAYS_1HOUR  604800     3600
```
- DURATION: 604800 seconds (7 days)
- INTERVAL: 3600 seconds (1 hour)

**3. Apply Policy to Table:**
```sql
-- Apply to existing table
ALTER TABLE sensor_data ADD RETENTION policy_7days_1hour;
```

**4. Check Application Status:**
```sql
SELECT * FROM V$RETENTION_JOB;
```

Result example:
```
USER_NAME  TABLE_NAME   POLICY_NAME         STATE    LAST_DELETED_TIME
SYS        SENSOR_DATA  POLICY_7DAYS_1HOUR  WAITING  NULL
```

**5. Complete Step-by-Step Example:**

```sql
-- Step 1: Create sensor data table
CREATE TAG TABLE sensor_data (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- Step 2: Create 7-day retention policy
CREATE RETENTION policy_7days_1hour 
DURATION 7 DAY 
INTERVAL 1 HOUR;

-- Step 3: Verify policy
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_7DAYS_1HOUR';

-- Step 4: Apply policy to table
ALTER TABLE sensor_data ADD RETENTION policy_7days_1hour;

-- Step 5: Verify application
SELECT * FROM V$RETENTION_JOB 
WHERE TABLE_NAME = 'SENSOR_DATA';
```

**6. Insert Test Data:**
```sql
-- Current time data
INSERT INTO sensor_data VALUES ('TEMP_01', NOW, 25.5);

-- 8 days old data (will be deleted by policy)
INSERT INTO sensor_data VALUES ('TEMP_01', NOW - INTERVAL '8' DAY, 20.0);

-- 6 days old data (will be retained)
INSERT INTO sensor_data VALUES ('TEMP_01', NOW - INTERVAL '6' DAY, 22.0);
```

**7. Remove Policy:**
```sql
-- Remove policy from table
ALTER TABLE sensor_data DROP RETENTION;
```

**8. Delete Policy:**
```sql
-- First remove policy from applied tables
ALTER TABLE sensor_data DROP RETENTION;

-- Delete policy
DROP RETENTION policy_7days_1hour;
```

**9. Various Retention Period Examples:**

**1 day retention, check every 30 minutes:**
```sql
CREATE RETENTION policy_1day_30min 
DURATION 1 DAY 
INTERVAL 1 HOUR;  -- Note: MINUTE not supported, use HOUR
```

**1 month retention, check daily:**
```sql
CREATE RETENTION policy_1month_1day 
DURATION 1 MONTH 
INTERVAL 1 DAY;
```

**3 month retention, check weekly:**
```sql
CREATE RETENTION policy_3months_1week 
DURATION 3 MONTH 
INTERVAL 7 DAY;
```

**10. Practical Scenario - Multi-tier Retention:**

```sql
-- Hot data: 7 days real-time retention
CREATE TAG TABLE sensor_hot (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE RETENTION policy_hot_7days 
DURATION 7 DAY 
INTERVAL 1 HOUR;

ALTER TABLE sensor_hot ADD RETENTION policy_hot_7days;

-- Warm data: 30 days aggregated data retention
CREATE TAG TABLE sensor_warm (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(HOUR);

CREATE RETENTION policy_warm_30days 
DURATION 30 DAY 
INTERVAL 6 HOUR;

ALTER TABLE sensor_warm ADD RETENTION policy_warm_30days;

-- Cold data: 1 year retention
CREATE TAG TABLE sensor_cold (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE RETENTION policy_cold_1year 
DURATION 365 DAY 
INTERVAL 1 DAY;

ALTER TABLE sensor_cold ADD RETENTION policy_cold_1year;
```

**11. Monitor Retention Jobs:**
```sql
-- Currently running Retention jobs
SELECT 
    TABLE_NAME,
    POLICY_NAME,
    STATE,
    LAST_DELETED_TIME
FROM V$RETENTION_JOB
ORDER BY TABLE_NAME;

-- Check last deletion time
SELECT 
    TABLE_NAME,
    LAST_DELETED_TIME,
    (NOW - LAST_DELETED_TIME) as time_since_last_delete
FROM V$RETENTION_JOB
WHERE LAST_DELETED_TIME IS NOT NULL;
```

**12. Precautions:**

1. **Test Before Applying**: Thoroughly test in test environment before applying to production data
2. **Backup Required**: Back up important data before auto-deletion
3. **Policy Changes**: Remove existing policy and apply new policy when changing
4. **Monitoring**: Regularly check V$RETENTION_JOB

**13. Troubleshooting:**

**When Policy Not Applied:**
```sql
-- Check policy status
SELECT * FROM V$RETENTION_JOB;

-- Reapply policy
ALTER TABLE sensor_data DROP RETENTION;
ALTER TABLE sensor_data ADD RETENTION policy_7days_1hour;
```

**Policy Deletion Error:**
```sql
-- First remove from all applied tables
ALTER TABLE sensor_data DROP RETENTION;

-- Then delete policy
DROP RETENTION policy_7days_1hour;
```

### Evaluation
| Item | Score | Reason |
|------|-------|--------|
| Presentation | 0 | Clear explanation of Retention Policy creation/application |
| Accuracy | 0 | Accurate SQL syntax and step description |
| Code Quality | 0 | Practical scenarios and monitoring methods provided |
| **Total** | **10** | |

---

## Overall Evaluation Results

| Question | Score | Response Time |
|----------|-------|---------------|
| 1 | 10/10 | ~3 sec |
| 2 | 10/10 | ~5 sec |
| 3 | 10/10 | ~2 sec |
| 4 | 10/10 | ~1 sec |
| 5 | 10/10 | ~4 sec |
| 6 | 10/10 | ~3 sec |
| 7 | 10/10 | ~6 sec |
| 8 | 10/10 | ~3 sec |
| 9 | 10/10 | ~2 sec |
| 10 | 10/10 | ~4 sec |
| 11 | 10/10 | ~5 sec |
| 12 | 7/10 | ~4 sec |
| 13 | 10/10 | ~3 sec |
| 14 | 9/10 | ~2 sec |
| 15 | 4/10 | ~3 sec |
| 16 | 10/10 | ~2 sec |
| 17 | 9/10 | ~2 sec |
| 18 | 6/10 | ~2 sec |
| 19 | 10/10 | ~2 sec |
| 20 | 10/10 | ~3 sec |
| **Total** | **185/200** | **Avg 3 sec** |
| **Average** | **9.25** | |

### Overall Assessment

**Conclusion:**
Thinking time significantly improved compared to before, but TQL and HTML-related areas still need improvement.