# TRANSACTION 기능 지원표

Machbase TRANSACTION 테이블은 트랜잭션이 필요한 일반 관계형 데이터를 저장합니다. Machbase SQL과
JDBC/ODBC 등 지원 드라이버를 통해 접근합니다.

> **주의**: TRANSACTION 테이블은 **Standard Edition에서만 지원**됩니다. Cluster Edition에서는 TRANSACTION 테이블을 생성하거나 사용할 수 없습니다.

무수식 `CREATE TABLE`, `CREATE TRANSACTION TABLE`, `CREATE TXN TABLE`은 모두 TRANSACTION
테이블을 생성합니다. 따라서 Cluster Edition에서는 세 문법이 모두 거부됩니다. Cluster
Edition에서 LOG 테이블을 만들 때는 `CREATE LOG TABLE`을 사용합니다.

## SQL 기능 지원 여부

| 기능 | 지원 여부 | 비고 |
|------|:---------:|------|
| **기본 DML** | | |
| SELECT | O | |
| INSERT | O | |
| UPDATE | O | |
| DELETE | O | |
| INSERT ... ON DUPLICATE KEY UPDATE | O | PRIMARY KEY·UNIQUE INDEX 충돌 시 기존 row 갱신 |
| **트랜잭션** | | |
| Transaction (COMMIT/ROLLBACK) | O | plain `BEGIN`, `COMMIT`, `ROLLBACK` |
| TRANSACTION TRUNCATE의 ROLLBACK | O | 명시적 트랜잭션 안의 전체 행 삭제로 처리 |
| Savepoint | X | 미지원 |
| **쿼리 기능** | | |
| Prepared Statement | O | |
| 파라미터 바인딩 | O | |
| JOIN | O | 다른 테이블 유형과 조인 가능 |
| Subquery | O | |
| VIEW | O | |
| **객체** | | |
| SEQUENCE | O | `CREATE SEQUENCE` |
| PRIMARY KEY / UNIQUE INDEX | O | 단일 PRIMARY KEY와 단일·복합 UNIQUE INDEX |
| 보조 INDEX | O | 단일·복합 BTREE 인덱스 |
| JSON path INDEX | O | `json_column->'$.path'` |
| AUTO_INCREMENT | O | `LONG`/`INT64` 컬럼 단위 PRIMARY KEY |
| ALTER ADD/DROP COLUMN | O | 컬럼 정의에 괄호 사용 |
| ALTER RENAME COLUMN / RENAME TO | O | 컬럼명·테이블명 변경 |
| ALTER MODIFY COLUMN | X | 미지원 |
| Trigger | X | 미지원 |
| Stored Procedure | X | 미지원 |
| Foreign Key | X | 미지원 |

`AUTO_INCREMENT` 사용법은 AUTO_INCREMENT, upsert는
INSERT ON DUPLICATE KEY UPDATE를
참고하십시오. Append는 client별 경로가 다르므로
SDK Append matrix를
정본으로 사용합니다.

## 트랜잭션과 동시 접근의 경계

활성 트랜잭션에서도 다른 테이블 타입의 SELECT와 혼합 JOIN은 허용됩니다.
하지만 LOG·TAG·LOOKUP·VOLATILE 쓰기를 같은 TRANSACTION 트랜잭션으로 묶지는 못합니다.
허용된 조회가 모든 타입에 공통인 스냅샷 시점을 보장하는 것도 아닙니다.

일반 제약 오류는 실패한 문장과 전체 트랜잭션을 구분합니다.
앞선 성공 변경을 취소하려면 ROLLBACK이 필요하며, 롤백 전용 상태에서는 후속 작업을
계속하지 말고 종료해야 합니다. 열린 TRANSACTION 커서는 COMMIT·ROLLBACK을 차단할 수
있습니다.

현재 여러 TRANSACTION 테이블의 커밋은 테이블별 저장소 핸들에 순차 적용됩니다.
정상적인 여러 테이블 COMMIT·ROLLBACK 지원과, 커밋 중 장애까지 포함한 다중 테이블
원자성 보장은 같은 뜻이 아닙니다. 오류·응답 유실 뒤에는 업무 키로 반영 상태를
확인하세요.

WAL의 오래된 읽기 스냅샷을 쓰기로 전환하는 충돌은
TRANSACTION_BUSY_TIMEOUT_MS=-1이어도 대기로 해소되지 않습니다.
트랜잭션 실습과
두 연결 충돌 실습을 참고하세요.

## 관련 문서

- TRANSACTION 테이블 활용
- TRANSACTION DDL과 DML
- SDK 기능 지원 범위
