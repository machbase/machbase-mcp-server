# 조회와 분석

조회 SQL이 문법상 맞아도 입력한 상태값과 조건이 다르면 결과는 0건입니다.
정렬 기준이 부족하면 같은 시간의 행이 조회할 때마다 다르게 보일 수도 있습니다.
다양한 상태와 경계 시각을 가진 표본으로 필터·정렬·집계를 함께 확인하겠습니다.

## 실습 데이터 준비

```sql
CREATE TRANSACTION TABLE ch8_query (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(32),
    item_id  LONG,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
CREATE TRANSACTION TABLE ch8_query_product (id LONG PRIMARY KEY, name VARCHAR(64));
INSERT INTO ch8_query_product VALUES (42, 'Pump');
INSERT INTO ch8_query_product VALUES (43, 'Valve');

INSERT INTO ch8_query VALUES (
    1001, 'C-01', 42, 10.25, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1002, 'C-01', 43, 20.50, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1003, 'C-02', 42, 30.75, 'SHIPPED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

SELECT order_id, amount, status FROM ch8_query WHERE order_id = 1001;
```

1001·10.25·PENDING이 조회됩니다.

## 시간 조건과 정렬

```sql
SELECT order_id, amount FROM ch8_query
 WHERE ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND ordered <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND status = 'PENDING'
 ORDER BY ordered DESC, order_id DESC
 LIMIT 1;
```

1002 한 행이 선택됩니다. ordered가 같아도 order_id로 순서를 고정했습니다.
LIMIT만 지정해 원하는 순서를 기대하지 마세요.
연속된 일별 집계는 시작 포함·끝 제외 조건으로 경계의 중복을 피할 수 있습니다.
LOG 전용 DURATION이나 자동 _arrival_time은 TRANSACTION에 적용하지 않습니다.

## 기준 정보 조인

```sql
SELECT o.order_id, p.name, o.amount
  FROM ch8_query o JOIN ch8_query_product p ON o.item_id = p.id
 WHERE o.customer = 'C-01'
 ORDER BY o.order_id;
```

결과는 (1001, Pump, 10.25), (1002, Valve, 20.50)입니다.
이 INNER JOIN에서는 기준 정보가 없는 주문이 빠집니다.
조인 상대에 같은 키가 여러 행이면 결과가 늘어나므로 키의 고유성도 확인해야 합니다.
다른 타입과의 조인은 JOIN 실습에서 다룹니다.

## 집계 조회

```sql
SELECT status, COUNT(*) AS cnt, SUM(amount) AS total_amount
  FROM ch8_query GROUP BY status ORDER BY status;
```

PENDING은 2건·30.75, SHIPPED는 1건·30.75입니다.
인덱스가 있다고 모든 집계가 자동으로 빨라지는 것은 아닙니다.
범위·그룹 수·반환량을 확인하고 반복 업무라면 별도 요약을 검토하세요.

## JSON 경로 조회

```sql
CREATE TRANSACTION TABLE ch8_query_json (id INTEGER PRIMARY KEY, state JSON);
INSERT INTO ch8_query_json VALUES (1, '{"status":"ALARM","score":90}');
INSERT INTO ch8_query_json VALUES (2, '{"status":"NORMAL","score":10}');
INSERT INTO ch8_query_json VALUES (3, '{"score":20}');

SELECT id, state->'$.status' AS status FROM ch8_query_json
 WHERE state->'$.status' = 'ALARM'
 ORDER BY id;
```

1번만 선택됩니다. 없는 경로와 조건값이 다른 행을 구분해서 표본을 준비하세요.
화살표 경로의 문자열 비교와 숫자 추출 함수의 비교를 혼동하지 마세요.
자주 쓰는 경로는 JSON path 인덱스를
검토할 수 있습니다.

## 인덱스와 실행 계획

```sql
CREATE INDEX ch8_query_status_time ON ch8_query(status, ordered);
EXPLAIN SELECT order_id FROM ch8_query
 WHERE status = 'PENDING'
   AND ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD');
```

복합 인덱스의 선두 컬럼과 조건을 맞추되, 실제 사용 여부는 EXPLAIN으로 확인하세요.
Machbase가 관계형 쿼리 전체를 내부 SQLite에 그대로 맡긴다고 가정하면
인덱스 선택과 함수 조건을 잘못 해석할 수 있습니다.

```sql
DROP TABLE ch8_query_json;
DROP TABLE ch8_query_product;
DROP TABLE ch8_query;
```

결과가 다르면 집계나 JOIN부터 복잡하게 분석하기보다 원본 건수, WHERE 조건,
정렬 기준을 차례로 확인해 보세요.
