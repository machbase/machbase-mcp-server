# Machbase Neo TQL Time Examples

## 사전 준비

원활한 실습을 위해 아래 쿼리를 실행해 테이블과 데이터를 준비합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12 12:00:00 123:456:789'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13 12:00:00 123:456:789'), 11);
```

TQL은 여러 `Time` 조작 함수를 지원합니다.

## 시간 함수

### Now

`time("now")`는 현재 시각을 반환합니다.

```js
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```

결과:
```
2021-08-12 12:00:00 123:456:789,10
2021-08-13 12:00:00 123:456:789,11
```

### Timestamp

`time(epoch)`은 UNIX epoch를 나노초 단위로 표현한 시각을 반환합니다.

```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```

## 시간 변환

TQL로 `Timestamp`와 `시간 포맷 문자열` 사이의 변환을 손쉽게 처리할 수 있습니다.

### Timestamp → 시간 포맷 문자열

아래 코드를 TQL 에디터에 붙여넣고 `time_to_format.tql`로 저장합니다.

```js
STRING(param("format_time") ?? "808210800", separator('\n'))
SCRIPT({
    epoch = parseInt($.values[0])
    time = new Date(epoch*1000)
    $.yield(epoch, time.toISOString())
})
CSV()
```

URL: http://127.0.0.1:5654/db/tql/time_to_format.tql?format_time=808210800000000001

### 시간 포맷 문자열 → Timestamp

아래 코드를 TQL 에디터에 붙여넣고 `format_to_time.tql`로 저장합니다.

```js
STRING(param("timestamp") ?? "1995-08-12T00:00:00.000Z", separator('\n'))
SCRIPT({
    ts = new Date(Date.parse($.values[0]));
    epoch = ts.getTime() / 1000;
    $.yield(epoch, ts.toISOString())
})
CSV()
```

URL: http://127.0.0.1:5654/db/tql/format_to_time.tql?timestamp=1995-08-12T00:00:00.000Z

## 시간 포맷

출력에서 시간을 어떻게 표현할지 지정합니다.

### 지정 없음

```js
SQL(`select to_char(time), time from example`)
CSV()
```

결과:
```
2021-08-12 12:00:00 123:456:789,1628737200123456789
2021-08-13 12:00:00 123:456:789,1628823600123456789
```

### Default

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```

#### 추가 Default 유형

| 유형 | 설명 |
|:-----|:------------|
| DEFAULT_MS | 2006-01-02 15:04:05.999 |
| DEFAULT_US | 2006-01-02 15:04:05.999999 |
| DEFAULT_NS | 2006-01-02 15:04:05.999999999 |
| DEFAULT.MS | 2006-01-02 15:04:05.000 |
| DEFAULT.US | 2006-01-02 15:04:05.000000 |
| DEFAULT.NS | 2006-01-02 15:04:05.000000000 |

### Numeric

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('NUMERIC'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,08/12 03:00:00AM '21 +0000
2021-08-13 12:00:00 123:456:789,08/13 03:00:00AM '21 +0000
```

### Ansic

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('ANSIC'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 2021
```

### Unix

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('UNIX'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 UTC 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 UTC 2021
```

### RFC822

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC822'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,12 Aug 21 03:00 UTC
2021-08-13 12:00:00 123:456:789,13 Aug 21 03:00 UTC
```

### RFC3339

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC3339'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12T03:00:00Z
2021-08-13 12:00:00 123:456:789,2021-08-13T03:00:00Z
```

## 시간대(Timezone)

`tz` 함수로 시간대를 지정합니다.

### Local

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('local'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### UTC

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('UTC'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```

### Seoul

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Asia/Seoul'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### EST

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('EST'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-11 22:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-12 22:00:00.123
```

### Paris

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Europe/Paris'))
```

결과:
```
2021-08-12 12:00:00 123:456:789,2021-08-12 05:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 05:00:00.123
```
