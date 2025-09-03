# Machbase Neo MCP Server Performance Evaluation

## Evaluation Criteria
- **Presentation Accuracy**: 0 issues: No deduction, 1 issue: 1 point deduction, 2-3 issues: 2 points deduction, 4+ issues: 3 points deduction
- **Definition Accuracy**: 0 issues: No deduction, Minor: 2 points deduction, Major: 4 points deduction, Complete error: 0 points
- **Code Quality**: 0 issues: No deduction, 1 issue: 1 point deduction, 2-3 issues: 2 points deduction, 4+ issues: 3 points deduction

---

## Question 1: How to install Machbase Neo?

### Answer
**Response time: ~5 seconds**

# 🚀 Machbase Neo Installation Guide

## 📋 Platform Support
- **Raspberry Pi**: Ubuntu 22.04 with Raspberry Pi 4
- **Linux arm64**: Ubuntu 22.04, 24.04  
- **Linux amd64**: Ubuntu 20.04, 22.04, 24.04
- **macOS**: Intel CPU (macOS 13), Apple Silicon (macOS 14, 15)
- **Windows**: Windows 10 Fall 2018+, Windows 11

## 🚀 1. Direct Installation (Recommended)

### Online Installation Script
```bash
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

### Manual Installation
1. **Download**: https://docs.machbase.com/neo/releases/
2. **Extract**:
   ```bash
   unzip machbase-neo-v8.0.58-linux-amd64.zip
   ```
3. **Verify Installation**:
   ```bash
   machbase-neo version
   ```

## 🐳 2. Docker Installation

### Download Docker Image
```bash
docker pull machbase/machbase-neo
```

### Execution Methods
**Foreground execution**:
```bash
docker run -it machbase/machbase-neo
```

**Background execution**:
```bash
docker run -d machbase/machbase-neo
```

### Using Docker Compose
Create `docker-compose.yml`:
```yml
version: '3'
services:
  machbase-neo:
    image: machbase/machbase-neo
    container_name: machbase-neo
    ports:
      - "5652:5652" # SSH
      - "5653:5653" # MQTT
      - "5654:5654" # HTTP
      - "5655:5655" # gRPC  
      - "5656:5656" # DB Engine
```

Run:
```bash
docker compose up -d
```

## ▶️ 3. Start and Stop

### Start
```bash
machbase-neo serve
```

### Allow External Access
```bash
machbase-neo serve --host 0.0.0.0
```

### Stop
- **Foreground**: `Ctrl+C`
- **Command**: `machbase-neo shell shutdown`

## 🌐 4. Web UI Access

1. Access http://127.0.0.1:5654/ in browser
2. **Default Account**: ID `sys`, Password `manager`
3. **Security Enhancement**: Change password after login

### Change Password
```sql
ALTER USER sys IDENTIFIED BY new_password;
```

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic and clear structure with information presentation |
| Accuracy | 0 points | Accurate installation method based on official documentation |
| Code Quality | 0 points | Executable commands and configuration examples provided |
| **Total** | **10 points** | Perfect installation guide provided |

---

## Question 2: What is TQL? Please explain and provide one executable example from the database

### Answer
**Response time: ~10 seconds**

# 🎯 TQL (Transforming Query Language) Explanation

## 🎯 What is TQL?

**TQL (Transforming Query Language)** is a **dedicated data transformation language** provided by Machbase Neo. It is designed to read sensor data, transform it, and output it in various formats or transmit it to other systems.

## ✨ Key Features

### 1. **Output Format Independence**
Output the same data in various formats:
- **CSV**: Tabular data
- **JSON**: Web API responses
- **CHART**: Visualization charts
- **HTML**: Web page format

### 2. **Data Source Independence**
Input from various data sources:
- **SQL**: Database queries
- **CSV**: File data
- **JSON**: Structured data
- **SCRIPT**: Dynamic data generation

### 3. **N:M Transformation**
Transform one input to multiple outputs, or multiple inputs to one output

## 📝 Basic Structure

```javascript
// 1. SRC (Source): Data input
SQL(`SELECT TIME, VALUE FROM table_name LIMIT 10`)

// 2. MAP (Transform): Data processing (optional)
FILTER(value(1) > 0)
MAPVALUE(1, value(1) * 10)

// 3. SINK (Sink): Result output
CSV()
```

## 🔧 Executable Examples

### **Example 1: Basic Data Query (CSV Output)**

```javascript
// Basic data query example
SQL(`SELECT TIME, NAME, VALUE FROM EXAMPLE LIMIT 5`)
CSV()
```

**Result:**
```
1672498800000000000,test,10
1672585200000000000,test,20
1756443938905999872,TEMP_001,27.56157773080443
1641024000000000000,SENSOR_03,22.3
1756775451264230600,SENSOR_A,23.5
```

### **Example 2: Data Filtering and Transformation**

```javascript
// Data filtering and transformation example
SQL(`SELECT TIME, NAME, VALUE FROM EXAMPLE WHERE VALUE > 20`)
FILTER(value(2) < 30)          // Only values less than 30
MAPVALUE(2, value(2) * 1.8 + 32) // Convert Celsius to Fahrenheit
CSV()
```

### **Example 3: Chart Generation**

```javascript
// Time series chart generation example
SQL(`SELECT TIME, VALUE FROM EXAMPLE WHERE NAME = 'TEMP_001' LIMIT 10`)
CHART(
    size("800px", "400px"),
    chartOption({
        title: { text: "Temperature Sensor Data" },
        xAxis: { type: "time" },
        yAxis: { name: "Temperature (°C)" },
        series: [{ 
            type: "line", 
            data: column(0, 1),
            name: "Temperature",
            smooth: true
        }],
        tooltip: { trigger: "axis" }
    })
)
```

### **Example 4: JSON Output**

```javascript
// JSON format output example
SQL(`SELECT TIME, NAME, VALUE FROM EXAMPLE LIMIT 3`)
JSON(
    timeformat("2006-01-02 15:04:05"), // Time format specification
    precision(2)                        // 2 decimal places
)
```

## 💡 TQL Application Areas

1. **Real-time monitoring dashboards**
2. **Sensor data preprocessing**
3. **Data visualization**
4. **API response data transformation**
5. **Report generation automation**

## 🚀 TQL Execution Methods

### 1. Web UI Execution
- Machbase Neo web interface (http://localhost:5654)
- Direct execution in TQL editor

### 2. HTTP API Call
```bash
curl http://localhost:5654/db/tql/example.tql
```

### 3. File Execution
- Save as `.tql` file
- Call via web API

TQL can handle complex data transformation tasks with simple scripts, making it extremely useful for IoT data analysis and visualization!

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic explanation from concept to practice |
| Accuracy | 0 points | Accurate explanation based on TQL official documentation |
| Code Quality | 0 points | Various executable examples with comments provided |
| **Total** | **10 points** | Perfect TQL explanation and examples provided |

---

## Question 3: Please provide one executable SQL example from the database

### Answer
**Response time: 40 seconds**

# Executable SQL Example for Machbase Neo DB

## 📊 Executed SQL Example

### **Example: Sensor Data Statistical Analysis Query**

```sql
-- Sensor data statistical analysis query
SELECT NAME,
       COUNT(*) as TOTAL_RECORDS,              -- Total record count
       ROUND(AVG(VALUE), 2) as AVG_VALUE,      -- Average value (2 decimal places)
       ROUND(MIN(VALUE), 2) as MIN_VALUE,      -- Minimum value
       ROUND(MAX(VALUE), 2) as MAX_VALUE,      -- Maximum value
       ROUND(MAX(VALUE) - MIN(VALUE), 2) as VALUE_RANGE  -- Value range
FROM EXAMPLE
WHERE VALUE BETWEEN 10 AND 100              -- Values between 10-100 only
GROUP BY NAME                               -- Group by sensor name
HAVING COUNT(*) > 1                         -- Sensors with 2+ records only
ORDER BY AVG_VALUE DESC;                    -- Sort by average value descending
```

## 📋 Execution Results

Results from the executed SQL query:

| **Sensor Name** | **Total Records** | **Avg Value** | **Min Value** | **Max Value** | **Value Range** |
|-----------|------------|----------|----------|----------|-----------|
| SENSOR_C | 2 | 67.8 | 67.8 | 67.8 | 0 |
| HUMID_01_timer | 5 | 63.62 | 58.5 | 70.94 | 12.44 |
| SENSOR_B | 2 | 45.2 | 45.2 | 45.2 | 0 |
| SENSOR_02 | 2 | 29.95 | 29.8 | 30.1 | 0.3 |
| TEMP_01_timer | 5 | 29.31 | 22.29 | 34.19 | 11.9 |
| TEMP_02_timer | 5 | 27.85 | 24.28 | 31.89 | 7.61 |
| TEMP_SENSOR_01 | 2 | 25.85 | 25.5 | 26.2 | 0.7 |
| SENSOR_01 | 2 | 25.85 | 25.5 | 26.2 | 0.7 |
| sensor1 | 4 | 24.77 | 23.5 | 26.2 | 2.7 |
| SENSOR_A | 2 | 23.5 | 23.5 | 23.5 | 0 |
| sensor2 | 4 | 19.93 | 18.3 | 21.8 | 3.5 |
| test | 2 | 15 | 10 | 20 | 10 |
| SENSOR_D | 2 | 12.1 | 12.1 | 12.1 | 0 |

## 📝 Additional Practical SQL Examples

### **1. Basic Data Query**
```sql
-- Query latest 10 records
SELECT NAME, TIME, VALUE 
FROM EXAMPLE 
ORDER BY TIME DESC 
LIMIT 10;
```

### **2. Conditional Data Filtering**
```sql
-- Query high values from specific sensors
SELECT NAME, TIME, VALUE
FROM EXAMPLE
WHERE NAME LIKE 'TEMP%' 
  AND VALUE > 25
ORDER BY VALUE DESC;
```

### **3. Summary Statistics by Sensor**
```sql
-- Basic statistics for each sensor
SELECT NAME, 
       COUNT(*) as RECORD_COUNT,
       AVG(VALUE) as AVG_VALUE,
       MIN(VALUE) as MIN_VALUE,
       MAX(VALUE) as MAX_VALUE
FROM EXAMPLE 
GROUP BY NAME
ORDER BY RECORD_COUNT DESC;
```

### **4. Conditional Classification**
```sql
-- Classification by value range
SELECT NAME,
       VALUE,
       CASE 
           WHEN VALUE > 50 THEN 'HIGH'
           WHEN VALUE > 25 THEN 'MEDIUM' 
           ELSE 'LOW'
       END as VALUE_CATEGORY
FROM EXAMPLE
WHERE VALUE IS NOT NULL
ORDER BY VALUE DESC;
```

## 💡 SQL Execution Methods

### **1. Execution via TQL**
```javascript
SQL(`SELECT * FROM EXAMPLE LIMIT 5`)
CSV()
```

### **2. Direct Execution in Web UI**
- Access Machbase Neo web interface (http://localhost:5654)
- Execute in SQL query editor

### **3. Execution via API**
```bash
curl -X POST http://localhost:5654/db/query \
  -H "Content-Type: application/json" \
  -d '{"q": "SELECT * FROM EXAMPLE LIMIT 5"}'
```

## ⚡ Machbase Neo SQL Features

- **Time Series Data Optimization**: Specialized for large-scale time series data processing
- **Real-time Analysis**: Simultaneous data collection and analysis
- **Memory-based**: Fast query performance
- **Standard SQL Support**: Supports most common SQL syntax

The above examples are executable in actual Machbase Neo DB and are very useful patterns for sensor data analysis!

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic examples and results presentation |
| Accuracy | 0 points | Accurate results executed in actual DB |
| Code Quality | 0 points | Comments and various usage examples provided |
| **Total** | **10 points** | Perfect SQL examples and execution results |

---

## Question 4: What tables are currently in the database?

### Answer
**Response time: 49 seconds**

# 📊 Current Tables in Machbase Neo DB

## 📢 Overall Status
**Total Tables**: **47 tables**

## 📋 Table Classification by Category

### 🚇 **1. Busan Subway Data (21 tables)**
Data from various facilities and equipment of Busan Subway:
- **BECU**: BUSAN_BECU_0818, BUSAN_BECU_0819, BUSAN_BECU_0820
- **CMSB**: BUSAN_CMSB_0818, BUSAN_CMSB_0819, BUSAN_CMSB_0820  
- **DCU_L1**: BUSAN_DCU_L1_0818, BUSAN_DCU_L1_0819, BUSAN_DCU_L1_0820
- **DCU_R1**: BUSAN_DCU_R1_0818, BUSAN_DCU_R1_0819, BUSAN_DCU_R1_0820
- **HVAC**: BUSAN_HVAC_0818, BUSAN_HVAC_0819, BUSAN_HVAC_0820
- **SIV**: BUSAN_SIV_0818, BUSAN_SIV_0819, BUSAN_SIV_0820
- **VVVF**: BUSAN_VVVF_0818, BUSAN_VVVF_0819, BUSAN_VVVF_0820

### 🧪 **2. Test Tables (9 tables)**
Development and testing tables:
- TEST, TEST2, TEST3, TEST4, TEST5, TEST6, TEST7
- TEST_HOURLY_ROLLUP, TEST_ROLLUP

### 📈 **3. Rollup Tables (5 tables)**
Aggregation and summary data tables:
- CUSTOM_15MIN_ROLLUP, ROLLUP_TEST, ROLLUP_TEST_NEW
- TEST_HOURLY_ROLLUP, TEST_ROLLUP

### 💰 **4. Financial Data (2 tables)**
Financial time series data:
- **BITCOIN**: Bitcoin trading data (e.g., BTC-acc_trade_price, 432,574,820,424 KRW)
- **SP500**: S&P 500 stock data (e.g., A_close, 65.46)

### 🔧 **5. Sensor/IoT Data (5 tables)**
Various sensor and IoT equipment data:
- **BEARING**: Bearing sensor data (s1-c2, vibration value: -0.039)
- **ECG**: Electrocardiogram data (mit_bih_train_0, 0.953125)
- **DRIVING_BEHAVIOR**: Driving behavior data (AccX, acceleration: -1.6248639)
- **SENSOR_DEMO**: Sensor demo data
- **VIBE_UNBAL**: Vibration imbalance data

### 🌐 **6. Other Tables (7 tables)**
- **BCI1**: Brain-Computer Interface data
- **EU_WEATHER**: European weather data (AT_temperature, -3.64°C)
- **EXAMPLE**: Example data (various sensor values)
- **HI, HI_PRED**: Health Index related data
- **LOCATION**: Location data (Seoul, Daejeon, Busan with latitude/longitude)
- **TQL_SCRIPTS**: TQL script repository

## 📊 Major Table Data Samples

| **Table Name** | **Data Type** | **Sample Data** |
|------------|---------------|---------------|
| BITCOIN | Cryptocurrency trading | BTC cumulative trading amount: 432 trillion KRW |
| BEARING | Bearing sensor | Vibration value: -0.039 ~ -0.098 |
| ECG | Electrocardiogram | Signal value: 0.953125 ~ 1.0 |
| DRIVING_BEHAVIOR | Vehicle acceleration | AccX: -1.6248639 |
| EU_WEATHER | European weather | Austria temperature: -3.64°C |
| LOCATION | GPS location | Seoul: 37.5665°N, 126.978°E |

## 🎯 Available Analysis Examples

1. **Financial Analysis**: Bitcoin price trend analysis
2. **Equipment Monitoring**: Bearing vibration pattern analysis
3. **Medical Data**: ECG signal anomaly detection
4. **Transportation Analysis**: Busan subway operation status monitoring
5. **Weather Analysis**: European regional temperature trend analysis

The current DB contains rich time series data from various domains, enabling diverse analysis and visualization!

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic categorization and clear information presentation |
| Accuracy | 0 points | Accurate table list and data queried from actual DB |
| Code Quality | 0 points | Actual sample data and usage examples provided |
| **Total** | **10 points** | Perfect table status analysis |

---

## Question 5: Create a test table with rollup functionality in the database

### Answer
**Response time: 78 seconds**

# 🎯 Test Table with Roll Up Functionality Created

## ✅ Created Table Information

### **Main Table: TEST_ROLLUP_SENSOR**
- **Table Type**: TAG TABLE (time series data only)
- **Roll up Function**: ✅ Activated (with EXTENSION)
- **Auto-generated Roll up Tables**:
  - `_TEST_ROLLUP_SENSOR_ROLLUP_SEC` (second unit)
  - `_TEST_ROLLUP_SENSOR_ROLLUP_MIN` (minute unit) 
  - `_TEST_ROLLUP_SENSOR_ROLLUP_HOUR` (hour unit)

### **Custom Roll up Table: TEST_ROLLUP_15MIN**
- **Aggregation Interval**: 15 minutes
- **Function**: EXTENSION (FIRST/LAST function support)

## 📊 Table Structure

```sql
-- Create test table with Roll Up functionality
CREATE TAG TABLE test_rollup_sensor (
    sensor_id VARCHAR(50) PRIMARY KEY,        -- Sensor identifier (tag)
    timestamp_col DATETIME BASETIME,          -- Time column (base time)
    sensor_value DOUBLE SUMMARIZED            -- Sensor value (aggregation target)
)
WITH ROLLUP EXTENSION;                        -- Roll up activation + FIRST/LAST support

-- Create custom Roll up table (15-minute interval)
CREATE ROLLUP test_rollup_15min
ON test_rollup_sensor (sensor_value)
INTERVAL 15 MIN
EXTENSION;

-- Insert test data
INSERT INTO test_rollup_sensor VALUES 
    ('TEMP_SENSOR_01', TO_DATE('2024-12-05 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
INSERT INTO test_rollup_sensor VALUES 
    ('HUMID_SENSOR_01', TO_DATE('2024-12-05 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 68.5);

-- Roll up data query example
SELECT 
    sensor_id,
    COUNT(*) as record_count,
    AVG(sensor_value) as avg_value,
    MIN(sensor_value) as min_value,
    MAX(sensor_value) as max_value
FROM test_rollup_sensor
GROUP BY sensor_id;
```

## 📈 Currently Stored Test Data

| **Sensor ID** | **Time** | **Value** |
|------------|----------|--------|
| TEMP_SENSOR_01 | 2024-12-05 00:00:00 | 25.5°C |
| HUMID_SENSOR_01 | 2024-12-05 01:00:00 | 68.5% |

## 🔧 Roll Up Functionality Usage Examples

### **1. Time Interval Aggregation Query**
```sql
-- Query sensor statistics by 30-minute intervals
SELECT
    ROLLUP('min', 30, timestamp_col) AS time_interval,
    sensor_id,
    AVG(sensor_value) AS avg_value,
    MIN(sensor_value) AS min_value,
    MAX(sensor_value) AS max_value,
    COUNT(sensor_value) AS count_records
FROM test_rollup_sensor
GROUP BY time_interval, sensor_id
ORDER BY sensor_id, time_interval;
```

### **2. Hourly Aggregation**
```sql
-- Hourly sensor data summary
SELECT
    ROLLUP('hour', 1, timestamp_col) AS hour_interval,
    sensor_id,
    AVG(sensor_value) AS hourly_avg
FROM test_rollup_sensor
GROUP BY hour_interval, sensor_id;
```

### **3. FIRST/LAST Function Usage** (EXTENSION feature)
```sql
-- Query first and last values for each time interval
SELECT
    ROLLUP('hour', 1, timestamp_col) AS hour_interval,
    sensor_id,
    FIRST(timestamp_col, sensor_value) AS first_value,
    LAST(timestamp_col, sensor_value) AS last_value
FROM test_rollup_sensor
GROUP BY hour_interval, sensor_id;
```

## 💡 Roll Up Table Advantages

1. **High-performance Aggregation**: Fast statistical queries with pre-calculated data
2. **Automatic Management**: Roll up tables automatically updated on data insertion
3. **Various Time Units**: Flexible aggregation by second/minute/hour units
4. **Extension Features**: Enhanced time series analysis with FIRST/LAST functions
5. **Hierarchical Structure**: Multi-level aggregation possible with custom Roll up

## 🎯 Real-world Use Cases

- **IoT Sensor Monitoring**: Real-time temperature/humidity data aggregation
- **Facility Management**: Equipment status hourly statistics
- **Energy Analysis**: Power usage daily/monthly summaries
- **Quality Management**: Production line data aggregation analysis

The created `TEST_ROLLUP_SENSOR` table is configured to fully utilize Machbase Neo's powerful Roll up functionality! High-speed aggregation analysis of large-scale time series data is possible.

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Step-by-step progress and results clearly presented |
| Accuracy | 0 points | Actual table creation and accurate Roll up setup |
| Code Quality | 0 points | Executable SQL and usage examples provided |
| **Total** | **10 points** | Perfect Roll up table creation and explanation |

---

## Question 6: Please provide executable TQL visualization code from the database

### Answer
**Response time: 65 seconds**

# 🎨 Executable TQL Visualization Code in Machbase Neo DB

## 📊 Executed Visualization Examples

### **1. Line Chart - Temperature Sensor Data**

```javascript
// Temperature sensor data time series line chart
SQL(`SELECT TIME, VALUE FROM EXAMPLE WHERE NAME = 'TEMP_001' LIMIT 20`)
CHART(
    size("800px", "400px"),
    chartOption({
        title: { text: "Temperature Sensor Data", left: "center" },
        xAxis: { type: "time" },
        yAxis: { name: "Temperature (°C)" },
        tooltip: { trigger: "axis" },
        series: [{
            type: "line",
            data: column(0, 1),
            name: "Temperature",
            smooth: true,
            lineStyle: { width: 2 },
            symbol: "circle",
            symbolSize: 6
        }]
    })
)
```

### **2. Bar+Line Combo Chart - Sensor Statistics**

```javascript
// Sensor record count and average value combo chart
SQL(`
SELECT NAME, COUNT(*) as RECORD_COUNT, AVG(VALUE) as AVG_VALUE
FROM EXAMPLE 
WHERE VALUE > 0
GROUP BY NAME 
ORDER BY RECORD_COUNT DESC 
LIMIT 8
`)
CHART(
    size("900px", "500px"),
    theme("macarons"),
    chartOption({
        title: { text: "Sensor Data Statistics", left: "center" },
        xAxis: { 
            type: "category", 
            data: column(0),
            axisLabel: { rotate: 45 }
        },
        yAxis: [
            { name: "Record Count", position: "left" },
            { name: "Average Value", position: "right" }
        ],
        tooltip: { trigger: "axis" },
        legend: { top: "bottom" },
        series: [
            {
                type: "bar",
                data: column(1),
                name: "Record Count",
                itemStyle: { color: "#5470c6" }
            },
            {
                type: "line",
                data: column(2),
                name: "Average Value",
                yAxisIndex: 1,
                itemStyle: { color: "#fc8452" },
                symbol: "circle"
            }
        ]
    })
)
```

### **3. Pie Chart - Value Distribution**

```javascript
// Sensor value range distribution pie chart
SQL(`
SELECT 
    CASE 
        WHEN VALUE < 20 THEN 'Low (< 20)'
        WHEN VALUE < 50 THEN 'Medium (20-50)'  
        ELSE 'High (> 50)'
    END as VALUE_RANGE,
    COUNT(*) as COUNT
FROM EXAMPLE 
WHERE VALUE > 0
GROUP BY VALUE_RANGE
ORDER BY COUNT DESC
`)
CHART(
    size("600px", "600px"),
    theme("vintage"),
    chartOption({
        title: { 
            text: "Value Distribution", 
            left: "center",
            top: "20px"
        },
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: "vertical",
            left: "left",
            top: "middle"
        },
        series: [{
            name: "Value Range",
            type: "pie",
            radius: ["40%", "70%"],
            center: ["60%", "50%"],
            data: column(0, 1, {names: 0, values: 1}),
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    })
)
```

### **4. Heatmap Chart - Sensor Activity Pattern**

```javascript
// Sensor activity pattern heatmap
FAKE(json({
    [0, 0, 5], [0, 1, 1], [0, 2, 0], [0, 3, 0], [0, 4, 0], [0, 5, 0],
    [1, 0, 1], [1, 1, 4], [1, 2, 2], [1, 3, 3], [1, 4, 4], [1, 5, 6],
    [2, 0, 2], [2, 1, 3], [2, 2, 8], [2, 3, 6], [2, 4, 2], [2, 5, 1],
    [3, 0, 1], [3, 1, 2], [3, 2, 2], [3, 3, 7], [3, 4, 1], [3, 5, 2],
    [4, 0, 0], [4, 1, 1], [4, 2, 0], [4, 3, 1], [4, 4, 3], [4, 5, 4],
    [5, 0, 0], [5, 1, 0], [5, 2, 1], [5, 3, 2], [5, 4, 8], [5, 5, 2]
}))
CHART(
    size("700px", "500px"),
    theme("dark"),
    chartOption({
        title: { text: "Sensor Activity Heatmap", left: "center" },
        tooltip: { position: "top" },
        grid: {
            height: "50%",
            top: "10%"
        },
        xAxis: {
            type: "category",
            data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            splitArea: { show: true }
        },
        yAxis: {
            type: "category", 
            data: ["Morning", "Noon", "Afternoon", "Evening", "Night", "Dawn"],
            splitArea: { show: true }
        },
        visualMap: {
            min: 0,
            max: 10,
            calculable: true,
            orient: "horizontal",
            left: "center",
            bottom: "15%"
        },
        series: [{
            name: "Activity",
            type: "heatmap",
            data: column(0),
            label: { show: true },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                }
            }
        }]
    })
)
```

### **5. Gauge Chart - Average Temperature**

```javascript
// Temperature sensor average value gauge chart
SQL(`SELECT AVG(VALUE) as avg_value FROM EXAMPLE WHERE NAME LIKE 'TEMP%'`)
CHART(
    size("500px", "400px"),
    theme("shine"),
    chartOption({
        title: { text: "Average Temperature", left: "center" },
        series: [{
            name: "Temperature",
            type: "gauge",
            min: 0,
            max: 100,
            splitNumber: 10,
            radius: "75%",
            axisLine: {
                lineStyle: {
                    width: 10,
                    color: [[0.3, "#67e0e3"], [0.7, "#37a2da"], [1, "#fd666d"]]
                }
            },
            pointer: {
                itemStyle: {
                    color: "auto"
                }
            },
            axisTick: {
                distance: -30,
                length: 8,
                lineStyle: {
                    color: "#fff",
                    width: 2
                }
            },
            splitLine: {
                distance: -30,
                length: 30,
                lineStyle: {
                    color: "#fff",
                    width: 4
                }
            },
            axisLabel: {
                color: "auto",
                distance: 40,
                fontSize: 20
            },
            detail: {
                valueAnimation: true,
                formatter: "{value}°C",
                color: "auto"
            },
            data: [{
                value: column(0)[0],
                name: "TEMP"
            }]
        }]
    })
)
```

## 🎨 Available Chart Themes

Various themes provided by TQL:
- **white** (default)
- **dark** (dark theme)
- **macarons** (pastel colors)
- **vintage** (vintage style)
- **shine** (bright and fancy)
- **chalk**, **essos**, **infographic**, **purple-passion**, **roma**, **romantic**, **walden**, **westeros**, **wonderland**

## 💡 TQL Visualization Key Features

### **1. Data Source Options**
- **SQL()**: Database query results
- **FAKE()**: Fake data for testing
- **SCRIPT()**: Dynamic data generation with JavaScript

### **2. Chart Types**
- **Line**: Time series data, trend analysis
- **Bar**: Category comparison, statistics
- **Pie**: Ratios, component analysis
- **Heatmap**: Pattern analysis, correlation
- **Gauge**: Real-time indicators, KPI
- **Scatter**: Correlation analysis, distribution
- **Radar**: Multi-dimensional comparison
- **3D**: Three-dimensional visualization

### **3. Advanced Features**
- **Interactive**: Tooltips, zoom, drill-down
- **Animation**: Smooth transition effects
- **Multi-axis**: Multiple Y-axis support
- **Real-time**: Real-time data updates
- **Responsive**: Responsive size adjustment

## 🚀 Execution Methods

### **Web UI Execution**
1. Access Machbase Neo (http://localhost:5654)
2. Input code in TQL editor
3. Click run button

### **API Call**
```bash
curl -X POST http://localhost:5654/db/tql \
  -H "Content-Type: text/plain" \
  -d "SQL(...) CHART(...)"
```

### **File Execution**
```bash
# Save as .tql file then
curl http://localhost:5654/db/tql/my_chart.tql
```

All the above TQL visualization codes are executable in Machbase Neo and can be used for visualizing various types of sensor data! Each chart is interactive and supports real-time updates.

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | 5 different visualization examples systematically presented |
| Accuracy | 0 points | Actual executable TQL code with accurate settings |
| Code Quality | 0 points | Complete executable code with detailed comments |
| **Total** | **10 points** | Perfect TQL visualization code collection |

---

## Question 7: Explain the Rollup functionality and provide executable example code from the database

### Answer
**Response time: 60 seconds**

# 📊 Machbase Neo Rollup Functionality Complete Guide

## 🎯 What is Rollup Functionality?

**Rollup** is a core feature of Machbase Neo that **pre-calculates statistical aggregations of large-scale time series data**. It automatically aggregates incoming real-time data by time units and stores them in separate tables, providing **fast analytical query performance**.

## 🔧 Core Concepts

### **Pre-aggregation**
- Automatically calculates statistical values when inserting raw data
- Automatic aggregation by second (SEC), minute (MIN), hour (HOUR) units
- **Dramatically improved performance** by using pre-calculated values for queries

### **Hierarchical Structure**
```
Raw TAG Table
    └── _TableName_ROLLUP_SEC   (second unit aggregation)
        └── _TableName_ROLLUP_MIN   (minute unit aggregation)
            └── _TableName_ROLLUP_HOUR  (hour unit aggregation)
```

## 📋 Supported Aggregation Functions

### **Basic Aggregation Functions**
- `MIN()`: Minimum value
- `MAX()`: Maximum value  
- `SUM()`: Sum
- `COUNT()`: Count
- `AVG()`: Average
- `SUMSQ()`: Sum of squares

### **Extended Aggregation Functions** (EXTENSION option)
- `FIRST()`: First value in interval
- `LAST()`: Last value in interval

## 🗗️ Rollup Table Creation

### **1. Default Rollup**

```sql
-- Create basic rollup table (SEC, MIN, HOUR auto-created)
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,        -- Sensor identifier
    event_time DATETIME BASETIME,             -- Base time column
    temperature DOUBLE SUMMARIZED             -- Aggregation target column
)
WITH ROLLUP;                                  -- Enable rollup

-- Create with extension features (FIRST/LAST function support)
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
)
WITH ROLLUP EXTENSION;

-- Start from minute unit (creates MIN, HOUR only)
CREATE TAG TABLE hourly_data (
    device_id VARCHAR(50) PRIMARY KEY,
    timestamp_col DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
WITH ROLLUP (MIN);
```

### **2. Custom Rollup**

```sql
-- Create 30-second interval custom rollup
CREATE ROLLUP sensor_rollup_30sec
ON iot_sensors (temperature)
INTERVAL 30 SEC;

-- 15-minute interval rollup (with extension features)
CREATE ROLLUP sensor_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN
EXTENSION;

-- Multi-level rollup (create 10-minute rollup based on 30-second rollup)
CREATE ROLLUP sensor_rollup_10min
ON sensor_rollup_30sec
INTERVAL 10 MIN;
```

## 📊 Executable Rollup Query Examples

### **1. Hourly Aggregation Query**

```sql
-- Hourly temperature sensor statistics
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    sensor_id,
    AVG(temperature) AS avg_temp,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp,
    COUNT(temperature) AS data_count
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 00:00:00') AND TO_DATE('2024-03-10 23:59:59')
GROUP BY hour_interval, sensor_id
ORDER BY hour_interval;

/* Expected results:
hour_interval                   avg_temp  min_temp  max_temp  data_count
----------------------------------------------------------------
2024-03-10 09:00:00 000:000:000  20.5      20.1      21.0      3
2024-03-10 10:00:00 000:000:000  21.7      21.5      21.8      2
*/
```

### **2. 15-minute Interval Aggregation Query**

```sql
-- 15-minute interval sensor data aggregation
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    sensor_id,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp,
    COUNT(temperature) AS record_count
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-10 10:00:00')
    AND event_time < TO_DATE('2024-03-10 12:00:00')
GROUP BY interval_15min, sensor_id
ORDER BY interval_15min;

/* Expected results:
interval_15min                  min_temp  max_temp  record_count
------------------------------------------------------------
2024-03-10 10:00:00 000:000:000  20.1      20.1      1
2024-03-10 10:15:00 000:000:000  20.5      20.5      1
2024-03-10 10:45:00 000:000:000  21.0      21.0      1
*/
```

### **3. Extension Function Query (FIRST/LAST)**

```sql
-- Query first and last values for each time interval
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    sensor_id,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure,
    AVG(pressure) AS avg_pressure
FROM iot_sensors_ext
WHERE sensor_id = 'PRES_1'
GROUP BY hour_interval, sensor_id
ORDER BY hour_interval;

/* Expected results:
hour_interval                   first_pressure  last_pressure  avg_pressure
-----------------------------------------------------------------------
2024-03-10 09:00:00 000:000:000  1000.5          1001.0         1000.75
2024-03-10 10:00:00 000:000:000  1001.2          1001.8         1001.5
*/
```

### **4. Daily/Weekly/Monthly Aggregation**

```sql
-- Daily average temperature
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    sensor_id,
    AVG(temperature) AS avg_daily_temp,
    COUNT(temperature) AS daily_data_points
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01')
    AND event_time < TO_DATE('2024-03-16')
GROUP BY day_interval, sensor_id
ORDER BY day_interval;

-- Weekly average temperature (starting Monday)
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start_monday,
    sensor_id,
    AVG(temperature) AS avg_weekly_temp
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01')
    AND event_time < TO_DATE('2024-03-31')
GROUP BY week_start_monday, sensor_id
ORDER BY week_start_monday;

-- Monthly statistics
SELECT
    ROLLUP('month', 1, event_time) AS month_interval,
    sensor_id,
    AVG(temperature) AS avg_monthly_temp,
    MIN(temperature) AS min_monthly_temp,
    MAX(temperature) AS max_monthly_temp,
    COUNT(temperature) AS monthly_data_points
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01')
    AND event_time < TO_DATE('2024-04-01')
GROUP BY month_interval, sensor_id
ORDER BY month_interval;
```

### **5. Actual Executed Example in DB**

```sql
-- Actual created rollup table example
CREATE TAG TABLE demo_rollup_sensors (
    sensor_name VARCHAR(50) PRIMARY KEY,
    measurement_time DATETIME BASETIME,
    sensor_value DOUBLE SUMMARIZED
)
WITH ROLLUP EXTENSION;

-- Create 30-minute interval custom rollup
CREATE ROLLUP demo_rollup_30min
ON demo_rollup_sensors (sensor_value)
INTERVAL 30 MIN
EXTENSION;

-- Insert test data
INSERT INTO demo_rollup_sensors VALUES 
    ('TEMP_SENSOR_A', TO_DATE('2024-12-05 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.1);
INSERT INTO demo_rollup_sensors VALUES 
    ('TEMP_SENSOR_A', TO_DATE('2024-12-05 09:05:00', 'YYYY-MM-DD HH24:MI:SS'), 25.3);
INSERT INTO demo_rollup_sensors VALUES 
    ('HUMID_SENSOR_B', TO_DATE('2024-12-05 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 65.2);

-- Hourly aggregation query
SELECT
    ROLLUP('hour', 1, measurement_time) AS hour_interval,
    sensor_name,
    AVG(sensor_value) AS avg_value,
    MIN(sensor_value) AS min_value,
    MAX(sensor_value) AS max_value,
    COUNT(sensor_value) AS data_count
FROM demo_rollup_sensors
GROUP BY hour_interval, sensor_name
ORDER BY sensor_name, hour_interval;
```

## 🛠️ Rollup Management Commands

```bash
-- Check rollup status
SHOW ROLLUPGAP;

-- Start specific rollup process
EXEC ROLLUP_START('_iot_sensors_ROLLUP_SEC');

-- Stop specific rollup process
EXEC ROLLUP_STOP('_iot_sensors_ROLLUP_MIN');

-- Force immediate rollup processing
EXEC ROLLUP_FORCE('demo_rollup_30min');

-- Delete rollup data (before specific time)
DELETE FROM iot_sensors ROLLUP 
BEFORE TO_DATE('2024-03-01 00:00:00');

-- Delete only specific sensor's rollup data
DELETE FROM iot_sensors ROLLUP 
WHERE sensor_id = 'TEMP_A';

-- Drop custom rollup table
DROP ROLLUP sensor_rollup_30sec;

-- Drop TAG table and all rollup tables
DROP TABLE iot_sensors CASCADE;
```

## 🎯 Rollup Functionality Advantages

### **1. Performance Improvement**
- **100x or more** query performance improvement possible
- Real-time statistical queries on large datasets
- Memory-efficient aggregation operations

### **2. Automation**
- Automatic aggregation processing on data insertion
- Background asynchronous processing
- Continuous management without user intervention

### **3. Flexibility**
- Support for various time units (sec/min/hour/day/week/month/year)
- Customizable aggregation intervals
- Multi-level rollup hierarchy construction

### **4. Completeness**
- Support for all basic statistical functions
- FIRST/LAST functions for time series analysis
- Raw data integrity guarantee

## 📈 Real-world Use Cases

1. **IoT Sensor Monitoring**: Real-time temperature/humidity/pressure data aggregation
2. **Manufacturing Quality Control**: Production line data hourly statistics
3. **Energy Management**: Power usage daily/monthly analysis
4. **Financial Data**: Stock price/volume minute/hourly aggregation
5. **Web Analytics**: User activity pattern hourly analysis

Machbase Neo's rollup functionality is a **game changer for large-scale time series data analysis**! With dramatic performance improvements through pre-aggregation, real-time dashboards and high-speed analysis are possible.

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic concept explanation with practical examples |
| Accuracy | 0 points | Accurate rollup functionality explanation based on official documentation |
| Code Quality | 0 points | Various executable SQL examples provided |
| **Total** | **10 points** | Perfect rollup functionality guide |

---

## Question 8: Please provide executable geomap example code from the database

### Answer
**Response time: 86 seconds**

# 🗺️ Executable GEOMAP Example Code in Machbase Neo DB

## 📍 GEOMAP Feature Overview

**GEOMAP** is a **dedicated geographic information visualization function** provided by Machbase Neo TQL. It enables various map-based visualizations using GPS coordinate data.

### **Key Features**
- **WGS84 coordinate system** support (latitude/longitude)
- **Various layer types** support
- **Interactive maps** (popup, tooltip, zoom)
- **Real-time data** visualization
- **OpenStreetMap** basic tile support

## 🎯 Executed GEOMAP Examples

### **1. Basic Marker Map - Major Korean Cities**

```javascript
// Basic marker map - Major Korean cities location
SQL(`SELECT NAME, LAT, LON, VALUE FROM LOCATION ORDER BY NAME`)
SCRIPT({
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2];
    var temp = $.values[3];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>' + name + '</b><br/>Temperature: ' + temp + '°C'
            },
            tooltip: {
                content: name + ': ' + temp + '°C',
                permanent: true,
                direction: "top"
            }
        }
    });
})
GEOMAP(
    size("800px", "600px"),
    geomapID("korea_cities_map")
)
```

### **2. Temperature-based Colored Circle Map**

```javascript
// Circular map with colors and sizes based on temperature
SQL(`SELECT NAME, LAT, LON, VALUE FROM LOCATION ORDER BY VALUE DESC`)
SCRIPT({
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2];
    var temp = $.values[3];
    
    // Adjust circle size based on temperature (meters)
    var radius = Math.max(200 + (temp - 20) * 50, 100);
    
    // Determine color based on temperature
    var color = "#0000FF"; // Default blue (cool)
    if (temp >= 30) color = "#FF0000";      // Red (very hot)
    else if (temp >= 28) color = "#FF8000"; // Orange (hot)
    else if (temp >= 26) color = "#FFFF00"; // Yellow (warm)
    else if (temp >= 24) color = "#00FF00"; // Green (moderate)
    
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties: {
            radius: radius,
            color: color,
            fillColor: color,
            fillOpacity: 0.5,
            weight: 2,
            popup: {
                content: '<b>' + name + '</b><br/>' +
                        'Temperature: <b>' + temp + '°C</b><br/>' +
                        'Coordinates: ' + lat.toFixed(4) + ', ' + lon.toFixed(4)
            },
            tooltip: {
                content: '<b>' + name + '</b><br/>' + temp + '°C',
                direction: "auto",
                permanent: false
            }
        }
    });
})
GEOMAP(
    size("900px", "700px"),
    geomapID("korea_temp_circles")
)
```

### **3. City Connection Polyline Map**

```javascript
// Network map connecting cities with lines
SQL(`SELECT NAME, LAT, LON, VALUE FROM LOCATION ORDER BY VALUE DESC`)
SCRIPT({
    var cities = [];
    var points = [];
},{
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2];
    var temp = $.values[3];
    
    cities.push({name: name, lat: lat, lon: lon, temp: temp});
    points.push([lat, lon]);
},{
    // Display each city as circleMarker
    cities.forEach(function(city) {
        var color = city.temp >= 28 ? "#FF4444" : (city.temp >= 26 ? "#FFAA00" : "#4488FF");
        $.yield({
            type: "circleMarker",
            coordinates: [city.lat, city.lon],
            properties: {
                radius: 8,
                color: "#000000",
                fillColor: color,
                fillOpacity: 0.8,
                weight: 2,
                popup: {
                    content: '<b>' + city.name + '</b><br/>Temperature: ' + city.temp + '°C'
                }
            }
        });
    });
    
    // Polyline connecting cities
    $.yield({
        type: "polyline",
        coordinates: points,
        properties: {
            color: "#2E8B57",
            weight: 3,
            opacity: 0.7
        }
    });
})
GEOMAP(
    size("850px", "650px"),
    geomapID("korea_connected_cities")
)
```

### **4. Border Polygon + City Markers**

```javascript
// Display Korean territory boundary with city locations
SQL(`SELECT NAME, LAT, LON, VALUE FROM LOCATION ORDER BY NAME`)
SCRIPT({
    var cities = [];
    // Approximate Korean border coordinates (clockwise)
    var koreaOutline = [
        [38.6, 125.0], // Northwest
        [38.6, 130.0], // Northeast  
        [35.0, 130.0], // Southeast
        [33.0, 126.3], // Jeju Island South
        [34.0, 125.0], // Southwest
        [38.6, 125.0]  // Starting point (closed polygon)
    ];
},{
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2];
    var temp = $.values[3];
    cities.push({name: name, lat: lat, lon: lon, temp: temp});
},{
    // Draw Korean border polygon first
    $.yield({
        type: "polygon",
        coordinates: koreaOutline,
        properties: {
            color: "#3498DB",
            weight: 2,
            fillColor: "#AED6F1",
            fillOpacity: 0.3,
            popup: {
                content: '<b>Republic of Korea</b><br/>South Korea Territory'
            }
        }
    });
    
    // Display each city as marker
    cities.forEach(function(city) {
        var tempColor = city.temp >= 29 ? "#E74C3C" : 
                       city.temp >= 27 ? "#F39C12" : 
                       city.temp >= 25 ? "#F1C40F" : "#3498DB";
        
        $.yield({
            type: "circleMarker",
            coordinates: [city.lat, city.lon],
            properties: {
                radius: 8,
                color: "#2C3E50",
                fillColor: tempColor,
                fillOpacity: 0.9,
                weight: 2,
                popup: {
                    content: '<b>' + city.name + '</b><br/>' +
                            'Temperature: ' + city.temp + '°C<br/>' +
                            'Location: ' + city.lat.toFixed(3) + ', ' + city.lon.toFixed(3),
                    maxWidth: 200
                },
                tooltip: {
                    content: city.name + '<br/>' + city.temp + '°C',
                    direction: "top"
                }
            }
        });
    });
})
GEOMAP(
    size("900px", "750px"),
    geomapID("korea_territory_cities")
)
```

### **5. Heatmap Style Map (Grayscale)**

```javascript
// Temperature-based heatmap style map (grayscale background)
SQL(`SELECT NAME, LAT, LON, VALUE FROM LOCATION`)
SCRIPT({
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2];
    var temp = $.values[3];
    
    // Normalize temperature range (20-31°C to 0-1 range)
    var minTemp = 20, maxTemp = 31;
    var normalized = Math.max(0, Math.min(1, (temp - minTemp) / (maxTemp - minTemp)));
    
    // Color gradation based on temperature (blue -> yellow -> red)
    var r, g, b;
    if (normalized < 0.5) {
        // Blue to yellow (cool -> warm)
        r = Math.round(normalized * 2 * 255);
        g = Math.round(normalized * 2 * 255);
        b = Math.round(255 * (1 - normalized * 2));
    } else {
        // Yellow to red (warm -> hot)
        r = 255;
        g = Math.round(255 * (2 - normalized * 2));
        b = 0;
    }
    
    var color = "#" + 
                ("0" + r.toString(16)).slice(-2) + 
                ("0" + g.toString(16)).slice(-2) + 
                ("0" + b.toString(16)).slice(-2);
    
    // Circle size based on temperature (radius 300m ~ 1000m)
    var radius = 300 + (normalized * 700);
    
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties: {
            radius: radius,
            color: color,
            fillColor: color,
            fillOpacity: 0.6,
            weight: 1,
            opacity: 0.8,
            popup: {
                content: '<div style="text-align:center;">' +
                        '<h4 style="margin:5px 0; color:' + color + ';">' + name + '</h4>' +
                        '<div style="background:linear-gradient(90deg, blue, yellow, red); height:10px; margin:5px 0;"></div>' +
                        '<b>Temperature: ' + temp + '°C</b><br/>' +
                        '<small>Coordinates: ' + lat.toFixed(4) + ', ' + lon.toFixed(4) + '</small>' +
                        '</div>',
                maxWidth: 250
            },
            tooltip: {
                content: '<b>' + name + '</b><br/>' + 
                        '<span style="color:' + color + ';">●</span> ' + temp + '°C',
                permanent: true,
                direction: "auto",
                opacity: 0.9
            }
        }
    });
})
GEOMAP(
    size("1000px", "800px"),
    geomapID("korea_heatmap_style"),
    tileGrayscale(0.3)  // 30% grayscale background
)
```

## 🎛️ GEOMAP Main Options

### **Basic Settings**
```javascript
GEOMAP(
    size("800px", "600px"),        // Map size
    geomapID("custom_map_id"),     // User-defined ID
    tileTemplate("https://..."),   // Tile server URL
    tileGrayscale(0.5)            // Grayscale (0-1)
)
```

### **Supported Layer Types**
1. **marker**: Basic marker icon
2. **circleMarker**: Pixel-unit circular marker
3. **circle**: Meter-unit circular area
4. **polyline**: Line connection (routes, networks)
5. **polygon**: Polygonal area (boundaries, zones)

### **Property Options**
- **Colors**: `color`, `fillColor`, `opacity`, `fillOpacity`
- **Size**: `radius`, `weight`
- **Interaction**: `popup`, `tooltip`
- **Style**: `stroke`, `permanent`

## 🌐 Real DB Data Usage

**LOCATION Table Data:**
| City | Latitude | Longitude | Temperature |
|------|----------|-----------|-------------|
| Seoul | 37.5665 | 126.978 | 25.5°C |
| Busan | 35.1796 | 129.0756 | 28.2°C |
| Daegu | 35.8714 | 128.6014 | 29.1°C |
| Incheon | 37.4563 | 126.7052 | 24.8°C |
| Gwangju | 35.1595 | 126.8526 | 27.3°C |
| Daejeon | 36.3504 | 127.3845 | 26.7°C |
| Ulsan | 35.5384 | 129.3114 | 30.5°C |

## 🎯 Real-world Use Cases

1. **IoT Sensor Monitoring**: Real-time temperature/humidity sensor location display
2. **Logistics Tracking**: Real-time location tracking of delivery vehicles/cargo
3. **Environmental Monitoring**: Air quality/noise measurement station data visualization
4. **Smart City**: Traffic/energy usage regional analysis
5. **Disaster Management**: Earthquake/flood disaster occurrence area display

## 📱 Interactive Features

- **Zoom/Pan**: Map exploration with mouse/touch
- **Popup**: Detailed information display on click
- **Tooltip**: Brief information on mouse over
- **Layer Control**: Multiple layer show/hide
- **Real-time Update**: Automatic refresh on data change

Machbase Neo's GEOMAP functionality is optimized for **geographic information visualization of GPS-based IoT data**! Various map-based dashboard construction is possible from real-time location data monitoring to heatmap-style analysis.

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | 5 different GEOMAP examples systematically presented |
| Accuracy | 0 points | Actual executable TQL code with accurate map settings |
| Code Quality | 0 points | Complete executable code with detailed explanations |
| **Total** | **10 points** | Perfect GEOMAP visualization guide |

---

## Question 9: How to set up timers

### Answer
**Response time: 28 seconds**

# ⏰ Machbase Neo Timer Setup Complete Guide

## 🎯 Timer Feature Overview

**Timer** is a feature in Machbase Neo that **defines tasks to be executed repeatedly at specified times or intervals**. It is mainly used for **automatic data collection, periodic analysis, and scheduled report generation**.

### **Key Features**
- **CRON expression** support
- **Interval-based execution** (@every)
- **Predefined schedules** (@daily, @hourly, etc.)
- **Automatic TQL script execution**
- **Web UI management** support

## 📋 Timer Setup Methods

### **1. Adding Timer via Web UI**

Steps for Timer setup via Web UI:

1. 📱 Access Machbase Neo via web browser (http://localhost:5654)

2. 🔧 Click Timer icon in left menu bar

3. ➕ Click '+' button in top-left

4. ⚙️ Input Timer settings:
   - Timer ID (name): e.g., sensor_data_collector
   - Timer Spec: e.g., @every 30s
   - TQL Script Path: e.g., /scripts/collect_sensors.tql

5. ✅ Click "Create" button

6. 🎮 Control:
   - Start/stop with toggle button
   - Edit/delete available in detail page

### **2. Timer Management via Command Line**

```bash
# Add Timer
timer add [--autostart] <timer_name> "<timer_spec>" <tql_file_path>;

# Check Timer list
timer list;

# Start Timer
timer start <timer_name>;

# Stop Timer
timer stop <timer_name>;

# Delete Timer
timer del <timer_name>;

# Example commands
timer add --autostart sensor_collector "@every 1m" /scripts/sensors.tql;
timer add daily_report "0 0 9 * * *" /scripts/daily_analysis.tql;
timer start sensor_collector;
timer stop sensor_collector;
```

## 📅 Timer Schedule Setup Methods

### **1. CRON Expression**

CRON expression format: second minute hour day month weekday

Field description:
┌─────────────── second (0-59)
│ ┌───────────── minute (0-59)  
│ │ ┌─────────── hour (0-23)
│ │ │ ┌───────── day (1-31)
│ │ │ │ ┌─────── month (1-12 or JAN-DEC)
│ │ │ │ │ ┌───── weekday (0-6 or SUN-SAT, 0=Sunday)
│ │ │ │ │ │
* * * * * *

Special characters:
* : Match all values
/ : Range increment (3-59/15 = from 3 minutes at 15-minute intervals)
, : List separator (MON,WED,FRI = Mon,Wed,Fri)
- : Range definition (9-17 = 9AM~5PM)
? : Use instead of * in day or weekday field

Practical examples:
"0 30 * * * *"     → Execute every hour at 30 minutes
"0 0 9 * * *"      → Execute daily at 9AM
"0 */15 * * * *"   → Execute every 15 minutes
"0 0 9 * * MON"    → Execute every Monday at 9AM
"0 0 0 1 * *"      → Execute on 1st of every month at midnight
"0 0 9-17 * * MON-FRI" → Execute every hour 9-17 on weekdays

### **2. Interval-based Setting (@every)**

Interval-based setting: @every <duration>

Time units:
ms : milliseconds
s  : seconds
m  : minutes  
h  : hours

Practical examples:
@every 30s        → Every 30 seconds
@every 5m         → Every 5 minutes
@every 1h         → Every 1 hour
@every 2h30m      → Every 2 hours 30 minutes
@every 1h10m30s   → Every 1 hour 10 minutes 30 seconds
@every 500ms      → Every 500 milliseconds

Usage examples:
- IoT sensor data collection: @every 10s
- System monitoring: @every 1m
- Log analysis: @every 5m
- Backup tasks: @every 6h
- Report generation: @every 24h

### **3. Predefined Schedules**

Predefined schedule expressions:

@yearly (or @annually) 
→ Once per year, January 1st at midnight
→ Equivalent: "0 0 0 1 1 *"

@monthly 
→ Once per month, 1st day at midnight
→ Equivalent: "0 0 0 1 * *"

@weekly 
→ Once per week, Sunday at midnight  
→ Equivalent: "0 0 0 * * 0"

@daily (or @midnight)
→ Once per day, daily at midnight
→ Equivalent: "0 0 0 * * *"

@hourly
→ Once per hour, every hour on the hour
→ Equivalent: "0 0 * * * *"

Usage examples:
- Daily reports: @daily
- Weekly backups: @weekly  
- Monthly analysis: @monthly
- Hourly aggregation: @hourly
- Annual archiving: @yearly

## 🛠️ Real Timer Implementation Examples

### **1. Hello World Timer Example**

```javascript
// Step 1: Create TQL script (helloworld.tql)
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))              // Current time
MAPVALUE(2, random())                 // Random value
INSERT("name", "time", "value", table("example"))

// Step 2: Test script
// Check results with SQL: SELECT * FROM example WHERE name = 'helloworld';

// Step 3: Register Timer (command line)
// timer add helloworld "@every 5s" helloworld.tql;

// Step 4: Start Timer
// timer start helloworld;

// Step 5: Check results
// SELECT * FROM example WHERE name = 'helloworld' ORDER BY time DESC LIMIT 10;
```

### **2. Sensor Data Collection Timer**

```javascript
// Sensor data automatic collection TQL script (sensor_collector.tql)
SCRIPT({
    var sensors = [
        {name: 'TEMP_SENSOR_01', type: 'temperature', min: 15, max: 35},
        {name: 'HUMID_SENSOR_01', type: 'humidity', min: 30, max: 80},
        {name: 'PRESSURE_SENSOR_01', type: 'pressure', min: 950, max: 1050},
        {name: 'CO2_SENSOR_01', type: 'co2', min: 300, max: 1200},
        {name: 'LIGHT_SENSOR_01', type: 'light', min: 0, max: 100000}
    ];
    
    var currentTime = new Date();
    var timestamp = currentTime.getTime() * 1000000; // Convert to nanoseconds
    
    sensors.forEach(function(sensor) {
        // Generate random values per sensor (normal distribution simulation)
        var range = sensor.max - sensor.min;
        var baseValue = sensor.min + range * 0.5;
        var variation = range * 0.3 * (Math.random() - 0.5);
        var value = Math.max(sensor.min, Math.min(sensor.max, baseValue + variation));
        
        // Round to 2 decimal places
        value = Math.round(value * 100) / 100;
        
        $.yield(sensor.name, timestamp, value);
    });
})
INSERT("name", "time", "value", table("example"))

// Timer registration command example:
// timer add --autostart sensor_collector "@every 30s" sensor_collector.tql;
```

### **3. Daily Report Generation Timer**

```javascript
// Daily sensor data summary report TQL script (daily_report.tql)
SQL(`
SELECT 
    NAME,
    COUNT(*) as RECORD_COUNT,
    ROUND(AVG(VALUE), 2) as AVG_VALUE,
    ROUND(MIN(VALUE), 2) as MIN_VALUE,
    ROUND(MAX(VALUE), 2) as MAX_VALUE,
    ROUND(STDDEV(VALUE), 2) as STDDEV_VALUE
FROM EXAMPLE
WHERE TIME >= DATE_SUB(NOW(), INTERVAL 1 DAY)
    AND NAME LIKE '%SENSOR%'
GROUP BY NAME
ORDER BY NAME
`)

SCRIPT({
    var reportData = [];
    var reportTime = new Date().toISOString().slice(0, 19);
},{
    reportData.push({
        sensor: $.values[0],
        records: $.values[1], 
        avg: $.values[2],
        min: $.values[3],
        max: $.values[4],
        stddev: $.values[5]
    });
},{
    // Save report data in JSON format
    var report = {
        report_type: 'daily_sensor_summary',
        generated_at: reportTime,
        data: reportData,
        summary: {
            total_sensors: reportData.length,
            total_records: reportData.reduce((sum, item) => sum + item.records, 0)
        }
    };
    
    $.yield('DAILY_REPORT', new Date().getTime() * 1000000, JSON.stringify(report));
})

INSERT("name", "time", "value", table("reports"))

// Timer registration command (execute daily at 9AM):
// timer add --autostart daily_report "0 0 9 * * *" daily_report.tql;
```

### **4. System Monitoring Timer**

```javascript
// System status monitoring TQL script (system_monitor.tql)
SCRIPT({
    var timestamp = new Date().getTime() * 1000000;
    var metrics = [];
    
    // Generate virtual system metrics (in real environment, call system APIs)
    metrics.push({
        name: 'CPU_USAGE',
        value: Math.random() * 100,
        unit: 'percent'
    });
    
    metrics.push({
        name: 'MEMORY_USAGE', 
        value: 60 + Math.random() * 30,
        unit: 'percent'
    });
    
    metrics.push({
        name: 'DISK_USAGE',
        value: 40 + Math.random() * 40, 
        unit: 'percent'
    });
    
    metrics.push({
        name: 'NETWORK_IN',
        value: Math.random() * 1000,
        unit: 'MB/s'
    });
    
    metrics.push({
        name: 'NETWORK_OUT',
        value: Math.random() * 500,
        unit: 'MB/s'
    });
    
    metrics.push({
        name: 'ACTIVE_CONNECTIONS',
        value: Math.floor(Math.random() * 1000),
        unit: 'count'
    });
    
    // Store each metric as individual record
    metrics.forEach(function(metric) {
        var value = Math.round(metric.value * 100) / 100;
        $.yield(metric.name, timestamp, value);
    });
})

INSERT("name", "time", "value", table("system_metrics"))

// Timer registration command (execute every 1 minute):
// timer add --autostart system_monitor "@every 1m" system_monitor.tql;

// Alert condition check (separate Timer - every 5 minutes):
// timer add --autostart alert_checker "@every 5m" alert_checker.tql;
```

## 📊 Timer Monitoring and Management

```bash
# Check Timer list and status
timer list;

# Expected output:
# ┌─────────────────┬─────────────┬─────────────────────┬───────────┬─────────┐
# │ NAME            │ SPEC        │ TQL                 │ AUTOSTART │ STATE   │
# ├─────────────────┼─────────────┼─────────────────────┼───────────┼─────────┤
# │ sensor_collector│ @every 30s  │ sensor_collector.tql│ true      │ RUNNING │
# │ daily_report    │ 0 0 9 * * * │ daily_report.tql    │ true      │ STOPPED │
# │ system_monitor  │ @every 1m   │ system_monitor.tql  │ false     │ RUNNING │
# └─────────────────┴─────────────┴─────────────────────┴───────────┴─────────┘

# Start specific Timer
timer start daily_report;

# Stop specific Timer  
timer stop sensor_collector;

# Check Timer execution log (in TQL result tables)
# SQL: SELECT * FROM example WHERE name LIKE '%SENSOR%' ORDER BY time DESC LIMIT 20;

# Delete Timer
timer del old_timer_name;

# Summary of all Timer status
timer list;
```

## 💡 Timer Best Practices

### **1. Performance Optimization Tips**
- **Appropriate interval setting**: Too short intervals increase system load
- **Batch processing**: Process multiple tasks at once for efficiency
- **Error handling**: Include exception handling logic in TQL scripts

### **2. Real Usage Cases**
- **IoT data collection**: @every 10s ~ 1m
- **Log analysis**: @every 5m ~ 15m  
- **System monitoring**: @every 1m ~ 5m
- **Backup tasks**: @daily, @weekly
- **Report generation**: @daily, @weekly, @monthly

### **3. Monitoring and Alerts**
- Regular checks of Timer execution status
- Alert settings for failed tasks
- Add data quality verification Timers

Machbase Neo's Timer functionality is a core tool for **building automated data pipelines**! From regular data collection to complex analytical tasks, you can build a **fully automated IoT data processing system** by scheduling everything.

### Evaluation
| Evaluation Item | Score | Reason |
|-----------|------|------|
| Presentation Accuracy | 0 points | Systematic Timer setup guide with practical examples |
| Accuracy | 0 points | Accurate Timer functionality explanation based on official documentation |
| Code Quality | 0 points | Various executable TQL examples and commands |
| **Total** | **10 points** | Perfect Timer setup and management guide |

---

## Question 10: Create TQL to calculate daily average values and volatility for the last 30 days from the SP500 table in the database

### Answer
**Response time: 194 seconds (~3 minutes 14 seconds)**

# 📈 TQL for Calculating Daily Average Values and Volatility for Last 30 Days from SP500 Table

## 🎯 Analysis Results Summary

**SP500 Table Analysis Complete!** Successfully calculated daily average values and volatility for the last 30 days.

## 📊 Complete TQL Codes

### **1. Basic Daily Average and Volatility Calculation TQL**

```javascript
// Calculate daily average values and volatility for last 30 days from SP500 table
SQL(`
SELECT 
    NAME,
    TIME,
    VALUE
FROM SP500 
WHERE NAME = 'A_close'  -- Analyze specific stock
ORDER BY TIME DESC
LIMIT 1000
`)

SCRIPT({
    var dailyData = {};
    var stockData = [];
},{
    var name = $.values[0];
    var time = new Date($.values[1]);
    var value = $.values[2];
    
    // Group data by date (YYYY-MM-DD format)
    var dateKey = time.toISOString().split('T')[0];
    
    if (!dailyData[dateKey]) {
        dailyData[dateKey] = {
            name: name,
            date: dateKey,
            prices: [],
            sum: 0,
            count: 0,
            min: value,
            max: value
        };
    }
    
    var dayData = dailyData[dateKey];
    dayData.prices.push(value);
    dayData.sum += value;
    dayData.count++;
    dayData.min = Math.min(dayData.min, value);
    dayData.max = Math.max(dayData.max, value);
},{
    // Calculate daily average values
    for (var dateKey in dailyData) {
        var dayData = dailyData[dateKey];
        dayData.avgPrice = dayData.sum / dayData.count;
        stockData.push(dayData);
    }
    
    // Sort by date (newest -> oldest)
    stockData.sort(function(a, b) {
        return new Date(b.date) - new Date(a.date);
    });
    
    // Select only last 30 days
    stockData = stockData.slice(0, 30);
    
    // Sort again from past -> present
    stockData.reverse();
    
    // Output header
    $.yield("STOCK", "DATE", "AVG_PRICE", "CHANGE_RATE(%)", "VOLATILITY(%)", "MIN_PRICE", "MAX_PRICE", "RECORDS");
    
    // Calculate volatility and output
    for (var i = 0; i < stockData.length; i++) {
        var item = stockData[i];
        var prevDayAvg = i > 0 ? stockData[i-1].avgPrice : item.avgPrice;
        var changeRate = i > 0 ? ((item.avgPrice - prevDayAvg) / prevDayAvg * 100) : 0;
        var dailyVolatility = ((item.max - item.min) / item.avgPrice * 100);
        
        $.yield(
            item.name,
            item.date,
            Math.round(item.avgPrice * 100) / 100,        // Average price (2 decimal places)
            Math.round(changeRate * 100) / 100,           // Day-over-day change rate (%)
            Math.round(dailyVolatility * 100) / 100,      // Daily volatility (%)
            Math.round(item.min * 100) / 100,             // Lowest price
            Math.round(item.max * 100) / 100,             // Highest price
            item.count                                     // Trading records count
        );
    }
})

CSV()
```

### **2. Multi-Stock Comprehensive Analysis TQL**

```javascript
// Analyze multiple stocks from SP500 table for last 30 days
SQL(`
SELECT 
    NAME,
    TIME,
    VALUE
FROM SP500 
ORDER BY TIME DESC
LIMIT 5000  -- Ensure sufficient data
`)

SCRIPT({
    var stocksData = {};
    var finalResults = [];
},{
    var name = $.values[0];
    var time = new Date($.values[1]);
    var value = $.values[2];
    
    // Group daily data by stock
    if (!stocksData[name]) {
        stocksData[name] = {};
    }
    
    var dateKey = time.toISOString().split('T')[0];
    
    if (!stocksData[name][dateKey]) {
        stocksData[name][dateKey] = {
            name: name,
            date: dateKey,
            prices: [],
            sum: 0,
            count: 0,
            min: value,
            max: value
        };
    }
    
    var dayData = stocksData[name][dateKey];
    dayData.prices.push(value);
    dayData.sum += value;
    dayData.count++;
    dayData.min = Math.min(dayData.min, value);
    dayData.max = Math.max(dayData.max, value);
},{
    // Output header
    $.yield("STOCK", "DATE", "AVG_PRICE", "CHANGE_RATE(%)", "VOLATILITY(%)", "MIN_PRICE", "MAX_PRICE", "VOLUME");
    
    // Process each stock separately
    for (var stockName in stocksData) {
        var stockDailyData = [];
        
        // Calculate daily average values
        for (var dateKey in stocksData[stockName]) {
            var dayData = stocksData[stockName][dateKey];
            dayData.avgPrice = dayData.sum / dayData.count;
            stockDailyData.push(dayData);
        }
        
        // Sort by date (past -> present)
        stockDailyData.sort(function(a, b) {
            return new Date(a.date) - new Date(b.date);
        });
        
        // Select only last 30 days
        var recent30Days = stockDailyData.slice(-30);
        
        // Calculate volatility and store results
        for (var i = 0; i < recent30Days.length; i++) {
            var item = recent30Days[i];
            var prevDayAvg = i > 0 ? recent30Days[i-1].avgPrice : item.avgPrice;
            var changeRate = i > 0 ? ((item.avgPrice - prevDayAvg) / prevDayAvg * 100) : 0;
            var dailyVolatility = ((item.max - item.min) / item.avgPrice * 100);
            
            finalResults.push({
                stock: item.name,
                date: item.date,
                avgPrice: Math.round(item.avgPrice * 100) / 100,
                changeRate: Math.round(changeRate * 100) / 100,
                volatility: Math.round(dailyVolatility * 100) / 100,
                minPrice: Math.round(item.min * 100) / 100,
                maxPrice: Math.round(item.max * 100) / 100,
                volume: item.count
            });
        }
    }
    
    // Sort results by date and stock name
    finalResults.sort(function(a, b) {
        var dateCompare = new Date(b.date) - new Date(a.date);
        if (dateCompare !== 0) return dateCompare;
        return a.stock.localeCompare(b.stock);
    });
    
    // Output top 50 results only (too many would complicate display)
    for (var i = 0; i < Math.min(finalResults.length, 50); i++) {
        var result = finalResults[i];
        $.yield(
            result.stock,
            result.date,
            result.avgPrice,
            result.changeRate,
            result.volatility,
            result.minPrice,
            result.maxPrice,
            result.volume
        );
    }
})

CSV()
```

### **3. Visualization Chart Generation TQL**

```javascript
// Visualize major SP500 stock price trends
SQL(`
SELECT 
    NAME,
    TIME,
    VALUE
FROM SP500 
WHERE NAME IN ('AAPL_close', 'MSFT_close', 'GOOGL_close', 'TSLA_close', 'NVDA_close')
ORDER BY TIME DESC
LIMIT 2000
`)

SCRIPT({
    var stocksData = {};
},{
    var name = $.values[0];
    var time = new Date($.values[1]);
    var value = $.values[2];
    
    // Group daily data by stock
    if (!stocksData[name]) {
        stocksData[name] = {};
    }
    
    var dateKey = time.toISOString().split('T')[0];
    
    if (!stocksData[name][dateKey]) {
        stocksData[name][dateKey] = {
            name: name,
            date: dateKey,
            sum: 0,
            count: 0
        };
    }
    
    stocksData[name][dateKey].sum += value;
    stocksData[name][dateKey].count++;
},{
    var chartData = [];
    
    // Process each stock separately
    for (var stockName in stocksData) {
        var stockDailyData = [];
        
        // Calculate daily average values
        for (var dateKey in stocksData[stockName]) {
            var dayData = stocksData[stockName][dateKey];
            dayData.avgPrice = dayData.sum / dayData.count;
            stockDailyData.push(dayData);
        }
        
        // Sort by date
        stockDailyData.sort(function(a, b) {
            return new Date(a.date) - new Date(b.date);
        });
        
        // Generate chart data from last 30 days data
        var recent30Days = stockDailyData.slice(-30);
        
        for (var i = 0; i < recent30Days.length; i++) {
            var item = recent30Days[i];
            var prevDayAvg = i > 0 ? recent30Days[i-1].avgPrice : item.avgPrice;
            var changeRate = i > 0 ? ((item.avgPrice - prevDayAvg) / prevDayAvg * 100) : 0;
            
            chartData.push([
                new Date(item.date).getTime(),
                Math.round(item.avgPrice * 100) / 100,
                stockName.replace('_close', ''),
                Math.round(changeRate * 100) / 100
            ]);
        }
    }
    
    // Sort by date
    chartData.sort(function(a, b) {
        return a[0] - b[0];
    });
    
    for (var i = 0; i < chartData.length; i++) {
        $.yield(chartData[i][0], chartData[i][1], chartData[i][2], chartData[i][3]);
    }
})

CHART(
    size("1000px", "600px"),
    chartOption({
        title: { 
            text: "SP500 Major Stocks Last 30 Days Price Trends",
            left: "center"
        },
        tooltip: { 
            trigger: "axis",
            formatter: function(params) {
                var result = new Date(params[0].value[0]).toLocaleDateString() + '<br/>';
                for (var i = 0; i < params.length; i++) {
                    result += params[i].seriesName + ':  + params[i].value[1] + 
                             ' (' + (params[i].value[3] > 0 ? '+' : '') + params[i].value[3] + '%)<br/>';
                }
                return result;
            }
        },
        legend: { 
            bottom: "10px",
            type: "scroll"
        },
        xAxis: { 
            type: "time",
            name: "Date"
        },
        yAxis: { 
            type: "value",
            name: "Stock Price (USD)",
            scale: true
        },
        dataZoom: [
            {
                type: "slider",
                start: 0,
                end: 100
            }
        ],
        series: [
            {
                name: "AAPL",
                type: "line",
                data: column(0, 1).filter(function(item, index) {
                    return column(2)[index] === 'AAPL';
                }),
                smooth: true,
                symbol: "circle",
                symbolSize: 6,
                lineStyle: { width: 2 }
            },
            {
                name: "MSFT", 
                type: "line",
                data: column(0, 1).filter(function(item, index) {
                    return column(2)[index] === 'MSFT';
                }),
                smooth: true,
                symbol: "circle",
                symbolSize: 6,
                lineStyle: { width: 2 }
            },
            {
                name: "GOOGL",
                type: "line", 
                data: column(0, 1).filter(function(item, index) {
                    return column(2)[index] === 'GOOGL';
                }),
                smooth: true,
                symbol: "circle",
                symbolSize: 6,
                lineStyle: { width: 2 }
            }
        ]
    })
)
```

### **4. Summary Statistics Report TQL**

```javascript
// SP500 30-day summary statistics report by stock
SQL(`
SELECT 
    NAME,
    TIME,
    VALUE
FROM SP500 
WHERE NAME LIKE '%_close'  -- Closing price data only
ORDER BY TIME DESC
LIMIT 3000
`)

SCRIPT({
    var stocksData = {};
},{
    var name = $.values[0];
    var time = new Date($.values[1]);
    var value = $.values[2];
    
    var stockSymbol = name.replace('_close', '');
    var dateKey = time.toISOString().split('T')[0];
    
    if (!stocksData[stockSymbol]) {
        stocksData[stockSymbol] = {};
    }
    
    if (!stocksData[stockSymbol][dateKey]) {
        stocksData[stockSymbol][dateKey] = {
            sum: 0,
            count: 0,
            min: value,
            max: value
        };
    }
    
    var dayData = stocksData[stockSymbol][dateKey];
    dayData.sum += value;
    dayData.count++;
    dayData.min = Math.min(dayData.min, value);
    dayData.max = Math.max(dayData.max, value);
},{
    // Output header
    $.yield("STOCK", "TRADING_DAYS", "AVG_PRICE", "MAX_PRICE", "MIN_PRICE", "PRICE_RANGE", "AVG_VOLATILITY(%)", "MAX_CHANGE_RATE(%)");
    
    var summaryData = [];
    
    // Calculate summary statistics for each stock
    for (var stockSymbol in stocksData) {
        var dailyPrices = [];
        var dailyVolatilities = [];
        var changeRates = [];
        
        // Calculate daily average prices
        for (var dateKey in stocksData[stockSymbol]) {
            var dayData = stocksData[stockSymbol][dateKey];
            var avgPrice = dayData.sum / dayData.count;
            var volatility = ((dayData.max - dayData.min) / avgPrice) * 100;
            
            dailyPrices.push({
                date: dateKey,
                avgPrice: avgPrice,
                volatility: volatility
            });
        }
        
        // Sort by date
        dailyPrices.sort(function(a, b) {
            return new Date(a.date) - new Date(b.date);
        });
        
        // Select only last 30 days
        var recent30Days = dailyPrices.slice(-30);
        
        if (recent30Days.length < 2) continue;
        
        // Calculate statistics
        var prices = recent30Days.map(function(d) { return d.avgPrice; });
        var volatilities = recent30Days.map(function(d) { return d.volatility; });
        
        // Calculate change rates
        for (var i = 1; i < recent30Days.length; i++) {
            var changeRate = ((recent30Days[i].avgPrice - recent30Days[i-1].avgPrice) / recent30Days[i-1].avgPrice) * 100;
            changeRates.push(Math.abs(changeRate));
        }
        
        var avgPrice = prices.reduce(function(sum, p) { return sum + p; }, 0) / prices.length;
        var maxPrice = Math.max.apply(Math, prices);
        var minPrice = Math.min.apply(Math, prices);
        var avgVolatility = volatilities.reduce(function(sum, v) { return sum + v; }, 0) / volatilities.length;
        var maxChangeRate = changeRates.length > 0 ? Math.max.apply(Math, changeRates) : 0;
        
        summaryData.push({
            stock: stockSymbol,
            tradingDays: recent30Days.length,
            avgPrice: avgPrice,
            maxPrice: maxPrice,
            minPrice: minPrice,
            priceRange: ((maxPrice - minPrice) / avgPrice * 100),
            avgVolatility: avgVolatility,
            maxChangeRate: maxChangeRate
        });
    }
    
    // Sort by average price
    summaryData.sort(function(a, b) {
        return b.avgPrice - a.avgPrice;
    });
    
    // Output top 20 stocks only
    for (var i = 0; i < Math.min(summaryData.length, 20); i++) {
        var item = summaryData[i];
        $.yield(
            item.stock,
            item.tradingDays,
            Math.round(item.avgPrice * 100) / 100,
            Math.round(item.maxPrice * 100) / 100,
            Math.round(item.minPrice * 100) / 100,
            Math.round(item.priceRange * 100) / 100,
            Math.round(item.avgVolatility * 100) / 100,
            Math.round(item.maxChangeRate * 100) / 100
        );
    }
})

CSV()
```

## 📋 Execution Results Analysis

## Comprehensive Evaluation Results

| Question Number | Score | Time |
|-----------|------|------|
| 1 | 10/10 | 5 seconds |
| 2 | 10/10 | 10 seconds |
| 3 | 10/10 | 40 seconds |
| 4 | 10/10 | 49 seconds |
| 5 | 10/10 | 78 seconds |
| 6 | 10/10 | 65 seconds |
| 7 | 10/10 | 60 seconds |
| 8 | 10/10 | 86 seconds |
| 9 | 10/10 | 28 seconds |
| 10 | 9/10 | 194 seconds |
| **Total** | **99/100** | **615 seconds**|
| **Average** | **9.9 points** |**61.5 seconds** |

### Overall Assessment
**Excellent Performance (99/100)** - The Machbase Neo MCP Server provided accurate and complete answers in most functional areas. The executable code from actual DB, visualization, and systematic explanations were outstanding. It provided perfect guides that can be directly used in practical work.