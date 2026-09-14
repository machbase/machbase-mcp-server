# Machbase Neo JavaScript VizSpec Module

`vizspec` 모듈은 ADVN 문서를 생성하고, 검증하고, 파싱하고, 다른 출력 형식으로 변환하는 JSH API입니다. ADVN은 Analysis Data Visualization Notation의 약자로, 분석 결과 시각화를 위한 렌더러 중립 문서 형식입니다. (Machbase Neo 8.0.75부터)

```js
const vizspec = require('vizspec');
```

- ADVN은 의미 중심의 semantic layer입니다. 분석 결과가 무엇을 의미하는지 표현하는 문서 형식입니다.
- `vizspec` 모듈은 ADVN 문서를 생성하고 변환하는 JSH API입니다.
- `viz`는 ADVN 문서를 검증하고 미리 보고 내보내는 명령어입니다.

## 기본 예제

```js
const vizspec = require('vizspec');

const spec = new vizspec.Builder()
    .setDomain({
        kind: 'time',
        timeformat: vizspec.Timeformat.ns,
    })
    .setXAxis({ id: 'time', type: 'time', label: 'Time' })
    .addYAxis({ id: 'value', type: 'linear', label: 'Value' })
    .addTimeBucketValueSeries({
        id: 'series-1',
        axis: 'value',
        data: [
            ['1712102400000000000', 10],
            ['1712102460000000000', 12],
        ],
    })
    .build();
```

## 상수

모듈은 다음 상수 그룹을 제공합니다. 애플리케이션 코드에서 ADVN 값을 명시적으로 지정할 때 이 상수들을 사용하면 오타를 줄일 수 있습니다.

### RepresentationKind

| 상수 | 값 | 설명 |
| --- | --- | --- |
| `RepresentationKind.rawPoint` | `raw-point` | `[x, y]` 형태의 raw point 샘플입니다. |
| `RepresentationKind.timeBucketValue` | `time-bucket-value` | 단일 numeric value를 가진 time bucket 집계 표현입니다. |
| `RepresentationKind.timeBucketBand` | `time-bucket-band` | `min/max/avg` band 값을 가진 time bucket 집계 표현입니다. |
| `RepresentationKind.distributionHistogram` | `distribution-histogram` | Histogram distribution bucket 표현입니다. |
| `RepresentationKind.distributionBoxplot` | `distribution-boxplot` | Boxplot distribution group 표현입니다. |
| `RepresentationKind.eventPoint` | `event-point` | 하나의 time/value 지점에 발생한 instant event 표현입니다. |
| `RepresentationKind.eventRange` | `event-range` | `from/to` 시간 범위를 가진 duration event 표현입니다. |

### AnnotationKind

| 상수 | 값 | 설명 |
| --- | --- | --- |
| `AnnotationKind.point` | `point` | 하나의 위치를 가리키는 point annotation입니다. |
| `AnnotationKind.line` | `line` | threshold 또는 reference line annotation입니다. |
| `AnnotationKind.range` | `range` | 범위를 강조하는 range annotation입니다. |

### Timeformat

| 상수 | 값 | 설명 |
| --- | --- | --- |
| `Timeformat.rfc3339` | `rfc3339` | RFC3339 문자열 시간 표현입니다. |
| `Timeformat.s` | `s` | epoch seconds입니다. |
| `Timeformat.ms` | `ms` | epoch milliseconds입니다. |
| `Timeformat.us` | `us` | epoch microseconds입니다. |
| `Timeformat.ns` | `ns` | epoch nanoseconds입니다. |

## parse()

ADVN JSON 문자열을 파싱해서 정규화된 spec 객체를 반환합니다.

<h6>문법</h6>

```js
parse(text)
```

<h6>사용 예제</h6>

```js
const vizspec = require('vizspec');
const spec = vizspec.parse('{"version":1,"series":[]}');
console.println(spec.version);
```

## stringify()

spec 객체를 ADVN JSON 문자열로 직렬화합니다.

<h6>문법</h6>

```js
stringify(spec)
```

## validate()

spec 객체를 검증합니다. 구조나 필드 조합이 잘못되면 예외를 발생시킵니다.

<h6>문법</h6>

```js
validate(spec)
```

## normalize()

부분적으로 작성된 spec 객체를 정규화하고 기본 구조 필드를 채웁니다.

<h6>문법</h6>

```js
normalize(spec)
```

## createSpec()

initializer로부터 spec 객체를 생성하고, 정규화하고, 검증합니다.

<h6>문법</h6>

```js
createSpec(init)
```

<h6>사용 예제</h6>

```js
const vizspec = require('vizspec');
const spec = vizspec.createSpec({
    domain: { kind: 'time', timeformat: vizspec.Timeformat.ns },
    series: [],
});
console.println(spec.domain.kind);
```

## listSeries()

`spec.series`의 정규화된 요약 목록을 반환합니다.

<h6>문법</h6>

```js
listSeries(spec)
```

<h6>반환 필드</h6>

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `index` | integer | `spec.series` 안의 0-based series index입니다. |
| `id` | string | Series id입니다. |
| `name` | string | 지정된 경우 series name입니다. |
| `title` | string | 표시 제목입니다. `name`이 있으면 `name`, 없으면 `id`를 사용합니다. |
| `kind` | string | Representation kind입니다. |
| `tuiLinesCompatible` | boolean | `toTUILines()`로 렌더링 가능한 series인지 여부입니다. |

## Series helper

Series helper 함수는 올바른 representation kind와 기본 필드 구성을 가진 series 객체를 만듭니다.

사용 가능한 helper:

- `rawPointSeries(init)`
- `timeBucketValueSeries(init)`
- `timeBucketBandSeries(init)`
- `distributionHistogramSeries(init)`
- `distributionBoxplotSeries(init)`
- `eventPointSeries(init)`
- `eventRangeSeries(init)`

<h6>공통 initializer 필드</h6>

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `id` | string | Series 식별자입니다. |
| `name` | string | Adapter에서 사용할 표시 이름입니다. |
| `axis` | string | Numeric renderer에서 사용할 y-axis id입니다. |
| `representation` | object | field 또는 representation 메타데이터 override에 사용합니다. |
| `data` | array | Series payload row 배열입니다. |
| `style` | object | color, opacity 같은 renderer hint style 값입니다. |
| `quality` | object | coverage, rowCount 같은 quality 메타데이터입니다. |
| `source` | object | Series provenance 메타데이터입니다. |
| `extra` | object | boxplot outlier 같은 representation-specific extra 데이터입니다. |

<h6>사용 예제</h6>

```js
const vizspec = require('vizspec');
const series = vizspec.timeBucketValueSeries({
    id: 'cpu',
    axis: 'value',
    data: [['1712102400000000000', 10]],
});
console.println(series.representation.kind);
```

## Annotation helper

Annotation helper 함수는 올바른 annotation kind를 가진 top-level annotation 객체를 만듭니다.

사용 가능한 helper:

- `pointAnnotation(init)`
- `lineAnnotation(init)`
- `rangeAnnotation(init)`

<h6>공통 initializer 필드</h6>

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `axis` | string | 대상 axis id입니다. |
| `label` | string | 사람이 읽을 annotation label입니다. |
| `value` | any | line 또는 point annotation에 사용할 값입니다. |
| `at` | any | point annotation 위치값입니다. |
| `from` | any | range 시작값입니다. |
| `to` | any | range 종료값입니다. |
| `style` | object | 선택적인 renderer hint style 값입니다. |

<h6>사용 예제</h6>

```js
const annotation = vizspec.lineAnnotation({ axis: 'value', value: 80, label: 'warning' });
console.println(annotation.kind);
```

## Builder

fluent 방식으로 ADVN 문서를 만들 때 사용합니다.

<h6>문법</h6>

```js
new Builder([init])
```

<h6>주요 메서드</h6>

| 메서드 | 설명 |
| --- | --- |
| `setDomain(definition)` | `spec.domain`을 설정합니다. |
| `setXAxis(definition)` | `spec.axes.x`를 설정합니다. |
| `addYAxis(definition)` | y-axis 정의를 하나 추가합니다. |
| `addRawPointSeries(definition)` | `raw-point` series를 추가합니다. |
| `addTimeBucketValueSeries(definition)` | `time-bucket-value` series를 추가합니다. |
| `addTimeBucketBandSeries(definition)` | `time-bucket-band` series를 추가합니다. |
| `addDistributionHistogramSeries(definition)` | histogram series를 추가합니다. |
| `addDistributionBoxplotSeries(definition)` | boxplot series를 추가합니다. |
| `addEventPointSeries(definition)` | event-point series를 추가합니다. |
| `addEventRangeSeries(definition)` | event-range series를 추가합니다. |
| `addAnnotation(definition)` | annotation 객체를 추가합니다. |
| `addLineAnnotation(definition)` | line annotation을 추가합니다. |
| `addRangeAnnotation(definition)` | range annotation을 추가합니다. |
| `setView(definition)` | `spec.view`를 설정합니다. |
| `setMeta(definition)` | `spec.meta`를 설정합니다. |
| `build()` | 정규화된 spec을 반환합니다. |
| `stringify()` | build 결과를 문자열로 직렬화합니다. |
| `listSeries()` | 정규화된 series 요약 목록을 반환합니다. |
| `toEChartsOption(options)` | build 결과를 ECharts option으로 변환합니다. |
| `toTUILines(options)` | build 결과를 터미널 친화적인 TUI chart line 배열로 변환합니다. |
| `toTUIBlocks(options)` | build 결과를 TUI block 배열로 변환합니다. |
| `toSVG(options)` | build 결과를 SVG 문자열로 변환합니다. |
| `toPNG([svgOptions[, pngOptions]])` | build 결과를 PNG 바이너리 데이터로 변환합니다. |

<h6>사용 예제</h6>

```js
const vizspec = require('vizspec');

const spec = new vizspec.Builder()
    .setDomain({ kind: 'time', timeformat: vizspec.Timeformat.ns })
    .setXAxis({ id: 'time', type: 'time', label: 'Time' })
    .addYAxis({ id: 'value', type: 'linear', label: 'Temperature' })
    .addTimeBucketBandSeries({
        id: 'sensor-1',
        axis: 'value',
        data: [
            ['1712102400000000000', 18, 24, 21],
            ['1712102460000000000', 17, 23, 20],
        ],
    })
    .build();
```

## Output adapter

### toEChartsOption()

spec을 ECharts option 객체로 변환합니다.

<h6>문법</h6>

```js
toEChartsOption(spec[, options])
```

<h6>옵션 필드</h6>

| 옵션 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `timeformat` | string | `rfc3339` | ECharts로 time value를 인코딩할 때 사용할 출력 시간 표현입니다. |
| `tz` | string | local timezone | RFC3339 시간값을 렌더링할 때 적용할 timezone입니다. |

<h6>사용 예제</h6>

```js
const option = vizspec.toEChartsOption(spec, {
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
console.println(JSON.stringify(option));
```

### toTUILines()

첫 번째 sparkline-compatible series를 터미널 친화적인 sparkline line 배열로 변환합니다.

<h6>문법</h6>

```js
toTUILines(spec[, options])
```

<h6>옵션 필드</h6>

| 옵션 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `height` | integer | `3` | raw-point 및 time-bucket-value line 출력에 사용할 차트 높이입니다. |
| `width` | integer | `40` | 값을 sampling하고 sparkline 본문을 렌더링할 때 사용할 폭입니다. |
| `seriesId` | string | 첫 번째 compatible series | `series[].id`로 렌더링할 series를 선택합니다. |
| `timeformat` | string | `rfc3339` | sparkline x-axis label에 사용할 출력 시간 형식입니다. |
| `tz` | string | local timezone | sparkline x-axis label에 적용할 timezone입니다. |

- `seriesId`를 주지 않으면 첫 번째 sparkline-compatible series를 반환합니다.
- 선택 가능한 series id를 미리 확인하려면 `listSeries()`를 사용하세요.
- `seriesId`가 없거나 sparkline-compatible하지 않은 series를 가리키면 오류가 발생합니다.
- `height`는 `raw-point`, `time-bucket-value` 출력에만 적용됩니다. `time-bucket-band`는 기존 `max/avg/min` 형식을 유지합니다.

### toTUIBlocks()

spec을 TUI block 배열로 변환합니다.

<h6>문법</h6>

```js
toTUIBlocks(spec[, options])
```

<h6>옵션 필드</h6>

| 옵션 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `width` | integer | `40` | sparkline, histogram, timeline 렌더링 폭입니다. |
| `rows` | integer | `8` | table, histogram, event block에서 보여줄 detail row 최대 개수입니다. |
| `compact` | boolean | `false` | series summary와 raw data table block을 숨깁니다. |
| `timeformat` | string | `rfc3339` | 출력 시간 형식입니다. `rfc3339`, `s`, `ms`, `us`, `ns`를 사용할 수 있습니다. |
| `tz` | string | local timezone | 출력 시간값에 적용할 timezone입니다. |

<h6>block 필드</h6>

| 필드 | 설명 |
| --- | --- |
| `type` | block 종류입니다. 예: `summary`, `series-summary`, `sparkline`, `bandline`, `bars`, `box-summary`, `event-list`, `timeline`, `table`, `annotations`. |
| `title` | block 제목입니다. |
| `stats` | summary 계열 block에서 사용하는 `{ label, value }` 객체 배열입니다. |
| `lines` | sparkline, timeline, histogram 같은 line-oriented block에서 사용하는 문자열 배열입니다. |
| `columns` | `table` block의 column 이름 배열입니다. |
| `rows` | `table` block의 row 배열입니다. 각 row는 column 순서에 맞는 value 배열입니다. |
| `meta` | block별 부가 정보입니다. 예: `representation`, `axis`, `totalRows`, `truncated`. |

### toSVG()

spec을 SVG 문자열로 변환합니다.

<h6>문법</h6>

```js
toSVG(spec[, options])
```

<h6>옵션 필드</h6>

| 옵션 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `width` | integer | `960` | SVG canvas 너비 픽셀값입니다. |
| `height` | integer | `420` | SVG canvas 높이 픽셀값입니다. |
| `padding` | integer | `48` | 차트 바깥 여백 픽셀값입니다. |
| `background` | string | `white` | SVG 배경색입니다. |
| `fontFamily` | string | `sans-serif` | 기본 font family입니다. |
| `fontSize` | integer | `12` | 기본 font 크기 픽셀값입니다. |
| `showLegend` | boolean | `true` | legend 렌더링 여부를 제어합니다. |
| `title` | string | empty | 선택적인 차트 제목입니다. |
| `timeformat` | string | `rfc3339` | axis label 및 출력 시간값에 사용할 시간 형식입니다. |
| `tz` | string | local timezone | RFC3339 시간 렌더링에 적용할 timezone입니다. |

### toPNG()

spec을 PNG 이미지 버퍼로 변환합니다. `toSVG()`와 같은 레이아웃·텍스트·시간 옵션을 받으며 raster 설정을 함께 지정할 수 있습니다.

<h6>문법</h6>

```js
toPNG(spec[, svgOptions[, pngOptions]])
```

## 시간 처리

epoch timestamp를 `s`, `ms`, `us`, `ns` 형식으로 사용하면 값 자체가 UTC 기준 절대 시간을 나타내므로 입력 데이터에 timezone을 따로 명시할 필요가 없습니다. timezone은 원본 timestamp에 붙이는 정보라기보다, 그 timestamp를 사람이 읽는 문자열로 렌더링할 때 적용하는 출력 옵션으로 이해하면 됩니다.

특히 `ns`는 값의 자릿수가 커서 JavaScript `number`로 표현하면 정밀도가 손실될 수 있습니다. 예를 들어 `1712102400000000000` 같은 값은 IEEE 754 배정밀도 부동소수점의 안전한 정수 범위를 넘기므로, nanosecond epoch는 **문자열로 전달**하는 것을 권장합니다.

Machbase Neo timestamp 데이터에는 다음 조합을 권장합니다.

- `timeformat: vizspec.Timeformat.ns`
- JavaScript number 대신 문자열 timestamp 사용

```js
const spec = vizspec.createSpec({
    domain: {
        kind: 'time',
        timeformat: vizspec.Timeformat.ns,
    },
    series: [vizspec.eventRangeSeries({
        id: 'maintenance',
        data: [['1712102400000000000', '1712102460000000000', 'maintenance']],
    })],
});
```

## 시간 렌더링

데이터 소스의 시간 인코딩과 출력 시점의 시간 표현은 서로 다른 관심사입니다.

- `domain.timeformat`은 ADVN 문서 안의 timestamp 인코딩을 설명합니다.
- adapter option의 `timeformat`, `tz`는 그 timestamp를 어떤 형식과 timezone으로 렌더링할지 설명합니다.

adapter option을 생략하면 `vizspec` adapter는 기본적으로 `rfc3339`와 local timezone을 사용합니다.

```js
const svg = vizspec.toSVG(spec, {
    title: 'CPU Usage',
    width: 960,
    height: 420,
    timeformat: vizspec.Timeformat.rfc3339,
    tz: 'Asia/Seoul',
});
```

같은 규칙이 `toTUIBlocks()`와 `toEChartsOption()`에도 적용됩니다.

## viz 명령어 사용

생성한 스펙을 검증하려면 다음과 같이 실행합니다.

```sh
/work > viz validate cpu-usage.json
VALID version=1 series=1 annotations=1
```

터미널에서 확인하려면 다음과 같이 실행합니다.

```sh
/work > viz view cpu-usage.json
```

SVG로 내보내려면 다음과 같이 실행합니다.

```sh
/work > viz export --title "CPU Usage" --output cpu-usage.svg cpu-usage.json
```
