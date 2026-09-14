# 쿼리와 성능 문제

## 쿼리가 느릴 때

문제가 발생한 SQL, 바인드 값의 범위, 시작·종료 시각, 기대 행 수와 실제 행 수를 기록합니다.

```sql
SELECT ID, SESS_ID, STATE, QUERY
  FROM V$STMT
 ORDER BY ID;

EXPLAIN SELECT ...;
```

실행 계획에서 다음을 확인합니다.

- 시간·태그 조건이 충분히 이른 단계에서 적용되는가
- 큰 테이블이 불필요하게 반복 스캔되는가
- 조인 키의 타입과 값 형태가 일치하는가
- 필요한 인덱스 또는 ROLLUP이 실제로 사용되는가
- 반환할 필요가 없는 열과 행을 읽고 있지 않은가

MINMAX 캐시를 검토할 때의 현재 속성명은
`DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE`입니다. 값을 바꾸기 전에 현재 값과 실행
계획을 기록하고 격리 환경에서 비교하십시오. 상세 절차는
성능 튜닝을 따릅니다.

## 검색 결과가 예상과 다를 때

```sql
SELECT COUNT(*), MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME)
  FROM target_log;
```

1. 대상 데이터베이스, 소유자와 테이블 이름을 확인합니다.
2. 필터 없이 소량 조회해 데이터 존재 여부와 실제 시간 값을 봅니다.
3. 연결 시간대와 입력 문자열의 시간대 해석을 확인합니다.
4. 태그 이름, 대소문자, 경계 연산자(`>`, `>=`, `<`, `<=`)를 확인합니다.
5. ROLLUP 결과라면 gap과 갱신 상태를 확인합니다.

서버 속성 `DEFAULT_TIMEZONE`을 찾지 마십시오. 시간대는 클라이언트 연결과 세션에서 명시하고,
원본 데이터의 기준 시간대를 함께 기록합니다.

```sql
SHOW ROLLUPGAP;
SELECT * FROM V$ROLLUP;
```

## 메모리 부족

```sql
SELECT * FROM V$SYSMEM;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
```

운영체제 메모리, swap, OOM 기록과 같은 시각의 Machbase 로그를 함께 확인합니다. 대량 결과를
한 번에 가져오는 쿼리, 넓은 조인·정렬, 과도한 동시 실행, 클라이언트의 큰 fetch·Append 버퍼를
각각 분리해 재현합니다.

현재 설정값은 `V$PROPERTY`에서 조회합니다. 허용 범위와 변경 방법은
설정 사전에서 확인하고, 변경은 하나씩
부하 시험한 뒤 적용합니다.
