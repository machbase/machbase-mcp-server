# Timer TQL Script Templates

Machbase Neo 타이머에서 실행할 TQL 스크립트 작성 가이드입니다.

## Schedule Options

### CRON Expression (6 fields)
```
Seconds Minutes Hours Day Month DayOfWeek
```
| Example | Description |
|---------|-------------|
| `0 30 * * * *` | Every hour at 30 minutes |
| `0 0 9 * * MON-FRI` | Weekdays at 9:00 AM |
| `*/10 * * * * *` | Every 10 seconds |

### Interval
`@every <duration>` — valid units: "ms", "s", "m", "h"
```
@every 1s
@every 5s
@every 1h30m
@every 500ms
```

### Predefined
| Expression | Description |
|------------|-------------|
| `@daily` | Once a day, midnight |
| `@hourly` | Once an hour |
| `@weekly` | Once a week |
| `@monthly` | Once a month |

## Machbase Neo 타이머 TQL 작성 규칙

타이머 TQL은 매 실행마다 데이터를 생성하거나 수집하여 TAG 테이블에 저장하는 스크립트입니다.

### 공통 규칙
- 주석은 // 한 줄 주석만 사용 (/* */ 블록 주석 불가)
- TAG 테이블 스키마: (NAME varchar, TIME datetime, VALUE double)
- 수학 함수(sqrt, pow, round 등)는 SQL 안이 아닌 MAPVALUE() 안에서 사용
- Machbase SQL에서 현재 시각은 now() 가 아니라 키워드 now 사용
- PUSHVALUE(0, "태그명") 실행 후 기존 컬럼 인덱스가 1씩 뒤로 밀림에 주의
- `auto_start` 옵션은 기본 `false`. 사용자가 명시적으로 요청하지 않으면 항상 `false`로 설정

### 소스 패턴 비교

패턴 A — CSV() 소스
  - tag name을 소스에 직접 포함, 단일 행 1개 생성
  - 시각: time('now') (자동 nanosecond, 별도 변환 불필요)
  - INSERT("name", "time", "value", table("테이블명")) 으로 저장

패턴 B — FAKE(linspace) 소스
  - FAKE(linspace(0, 0, 1)) 로 더미 행 1개 생성
  - 시각: timeUnix(time('now')) * 1000000000 (수동 nanosecond 변환 필요)
  - PUSHVALUE(0, "태그명") 으로 name 컬럼을 앞에 추가
  - APPEND(table("테이블명")) 으로 저장

패턴 C — SQL() 소스 (다중 태그 읽기 + 계산 후 저장)
  - 전제 조건: 원본 테이블에 데이터가 타이머 주기보다 빠르게 계속 수집되고 있어야 함
  - SQL() 로 기존 태그 데이터를 읽어 계산 후 새 테이블에 저장
  - 시간 범위는 타이머 실행 주기보다 충분히 넓게 설정해야 NULL 방지 가능
    (예: 1초 타이머 → WHERE TIME >= now - 5000000000 으로 최근 5초 범위 사용)
  - MAPVALUE() 로 수학 계산 수행 (sqrt, pow 등)
  - PUSHVALUE 후 컬럼 인덱스가 바뀌므로 INSERT 컬럼 순서를 반드시 맞출 것
  - INSERT() 또는 APPEND() 로 결과 저장

패턴 D — FAKE(csv()) 소스 (다중 태그 배치 INSERT)
  - 여러 tag name을 멀티라인 CSV로 한 번에 정의, N개 행 동시 생성
  - strTrimSpace() 로 앞뒤 공백/개행 제거 후 csv() 파싱
  - 시각: roundTime(time('now'), '1s') — 모든 행의 timestamp를 같은 초 단위로 통일
  - 각 행마다 MAPVALUE() 가 독립적으로 실행되어 행별로 다른 값 생성 가능
  - APPEND(table("테이블명")) 으로 저장

패턴 E — SCRIPT("js") 소스 (외부 HTTP API 수집)
  - $.request(url).do(callback) 으로 외부 REST API 호출
  - 응답 JSON을 파싱해서 $.yield(name, timestamp, value) 로 행 생성
  - $.yield() 인자 순서가 곧 value(0), value(1), value(2) 인덱스
  - API 응답 timestamp가 ms 단위일 경우: parseTime(value(N), 'ms', tz('UTC')) 로 변환
  - APPEND(table("테이블명")) 으로 저장

패턴 F — FAKE(arrange) 소스 (고주파 대량 배치 INSERT)
  - FAKE(arrange(1, N, 1)) 로 N개 행 시퀀스 생성
  - 타임스탬프를 수동으로 계산: (timeUnix(time('now')) * 1e9) + (value(0) * 간격ns)
  - 샘플링 간격(ns) = 1,000,000,000 / 샘플링레이트 (예: 111kHz → 약 9000ns)
  - sin(), cos() 등 수학 함수로 파형을 수식으로 직접 설계
  - 한 번 실행에 수만~수십만 개 행을 배치 저장할 때 사용
  - APPEND(table("테이블명")) 으로 저장

패턴 G — FAKE(oscillator) 소스 (주파수 합성 진동 신호 생성)
  - FAKE(oscillator(freq(hz, amplitude), ..., range("now", "기간", "간격"))) 로 복수 주파수 합성 신호 자동 생성
  - 타임스탬프와 합성값이 자동 계산됨 (수동 계산 불필요)
  - range()의 간격이 샘플링 레이트 결정 (예: "1ms" → 1kHz)
  - MAPVALUE(1, value(1) + (random()-0.5) * 비율 * value(1)) 로 신호 크기 비례 노이즈 추가 가능
  - PUSHVALUE(0, "태그명") 으로 name 컬럼 추가
  - APPEND(table("테이블명")) 으로 저장

---

### 예제 1 — 단순 (패턴 A: CSV 소스, 단일 태그)

```tql
// 1초마다 실행 — outdoor_humidity 태그에 습도값 저장
// 대상 테이블: sensor (NAME, TIME, VALUE)

CSV(`outdoor_humidity,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, 30 + random() * 60)
INSERT("name", "time", "value", table("sensor"))
```

---

### 예제 2 — 단순 (패턴 B: FAKE 소스, 단일 태그)

```tql
// 1초마다 실행 — temp_01 태그에 온도값 저장
// 대상 테이블: sensor (NAME, TIME, VALUE)

FAKE(linspace(0, 0, 1))
MAPVALUE(0, timeUnix(time('now')) * 1000000000)
MAPVALUE(1, round((20 + random() * 10) * 100) / 100)
PUSHVALUE(0, "temp_01")
APPEND(table("sensor"))
```

---

### 예제 3 — 단순 (패턴 D: FAKE(csv) 소스, 다중 태그 배치)

```tql
// 1초마다 실행 — 여러 태그를 한 번에 배치 INSERT
// 대상 테이블: tag (NAME, TIME, VALUE)
// 모든 행의 timestamp가 1초 단위로 동일하게 맞춰짐

FAKE(csv(strTrimSpace(`
TAG-01,0,0
TAG-02,0,0
TAG-03,0,0
`)))
MAPVALUE(1, roundTime(time('now'), '1s'))
MAPVALUE(2, random() * 100)
APPEND(table("tag"))
```

---

### 예제 4 — 단순 (패턴 E: 외부 HTTP API 수집)

```tql
// 1초마다 실행 — 빗썸 API에서 BTC 현재가 수집 후 저장
// 대상 테이블: bitcoin (NAME, TIME, VALUE)
// API 응답 timestamp는 millisecond 단위 → parseTime으로 변환

SCRIPT("js", {
    $.request("https://api.bithumb.com/v1/ticker?markets=KRW-BTC")
     .do(function(rsp){
        if ( rsp.error() !== undefined) {
            console.error(rsp.error())
        }
        rsp.text( function(txt){
            list = JSON.parse(txt);
            for (i = 0; i < list.length; i++) {
                obj = list[i];
                $.yield(obj.market, obj.timestamp, obj.trade_price);
            }
        })
    })
})
MAPVALUE(1, parseTime(value(1), 'ms', tz('UTC')))
APPEND(table('bitcoin'))
```

---

### 예제 5 — 복잡 (패턴 F: 고주파 진동 데이터 배치 INSERT)

```tql
// 1초마다 실행 — 약 111kHz 샘플링, 10만 개 사인파 데이터 배치 저장
// 대상 테이블: test (NAME, TIME, VALUE)
// 샘플 간격: 1,000,000,000ns / 100,000 = 9,000ns ≈ 111kHz

FAKE(arrange(1, 100000, 1))
// 사인파: 주기 100포인트 + ±0.005 노이즈
MAPVALUE(1, sin((2*PI*value(0)/100)) + (0.01 * (random() - 0.5)))
// 현재 시각 기준 9000ns 간격으로 타임스탬프 배분
MAPVALUE(0, (timeUnix(time('now')) * 1000000000) + (value(0) * 9000))
PUSHVALUE(0, "data")
APPEND(table("test"))
```

---

### 예제 6 — 복잡 (패턴 G: 주파수 합성 진동 신호 생성)

```tql
// 1초마다 실행 — 150Hz + 300Hz 합성 진동 신호, 1초 분량(1000개) 저장
// 대상 테이블: vibe_data (NAME, TIME, VALUE)
// 비례 노이즈: 신호 크기의 ±5%

FAKE(oscillator(freq(150, 2.0), freq(300, 50), range("now", "1s", "1ms")))
MAPVALUE(1, value(1) + (random()-0.5) * 0.1 * value(1))
PUSHVALUE(0, "vib-x", "name")
APPEND(table("vibe_data"))
```

---

### 예제 7 — 복잡 (패턴 C: 두 태그 읽어 계산 후 INSERT)

```tql
// 전제 조건: VIBE_DATA 테이블에 vib-x, vib-y 태그 데이터가
//            이 타이머보다 빠른 주기로 계속 수집되고 있어야 함
// 1초마다 실행 — vib-x, vib-y 두 태그의 평균으로 합성 진폭 계산 후 저장
// 원본 테이블: VIBE_DATA (NAME, TIME, VALUE)
// 결과 테이블: sensor_derived (NAME, TIME, VALUE)
// 계산식: amplitude = sqrt(x^2 + y^2)
// 시간 범위: 타이머 주기(1s)보다 넉넉하게 최근 5초로 설정

SQL(`
    SELECT
        AVG(CASE WHEN NAME = 'vib-x' THEN VALUE END) as x_val,
        AVG(CASE WHEN NAME = 'vib-y' THEN VALUE END) as y_val
    FROM VIBE_DATA
    WHERE TIME >= now - 5000000000
      AND NAME IN ('vib-x', 'vib-y')
`)
// value(0)=x_val, value(1)=y_val → amplitude로 덮어쓰기
MAPVALUE(0, sqrt(pow(value(0), 2) + pow(value(1), 2)))
MAPVALUE(1, time('now'))
// PUSHVALUE 후: value(0)=name, value(1)=amplitude, value(2)=time
PUSHVALUE(0, "amplitude_xy")
INSERT("name", "value", "time", table("sensor_derived"))
```
