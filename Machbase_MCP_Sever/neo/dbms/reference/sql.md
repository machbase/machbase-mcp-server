# SQL 레퍼런스

SQL 문법, 함수, 데이터 타입, 쿼리 힌트, 상대 시간 표현의 정확한 정의를 제공합니다.

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| SQL 문법 사전 | CREATE, DROP, ALTER, SELECT, WITH/CTE, INSERT, DELETE, UPDATE, BACKUP, MOUNT 등 모든 SQL 구문의 BNF 문법과 예시 |
| 함수 사전 | 집계 함수, 수학 함수, 문자열 함수, 날짜/시간 함수, 타입 변환 함수, TAG 전용 함수 목록 및 설명 |
| 데이터 타입 사전 | 지원 데이터 타입의 크기, 범위, 기본값, 테이블 유형별 사용 가능 여부 |
| SELECT hint syntax | SELECT 힌트 문법, 사용법, 적용 대상 |
| 상대 시간 표현 사전 | `now - 1h` 형태의 상대 시간 literal과 접미사 |
| ROWID | 테이블별 ROWID 의미, 조회 조건과 INSERT 결과 |

## SQL 특징

표준 ANSI SQL을 기반으로 시계열 데이터 처리에 최적화된 확장 문법을 제공합니다.

- **TAG 시계열 기능**: BASETIME, METADATA, `FIRST`/`LAST`, `SERIES BY`, ROLLUP
- **시간 범위 조회**: `DURATION`, `BEFORE`, `AFTER`, `RANGE` 절
- **공통 테이블 표현식**: Standard Edition의 비재귀 `WITH`/CTE
- **대량 입력 연동**: 클라이언트 SDK의 Append API (SQL 문장이 아닌 별도 입력 API)
- **텍스트 검색**: `SEARCH`, `ESEARCH`, `REGEXP` 연산자
- **집합 연산**: `UNION ALL` (UNION, INTERSECT, EXCEPT 미지원)
