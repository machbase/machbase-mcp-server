# 데이터 입력과 변경

UPDATE가 성공했다는 응답과 주문 한 건이 원하는 상태로 바뀌었다는 사실은 다릅니다.
조건에 맞는 행이 없으면 오류 없이 0행이 처리될 수 있기 때문입니다.
수정 전 대상, 영향 행 수, 수정 후 값을 함께 확인하는 습관이 필요합니다.

## 조건부 UPDATE와 DELETE

```sql
CREATE TRANSACTION TABLE ch8_mutation (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_mutation VALUES (
    1001, 19900.25, 'PENDING', TO_DATE('2026-01-01', 'YYYY-MM-DD'));
INSERT INTO ch8_mutation VALUES (
    1002, 29900.50, 'CANCELLED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

BEGIN;
UPDATE ch8_mutation SET status = 'SHIPPED'
 WHERE order_id = 1001 AND status = 'PENDING';
SELECT order_id, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

1001은 SHIPPED, 1002는 CANCELLED입니다.
같은 UPDATE를 다시 실행하면 PENDING이 아니므로 영향 행 수가 0입니다.
애플리케이션은 SDK의 영향 행 수를 확인해서 작업 성공·이미 처리됨·대상 없음 등을
업무 규칙에 맞게 구분해야 합니다.

아래 삭제도 대상 건수를 확인한 뒤 트랜잭션 안에서 실행합니다.

```sql
BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_mutation WHERE status = 'CANCELLED';
DELETE FROM ch8_mutation WHERE status = 'CANCELLED';
SELECT order_id, amount, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

대상은 1행이고 삭제 후 1001 한 행만 남습니다.
WHERE가 없는 UPDATE·DELETE는 전체 행 대상입니다.
운영에서 사전 SELECT와 실제 변경 사이에 다른 세션이 데이터를 바꿀 수 있으므로
사전 건수만을 성공의 근거로 삼지 마세요.

## INSERT SELECT와 자기 참조

```sql
CREATE TRANSACTION TABLE ch8_archive (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_archive(order_id, amount, status, ordered)
SELECT order_id, amount, status, ordered FROM ch8_mutation
 WHERE ordered < TO_DATE('2026-02-01', 'YYYY-MM-DD');

INSERT INTO ch8_mutation(order_id, amount, status, ordered)
SELECT order_id + 10000, amount, status, ordered FROM ch8_mutation
 WHERE order_id = 1001;

SELECT order_id FROM ch8_archive ORDER BY order_id;
SELECT order_id FROM ch8_mutation ORDER BY order_id;
```

아카이브는 1001, 원본은 1001·11001입니다.
자기 테이블에서 읽은 결과를 다시 삽입해도 이 예제가 새 행을 끝없이 재입력하지는 않습니다.
다만 키를 바꾸지 않고 복사하면 고유성 위반이 날 수 있습니다.
대상 컬럼 수와 타입을 맞추고 복사 범위를 재실행 가능하게 나누세요.

일반 제약 오류와 연결 장애를 같은 실패로 취급하지 마세요.
문장 실패가 전체 BEGIN을 자동 롤백하지는 않으며, 커밋 응답을 잃었을 때는 반영 여부를
다시 조회해야 합니다. 트랜잭션에서 처리 경계를 설명합니다.

```sql
DROP TABLE ch8_archive;
DROP TABLE ch8_mutation;
```

## 대량 입력과 배치 경계

TRANSACTION도 Append API를 지원합니다.
예전 파일명이나 앵커에 reject·unsupported가 남아 있다는 이유로 현재 지원하지 않는다고
판단하지 마세요. 언어별 공개 API는
SDK 기능 지원 범위를
기준으로 선택합니다.

| 입력 방식 | 확인할 기준 |
|---|---|
| SQL INSERT·prepared 실행 | 문장별 오류와 명시적 트랜잭션 경계 |
| 드라이버 batch | 실제 전송 단위, 부분 성공, 자동 커밋 |
| Append | SDK 버퍼·서버 배치 경계, 오류 콜백·반환값 |
| machloader | 매핑과 실패 행, 처리 구간 기록 |

현재 SQLCLI SQLAppendBatch 경로는 별도의 활성 트랜잭션이 없으면 서버 배치를
트랜잭션으로 처리합니다. 이 경로의 제약 오류 회귀에서는 실패한 배치 전체가 롤백됩니다.
이를 모든 SDK의 논리 배치, 여러 번의 flush, Appender 전체 수명에 대한 하나의
원자적 작업으로 확대해석해서는 안 됩니다.

AUTO_INCREMENT와 DECIMAL 입력은
SQLCLI와 ODBC의 전용 규칙도 확인하세요.
Append 프로토콜의 도착 시각 필드가 TRANSACTION에 LOG의 자동 시간 컬럼을 만드는 것은
아닙니다.

실제 도입 전에는 정상 행에 중복 키·NULL 오류 한 행을 섞어 성공·실패 건수와 저장 결과를
확인하세요. 네트워크 오류 뒤 재전송은 이미 커밋된 데이터의 중복 처리까지 고려해야 합니다.
