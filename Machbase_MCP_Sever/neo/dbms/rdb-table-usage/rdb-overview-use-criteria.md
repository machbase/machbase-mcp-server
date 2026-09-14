# 개요와 사용 기준

장비의 측정값은 계속 쌓이지만, 점검 상태나 재고 수량은 기존 값을 바꾸어야 합니다.
둘을 같은 모델로 처리하려 하면 원본 보관과 상태 변경의 요구가 섞이기 쉽습니다.
TRANSACTION은 변경 가능한 업무 데이터를 맡기고, 원본 시계열은 TAG·LOG에 남기는 구성을
먼저 생각해 보세요.

## TRANSACTION 테이블의 특성

TRANSACTION은 SELECT·INSERT·UPDATE·DELETE, PRIMARY KEY, UNIQUE INDEX와 보조 인덱스를
지원합니다. Standard Edition 전용이며 다음 세 문법은 같은 테이블을 만듭니다.

| 문법 | 의미 |
|---|---|
| CREATE TABLE | 타입을 생략한 기본 TRANSACTION 생성 |
| CREATE TRANSACTION TABLE | 타입을 명시한 생성 |
| CREATE TXN TABLE | 축약형 생성 |

공개 문서와 운영 스크립트에서는 타입이 드러나는 CREATE TRANSACTION TABLE을 권장합니다.
CREATE RDB TABLE·CREATE TRX TABLE은 지원하지 않습니다.
Cluster에서는 위 세 생성 문법을 모두 사용할 수 없으며 LOG는 CREATE LOG TABLE로 명시합니다.

## 상태 변경과 롤백

```sql
CREATE TRANSACTION TABLE ch8_overview (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_overview VALUES (42, 10);

BEGIN;
UPDATE ch8_overview SET qty = qty - 3 WHERE item_id = 42 AND qty >= 3;
SELECT item_id, qty FROM ch8_overview;
ROLLBACK;

SELECT item_id, qty FROM ch8_overview;
DROP TABLE ch8_overview;
```

같은 연결에서 트랜잭션 안의 조회는 수량 7, ROLLBACK 뒤 조회는 10입니다.
`qty >= 3`은 재고가 부족하면 변경하지 않도록 하는 업무 조건입니다.

실수하기 쉬운 부분은 UPDATE가 오류 없이 끝나면 업무도 성공했다고 판단하는 것입니다.
조건에 맞는 행이 없으면 변경 건수는 0일 수 있습니다. 애플리케이션에서는 영향 행 수가
기대한 1인지 확인하고 다음 작업이나 롤백을 결정해야 합니다.
SQL 예제에 등장하는 숫자만 그대로 바꾸는 것보다 이 확인 절차가 더 중요합니다.

## 다른 테이블과의 비교

| 주된 요구 | 먼저 검토할 테이블 |
|---|---|
| 센서 이름별 측정값과 ROLLUP | TAG |
| 수정하지 않는 로그·이벤트 원본 | LOG |
| 작은 현재 기준 정보 | LOOKUP |
| 관계형 DML과 명시적 트랜잭션 | TRANSACTION |
| 재시작 후 사라져도 되는 메모리 상태 | VOLATILE |

TRANSACTION에는 장비 점검 상태, 업무 이력, 별도 요약 결과 등을 둘 수 있습니다.
대량 원본 수집은 TAG·LOG와 처리량·입력 경로를 비교하세요.
TRANSACTION도 Append를 지원하지만 TAG·LOG와 같은 처리량이나 배치 경계를 가정해서는
안 됩니다. 입력 방식에서 구체적으로 구분합니다.

LOOKUP은 TRANSACTION의 모든 기능을 대신하는 테이블이 아닙니다.
Cluster에서 관계형 트랜잭션이 꼭 필요하다면 별도 RDBMS를 포함한 구성을 검토해야 합니다.

## 설계 기준

한 행을 식별할 키와 중복을 막을 업무 키를 구분하세요.
내부 번호에는 PRIMARY KEY, 외부 시스템 코드 같은 별도 고유값에는 UNIQUE INDEX가
필요할 수 있습니다. 자동 번호를 사용해도 업무 키의 중복이 저절로 없어지지는 않습니다.

이어서 자주 실행할 WHERE 조건과 업무의 성공 기준을 정합니다.
트랜잭션을 어디서 끝내고 오류가 나면 무엇을 확인할지까지 정해 두면,
동시 요청이나 연결 장애가 생겨도 처리 방향이 흔들리지 않습니다.
스키마와 트랜잭션을 함께 읽어 보세요.
