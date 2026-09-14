# Machbase Neo TQL Syntax Reference

## 기본 타입

TQL에는 `string`, `number`, `boolean`, `time`의 기본 타입이 있습니다.

### string

일반적인 프로그래밍 언어처럼 작은따옴표('), 큰따옴표("), 백틱(`)으로 상수 문자열을 정의합니다. 백틱 문자열은 긴 SQL 문처럼 내부에 따옴표가 있고 여러 줄에 걸친 문자열을 정의할 때 유용합니다.

**예제: 백슬래시로 작은따옴표 이스케이프**
```js
SQL( 'select * from example where name=\'temperature\' limit 10' )
CSV()
```

**예제: 큰따옴표 문자열**
```js
SQL( "select * from example where name='temperature' limit 10" )
CSV()
```

**예제: 백틱으로 이스케이프 없이 여러 줄 SQL 문 사용**
```js
SQL( `select * 
      from example 
      where name='temperature'
      limit 10` )
CSV()
```

TQL 스크립트에서 JSON 문자열을 편하게 지정하는 방법으로 이중 중괄호가 있습니다. 따옴표 이스케이프가 필요 없습니다.

아래 두 문자열 표현은 동일합니다:

```js
STRING({{ 
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}})
CSV()
```

```js
STRING(`{ 
    "name": "Connan",
    "hired": true,
    "company": {
        "name":"acme",
        "employee": 123
    }
}`)
CSV()
```

### number

TQL은 모든 숫자 상수를 64비트 부동소수점으로 처리합니다.

```js
SQL_SELECT( 'time', 'value', from('example', 'temperature'), limit(10))
CSV()
```

```js
FAKE( oscillator( freq(12.34, 20), range("now", "1s", "100ms")) )
CSV()
```

### boolean

`true`와 `false`입니다.

```js
FAKE( linspace(0, 1, 1))
CSV( heading(false) )
```

### time

Time 타입 값은 `time()`, `parseTime()` 함수를 호출하거나 SQL 쿼리 결과의 `datetime` 컬럼에서 얻을 수 있습니다.

### timeZone

TimeZone 타입 값은 `tz()` 함수를 호출해 만듭니다.

예: `tz('UTC')`, `tz('Local')`, `tz('Asia/Seoul')`

### list

list는 다른 값들의 배열이며 `list()` 함수로 만듭니다.

예: `list(1, 2, 3)`

### dictionary

dictionary는 (문자열) 이름과 값의 쌍 집합이며 `dict()` 함수로 만듭니다.

예: `dict("name", "pi", "value", 3.14)`

## 문(Statement)

TQL의 모든 문은 문자열·숫자·불리언 리터럴 상수를 제외하면 함수 호출이어야 합니다.

```js
// A comment line starts with '//'

// Each statement should start from first column.
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
CSV()
```

## SRC와 SINK

모든 `.tql` 스크립트는 레코드를 생성하는 소스 문 하나로 시작해야 합니다. 예를 들어 `SQL()`, `SQL_SELECT()`, 그리고 `yield()`·`yieldKey()`로 레코드를 만드는 `SCRIPT()`가 소스가 될 수 있습니다. 마지막 문은 결과를 인코딩하거나 데이터베이스에 쓰는 싱크 문이어야 합니다. 예를 들어 `APPEND()`, `INSERT()`와 모든 `CHART()` 함수가 싱크가 될 수 있습니다.

## MAP 함수

소스와 싱크 문 사이에는 0개 이상의 map 함수가 올 수 있습니다. 모든 map 함수 이름은 대문자이며, 반대로 소문자 카멜 표기 함수는 다른 map 함수의 인자로 사용됩니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    limit(10)
)
DROP(5)
TAKE(5)
CSV()
```

## Param

외부 애플리케이션이 HTTP로 *.tql 스크립트를 호출할 때 쿼리 파라미터로 인자를 전달할 수 있습니다. `param()` 함수는 TQL 스크립트에서 그 쿼리 파라미터 값을 가져오기 위한 것입니다.

아래 스크립트를 'hello2.tql'로 저장하면, 애플리케이션은 `http://127.0.0.1:5654/db/tql/hello2.tql?name=temperature&count=10` 처럼 HTTP GET으로 호출할 수 있습니다. 그러면 `param('name')`은 "temperature"를, `param('count')`는 10을 반환합니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', param('name')),
    limit( param('count') )
)
CSV()
```

**예제:**

아래 코드를 `example.tql`로 저장합니다:

```js
SQL( `select * from example where name = ?`, param('name'))
CSV()
```

`curl` 명령으로 쿼리 파라미터와 함께 tql 파일을 호출합니다:

```sh
curl http://127.0.0.1:5654/db/tql/param.tql?name=TAG0
```

## 연산자

### 산술 연산자

산술 연산자는 덧셈 `+`, 뺄셈 `-`, 곱셈 `*`, 나눗셈 `/` 연산을 수행합니다.

```js
FAKE(linspace(1, 10, 5))
MAPVALUE( 1, value(0) * 100 )
CSV()
```

결과:
```csv
1,100
3.25,325
5.5,550
7.75,775
10,1000
```

### 나머지 연산자

`%`로 표기하는 나머지(모듈로) 연산자는 산술 연산자입니다. 정수 나눗셈의 나머지를 구합니다.

```js
FAKE(arrange(1, 10, 1))
FILTER(value(0) % 3 == 0)
CSV()
```

결과:
```csv
3
6
9
```

### 문자열 연결

`+` 연산자가 문자열을 피연산자로 받으면 연결된 문자열을 반환합니다.

```js
FAKE(json({
    ["hello", "world"]
}))
MAPVALUE(2, value(0) + " " + value(1) + "?")
CSV()
```

결과:
```csv
hello,world,hello world?
```

### 관계 연산자

| 관계 연산 | 연산자 | 설명 |
|:---------------|:---------|:------------|
| 같음 | `==` | 두 피연산자가 같으면 TRUE |
| 다름 | `!=` | 두 피연산자가 다르면 TRUE |
| 초과 | `>` | 왼쪽 값이 오른쪽보다 큰지 검사 |
| 이상 | `>=` | 왼쪽 값이 오른쪽보다 크거나 같은지 검사 |
| 미만 | `<` | 왼쪽 값이 오른쪽보다 작은지 검사 |
| 이하 | `<=` | 왼쪽 값이 오른쪽보다 작거나 같은지 검사 |

```js
FAKE(linspace(1, 5, 5))
FILTER( value(0) >= 4 )
CSV()
```

결과:
```csv
4
5
```

### 논리 연산자

논리 연산자는 and, or, not 연산을 수행합니다.

| 논리 연산 | 연산자 | 설명 |
|:------------|:---------|:------------|
| AND | `&&` | 두 피연산자가 모두 TRUE면 TRUE |
| OR | `||` | 둘 중 하나라도 TRUE면 TRUE |
| NOT | `!` | 피연산자를 하나만 받음 |

```js
FAKE(linspace(1, 5, 5))
FILTER( value(0) > 0  && mod(value(0), 2) == 0 )
CSV()
```

결과:
```csv
2
4
```

### IN 연산자

`A in (args...)`는 args에 `A`가 포함되면 true를, 아니면 false를 반환합니다.

```js
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(0) in ("A", "C") )
CSV()
```

```js
FAKE(json({
    ["A", 1.0],
    ["B", 1.5],
    ["C", 2.0],
    ["D", 2.5]
}))
FILTER( value(1) in (1.5, 2.5) )
CSV()
```

### 삼항 연산자

삼항 연산자 `? :`는 다른 프로그래밍 언어의 if-else 문과 같은 방식으로 동작합니다.

**param('name')이 정의됐는지에 따라:**

```js
SQL_SELECT(
    'time', 'value',
    from('example',
        param('name') == NULL ? 'temperature' : param('name')
    ),
    limit( param('count') ?? 10 )
)
CSV()
```

**조건에 따른 값 변경:**

```js
FAKE(linspace(1, 5, 5))
MAPVALUE(0, mod(value(0), 2) == 0 ? value(0)*10 : value(0))
CSV()
```

결과:
```
1
20
3
40
5
```

### Nil 병합

`??` 연산자는 좌우 피연산자를 받습니다. 왼쪽이 정의돼 있으면 그 값을, 정의돼 있지 않으면 오른쪽 피연산자를 반환합니다. 아래 예제는 `??` 연산자의 일반적인 사용 패턴입니다. 호출자가 쿼리 파라미터를 주지 않으면 오른쪽 피연산자가 기본값이 됩니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', param('name') ?? 'temperature'),
    limit( param('count') ?? 10 )
)
CSV()
```

> tql 스크립트를 저장하면 에디터 우측 상단에 링크 아이콘이 표시됩니다. 클릭하면 스크립트 파일의 주소가 복사됩니다.

**예제:**

아래 코드를 `param-default.tql`로 저장합니다:

```js
SQL( `select * from example limit ?`, param('limit') ?? 1)
CSV()
```

쿼리 파라미터 없이 GET 요청:

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql
```

결과:
```csv
TAG0,1628694000000000000,10
```

쿼리 파라미터와 함께 GET 요청:

```sh
curl http://127.0.0.1:5654/db/tql/param-default.tql?limit=2
```

결과:
```csv
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

## Pragma

`//+ name=value` 지시자는 Machbase Neo가 TQL 스크립트를 어떻게 실행할지 지정합니다.

### log-level

로그 레벨을 `[TRACE | DEBUG | INFO | WARN | ERROR]` 중 하나로 설정합니다. 기본값은 `ERROR`이며, HTTP·MQTT API로 호출될 때 대부분의 로그 메시지를 억제합니다.

```js
//+ log-level=TRACE
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```

### sql-thread-lock

이 프라그마는 지정된 `SQL()`이 전용 네이티브 스레드에서 실행되도록 하며, 그 스레드는 TQL 스크립트가 끝나면 종료됩니다. SRC `SQL()`에서만 동작합니다.

TQL 파일을 실행하는 HTTP 클라이언트 요청 100개를 동시에 보낸 내부 성능 테스트에 따르면, 이 옵션을 켜면 응답 지연이 35% 늘어나지만 메모리 해제 지연은 크게 줄어듭니다.

```js
//+ sql-thread-lock
SQL(`select * from my_table where name = ?`, param("name"))
WHEN(true, doLog('hello world'))
CSV()
```
