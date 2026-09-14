# Machbase Neo JavaScript Pretty Module

`pretty` 모듈은 JSH 애플리케이션을 위해 값을 서식화하고 터미널 친화적인 출력을 렌더링합니다. 읽기 좋은 표, 사람이 알아보기 쉬운 바이트·기간 문자열, 장시간 작업의 진행 표시가 필요할 때 유용합니다.

```js
const pretty = require('pretty');
```

## Table()

표 writer를 만듭니다.

<h6>문법</h6>

```js
Table(config)
```

<h6>공통 옵션</h6>

| 옵션 | 타입 | 설명 | 기본값 |
| --- | --- | --- | --- |
| `format` | `String` | 출력 형식: `box`, `csv`, `tsv`, `json`, `ndjson`, `html`, `md` | `box` |
| `boxStyle` | `String` | Box style: `light`, `double`, `bold`, `rounded`, `simple`, `compact` | `light` |
| `rownum` | `Boolean` | 앞에 `ROWNUM` 컬럼 포함 | `true` |
| `timeformat` | `String` | 날짜·시간 형식 | `default` |
| `tz` | `String` | 시간대: `local`, `UTC`, 또는 IANA 시간대 이름 | `local` |
| `precision` | `Number` | `0` 이상이면 실수 값을 반올림 | `-1` |
| `header` | `Boolean` | 헤더 행 표시 | `true` |
| `footer` | `Boolean` | 푸터 또는 캡션 표시 | `true` |
| `nullValue` | `String` | null 값에 사용할 문자열 | `NULL` |
| `stringEscape` | `Boolean` | 출력 불가 문자를 `\uXXXX`로 이스케이프 | `false` |

<h6>주요 메서드</h6>

- `appendHeader(values)` 헤더 행을 추가합니다
- `appendRow(row)` 행 하나를 추가합니다
- `appendRows(rows)` 여러 행을 추가합니다
- `append(values)` 행 하나 또는 여러 행을 추가합니다
- `row(...values)` 표 값 변환을 적용해 행을 만듭니다
- `render()` 현재 렌더링된 출력을 문자열로 반환합니다
- `close()` 남은 행을 플러시하고 마지막 렌더링 출력을 반환합니다
- `resetRows()` 버퍼에 쌓인 행을 비웁니다
- `pauseAndWait()` 페이지 모드에서 키 입력을 대기합니다

<h6>사용 예제: 기본 box 표</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light' });
tw.appendHeader(['Name', 'Age']);
tw.appendRow(tw.row('Alice', 30));
tw.appendRow(tw.row('Bob', 25));
console.println(tw.render());
```

Output:

```text
┌────────┬───────┬─────┐
│ ROWNUM │ NAME  │ AGE │
├────────┼───────┼─────┤
│      1 │ Alice │  30 │
│      2 │ Bob   │  25 │
└────────┴───────┴─────┘
```

<h6>사용 예제: JSON 출력</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ format: 'json', rownum: false });
tw.appendHeader(['ID', 'Status', 'Value']);
tw.append([1, 'active', 42.5]);
tw.append([2, 'pending', 31.2]);
console.println(tw.render());
```

<h6>사용 예제: CSV 출력</h6>

```js
const pretty = require('pretty');
const tw = pretty.Table({ format: 'csv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

## Progress()

터미널 출력용 진행 표시 writer를 만듭니다.

<h6>문법</h6>

```js
Progress(options)
```

<h6>옵션</h6>

- `showPercentage` `Boolean` 백분율 표시, 기본값 `true`
- `showETA` `Boolean` 예상 남은 시간 표시, 기본값 `true`
- `showSpeed` `Boolean` 처리 속도 표시, 기본값 `true`
- `updateFrequency` `Number` 갱신 주기(밀리초), 기본값 `250`
- `trackerLength` `Number` 진행 막대 너비, 기본값 `20`

<h6>사용 예제</h6>

```js
const pretty = require('pretty');
const pw = pretty.Progress({ showPercentage: true, showETA: true });
const tracker = pw.tracker({ message: 'Processing', total: 100 });

let interval = setInterval(function() {
    tracker.increment(10);
    if (tracker.value() >= 100) {
        tracker.markAsDone();
        clearInterval(interval);
    }
}, 200);
```

## Bytes()

바이트 수를 사람이 읽기 쉬운 문자열로 서식화합니다.

```js
pretty.Bytes(512);       // "512B"
pretty.Bytes(1536);      // "1.5KB"
pretty.Bytes(1048576);   // "1.0MB"
pretty.Bytes(1073741824);// "1.0GB"
```

## Ints()

정수에 자릿수 구분 기호를 넣어 서식화합니다.

```js
pretty.Ints(1234567890); // "1,234,567,890"
```

## Durations()

나노초 단위 기간을 짧고 읽기 쉬운 문자열로 서식화합니다.

```js
pretty.Durations(1234);           // "1.23μs"
pretty.Durations(2340000);        // "2.34ms"
pretty.Durations(3010000000);     // "3.01s"
pretty.Durations(3661000000000);  // "1h 1m"
pretty.Durations(86400000000000); // "1d 0h"
```

## 터미널 도우미

- `isTerminal()` stdin이 터미널에 연결되어 있는지 반환합니다
- `getTerminalSize()` 터미널의 너비와 높이를 반환합니다
- `pauseTerminal()` 키 입력을 기다립니다
- `parseTime(value, format, tz)` 텍스트를 시간 값으로 파싱합니다

## MakeRow()

지정한 크기의 빈 행 배열을 생성합니다.

<h6>문법</h6>

```js
pretty.MakeRow(size)
```

<h6>사용 예제</h6>

```js
const pretty = require('pretty');
const row = pretty.MakeRow(3);
console.println(row.length);
console.println(Array.isArray(row));
```
