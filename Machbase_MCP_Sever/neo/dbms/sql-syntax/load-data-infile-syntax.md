# LOAD DATA INFILE

`LOAD DATA INFILE`은 CSV 포맷 데이터 파일을 서버에서 직접 읽어 테이블에 입력하는 구문입니다.

> 대용량 데이터 입력에는 `machloader` 유틸리티 사용을 권장합니다. `machloader`는 병렬 처리와 다양한 옵션을 제공하여 더 빠른 입력 성능을 제공합니다.

## 문법

```sql
LOAD DATA INFILE 'file_path' INTO TABLE table_name
    [TABLESPACE tablespace_name]
    [AUTO { BULKLOAD | HEADUSE | HEADUSE_ESCAPE }]
    [{ FIELDS | COLUMNS } [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
    [LINES TERMINATED BY 'char']
    [TRIM { ON | OFF }]
    [IGNORE number LINES]
    [MAX_LINE_LENGTH number]
    [ENCODED BY coding_name]
    [ON ERROR { STOP | IGNORE }]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `AUTO BULKLOAD` | 행 전체를 하나의 컬럼으로 입력 |
| `AUTO HEADUSE` | 첫 번째 행의 컬럼명으로 테이블을 자동 생성 후 입력 |
| `AUTO HEADUSE_ESCAPE` | `HEADUSE`와 동일하나 예약어, 특수문자를 `_`로 치환 |
| `TERMINATED BY 'char'` | 필드 구분자 (기본값: `,`) |
| `ENCLOSED BY 'char'` | 필드 인용 문자 (기본값: `"`) |
| `LINES TERMINATED BY 'char'` | 레코드 구분자 |
| `TRIM { ON \| OFF }` | 컬럼 앞뒤 공백 제거 여부 (기본값: ON) |
| `IGNORE number LINES` | 첫 N줄 무시 (헤더 스킵 등) |
| `MAX_LINE_LENGTH number` | 한 줄 최대 길이 (기본값: 512KB) |
| `ENCODED BY coding_name` | 파일 인코딩 (기본값: UTF8) |
| `ON ERROR STOP\|IGNORE` | 오류 발생 시 중단 또는 무시 (기본값: STOP) |

지원 인코딩: `UTF8`, `MS949`, `KSC5601`, `EUCJP`, `SHIFTJIS`, `BIG5`, `GB231280`

## 예시

```sql
-- 기본 CSV 파일 입력 (구분자: ,  인용: ")
LOAD DATA INFILE '/tmp/sensor_data.csv' INTO TABLE sensor_log;

-- 헤더 1줄 무시하고 ;로 구분된 파일 입력
LOAD DATA INFILE '/tmp/data.csv' INTO TABLE sample_data
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    IGNORE 1 LINES
    ON ERROR IGNORE;

-- AUTO BULKLOAD: 각 줄을 단일 컬럼으로 입력 (테이블 자동 생성)
LOAD DATA INFILE '/tmp/raw.txt' INTO TABLE raw_table AUTO BULKLOAD;

-- AUTO HEADUSE: 첫 줄을 컬럼명으로 사용해 테이블 자동 생성 후 입력
LOAD DATA INFILE '/tmp/data_with_header.csv' INTO TABLE auto_table AUTO HEADUSE;

-- 인코딩 지정
LOAD DATA INFILE '/tmp/korean_data.csv' INTO TABLE Korean_table ENCODED BY MS949;
```

## 주의사항

- `AUTO` 옵션을 사용하지 않는 경우, 대상 테이블의 모든 컬럼은 `VARCHAR` 또는 `TEXT` 타입이어야 합니다.
- 파일 경로는 Machbase 서버 프로세스가 접근 가능한 경로여야 합니다.
- 입력 도중 오류가 발생해도 이미 입력된 행은 롤백되지 않습니다.
- 대용량 파일은 `machloader`를 사용하는 것이 성능 면에서 유리합니다.

## machloader와의 비교

| 항목 | LOAD DATA INFILE | machloader |
|------|-----------------|------------|
| 병렬 처리 | 미지원 | 지원 |
| 사용 방법 | SQL 문 | CLI 유틸리티 |
| 용도 | 소량 데이터, 스크립트 내 사용 | 대용량 일괄 입력 |

## 관련 문서

- SAVE DATA INTO syntax — SELECT 결과를 파일로 저장
