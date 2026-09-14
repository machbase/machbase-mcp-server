# SEQUENCE 컬럼

LOOKUP 테이블의 SEQUENCE 컬럼 설정과 활용을 다룹니다.

## LOOKUP SEQUENCE 컬럼 정의

SEQUENCE 컬럼은 `NEXTVAL`로 입력 번호를 생성할 때 사용합니다. LOOKUP 테이블은
PRIMARY KEY가 필수이므로, SEQUENCE 컬럼 자체를 PRIMARY KEY로
지정할지 다른 컬럼을 PRIMARY KEY로 둘지 함께 정합니다. 이 번호를 이벤트 발생 시각의
순서와 동일하게 해석하지 않습니다.

## SEQUENCE 컬럼이 필요한 이유

같은 시각에 발생한 알람이나 관리 이력을 서로 다른 행으로 식별해야 할 때 사용할 수
있습니다. LOOKUP은 전체 행을 메모리에 유지하므로 이 예제는 소규모 관리 이력에 해당합니다.
장기간 누적하는 대량 이벤트는 LOG 테이블을 검토합니다.

## SEQUENCE 컬럼 선언

SEQUENCE는 `LONG` 또는 `INT64` 타입 컬럼에 지정할 수 있습니다. PROPERTY 절의 `SEQUENCE`
파라미터로 시작값을 설정하며, 이 속성은 LOOKUP 테이블에서만 사용할 수 있습니다.

```sql
CREATE LOOKUP TABLE ch9_sequence (
    seq       LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id VARCHAR(40),
    alarm_type VARCHAR(20),
    occurred_at DATETIME,
    message   VARCHAR(200)
);
```

- `SEQUENCE=1`: seq 컬럼이 1부터 자동 증가
- 시작값은 1 이상 4,294,967,295 미만의 정수만 지정할 수 있습니다.
- 위 예제처럼 SEQUENCE 컬럼을 PRIMARY KEY로 지정하면 번호의 고유성까지 함께 보장됩니다.

## SEQUENCE 값 삽입: NEXTVAL()

서버는 SEQUENCE 컬럼마다 다음에 사용할 번호를 카운터로 보관하며, `NEXTVAL()`은 그 값을
가져와 삽입합니다. 매번 테이블의 최댓값을 다시 계산하지 않습니다.

```sql
-- NEXTVAL()로 자동 증가값 입력
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');

INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'PRESS-02', 'LOW', NOW, '압력 저하');

-- 조회
SELECT * FROM ch9_sequence ORDER BY seq;
-- seq=1, seq=2 순으로 정렬됨
```

## 일반 컬럼처럼 직접 값 지정

SEQUENCE 컬럼에 직접 값을 입력하는 것도 허용됩니다. 입력값이 현재 카운터보다 크면
카운터가 `입력값 + 1`로 올라갑니다. 현재 카운터보다 작은 값을 입력해도 카운터는
내려가지 않습니다.

```sql
-- 직접 값 지정 (nextval을 쓰지 않아도 됨)
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (100, 'FLOW-03', 'NORMAL', NOW, '정상 복구');

-- 이후 NEXTVAL() 호출 시 101이 됩니다
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'NORMAL', NOW, '온도 정상');
-- seq = 101
```

## 활용 패턴

```sql
-- 최신 알람 N건 조회
SELECT * FROM ch9_sequence ORDER BY seq DESC LIMIT 10;

-- 특정 seq 이후 알람 조회
SELECT * FROM ch9_sequence WHERE seq > 500 ORDER BY seq;

-- 알람 확인 처리 (PK 기준 UPDATE)
UPDATE ch9_sequence SET alarm_type = 'ACKNOWLEDGED'
WHERE seq = 101;
```

실습 테이블은 다음과 같이 정리합니다.

```sql
DROP TABLE ch9_sequence;
```

## 주의 사항

- SEQUENCE 컬럼은 `LONG`, `INT64` 타입을 지원합니다.
- 시작값은 양수(`SEQUENCE=1` 이상)만 허용되며 4,294,967,295 미만이어야 합니다.
- 카운터는 서버에 저장되고 한 방향으로만 올라갑니다. 가장 큰 seq 행을 DELETE해도 그 번호는
  다시 사용되지 않으므로, 번호가 비어 있는 구간이 생길 수 있습니다.
- SEQUENCE 컬럼을 PRIMARY KEY로 지정하지 않으면 `NEXTVAL()`을 쓰지 않고 중복 값을 직접
  입력할 수 있습니다. 번호의 고유성이 필요하면 이 컬럼을 PRIMARY KEY로 지정합니다.
