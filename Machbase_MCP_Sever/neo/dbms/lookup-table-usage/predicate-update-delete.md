# 일반 predicate UPDATE/DELETE

LOOKUP 테이블은 기본 키뿐 아니라 일반 조건식으로 여러 행을 수정하거나 삭제할 수 있습니다.
변경 전 같은 조건으로 대상 행 수를 확인하십시오.

이 페이지의 실습은 다음 테이블 하나로 진행하며 마지막에 정리합니다.

```sql
CREATE LOOKUP TABLE ch9_predicate (
    equip_id VARCHAR(32) PRIMARY KEY,
    site     VARCHAR(16),
    status   VARCHAR(16),
    score    INTEGER
);

INSERT INTO ch9_predicate VALUES ('EQ-01', 'SEOUL', 'READY',   10);
INSERT INTO ch9_predicate VALUES ('EQ-02', 'SEOUL', 'READY',   20);
INSERT INTO ch9_predicate VALUES ('EQ-03', 'SEOUL', 'RETIRED', 30);
INSERT INTO ch9_predicate VALUES ('EQ-04', 'BUSAN', 'READY',   40);
```

## UPDATE

조건에 맞는 모든 행을 갱신합니다. `SET` 표현식은 현재 행 값을 참조할 수 있지만 기본 키
컬럼 자체는 변경할 수 없습니다.

LOOKUP UPDATE에는 `WHERE` 조건이 필요합니다. 전체 행을 갱신하려는 경우에도 지원되는
조건식을 명시합니다. `WHERE` 없이 전체 삭제가 가능한 DELETE와 구분하십시오.

```sql
-- 변경 전 영향 범위를 먼저 셉니다.
SELECT COUNT(*) FROM ch9_predicate
 WHERE site = 'SEOUL' AND status = 'READY';

UPDATE ch9_predicate
   SET status = 'ACTIVE', score = score + 10
 WHERE site = 'SEOUL' AND status = 'READY';

SELECT equip_id, site, status, score FROM ch9_predicate ORDER BY equip_id;
```

COUNT는 2이고, EQ-01과 EQ-02만 `ACTIVE`로 바뀌면서 score가 20·30이 됩니다.
같은 SEOUL이라도 status가 다른 EQ-03과, 같은 READY라도 site가 다른 EQ-04는 그대로입니다.

## DELETE

조건에 맞는 모든 행을 삭제합니다. `WHERE`를 생략하면 테이블의 모든 행이 삭제됩니다.

```sql
SELECT COUNT(*) FROM ch9_predicate WHERE status = 'RETIRED';

DELETE FROM ch9_predicate WHERE status = 'RETIRED';

SELECT equip_id, status FROM ch9_predicate ORDER BY equip_id;
```

COUNT는 1이고 EQ-03이 삭제되어 세 행이 남습니다.

## 조건 설계 지침

1. 단건 변경에는 기본 키 조건을 사용합니다.
2. 일괄 변경 전 동일한 조건의 `SELECT COUNT(*)`로 영향 범위를 확인합니다.
3. 자주 필터링하는 JSON 값은 일반 컬럼으로 분리해 인덱스를 적용하는 방안을 검토합니다.
4. 기본 키를 바꿔야 한다면 기존 행을 삭제하고 새 키로 삽입합니다.

지원 연산자와 JSON 조건의 정확한 범위는 SQL 레퍼런스를 기준으로 확인하십시오.

- LOOKUP predicate UPDATE
- LOOKUP predicate DELETE

## 권한과 성능

UPDATE와 DELETE에는 각각 대상 테이블의 `UPDATE`, `DELETE` 권한이 필요합니다. 애플리케이션이
변경 전후 값을 직접 조회할 때만 `SELECT`도 부여합니다. 권한 SQL은
권한 관리를 정본으로 사용합니다.

기본 키 equality는 단건 대상을 직접 찾고, 일반 조건식은 조건을 평가해 변경 대상을 수집합니다.
반복 단건 변경에는 prepared statement와 bind를 사용하고, 대량 변경은 같은 조건의 행 수와
실행 시간을 검증 환경에서 측정하십시오.

```sql
DROP TABLE ch9_predicate;
```
