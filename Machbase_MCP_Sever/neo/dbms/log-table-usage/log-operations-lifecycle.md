# 운영과 데이터 생명주기

입력은 잘 되는데 디스크가 계속 늘어난다면 삭제 기준부터 확인할 차례입니다.
LOG는 업무 조건으로 특정 행을 골라 지우는 모델이 아니라, 오래된 영역부터 정리하는
모델입니다. 보관할 기간과 실제로 삭제되는 경계를 함께 확인해야 합니다.

## 삭제 방법 선택

| 목적 | 명령 | 기준 |
|---|---|---|
| 오래된 N행 삭제 | OLDEST n ROWS | 오래된 입력 행부터 |
| 최근 N행만 남김 | EXCEPT n ROWS | 남길 행 수 |
| 최근 기간만 남김 | EXCEPT n DAY 등 | 서버 현재 시각에서 기간을 뺀 경계 |
| 고정 시각까지 삭제 | BEFORE datetime_expr | 해당 _arrival_time 경계 포함 |
| 전체 데이터 삭제 | 조건 없는 DELETE 또는 TRUNCATE | 전체 행 |
| 주기적인 기간 관리 | Retention Policy | 보존 기간과 실행 주기 |

주의: 삭제는 되돌릴 수 있다고 가정하면 안 됩니다. LOG 데이터는 TRANSACTION 테이블의
ROLLBACK 대상이 아닙니다. 운영에서는 백업과 실제 대상 범위를 확인한 뒤 실행하세요.

## 삭제 방식 비교

명령을 연속해서 실행하면 앞선 삭제가 다음 결과에 영향을 줍니다.
여기서는 같은 세 행을 서로 다른 테이블에 복사해 비교하겠습니다.

```sql
CREATE LOG TABLE ch7_lifecycle (event_id INTEGER);
CREATE LOG TABLE ch7_oldest (event_id INTEGER);
CREATE LOG TABLE ch7_keep (event_id INTEGER);
CREATE LOG TABLE ch7_before (event_id INTEGER);

INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01', 'YYYY-MM-DD'), 1);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-02', 'YYYY-MM-DD'), 2);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-03', 'YYYY-MM-DD'), 3);

INSERT INTO ch7_oldest(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_keep(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_before(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;

SELECT COUNT(*) AS delete_candidates FROM ch7_before
 WHERE _arrival_time <= TO_DATE('2026-01-02', 'YYYY-MM-DD');

DELETE FROM ch7_oldest OLDEST 1 ROWS;
DELETE FROM ch7_keep EXCEPT 1 ROWS;
DELETE FROM ch7_before BEFORE TO_DATE('2026-01-02', 'YYYY-MM-DD');

SELECT event_id FROM ch7_oldest ORDER BY event_id;
SELECT event_id FROM ch7_keep ORDER BY event_id;
SELECT event_id FROM ch7_before ORDER BY event_id;
```

삭제 전 확인 건수는 2입니다. 각 테이블에 남는 이벤트는 다음과 같습니다.

| 테이블 | 남는 event_id |
|---|---|
| ch7_oldest | 2, 3 |
| ch7_keep | 3 |
| ch7_before | 3 |

실수하기 쉬운 부분은 BEFORE라는 이름입니다.
현재 LOG 삭제는 지정한 시각과 같은 행도 포함합니다.
`WHERE _arrival_time < 경계`로 사전 건수를 세면 삭제 대상과 달라질 수 있으므로
위처럼 `<=`로 확인하세요.

```sql
DELETE FROM ch7_lifecycle;
SELECT COUNT(*) AS remaining_rows FROM ch7_lifecycle;

DROP TABLE ch7_before;
DROP TABLE ch7_keep;
DROP TABLE ch7_oldest;
DROP TABLE ch7_lifecycle;
```

전체 DELETE 뒤 건수는 0이고 테이블 정의는 남습니다.

## 상대 기간 삭제

```sql
CREATE LOG TABLE ch7_period (event_id INTEGER);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE, 2);

DELETE FROM ch7_period EXCEPT 1 DAY;
SELECT event_id FROM ch7_period ORDER BY event_id;

DROP TABLE ch7_period;
```

생성부터 조회까지 바로 실행하면 2번만 남습니다.
기준은 “마지막으로 들어온 행의 시각”이 아니라 서버 현재 시각입니다.
입력이 멈춰 있어도 시간은 계속 흐른다는 점을 보존 정책에도 반영하세요.

## Retention Policy

다음은 1일 보존·1분 주기의 검증용 예제입니다.
운영 권장값이 아니며, 정책 생성과 테이블 연결에 필요한 권한이 있는 계정을 사용하세요.

```sql
CREATE LOG TABLE ch7_retention (event_id INTEGER);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE, 2);

CREATE RETENTION ch7_policy DURATION 1 DAY INTERVAL 1 MIN;
ALTER TABLE ch7_retention ADD RETENTION ch7_policy;

SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'CH7_POLICY';
SELECT TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

DURATION은 남길 기간, INTERVAL은 삭제를 실행하는 주기입니다.
연결 직후에는 두 행이 보일 수 있습니다. 한 주기와 작업 처리 시간이 지난 뒤 아래 쿼리를
다시 실행해 2번만 남는지 확인하세요. LAST_DELETED_TIME은 삭제 기준 시각이지
벽시계 기준의 작업 완료 시각이 아닙니다.

```sql
SELECT TABLE_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

실습을 마쳤으면 연결부터 해제한 뒤 정책과 테이블을 삭제합니다.

```sql
ALTER TABLE ch7_retention DROP RETENTION;
SELECT TABLE_NAME FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
DROP RETENTION ch7_policy;
DROP TABLE ch7_retention;
```

해제 후 작업 조회는 0건입니다. 이미 삭제된 행이 복원되는 것은 아닙니다.
한 테이블에는 하나의 정책을 연결하며, 사용 중인 정책은 먼저 해제해야 삭제할 수 있습니다.
전체 운영 기준은 데이터 보존 정책을
참고하세요.

## 삭제 전 백업 검증

백업 파일이 있다는 사실만으로 복구 준비가 끝나지는 않습니다.
삭제할 기간을 Mount 또는 격리된 Restore 환경에서 실제로 조회해 보세요.
원본, 백업, 별도 집계 데이터의 보관 기간도 각각 정해야 합니다.
환경별 명령은 백업·복원·마운트를
따릅니다.

## 데이터와 디스크 공간

행이 조회에서 사라지는 것과 운영체제에서 파일 공간이 회수되는 시점은 같지 않을 수
있습니다. 입력량, 남은 행의 가장 오래된 시각, 인덱스·저장소 정리 상태, 디스크 사용량을
함께 확인하세요. 삭제 직후 디스크가 줄지 않는다는 이유로 더 넓은 기간을 지우지 마세요.

삭제 결과가 예상과 다르면 경계 시각과 적용된 정책부터 확인해 보세요.
보관 의무가 있는 데이터라면 추가 삭제를 멈추고 담당자와 범위를 먼저 맞추는 것이 좋습니다.
