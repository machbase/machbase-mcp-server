# SAVE DATA INTO

`SAVE DATA INTO`는 `SELECT` 쿼리 결과를 CSV 파일로 저장하는 구문입니다.

## 문법

```sql
SAVE DATA INTO 'file_path'
    [HEADER { ON | OFF }]
    [{ FIELDS | COLUMNS }
        [TERMINATED BY 'char']
        [ENCLOSED BY 'char']
    ]
    [ENCODED BY coding_name]
    AS select_query
```

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `HEADER { ON \| OFF }` | OFF | 첫 줄에 컬럼명 출력 여부 |
| `TERMINATED BY 'char'` | `,` | 필드 구분자 |
| `ENCLOSED BY 'char'` | `"` | 필드 인용 문자 |
| `ENCODED BY coding_name` | UTF8 | 출력 파일 인코딩 |

지원 인코딩: `UTF8`, `MS949`, `KSC5601`, `EUCJP`, `SHIFTJIS`, `BIG5`, `GB231280`

## 예시

```sql
-- 기본 CSV 저장
SAVE DATA INTO '/tmp/result.csv' AS SELECT * FROM sensor_log;

-- 헤더 포함, 세미콜론 구분자
SAVE DATA INTO '/tmp/output.csv'
    HEADER ON
    FIELDS TERMINATED BY ';'
    AS SELECT name, time, value FROM sensor_log WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 특수 구분자와 인용 문자 지정
SAVE DATA INTO '/tmp/export.csv'
    HEADER ON
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    ENCODED BY MS949
    AS SELECT * FROM t1 WHERE i1 > 100;

-- TAG 테이블 데이터 내보내기
SAVE DATA INTO '/tmp/tag_export.csv'
    HEADER ON
    AS SELECT name, time, value
         FROM sensor_tag
        WHERE name = 'TEMP-01'
          AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2024-01-02', 'YYYY-MM-DD')
        ORDER BY time;
```

## 주의사항

- 파일 경로는 Machbase 서버 프로세스가 쓰기 가능한 경로여야 합니다.
- 출력 경로에 파일이 이미 존재하면 오류가 발생하며, 기존 파일은 변경되지 않습니다.
  다른 파일명을 지정하거나 기존 파일을 이동한 후 다시 실행하십시오.
- SELECT 결과가 없는 경우 빈 파일(헤더만)이 생성될 수 있습니다.
- 파일 경로에 접근 권한이 없으면 오류가 반환됩니다.

## 관련 문서

- LOAD DATA INFILE syntax — 파일에서 테이블로 데이터 입력
