# LOOKUP SQL/JSON 지원표

이 페이지는 LOOKUP 테이블의 SQL 기능과 JSON 관련 제약을 정리합니다.

## 지원 현황

| 기능 | 지원 | 비고 |
|------|:---:|------|
| **기본 CRUD** | | |
| INSERT | O | 일반 INSERT 사용 |
| SELECT | O | 기본 키(PK) 조건과 일반 검색 조건 모두 사용 가능 |
| UPDATE (PK 조건) | O | Primary key fast path 사용 |
| DELETE (PK 조건) | O | Primary key fast path 사용 |
| UPDATE (일반 검색 조건) | O | 조건에 맞는 기본 키 집합을 수집한 뒤 갱신 |
| DELETE (일반 검색 조건) | O | 조건에 맞는 기본 키 집합을 수집한 뒤 삭제 |
| **JSON 기능** | | |
| JSON 타입 컬럼 | O | 일반 컬럼으로 생성, 저장, 조회, 갱신 가능 |
| JSON path query (`$.key`) | O | `->`, `JSON_EXTRACT_*`, `JSON_TYPEOF`, `JSON_IS_VALID` 사용 가능 |
| JSON PK | X | JSON 컬럼은 primary key로 선언할 수 없음 |
| JSON path index | X | 별도 JSON path index는 지원하지 않음 |
| **기타** | | |
| 명시적 트랜잭션 (`BEGIN`/`COMMIT`/`ROLLBACK`) | X | 각 DML은 개별 문장 단위로 반영되며 여러 문장을 함께 롤백할 수 없음 |
| Prepared Statement | O | 기본 키 조건과 일반 검색 조건에서 매개변수 바인딩 지원 |
| Append API | △ | 일반 SQL INSERT가 기본이며, Append는 별도 LOOKUP append 정책을 따름 |

## 정본

LOOKUP JSON 스키마와 실행 예제는 JSON 컬럼과 조회를, UPDATE·DELETE 문법은 DML 문법을 참고하십시오.
