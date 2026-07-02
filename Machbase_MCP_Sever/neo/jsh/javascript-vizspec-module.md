# Machbase Neo JavaScript VizSpec Module

The `vizspec` module implements ADVN (Analysis Data Visualization Notation), a declarative specification for describing time-series visualizations.

```js
const viz = require('@jsh/vizspec');
```

## Constants

### RepresentationKind

| Constant | Value | Description |
|:---------|:------|:------------|
| `viz.LINE` | `"line"` | Line chart |
| `viz.BAR` | `"bar"` | Bar chart |
| `viz.SCATTER` | `"scatter"` | Scatter plot |
| `viz.AREA` | `"area"` | Area chart |
| `viz.HEATMAP` | `"heatmap"` | Heatmap |
| `viz.HISTOGRAM` | `"histogram"` | Histogram |
| `viz.PIE` | `"pie"` | Pie chart |

### AnnotationKind

| Constant | Value | Description |
|:---------|:------|:------------|
| `viz.THRESHOLD_LINE` | `"thresholdLine"` | Horizontal threshold line |
| `viz.BAND` | `"band"` | Shaded band region |
| `viz.REGION` | `"region"` | Time-range highlight |
| `viz.MARKER` | `"marker"` | Point marker |
| `viz.REFERENCE_LINE` | `"referenceLine"` | Vertical reference line |

### Timeformat

| Constant | Value | Description |
|:---------|:------|:------------|
| `viz.RFC3339` | `"2006-01-02T15:04:05Z07:00"` | RFC 3339 format |
| `viz.RFC3339Nano` | `"2006-01-02T15:04:05.999999999Z07:00"` | RFC 3339 with nanoseconds |
| `viz.Kitchen` | `"3:04PM"` | Kitchen time format |
| `viz.DateTime` | `"2006-01-02 15:04:05"` | Standard datetime |
| `viz.DateOnly` | `"2006-01-02"` | Date only |
| `viz.TimeOnly` | `"15:04:05"` | Time only |

## Core Functions

### parse(jsonString)

Parses a JSON string into a VizSpec object.

```js
const spec = viz.parse(jsonString);
```

### stringify(spec)

Serializes a VizSpec object to a JSON string.

```js
const json = viz.stringify(spec);
```

### validate(spec)

Validates a VizSpec object and returns an array of validation errors. Returns an empty array if valid.

```js
const errors = viz.validate(spec);
if (errors.length > 0) {
    console.log('Validation errors:', errors);
}
```

### normalize(spec)

Normalizes a VizSpec object by filling in default values and resolving shorthand notations.

```js
const normalized = viz.normalize(spec);
```

### createSpec([options])

Creates a new empty VizSpec object with optional initial configuration.

```js
const spec = viz.createSpec({
    title: 'Temperature Monitor',
    timeRange: { last: '1h' }
});
```

### listSeries(spec)

Lists all series defined in the spec with summary information.

| Field | Type | Description |
|:------|:-----|:------------|
| `name` | String | Series name |
| `kind` | String | Representation kind |
| `source` | String | Data source identifier |
| `yAxis` | Number | Y-axis index (0 or 1) |

## Series Helpers

Series helpers create pre-configured series objects for common chart types.

### Common Initializer Fields

| Field | Type | Description |
|:------|:-----|:------------|
| `name` | String | Series display name |
| `source` | String | Data source identifier |
| `color` | String | Series color |
| `yAxisIndex` | Number | Y-axis index (0 or 1) |
| `opacity` | Number | Fill/line opacity (0-1) |

### viz.lineSeries(options)

Creates a line series.

```js
viz.lineSeries({ name: 'Temperature', source: 'sensor/temp', color: '#ff0000' })
```

### viz.barSeries(options)

Creates a bar series.

### viz.scatterSeries(options)

Creates a scatter series.

### viz.areaSeries(options)

Creates an area series.

### viz.heatmapSeries(options)

Creates a heatmap series.

### viz.histogramSeries(options)

Creates a histogram series.

### viz.pieSeries(options)

Creates a pie series.

## Annotation Helpers

Annotation helpers create overlay annotations for charts.

### Common Fields

| Field | Type | Description |
|:------|:-----|:------------|
| `label` | String | Annotation label text |
| `color` | String | Annotation color |
| `opacity` | Number | Opacity (0-1) |

### viz.thresholdLine(options)

Creates a horizontal threshold line annotation.

```js
viz.thresholdLine({ value: 80, label: 'Warning', color: 'red' })
```

### viz.band(options)

Creates a shaded band annotation between two values.

```js
viz.band({ from: 60, to: 80, label: 'Normal Range', color: 'green', opacity: 0.2 })
```

### viz.region(options)

Creates a time-range highlight annotation.

### viz.marker(options)

Creates a point marker annotation.

### viz.referenceLine(options)

Creates a vertical reference line annotation.

## Builder

The Builder class provides a fluent API for constructing VizSpec objects.

```js
const builder = new viz.Builder();
```

### Methods

| Method | Description |
|:-------|:------------|
| `title(text)` | Sets the chart title |
| `subtitle(text)` | Sets the chart subtitle |
| `timeRange(range)` | Sets the time range (`{ last: '1h' }` or `{ from, to }`) |
| `timezone(tz)` | Sets the timezone |
| `addSeries(series)` | Adds a series to the spec |
| `addAnnotation(annotation)` | Adds an annotation |
| `yAxis(index, options)` | Configures a Y-axis |
| `xAxis(options)` | Configures the X-axis |
| `legend(options)` | Configures the legend |
| `grid(options)` | Configures the grid layout |
| `tooltip(options)` | Configures tooltips |
| `theme(name)` | Sets the theme |
| `build()` | Returns the constructed VizSpec object |

### Example

```js
const spec = new viz.Builder()
    .title('Sensor Dashboard')
    .timeRange({ last: '24h' })
    .timezone('Asia/Seoul')
    .addSeries(viz.lineSeries({
        name: 'Temperature',
        source: 'sensor/temp',
        color: '#ff6b6b'
    }))
    .addSeries(viz.lineSeries({
        name: 'Humidity',
        source: 'sensor/humidity',
        color: '#4ecdc4',
        yAxisIndex: 1
    }))
    .addAnnotation(viz.thresholdLine({
        value: 35,
        label: 'High Temp',
        color: 'red'
    }))
    .yAxis(0, { label: 'Temperature (C)', min: 0, max: 50 })
    .yAxis(1, { label: 'Humidity (%)', min: 0, max: 100 })
    .build();
```

## Output Adapters

### toEChartsOption(spec[, data])

Converts a VizSpec to an Apache ECharts option object.

```js
const option = viz.toEChartsOption(spec, data);
// Use with CHART() in TQL or pass to ECharts instance
```

### toTUILines(spec, data[, options])

Renders the visualization as TUI (Text User Interface) line chart for terminal output.

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `width` | Number | 80 | Terminal width in characters |
| `height` | Number | 24 | Terminal height in lines |
| `color` | Boolean | true | Whether to use ANSI colors |

```js
const output = viz.toTUILines(spec, data, { width: 120, height: 30 });
console.log(output);
```

### toTUIBlocks(spec, data[, options])

Renders the visualization as TUI block chart using Unicode block characters.

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `width` | Number | 80 | Terminal width in characters |
| `height` | Number | 24 | Terminal height in lines |
| `color` | Boolean | true | Whether to use ANSI colors |

**Return value**

| Field | Type | Description |
|:------|:-----|:------------|
| `text` | String | Rendered chart text |
| `lines` | Array | Array of individual lines |
| `width` | Number | Actual rendered width |
| `height` | Number | Actual rendered height |

### toSVG(spec, data[, options])

Renders the visualization as an SVG string.

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `width` | Number | 800 | SVG width in pixels |
| `height` | Number | 400 | SVG height in pixels |
| `font` | String | `"sans-serif"` | Font family |

```js
const svg = viz.toSVG(spec, data, { width: 1200, height: 600 });
```

### toPNG(spec, data[, options])

Renders the visualization as a PNG image buffer.

| Option | Type | Default | Description |
|:-------|:-----|:--------|:------------|
| `width` | Number | 800 | Image width in pixels |
| `height` | Number | 400 | Image height in pixels |
| `font` | String | `"sans-serif"` | Font family |
| `dpi` | Number | 96 | Image DPI |
| `background` | String | `"#ffffff"` | Background color |

```js
const pngBuffer = viz.toPNG(spec, data, { width: 1200, height: 600, dpi: 144 });
```

## Time Handling

VizSpec uses nanosecond-precision Unix timestamps internally, consistent with Machbase's time representation. When specifying time ranges:

- Relative: `{ last: '1h' }`, `{ last: '30m' }`, `{ last: '7d' }`
- Absolute: `{ from: timestamp, to: timestamp }`

Supported duration units: `s` (seconds), `m` (minutes), `h` (hours), `d` (days), `w` (weeks).

## Time Rendering

Output adapters handle time formatting automatically based on the configured timezone and time format. The `Timeformat` constants provide standard format strings compatible with Go's time formatting conventions.

## Using viz Command

The `viz` command-line tool can render VizSpec files directly:

```sh
viz render spec.json --format svg --output chart.svg
viz render spec.json --format png --output chart.png
viz render spec.json --format tui
viz validate spec.json
```
