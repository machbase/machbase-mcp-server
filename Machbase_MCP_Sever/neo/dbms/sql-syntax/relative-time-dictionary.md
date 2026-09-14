# 상대 시간 표현 사전

상대 시간 표현을 사용하면 `NOW`, `SYSDATE`와 같은 기준 시점으로부터의 차이를 SQL 문 안에서 직접 기술할 수 있습니다. 별도 함수 호출 없이 시계열 윈도우를 간결하게 표현할 때 유용합니다.

> 상대 시간 리터럴(`now - 1h` 형태)은 Machbase 8.0.50 이상에서 지원됩니다. 월/연 단위 보정이 필요하면 `ADD_TIME`, 문자열 변환이 필요하면 `TO_DATE`를 사용합니다.

## 빠른 참조표

| 표현 | 예시 | 설명 |
|------|------|------|
| `NOW` / `now` | `now` | 현재 시각 (나노초 정밀도) |
| `SYSDATE` / `sysdate` | `sysdate` | 현재 시각 (`NOW`와 동일) |
| `now - offset` | `now - 1h` | 현재 시각에서 오프셋 뺄셈 |
| `now + offset` | `now + 30m` | 현재 시각에서 오프셋 덧셈 |
| 나노초 정수 직접 사용 | `value + 1000000000` | 나노초 단위 정수를 DATETIME에 더함 |

## 상대 시간 단위 (리터럴 접미사)

| 접미사 | 의미 | 예시 |
|--------|------|------|
| `ns` | 나노초 | `500ns` |
| `us` | 마이크로초 | `20us` |
| `ms` | 밀리초 | `15ms` |
| `s` | 초 | `45s` |
| `m` | 분 | `30m` |
| `h` | 시간 | `12h` |
| `d` | 일 | `7d` |
| `w` | 주 | `2w` (= 14일) |

> 월(`month`, `mo`)과 연(`year`, `y`) 접미사는 지원하지 않습니다. 달력 기준으로 한 달이나
> 한 해를 이동하려면 `ADD_TIME()`을 사용합니다. `30d`와 `365d`는 각각 고정된 일수이므로
> 달력상의 한 달·한 해와 항상 같지는 않습니다.

## ADD_TIME 함수

월·연처럼 상대 시간 리터럴에 없는 달력 보정에는 `ADD_TIME()`을 사용합니다. 인자, 형식과
오류 조건은 SQL 함수 사전을 참고하십시오.

## TO_DATE 함수

조회 구간의 시작과 끝을 날짜 문자열로 지정할 때는 `TO_DATE()`로 DATETIME 값을 만듭니다.
날짜 형식과 변환 오류는 SQL 함수 사전을 참고하십시오.

## 활용 패턴

### 시간 구간 필터링

```sql
-- 최근 1시간 데이터 (상대 시간 리터럴)
SELECT * FROM sensor_tag WHERE time > now - 1h;

-- 최근 1시간 데이터 (ADD_TIME 함수)
SELECT * FROM sensor_tag WHERE time > ADD_TIME(now, '0/0/0 -1:0:0');

-- 최근 24시간 기록
SELECT * FROM app_log WHERE _arrival_time BETWEEN now - 1d AND now;

-- 최근 10분 이내 알람
SELECT alert_id, level, occurred_at FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### 복합 시간 표현

```sql
-- 2일 6시간 15분 후
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h15m;

-- 하위 초 단위 조합
SELECT TO_CHAR(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

### TO_DATE 결과에 오프셋 적용

```sql
-- 문자열 날짜에 3일 추가
SELECT TO_CHAR(TO_DATE('2024-05-01', 'YYYY-MM-DD') + 3d, 'YYYY-MM-DD');
-- 결과: 2024-05-04

-- 문자열 날짜에서 4시간 15분 빼기
SELECT TO_CHAR(
    TO_DATE('2024-05-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS') - 4h15m,
    'YYYY-MM-DD HH24:MI:SS'
);
-- 결과: 2024-05-01 03:45:00
```

### 나노초 정수 직접 사용

숫자 리터럴은 나노초로 해석됩니다.

```sql
-- 1초 = 1,000,000,000 나노초
SELECT event_time + 1000000000 AS event_time_plus_1s FROM events;

-- 250나노초 빼기
SELECT event_time - 250 AS event_time_minus_250ns FROM events;
```

## 제한사항

- 상대 시간 리터럴(`1h`, `30m` 등)은 Machbase 8.0.50 이상에서만 지원됩니다.
- 월(`mo`)과 연(`y`) 단위는 리터럴로 지원하지 않습니다. `ADD_TIME()`의 년/월 위치를 사용합니다.
- 문자열 리터럴은 interval 산술에서 DATETIME으로 암시적 변환되지 않으므로 `TO_DATE()`로 먼저 변환해야 합니다.
- 인터벌 자체는 `ORDER BY` 절에서 사용할 수 없습니다.

## 오류 처리

| 상황 | 오류 | 해결 방법 |
|------|------|-----------|
| 지원하지 않는 접미사(`1y`, `5mo`) | `ERR-02034` invalid time expression | 달력 단위는 `ADD_TIME()`, 고정 기간은 `d` 등 지원 접미사 사용 |
| 단위 누락(`now + 10`) | 나노초로 해석됨 | 의도한 단위 접미사 명시 |
| 너무 큰 값(`1000000d`) | `ERR_OVERFLOW_INTERVAL` | 값 범위 축소 |

## LOG의 DURATION

상대 시간 리터럴과 DURATION은 역할이 다릅니다.
`event_time >= now - 1h`는 선택한 컬럼의 WHERE 조건이고,
DURATION은 LOG의 `_arrival_time` 범위를 지정합니다.
TAG의 시간 컬럼이나 사용자 DATETIME 컬럼에는 WHERE 조건을 사용하세요.

```text
SELECT ... FROM log_table
 [WHERE ...]
 DURATION n unit [BEFORE base_time | AFTER base_time]
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]

SELECT ... FROM log_table
 [WHERE ...]
 DURATION FROM from_time TO to_time
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]
```

위는 기본 형태입니다. 기간에는 `HOUR`, `MINUTE`, `DAY` 같은 단위를 사용합니다.
전체 범위를 표현하는 `ALL`도 사용할 수 있습니다.
DURATION은 WHERE 다음, GROUP BY·ORDER BY 앞에 둡니다.

| 형태 | 범위 | 지정되는 스캔 방향 |
|---|---|---|
| DURATION 1 HOUR | 현재 시각 기준 최근 1시간 | 최신 쪽부터 |
| DURATION 1 HOUR BEFORE t | t−1시간부터 t까지 | 최신 쪽부터 |
| DURATION 1 HOUR AFTER t | t부터 t+1시간까지 | 오래된 쪽부터 |
| DURATION FROM a TO b, a < b | a부터 b까지 | 오래된 쪽부터 |
| DURATION FROM a TO b, a > b | b부터 a까지 | 최신 쪽부터 |

범위의 양 끝을 포함합니다. FROM과 TO가 같은 시각이면 그 시각의 행이 대상입니다.
스캔 방향과 조인·집계 이후의 최종 출력 순서는 구분하세요.
결과 순서가 필요하면 ORDER BY를 명시하고, 같은 시각의 여러 행에는 추가 정렬 기준을 둡니다.

다음 예제에서는 끝 시각에 있는 2번 행도 선택됩니다.

```sql
CREATE LOG TABLE ch7_ref_duration (event_id INTEGER);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);

SELECT event_id FROM ch7_ref_duration
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

DROP TABLE ch7_ref_duration;
```

결과는 1·2번입니다. 일별로 연속 구간을 나눌 때는
`WHERE _arrival_time >= 시작 AND _arrival_time < 끝`처럼 반개구간을 사용하면
경계 행을 중복 집계하지 않을 수 있습니다.
LOG와 LOOKUP이 함께 있는 쿼리는 DURATION 대신 LOG 컬럼의 WHERE 범위를 사용하세요.

## 관련 문서

- LOG 시간 범위 실습 — 경계·정렬·조인 결과 비교
- 상대 시간 표현 — 8.5 레퍼런스 상세
