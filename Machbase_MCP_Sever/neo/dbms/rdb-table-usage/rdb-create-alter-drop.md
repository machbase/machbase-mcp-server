# 생성, 변경, 삭제

스키마 변경에서는 명령의 성공 여부만큼 기존 데이터와 입력 프로그램의 상태가 중요합니다.
이름을 바꾼 뒤 예전 SQL을 계속 실행하거나, 인덱스가 참조하는 컬럼부터 삭제하면 오류를
만나게 됩니다. 이 절에서는 표본을 넣은 상태에서 변경 전후를 확인합니다.

## 테이블 생성

```sql
CREATE TRANSACTION TABLE ch8_ddl (
    id   LONG,
    code VARCHAR(32),
    qty  INTEGER
);
INSERT INTO ch8_ddl VALUES (1, 'P-01', 10);
```

## 키와 인덱스 생성

```sql
CREATE PRIMARY KEY INDEX ch8_ddl_pk ON ch8_ddl(id);
CREATE UNIQUE INDEX ch8_ddl_code ON ch8_ddl(code);
CREATE INDEX ch8_ddl_qty ON ch8_ddl(qty);
SHOW INDEX ch8_ddl_code;
```

id는 단일 PRIMARY KEY, code는 별도 업무 키입니다.
기존 데이터에 중복이나 PRIMARY KEY의 NULL이 있으면 생성이 실패할 수 있습니다.
복합 고유성은 CREATE UNIQUE INDEX로 만들며, CREATE TABLE 내부의 UNIQUE 제약 문법은
지원하지 않습니다.

자동 번호가 필요한 경우에는 생성 시 `LONG PRIMARY KEY AUTO_INCREMENT`를 지정합니다.
이 절의 id는 직접 입력한 값이며 자동 번호 컬럼이 아닙니다.
두 생성 방식을 같은 객체에 중복 실행하지 마세요.
AUTO_INCREMENT에 별도 실습이 있습니다.

## 컬럼 추가와 기본값

```sql
ALTER TABLE ch8_ddl ADD COLUMN (label VARCHAR(64));
ALTER TABLE ch8_ddl ADD COLUMN (status VARCHAR(16) DEFAULT 'NEW');
ALTER TABLE ch8_ddl ADD COLUMN (limits DECIMAL(12)[2] DEFAULT [10, 20]);

SELECT id, label, status, limits FROM ch8_ddl ORDER BY id;
```

1번 행에서 label은 NULL, status는 NEW, limits는 [10, 20]입니다.
DEFAULT가 없는 ARRAY 컬럼을 추가하면 기존 행은 배열 전체가 NULL입니다.

`ADD COLUMN`의 `DEFAULT`와 `CREATE TABLE`의 `DEFAULT`는 허용 범위가 다릅니다.
위처럼 `ADD COLUMN`에는 타입에 맞는 값을 지정할 수 있지만, `CREATE TABLE`의 컬럼 정의에서는
`DATETIME` 컬럼의 `DEFAULT SYSDATE`만 사용할 수 있습니다. 다른 타입이나 다른 값을 지정하면
각각 `ERR-02346`, `ERR-02347`로 거부됩니다. 생성 시점에 기본값이 필요하면 컬럼을 먼저
만들고 `ADD COLUMN`으로 추가하거나, 입력 구문에서 값을 지정하십시오.
배열 안의 일부 요소가 NULL인 경우와 구분하세요.

컬럼 정의는 괄호로 묶습니다. 이 문법은 다른 DBMS의 ALTER TABLE 형식과 혼동하기 쉽습니다.
TRANSACTION은 MODIFY COLUMN으로 길이·타입을 변경하는 기능을 지원하지 않습니다.
필요하면 새 스키마로 이관하는 절차를 별도로 준비하세요.

## 컬럼 변경과 의존 객체

```sql
DROP INDEX ch8_ddl_qty;
ALTER TABLE ch8_ddl DROP COLUMN (qty);
ALTER TABLE ch8_ddl DROP COLUMN (label);
ALTER TABLE ch8_ddl DROP COLUMN (limits);
ALTER TABLE ch8_ddl RENAME COLUMN code TO product_code;

SELECT id, product_code, status FROM ch8_ddl;
SHOW INDEX ch8_ddl_code;
```

기존 1번 행의 P-01·NEW 값과 업무 키 인덱스가 유지됩니다.
PRIMARY KEY·UNIQUE·일반·JSON path 인덱스가 참조하는 컬럼은 해당 인덱스부터 확인해야
합니다. 마지막 사용자 컬럼은 삭제할 수 없습니다.

VIEW가 테이블이나 컬럼을 참조하면 관련 이름 변경·삭제가 거부될 수 있습니다.
VIEW뿐 아니라 애플리케이션 SQL과 prepared statement도 변경 영향을 받습니다.
DDL 이후에는 기존 prepared statement를 무조건 재사용하지 말고 다시 준비할 필요를
확인하세요.

```sql
ALTER TABLE ch8_ddl RENAME TO ch8_product;
SELECT id, product_code, status FROM ch8_product;
```

테이블 이름을 바꾼 뒤에는 ch8_product로 조회합니다.

## 전체 삭제와 테이블 삭제

```sql
BEGIN;
TRUNCATE TABLE ch8_product;
SELECT COUNT(*) AS during_delete FROM ch8_product;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_product;
DROP TABLE ch8_product;
```

건수는 각각 0과 1입니다. 현재 TRANSACTION의 TRUNCATE는 전체 행 삭제로 처리되어
명시적 트랜잭션 안에서 롤백할 수 있습니다. 이 동작을 LOG·TAG의 TRUNCATE에 확대해서
적용하지 마세요. 마지막 DROP은 데이터·정의·관련 인덱스를 삭제합니다.

## DDL 운영 주의사항

TRUNCATE의 위 동작과 CREATE·ALTER·DROP 같은 스키마 작업을 구분해야 합니다.
스키마 변경을 BEGIN 안에 넣어 나중에 ROLLBACK할 수 있다고 가정하지 마세요.
같은 테이블의 활성 트랜잭션이나 열린 커서는 DDL을 차단할 수 있으므로 먼저 결과 집합과
업무 트랜잭션을 정리합니다.

ADD·DROP COLUMN은 카탈로그와 별도 저장 파일을 함께 변경합니다.
작업 중 서버가 중단되었다면 재시작 복구가 끝나기 전에 같은 DDL을 반복하지 마세요.
복구 후 DESC, 대표 SELECT·INSERT, 인덱스·VIEW를 확인하고 서버 로그도 점검합니다.
내부 저장 파일을 직접 이동·수정·삭제하는 방식으로 복구하려 하지 마세요.

예상과 다른 스키마가 보이면 변경 전 DDL, 실행 순서, 첫 오류를 함께 살펴보세요.
마지막 오류만 보는 것보다 원인을 찾기 쉽습니다.
