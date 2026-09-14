# 함수 사전

내장 함수를 카테고리별로 정리합니다.

| 카테고리 | 설명 |
|----------|------|
| 집계 함수 | COUNT, SUM, AVG, MIN, MAX, STDDEV, FIRST, LAST 등 그룹 집계 함수 |
| 윈도우/시리즈 함수 | ROWNUM, SERIESNUM 등 윈도우·시리즈 분석 함수 |
| 날짜/시간 함수 | TO_DATE, TO_CHAR, DATE_TRUNC, ADD_TIME 등 날짜·시간 처리 함수 |
| JSON 함수와 JSON dot 표기법 | JSON 데이터 추출·조작 함수 및 멤버 접근 문법 |
| 정규식 함수 | REGEXP_LIKE, REGEXP_SUBSTR 등 정규식 기반 검색·변환 함수 |
| NEXTVAL 함수 | Lookup 테이블 Sequence 컬럼용 자동 증가값 생성 함수 |
| 사용자 컨텍스트 함수 | CURRENT_USER, SESSION_USER와 내부 사용자 ID 조회 |
| 전체 함수 레퍼런스 | 기존 함수 항목과 CAST를 포함한 전체 함수 레퍼런스 |

## 공통 규칙

- 입력 값이 `NULL`이면 결과도 `NULL`입니다 (별도 명시가 없는 한).
- 인자 타입 불일치 시 `ERR-02036` 또는 `ERR-02037` 오류가 발생합니다.
