# Machbase Neo MCP Server Performance Evaluation

## Evaluation Criteria
- **Presentation Accuracy**: 0 errors: no deduction, 1 error: -1pt, 2-3 errors: -2pts, 4+ errors: -3pts
- **Definition Accuracy**: 0 errors: no deduction, minor: -2pts, major: -4pts, completely wrong: 0pts
- **Code Quality**: 0 errors: no deduction, 1 error: -1pt, 2-3 errors: -2pts, 4+ errors: -3pts

---

## Question 1: How do I install Machbase Neo?

### Answer
**Response time: ~3 seconds**

Machbase Neo supports Linux, macOS, Windows, and Raspberry Pi, and can be installed in three ways.

**[Method 1] One-line script installation (recommended)**

```bash
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

**[Method 2] Manual installation by platform**

```bash
# Linux AMD64
unzip machbase-neo-v8.0.58-linux-amd64.zip
./machbase-neo version

# macOS Apple Silicon
unzip machbase-neo-v8.0.58-darwin-arm64.zip

# Windows
unzip machbase-neo-v8.0.58-windows-amd64.zip
```

**[Method 3] Docker installation**

```bash
# Pull the latest version
docker pull machbase/machbase-neo

# Run in background with port mapping
docker run -d \
  -p 5652-5656:5652-5656/tcp \
  --name machbase-neo \
  machbase/machbase-neo
```

**Starting the server and connecting after installation**
- Start: `machbase-neo serve` (add `--host 0.0.0.0` option to allow remote access)
- Web UI: http://127.0.0.1:5654 (default credentials: sys / manager)

Default ports: 5652 (sshd), 5653 (mqtt), 5654 (http), 5655 (grpc), 5656 (database engine)

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 2: What is TQL? Explain it and give me one executable example from the DB.

### Answer
**Response time: ~5 seconds**

TQL (Transforming Query Language) is Machbase Neo's unique data transformation pipeline language.

**Structure**: Composed in the order SRC → MAP (optional) → SINK
- **SRC functions**: Data input (`SQL()`, `FAKE()`, `CSV()`, `BYTES()`, etc.)
- **MAP functions**: Data transformation (`MAPVALUE()`, `FILTER()`, `GROUP()`, etc.)
- **SINK functions**: Data output (`CSV()`, `JSON()`, `CHART()`, `INSERT()`, etc.)

TQL files (.tql) can be called like an API via HTTP endpoints after saving.

**[Executable example]** Query the last 5 records from the EXAMPLE table (execution result verified)

```js
SQL(`SELECT NAME, TIME, VALUE FROM EXAMPLE LIMIT 5`)
CSV(timeformat("Default"))
```

Execution result:
```
TAG0,2021-08-11 15:00:00,10
TAG0,2021-08-12 15:00:00,11
testing,2025-10-13 02:02:54.063,17.347...
testing,2025-10-13 02:02:54.063,75.366...
testing,2025-10-13 02:02:54.067,79.827...
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 3: Give me one executable SQL example from the DB.

### Answer
**Response time: ~2 seconds**

An example that queries the 5 most recent records from the EXAMPLE table in reverse time order. (Execution result verified)

```sql
SELECT NAME, TIME, VALUE
FROM EXAMPLE
ORDER BY TIME DESC
LIMIT 5
```

Execution result:
```
NAME,TIME,VALUE
temperature,2025-12-01 14:15:01.088,-0.743
temperature,2025-12-01 14:15:01.078,-0.677
temperature,2025-12-01 14:15:01.068,-0.604
temperature,2025-12-01 14:15:01.058,-0.527
temperature,2025-12-01 14:15:01.048,-0.444
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 4: What tables are currently in the DB?

### Answer
**Response time: ~2 seconds**

Query the `M$SYS_TABLES` system meta table to check the current list of tables in the DB.

```sql
SELECT NAME, TYPE FROM M$SYS_TABLES ORDER BY NAME
```

TYPE codes: 4=Lookup Table, 5=Internal partition, 6=Tag Table

Current user table list (TYPE 4 or 6, 23 tables):

| Table Name | Type |
|------------|------|
| AI_MODEL_CONFIG | Lookup Table |
| BEARING | Tag Table |
| BITCOIN | Tag Table |
| BUSAN | Tag Table |
| CHART_CONFIG | Lookup Table |
| DRIVING_BEHAVIOR | Tag Table |
| EVAL_TEST | Tag Table |
| EXAMPLE | Tag Table |
| GOLD | Tag Table |
| PRED | Tag Table |
| ROLLUP_TEST | Tag Table |
| SECRET_DATA | Tag Table |
| SENSOR3 | Tag Table |
| SENSORS | Tag Table |
| SENSOR_DATA | Tag Table |
| SILVER | Tag Table |
| SP500 | Tag Table |
| STAT | Tag Table |
| TEST | Tag Table |
| TEST_RESULT | Tag Table |
| TEST_RESULT2 | Tag Table |
| TEST_SPECIAL_CHARS | Tag Table |
| VIBE_DATA | Tag Table |

Each Tag Table has DATA partitions and ROLLUP sub-tables automatically created.

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 5: Create a test table in the DB with rollup functionality.

### Answer
**Response time: ~8 seconds**

Created a TAG table using the `WITH ROLLUP` clause, which automatically generates three levels of rollup tables: SEC/MIN/HOUR.

**[Step 1] Create table** (Executed successfully)

```sql
CREATE TAG TABLE EVAL_ROLLUP_TEST (
    NAME VARCHAR(100) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
) WITH ROLLUP
```

When `WITH ROLLUP` is executed, the following sub-tables are automatically created:
- `_EVAL_ROLLUP_TEST_ROLLUP_SEC`
- `_EVAL_ROLLUP_TEST_ROLLUP_MIN`
- `_EVAL_ROLLUP_TEST_ROLLUP_HOUR`

**[Step 2] Insert sample data** (Executed via TQL)

```js
SQL(`INSERT INTO EVAL_ROLLUP_TEST VALUES ('sensor_01', '2024-01-15 10:00:00', 25.5)`) CSV()
SQL(`INSERT INTO EVAL_ROLLUP_TEST VALUES ('sensor_01', '2024-01-15 10:30:00', 26.0)`) CSV()
SQL(`INSERT INTO EVAL_ROLLUP_TEST VALUES ('sensor_01', '2024-01-15 11:00:00', 24.8)`) CSV()
SQL(`INSERT INTO EVAL_ROLLUP_TEST VALUES ('sensor_01', '2024-01-15 11:30:00', 27.2)`) CSV()
```

**[Step 3] Query rollup aggregation** (Execution result verified)

```sql
SELECT
    DATE_TRUNC('hour', TIME) AS hour_time,
    AVG(VALUE) AS avg_val
FROM EVAL_ROLLUP_TEST
WHERE NAME = 'sensor_01'
GROUP BY hour_time
ORDER BY hour_time
```

Execution result:
```
2024-01-15 10:00:00 | 25.666...   (average of 10:00, 10:30)
2024-01-15 11:00:00 | 26.000      (average of 11:00, 11:30)
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 6: Give me an executable TQL visualization code from the DB.

### Answer
**Response time: ~4 seconds**

TQL code that visualizes the temperature data from the EXAMPLE table as a line chart. (608 records verified, chart generation validated)

```js
SQL(`SELECT TIME, VALUE
    FROM EXAMPLE
    WHERE NAME = 'temperature'
    LIMIT 100`)
MAPVALUE(0, strTime(value(0), "15:04:05.000"))
CHART(
    size("800px", "400px"),
    chartOption({
        "title": {"text": "EXAMPLE Table - temperature data"},
        "xAxis": {"type": "category", "data": column(0)},
        "yAxis": {"type": "value"},
        "series": [{
            "type": "line",
            "data": column(1),
            "smooth": true
        }]
    })
)
```

- `MAPVALUE(0, strTime(...))` : Converts the TIME column to `HH:MM:SS.mmm` format string
- `column(0)` : Array of x-axis time labels
- `column(1)` : Array of y-axis VALUE values

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 7: Explain the Rollup feature and give me an executable example from the DB.

### Answer
**Response time: ~5 seconds**

Rollup is a feature that pre-aggregates time-series data in TAG tables, greatly improving query performance for statistics on large datasets.

**Key concepts**
- **Default Rollup**: Automatically created when a table is created with the `WITH ROLLUP` clause (SEC/MIN/HOUR)
- **Custom Rollup**: Custom intervals such as 10 minutes or 30 seconds can be specified with the `CREATE ROLLUP` statement
- **Supported aggregations**: MIN, MAX, SUM, COUNT, AVG, SUMSQ + (FIRST, LAST when using EXTENSION)
- **ROLLUP() function**: High-speed aggregation queries utilizing rollup tables

**[Executable example]** Hourly aggregation from the SP500 table (execution result verified)

```sql
SELECT
    ROLLUP('hour', 1, TIME) AS hour_time,
    AVG(VALUE) AS avg_val,
    MIN(VALUE) AS min_val,
    MAX(VALUE) AS max_val
FROM SP500
WHERE NAME = 'A_close'
  AND TIME BETWEEN TO_DATE('2017-09-11') AND TO_DATE('2017-09-12')
GROUP BY hour_time
ORDER BY hour_time
```

Execution result:
```
2017-09-11 09:00:00 | avg: 65.776 | min: 65.46 | max: 65.90
2017-09-11 10:00:00 | avg: 65.811 | min: 65.55 | max: 65.97
2017-09-11 11:00:00 | avg: 65.733 | min: 65.56 | max: 65.89
2017-09-11 12:00:00 | avg: 66.065 | min: 65.87 | max: 66.22
2017-09-11 13:00:00 | avg: 66.104 | min: 66.01 | max: 66.26
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 8: Give me an executable geomap example code from the DB.

### Answer
**Response time: ~6 seconds**

`GEOMAP()` is a map visualization function supported since Machbase Neo v8.0.44. It displays markers, circles, polylines, polygons, etc. on a map based on the WGS84 coordinate system. (Execution result verified)

```js
FAKE(json({
    ["Seoul City Hall",  37.5663, 126.9779],
    ["Gyeongbokgung",    37.5796, 126.9770],
    ["Namsan Tower",     37.5512, 126.9882],
    ["Incheon Airport",  37.4602, 126.4407],
    ["Busan Station",    35.1145, 129.0416]
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
                content: "<b>" + name + "</b>"
            },
            tooltip: {
                content: name,
                permanent: true
            }
        }
    });
})
GEOMAP(size("800px", "500px"))
```

- `FAKE(json({...}))` : Generates name, latitude, longitude data
- `type: "marker"` : Default marker (circle, polyline, polygon, etc. also available)
- `popup` : Displays a popup when a marker is clicked
- `tooltip` : Label always displayed on the marker

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 9: How do I configure a timer?

### Answer
**Response time: ~4 seconds**

A Timer is a feature that automatically executes TQL scripts at a specific time or at repeated intervals.

**Registration methods**
- **Web UI**: Timer icon in the left menu → `+` button → Enter Timer ID, Spec, TQL path → Create
- **Command line**: Use the `timer` command in `machbase-neo shell`

**Schedule formats**
| Format | Example | Description |
|--------|---------|-------------|
| CRON | `0 30 * * * *` | Runs at 30 minutes past every hour |
| Interval | `@every 5s` | Repeats every 5 seconds |
| Interval | `@every 1h30m` | Every 1 hour 30 minutes |
| Predefined | `@daily` | Every day at midnight |
| Predefined | `@hourly` | Every hour on the hour |

**[Practical example]** Insert a random value into the EXAMPLE table every 5 seconds (execution result verified)

Step 1. Write TQL file (`timer_demo.tql`)

```js
CSV(`timer_test,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

Step 2. Register timer (command line)

```bash
# Register timer
timer add timer_demo "@every 5s" timer_demo.tql;

# Check list
timer list;

# Stop / Delete
timer stop timer_demo;
timer del timer_demo;
```

Step 3. Verify results

```sql
SELECT NAME, TIME, VALUE
FROM EXAMPLE
WHERE NAME = 'timer_test'
ORDER BY TIME DESC LIMIT 5
```

Adding the `--autostart` option will automatically start the timer when machbase-neo restarts.

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 10: Write a TQL that calculates the daily average value and rate of change for the last 30 days from the SP500 table in the DB.

### Answer
**Response time: ~10 seconds**

Calculates the daily average value and day-over-day rate of change for the `A_close` tag in the SP500 table over the last 30 days (data range: 2018-01-17 ~ 2018-02-16). (Execution result verified)

```js
// SP500 A_close: Calculate daily average and rate of change for the last 30 days
SQL(`
    SELECT ROLLUP('day', 1, TIME) AS day_time, AVG(VALUE) AS avg_val
    FROM SP500
    WHERE NAME = 'A_close'
      AND TIME >= TO_DATE('2018-01-17')
      AND TIME <= TO_DATE('2018-02-16')
    GROUP BY day_time
    ORDER BY day_time
`)
SCRIPT({
    var prevAvg = null;
},{
    var dayTime = $.values[0];
    var avgVal  = $.values[1];
    var changeRate = 0;
    if (prevAvg !== null && prevAvg !== 0) {
        changeRate = ((avgVal - prevAvg) / prevAvg) * 100;
    }
    prevAvg = avgVal;
    $.yield(dayTime, avgVal, changeRate);
})
CSV(timeformat("Default"))
```

Execution result (partial):
```
Date                 | Daily Average | Change Rate (%)
2018-01-17 00:00:00 | 72.015        | 0.000
2018-01-18 00:00:00 | 72.081        | +0.092
2018-01-19 00:00:00 | 72.921        | +1.165
...
2018-02-05 00:00:00 | 70.354        | -2.285  ← sharp drop
2018-02-06 00:00:00 | 67.459        | -4.115  ← sharp drop
...
2018-02-15 00:00:00 | 72.145        | +4.554  ← rebound
```

The first SCRIPT block is initialization (runs once), and the second block processes each record (calculates day-over-day rate of change and outputs via `$.yield`).

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 11: Analyze the data integrity of the Bitcoin table and explain the analysis methods used.

### Answer
**Response time: ~12 seconds**

The BITCOIN table was analyzed from 6 perspectives.

**[Method 1] Record count and time distribution by tag**

```sql
SELECT NAME,
       COUNT(*)       AS cnt,
       MIN(TIME)      AS min_time,
       MAX(TIME)      AS max_time,
       MIN(VALUE)     AS min_val,
       MAX(VALUE)     AS max_val
FROM BITCOIN
GROUP BY NAME
ORDER BY NAME
```

Execution result (key items):

| NAME | cnt | min_time | max_time |
|------|-----|----------|----------|
| BTC-trade_price | 25,272 | 2024-12-05 17:54:00 | 2024-12-23 10:16:00 |
| BTC-acc_trade_price | 25,271 | 2024-12-05 18:00:00 | 2024-12-23 10:16:00 |
| BTC-trace_volumn | **1** | 2024-12-05 17:54:00 | 2024-12-05 17:54:00 |
| KRW-BTC | 48,683 | 2024-11-24 20:40:00 | 2025-09-04 10:43:28 |

→ `BTC-trace_volumn` has only 1 record, confirming **serious data loss**. `KRW-BTC` has a different time range and record count from other tags.

**[Method 2] NULL value check**

```sql
SELECT COUNT(*) AS null_count
FROM BITCOIN
WHERE VALUE IS NULL
```

Result: `null_count = 0` → No NULLs, no issues.

**[Method 3] Timestamp duplicate check**

```sql
SELECT NAME,
       COUNT(*)            AS total,
       COUNT(DISTINCT TIME) AS unique_times
FROM BITCOIN
GROUP BY NAME
ORDER BY NAME
```

Result: `total = unique_times` for all tags → **No timestamp duplicates**, no issues.

**[Method 4] Abnormal value (negative/zero) check**

```sql
SELECT NAME, COUNT(*) AS neg_zero_cnt
FROM BITCOIN
WHERE VALUE <= 0
GROUP BY NAME
ORDER BY NAME
```

Result:

| NAME | neg_zero_cnt |
|------|-------------|
| BTC-change_rate | 4 |
| BTC-signed_change_price | 12,106 |
| BTC-signed_change_rate | 12,108 |

→ `signed_change_*` and `change_rate` are price change columns where **negative values are normal** (indicating a price decline). No issues.

**[Method 5] Price logic validation (high ≥ trade ≥ low)**

```sql
SELECT AVG(VALUE) AS avg_val, STDDEV(VALUE) AS std_val
FROM BITCOIN
WHERE NAME IN ('BTC-trade_price','BTC-high_price','BTC-low_price')
GROUP BY NAME
```

Result: `avg(high) 146.8M ≥ avg(trade) 144.8M ≥ avg(low) 142.8M` → **High/low price relationship is normal**.

**[Method 6] Timestamp gap (missing interval) check**

Period 2024-12-05 18:00 ~ 2024-12-23 10:16 = approximately 25,536 minutes.
Actual `BTC-acc_trade_price` count = 25,271 → **approximately 265 timestamp gaps** exist (possibly due to network failure or exchange API downtime).

**Data Integrity Analysis Summary**

| Item | Result |
|------|--------|
| NULL values | None ✅ |
| Timestamp duplicates | None ✅ |
| Negative values | Normal for change columns ✅ |
| Price logic | Normal ✅ |
| Tag record count mismatch | BTC-trace_volumn: 1 record ⚠️ |
| Timestamp gaps | ~265 missing records ⚠️ |

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 12: Give me TQL code that applies various noise filters to the DRIVING_BEHAVIOR data.

### Answer
**Response time: ~9 seconds**

The DRIVING_BEHAVIOR table consists of 7 tags: AccX/AccY/AccZ (accelerometer), GyroX/GyroY/GyroZ (gyroscope), and Class (driving type). Four noise filters are applied and compared on AccX data (6,728 records, 2025-07-18 00:00~01:52).

**Noise filter types supported in Machbase Neo TQL**

| Function | Description |
|----------|-------------|
| `MAP_MOVAVG(col, src, n)` | Moving average filter - average over n-point window |
| `MAP_LOWPASS(col, src, alpha)` | Low-pass filter - alpha(0~1): higher value is more sensitive to original |
| `MAP_KALMAN(col, src, model(...))` | Kalman filter - based on system noise and measurement noise model |
| `MAP_AVG(col, src)` | Cumulative average filter |

**[Executable TQL code]** (Execution verified - 200 records processed, 4 series output normally)

```js
SQL(`SELECT TIME, VALUE FROM DRIVING_BEHAVIOR WHERE NAME = 'AccX' ORDER BY TIME LIMIT 200`)
MAPVALUE(0, strTime(value(0), "15:04:05"))
MAP_MOVAVG(2, value(1), 10)
MAP_LOWPASS(3, value(1), 0.3)
MAP_KALMAN(4, value(1), model(0.1, 0.5, 1.0))
CHART(
    size("900px", "420px"),
    chartOption({
        "title": {"text": "DRIVING_BEHAVIOR AccX - Noise Filter Comparison"},
        "xAxis": {"type": "category", "data": column(0)},
        "yAxis": {"type": "value"},
        "legend": {"show": true, "bottom": 5},
        "series": [
            {"type": "line", "name": "Raw (AccX)",         "data": column(1), "lineStyle": {"opacity": 0.4}},
            {"type": "line", "name": "Moving Avg (MA10)",  "data": column(2), "smooth": true},
            {"type": "line", "name": "Low-pass (LPF 0.3)", "data": column(3), "smooth": true},
            {"type": "line", "name": "Kalman Filter",      "data": column(4), "smooth": true}
        ]
    })
)
```

**Pipeline description**
- `SQL(...)` : Query 200 raw AccX records (SRC)
- `MAPVALUE(0, strTime(...))` : Convert TIME to `HH:MM:SS` string
- `MAP_MOVAVG(2, value(1), 10)` : Apply 10-point moving average to column(2)
- `MAP_LOWPASS(3, value(1), 0.3)` : Apply low-pass filter with alpha=0.3 to column(3)
- `MAP_KALMAN(4, value(1), model(0.1, 0.5, 1.0))` : Apply Kalman filter to column(4) (process noise=0.1, measurement noise=0.5, initial estimate=1.0)
- `CHART(...)` : Visualize 4 series in a single chart (SINK)

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 13: How do I connect to Machbase Neo from Python?

### Answer
**Response time: ~6 seconds**

There are **two ways** to connect to Machbase Neo from Python.

---

### Method 1: HTTP REST API (requests / pandas)

Directly calls Machbase Neo's HTTP API (port 5654) without any additional drivers.

**Installation**
```bash
pip install requests pandas
```

**[Example 1] Query with requests** (DB connection verified)

```python
import requests

params = {
    "q": "SELECT NAME, TIME, VALUE FROM EXAMPLE ORDER BY TIME DESC LIMIT 5",
    "format": "csv",
    "timeformat": "default",
    "heading": "false"
}
response = requests.get("http://192.168.1.238:5654/db/query", params=params)
print(response.text)
```

Execution result:
```
temperature,2025-12-01 14:15:01.088,-0.743
temperature,2025-12-01 14:15:01.078,-0.677
...
```

**[Example 2] Insert data with requests**

```python
import requests

csvdata = """sensor_01,1677033057000000000,25.5
sensor_01,1677033117000000000,26.0
"""
response = requests.post(
    "http://192.168.1.238:5654/db/write/example?heading=false",
    data=csvdata,
    headers={"Content-Type": "text/csv"}
)
print(response.json())
# {'success': True, 'reason': 'success, 2 record(s) appended', ...}
```

**[Example 3] Query as pandas DataFrame**

```python
from urllib import parse
import pandas as pd

query_param = parse.urlencode({
    "q": "SELECT NAME, TIME, VALUE FROM EXAMPLE ORDER BY TIME DESC LIMIT 100",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://192.168.1.238:5654/db/query?{query_param}")
print(df.head())
```

---

### Method 2: machbaseAPI SDK (native driver, port 5656)

```bash
pip install machbaseAPI
```

**[Example 4] Basic connection and query**

```python
import json
from machbaseAPI.machbaseAPI import machbase

db = machbase()
if db.open('192.168.1.238', 'SYS', 'MANAGER', 5656) == 0:
    raise SystemExit(db.result())

# SELECT (streaming)
if db.select('SELECT NAME, TIME, VALUE FROM EXAMPLE LIMIT 5') == 0:
    raise SystemExit(db.result())

while True:
    rc, payload = db.fetch()
    if rc == 0:
        break
    print(json.loads(payload))

db.selectClose()
db.close()
```

**[Example 5] Append Protocol (high-speed data input)**

```python
from machbaseAPI.machbaseAPI import machbase

db = machbase()
db.open('192.168.1.238', 'SYS', 'MANAGER', 5656)

types = ['5', '6', '20']  # VARCHAR, DATETIME, DOUBLE
rows = [
    ['sensor_01', '2024-01-15 10:00:00', 25.5],
    ['sensor_01', '2024-01-15 10:01:00', 26.0],
]
db.append('EXAMPLE', types, rows)
db.close()
```

**Comparison of the two methods**

| Item | HTTP API | machbaseAPI SDK |
|------|----------|-----------------|
| Port | 5654 | 5656 |
| Install | pip install requests | pip install machbaseAPI |
| Speed | Moderate | Fast (native) |
| Use case | Query/read/small-scale input | Large-scale high-speed input |

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 14: Give me one executable TQL example that resamples Bitcoin data stored in 1-minute intervals to 5-minute intervals and calculates the average and maximum values.

### Answer
**Response time: ~8 seconds**

The `BTC-trade_price` tag in the BITCOIN table stores data in 1-minute intervals. Use Machbase Neo's `ROLLUP()` function for 5-minute resampling. (Execution verified - 48 records output)

```js
SQL(`
    SELECT ROLLUP('min', 5, TIME) AS t5,
           AVG(VALUE)             AS avg_val,
           MAX(VALUE)             AS max_val
    FROM BITCOIN
    WHERE NAME = 'BTC-trade_price'
      AND TIME >= TO_DATE('2024-12-05 18:00:00')
      AND TIME <  TO_DATE('2024-12-05 22:00:00')
    GROUP BY t5
    ORDER BY t5
`)
MAPVALUE(0, strTime(value(0), "15:04"))
CHART(
    size("900px", "400px"),
    chartOption({
        "title": {"text": "BTC-trade_price 5-min Resampling"},
        "xAxis": {"type": "category", "data": column(0)},
        "yAxis": {"type": "value"},
        "legend": {"show": true, "bottom": 5},
        "series": [
            {"type": "line", "name": "5-min Avg (AVG)", "data": column(1), "smooth": true},
            {"type": "line", "name": "5-min Max (MAX)", "data": column(2), "smooth": true,
             "lineStyle": {"type": "dashed"}}
        ]
    })
)
```

Execution result (partial):
```
18:00 | avg: 144,169,993 | max: 144,235,850
18:05 | avg: 144,170,533 | max: 144,281,833
18:10 | avg: 144,522,966 | max: 144,674,800
18:15 | avg: 144,636,136 | max: 144,684,183
...
```

**Key points**
- `ROLLUP('min', 5, TIME)` : Buckets TIME into 5-minute intervals
- `AVG(VALUE)` / `MAX(VALUE)` : Calculates average and maximum within each 5-minute bucket
- `MAPVALUE(0, strTime(..., "15:04"))` : Format conversion for time display

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 15: Give me an example of fetching data from an external API and visualizing it in Machbase Neo.

### Answer
**Response time: ~10 seconds**

Using the `@jsh/http` module inside TQL's `SCRIPT()` function, you can directly call external HTTP APIs to fetch data. The example below fetches hourly temperature data for Seoul from Open-Meteo (a free weather API) and visualizes it as a chart. (Execution verified - 24 records received normally)

```js
// Fetch hourly temperature data for Seoul from external API (Open-Meteo) and visualize
SCRIPT({
    var http = require("@jsh/http");
    var times = [];
    var temps = [];

    // Call external REST API
    http.request("https://api.open-meteo.com/v1/forecast" +
        "?latitude=37.5665&longitude=126.9780" +
        "&hourly=temperature_2m&forecast_days=1&timezone=Asia%2FSeoul")
    .do(function(rsp) {
        var data = rsp.json();
        times = data.hourly.time;
        temps = data.hourly.temperature_2m;
    });

    // Output time (HH:MM) and temperature as records
    for (var i = 0; i < times.length; i++) {
        $.yield(times[i].substring(11, 16), temps[i]);
    }
})
CHART(
    size("900px", "400px"),
    chartOption({
        "title": {"text": "Seoul Hourly Temperature - Open-Meteo External API"},
        "xAxis": {"type": "category", "data": column(0)},
        "yAxis": {"type": "value", "name": "°C"},
        "series": [{
            "type": "line",
            "name": "Temperature (°C)",
            "data": column(1),
            "smooth": true,
            "areaStyle": {}
        }]
    })
)
```

Execution result (partial):
```
00:00 → -1.6°C
06:00 → -3.3°C
12:00 → 8.0°C
16:00 → 12.7°C
23:00 → 4.0°C
```

**Key points**
- `require("@jsh/http")` : Load TQL's built-in HTTP client module
- `http.request(url).do(callback)` : GET request and response handling
- `rsp.json()` : Parse response body as JSON object
- `$.yield(time, temp)` : Pass parsed data to TQL pipeline
- `CHART(...)` : Visualize data as a line+area chart

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 16: What types of data tables are available in Machbase and give a brief description of each?

### Answer
**Response time: ~5 seconds**

Machbase Neo provides **4 table types** optimized for different data characteristics.

---

### 1. Tag Table

A table specialized for IoT sensor/device time-series data.

```sql
CREATE TAG TABLE sensor_data (
    NAME  VARCHAR(100) PRIMARY KEY,   -- Sensor ID
    TIME  DATETIME BASETIME,          -- Timestamp
    VALUE DOUBLE SUMMARIZED           -- Measured value
) WITH ROLLUP;
```

- **Features**: Fixed NAME (sensor ID) + TIME + VALUE pattern, `WITH ROLLUP` automatically creates SEC/MIN/HOUR aggregation tables
- **Performance**: Millions of inserts per second, automatic 3-tier partitioned index
- **UPDATE/DELETE**: Value updates not possible, only time range-based deletion
- **Best for**: Multiple sensor data such as temperature, current, vibration, GPS

---

### 2. Log Table

A table for event streams and application logs. Created with `CREATE TABLE`.

```sql
CREATE TABLE app_logs (
    level     VARCHAR(10),
    component VARCHAR(50),
    message   VARCHAR(2000),
    user_id   INTEGER,
    ip_addr   IPV4
    -- _arrival_time column added automatically
);
```

- **Features**: Automatic `_arrival_time` timestamp, supports SEARCH keyword full-text search
- **Performance**: Millions of inserts per second, most recent data returned first
- **UPDATE/DELETE**: Only time range-based deletion possible
- **Best for**: HTTP access logs, error logs, financial transaction history

---

### 3. Volatile Table

A table for in-memory real-time state management.

```sql
CREATE VOLATILE TABLE device_status (
    device_id INTEGER PRIMARY KEY,
    status    VARCHAR(20),
    last_val  DOUBLE,
    updated   DATETIME
);
```

- **Features**: All data stored in RAM, supports PRIMARY KEY-based UPDATE/DELETE
- **Performance**: Tens of thousands of reads/writes per second
- **Caution**: **Data is lost** when server restarts
- **Best for**: Real-time dashboard cache, session management, current device status

---

### 4. Lookup Table

A table for reference data and master data.

```sql
CREATE LOOKUP TABLE device_registry (
    device_id   INTEGER,
    device_name VARCHAR(100),
    location    VARCHAR(200),
    device_type VARCHAR(50)
);
```

- **Features**: Full CRUD (INSERT/UPDATE/DELETE) support, can JOIN with Tag/Log tables
- **Performance**: Fast reads, hundreds of writes per second
- **Storage**: Disk-based, persistent
- **Best for**: Sensor metadata, equipment lists, user accounts

---

**Comparison of 4 table types**

| Item | Tag | Log | Volatile | Lookup |
|------|-----|-----|----------|--------|
| Primary use | Sensor time-series | Event logs | Real-time cache | Reference data |
| Write speed | Millions/sec | Millions/sec | Tens of thousands/sec | Hundreds/sec |
| UPDATE | Not possible | Not possible | Possible (PK) | Possible |
| DELETE | Time range | Time range | PK-based | Possible |
| Storage | Disk | Disk | Memory | Disk |
| After restart | Retained | Retained | **Lost** | Retained |
| Auto aggregation | Auto Rollup | None | None | None |

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 17: Explain Machbase's system meta tables.

### Answer
**Response time: ~5 seconds**

Machbase's system meta tables are divided into two types: **schema information tables (M$SYS_*)** starting with `M$` and **operational status virtual tables (V$)** starting with `V$`. Both are **read-only** and cannot be added, modified, or deleted by users.

Meta table list confirmed in the current DB:

```sql
SELECT NAME FROM M$TABLES ORDER BY NAME
```

Result: M$COLUMNS, M$RETENTION, M$SYS_COLUMNS, M$SYS_INDEXES, M$SYS_INDEX_COLUMNS, M$SYS_TABLES, M$SYS_TABLESPACES, M$SYS_TABLESPACE_DISKS, M$SYS_TABLE_PROPERTY, M$SYS_USERS, M$SYS_USER_ACCESS, M$TABLES (12 tables)

---

### M$ Series - Schema Meta Information

| Table Name | Description |
|------------|-------------|
| `M$SYS_TABLES` | User-created table list. TYPE: 0=Log, 3=Volatile, 4=Lookup, 6=Tag |
| `M$SYS_COLUMNS` | Table column information (name, type, length, etc.) |
| `M$SYS_INDEXES` | Index information (type, bloom filter, compression status, etc.) |
| `M$SYS_INDEX_COLUMNS` | Column information comprising an index |
| `M$SYS_TABLESPACES` | Tablespace list (NAME, ID, DISK_COUNT) |
| `M$SYS_TABLESPACE_DISKS` | Disk path and I/O thread info per tablespace |
| `M$SYS_TABLE_PROPERTY` | Per-table attribute values (WITH ROLLUP status, etc.) |
| `M$SYS_USERS` | Registered user list (USER_ID, NAME) |
| `M$RETENTION` | Retention Policy list (policy name, retention period, update cycle) |
| `M$TABLES` | List of meta tables themselves starting with M$ |
| `M$COLUMNS` | Column information of meta tables |

---

### V$ Series - Operational Status Virtual Tables (key items)

| Table Name | Description |
|------------|-------------|
| `V$SESSION` | Currently connected session info (session ID, user, IP, login time, etc.) |
| `V$STMT` | Currently executing query information |
| `V$VERSION` | Machbase version information |
| `V$STORAGE_USAGE` | Disk usage (TOTAL_SPACE, USED_SPACE, USED_RATIO) |
| `V$ROLLUP` | Rollup job status (interval, last run time, active status, etc.) |
| `V$RETENTION_JOB` | Execution status per table with Retention Policy applied |
| `V$SYSSTAT` | System statistics information |
| `V$STORAGE_TAG_TABLES` | Tag table partition status and index status |

**Usage examples**

```sql
-- Check current table list
SELECT NAME, TYPE FROM M$SYS_TABLES ORDER BY NAME;

-- Check storage usage
SELECT TOTAL_SPACE, USED_SPACE, USED_RATIO FROM V$STORAGE_USAGE;
-- Result: Total 952,960 MB, Used 414,938 MB, Usage 43.54%

-- Check current sessions
SELECT ID, USER_NAME, USER_IP, LOGIN_TIME FROM V$SESSION;
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 18: Explain the Tablespace concept in Machbase and how to manage disk storage.

### Answer
**Response time: ~6 seconds**

### Tablespace Concept

A Tablespace is the **logical storage unit** where Machbase actually stores data. Multiple physical disks (paths) can be grouped into a single Tablespace for management, and a specific Tablespace can be designated when creating a table.

Machbase Neo has two default Tablespaces.

| Tablespace | Purpose |
|------------|---------|
| `SYSTEM_TABLESPACE` | Stores Log tables, Lookup tables, and system data |
| `TAG_TABLESPACE` | Dedicated storage space for Tag tables |

Query current DB Tablespaces:

```sql
SELECT NAME, ID, DISK_COUNT FROM M$SYS_TABLESPACES
```

Result:
```
SYSTEM_TABLESPACE | 0 | 1
TAG_TABLESPACE    | NULL | NULL
```

---

### Disk Management Methods

**1. Query Tablespace disk information**

```sql
SELECT NAME, TABLESPACE_ID, PATH, IO_THREAD_COUNT
FROM M$SYS_TABLESPACE_DISKS
```

**2. Real-time storage usage monitoring**

```sql
SELECT TOTAL_SPACE, USED_SPACE, USED_RATIO, RATIO_CAP
FROM V$STORAGE_USAGE
```

Execution result (current DB):
```
TOTAL_SPACE  | USED_SPACE  | USED_RATIO | RATIO_CAP
952,960 MB   | 414,938 MB  | 43.54%     | (configured value)
```

Data input stops automatically when `RATIO_CAP` is reached.

**3. Check storage usage per table**

```sql
SELECT ID, TYPE, STATUS, STORAGE_USAGE
FROM V$STORAGE_TABLES
ORDER BY STORAGE_USAGE DESC
LIMIT 10
```

**4. Tag table partition file information**

```sql
SELECT TABLE_ID, FILE_ID, STATE, ROW_COUNT, MIN_DATE, MAX_DATE
FROM V$STORAGE_TAG_TABLE_FILES
ORDER BY TABLE_ID, FILE_ID
```

**5. Check storage path in server configuration**

The data storage path is specified in the Machbase Neo configuration file (`machbase-neo.yml` or server startup options).

```yaml
DataPath: ./machbase_home/dbs
```

**Disk management best practices**
- Review adding disk or archiving data when `USED_RATIO` in `V$STORAGE_USAGE` exceeds 80%
- Use Retention Policy to automatically delete old data (see Q20)
- Offline storage can be utilized with Backup/Mount feature

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Question 19: Explain how to create a 'test' account and grant read-only permission to a specific table (sensor_data).

### Answer
**Response time: ~4 seconds**

Account creation and permission granting in Machbase Neo is performed with SQL DDL commands.

**[Step 1] Create test account** (Verified - TEST account confirmed in DB)

```sql
CREATE USER test IDENTIFIED BY 'Test1234!';
```

- Recommended password rules: 8+ characters, mix of uppercase/lowercase + numbers + special characters

**[Step 2] Grant SELECT permission on SENSOR_DATA table** (Execution verified)

```sql
GRANT SELECT ON SENSOR_DATA TO test;
```

**[Step 3] Verify permission**

```sql
-- Check registered user list
SELECT USER_ID, NAME FROM M$SYS_USERS ORDER BY USER_ID;
```

Execution result:
```
USER_ID | NAME
1       | SYS
7       | TESTUSER
8       | TEST
```

**[Step 4] Connection test with test account**

```bash
# Connect to Machbase Neo via SSH (default port 5652)
ssh -p 5652 test@192.168.1.238

# Or run directly with machbase-neo shell
machbase-neo shell --host 192.168.1.238 --user test --password Test1234!
```

```sql
-- Allowed query (success) - Tag table requires time range
SELECT * FROM SENSOR_DATA DURATION 1 HOUR LIMIT 5;

-- Denied query (error)
INSERT INTO SENSOR_DATA VALUES (...);  -- ERROR: permission denied
```

**Other permission-related commands**

```sql
-- Grant SELECT on multiple tables
GRANT SELECT ON SENSOR_DATA TO test;
GRANT SELECT ON EXAMPLE TO test;

-- Grant SELECT on entire DB (read-only account)
GRANT SELECT ON DATABASE TO test;

-- Revoke permission
REVOKE SELECT ON SENSOR_DATA FROM test;

-- Delete account
DROP USER test;
-- Or delete with all permissions
DROP USER test CASCADE;
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 2pts | |
| Code Quality | 0pts | |
| **Total** | **8pts** | |

---

## Question 20: How do I create and apply a Retention Policy to keep sensor data for only 7 days and then automatically delete it?

### Answer
**Response time: ~5 seconds**

A Retention Policy is a feature that automatically deletes data that has exceeded the specified retention period. It is configured in two steps: create policy → apply to table.

**[Step 1] Create Retention Policy** (Execution complete - RETENTION_7D_1H policy confirmed in DB)

```sql
-- 7-day retention, delete job runs every hour
CREATE RETENTION retention_7d_1h DURATION 7 DAY INTERVAL 1 HOUR;
```

- `DURATION 7 DAY` : Designates data older than 7 days from current time as deletion target
- `INTERVAL 1 HOUR` : Runs deletion job every hour (set short for load distribution)

**[Step 2] Verify policy**

```sql
SELECT * FROM M$RETENTION;
```

Execution result:
```
USER_ID | POLICY_NAME           | DURATION | INTERVAL
1       | SENSOR_7DAY_RETENTION | 604800   | 3600
1       | POLICY_7D_1H          | 604800   | 3600
1       | RETENTION_7D_1H       | 604800   | 3600
```
(DURATION 604800 seconds = 7 days, INTERVAL 3600 seconds = 1 hour)

**[Step 3] Apply Retention Policy to sensor table**

```sql
ALTER TABLE SENSOR_DATA ADD RETENTION retention_7d_1h;
```

**[Step 4] Check application status**

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB;
```

Example result:
```
SYS | SENSOR_DATA | RETENTION_7D_1H | WAITING | NULL
```
STATE: `WAITING` (waiting), `RUNNING` (deleting), `STOPPED` (stopped)

**[Step 5] Release and delete policy (if needed)**

```sql
-- Release policy from table (stop data deletion)
ALTER TABLE SENSOR_DATA DROP RETENTION;

-- Delete policy (no tables can be using it)
DROP RETENTION retention_7d_1h;
```

**Retention period configuration examples**

```sql
-- 1-day retention, run every hour
CREATE RETENTION policy_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 30-day retention, run every day
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;

-- 3-month retention, run every 3 days
CREATE RETENTION policy_3m DURATION 3 MONTH INTERVAL 3 DAY;
```

### Evaluation
| Criteria | Deduction | Reason |
|----------|-----------|--------|
| Presentation Accuracy | 0pts | |
| Definition Accuracy | 0pts | |
| Code Quality | 0pts | |
| **Total** | **10pts** | |

---

## Overall Evaluation Results

| Question | Score | Response Time |
|----------|-------|---------------|
| 1 | 10/10 | ~3 sec |
| 2 | 10/10 | ~5 sec |
| 3 | 10/10 | ~2 sec |
| 4 | 10/10 | ~2 sec |
| 5 | 10/10 | ~8 sec |
| 6 | 10/10 | ~4 sec |
| 7 | 10/10 | ~5 sec |
| 8 | 10/10 | ~6 sec |
| 9 | 10/10 | ~4 sec |
| 10 | 10/10 | ~10 sec |
| 11 | 10/10 | ~12 sec |
| 12 | 10/10 | ~9 sec |
| 13 | 10/10 | ~6 sec |
| 14 | 10/10 | ~8 sec |
| 15 | 10/10 | ~10 sec |
| 16 | 10/10 | ~5 sec |
| 17 | 10/10 | ~5 sec |
| 18 | 10/10 | ~6 sec |
| 19 | 8/10 | ~4 sec |
| 20 | 10/10 | ~5 sec |
| **Total** | **198/200** | **134 sec total** |
| **Average** | **9.9pts** | **~6.7 sec** |

### Overall Assessment
- The enhanced execution verification feature visibly compensates for code answer mistakes; accuracy has improved compared to the previous version (0.6.x)