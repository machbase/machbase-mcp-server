# JOIN과 관계형 조회 설계

JOIN을 붙였는데 주문 건수가 줄거나 늘어났다면 먼저 관계의 모양을 확인해야 합니다.
INNER JOIN은 상대가 없는 행을 제외하고, 한 건에 여러 상대가 맞으면 결과를 늘립니다.
SQL이 오류 없이 실행되는 것과 업무 건수를 올바르게 집계하는 것은 다른 문제입니다.

## TRANSACTION–LOOKUP 조인

```sql
CREATE TRANSACTION TABLE ch8_join_order (
    order_id LONG PRIMARY KEY,
    item_id  LONG,
    qty      INTEGER
);
CREATE LOOKUP TABLE ch8_join_product (id LONG PRIMARY KEY, name VARCHAR(64));
CREATE TRANSACTION TABLE ch8_join_payment (order_id LONG PRIMARY KEY, status VARCHAR(16));

INSERT INTO ch8_join_order VALUES (1, 42, 2);
INSERT INTO ch8_join_order VALUES (2, 99, 1);
INSERT INTO ch8_join_product VALUES (42, 'Pump');
INSERT INTO ch8_join_payment VALUES (1, 'PAID');

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o LEFT JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;
```

INNER JOIN은 1번 주문만, LEFT JOIN은 1·2번 주문을 반환합니다.
2번의 제품 이름은 NULL입니다. 제품 99가 없어도 주문 입력 자체는 외래 키로 차단되지
않으므로, 필요한 참조 검증은 별도로 설계해야 합니다.

실수하기 쉬운 부분은 LEFT JOIN 뒤 오른쪽 테이블 조건을 WHERE에 넣는 것입니다.
예를 들어 `WHERE p.name = 'Pump'`를 추가하면 NULL 행이 제외됩니다.
상대를 찾는 조건인지 최종 결과를 거르는 조건인지 구분하세요.

## TRANSACTION 간 조인

```sql
SELECT o.order_id, o.qty, p.status
  FROM ch8_join_order o
  JOIN ch8_join_payment p ON o.order_id = p.order_id
 ORDER BY o.order_id;
```

(1, 2, PAID) 한 행이 조회됩니다.
실제 결제 이력이 주문당 여러 행이면 이 결과도 여러 행이 됩니다.
주문 금액을 조인 후 합산할 때 중복 합계가 생기지 않도록 관계와 집계 단위를 확인하세요.

## TAG 근접 시간 조인

다음은 알람 전후 5초에 있는 모든 측정값을 연결하는 예제입니다.

```sql
CREATE TRANSACTION TABLE ch8_join_alarm (
    alarm_id LONG PRIMARY KEY,
    sensor   VARCHAR(32),
    occurred DATETIME
);
CREATE TAG TABLE ch8_join_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch8_join_alarm VALUES (
    1, 'TEMP-01', TO_DATE('2026-01-01 10:00:05', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:11', 'YYYY-MM-DD HH24:MI:SS'), 30);

SELECT a.alarm_id, s.time, s.value
  FROM ch8_join_alarm a JOIN ch8_join_sensor s ON a.sensor = s.name
 WHERE s.time >= a.occurred - 5s
   AND s.time <= a.occurred + 5s
 ORDER BY a.alarm_id, s.time;
```

알람 1번에 값 10·20의 두 행이 연결됩니다. 양쪽 경계를 포함하며 값 30은 제외됩니다.
이 쿼리는 가장 가까운 측정값 하나나 정확히 같은 시각의 값을 고르는 기능이 아닙니다.
한 값만 필요하면 최근 이전 값·최단 거리 등 선택 기준과 동률 처리 규칙을 별도로 정하세요.

## 조인 설계 기준

조인 키의 타입과 값 형식을 맞추고 시간 범위를 제한한 뒤 실행 계획을 확인합니다.
필요한 컬럼만 반환하고, 함수·형 변환을 조인 키에 무심코 추가해 접근 경로가 달라지지
않는지 비교하세요. 조인 순서나 알고리즘이 다른 RDBMS와 같다고 가정하지 마세요.

혼합 조인이 허용되어도 다른 테이블 타입이 TRANSACTION과 동일한 트랜잭션 스냅샷을
공유하는 것은 아닙니다. 또한 현재 LOOKUP 설명을 붙인 결과가 과거 시점의 설명까지
재현하지는 않습니다.

```sql
DROP TABLE ch8_join_sensor;
DROP TABLE ch8_join_alarm;
DROP TABLE ch8_join_payment;
DROP TABLE ch8_join_product;
DROP TABLE ch8_join_order;
```

결과 건수가 맞지 않으면 조인 전 건수와 키별 상대 행 수를 먼저 비교해 보세요.
이 두 가지가 확인되면 쿼리를 어떻게 고쳐야 할지도 명확해집니다.
