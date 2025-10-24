# Machbase Neo MCP 서버 성능 평가

## 평가 기준
- **표현의 정확성 (Presentation)**: 0개: 감점 없음, 1개: 감점 1점, 2-3개: 감점 2점, 4개 이상: 감점 3점
- **정확성 (Definition Accuracy)**: 0개: 감점 없음, 경미: 감점 2점, 중대: 감점 4점, 완전 오류: 0점
- **코드 품질 (Code Quality)**: 0개: 감점 없음, 1개: 감점 1점, 2-3개: 감점 2점, 4개 이상: 감점 3점

---

## 질문 1: Machbase Neo 설치 방법 알려줘

### 답변
**응답시간: 약 3초**

Machbase Neo의 설치 방법은 크게 **직접 설치**와 **Docker 설치** 두 가지 방식이 있습니다.

#### 1. 직접 설치 (권장)

**원라인 설치 스크립트:**
```bash
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

**수동 설치 단계:**

1. 플랫폼별 다운로드:
   - https://docs.machbase.com/neo/releases/ 에서 최신 버전 다운로드
   
2. 압축 해제:
```bash
# Linux AMD64
unzip machbase-neo-v8.0.58-linux-amd64.zip

# Linux ARM64
unzip machbase-neo-v8.0.58-linux-arm64.zip

# macOS Apple Silicon
unzip machbase-neo-v8.0.58-darwin-arm64.zip

# macOS Intel
unzip machbase-neo-v8.0.58-darwin-amd64.zip

# Windows
unzip machbase-neo-v8.0.58-windows-amd64.zip
```

3. 실행 파일 확인:
```bash
machbase-neo version
```

#### 2. Docker 설치

**Docker Pull:**
```bash
# 최신 버전
docker pull machbase/machbase-neo

# 특정 버전
docker pull machbase/machbase-neo:v8.0.58
```

**Docker Run:**
```bash
# 포그라운드 실행
docker run -it machbase/machbase-neo

# 백그라운드 실행
docker run -d machbase/machbase-neo

# 포트 매핑과 볼륨 마운트
docker run -d \
  -p 5652-5656:5652-5656/tcp \
  -v /path/to/host/data:/data \
  -v /path/to/host/file:/file \
  --name machbase-neo \
  machbase/machbase-neo
```

#### 3. 시작 및 종료

**Linux & macOS:**
```bash
# 시작 (로컬호스트만)
machbase-neo serve

# 원격 접속 허용
machbase-neo serve --host 0.0.0.0

# 종료
machbase-neo shell shutdown
```

**Windows:**
- neow.exe 실행 후 "machbase-neo serve" 버튼 클릭

#### 4. 웹 UI 접속

- URL: http://127.0.0.1:5654/
- 기본 계정: ID `sys`, Password `manager`
- 보안을 위해 첫 로그인 후 비밀번호 변경 권장

**포트 정보:**
- 5652: sshd
- 5653: mqtt
- 5654: http
- 5655: grpc
- 5656: database engine

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확하고 체계적인 설명 |
| 정확성 | 0점 | 공식 문서 기반의 정확한 정보 |
| 코드 품질 | 0점 | 실행 가능한 명령어 제공 |
| **총점** | **10점** | |

---

## 질문 2: TQL이 뭐야? 설명이랑 DB에서 실행 가능한 예제 한개 알려줘

### 답변
**응답시간: 약 4초**

#### TQL(Transforming Query Language)이란?

TQL은 Machbase Neo의 **데이터 변환 전용 언어**로, 데이터베이스에서 데이터를 조회하고, 변환하고, 시각화하는 전 과정을 몇 줄의 스크립트로 처리할 수 있는 도메인 특화 언어(DSL)입니다.

**주요 특징:**

1. **SRC → MAP → SINK 구조**
   - **SRC (Source)**: 데이터 소스 정의 (SQL, CSV, FAKE 등)
   - **MAP (Transform)**: 데이터 변환 처리
   - **SINK (Output)**: 출력 형식 정의 (CHART, CSV, JSON 등)

2. **다양한 출력 형식 지원**
   - 동일한 데이터를 CSV, JSON, CHART, HTML 등 다양한 형식으로 출력 가능

3. **RESTful API로 활용**
   - TQL 스크립트를 저장하면 HTTP 엔드포인트로 자동 변환

#### 실행 가능한 예제

**예제 1: 데이터 생성 및 CSV 출력**

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CSV()
```

**실행 결과:**
```
1761282103873595600,-0.9288637935916196
1761282103883595600,-0.8898825776269057
1761282103893595600,-0.8430009619703097
1761282103903595600,-0.7886388468673482
1761282103913595600,-0.7272743767454072
...
```

**예제 2: 라인 차트 시각화**

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_LINE()
```

**예제 3: 실제 DB 데이터 조회 및 시각화**

```js
SQL(`select time, value from example where name = 'temperature' limit 50`)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

**검증 결과:** 위 코드는 실제 DB에서 실행되어 차트 ID가 반환되었습니다.

#### TQL의 장점

- 애플리케이션 개발 없이 데이터 API 생성 가능
- 복잡한 데이터 변환 로직을 간결하게 표현
- 다양한 데이터 소스와 출력 형식 지원

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 개념 설명과 구조 제시 |
| 정확성 | 0점 | 정확한 TQL 개념 및 문법 설명 |
| 코드 품질 | 0점 | 실제 실행 검증 완료 |
| **총점** | **10점** | |

---

## 질문 3: DB 에서 실행 가능한 SQL 예제 한개 알려줘

### 답변
**응답시간: 약 2초**

현재 DB에 있는 EXAMPLE 테이블에서 데이터를 조회하는 SQL 예제입니다.

#### 예제: 기본 SELECT 쿼리

```sql
SELECT * FROM EXAMPLE LIMIT 10
```

**실행 결과:**
```csv
NAME,TIME,VALUE
TAG0,2021-08-12 00:00:00,10
TAG0,2021-08-13 00:00:00,11
testing,2025-10-13 11:02:54.063,17.34753619634643
testing,2025-10-13 11:02:54.063,75.36623344830315
testing,2025-10-13 11:02:54.067,79.82716797313066
temperature,2024-02-22 15:19:50,23.45
temperature,2024-02-22 15:19:51,24.56
temperature,2024-02-22 15:19:52,32.34
temperature,2024-02-22 15:19:53,33.45
temperature,2024-02-22 15:19:52,32.34
```

#### 추가 예제: 특정 태그 조회

```sql
SELECT NAME, TIME, VALUE 
FROM EXAMPLE 
WHERE NAME = 'temperature' 
ORDER BY TIME DESC 
LIMIT 5
```

#### 추가 예제: 집계 쿼리

```sql
SELECT 
    NAME,
    COUNT(*) as count,
    AVG(VALUE) as avg_value,
    MIN(VALUE) as min_value,
    MAX(VALUE) as max_value
FROM EXAMPLE
GROUP BY NAME
```

**검증:** 모든 쿼리는 실제 DB에서 실행되어 결과가 확인되었습니다.

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 SQL 예제 제시 |
| 정확성 | 0점 | 실제 실행 가능한 쿼리 |
| 코드 품질 | 0점 | 표준 SQL 문법 준수 |
| **총점** | **10점** | |

---

## 질문 4: 현재 DB 에 있는 테이블 뭐가 있는지 알려줘

### 답변
**응답시간: 약 1초**

현재 Machbase Neo 데이터베이스에는 다음 테이블들이 있습니다:

1. **BITCOIN** - 비트코인 관련 데이터
2. **BUSAN_VVVF_0818** - 부산 VVVF 데이터 (8월 18일)
3. **BUSAN_VVVF_0819** - 부산 VVVF 데이터 (8월 19일)
4. **BUSAN_VVVF_0820** - 부산 VVVF 데이터 (8월 20일)
5. **DRIVING_BEHAVIOR** - 운전 행동 데이터
6. **EXAMPLE** - 예제 데이터 테이블
7. **IMPORTANT_DATA** - 중요 데이터
8. **SECRET_DATA** - 비밀 데이터
9. **SENSOR_TEST** - 센서 테스트 데이터
10. **SP500** - S&P 500 주식 데이터
11. **STAT** - 통계 데이터
12. **TEST** - 테스트 테이블
13. **TEST_ROLLUP** - 롤업 기능 테스트 테이블
14. **TEST_SPECIAL_CHARS** - 특수문자 테스트 테이블

**총 14개 테이블**

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 테이블 목록 제시 |
| 정확성 | 0점 | 실제 DB 테이블 정보 |
| 코드 품질 | 0점 | 해당 없음 |
| **총점** | **10점** | |

---

## 질문 5: DB에 roll up 기능이 포함된 test 테이블을 만들어줘

### 답변
**응답시간: 약 3초**

Rollup 기능이 포함된 TAG 테이블을 생성했습니다.

#### 테이블 생성 SQL

```sql
CREATE TAG TABLE test_rollup (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP
```

#### Rollup 테이블 설명

**생성된 테이블:**
- `test_rollup`: 원본 TAG 테이블

**자동 생성된 Rollup 테이블들:**
- `_test_rollup_ROLLUP_SEC`: 초 단위 집계
- `_test_rollup_ROLLUP_MIN`: 분 단위 집계
- `_test_rollup_ROLLUP_HOUR`: 시간 단위 집계

#### 테이블 구조 설명

1. **sensor_id** (VARCHAR PRIMARY KEY): 센서 식별자
2. **event_time** (DATETIME BASETIME): 시간 기준 컬럼
3. **value** (DOUBLE SUMMARIZED): 집계 대상 값

#### Rollup 기능

Rollup은 대규모 시계열 데이터에 대한 통계 집계를 사전 계산하여 쿼리 성능을 크게 향상시키는 기능입니다.

**지원 집계 함수:**
- MIN(), MAX(), AVG(), SUM(), COUNT(), SUMSQ()

**사용 예제:**
```sql
-- 시간별 평균값 조회 (Rollup 활용)
SELECT
    ROLLUP('hour', 1, event_time) AS hour_time,
    AVG(value) AS avg_value
FROM test_rollup
WHERE sensor_id = 'SENSOR_A'
GROUP BY hour_time
ORDER BY hour_time
```

**검증:** 테이블이 성공적으로 생성되었으며, 테이블 목록에서 확인되었습니다.

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 테이블 생성 설명 |
| 정확성 | 0점 | 올바른 Rollup 문법 사용 |
| 코드 품질 | 0점 | 실행 가능한 DDL |
| **총점** | **10점** | |

---

## 질문 6: DB 에서 실행 가능한 TQL 시각화 코드 알려줘

### 답변
**응답시간: 약 3초**

DB에서 실행 가능한 TQL 시각화 예제입니다.

#### 예제 1: 실제 DB 데이터 라인 차트

```js
SQL(`select time, value from example where name = 'temperature' limit 50`)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        tooltip: { trigger:"axis" },
        series: [
            {
                type: "line",
                data: column(0)
            }
        ]
    })
)
```

**검증 결과:** 
- HTTP 200 응답
- 차트 ID 생성 확인: `MjY5OTgxODc0NDI1NDk5NjQ4`
- 데이터 존재 확인: 308개 레코드

#### 예제 2: 여러 시리즈가 있는 라인 차트

```js
FAKE( json({
    ["Mon", 820],
    ["Tue", 932],
    ["Wed", 901],
    ["Thu", 934],
    ["Fri", 1290],
    ["Sat", 1330],
    ["Sun", 1320]
}) )
CHART(
    chartOption({
        legend:{ show:false },
        xAxis: { type:"category", data: column(0) },
        yAxis: {},
        series:[
            { 
                type: "line", 
                smooth:false, 
                color:"#7585CE", 
                areaStyle:{}, 
                data: column(1) 
            }
        ]
    })
)
```

#### 예제 3: 실시간 데이터 시뮬레이션

```js
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART(
    chartOption({
        xAxis: {
            type: "category",
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "line",
                data: column(1)
            }
        ]
    })
)
```

#### 차트 타입 변형

```js
// BAR 차트
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_BAR()

// SCATTER 차트
FAKE( oscillator(freq(1.5, 1.0), range('now', '3s', '10ms')) )
CHART_SCATTER()
```

**모든 예제는 실제 실행 및 검증 완료되었습니다.**

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 다양한 시각화 예제 제공 |
| 정확성 | 0점 | 실행 가능하고 정확한 TQL 코드 |
| 코드 품질 | 0점 | 실제 실행 검증 완료 |
| **총점** | **10점** | |

---

## 질문 7: 롤업(Rollup) 기능 설명 및 DB 에서 실행 가능한 예제 코드 알려줘

### 답변
**응답시간: 약 5초**

#### Rollup 기능이란?

Rollup은 Machbase Neo의 **시계열 데이터 사전 집계 기능**으로, 대규모 데이터에 대한 통계 쿼리 성능을 극적으로 향상시킵니다.

#### 핵심 개념

**1. 자동 사전 집계**
- 데이터가 삽입되면 자동으로 시간 단위별 집계 수행
- SEC (초), MIN (분), HOUR (시간) 단위 지원

**2. 성능 비교**
```sql
-- SLOW: 일반 집계 (수백만 레코드 스캔)
SELECT DATE_TRUNC('hour', time) as hour_time, AVG(value)
FROM sensor_data
WHERE name = 'SENSOR_A'
GROUP BY DATE_TRUNC('hour', time);

-- FAST: Rollup 사용 (사전 집계 데이터 읽기, 100배+ 빠름)
SELECT ROLLUP('hour', 1, time) AS hour_time, AVG(value)
FROM sensor_data
WHERE name = 'SENSOR_A'
GROUP BY hour_time;
```

#### 지원 집계 함수

**기본 함수:**
- MIN(), MAX(), AVG(), SUM(), COUNT(), SUMSQ()

**확장 함수 (EXTENSION 사용 시):**
- FIRST(), LAST()

#### 실행 가능한 예제

**예제 1: Rollup 테이블 생성**

```sql
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;
```

**예제 2: 데이터 삽입 및 조회**

```sql
-- 데이터 삽입
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 10:00:00', 20.5);
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 10:05:00', 21.0);
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 11:00:00', 23.0);
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 10:10:00', 21.5);
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 10:15:00', 22.0);
INSERT INTO test_rollup VALUES ('SENSOR_A', '2024-10-24 11:30:00', 24.0);

-- Rollup을 활용한 시간별 집계
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value
FROM test_rollup
WHERE sensor_id = 'SENSOR_A'
GROUP BY hour_interval
ORDER BY hour_interval;
```

**예제 3: 커스텀 Rollup 생성**

```sql
-- 15분 단위 Rollup 생성
CREATE ROLLUP iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;

-- 15분 단위 집계 조회
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
GROUP BY interval_15min
ORDER BY interval_15min;
```

#### Rollup 관리 명령

```sql
-- Rollup 상태 확인
SHOW ROLLUPGAP;

-- Rollup 강제 처리
EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_SEC');

-- Rollup 데이터 삭제
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');

-- Rollup 테이블 삭제
DROP ROLLUP _iot_sensors_rollup_15min;
```

**검증:** test_rollup 테이블이 생성되고 데이터가 삽입되었습니다.

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 개념 설명 |
| 정확성 | 0점 | 정확한 Rollup 기능 설명 |
| 코드 품질 | 0점 | 실행 가능한 예제 제공 |
| **총점** | **10점** | |

---

## 질문 8: DB 에서 실행 가능한 geomap 예제 코드 알려줘

### 답변
**응답시간: 약 3초**

DB에서 실행 가능한 GEOMAP 시각화 예제입니다.

#### GEOMAP이란?

GEOMAP은 **지리적 좌표를 기반으로 지도에 마커와 도형을 표시**하는 TQL 함수입니다. WGS84 좌표 시스템을 사용합니다.

#### 예제 1: 기본 마커 표시

```js
FAKE(json({
    ["Seoul", 37.5665, 126.9780],
    ["Busan", 35.1796, 129.0756]
}))

SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            tooltip: {
                content: '<b>'+name+'</b>',
                permanent: true
            }
        }
    });
})

GEOMAP()
```

**실행 결과:**
- HTTP 200 응답
- Geomap ID: `MjY5OTgyODAxNDg0MTI0MTYw`
- 지도에 서울과 부산 마커 표시

#### 예제 2: 원형 마커 (Circle Marker)

```js
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circleMarker",
        coordinates: [lat, lon],
        properties:{
            radius: 40
        }
    });
})

GEOMAP()
```

#### 예제 3: 반경 원 표시 (Circle)

```js
FAKE(json({
    [38.935, -105.520]
}))

SCRIPT({
    var lat = $.values[0];
    var lon = $.values[1];
    $.yield({
        type: "circle",
        coordinates: [lat, lon],
        properties:{
            radius: 400  // 미터 단위
        }
    });
})

GEOMAP()
```

#### 예제 4: 경로 선 (Polyline)

```js
FAKE(json({
    [45.51, -122.68],
    [37.77, -122.43],
    [34.04, -118.2]
}))

SCRIPT({
    var points = [];
    function finalize() {
        $.yield({
            type: "polyline",
            coordinates: points
        });
    }
},{
    var lat = $.values[0];
    var lon = $.values[1];
    points.push( [lat, lon] );
})

GEOMAP()
```

#### 예제 5: 팝업과 툴팁

```js
FAKE(json({
    ["Stoll Mountain", 38.9934, -105.5018],
    ["Pulver Mountain", 39.0115, -105.5173]
}))

SCRIPT({
    var name = $.values[0];
    var lat  = $.values[1];
    var lon  = $.values[2];
    $.yield({
        type: "marker",
        coordinates: [lat, lon],
        properties: {
            popup: {
                content: '<b>'+name+'</b>'
            },
            tooltip: {
                content: '<b>'+name+'</b>',
                direction: "auto",
                permanent: true
            }
        }
    });
})

GEOMAP()
```

#### 레이어 타입

- **marker**: 기본 마커
- **circleMarker**: 픽셀 단위 원형 마커
- **circle**: 미터 단위 원
- **polyline**: 선
- **polygon**: 다각형

**모든 예제는 실제 실행 및 검증이 완료되었습니다.**

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 GEOMAP 설명 |
| 정확성 | 0점 | 정확한 좌표 및 문법 |
| 코드 품질 | 0점 | 실행 검증 완료 |
| **총점** | **10점** | |

---

## 질문 9: timer 설정 방법 알려줘

### 답변
**응답시간: 약 2초**

Machbase Neo의 Timer는 **특정 시간에 자동으로 작업을 실행하거나 주기적으로 반복 실행**하는 기능입니다.

#### Timer 추가 방법

**1. 웹 UI 사용 (v8.0.20 이상)**
1. 좌측 메뉴에서 타이머 아이콘 선택
2. 좌측 상단 `+` 버튼 클릭
3. Timer ID, Timer Spec, TQL 스크립트 경로 설정
4. "Create" 버튼 클릭

**2. 명령줄 사용**
```bash
timer add [--autostart] <name> <timer_spec> <tql-path>;
```

#### Timer 스케줄 사양

**1. CRON 표현식**
```
0 30 * * * *           # 매시 30분
0 0 9 * * MON-FRI      # 평일 오전 9시
0 0 0 1 * *            # 매월 1일 자정
```

**CRON 필드:**
| 필드 | 값 | 특수문자 |
|------|-------|----------|
| Seconds | 0-59 | * / , - |
| Minutes | 0-59 | * / , - |
| Hours | 0-23 | * / , - |
| Day | 1-31 | * / , - ? |
| Month | 1-12, JAN-DEC | * / , - |
| Day of Week | 0-6, SUN-SAT | * / , - ? |

**2. 사전 정의된 스케줄**
```
@yearly 또는 @annually   # 매년 1월 1일 자정
@monthly                  # 매월 1일 자정
@weekly                   # 매주 일요일 자정
@daily 또는 @midnight     # 매일 자정
@hourly                   # 매시간
```

**3. 간격 지정**
```
@every 10h               # 10시간마다
@every 1h30m             # 1시간 30분마다
@every 5s                # 5초마다
```

#### 실전 예제: Hello World Timer

**1. TQL 스크립트 생성 (helloworld.tql)**
```js
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

**2. Timer 등록**
```bash
timer add helloworld "@every 5s" helloworld.tql;
```

**3. Timer 시작**
```bash
timer start helloworld;
```

**4. 결과 확인**
```sql
SELECT * FROM example WHERE name = 'helloworld' ORDER BY time DESC LIMIT 10;
```

#### Timer 관리 명령

```bash
# Timer 목록 확인
timer list;

# Timer 시작
timer start <name>;

# Timer 중지
timer stop <name>;

# Timer 삭제
timer del <name>;
```

#### Timer 상태 확인 예시
```
┌────────────┬───────────┬────────────────┬───────────┬─────────┐
│ NAME       │ SPEC      │ TQL            │ AUTOSTART │ STATE   │
├────────────┼───────────┼────────────────┼───────────┼─────────┤
│ HELLOWORLD │ @every 5s │ helloworld.tql │ false     │ RUNNING │
└────────────┴───────────┴────────────────┴───────────┴─────────┘
```

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 Timer 설정 방법 |
| 정확성 | 0점 | 정확한 CRON 문법 및 명령어 |
| 코드 품질 | 0점 | 실행 가능한 예제 |
| **총점** | **10점** | |

---

## 질문 10: DB 에 있는 SP500 테이블에서 최근 30일간의 일별 평균값과 변동률을 계산하는 TQL을 작성해줘

### 답변
**응답시간: 약 4초**

SP500 테이블의 최근 30일간 일별 평균값과 변동률을 계산하는 TQL입니다.

#### SP500 테이블 정보
- 시간 범위: 2017-09-11 ~ 2018-02-16
- 샘플 데이터: A_close 종목의 분단위 주가 데이터

#### TQL 스크립트

```js
SQL(`
    SELECT 
        DATE_TRUNC('day', time) as day,
        AVG(value) as daily_avg
    FROM SP500
    WHERE name = 'A_close'
        AND time >= '2018-01-17'
        AND time <= '2018-02-16'
    GROUP BY DATE_TRUNC('day', time)
    ORDER BY day
`)

// Calculate daily change rate
SCRIPT({
    var prevAvg = null;
},{
    var day = $.values[0];
    var dailyAvg = $.values[1];
    var changeRate = prevAvg === null ? 0 : ((dailyAvg - prevAvg) / prevAvg) * 100;
    
    $.yield(day, dailyAvg.toFixed(2), changeRate.toFixed(2));
    prevAvg = dailyAvg;
})

CSV()
```

#### 실행 결과 (22일간의 데이터)

```csv
day,daily_avg,change_rate(%)
2018-01-17,72.02,0.00
2018-01-18,72.08,0.09
2018-01-19,72.92,1.17
2018-01-22,73.08,0.22
2018-01-23,73.53,0.61
2018-01-24,73.59,0.09
2018-01-25,73.99,0.54
2018-01-26,74.38,0.53
2018-01-29,74.58,0.27
2018-01-30,73.30,-1.72
2018-01-31,73.71,0.56
2018-02-01,72.92,-1.07
2018-02-02,72.00,-1.26
2018-02-05,70.35,-2.28
2018-02-06,67.46,-4.11
2018-02-07,68.48,1.52
2018-02-08,66.80,-2.45
2018-02-09,66.23,-0.86
2018-02-12,68.35,3.20
2018-02-13,68.03,-0.47
2018-02-14,69.00,1.43
2018-02-15,72.15,4.55
```

#### 코드 설명

**1. SQL 부분:**
- `DATE_TRUNC('day', time)`: 시간을 일 단위로 절삭
- `AVG(value)`: 일별 평균값 계산
- 30일 범위: 2018-01-17 ~ 2018-02-16

**2. SCRIPT 부분:**
- `prevAvg`: 이전 날의 평균값 저장
- `changeRate`: 전일 대비 변동률 계산 공식
  - `((오늘 평균 - 어제 평균) / 어제 평균) × 100`
- 첫날은 변동률 0%로 설정

**3. CSV() 출력:**
- 날짜, 평균값, 변동률을 CSV 형식으로 출력

#### 차트 시각화 버전

```js
SQL(`
    SELECT 
        DATE_TRUNC('day', time) as day,
        AVG(value) as daily_avg
    FROM SP500
    WHERE name = 'A_close'
        AND time >= '2018-01-17'
        AND time <= '2018-02-16'
    GROUP BY DATE_TRUNC('day', time)
    ORDER BY day
`)

SCRIPT({
    var prevAvg = null;
    var data = [];
},{
    var day = $.values[0];
    var dailyAvg = $.values[1];
    var changeRate = prevAvg === null ? 0 : ((dailyAvg - prevAvg) / prevAvg) * 100;
    
    data.push([day, dailyAvg, changeRate]);
    prevAvg = dailyAvg;
},{
    $.yield({
        xAxis: { type: "time" },
        yAxis: [
            { name: "Average" },
            { name: "Change Rate (%)", position: "right" }
        ],
        series: [
            { type: "line", name: "Daily Avg", data: data.map(d => [d[0], d[1]]) },
            { type: "bar", name: "Change Rate", yAxisIndex: 1, data: data.map(d => [d[0], d[2]]) }
        ]
    });
})

CHART()
```

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 로직 설명 |
| 정확성 | 0점 | 정확한 변동률 계산 |
| 코드 품질 | 0점 | 실행 검증 완료 |
| **총점** | **10점** | |


## 질문 11: 비트코인 테이블의 데이터 정합성을 분석해주고 분석한 방법에 대해 알려줘

### 답변
**응답시간: 약 4초**

비트코인 테이블의 데이터 정합성을 다각도로 분석했습니다.

#### 테이블 기본 정보
```
총 레코드 수: 453,021개
고유 NAME 수: 18개
시간 범위: 2024-11-24 20:40:00 ~ 2025-09-04 10:43:28
```

#### 분석 1: 통계적 데이터 정합성

```sql
SELECT 
    name,
    COUNT(*) as record_count,
    COUNT(DISTINCT time) as unique_times,
    MIN(value) as min_value,
    MAX(value) as max_value,
    AVG(value) as avg_value,
    COUNT(CASE WHEN value IS NULL THEN 1 END) as null_count,
    COUNT(CASE WHEN value < 0 THEN 1 END) as negative_count
FROM BITCOIN
GROUP BY name
ORDER BY name
```

**주요 발견 사항:**

1. **NULL 값**: 모든 NAME에서 NULL 값 0개 ✓
2. **음수 값**: 
   - `BTC-signed_change_price`: 12,106개 (정상 - 가격 하락)
   - `BTC-signed_change_rate`: 12,104개 (정상 - 변동률 하락)
3. **고유 시간**: 대부분 NAME에서 record_count = unique_times ✓
4. **단일 레코드**: `BTC-trace_volumn` 1개만 존재

#### 분석 2: 시간 간격 정합성

```js
SQL(`
    SELECT name, time
    FROM BITCOIN
    WHERE name = 'BTC-trade_price'
    ORDER BY time
    LIMIT 100
`)

SCRIPT({
    var prevTime = null;
    var gaps = [];
},{
    var currentTime = $.values[1];
    if (prevTime !== null) {
        var gap = (currentTime.Unix() - prevTime.Unix());
        gaps.push(gap);
    }
    prevTime = currentTime;
},{
    if (gaps.length > 0) {
        gaps.sort((a, b) => a - b);
        var sum = gaps.reduce((a, b) => a + b, 0);
        var avg = sum / gaps.length;
        var median = gaps[Math.floor(gaps.length / 2)];
        var min = gaps[0];
        var max = gaps[gaps.length - 1];
        
        $.yield({
            "count": gaps.length,
            "min": min,
            "max": max,
            "avg": avg.toFixed(2),
            "median": median
        });
    }
})

JSON()
```

**결과:**
- 평균 간격: 63.03초
- 중앙값: 60초
- 최소 간격: 60초
- 최대 간격: 360초
- **정합성 평가**: 대체로 1분 간격으로 균일하게 저장됨 ✓

#### 분석 3: 이상치 탐지 (변동률 분석)

```js
SQL(`
    SELECT name, time, value
    FROM BITCOIN
    WHERE name = 'BTC-trade_price'
    ORDER BY time
    LIMIT 1000
`)

SCRIPT({
    var prevValue = null;
    var anomalies = 0;
    var changes = [];
    var records = 0;
},{
    var value = $.values[2];
    records++;
    
    if (prevValue !== null && prevValue !== 0) {
        var changeRate = Math.abs((value - prevValue) / prevValue);
        changes.push(changeRate);
        
        // 10% 이상 변동은 이상치로 간주
        if (changeRate > 0.1) {
            anomalies++;
        }
    }
    prevValue = value;
},{
    if (changes.length > 0) {
        var sum = changes.reduce((a, b) => a + b, 0);
        var avg = sum / changes.length;
        
        $.yield("Total Records", records);
        $.yield("Valid Comparisons", changes.length);
        $.yield("Anomalies (>10% change)", anomalies);
        $.yield("Anomaly Rate", (anomalies / changes.length * 100).toFixed(2) + "%");
        $.yield("Avg Change Rate", (avg * 100).toFixed(4) + "%");
    }
})

CSV()
```

**결과:**
- 총 레코드: 1,000개
- 비교 가능: 999개
- 이상치 (10% 이상 변동): 0개
- 이상치 비율: 0.00%
- 평균 변동률: 0.0630%
- **정합성 평가**: 매우 안정적이고 정상적인 데이터 ✓

#### 종합 분석 결과

**정합성 점수: 9.5/10**

**강점:**
1. ✓ NULL 값 없음
2. ✓ 시간 간격 일정 (약 1분)
3. ✓ 이상치 없음
4. ✓ 변동률 정상 범위
5. ✓ 음수 값은 의미상 정상 (가격 하락)

**개선 필요:**
- `BTC-trace_volumn`이 1개 레코드만 존재 (확인 필요)

**분석 방법론:**
1. SQL 집계를 통한 기본 통계
2. 시계열 간격 분석
3. 변동률 기반 이상치 탐지
4. TQL SCRIPT를 활용한 실시간 분석

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 체계적이고 명확한 분석 |
| 정확성 | 0점 | 정확한 데이터 분석 |
| 코드 품질 | 0점 | 실행 검증 완료 |
| **총점** | **10점** | |

---

## 질문 12: driving behavior 의 데이터를 다양한 노이즈 필터를 적용하는 tql 코드를 알려줘

### 답변
**응답시간: 약 3초**

DRIVING_BEHAVIOR 테이블의 가속도 데이터에 다양한 노이즈 필터를 적용하는 TQL 코드입니다.

#### 테이블 정보
- 센서 종류: AccX, AccY, AccZ, GyroX, GyroY, GyroZ, Class
- AccX 레코드 수: 6,728개

#### 다양한 필터 적용 TQL

```js
SQL(`
    SELECT time, value
    FROM DRIVING_BEHAVIOR
    WHERE name = 'AccX'
    ORDER BY time
    LIMIT 200
`)

// Apply various noise filters
MAP_MOVAVG(2, value(1), 5)      // Moving Average (window=5)
MAP_MOVAVG(3, value(1), 10)     // Moving Average (window=10)
MAP_LOWPASS(4, value(1), 0.3)   // Low Pass Filter (alpha=0.3)
MAP_LOWPASS(5, value(1), 0.5)   // Low Pass Filter (alpha=0.5)

CHART(
    size("800px", "500px"),
    chartOption({
        title: { text: "Driving Behavior - AccX with Noise Filters" },
        xAxis: { type: "category", data: column(0) },
        yAxis: { name: "Acceleration (m/s²)" },
        legend: { bottom: 10 },
        tooltip: { trigger: "axis" },
        series: [
            { type: "line", name: "Original", data: column(1), lineStyle: { width: 1 } },
            { type: "line", name: "MA(5)", data: column(2), smooth: true },
            { type: "line", name: "MA(10)", data: column(3), smooth: true },
            { type: "line", name: "LPF(0.3)", data: column(4), smooth: true },
            { type: "line", name: "LPF(0.5)", data: column(5), smooth: true }
        ]
    })
)
```

#### 필터별 특징

**1. Moving Average (이동 평균)**

```js
MAP_MOVAVG(2, value(1), 5)   // 5개 샘플 평균
MAP_MOVAVG(3, value(1), 10)  // 10개 샘플 평균
```

- 고정 윈도우 크기의 샘플 평균
- 윈도우가 클수록 더 부드러운 곡선
- 최근 트렌드 반영이 느림

**2. Low Pass Filter (저주파 통과 필터)**

```js
MAP_LOWPASS(4, value(1), 0.3)  // alpha=0.3
MAP_LOWPASS(5, value(1), 0.5)  // alpha=0.5
```

- 최근 값에 더 많은 가중치
- alpha 값이 클수록 빠른 반응
- 신호 변화에 민감

**3. Kalman Filter (칼만 필터)**

```js
MAP_KALMAN(2, value(1), model(0.1, 0.5, 1.0))
```

- 시스템 모델 기반 최적 추정
- 노이즈와 신호 특성 모두 고려
- 가장 정교한 필터

#### 추가 예제: 모든 필터 비교

```js
SQL(`
    SELECT time, value
    FROM DRIVING_BEHAVIOR
    WHERE name = 'AccX'
    ORDER BY time
    LIMIT 300
`)

// 원본 데이터
PUSHVALUE(2, value(1))  // Original

// 다양한 필터 적용
MAP_MOVAVG(3, value(1), 5)              // MA(5)
MAP_MOVAVG(4, value(1), 20)             // MA(20)
MAP_LOWPASS(5, value(1), 0.2)           // LPF(0.2)
MAP_LOWPASS(6, value(1), 0.6)           // LPF(0.6)
MAP_KALMAN(7, value(1), model(0.1, 0.5, 1.0))  // Kalman

CHART(
    size("1000px", "600px"),
    chartOption({
        title: { 
            text: "AccX Signal - Comprehensive Filter Comparison",
            subtext: "Moving Average, Low Pass, and Kalman Filters"
        },
        xAxis: { 
            type: "category", 
            data: column(0),
            axisLabel: { show: false }
        },
        yAxis: { 
            name: "Acceleration",
            type: "value"
        },
        legend: { 
            bottom: 10,
            type: "scroll"
        },
        tooltip: { 
            trigger: "axis",
            axisPointer: { type: "cross" }
        },
        dataZoom: [
            { type: "inside" },
            { type: "slider", bottom: 50 }
        ],
        series: [
            { 
                type: "line", 
                name: "Original", 
                data: column(2), 
                lineStyle: { width: 1, opacity: 0.5 },
                symbol: "none"
            },
            { 
                type: "line", 
                name: "MA(5)", 
                data: column(3),
                smooth: true,
                symbol: "none"
            },
            { 
                type: "line", 
                name: "MA(20)", 
                data: column(4),
                smooth: true,
                symbol: "none"
            },
            { 
                type: "line", 
                name: "LPF(0.2)", 
                data: column(5),
                smooth: true,
                symbol: "none"
            },
            { 
                type: "line", 
                name: "LPF(0.6)", 
                data: column(6),
                smooth: true,
                symbol: "none"
            },
            { 
                type: "line", 
                name: "Kalman", 
                data: column(7),
                smooth: true,
                lineStyle: { width: 2 },
                symbol: "none"
            }
        ]
    })
)
```

#### 필터 선택 가이드

| 필터 종류 | 용도 | 장점 | 단점 |
|----------|------|------|------|
| Moving Average | 일반적인 노이즈 제거 | 구현 간단 | 지연 발생 |
| Low Pass | 실시간 처리 | 빠른 반응 | 파라미터 조정 필요 |
| Kalman | 정밀 측정 | 최적 추정 | 모델 설정 복잡 |

**검증:** 코드 실행 확인, 차트 ID 생성됨

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 필터 설명 |
| 정확성 | 0점 | 정확한 TQL 문법 |
| 코드 품질 | 0점 | 실행 가능한 코드 |
| **총점** | **10점** | |

---

## 질문 13: Python서 Machbase Neo에 연결하는 방법을 알려줘

### 답변
**응답시간: 약 2초**

Python에서 Machbase Neo에 연결하는 방법을 상세히 설명드립니다.

#### 1. 설치

```bash
pip3 install machbaseAPI
```

**검증:**
```bash
python3 - <<'PY'
from machbaseAPI.machbaseAPI import machbase
print('machbaseAPI import ok')
cli = machbase()
print('isConnected():', cli.isConnected())
PY
```

#### 2. 기본 연결 예제

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    # 데이터베이스 객체 생성
    db = machbase()
    
    # 연결
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())
    
    print('Connected! Session ID:', db.getSessionId())
    print('Is Connected:', db.isConnected())
    
    # 연결 종료
    if db.close() == 0:
        raise SystemExit(db.result())
    
    print('Connection closed')

if __name__ == '__main__':
    main()
```

#### 3. 테이블 생성 및 데이터 삽입

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        # 테이블 삭제 (존재하는 경우)
        db.execute('DROP TABLE py_sample')
        
        # 테이블 생성
        ddl = (
            "CREATE TABLE py_sample ("
            "ts DATETIME,"
            "device VARCHAR(40),"
            "value DOUBLE"
            ")"
        )
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('Table created:', db.result())

        # 데이터 삽입
        for seq in range(3):
            sql = (
                "INSERT INTO py_sample VALUES ("
                f"TO_DATE('2024-01-0{seq+1}','YYYY-MM-DD'),"
                f"'sensor-{seq}',"
                f"{20.5 + seq}"
                ")"
            )
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print(f'Inserted row {seq+1}:', db.result())

    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### 4. 데이터 조회 (SELECT)

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        # SELECT 실행
        if db.select('SELECT * FROM py_sample ORDER BY ts') == 0:
            raise SystemExit(db.result())

        print('Rows available:', db.count())
        
        # 결과 페치
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            row = json.loads(payload)
            print('Row:', row)

        # 결과셋 닫기
        db.selectClose()
        
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### 5. Append Protocol (고성능 삽입)

```python
#!/usr/bin/env python3
import json
import re
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        # 테이블 생성
        ddl = 'CREATE TABLE py_append_demo(ts DATETIME, device VARCHAR(32), value DOUBLE)'
        db.execute(ddl)
        
        # 컬럼 타입 조회
        if db.columns('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())
        column_payload = db.result()
        col_specs = [json.loads(item) for item in re.findall(r'\{[^}]+\}', column_payload)]
        types = [spec.get('type') for spec in col_specs]
        print('Column types:', types)

        # Append 세션 열기
        if db.appendOpen('PY_APPEND_DEMO', types) == 0:
            raise SystemExit(db.result())

        # 데이터 추가
        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', types, rows) == 0:
            raise SystemExit(db.result())
        print('Data appended')

        # Flush
        if db.appendFlush() == 0:
            raise SystemExit(db.result())
        
        # Append 세션 닫기
        if db.appendClose() == 0:
            raise SystemExit(db.result())
        print('Append completed')
        
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### 6. 편의 함수 (append)

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('CREATE TABLE py_append_auto(ts DATETIME, tag VARCHAR(16), reading DOUBLE)')
        
        # 타입 코드: '6'=DATETIME, '5'=VARCHAR, '20'=DOUBLE
        types = ['6', '5', '20']
        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        
        # 한 번에 append
        if db.append('PY_APPEND_AUTO', types, values) == 0:
            raise SystemExit(db.result())
        print('Append successful:', db.result())
        
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### 주요 API 메서드

| 메서드 | 설명 | 반환값 |
|--------|------|--------|
| `open(host, user, password, port)` | 연결 | 1=성공, 0=실패 |
| `close()` | 연결 종료 | 1=성공, 0=실패 |
| `isConnected()` | 연결 상태 확인 | 1 또는 0 |
| `getSessionId()` | 세션 ID | 정수 |
| `execute(sql)` | SQL 실행 | 1=성공, 0=실패 |
| `select(sql)` | SELECT 실행 | 1=성공, 0=실패 |
| `fetch()` | 행 가져오기 | (rc, json_str) |
| `selectClose()` | 결과셋 닫기 | 1=성공, 0=실패 |
| `result()` | 결과 메시지 | JSON 문자열 |
| `count()` | 행 개수 | 정수 |
| `append(table, types, values)` | 데이터 추가 | 1=성공, 0=실패 |

#### 연결 정보

- **기본 호스트**: 127.0.0.1
- **기본 포트**: 5656
- **기본 계정**: SYS / MANAGER

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 예제 제공 |
| 정확성 | 0점 | 공식 문서 기반 |
| 코드 품질 | 0점 | 실행 가능한 코드 |
| **총점** | **10점** | |

---

## 질문 14: 1분 단위로 저장된 비트코인 데이터 테이블에서, 5분 단위로 리샘플링하여 평균값과 최대값을 계산하는 실행 가능한 TQL 예제 한 개만 알려줘

### 답변
**응답시간: 약 2초**

비트코인 테이블의 1분 데이터를 5분 단위로 리샘플링하는 TQL 예제입니다.

#### 실행 가능한 TQL 코드

```js
SQL(`
    SELECT 
        time,
        value
    FROM BITCOIN
    WHERE name = 'BTC-trade_price'
        AND time >= '2024-12-05 18:00:00'
        AND time < '2024-12-05 20:00:00'
    ORDER BY time
`)

// Resample to 5-minute intervals
SCRIPT({
    var buckets = {};
},{
    var ts = $.values[0].Unix();
    var value = $.values[1];
    
    // Round to 5-minute bucket (300 seconds)
    var bucket = Math.floor(ts / 300) * 300;
    
    if (!buckets[bucket]) {
        buckets[bucket] = {
            values: [],
            sum: 0,
            max: value,
            count: 0
        };
    }
    
    buckets[bucket].values.push(value);
    buckets[bucket].sum += value;
    buckets[bucket].max = Math.max(buckets[bucket].max, value);
    buckets[bucket].count++;
},{
    // Output results
    for (var bucket in buckets) {
        var data = buckets[bucket];
        var avg = data.sum / data.count;
        var bucketTime = new Date(parseInt(bucket) * 1000).toISOString();
        
        $.yield(bucketTime, avg.toFixed(2), data.max.toFixed(2), data.count);
    }
})

CSV()
```

#### 실행 결과 (샘플)

```csv
time,avg_price,max_price,count
2024-12-05T09:00:00.000Z,144169993.33,144235850.00,5
2024-12-05T09:05:00.000Z,144170533.33,144281833.33,5
2024-12-05T09:10:00.000Z,144522966.67,144674800.00,5
2024-12-05T09:15:00.000Z,144636136.67,144684183.33,5
2024-12-05T09:20:00.000Z,144494653.33,144555300.00,5
2024-12-05T09:25:00.000Z,144348720.00,144360700.00,5
2024-12-05T09:30:00.000Z,144314623.33,144350833.33,5
...
```

#### 코드 설명

**1. SQL 부분:**
- `BTC-trade_price` 데이터 조회
- 2시간 범위 지정 (18:00~20:00)
- 시간 순 정렬

**2. SCRIPT 초기화:**
```js
var buckets = {};  // 5분 버킷 저장
```

**3. 데이터 처리:**
```js
var ts = $.values[0].Unix();  // Unix timestamp
var bucket = Math.floor(ts / 300) * 300;  // 5분(300초) 단위로 버킷 생성
```

**4. 집계:**
- `sum`: 합계 계산 → 평균 산출
- `max`: 최대값 추적
- `count`: 레코드 수 카운트

**5. 결과 출력:**
- ISO 시간 형식 변환
- 평균값: `sum / count`
- 최대값: `max`
- 데이터 수: `count`

#### 차트 시각화 버전

```js
SQL(`
    SELECT time, value
    FROM BITCOIN
    WHERE name = 'BTC-trade_price'
        AND time >= '2024-12-05 18:00:00'
        AND time < '2024-12-05 20:00:00'
    ORDER BY time
`)

SCRIPT({
    var buckets = {};
},{
    var ts = $.values[0].Unix();
    var value = $.values[1];
    var bucket = Math.floor(ts / 300) * 300;
    
    if (!buckets[bucket]) {
        buckets[bucket] = {
            sum: 0,
            max: value,
            min: value,
            count: 0
        };
    }
    
    buckets[bucket].sum += value;
    buckets[bucket].max = Math.max(buckets[bucket].max, value);
    buckets[bucket].min = Math.min(buckets[bucket].min, value);
    buckets[bucket].count++;
},{
    var results = [];
    for (var bucket in buckets) {
        var data = buckets[bucket];
        var avg = data.sum / data.count;
        var bucketTime = new Date(parseInt(bucket) * 1000);
        
        results.push([bucketTime, avg, data.max, data.min]);
    }
    
    // Sort by time
    results.sort((a, b) => a[0] - b[0]);
    
    for (var r of results) {
        $.yield(r[0], r[1], r[2], r[3]);
    }
})

CHART(
    size("900px", "500px"),
    chartOption({
        title: { text: "Bitcoin Price - 5 Minute Resampling" },
        xAxis: { 
            type: "time",
            data: column(0)
        },
        yAxis: { 
            name: "Price (KRW)",
            scale: true
        },
        legend: { bottom: 10 },
        tooltip: { 
            trigger: "axis",
            axisPointer: { type: "cross" }
        },
        series: [
            { 
                type: "line", 
                name: "Avg", 
                data: column(1),
                smooth: true
            },
            { 
                type: "line", 
                name: "Max", 
                data: column(2),
                lineStyle: { type: "dashed" }
            },
            { 
                type: "line", 
                name: "Min", 
                data: column(3),
                lineStyle: { type: "dashed" }
            }
        ]
    })
)
```

**검증:** 실제 실행 결과 24개 5분 버킷 생성 확인

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 리샘플링 로직 |
| 정확성 | 0점 | 정확한 5분 버킷 계산 |
| 코드 품질 | 0점 | 실행 검증 완료 |
| **총점** | **10점** | |

---

## 질문 15: Machbase Neo에서 외부 API 데이터를 가져와서 시각화 하는 예제 알려줘

### 답변
**응답시간: 약 3초**

Machbase Neo에서 외부 API 데이터를 가져와서 시각화하는 방법입니다.

#### 방법 1: HTTP 모듈 사용 (권장)

```js
SCRIPT({
    const http = require("@jsh/http");
    const client = new http.Client();
    
    // 외부 API 호출
    client.do("https://api.coindesk.com/v1/bpi/currentprice.json", 
        { method: "GET" }, 
        (rsp) => {
            if (rsp.error()) {
                $.yield("Error", rsp.error());
            } else {
                var data = JSON.parse(rsp.text());
                
                // 비트코인 가격 추출
                var usdPrice = parseFloat(data.bpi.USD.rate.replace(/,/g, ''));
                var eurPrice = parseFloat(data.bpi.EUR.rate.replace(/,/g, ''));
                var gbpPrice = parseFloat(data.bpi.GBP.rate.replace(/,/g, ''));
                
                $.yield("USD", usdPrice.toFixed(2));
                $.yield("EUR", eurPrice.toFixed(2));
                $.yield("GBP", gbpPrice.toFixed(2));
            }
        }
    );
})

CHART(
    chartOption({
        title: { text: "Current Bitcoin Price from CoinDesk API" },
        xAxis: { 
            type: "category", 
            data: column(0)
        },
        yAxis: { 
            name: "Price"
        },
        series: [
            {
                type: "bar",
                data: column(1),
                label: {
                    show: true,
                    position: "top"
                },
                itemStyle: {
                    color: "#5470C6"
                }
            }
        ],
        tooltip: {
            trigger: "axis"
        }
    })
)
```

#### 방법 2: 로컬 Machbase API 사용

```js
SCRIPT({
    const http = require("@jsh/http");
    const client = new http.Client();
    
    // Machbase Neo 자체 API 호출
    client.do(
        "http://127.0.0.1:5654/db/query",
        { 
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "q": "SELECT name, AVG(value) as avg_value FROM BITCOIN WHERE name LIKE 'BTC-%' GROUP BY name LIMIT 5",
                "format": "json"
            })
        },
        (rsp) => {
            if (rsp.error()) {
                $.yield("Error", rsp.error());
            } else {
                var result = JSON.parse(rsp.text());
                var rows = result.data.rows;
                
                for (var row of rows) {
                    $.yield(row[0], row[1]);
                }
            }
        }
    );
})

CHART(
    chartOption({
        title: { text: "Bitcoin Metrics - Average Values" },
        xAxis: { 
            type: "category", 
            data: column(0),
            axisLabel: {
                interval: 0,
                rotate: 45
            }
        },
        yAxis: { 
            name: "Average Value",
            type: "log"
        },
        series: [
            {
                type: "bar",
                data: column(1)
            }
        ]
    })
)
```

#### 방법 3: HTTP() 함수 사용

```js
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=SELECT * FROM BITCOIN WHERE name='BTC-trade_price' LIMIT 100
        &format=csv
        &timeformat=default
})

TEXT()
```

#### 방법 4: 날씨 API 예제

```js
SCRIPT({
    const http = require("@jsh/http");
    const client = new http.Client();
    
    // OpenWeatherMap API (API 키 필요)
    var apiKey = "YOUR_API_KEY";
    var city = "Seoul";
    var url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    
    client.do(url, { method: "GET" }, (rsp) => {
        if (rsp.error()) {
            $.yield("Error", "Failed to fetch weather data");
        } else {
            var data = JSON.parse(rsp.text());
            
            $.yield("Temperature", data.main.temp);
            $.yield("Feels Like", data.main.feels_like);
            $.yield("Humidity", data.main.humidity);
            $.yield("Pressure", data.main.pressure);
            $.yield("Wind Speed", data.wind.speed);
        }
    });
})

CHART(
    chartOption({
        title: { 
            text: "Seoul Weather Data",
            subtext: "Real-time from OpenWeatherMap API"
        },
        xAxis: { 
            type: "category", 
            data: column(0)
        },
        yAxis: {},
        series: [
            {
                type: "bar",
                data: column(1),
                label: {
                    show: true,
                    position: "top"
                }
            }
        ]
    })
)
```

#### 방법 5: REST API 데이터를 DB에 저장 후 시각화

```js
SCRIPT({
    const http = require("@jsh/http");
    const client = new http.Client();
    const db = require("@jsh/db");
    
    // API에서 데이터 가져오기
    client.do("https://api.example.com/data", { method: "GET" }, (rsp) => {
        if (!rsp.error()) {
            var data = JSON.parse(rsp.text());
            
            // DB에 저장
            var dbClient = new db.Client();
            var conn = dbClient.connect();
            
            for (var item of data.items) {
                var sql = `INSERT INTO api_data VALUES ('${item.name}', NOW(), ${item.value})`;
                conn.exec(sql);
            }
            
            conn.close();
        }
    });
})

// 저장된 데이터 조회 및 시각화
SQL(`SELECT name, value FROM api_data ORDER BY time DESC LIMIT 10`)

CHART(
    chartOption({
        title: { text: "API Data Stored in DB" },
        xAxis: { type: "category", data: column(0) },
        yAxis: {},
        series: [{ type: "line", data: column(1) }]
    })
)
```

#### HTTP Client 주요 기능

| 기능 | 설명 |
|------|------|
| `client.do(url, options, callback)` | HTTP 요청 |
| `rsp.text()` | 응답 텍스트 |
| `rsp.status` | HTTP 상태 코드 |
| `rsp.headers` | 응답 헤더 |
| `rsp.error()` | 에러 메시지 |

#### 지원 HTTP 메서드

- GET
- POST
- PUT
- DELETE
- PATCH

**참고:** 네트워크 설정에 따라 외부 API 접근이 제한될 수 있습니다.

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 다양한 예제 제공 |
| 정확성 | 0점 | 정확한 HTTP 모듈 사용법 |
| 코드 품질 | 1점 | 실용적인 예제 |
| **총점** | **9점** | |

---

## 질문 16: Machbase 에서 활용가능한 데이터 테이블의 종류와 각 테이블에 대한 간략한 설명 알려줘

### 답변
**응답시간: 약 1초**

Machbase Neo에서 사용 가능한 4가지 테이블 종류입니다.

#### 1. TAG 테이블 (Tag Tables)

**용도:** 센서/디바이스 시계열 데이터

**특징:**
- 시계열 데이터에 최적화
- TAG(센서ID) + TIME + VALUE 구조
- Rollup 기능 지원
- 초고속 데이터 수집 및 조회

**생성 문법:**
```sql
CREATE TAG TABLE sensor_data (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
);
```

**활용 사례:**
- IoT 센서 데이터
- 주식 시세 데이터
- 네트워크 모니터링
- 비트코인 가격 데이터

#### 2. LOG 테이블 (Log Tables)

**용도:** 이벤트 스트림 및 로그 데이터

**특징:**
- 유연한 스키마
- 빠른 INSERT 성능
- 다양한 인덱스 지원
- 텍스트 검색 가능

**생성 문법:**
```sql
CREATE TABLE app_logs (
    log_time DATETIME,
    level VARCHAR(10),
    message VARCHAR(1000),
    user_id INTEGER
);
```

**활용 사례:**
- 애플리케이션 로그
- 시스템 이벤트
- 웹 액세스 로그
- 트랜잭션 기록

#### 3. VOLATILE 테이블 (Volatile Tables)

**용도:** 인메모리 실시간 데이터

**특징:**
- 메모리에만 저장 (디스크 미사용)
- 초고속 읽기/쓰기
- 서버 재시작 시 데이터 소실
- 세션 데이터 저장

**생성 문법:**
```sql
CREATE VOLATILE TABLE realtime_cache (
    session_id VARCHAR(50) PRIMARY KEY,
    last_access DATETIME,
    data VARCHAR(500)
);
```

**활용 사례:**
- 실시간 캐시
- 세션 관리
- 임시 계산 결과
- 실시간 대시보드 데이터

#### 4. LOOKUP 테이블 (Lookup Tables)

**용도:** 참조 및 마스터 데이터

**특징:**
- 정적 데이터 저장
- 빠른 조회 성능
- JOIN 최적화
- 설정 데이터 관리

**생성 문법:**
```sql
CREATE LOOKUP TABLE device_registry (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(100),
    install_date DATETIME
);
```

**활용 사례:**
- 디바이스 레지스트리
- 설정 정보
- 코드 테이블
- 지역 정보

#### 테이블 종류 비교

| 테이블 타입 | 저장 위치 | 성능 | 지속성 | 주요 용도 |
|------------|----------|------|--------|----------|
| TAG | 디스크 | 매우 빠름 | 영구 | 시계열 센서 데이터 |
| LOG | 디스크 | 빠름 | 영구 | 이벤트/로그 |
| VOLATILE | 메모리 | 초고속 | 휘발성 | 실시간 캐시 |
| LOOKUP | 디스크 | 빠름 | 영구 | 참조 데이터 |

#### 선택 가이드

**TAG 테이블 선택 시기:**
- 센서 데이터 (ID, 시간, 값)
- 시간 기반 집계 필요
- Rollup 기능 필요
- 초당 수만 건 이상 INSERT

**LOG 테이블 선택 시기:**
- 다양한 컬럼 구조
- 유연한 스키마 필요
- 로그/이벤트 데이터
- 텍스트 검색 필요

**VOLATILE 테이블 선택 시기:**
- 실시간 성능 중요
- 데이터 지속성 불필요
- 캐시 용도
- 세션 관리

**LOOKUP 테이블 선택 시기:**
- 변경 빈도 낮음
- 참조 데이터
- 마스터 데이터
- 설정 정보

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 구분 및 설명 |
| 정확성 | 0점 | 정확한 테이블 종류 |
| 코드 품질 | 0점 | 실행 가능한 예제 |
| **총점** | **10점** | |

---

## 질문 17: Machbase의 시스템 메타 테이블에 대한 설명 해줘

### 답변
**응답시간: 약 2초**

Machbase Neo의 시스템 메타 테이블은 데이터베이스의 스키마 정보를 제공하는 특수 테이블입니다.

#### 메타 테이블 개요

메타 테이블은 `M$`로 시작하는 이름을 가지며, 테이블, 컬럼, 인덱스 등의 메타데이터를 저장합니다.

**특징:**
- 사용자가 직접 수정 불가
- DDL 실행 시 자동 업데이트
- SELECT 쿼리로 조회 가능

#### 주요 메타 테이블

### 1. M$SYS_TABLES

사용자가 생성한 테이블 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| NAME | 테이블 이름 |
| TYPE | 테이블 타입<br>0: Log, 1: Fixed, 3: Volatile, 4: Lookup, 6: Tag |
| DATABASE_ID | 데이터베이스 식별자 |
| ID | 테이블 식별자 |
| USER_ID | 생성자 ID |
| COLCOUNT | 컬럼 수 |
| FLAG | 테이블 분류<br>1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat |

**사용 예:**
```sql
-- 모든 테이블 조회
SELECT NAME, TYPE, COLCOUNT FROM M$SYS_TABLES;

-- TAG 테이블만 조회
SELECT NAME FROM M$SYS_TABLES WHERE TYPE = 6;
```

### 2. M$SYS_COLUMNS

테이블의 컬럼 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| NAME | 컬럼 이름 |
| TYPE | 컬럼 타입 |
| DATABASE_ID | 데이터베이스 식별자 |
| ID | 컬럼 식별자 |
| LENGTH | 컬럼 길이 |
| TABLE_ID | 소속 테이블 ID |
| FLAG | 내부 사용 정보 |

**사용 예:**
```sql
-- 특정 테이블의 컬럼 조회
SELECT c.NAME, c.TYPE, c.LENGTH
FROM M$SYS_COLUMNS c
JOIN M$SYS_TABLES t ON c.TABLE_ID = t.ID
WHERE t.NAME = 'BITCOIN';
```

### 3. M$SYS_INDEXES

사용자가 생성한 인덱스 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| NAME | 인덱스 이름 |
| TYPE | 인덱스 타입 |
| DATABASE_ID | 데이터베이스 식별자 |
| ID | 인덱스 식별자 |
| TABLE_ID | 소속 테이블 ID |
| COLCOUNT | 인덱스 컬럼 수 |
| BLOOM_FILTER | Bloom Filter 사용 여부 |

**사용 예:**
```sql
-- 테이블별 인덱스 조회
SELECT i.NAME, i.TYPE, t.NAME as TABLE_NAME
FROM M$SYS_INDEXES i
JOIN M$SYS_TABLES t ON i.TABLE_ID = t.ID;
```

### 4. M$SYS_INDEX_COLUMNS

인덱스를 구성하는 컬럼 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| INDEX_ID | 인덱스 식별자 |
| INDEX_TYPE | 인덱스 타입 |
| NAME | 컬럼 이름 |
| COL_ID | 컬럼 식별자 |
| TABLE_ID | 테이블 식별자 |
| TYPE | 컬럼 데이터 타입 |

### 5. M$SYS_TABLESPACES

테이블스페이스 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| NAME | 테이블스페이스 이름 |
| ID | 테이블스페이스 식별자 |
| DISK_COUNT | 디스크 수 |

**사용 예:**
```sql
-- 테이블스페이스 목록
SELECT NAME, DISK_COUNT FROM M$SYS_TABLESPACES;
```

### 6. M$SYS_TABLESPACE_DISKS

테이블스페이스의 디스크 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| NAME | 디스크 이름 |
| ID | 디스크 식별자 |
| TABLESPACE_ID | 소속 테이블스페이스 ID |
| PATH | 디스크 경로 |
| IO_THREAD_COUNT | IO 스레드 수 |

### 7. M$SYS_USERS

등록된 사용자 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| USER_ID | 사용자 식별자 |
| NAME | 사용자 이름 |

**사용 예:**
```sql
-- 사용자 목록
SELECT USER_ID, NAME FROM M$SYS_USERS;
```

### 8. M$RETENTION

Retention Policy 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| USER_ID | 사용자 ID |
| POLICY_NAME | 정책 이름 |
| DURATION | 보관 기간 (초) |
| INTERVAL | 갱신 주기 (초) |

**사용 예:**
```sql
-- Retention Policy 조회
SELECT POLICY_NAME, DURATION, INTERVAL FROM M$RETENTION;
```

### 9. M$SYS_TABLE_PROPERTY

테이블별 속성 정보

**컬럼:**
| 컬럼명 | 설명 |
|--------|------|
| ID | 테이블 식별자 |
| NAME | 속성 이름 |
| VALUE | 속성 값 |

#### 기타 메타 테이블

### M$TABLES

모든 메타 테이블 목록 (`M$`로 시작)

### M$COLUMNS

메타 테이블의 컬럼 정보

#### 실용적인 쿼리 예제

**1. 데이터베이스 스키마 전체 개요:**
```sql
SELECT 
    t.NAME as TABLE_NAME,
    CASE t.TYPE
        WHEN 0 THEN 'LOG'
        WHEN 3 THEN 'VOLATILE'
        WHEN 4 THEN 'LOOKUP'
        WHEN 6 THEN 'TAG'
    END as TABLE_TYPE,
    t.COLCOUNT as COLUMNS,
    COUNT(i.ID) as INDEX_COUNT
FROM M$SYS_TABLES t
LEFT JOIN M$SYS_INDEXES i ON t.ID = i.TABLE_ID
GROUP BY t.NAME, t.TYPE, t.COLCOUNT;
```

**2. 특정 테이블의 상세 정보:**
```sql
-- 테이블 정보
SELECT * FROM M$SYS_TABLES WHERE NAME = 'BITCOIN';

-- 컬럼 정보
SELECT c.NAME, c.TYPE, c.LENGTH
FROM M$SYS_COLUMNS c
JOIN M$SYS_TABLES t ON c.TABLE_ID = t.ID
WHERE t.NAME = 'BITCOIN';

-- 인덱스 정보
SELECT i.NAME, i.TYPE
FROM M$SYS_INDEXES i
JOIN M$SYS_TABLES t ON i.TABLE_ID = t.ID
WHERE t.NAME = 'BITCOIN';
```

**3. 사용자별 테이블 통계:**
```sql
SELECT 
    u.NAME as USER_NAME,
    COUNT(t.ID) as TABLE_COUNT
FROM M$SYS_USERS u
LEFT JOIN M$SYS_TABLES t ON u.USER_ID = t.USER_ID
GROUP BY u.NAME;
```

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 체계적인 메타 테이블 설명 |
| 정확성 | 2점 | 정확한 컬럼 정의 |
| 코드 품질 | 0점 | 실용적인 쿼리 예제 |
| **총점** | **8점** | |

---

## 질문 18: Machbase의 Tablespace 개념과 디스크 관리 방법을 설명 해줘

### 답변
**응답시간: 약 2초**

**참고:** 이 질문은 DBMS 내부 구조에 관한 것으로, 일반 사용자가 직접 관리하는 경우는 드뭅니다. Machbase Neo는 대부분의 테이블스페이스 관리를 자동으로 처리합니다.

#### Tablespace 개념

**Tablespace**는 데이터가 물리적으로 저장되는 디스크 공간의 논리적 그룹입니다.

**주요 특징:**
- 하나 이상의 디스크로 구성
- 테이블 데이터의 저장 위치 결정
- 디스크 I/O 성능 최적화
- 저장 공간 관리

#### Tablespace 조회

**1. 테이블스페이스 목록:**
```sql
SELECT NAME, ID, DISK_COUNT 
FROM M$SYS_TABLESPACES;
```

**2. 디스크 정보:**
```sql
SELECT 
    d.NAME as DISK_NAME,
    d.PATH as DISK_PATH,
    d.IO_THREAD_COUNT,
    t.NAME as TABLESPACE_NAME
FROM M$SYS_TABLESPACE_DISKS d
JOIN M$SYS_TABLESPACES t ON d.TABLESPACE_ID = t.ID;
```

#### 디스크 관리 방법

**일반적으로 Machbase Neo는 자동으로 디스크를 관리**하지만, 필요한 경우 수동 설정이 가능합니다.

**관리 항목:**
1. 디스크 경로 설정
2. IO 스레드 할당
3. 가상 디스크 구성
4. 용량 모니터링

#### Machbase Neo의 기본 디스크 구조

```
machbase-neo/
├── dbs/              # 데이터베이스 파일
│   ├── meta/        # 메타데이터
│   ├── log/         # LOG 테이블 데이터
│   ├── tag/         # TAG 테이블 데이터
│   └── lookup/      # LOOKUP 테이블 데이터
└── trc/             # 로그 파일
```

#### 스토리지 최적화 팁

**1. 데이터 분산:**
- 여러 디스크에 데이터 분산
- RAID 구성 활용
- SSD 사용 권장

**2. 파티셔닝:**
- 시간 기반 파티셔닝
- TAG 테이블의 자동 파티셔닝
- 오래된 데이터 아카이빙

**3. 용량 모니터링:**
```bash
# 데이터베이스 크기 확인
du -sh machbase-neo/dbs/

# 테이블별 크기 확인 (TQL 사용)
```

```sql
-- 테이블 통계
SELECT * FROM M$SYS_TABLES;
```

**4. 데이터 정리:**
- Retention Policy 활용
- DELETE 문으로 오래된 데이터 삭제
- VACUUM (해당되는 경우)

#### 실무 권장 사항

**1. 기본 설정 사용:**
- Machbase Neo의 기본 설정 사용 권장
- 특별한 요구사항 없으면 수동 설정 불필요

**2. 모니터링:**
- 디스크 사용량 주기적 확인
- 성능 병목 지점 파악

**3. 백업:**
- 정기적인 백업 수행
- 중요 데이터는 별도 저장소에 백업

**참고:** Machbase Neo는 엔터프라이즈 DBMS인 Machbase의 경량 버전으로, 복잡한 테이블스페이스 관리보다는 사용 편의성에 초점을 맞추고 있습니다.

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 명확한 개념 설명 |
| 정확성 | 0점 | 정확한 정보 제공 |
| 코드 품질 | 0점 | 실용적인 쿼리 |
| **총점** | **10점** | |

---

## 질문 19: 'test' 계정을 생성하고, 특정 테이블(sensor_data)에는 조회만 가능하도록 권한을 부여 하는 방법 알려줘

### 답변
**응답시간: 약 2초**

사용자 계정을 생성하고 특정 테이블에 조회 권한만 부여하는 방법입니다.

#### 1단계: 사용자 생성

```sql
-- 'test' 사용자 생성
CREATE USER test IDENTIFIED BY 'test_password';
```

#### 2단계: 테이블 생성 (예제용)

```sql
-- sensor_data 테이블 생성 (SYS 계정으로)
CREATE TABLE sensor_data (
    sensor_id VARCHAR(50),
    timestamp DATETIME,
    temperature DOUBLE,
    humidity DOUBLE
);

-- 샘플 데이터 삽입
INSERT INTO sensor_data VALUES ('SENSOR_001', NOW(), 25.5, 60.2);
INSERT INTO sensor_data VALUES ('SENSOR_002', NOW(), 26.1, 58.7);
```

#### 3단계: 조회 권한 부여

```sql
-- SELECT 권한만 부여
GRANT SELECT ON sensor_data TO test;
```

#### 전체 프로세스 예제

```sql
-- ============================================
-- 1. SYS 계정으로 연결
-- ============================================

-- 사용자 생성
CREATE USER test IDENTIFIED BY 'test_password';

-- 테이블 생성
CREATE TABLE sensor_data (
    sensor_id VARCHAR(50),
    timestamp DATETIME,
    temperature DOUBLE,
    humidity DOUBLE
);

-- 데이터 삽입
INSERT INTO sensor_data VALUES ('SENSOR_001', NOW(), 25.5, 60.2);
INSERT INTO sensor_data VALUES ('SENSOR_002', NOW(), 26.1, 58.7);
INSERT INTO sensor_data VALUES ('SENSOR_003', NOW(), 24.8, 62.1);

-- SELECT 권한 부여
GRANT SELECT ON sensor_data TO test;

-- ============================================
-- 2. test 계정으로 연결
-- ============================================

-- 연결 방법 (machbase-neo shell)
-- machbase-neo shell --user test --password test_password

-- 조회 가능 (성공)
SELECT * FROM sensor_data;

-- 삽입 시도 (실패 - 권한 없음)
INSERT INTO sensor_data VALUES ('SENSOR_004', NOW(), 27.0, 55.5);
-- [ERR-02113: No grant to execute. (INSERT)]

-- 삭제 시도 (실패 - 권한 없음)
DELETE FROM sensor_data WHERE sensor_id = 'SENSOR_001';
-- [ERR-02113: No grant to execute. (DELETE)]

-- 수정 시도 (실패 - 권한 없음)
UPDATE sensor_data SET temperature = 30.0 WHERE sensor_id = 'SENSOR_001';
-- [ERR-02113: No grant to execute. (UPDATE)]
```

#### 권한 관리 추가 명령

**권한 조회:**
```sql
-- 시스템 테이블에서 권한 확인 (SYS 계정으로)
SELECT * FROM M$SYS_USERS WHERE NAME = 'TEST';
```

**권한 회수:**
```sql
-- SELECT 권한 회수
REVOKE SELECT ON sensor_data FROM test;
```

**추가 권한 부여:**
```sql
-- INSERT 권한 추가
GRANT INSERT ON sensor_data TO test;

-- UPDATE 권한 추가
GRANT UPDATE ON sensor_data TO test;

-- DELETE 권한 추가
GRANT DELETE ON sensor_data TO test;

-- 모든 권한 부여
GRANT ALL ON sensor_data TO test;
```

#### Python 연결 예제 (test 계정)

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    
    # test 계정으로 연결
    if db.open('127.0.0.1', 'test', 'test_password', 5656) == 0:
        raise SystemExit(db.result())
    
    print('Connected as test user')
    
    try:
        # SELECT 실행 (성공)
        if db.select('SELECT * FROM sensor_data') == 0:
            raise SystemExit(db.result())
        
        print(f'Rows: {db.count()}')
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print(payload)
        
        db.selectClose()
        
        # INSERT 시도 (실패)
        sql = "INSERT INTO sensor_data VALUES ('SENSOR_004', NOW(), 27.0, 55.5)"
        if db.execute(sql) == 0:
            print('INSERT failed:', db.result())
        
    finally:
        db.close()

if __name__ == '__main__':
    main()
```

#### 계정 관리 명령

**비밀번호 변경:**
```sql
-- SYS 계정으로 다른 사용자 비밀번호 변경
ALTER USER test IDENTIFIED BY 'new_password';

-- 자신의 비밀번호 변경 (test 계정으로)
ALTER USER test IDENTIFIED BY 'my_new_password';
```

**사용자 삭제:**
```sql
-- test 사용자 삭제
DROP USER test;
```

#### 보안 권장 사항

1. **강력한 비밀번호 사용**
   - 대소문자, 숫자, 특수문자 조합
   - 최소 8자 이상

2. **최소 권한 원칙**
   - 필요한 권한만 부여
   - 정기적인 권한 검토

3. **계정 모니터링**
   - 로그인 기록 확인
   - 비정상 활동 감지

4. **기본 계정 보호**
   - SYS 계정 비밀번호 즉시 변경
   - SYS 계정 직접 사용 최소화

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 단계별 명확한 설명 |
| 정확성 | 1점 | 정확한 SQL 문법 |
| 코드 품질 | 0점 | 실행 가능한 예제 |
| **총점** | **9점** | |

---

## 질문 20: 센서 데이터를 7일만 보관하고 자동 삭제하려면 Retention Policy를 어떻게 생성하고 적용해야하는지 알려줘

### 답변
**응답시간: 약 2초**

센서 데이터를 7일 동안만 보관하는 Retention Policy 설정 방법입니다.

#### 1단계: Retention Policy 생성

```sql
-- 7일 보관, 1시간마다 확인
CREATE RETENTION sensor_7day_retention 
DURATION 7 DAY 
INTERVAL 1 HOUR;
```

**파라미터 설명:**
- `sensor_7day_retention`: Policy 이름
- `DURATION 7 DAY`: 7일 동안 데이터 보관
- `INTERVAL 1 HOUR`: 1시간마다 확인 및 삭제 수행

#### 2단계: 센서 테이블 생성

```sql
-- TAG 테이블 생성 (센서 데이터용)
CREATE TAG TABLE sensor_readings (
    sensor_id VARCHAR(50) PRIMARY KEY,
    measurement_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    humidity DOUBLE SUMMARIZED
);
```

#### 3단계: Retention Policy 적용

```sql
-- 테이블에 Retention Policy 적용
ALTER TABLE sensor_readings ADD RETENTION sensor_7day_retention;
```

#### 4단계: 상태 확인

```sql
-- Retention Policy 목록 확인
SELECT * FROM M$RETENTION;

-- 결과:
-- USER_ID | POLICY_NAME            | DURATION | INTERVAL
-- --------|------------------------|----------|----------
-- 1       | SENSOR_7DAY_RETENTION  | 604800   | 3600
```

**참고:**
- DURATION: 604800초 = 7일
- INTERVAL: 3600초 = 1시간

```sql
-- 적용된 Retention Job 확인
SELECT * FROM V$RETENTION_JOB;

-- 결과:
-- USER_NAME | TABLE_NAME       | POLICY_NAME           | STATE   | LAST_DELETED_TIME
-- ----------|------------------|------------------------|---------|-------------------
-- SYS       | SENSOR_READINGS  | SENSOR_7DAY_RETENTION | WAITING | NULL
```

#### 완전한 예제

```sql
-- ============================================
-- 전체 프로세스
-- ============================================

-- 1. Retention Policy 생성
CREATE RETENTION sensor_7day_retention 
DURATION 7 DAY 
INTERVAL 1 HOUR;

-- 2. 센서 테이블 생성
CREATE TAG TABLE sensor_readings (
    sensor_id VARCHAR(50) PRIMARY KEY,
    measurement_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    humidity DOUBLE SUMMARIZED
);

-- 3. 테스트 데이터 삽입
INSERT INTO sensor_readings VALUES ('TEMP_01', NOW(), 25.5, 60.0);
INSERT INTO sensor_readings VALUES ('TEMP_01', NOW() - INTERVAL '8' DAY, 22.0, 55.0);
INSERT INTO sensor_readings VALUES ('TEMP_01', NOW() - INTERVAL '10' DAY, 20.5, 58.0);

-- 4. Retention Policy 적용
ALTER TABLE sensor_readings ADD RETENTION sensor_7day_retention;

-- 5. 정책 확인
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'SENSOR_7DAY_RETENTION';

-- 6. Job 상태 확인
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'SENSOR_READINGS';

-- 대기 후 (1시간 후) 8일, 10일 된 데이터는 자동 삭제됨
-- 7일 이내 데이터만 남음
```

#### Retention Policy 해제

```sql
-- Retention Policy 해제
ALTER TABLE sensor_readings DROP RETENTION;
```

#### Retention Policy 삭제

```sql
-- 주의: Policy가 적용된 테이블이 있으면 삭제 불가
-- 먼저 모든 테이블에서 해제 필요

-- Policy 삭제
DROP RETENTION sensor_7day_retention;
```

#### 다양한 Retention 설정 예제

**1. 1일 보관, 30분마다 확인:**
```sql
CREATE RETENTION daily_retention 
DURATION 1 DAY 
INTERVAL 30 MINUTE;
```

**오류:** INTERVAL은 HOUR 또는 DAY 단위만 지원
```sql
-- 올바른 설정
CREATE RETENTION daily_retention 
DURATION 1 DAY 
INTERVAL 1 HOUR;
```

**2. 30일 보관, 하루에 한 번 확인:**
```sql
CREATE RETENTION monthly_retention 
DURATION 30 DAY 
INTERVAL 1 DAY;
```

**3. 1개월 보관, 3일마다 확인:**
```sql
CREATE RETENTION long_term_retention 
DURATION 1 MONTH 
INTERVAL 3 DAY;
```

**4. 90일 보관, 일주일마다 확인:**
```sql
CREATE RETENTION quarterly_retention 
DURATION 90 DAY 
INTERVAL 7 DAY;
```

#### Retention 동작 원리

```
시간 흐름 →
[─────7일─────][삭제 대상]
     ↑              ↑
  보관 영역    자동 삭제

확인 주기: 1시간마다
- 현재 시간 - 7일 이전 데이터 삭제
- 백그라운드에서 자동 실행
- 테이블 잠금 최소화
```

#### 주의사항

**1. 삭제는 비가역적:**
- 삭제된 데이터는 복구 불가
- 중요 데이터는 백업 필수

**2. INTERVAL 설정:**
- 너무 짧으면 시스템 부하
- 너무 길면 디스크 공간 낭비
- 권장: 1~6시간

**3. 여러 테이블에 동일 Policy 적용 가능:**
```sql
ALTER TABLE sensor_readings ADD RETENTION sensor_7day_retention;
ALTER TABLE device_logs ADD RETENTION sensor_7day_retention;
ALTER TABLE event_data ADD RETENTION sensor_7day_retention;
```

**4. 테이블별 다른 Policy 적용 가능:**
```sql
-- sensor_readings: 7일 보관
ALTER TABLE sensor_readings ADD RETENTION sensor_7day_retention;

-- device_logs: 30일 보관
ALTER TABLE device_logs ADD RETENTION monthly_retention;
```

#### 모니터링 쿼리

```sql
-- 1. 모든 Retention Policy 확인
SELECT 
    POLICY_NAME,
    DURATION / 86400 as DAYS,
    INTERVAL / 3600 as HOURS
FROM M$RETENTION;

-- 2. 활성 Retention Job 확인
SELECT 
    TABLE_NAME,
    POLICY_NAME,
    STATE,
    LAST_DELETED_TIME
FROM V$RETENTION_JOB;

-- 3. 특정 테이블의 데이터 보관 현황
SELECT 
    MIN(measurement_time) as oldest_data,
    MAX(measurement_time) as newest_data,
    COUNT(*) as total_records
FROM sensor_readings
WHERE sensor_id = 'TEMP_01';
```

### 평가
| 평가 항목 | 감점 | 사유 |
|-----------|------|------|
| 표현의 정확성 | 0점 | 단계별 명확한 설명 |
| 정확성 | 0점 | 정확한 Retention 문법 |
| 코드 품질 | 0점 | 실행 가능한 예제 |
| **총점** | **10점** | |

---

## 최종 종합 평가 결과 (질문 1-20)

### 전체 질문 요약

| 질문 번호 | 점수 | 응답 시간 | 주요 내용 |
|-----------|------|-----------|-----------|
| 1 | 10/10 | 약 3초 | Machbase Neo 설치 방법 |
| 2 | 10/10 | 약 3초 | 웹 UI 접속 및 기본 사용법 |
| 3 | 10/10 | 약 2초 | TQL 기본 구조 및 데이터 흐름 |
| 4 | 10/10 | 약 2초 | TAG 테이블 생성 및 활용 |
| 5 | 10/10 | 약 4초 | 시계열 데이터 집계 및 시각화 |
| 6 | 10/10 | 약 3초 | SQL 함수 (AVG, PERCENTILE_APPROX) |
| 7 | 10/10 | 약 3초 | Rollup 기능 (자동 집계) |
| 8 | 10/10 | 약 3초 | 멀티 라인 차트 시각화 |
| 9 | 10/10 | 약 3초 | TQL과 Python 통합 |
| 10 | 10/10 | 약 3초 | MQTT 데이터 수집 |
| 11 | 10/10 | 약 4초 | 비트코인 데이터 정합성 분석 |
| 12 | 10/10 | 약 3초 | 노이즈 필터 TQL (MA, LPF, Kalman) |
| 13 | 10/10 | 약 2초 | Python Machbase 연결 방법 |
| 14 | 10/10 | 약 2초 | 5분 리샘플링 TQL |
| 15 | 9/10 | 약 3초 | 외부 API 데이터 시각화 |
| 16 | 10/10 | 약 1초 | 4가지 테이블 타입 설명 |
| 17 | 8/10 | 약 2초 | 시스템 메타 테이블 |
| 18 | 10/10 | 약 2초 | Tablespace 개념 |
| 19 | 9/10 | 약 2초 | 사용자 권한 관리 |
| 20 | 10/10 | 약 2초 | Retention Policy 설정 |
| **전체 총점** | **196/200** | **평균 2.6초** | |

**전체 평가**

이전 0.5.0 버전 보다 정확성이 증가함,DBMS 관련 내용 재점검 필요한 것으로 보임. 전체 적으로 성능 및 시간이 향상됨.
