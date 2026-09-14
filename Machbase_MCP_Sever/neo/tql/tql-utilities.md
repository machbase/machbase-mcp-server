# Machbase Neo TQL Utility Functions

유틸리티 함수는 어떤 함수의 파라미터로도 공통으로 사용할 수 있습니다.

## Constants

| 상수 | 설명 |
|:----------|:------------|
| `NULL` | null value |
| `PI` | 3.141592.... https://oeis.org/A000796 |

## Context

### key()

**문법**: `key()`

현재 레코드의 키를 반환합니다.

### value()

**문법**: `value( [index] )`

**Parameters:**
- `index` - 정수 (선택), 값 배열의 인덱스

현재 레코드의 전체 값을 배열로 반환합니다. 인덱스를 주면 해당 위치의 값을 반환합니다.

예를 들어 현재 값이 `[0, true, "hello", "world"]` 라면

- `value()`는 전체 값 배열 `[0, true, "hello", "world"]` 를 반환합니다
- `value(0)`은 값의 첫 번째 요소 `0` 을 반환합니다
- `value(3)`은 값의 마지막 요소 `"world"` 를 반환합니다

### payload()

**문법**: `payload()`

TQL 스크립트 호출자가 보낸 현재 입력 스트림을 반환합니다. HTTP로 호출되면 `payload()`는 POST 요청 본문의 스트림이고, MQTT로 호출되면 PUBLISH 메시지의 페이로드를 반환합니다.

### param()

**문법**: `param( name )`

**Parameters:**
- `name` - 문자열, 쿼리 파라미터 이름

TQL 스크립트가 HTTP로 호출되면 `param()` 함수로 요청의 쿼리 파라미터에 접근할 수 있습니다.

### context()

**문법**: `context()`

스크립트 런타임의 컨텍스트 객체를 반환합니다.

## String

### escapeParam()

**문법**: `escapeParam( str ) : string` 

*버전 8.0.7 이상*

`escapeParam()`은 문자열을 URL 쿼리 안에 안전하게 넣을 수 있도록 이스케이프합니다.

```js
CSV(
    file(`http://127.0.0.1:5654/db/query?format=csv&q=`+
        escapeParam(`select count(*) from example`)
    )
)
CSV()
```

### strTrimSpace()

**문법**: `strTrimSpace(str) : string`

*버전 8.0.7 이상*

`strTrimSpace`는 문자열 str의 앞뒤 공백을 모두 제거한 결과를 반환합니다.

### strTrimPrefix()

**문법**: `strTrimPrefix(str, prefix) : string`

*버전 8.0.7 이상*

`strTrimPrefix`는 주어진 접두 문자열을 제거한 str을 반환합니다. str이 해당 접두로 시작하지 않으면 str을 그대로 반환합니다.

### strTrimSuffix()

**문법**: `strTrimSuffix(str, suffix) : string`

*버전 8.0.7 이상*

`strTrimSuffix`는 주어진 접미 문자열을 제거한 str을 반환합니다. str이 해당 접미로 끝나지 않으면 str을 그대로 반환합니다.

### strHasPrefix()

**문법**: `strHasPrefix(str, prefix) : boolean`

*버전 8.0.7 이상*

`strHasPrefix`는 문자열 str이 주어진 접두로 시작하는지 검사합니다.

### strHasSuffix()

**문법**: `strHasSuffix(str, suffix) : boolean`

*버전 8.0.7 이상*

`strHasSuffix`는 문자열 s가 주어진 접미로 끝나는지 검사합니다.

### strReplaceAll()

**문법**: `strReplaceAll(str, old, new) : string`

*버전 8.0.7 이상*

`strReplaceAll`은 문자열 s에서 겹치지 않는 old를 모두 new로 바꾼 사본을 반환합니다. old가 비어 있으면 문자열 시작과 각 UTF-8 시퀀스 뒤에서 매칭되어, k개 문자 문자열에 대해 최대 k+1번 치환됩니다.

### strReplace()

**문법**: `strReplace(str, old, new, n) : string`

*버전 8.0.7 이상*

**Parameters:**
- `str` - String
- `old` - String
- `new` - String
- `n` - Integer

`strReplace`는 문자열 s에서 겹치지 않는 old를 앞에서부터 n개까지 new로 바꾼 사본을 반환합니다. old가 비어 있으면 문자열 시작과 각 UTF-8 시퀀스 뒤에서 매칭되어, k개 문자 문자열에 대해 최대 k+1번 치환됩니다. n이 0보다 작으면 치환 횟수에 제한이 없습니다.

### strSub()

**문법**: `strSub(str, offset [, count]) : string`

*버전 8.0.7 이상*

`strSub`는 str의 부분 문자열을 반환합니다.

### strIndex()

**문법**: `strIndex(str, substr) : number`

*버전 8.0.15 이상*

str에서 substr이 처음 나타나는 인덱스를 반환하며, 없으면 -1을 반환합니다.

### strLastIndex()

**문법**: `strLastIndex(str, substr) : number`

*버전 8.0.15 이상*

str에서 substr이 마지막으로 나타나는 인덱스를 반환하며, 없으면 -1을 반환합니다.

### strToUpper()

**문법**: `strToUpper(str) : string`

*버전 8.0.7 이상*

`strToUpper`는 str의 모든 유니코드 문자를 대문자로 바꿔 반환합니다.

### strToLower()

**문법**: `strToLower(str, suffix) : string`

*버전 8.0.7 이상*

`strToLower`는 str의 모든 유니코드 문자를 소문자로 바꿔 반환합니다.

### strSprintf()

**문법**: `strSprintf(fmt, args...) : string`

*버전 8.0.7 이상*

`strSprintf()`는 형식 지정자에 따라 서식을 적용한 문자열을 반환합니다.

`fmt` 형식 문자열의 문법은 `%[flags][width][.precision]verb` 입니다.

끝의 verb가 대응 인자의 타입과 해석 방식을 정의합니다.

| Verb | 설명 |
| :--- | :---------- |
| f | 10진 부동소수점, 소문자 |
| F | 10진 부동소수점, 대문자 |
| e | 지수 표기(가수/지수), 소문자 |
| E | 지수 표기(가수/지수), 대문자 |
| g | %e 또는 %f 중 더 짧은 표현 |
| G | %E 또는 %F 중 더 짧은 표현 |
| q | 따옴표로 감싼 문자열 |
| t | true 또는 false |
| s | a string |
| v | 기본 형식 |
| %% | a single % |

**Example:**

```js
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
MAPVALUE(2, strSprintf(`hello %s? %1.2f`, value(0), value(1)))
CSV()
```

**Output:**

```csv
world,3.141792,hello world? 3.14
```

### strTime()

**문법**: `strTime(time, format [, tz]) : string`

*버전 8.0.7 이상*

**Parameters:**
- `time` - Time
- `format` - 문자열 또는 sqlTimeformat()
- `tz` - 시간대 (선택). 원하는 지역은 `tz()`로 지정하며, 생략하면 기본값은 `tz('UTC')` 입니다.

`strTime()`은 주어진 형식과 시간대에 따라 시간 값을 문자열로 변환합니다.

#### 숫자 시간 형식

```js
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
MARKDOWN(rownum(true))
```

#### SQL 시간 형식

```js
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), sqlTimeformat("YYYY/MM/DD HH24:MI:SS.nnn"), tz("UTC")), "result")
MARKDOWN(rownum(true))
```

| ROWNUM | 결과 |
|:-------|:-------|
| 1 | 2024/01/10 07:27:29.667 |

#### 이름 있는 시간 형식

*버전 8.0.12 이상*

```js
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "RFC822", tz("UTC")), "time")
MARKDOWN(rownum(true))
```

| ROWNUM | time |
|:-------|:-----|
| 1 | 10 Jan 24 07:23 UTC |

### parseFloat()

**문법**: `parseFloat( str ) : number`

*버전 8.0.7 이상*

**Parameters:**
- `str` - String

`str`을 실수로 파싱합니다.

**Example:**

```js
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
JSON()
```

**Output:**

```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "double" ],
        "rows": [ [ "world", 3.141792 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "140.125µs"
}
```

### parseBool()

**문법**: `parseBool( str ) : boolean`

*버전 8.0.7 이상*

**Parameters:**
- `str` - String

"1", "t", "T", "TRUE", "true", "True", "0", "f", "F", "FALSE", "false", "False" 중 하나를 받아 true 또는 false로 변환합니다. 그 밖의 문자열에 대해서는 오류를 반환합니다.

**Example:**

```js
FAKE( csv(`world,True`) )
MAPVALUE(1, parseBool(value(1)))
JSON()
```

**Output:**

```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "bool" ],
        "rows": [ [ "world", true ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "122.667µs"
}
```

## 문자열 매칭

### glob()

**문법**: `glob(pattern, text) : boolean`

*버전 8.0.7 이상*

`glob`은 `text`가 `pattern`과 일치하면 true를 반환합니다.

```js
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( glob("*.3", value(0)), doLog("found", value(1)))
CSV()
```

### regexp()

**문법**: `regexp(expression, text) : boolean`

*버전 8.0.7 이상*

`regexp`는 `text`가 `expression`과 일치하면 true를 반환합니다.

```js
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( regexp(`^map\.[2,3]$`, value(0)), doLog("found", value(1)))
CSV()
```

## Time

### time()

**문법**: `time( number|string ) : time`

**Examples:**
- `time('now')`는 현재 시각을 반환합니다.
- `time('now -10s50ms')`는 현재로부터 10.05초 전의 시각을 반환합니다.
- `time(1672531200*1000000000)`는 2023년 1월 1일 오전 12:00:00을 반환합니다

#### time('now') 사용

```js
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```

#### time(epoch) 사용

```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```

### timeYear()

**문법**: `timeYear( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeYear()는 해당 시간이 속한 연도를 반환합니다.

### timeMonth()

**문법**: `timeMonth( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeMonth()는 해당 시간의 월을 반환합니다.

### timeDay()

**문법**: `timeDay( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeDay()는 해당 시간의 일(날짜)을 반환합니다.

### timeHour()

**문법**: `timeHour( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeHour()는 해당 시간의 시(0~23)를 반환합니다.

### timeMinute()

**문법**: `timeMinute( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeMinute()는 해당 시간의 분(0~59)을 반환합니다.

### timeSecond()

**문법**: `timeSecond( time ) : number`

*버전 8.0.15 이상*

timeSecond()는 해당 시간의 초(0~59)를 반환합니다.

### timeNanosecond()

**문법**: `timeNanosecond( time ) : number`

*버전 8.0.15 이상*

timeNanosecond()는 해당 시간의 나노초(0~999999999)를 반환합니다.

### timeISOYear()

**문법**: `timeISOYear( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeISOYear()는 ts가 속한 ISO 8601 연도를 반환합니다.

### timeISOWeek()

**문법**: `timeISOWeek( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeISOWeek()는 해당 시간이 속한 ISO 8601 주차를 반환합니다. 주차는 1~53입니다. n년 1월 1일~3일은 n-1년의 52 또는 53주차에, 12월 29일~31일은 n+1년의 1주차에 속할 수 있습니다.

한 해의 첫 주는 그해 첫 목요일이 포함된 주이고, 마지막 주는 다음 해 첫 주 바로 앞의 주라는 규칙을 따릅니다. 자세한 내용은 https://www.iso.org/obp/ui#iso:std:iso:8601:-1:ed-1:v1:en:term:3.1.1.23 를 참고하세요.

### timeYearDay()

**문법**: `timeYearDay( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeYearDay()는 해당 시간의 연중 일자를 반환합니다. 평년은 [1,365], 윤년은 [1,366] 범위입니다.

### timeWeekDay()

**문법**: `timeWeekDay( time [, timezone] ) : number`

*버전 8.0.15 이상*

timeWeekDay()는 해당 시간의 요일을 반환합니다. (일요일 = 0, ...)

```js
FAKE(arrange(1, 7, 1))
MAPVALUE(0, time(strSprintf("now - %.fd",value(0))))
GROUP( lazy(true), by(timeWeekDay(value(0))), count(value(0)) )
CSV()
```

### timeUnix()

**문법**: `timeUnix( time ) : number`

*버전 8.0.13 이상*

timeUnix는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC 이후 경과한 초 수로 반환합니다. 결과는 `time`에 연결된 지역과 무관합니다.

### timeUnixMilli()

**문법**: `timeUnixMilli( time ) : number`

*버전 8.0.13 이상*

timeUnixMilli는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC 이후 경과한 밀리초 수로 반환합니다. 결과는 `time`에 연결된 지역과 무관합니다.

### timeUnixMicro()

**문법**: `timeUnixMicro( time ) : number`

*버전 8.0.13 이상*

timeUnixMicro는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC 이후 경과한 마이크로초 수로 반환합니다. 결과는 `time`에 연결된 지역과 무관합니다.

### timeUnixNano()

**문법**: `timeUnixNano( time ) : number`

*버전 8.0.13 이상*

timeUnixNano는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC 이후 경과한 나노초 수로 반환합니다. 결과는 `time`에 연결된 지역과 무관합니다.

### timeAdd()

**문법**: `timeAdd( number|string|time [, timeExpression] ) : time`

**Examples:**
- `timeAdd('now', 0)`은 현재 시각을 반환합니다.
- `timeAdd('now', '-10s50ms')`는 현재로부터 10.05초 전의 시각을 반환합니다.
- `timeAdd(value(0), '1m')`은 value(0)이 시간일 때 value(0)으로부터 1분 뒤의 시각을 반환합니다.

#### timeAdd('now') 사용

```js
SQL(`select to_char(time), value from example where time < ?`, timeAdd('now', '-10s'))
CSV()
```

#### timeAdd(epoch) 사용

```js
SQL(`select to_char(time), value from example where time = ?`, timeAdd(1628737200123456789, '-5s'))
CSV()
```

### roundTime()

**문법**: `roundTime( time, duration ) : time`

반올림된 시간을 반환합니다.

**Examples:**
- `roundTime(time('now'), '1h')`
- `roundTime(value(0), '1s')`

### parseTime()

**문법**: `parseTime( time, format [, timezone] ) : time`

**Parameters:**
- `time` - 문자열, 시간 표현
- `format` - 문자열, 시간 형식 표현
- `timezone` - 시간대. 원하는 지역은 `tz()`로 지정하며, 생략하면 기본값은 `tz("UTC")` 입니다.

**Examples:**
- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("Asia/Tokyo"))`
- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("local"))`

### tz()

**문법**: `tz( name ) : timeZone`

주어진 이름에 해당하는 시간대를 반환합니다.

**Examples:**
- `tz('local')`
- `tz('UTC')`
- `tz('EST')`
- `tz("Europe/Paris")`

### timeformat()

**문법**: `timeformat( format )`

**Parameters:**
- `format` - String

**Example:**

```js
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV(timeformat("DEFAULT"), tz("Asia/Seoul"))
```

**Output:**

```
2023-11-30 20:50:32.123,10
2023-11-30 20:50:43.219,11
```

**사용 가능한 형식:**

| 형식 | 시간 서식 결과 |
|:-------|:-------------------------|
| DEFAULT | 2006-01-02 15:04:05.999 |
| NUMERIC | 01/02 03:04:05PM '06 -0700 |
| ANSIC | Mon Jan _2 15:04:05 2006 |
| UNIX | Mon Jan _2 15:04:05 MST 2006 |
| RUBY | Mon Jan 02 15:04:05 -0700 2006 |
| RFC822 | 02 Jan 06 15:04 MST |
| RFC822Z | 02 Jan 06 15:04 -0700 |
| RFC850 | Monday, 02-Jan-06 15:04:05 MST |
| RFC1123 | Mon, 02 Jan 2006 15:04:05 MST |
| RFC1123Z | Mon, 02 Jan 2006 15:04:05 -0700 |
| RFC3339 | 2006-01-02T15:04:05Z07:00 |
| RFC3339NANO | 2006-01-02T15:04:05.999999999Z07:00 |
| KITCHEN | 3:04:05PM |
| STAMP | Jan _2 15:04:05 |
| STAMPMILLI | Jan _2 15:04:05.000 |
| STAMPMICRO | Jan _2 15:04:05.000000 |
| STAMPNANO | Jan _2 15:04:05.000000000 |
| s | 초 단위 unix epoch 시간 |
| ms | 밀리초 단위 unix epoch 시간 |
| us | 마이크로초 단위 unix epoch 시간 |
| ns | 나노초 단위 unix epoch 시간 |
| s_ms | 초와 밀리초 (05.999) |
| s_us | 초와 마이크로초 (05.999999) |
| s_ns | 초와 나노초 (05.999999999) |
| s.ms | 초와 밀리초, 0 채움 (05.000) |
| s.us | 초와 마이크로초, 0 채움 (05.000000) |
| s.ns | 초와 나노초, 0 채움 (05.000000000) |

### sqlTimeformat()

**문법**: `sqlTimeformat( format )`

**Parameters:**
- `format` - String

**사용 가능한 형식:**

| 형식 | 시간 서식 결과 |
|:-------|:-------------------------|
| YYYY | 네 자리 연도 |
| YY | 두 자리 연도 |
| MM | 01~12의 두 자리 월 |
| MMM | 요일 |
| DD | 01~31의 두 자리 일 |
| HH24 | 00~23의 두 자리 시 |
| HH12 | 0~12의 두 자리 시 |
| HH | 0~12의 두 자리 시 |
| MI | 00~59의 두 자리 분 |
| SS | 0~59의 두 자리 초 |
| AM | AM/PM |
| nnn... | 1~9자리 소수점 이하 초 |

**Example:**

```js
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( sqlTimeformat("YYYY-MM-DD HH24:MI:SS.nnnnnn"), tz("Asia/Seoul") )
```

**Output:**

```
2023-11-30 20:50:32.123456,10
2023-11-30 20:50:43.219876,11
```

### ansiTimeformat()

**문법**: `ansiTimeformat( format )`

**Parameters:**
- `format` - String

**Example:**

```js
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( ansiTimeformat("yyyy-mm-dd hh:nn:ss.ffffff"), tz("UTC"))
```

**Output:**

```
2023-11-30 11:50:32.123456,10
2023-11-30 11:50:43.219876,11
```

**사용 가능한 형식:**

| 형식 | 시간 서식 결과 |
|:-------|:-------------------------|
| yyyy | 네 자리 연도 |
| mm | 01~12의 두 자리 월 |
| dd | 01~31의 두 자리 일 |
| hh | 00~23의 두 자리 시 |
| nn | 00~59의 두 자리 분 |
| ss | 0~59의 두 자리 초 |
| fff... | 1~9자리 소수점 이하 초 |

## Math

수학 함수입니다.

*버전 8.0.6 이상*

> 이 함수는 시스템 아키텍처가 달라도 비트 단위로 동일한 결과를 보장하지는 않습니다.

| 함수 | 설명 |
|:---------|:------------|
| `abs(x)` | x의 절댓값. |
| `acos(x)` | x의 아크코사인(라디안). |
| `acosh(x)` | x의 역쌍곡코사인. |
| `asin(x)` | x의 아크사인(라디안). |
| `asinh(x)` | x의 역쌍곡사인. |
| `atan(x)` | x의 아크탄젠트(라디안). |
| `atanh(x)` | x의 역쌍곡탄젠트. |
| `ceil(x)` | x 이상인 가장 작은 정수. |
| `cos(x)` | 라디안 인자 x의 코사인. |
| `cosh(x)` | x의 쌍곡코사인. |
| `exp(x)` | e**x, x의 자연지수. |
| `exp2(x)` | 2**x, x의 밑 2 지수. |
| `floor(x)` | x 이하인 가장 큰 정수. |
| `log(x)` | x의 자연로그. |
| `log2(x)` | x의 이진로그. 특수 경우는 log와 같습니다. |
| `log10(x)` | x의 상용로그. 특수 경우는 log와 같습니다. |
| `max(x,y)` | x와 y 중 큰 값. |
| `min(x,y)` | x와 y 중 작은 값. |
| `mod(x,y)` | x/y의 부동소수점 나머지. 결과의 크기는 y보다 작고 부호는 x와 같습니다. |
| `pow(x, y)` | x**y, 밑이 x인 y 제곱. |
| `pow10(x)` | 10**x, 밑이 10인 x 제곱. |
| `remainder(x,y)` | x/y의 IEEE 754 부동소수점 나머지. |
| `round(x)` | 가장 가까운 정수. 0.5는 0에서 먼 쪽으로 반올림. |
| `sin(x)` | 라디안 인자 x의 사인. |
| `sinh(x)` | x의 쌍곡사인. |
| `sqrt(x)` | x의 제곱근. |
| `tan(x)` | 라디안 인자 x의 탄젠트. |
| `tanh(x)` | x의 쌍곡탄젠트. |
| `trunc(x)` | x의 정수부. |

`MAPVALUE`와 함께 수학 함수를 사용하는 예제입니다.

**Example:**

```js
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
MAPVALUE(2,
    sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2))
)
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{},
        yAxis3D:{},
        zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```

### random()

**문법**: `random() : number`

*버전 8.0.7 이상*

`random()`은 반열린 구간 [0.0,1.0)의 의사난수 실수를 반환합니다.

### simplex()

**문법**: `simplex(seed, dim1 [, dim2 [, dim3 [, dim4]]]) : number`

*버전 8.0.7 이상*

**Parameters:**
- `seed` - 정수, 시드 번호
- `dim1` ~ `dim4` - 실수

`simplex()`는 주어진 시드와 차원 값으로 SimpleX 노이즈를 반환합니다.

**Example:**

```js
FAKE(
    meshgrid(
        linspace(0, 10, 100), linspace(0, 10, 100)
    )
)
MAPVALUE(2, abs( simplex(123, value(0), value(1)) ) * 10)
MAPVALUE(0, list(value(0), value(1), value(2)))
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        visualMap: {
            max: 8,
            inRange:{ color:[ 
                    "#313695", "#74add1", "#e0f3f8",
                    "#fee090",  "#f46d43", "#a50026"]}
        },
        grid3D:{ boxWidth:100, boxDepth:100, boxHeight:20},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "bar3D", data: column(0), itemStyle:{opacity:1.0}},
        ]
    })
)
```

## List

### count()

**문법**: `count( array|tuple ) : number`

요소의 개수를 반환합니다.

### list()

**문법**: `list(args...) : list`

*버전 8.0.7 이상*

`list()`는 `args`를 요소로 갖는 새 튜플을 반환합니다.

### dict()

**문법**: `dict( name1, value1 [, name2, value2 ...]) : dictionary`

*버전 8.0.8 이상*

`dict()`는 name*n*:value*n* 쌍을 담은 새 딕셔너리를 반환합니다.
