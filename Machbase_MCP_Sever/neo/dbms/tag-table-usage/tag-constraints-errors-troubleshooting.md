# 제약, 오류, 문제 해결

이 페이지의 UPDATE 실습은 Standard Edition을 전제로 합니다. 먼저 다음 테이블을 만들고,
정상 SQL과 의도적으로 실패하는 SQL을 구분해 실행합니다. 실패 예제를 한꺼번에 정상
스크립트에 넣지 마십시오. 이름이 겹치는 기존 객체를 삭제하지 않습니다.

```sql
CREATE TAG TABLE ch5_error_time (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    status INTEGER
) METADATA (location VARCHAR(64));
INSERT INTO ch5_error_time METADATA VALUES ('sensor-01', 'zone-1');
INSERT INTO ch5_error_time METADATA VALUES ('sensor-02', 'zone-2');
INSERT INTO ch5_error_time VALUES
    ('sensor-01', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_error_time VALUES
    ('sensor-02', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
CREATE TAG TABLE ch5_error_distance (
    name VARCHAR(64) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value DOUBLE SUMMARIZED
);
```

## TAG data UPDATE WHERE 조건 오류

WHERE 절에 태그 선택 조건과 BASETIME 조건이 모두 있어야 합니다.
조건이 모호하거나 허용되지 않는 형태이면 UPDATE가 거부됩니다.

> **주의**
> **필수 조건**
>
> `WHERE name ...` 형태의 태그 선택 조건과 `time ...` 형태의 BASETIME 조건을 함께 지정합니다.
> 조건 없는 전체 UPDATE, 태그 조건만 있는 UPDATE, 시간 조건만 있는 UPDATE는 허용되지 않습니다.

### TAG data UPDATE WHERE 조건 오류 증상

다음과 같은 UPDATE가 오류로 거부됩니다.

```sql
-- 시간 조건 없음
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01';

-- 태그 선택 조건 없음
UPDATE ch5_error_time SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- OR 조건 사용
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```

### 원인

대상 태그와 시간 범위를 명확하게 제한할 수 없는 조건은 거부됩니다.

| 조건 형태 | 지원 여부 |
|-----------|:--------:|
| `name = 'sensor-01' AND time >= ...` | O |
| `name IN ('sensor-01', 'sensor-02') AND time BETWEEN ...` | O |
| `name LIKE 'sensor-%' AND time < ...` | O |
| `value > 10`만 사용 | X |
| `name = 'sensor-01'`만 사용 | X |
| `time >= ...`만 사용 | X |
| `OR`, 서브쿼리, 집계 조건 | X |

### TAG data UPDATE WHERE 조건 오류 해결 방법

태그 선택 조건과 시간 조건을 함께 명시합니다.

```sql
UPDATE ch5_error_time
   SET value = 99.9
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE ch5_error_time
   SET status = 1
 WHERE name IN ('sensor-01', 'sensor-02')
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### NAME 또는 TIME bind가 `ERR-02190`으로 거부될 때

Machbase 8.7.0부터 Standard Edition에서는 다음과 같이 NAME과 BASETIME 조건 값에 bind
parameter를 사용할 수 있습니다.

```sql
UPDATE ch5_error_time
   SET value = ?
 WHERE name = ?
   AND time = ?;
```

태그 선택 조건과 BASETIME 조건이 모두 있는데도 이 문장이
`ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)`로
거부되면 서버 버전을 확인합니다. 구버전 서버는 TAG data UPDATE의 NAME/TIME
bind를 지원하지 않습니다. 서버를 8.7.0 이상으로 업그레이드하고, named marker를 사용하면
해당 이름 기반 API를 지원하는 8.7.0 SDK를 함께 사용합니다.

`?` 예제는 SDK에서 준비·바인딩할 SQL이며 machsql에 값 없이 그대로 실행할 문장은 아닙니다.
같은 prepared statement를 재사용할 때는 SET, NAME, TIME 값을 모두 다시 바인딩합니다.
자세한 marker 규칙은
TAG data UPDATE bind를
참고하십시오.

대량 UPDATE 전에는 같은 WHERE 조건으로 `SELECT COUNT(*)`를 실행해 수정 대상 row 수를
확인합니다.

## TAG data UPDATE SET 대상 컬럼 오류

SET 절은 실제 데이터 컬럼만 대상으로 합니다. PRIMARY KEY, BASETIME,
메타데이터 컬럼을 SET 대상으로 지정하면 오류가 발생합니다.

> **주의**
> **SET 대상**
>
> `value`와 사용자 데이터 컬럼은 UPDATE할 수 있습니다. `name`, `time`, METADATA 블록의 컬럼은
> TAG data UPDATE의 SET 대상이 아닙니다.

### TAG data UPDATE SET 대상 컬럼 오류 증상

```sql
-- 오류: PRIMARY KEY 컬럼(name) 업데이트 시도
UPDATE ch5_error_time
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: BASETIME 컬럼(time) 업데이트 시도
UPDATE ch5_error_time
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: 메타데이터 컬럼을 data UPDATE에서 수정
UPDATE ch5_error_time
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

### 컬럼 유형별 UPDATE 가능 여부

| 컬럼 유형 | 설명 | data UPDATE |
|-----------|------|:-----------:|
| PRIMARY KEY (`name`) | TAG를 식별하는 고유 키 | X |
| BASETIME (`time`) | 시계열 데이터의 타임스탬프 | X |
| 데이터 컬럼 (`value`, 보조 컬럼) | 실제 row 값 | O |
| `SUMMARIZED` 데이터 컬럼 | 통계 대상 데이터 컬럼 | O |
| 메타데이터 컬럼 | METADATA 블록의 태그 속성 | X |

### TAG data UPDATE SET 대상 컬럼 오류 해결 방법

데이터 값은 일반 UPDATE로 수정합니다.

```sql
UPDATE ch5_error_time
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

메타데이터는 별도 구문을 사용합니다.

```sql
UPDATE ch5_error_time METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```

태그 이름이나 시간 축을 변경해야 하는 경우에는 새 `name`/`time` 값으로 데이터를 삽입한 뒤
운영 정책에 따라 기존 데이터를 삭제합니다.

## BASE DISTANCE TAG STAT 컬럼 오류

Machbase 8.7.0은 BASE DISTANCE TAG의 `V$<TABLE>_STAT` 축 컬럼을 거리 이름과 숫자
타입으로 제공합니다. 업그레이드 전 SQL이 `MIN_TIME`, `MAX_TIME`, `RECENT_ROW_TIME`
등을 조회하면 컬럼을 찾을 수 없다는 오류가 발생할 수 있습니다.

### BASE DISTANCE TAG STAT 컬럼 오류 증상

- 업그레이드 후 BASE DISTANCE 통계 뷰에서 기존 `*_TIME` 컬럼을 조회할 수 없습니다.
- 구버전 서버에서는 거리값이 `DATETIME`으로 해석되어 의미 없는 날짜처럼 보일 수 있습니다.
- Cluster Edition에서 Standard와 같은 ordinal result mapping을 사용하면 선두의
  `HOSTNAME` 때문에 이후 컬럼이 어긋날 수 있습니다.

### 진단

대상 테이블의 축과 실제 통계 뷰 스키마를 함께 확인합니다.

```sql
DESC ch5_error_distance;
DESC V$CH5_ERROR_DISTANCE_STAT;
```

BASE DISTANCE 테이블이면 `MIN_DISTANCE`, `MAX_DISTANCE`, `MIN_VALUE_DISTANCE`,
`MAX_VALUE_DISTANCE`, `RECENT_ROW_DISTANCE`가 원본 거리축 타입으로 표시되어야 합니다.
Cluster Edition에서는 `HOSTNAME VARCHAR(64)`가 첫 컬럼에 추가됩니다.

### BASE DISTANCE TAG STAT 컬럼 오류 해결 방법

1. SQL의 기존 `*_TIME` 이름을 대응하는 `*_DISTANCE` 이름으로 변경합니다.
2. SDK result mapping을 `DATETIME`이 아니라 원본 `DOUBLE`, `LONG`, `ULONG` 타입으로
   변경합니다.
3. Cluster 결과는 컬럼 이름으로 읽거나 `HOSTNAME`을 포함한 ordinal을 다시 확인합니다.
4. BASE TIME TAG 쿼리는 기존 `*_TIME DATETIME` mapping을 유지합니다.

전체 변환표와 Cluster 집계 주의사항은
TAG별 통계 뷰를 참고하십시오.

## 제약 및 주의사항

### 기능 지원 범위

| 기능 | 상태 |
|------|------|
| 실제 시계열 데이터 UPDATE | Standard Edition에서 지원 (태그/BASETIME 조건 필요) |
| 메타데이터 UPDATE | 지원 (`UPDATE ... METADATA`) |
| DELETE | 지원 (`BEFORE`, 태그/축 조건 또는 전체 삭제) |
| 다중 PRIMARY KEY | 미지원 (단일 컬럼만) |
| BASETIME과 BASEDISTANCE 동시 사용 | 미지원 |
| TAG DATA 일반 컬럼 ALTER ADD/DROP | 미지원 |
| TAG METADATA 컬럼 ALTER ADD/DROP | 지원 (Standard Edition) |

### 태그 수 제한

- 단일 TAG 테이블에 생성 가능한 태그 수는 시스템 설정에 따라 제한됩니다.
- 태그 수가 늘면 태그 인덱스와 메타데이터의 메모리 사용량도 증가하므로 운영 규모의 데이터로
  조회와 입력 성능을 측정합니다.
- 태그 이름이 레코드마다 고유한 값이 되도록 설계하면 안 됩니다 (안티패턴 — 센서별 테이블 생성 참고).

### 지연 도착 데이터

- BASETIME 컬럼에는 임의의 과거 시각을 삽입할 수 있습니다.
- 늦게 도착한 데이터가 많은 워크로드는 실제 입력률과 조회 성능을 별도로 측정합니다.

### Cluster Edition 지원

TAG 테이블은 Cluster Edition에서 지원됩니다.

단, TAG data UPDATE는 Standard Edition 전용이며 Cluster Edition에서는 지원되지 않습니다.

### 요약

```
TAG 테이블 = 센서 이름 (PK) + 시간/거리 축 + 계측값
- INSERT/APPEND: O
- UPDATE: 실제 DATA는 Standard Edition의 태그/BASETIME 조건, METADATA는 별도 SQL
- DELETE: O (BEFORE 또는 태그/축 조건)
- METADATA: O (별도 속성 저장, UPDATE 가능)
```

---

**다음 읽을 내용**
- TRANSACTION 테이블 설계

## 실습 정리

정상 수정 결과는 SELECT로 확인하고 이번 실습 테이블만 제거합니다.

```sql
SELECT name, time, value, status FROM ch5_error_time ORDER BY name, time;
DROP TABLE ch5_error_time;
DROP TABLE ch5_error_distance;
```
