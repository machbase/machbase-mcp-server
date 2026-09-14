# 트랜잭션

여러 SQL을 실행하다가 중간 문장이 실패하면 앞선 변경도 사라졌다고 생각하기 쉽습니다.
하지만 일반 제약 오류는 실패한 문장과 전체 트랜잭션을 구분해서 처리합니다.
이 절에서는 같은 테이블 안의 변경으로 COMMIT·ROLLBACK 경계를 먼저 확인합니다.

## 트랜잭션 실행

```sql
CREATE TRANSACTION TABLE ch8_tx (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_tx VALUES (1, 10);
INSERT INTO ch8_tx VALUES (2, 20);

BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;

SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

트랜잭션 안에서는 7·23, ROLLBACK 뒤에는 10·20이 조회됩니다.
애플리케이션은 두 UPDATE가 각각 기대한 1행을 처리했는지 확인해야 합니다.
조건 미일치로 0행이 갱신된 것은 SQL 오류가 아니므로 DB가 업무 실패를 자동 판단하지는
않습니다.

다음은 같은 변경을 확정하는 정상 실습입니다.

```sql
BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
COMMIT;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

확정 후 값은 7·23입니다.
공개 문법은 BEGIN이며 BEGIN TRANSACTION, 중첩 BEGIN, SAVEPOINT는 지원하지 않습니다.
명시적 트랜잭션이 없으면 TRANSACTION DML은 문장 단위로 처리됩니다.
드라이버의 자동 커밋·트랜잭션 API는 별도로 확인하세요.

## 문장 오류와 롤백

아래는 오류 처리 학습용 흐름입니다. 중복 INSERT는 의도적으로 실패합니다.
SQL 실행 도구가 오류에서 중단되면 같은 연결에서 반드시 ROLLBACK까지 실행하세요.

```sql
BEGIN;
UPDATE ch8_tx SET qty = 100 WHERE item_id = 1;
```

```sql
-- 의도적으로 실패: item_id 중복
INSERT INTO ch8_tx VALUES (1, 999);
```

```sql
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

첫 조회는 100·23, ROLLBACK 뒤는 7·23입니다.
일반 제약 오류가 실패한 문장을 되돌려도 앞선 성공 문장은 트랜잭션 안에 남습니다.
업무 전체를 취소하려면 애플리케이션이 ROLLBACK을 선택해야 합니다.
모든 오류 뒤 계속 실행할 수 있는 것은 아닙니다. 복구 과정에서 롤백 전용 상태가 되었다면
ROLLBACK으로 종료해야 합니다.

## TRUNCATE와 롤백

```sql
BEGIN;
TRUNCATE TABLE ch8_tx;
SELECT COUNT(*) AS during_truncate FROM ch8_tx;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_tx;
```

결과는 0과 2입니다.
현재 TRANSACTION의 TRUNCATE는 전체 행 삭제로 명시적 트랜잭션에 포함됩니다.
LOG·TAG의 데이터 정리나 CREATE·ALTER·DROP 같은 스키마 변경과 혼동하지 마세요.
스키마 작업은 업무 트랜잭션 밖에서 수행하는 것이 운영 기준입니다.

## 테이블 타입별 트랜잭션 범위

활성 TRANSACTION 트랜잭션에서도 LOG·TAG·LOOKUP·VOLATILE 조회와 혼합 조인은 허용됩니다.
반면 이 타입들의 쓰기를 같은 트랜잭션에 묶을 수는 없습니다.
허용된 조회라고 해서 해당 타입이 TRANSACTION과 동일한 스냅샷·롤백 보장을 얻는 것도
아닙니다. 원본 수집과 업무 상태 변경 사이의 일관성은 별도로 설계하세요.

TRANSACTION 테이블의 읽기는 다른 세션의 미커밋 변경을 보지 않는 스냅샷을 사용합니다.
BEGIN 호출 시 모든 테이블에 공통인 읽기 시점이 한꺼번에 고정된다고 가정하지 마세요.
읽은 뒤 쓰기로 전환할 때의 충돌은 잠금과 재시도에서 다룹니다.

## 다중 테이블 커밋과 장애

여러 TRANSACTION 테이블의 DML을 BEGIN으로 묶고 정상적으로 COMMIT·ROLLBACK할 수 있습니다.
다만 현재 저장소는 테이블별 핸들을 사용하고 COMMIT도 핸들별로 순차 처리합니다.
따라서 커밋 도중 장애가 나도 여러 테이블 전체가 반드시 함께 확정되거나 함께 취소되는
원자적 커밋을 보장한다고 해석하면 안 됩니다.

여러 테이블의 불가분 처리가 필수인 업무는 이 제한을 먼저 검토하세요.
커밋 실패나 응답 유실 후 ROLLBACK을 보냈다는 이유만으로 모든 테이블이 원상 복구되었다고
판단하지 말고, 업무 키로 반영 상태를 다시 확인해야 합니다.
이 절의 기본 실습을 한 테이블의 두 행으로 구성한 이유이기도 합니다.

## 커서와 트랜잭션 종료

열린 TRANSACTION 커서가 있으면 COMMIT·ROLLBACK이 Resource busy로 실패할 수 있습니다.
SDK의 결과 집합·statement를 정리한 뒤 종료 문을 다시 실행하세요.
연결 종료 시 미커밋 변경은 롤백되지만, 연결을 잃기 전에 서버에서 이미 커밋했는지는
클라이언트가 별도로 확인해야 합니다.

```sql
DROP TABLE ch8_tx;
```

BEGIN 안에서 외부 API 호출이나 긴 계산을 기다리지 마세요.
트랜잭션을 짧게 유지하고, 실패할 때 “다시 실행할 것인가, 결과부터 확인할 것인가”를
구분해 두면 운영 중 판단이 훨씬 명확해집니다.
