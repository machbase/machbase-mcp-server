# Machbase Neo TQL Examples Guide (Execution Verified Edition)

## Document Structure
All examples have been tested and verified to work with actual Machbase Neo installation.

---

## 1. SRC - Data Sources (5 Examples)

### 1.1 Basic SQL Query
**Purpose**: Query specific sensor data
**Keywords**: SQL, WHERE condition

```tql
SQL(`
    SELECT time, value 
    FROM example 
    WHERE name = 'TEMP_001'
    LIMIT 5
`)
CSV()
```

### 1.2 Parameterized SQL Query  
**Purpose**: Use variables in SQL queries
**Keywords**: SQL parameters

```tql
SQL(`SELECT time, value FROM example WHERE name = ? LIMIT ?`,
    'sensor1',
    5)
CSV()
```

### 1.3 All Sensor Names Query
**Purpose**: Get list of all available sensors
**Keywords**: GROUP BY, DISTINCT

```tql
SQL(`SELECT name FROM example GROUP BY name ORDER BY name`)
CSV()
```

### 1.4 Time Range Query
**Purpose**: Query data within specific time range
**Keywords**: time filtering, ORDER BY

```tql
SQL(`
    SELECT name, time, value 
    FROM example 
    WHERE time >= 1690851600000000000
    ORDER BY time DESC 
    LIMIT 10
`)
CSV()
```

### 1.5 FAKE Data Generation
**Purpose**: Generate test data with linspace
**Keywords**: FAKE, linspace, synthetic data

```tql
FAKE(linspace(1, 100, 10))
MAPVALUE(0, 'TEST_SENSOR')
MAPVALUE(1, time('now'))
MAPVALUE(2, value(0))
CSV()
```

---

## 2. MAP - Data Processing (5 Examples)

### 2.1 Value Transformation
**Purpose**: Transform values with mathematical operations
**Keywords**: MAPVALUE, mathematical operations

```tql
FAKE(linspace(0, 10, 5))
MAPVALUE(0, value(0) * 10)
MAPVALUE(1, pow(value(0), 2))
CSV()
```

### 2.2 Data Filtering
**Purpose**: Filter data based on conditions
**Keywords**: FILTER, conditions

```tql
FAKE(linspace(1, 20, 20))
FILTER(value(0) > 10)
MAPVALUE(1, 'HIGH_VALUE')
CSV()
```

### 2.3 Data Aggregation
**Purpose**: Group data and calculate statistics
**Keywords**: GROUP, aggregation, statistics

```tql
SQL(`SELECT name, value FROM example LIMIT 10`)
GROUP(
    lazy(true),
    by(value(0), "sensor_type"),
    count(value(1), "total_count"),
    avg(value(1), "average_value")
)
CSV()
```

### 2.4 String Processing
**Purpose**: Process string data
**Keywords**: string functions, cleaning

```tql
SQL(`SELECT name, value FROM example LIMIT 5`)
MAPVALUE(0, strTrimSpace(strToUpper(value(0))))
MAPVALUE(2, strHasPrefix(value(0), 'TEMP'))
CSV()
```

### 2.5 Time-based Processing
**Purpose**: Extract time components from data
**Keywords**: time functions, temporal processing

```tql
SQL(`SELECT name, time, value FROM example LIMIT 5`)
MAPVALUE(3, strTime(value(1), sqlTimeformat('YYYY-MM-DD')))
MAPVALUE(4, strTime(value(1), sqlTimeformat('HH24')))
CSV()
```

---

## 3. SINK - Data Output (5 Examples)

### 3.1 CSV Export
**Purpose**: Export data in CSV format
**Keywords**: CSV output

```tql
SQL(`SELECT name, time, value FROM example LIMIT 5`)
CSV()
```

### 3.2 CSV with Headers
**Purpose**: Export CSV with column headers
**Keywords**: CSV headers

```tql
SQL(`
    SELECT name, COUNT(*) as record_count, AVG(value) as avg_value 
    FROM example 
    GROUP BY name 
    LIMIT 5
`)
CSV(header(true))
```

### 3.3 JSON Output
**Purpose**: Export data in JSON format  
**Keywords**: JSON output

```tql
SQL(`SELECT name, value FROM example LIMIT 3`)
JSON()
```

### 3.4 Data Insertion
**Purpose**: Insert new data into database
**Keywords**: FAKE, APPEND

```tql
FAKE(json({
    ["NEW_SENSOR_01", 1641024000000000000, 25.5],
    ["NEW_SENSOR_02", 1641024000000000000, 30.2]
}))
APPEND(table('example'))
```

### 3.5 Bulk Data Generation and Insert
**Purpose**: Generate and insert multiple data points
**Keywords**: oscillator, bulk insert

```tql
FAKE(
    oscillator(freq(1, 10), range('now', '5s', '1s'))
)
PUSHVALUE(0, 'OSCILLATOR_TEST')
APPEND(table('example'))
```

---

## 4. Chart Visualization (15 Examples)

### 4.1 Basic Bar Chart
**Purpose**: Visualize sensor data counts
**Keywords**: CHART, bar chart

```tql
SQL(`
    SELECT name, COUNT(*) as count 
    FROM example 
    GROUP BY name 
    ORDER BY count DESC 
    LIMIT 10
`)
CHART(
    chartOption({
        title: {text: "Records Count by Sensor"},
        xAxis: {
            type: "category", 
            data: column(0)
        },
        yAxis: {name: "Count"},
        series: [{
            type: "bar",
            data: column(1)
        }]
    })
)
```

### 4.2 Pie Chart Distribution
**Purpose**: Show data distribution as pie chart
**Keywords**: CHART, pie chart

```tql
SQL(`
    SELECT 
        CASE 
            WHEN value < 25 THEN 'Low'
            WHEN value < 50 THEN 'Medium'
            ELSE 'High'
        END as category,
        COUNT(*) as count
    FROM example 
    GROUP BY 
        CASE 
            WHEN value < 25 THEN 'Low'
            WHEN value < 50 THEN 'Medium'
            ELSE 'High'
        END
`)
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        title: {text: "Value Distribution"},
        dataset: [{source: column(0)}],
        series: [{
            type: "pie",
            datasetIndex: 0
        }]
    })
)
```

### 4.3 Gauge Chart
**Purpose**: Show current sensor reading
**Keywords**: CHART, gauge

```tql
SQL(`
    SELECT value 
    FROM example 
    WHERE name = 'TEMP_001' 
    ORDER BY time DESC 
    LIMIT 1
`)
CHART(
    chartOption({
        title: {text: "Current Temperature"},
        series: [{
            type: "gauge",
            min: 0,
            max: 100,
            data: [{
                value: column(0)[0],
                name: "°C"
            }]
        }]
    })
)
```

### 4.4 Line Chart Time Series
**Purpose**: Show sensor data over time
**Keywords**: CHART, line, time series

```tql
SQL(`
    SELECT time, value 
    FROM example 
    WHERE name = 'sensor1'
    ORDER BY time ASC
`)
CHART(
    chartOption({
        title: {text: "Sensor Data Over Time"},
        xAxis: {type: "time"},
        yAxis: {name: "Value"},
        series: [{
            type: "line",
            data: column(0, 1)
        }]
    })
)
```

### 4.5 3D Scatter Plot
**Purpose**: 3D visualization of mathematical function
**Keywords**: CHART, 3D, scatter

```tql
FAKE(meshgrid(linspace(-2, 2, 10), linspace(-2, 2, 10)))
MAPVALUE(2, sin(pow(value(0), 2) + pow(value(1), 2)))
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D: {},
        xAxis3D: {}, yAxis3D: {}, zAxis3D: {},
        series: [{
            type: "scatter3D",
            data: column(0)
        }]
    })
)
```

### 4.6 Scatter Chart
**Purpose**: Basic scatter plot for correlation analysis
**Keywords**: CHART, scatter, correlation

```tql
FAKE(linspace(0, 360, 100))
MAPVALUE(1, sin((value(0)/180)*PI))
CHART(
    chartOption({
        title: {text: "Sine Wave Scatter Plot"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [{
            type: "scatter", 
            data: column(1)
        }]
    })
)
```

### 4.7 Heatmap Visualization
**Purpose**: 2D data density visualization
**Keywords**: CHART, heatmap, density

```tql
FAKE(json({
    [0, 0, 5], [1, 0, 8], [2, 0, 3],
    [0, 1, 2], [1, 1, 9], [2, 1, 6], 
    [0, 2, 4], [1, 2, 7], [2, 2, 1]
}))
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    chartOption({
        title: {text: "Simple Heatmap"},
        xAxis: {type: "category", data: [0, 1, 2]},
        yAxis: {type: "category", data: [0, 1, 2]},
        visualMap: {
            min: 0,
            max: 10,
            calculable: true
        },
        series: [{
            type: "heatmap",
            data: column(0),
            label: {show: true}
        }]
    })
)
```

### 4.8 Area Chart
**Purpose**: Area chart for filled time series
**Keywords**: CHART, area, filled

```tql
FAKE(linspace(0, 20, 20))
MAPVALUE(1, sin(value(0)) + random() * 0.3)
CHART(
    chartOption({
        title: {text: "Area Chart Example"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [{
            type: "line",
            areaStyle: {},
            data: column(1)
        }]
    })
)
```

### 4.9 Stacked Bar Chart
**Purpose**: Multiple series stacked bar chart
**Keywords**: CHART, stacked bar, multiple series

```tql
FAKE(json({
    ["Jan", 120, 132, 101],
    ["Feb", 220, 182, 191], 
    ["Mar", 150, 232, 210],
    ["Apr", 820, 932, 934],
    ["May", 180, 267, 290]
}))
CHART(
    chartOption({
        title: {text: "Monthly Data Comparison"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [
            {name: "Series A", type: "bar", stack: "total", data: column(1)},
            {name: "Series B", type: "bar", stack: "total", data: column(2)},
            {name: "Series C", type: "bar", stack: "total", data: column(3)}
        ]
    })
)
```

### 4.10 Radar Chart
**Purpose**: Multi-dimensional data comparison
**Keywords**: CHART, radar, multi-dimensional

```tql
FAKE(json({
    ["Performance", 80, 90],
    ["Reliability", 70, 85],
    ["Efficiency", 90, 75], 
    ["Scalability", 85, 80],
    ["Security", 75, 95]
}))
CHART(
    chartOption({
        title: {text: "System Metrics Comparison"},
        radar: {
            indicator: [
                {name: "Performance", max: 100},
                {name: "Reliability", max: 100},
                {name: "Efficiency", max: 100},
                {name: "Scalability", max: 100},
                {name: "Security", max: 100}
            ]
        },
        series: [{
            type: "radar",
            data: [
                {value: column(1), name: "System A"},
                {value: column(2), name: "System B"}
            ]
        }]
    })
)
```

### 4.11 Candlestick Chart
**Purpose**: Financial OHLC data visualization
**Keywords**: CHART, candlestick, financial

```tql
FAKE(json({
    ["2024-01-01", 20, 34, 10, 25],
    ["2024-01-02", 25, 37, 20, 30],
    ["2024-01-03", 30, 42, 25, 35],
    ["2024-01-04", 35, 45, 30, 40],
    ["2024-01-05", 40, 48, 35, 42]
}))
MAPVALUE(1, list(value(1), value(2), value(3), value(4)))
POPVALUE(2, 3, 4)
CHART(
    chartOption({
        title: {text: "Stock Price Movement"},
        xAxis: {type: "category", data: column(0)},
        yAxis: {scale: true},
        series: [{
            type: "candlestick",
            data: column(1)
        }]
    })
)
```

### 4.12 Donut Chart
**Purpose**: Donut-style pie chart with inner radius
**Keywords**: CHART, donut, pie variant

```tql
SQL(`
    SELECT name, COUNT(*) as count 
    FROM example 
    GROUP BY name 
    LIMIT 6
`)
MAPVALUE(0, list(value(0), value(1)))
CHART(
    chartOption({
        title: {text: "Sensor Distribution"},
        dataset: [{source: column(0)}],
        series: [{
            type: "pie",
            radius: ["40%", "70%"],
            datasetIndex: 0,
            label: {
                show: false
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: "20"
                }
            }
        }]
    })
)
```

### 4.13 Mixed Chart (Line + Bar)
**Purpose**: Combine different chart types
**Keywords**: CHART, mixed, line and bar

```tql
FAKE(json({
    ["Jan", 150, 120],
    ["Feb", 230, 132],
    ["Mar", 224, 101],
    ["Apr", 218, 134],
    ["May", 135, 90]
}))
CHART(
    chartOption({
        title: {text: "Revenue vs Profit"},
        xAxis: {data: column(0)},
        yAxis: [{type: "value"}, {type: "value"}],
        series: [
            {name: "Revenue", type: "bar", data: column(1)},
            {name: "Profit", type: "line", yAxisIndex: 1, data: column(2)}
        ]
    })
)
```

### 4.14 Liquid Fill Gauge
**Purpose**: Percentage display with liquid effect
**Keywords**: CHART, liquidFill, percentage

```tql
FAKE(json({
    [0.6, 0.7, 0.8]
}))
CHART(
    plugins("liquidfill"),
    chartOption({
        title: {text: "System Usage"},
        series: [{
            type: "liquidFill",
            data: column(0),
            color: ['#294D99', '#156ACF', '#1598ED']
        }]
    })
)
```

### 4.15 Funnel Chart
**Purpose**: Show data flow through stages
**Keywords**: CHART, funnel, conversion

```tql
FAKE(json({
    ["Visits", 100],
    ["Views", 80], 
    ["Clicks", 60],
    ["Purchases", 40],
    ["Returns", 20]
}))
MAPVALUE(0, dict("name", value(0), "value", value(1)))
CHART(
    chartOption({
        title: {text: "Conversion Funnel"},
        series: [{
            type: "funnel",
            left: "10%",
            width: "80%",
            data: column(0)
        }]
    })
)
```

---

## 5. Advanced Features (15 Examples)

### 5.1 Signal Analysis with FFT
**Purpose**: Frequency analysis of oscillating data
**Keywords**: FFT, GROUPBYKEY, frequency analysis

```tql
FAKE(
    oscillator(freq(5, 1.0), freq(10, 0.5), range('now', '2s', '10ms'))
)
MAPKEY('signal')
GROUPBYKEY()
FFT()
CHART(
    chartOption({
        title: {text: "Frequency Analysis"},
        xAxis: {name: "Hz"},
        yAxis: {name: "Amplitude"},
        series: [{
            type: "line",
            data: column(0, 1)
        }]
    })
)
```

### 5.2 Geographic Data Visualization
**Purpose**: Display sensor locations on map
**Keywords**: GEOMAP, coordinates, marker

```tql
FAKE(json({
    ["Seoul_Station", 37.5665, 126.9780, 23.5],
    ["Busan_Port", 35.1796, 129.0756, 25.2]
}))
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
                content: '<b>' + name + '</b><br/>Temp: ' + temp + '°C'
            }
        }
    });
})
GEOMAP()
```

### 5.3 Moving Average Filter
**Purpose**: Apply smoothing filter to noisy data
**Keywords**: MAP_MOVAVG, signal filtering

```tql
FAKE(linspace(1, 10, 10))
MAPVALUE(1, sin(value(0)) + random() * 0.2)
MAP_MOVAVG(2, value(1), 3)
CHART(
    chartOption({
        title: {text: "Simple Moving Average"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [
            {name: "Original", type: "line", data: column(1)},
            {name: "Smoothed", type: "line", data: column(2)}
        ]
    })
)
```

### 5.4 Statistical Analysis
**Purpose**: Calculate comprehensive statistics
**Keywords**: statistical functions, analysis

```tql
SQL(`
    SELECT name,
           COUNT(*) as total_records,
           AVG(value) as avg_value,
           MIN(value) as min_value,
           MAX(value) as max_value,
           MAX(value) - MIN(value) as value_range
    FROM example 
    GROUP BY name
    ORDER BY total_records DESC
    LIMIT 10
`)
CSV(header(true))
```

### 5.5 Data Quality Assessment
**Purpose**: Assess data completeness and validity
**Keywords**: data quality, validation

```tql
SQL(`
    SELECT name,
           COUNT(*) as total_records,
           COUNT(value) as valid_values,
           COUNT(*) - COUNT(value) as null_values
    FROM example 
    GROUP BY name
`)
SET(quality, value(3) == 0 ? 'COMPLETE' : 'INCOMPLETE')
SET(completeness, value(2) * 100.0 / value(1))
MAPVALUE(4, $quality)
MAPVALUE(5, round($completeness * 100) / 100)
CSV(header(true))
```

### 5.6 Geographic Heat Zones
**Purpose**: Visualize data intensity with geographic circles
**Keywords**: GEOMAP, circle, heat zones, conditional colors

```tql
FAKE(json({
    [37.5665, 126.9780, "Seoul", 150],
    [35.1796, 129.0756, "Busan", 80],
    [37.4563, 126.7052, "Incheon", 60],
    [35.8714, 128.6014, "Daegu", 90],
    [36.3504, 127.3845, "Daejeon", 70]
}))
SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    var city = $.values[2];
    var value = $.values[3];
    var radius = value / 2;
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties: {
            radius: radius,
            fillOpacity: 0.6,
            color: value > 100 ? "#ff0000" : value > 50 ? "#ffaa00" : "#00ff00",
            popup: {
                content: '<b>' + city + '</b><br/>Value: ' + value
            }
        }
    });
})
GEOMAP()
```

### 5.7 GPS Tracking Path
**Purpose**: Display movement trajectory on map
**Keywords**: GEOMAP, polyline, GPS tracking, path

```tql
FAKE(json({
    [37.5665, 126.9780],
    [37.5660, 126.9785],
    [37.5670, 126.9790],
    [37.5680, 126.9800],
    [37.5690, 126.9810]
}))
SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            coordinates: points,
            properties: {
                color: "#ff0000",
                weight: 3,
                opacity: 0.8
            }
        });
    }
}, {
    var lat = $.values[0];
    var lon = $.values[1];
    points.push([lat, lon]);
})
GEOMAP()
```

### 5.8 Geographic Area Boundaries
**Purpose**: Define geographic regions and boundaries
**Keywords**: GEOMAP, polygon, area boundaries, regions

```tql
SCRIPT({
    $.yield({
        type: "polygon",
        coordinates: [
            [37.5, 126.8],
            [37.6, 126.8], 
            [37.6, 127.0],
            [37.5, 127.0],
            [37.5, 126.8]
        ],
        properties: {
            fillColor: "#00ff00",
            fillOpacity: 0.3,
            color: "#0000ff",
            weight: 2,
            popup: {
                content: "<b>Seoul Area</b><br/>Protected Zone"
            }
        }
    });
})
GEOMAP()
```

### 5.9 Multi-layer Geographic Visualization
**Purpose**: Combine multiple geographic elements
**Keywords**: GEOMAP, multi-layer, complex visualization

```tql
SCRIPT({
    // Area boundary
    $.yield({
        type: "polygon",
        coordinates: [
            [37.4, 126.7],
            [37.7, 126.7],
            [37.7, 127.1], 
            [37.4, 127.1],
            [37.4, 126.7]
        ],
        properties: {
            fillColor: "#e6f3ff",
            fillOpacity: 0.2,
            color: "#0066cc",
            weight: 1
        }
    });
    
    // Central marker
    $.yield({
        type: "marker",
        coordinates: [37.5665, 126.9780],
        properties: {
            popup: {content: "<b>Seoul Station</b>"}
        }
    });
    
    // Coverage circle
    $.yield({
        type: "circle",
        coordinates: [37.5665, 126.9780],
        properties: {
            radius: 1000,
            fillOpacity: 0.1,
            color: "#ff6600"
        }
    });
})
GEOMAP()
```

### 5.10 Kalman Filter Implementation
**Purpose**: Advanced signal estimation with Kalman filtering
**Keywords**: MAP_KALMAN, optimal estimation, noise reduction

```tql
FAKE(arrange(0, 5, 0.1))
SET(true_value, 25.0 + sin(value(0)))
SET(measurement_noise, (random() - 0.5) * 3)
SET(measurement, $true_value + $measurement_noise)
MAPVALUE(1, $true_value)
MAPVALUE(2, $measurement)
MAP_KALMAN(3, $measurement, model(0.1, 0.01, 1.0))
CHART(
    chartOption({
        title: {text: "Kalman Filter Estimation"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [
            {name: "True Signal", type: "line", data: column(1)},
            {name: "Noisy Measurement", type: "scatter", data: column(2)},
            {name: "Kalman Estimate", type: "line", data: column(3)}
        ]
    })
)
```

### 5.11 Interactive Tooltip Maps
**Purpose**: Rich interactive tooltips on geographic data
**Keywords**: GEOMAP, tooltip, interactive, rich content

```tql
FAKE(json({
    ["Sensor_A", 37.5665, 126.9780, 23.5, 65.2, "OK"],
    ["Sensor_B", 35.1796, 129.0756, 25.8, 58.7, "WARNING"],
    ["Sensor_C", 37.4563, 126.7052, 21.2, 72.1, "OK"]
}))
SCRIPT({
    var name = $.values[0];
    var lat = $.values[1];
    var lon = $.values[2]; 
    var temp = $.values[3];
    var humidity = $.values[4];
    var status = $.values[5];
    
    var color = status === "OK" ? "#00ff00" : 
                status === "WARNING" ? "#ffaa00" : "#ff0000";
    
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties: {
            radius: 8,
            fillColor: color,
            color: "#000000",
            weight: 1,
            fillOpacity: 0.8,
            tooltip: {
                content: '<div style="padding:5px;">' +
                        '<b>' + name + '</b><br/>' +
                        'Temperature: ' + temp + '°C<br/>' +
                        'Humidity: ' + humidity + '%<br/>' +
                        'Status: <span style="color:' + color + '">' + status + '</span>' +
                        '</div>',
                permanent: true
            }
        }
    });
})
GEOMAP()
```

### 5.12 Time-based Map Animation Data
**Purpose**: Generate time-series data for animated maps
**Keywords**: GEOMAP, time-series, animation data, temporal

```tql
FAKE(linspace(0, 10, 11))
SCRIPT({
    var time_step = $.values[0];
    var base_lat = 37.5665;
    var base_lon = 126.9780;
    
    // Simulate movement over time
    var lat = base_lat + Math.sin(time_step * 0.5) * 0.01;
    var lon = base_lon + Math.cos(time_step * 0.5) * 0.01;
    var intensity = Math.abs(Math.sin(time_step)) * 100;
    
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties: {
            radius: intensity / 10 + 3,
            fillColor: intensity > 50 ? "#ff4444" : "#44ff44",
            fillOpacity: 0.7,
            popup: {
                content: 'Time: ' + time_step.toFixed(1) + '<br/>Intensity: ' + intensity.toFixed(0)
            }
        }
    });
})
GEOMAP()
```

### 5.13 Custom JavaScript Data Processing
**Purpose**: Advanced data manipulation with custom logic
**Keywords**: SCRIPT, JavaScript, custom processing, complex logic

```tql
SQL(`SELECT name, value FROM example LIMIT 10`)
SCRIPT({
    var stats = {
        total: 0,
        count: 0,
        categories: {}
    };
    
    function finalize() {
        var avg = stats.total / stats.count;
        Object.keys(stats.categories).forEach(function(category) {
            var count = stats.categories[category];
            var percentage = (count / stats.count * 100).toFixed(1);
            $.yield(category, count, percentage, avg.toFixed(2));
        });
    }
}, {
    var name = $.values[0];
    var value = $.values[1];
    
    stats.total += value;
    stats.count++;
    
    // Categorize sensors
    var category = name.startsWith('TEMP') ? 'Temperature' :
                  name.startsWith('HUMID') ? 'Humidity' : 
                  name.startsWith('PRESSURE') ? 'Pressure' : 'Other';
    
    stats.categories[category] = (stats.categories[category] || 0) + 1;
})
CSV(header(true))
```

### 5.14 Low Pass Filter with Visualization
**Purpose**: Apply and visualize low pass filtering
**Keywords**: MAP_LOWPASS, signal processing, filter comparison

```tql
FAKE(linspace(0, 4 * PI, 100))
SET(original, sin(value(0)) + 0.5 * sin(5 * value(0)) + 0.3 * (random() - 0.5))
MAPVALUE(1, $original)
MAP_LOWPASS(2, $original, 0.1)
MAP_LOWPASS(3, $original, 0.3)
CHART(
    chartOption({
        title: {text: "Low Pass Filter Comparison"},
        xAxis: {data: column(0)},
        yAxis: {},
        series: [
            {name: "Original", type: "line", data: column(1), opacity: 0.6},
            {name: "Alpha=0.1", type: "line", data: column(2)},
            {name: "Alpha=0.3", type: "line", data: column(3)}
        ]
    })
)
```

### 5.15 Geographic Sensor Network Monitoring
**Purpose**: Real-time monitoring of geographic sensor network
**Keywords**: GEOMAP, sensor network, real-time, monitoring

```tql
SQL(`
    SELECT name, 
           37.5 as lat,
           126.9 as lon,
           AVG(value) as avg_value,
           COUNT(*) as data_points
    FROM example 
    GROUP BY name 
    HAVING COUNT(*) > 1
    LIMIT 5
`)
SCRIPT({
    var name = $.values[0];
    var lat = $.values[1] + (Math.random() - 0.5) * 0.1; // Add variation
    var lon = $.values[2] + (Math.random() - 0.5) * 0.1;
    var value = $.values[3];
    var points = $.values[4];
    
    var status = points > 2 ? "ACTIVE" : "LOW";
    var health = value > 0 && value < 100 ? "GOOD" : "CHECK";
    
    var color = status === "ACTIVE" && health === "GOOD" ? "#00ff00" :
                status === "ACTIVE" ? "#ffaa00" : "#ff0000";
    
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>' + name + '</b><br/>' +
                        'Value: ' + value.toFixed(1) + '<br/>' +
                        'Points: ' + points + '<br/>' +
                        'Status: ' + status
            }
        }
    });
})
GEOMAP()
```