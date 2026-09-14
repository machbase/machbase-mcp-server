# Machbase Neo JavaScript Parser Module

`parser` 모듈은 CSV와 NDJSON 데이터를 위한 스트리밍 디코더를 제공합니다.
JSH 스트림과 함께 쓰도록 설계되었으며 파싱된 객체를 이벤트로 내보냅니다.

```js
const parser = require('parser');
```

## 내보내는 멤버

- `csv(options)`
- `ndjson(options)`
- `CSVParser`
- `NDJSONParser`

## csv()

CSV 파서 스트림을 만듭니다.

<h6>문법</h6>

```js
parser.csv([options])
```

<h6>옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-------|:-----|:--------|:------------|
| `separator` | String | `,` | 필드 구분자 |
| `quote` | String | `"` | 인용 문자 |
| `escape` | String | `quote`와 동일 | 이스케이프된 따옴표에 쓰는 이스케이프 문자 |
| `headers` | `true` / `false` / `String[]` | `true` | 헤더 처리 방식 |
| `skipLines` | Number | `0` | 무시할 앞부분 줄 수 |
| `skipComments` | Boolean \| String | `false` | 주석 줄 건너뛰기 |
| `strict` | Boolean | `false` | 행의 컬럼 수가 다르면 실패 |
| `mapHeaders` | Function | | 헤더 이름을 매핑합니다 |
| `mapValues` | Function | | 행을 내보내기 전에 필드 값을 매핑합니다 |
| `trimLeadingSpace` | Boolean | `true` | 각 필드의 앞 공백을 제거합니다 |

<h6>반환값</h6>

`CSVParser` 인스턴스를 반환합니다.

## CSVParser

<h6>이벤트</h6>

- `headers`: 헤더 행이 파싱된 뒤 한 번 발생합니다
- `data`: 파싱된 행 객체마다 발생합니다
- `error`: 엄격 파싱이 실패할 때 발생합니다
- `end`: 상위 스트림이 끝날 때 발생합니다

<h6>속성</h6>

- `bytesWritten`: 받은 입력 바이트 수
- `bytesRead`: 파서가 소비한 바이트 수

<h6>행 구조</h6>

- `headers`를 생략하거나 `true`로 두면 건너뛰지 않은 첫 줄이 헤더 행이 됩니다.
- `headers`가 `false`이면 필드가 `"0"`, `"1"`, `"2"`, ... 로 노출됩니다.
- `headers`가 배열이면 그 이름들을 사용하고 첫 줄은 데이터로 취급합니다.

## ndjson()

NDJSON 파서 스트림을 만듭니다.

<h6>문법</h6>

```js
parser.ndjson([options])
```

<h6>옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-------|:-----|:--------|:------------|
| `strict` | Boolean | `true` | 잘못된 JSON 줄을 건너뛰지 않고 실패 처리합니다 |

## NDJSONParser

<h6>이벤트</h6>

- `data`: 파싱된 JSON 객체마다 발생합니다
- `warning`: `strict: false`일 때 잘못된 줄마다 발생합니다
- `error`: 엄격 파싱이 실패할 때 발생합니다
- `end`: 상위 스트림이 끝날 때 발생합니다

`warning` 이벤트 객체는 `line`, `data`, `error`를 포함합니다.

## CSV example

```js
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.csv')
    .pipe(parser.csv({
        headers: true,
        mapValues: ({ header, value }) => header === 'age' ? parseInt(value, 10) : value,
    }))
    .on('headers', (headers) => {
        console.println(headers.join(','));
    })
    .on('data', (row) => {
        console.println(row.name, row.age);
    });
```

## NDJSON 예제

```js
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.ndjson')
    .pipe(parser.ndjson({ strict: false }))
    .on('data', (obj) => {
        console.println(obj.id);
    })
    .on('warning', (warn) => {
        console.println('Skipped line:', warn.line);
    });
```

## 동작 참고사항

- 두 파서 클래스 모두 JSH `stream.Transform` 구현을 상속합니다.
- 파싱된 행과 객체는 `data` 이벤트로 전달됩니다.
- 두 파서 모두 빈 줄을 무시합니다.
- `NDJSONParser`는 파싱 전에 각 줄의 공백을 제거합니다.
- `CSVParser`는 끝의 `\r`을 제거해 `\r\n` 입력을 올바르게 처리합니다.
