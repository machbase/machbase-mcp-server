# 인덱스와 성능

인덱스를 만들었는데도 조회가 빨라지지 않으면 먼저 쿼리가 그 인덱스를 사용할 수 있는지
확인해야 합니다. 인덱스는 읽기 비용을 줄이는 대신 입력·저장·백그라운드 처리 비용을
늘립니다. 컬럼마다 하나씩 만드는 것보다 대표 조건을 정하는 편이 출발점으로 좋습니다.

## 인덱스 선택

| 조회 조건 | 검토할 인덱스 | 확인할 점 |
|---|---|---|
| 숫자·DATETIME 등의 값과 범위 | LSM | 조건에 맞는 지원 타입과 실제 실행 계획 |
| VARCHAR·TEXT의 단어·토큰 패턴 | KEYWORD | SEARCH·ESEARCH 사용, LIKE와 결과 의미가 다름 |
| 지원 타입의 반복 값 분석 | BITMAP | 값 분포와 인코딩, 입력·저장 비용 |

LOG의 `_arrival_time` 범위는 기본 시간 접근 경로를 먼저 활용합니다.
같은 목적의 인덱스를 관성적으로 추가할 필요는 없습니다.
지원 타입과 속성은 INDEX 문법을
기준으로 확인하세요. 일반적인 RDBMS의 복합 인덱스 설계를 그대로 적용하지 마세요.

## 인덱스 생성 전후 비교

```sql
CREATE LOG TABLE ch7_index (
    event_id   INTEGER,
    event_time DATETIME,
    severity   SHORT,
    message    VARCHAR(256)
);
INSERT INTO ch7_index VALUES (
    1, TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'service started');
INSERT INTO ch7_index VALUES (
    2, TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'database timeout');
INSERT INTO ch7_index VALUES (
    3, TO_DATE('2026-01-01 10:02:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'connection timeout');

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;

CREATE INDEX ch7_index_time ON ch7_index(event_time) INDEX_TYPE LSM;
CREATE INDEX ch7_index_message ON ch7_index(message) INDEX_TYPE KEYWORD;
CREATE INDEX ch7_index_severity ON ch7_index(severity)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;

EXEC TABLE_FLUSH(ch7_index);
EXEC INDEX_FLUSH(ch7_index);

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;
EXPLAIN SELECT event_id FROM ch7_index WHERE message SEARCH 'timeout';

SELECT event_id FROM ch7_index
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;
SHOW INDEXES;
```

검색 결과는 2·3번입니다. 실행 계획에서 값 조건과 SEARCH가 사용하는 접근 경로를
비교하고, SHOW INDEXES로 생성된 이름을 확인하세요.
이 세 행은 동작을 이해하기 위한 표본이지 성능 측정 데이터는 아닙니다.

## 데이터와 인덱스 반영

`TABLE_FLUSH`는 테이블 데이터를 반영하는 작업이고, `INDEX_FLUSH`는 인덱스 빌드가
진행될 때까지 기다리는 작업입니다. 실습에서 생성 전후 계획과 시간을 비교할 때는 위처럼
구분해서 사용하세요.

인덱스가 존재하는 것과 입력된 데이터 전체의 인덱스 반영이 끝난 것은 같지 않습니다.
빌드 지연이 검색 비용에 영향을 줄 수 있습니다. 그렇다고 매 행 입력마다 두 명령을
호출하면 배치 입력의 이점을 줄이게 됩니다. 운영에서는 입력률과 백그라운드 처리 속도를
함께 관찰하고 필요한 동기화 시점만 정하세요.

실수하기 쉬운 부분은 인덱스 반영이 늦다는 이유로 같은 데이터를 재입력하는 것입니다.
재입력 전에 원본 조회 건수와 인덱스 상태를 각각 확인해야 중복을 피할 수 있습니다.

## 성능 측정 기준

생성 전후에 같은 데이터량·조건값·동시 입력 부하를 사용하세요.
한 번의 실행 시간뿐 아니라 반복 조회 시간, 입력 처리량, 인덱스 공간과 빌드 지연을
함께 기록합니다. LIKE·REGEXP는 원문 문자열에 조건을 평가하므로 먼저 시간 범위를
제한하면 검사할 대상을 줄일 수 있습니다. KEYWORD 인덱스가 있다고 LIKE가 SEARCH로
바뀌는 것은 아닙니다.

```sql
DROP INDEX ch7_index_severity;
DROP INDEX ch7_index_message;
DROP INDEX ch7_index_time;
DROP TABLE ch7_index;
```

계획을 읽기 어렵다면 쿼리와 EXPLAIN 결과를 함께 비교해 보세요.
인덱스 튜닝의 진단 순서가 다음 확인 지점을
잡는 데 도움이 됩니다.
