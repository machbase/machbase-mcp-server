# tagmetaimport와 메타데이터 일괄 등록

## tagmetaimport로 메타데이터 등록

`tagmetaimport`는 CSV의 태그명과 사용자 메타데이터를 가져오는 도구입니다.
일반 SQL의 논리 TAG 이름과 `-t` 입력 대상을 구분해야 합니다. 현재 래퍼는 `-t`를
machloader에 전달합니다. 아래 논리 테이블 `ch5_meta_import`의 메타데이터 입력 대상은
`_CH5_META_IMPORT_META`입니다. `-t ch5_meta_import`가 자동으로 METADATA를
선택한다고 가정하지 마십시오.

이 이름은 도구의 대상 지정에 사용합니다. SQL 조회·변경은 `ch5_meta_import METADATA`를
사용하며 저장 객체를 직접 수정하는 절차로 확장하지 않습니다. 기본 대상에 의존하지 말고
`-t`를 명시합니다.

## 1. 테이블 준비

기존 객체가 없는 실습 데이터베이스에서 다음 SQL을 실행합니다.

```sql
CREATE TAG TABLE ch5_meta_import (
    name VARCHAR(40) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
) METADATA (
    location VARCHAR(40),
    status VARCHAR(20)
);
```

## 2. CSV 준비

다음 내용을 클라이언트의 `ch5_metadata.csv`로 저장합니다.

```csv
name,location,status
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
TEMP_003,Building-B/F3,READY
```

파일에는 태그명 다음에 METADATA 선언 순서대로 값을 넣습니다. DATA의 time·value와
시스템 컬럼 `_ID`·`_LAST_UPDATE_TIME`은 넣지 않습니다. 헤더가 있으면 `-H`를 지정하며,
헤더가 임의의 컬럼 순서를 자동으로 맞춰 준다고 가정하지 않습니다.

## 3. 입력과 결과 확인

주소·계정은 실제 실습 서버에 맞추고, 사용하는 8.7.0 패키지의 `MACHBASE_HOME`과
라이브러리 환경에서 실행합니다.

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
  -t _CH5_META_IMPORT_META -d ch5_metadata.csv -H \
  -l ch5_import.log -b ch5_import.bad
```

첫 실행은 성공 3건·실패 0건을 기대합니다. 아래 METADATA 조회는 세 행을 반환하고
DATA COUNT는 0입니다. 메타데이터 등록은 측정값 입력과 다릅니다.

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta_import METADATA ORDER BY name;
SELECT COUNT(*) FROM ch5_meta_import;
```

## 4. 기존 태그와 재실행

같은 파일을 다시 입력해도 기존 태그가 자동 갱신되지 않습니다. 현재 경로는 일반
METADATA INSERT이므로 중복 태그는 오류 행으로 집계됩니다. 두 번째 실행은 성공
0건·실패 3건을 기대하며 기존 속성은 유지됩니다. 종료 상태만 보지 말고 성공·실패 건수와
bad/log 파일을 함께 확인합니다.

새 행과 잘못된 행이 섞인 파일도 전체가 하나의 트랜잭션이라고 가정하지 않습니다.
이미 반영된 태그를 확인하고 실패 행만 고쳐 재처리합니다. 기존 속성은 명시적인 UPDATE
또는 지원 UPSERT로 바꿉니다.

```sql
UPDATE ch5_meta_import METADATA SET status = 'DONE' WHERE name = 'TEMP_001';
INSERT INTO ch5_meta_import METADATA VALUES ('TEMP_002', 'Building-C/F2', 'READY')
ON DUPLICATE KEY UPDATE;
SELECT name, location, status FROM ch5_meta_import METADATA ORDER BY name;
```

TEMP_001은 DONE으로, TEMP_002는 Building-C/F2·READY로 바뀝니다.
실제 값이 바뀌면 변경 시각이 갱신되고 같은 값의 no-op은 유지됩니다.
`tagmetaimport`에 자동 UPSERT 옵션이 있다고 해석하지 마십시오.

## 정리와 관련 문서

결과 확인 후 `DROP TABLE ch5_meta_import;`로 이번 실습 테이블만 정리합니다.
CSV·로그·bad 파일은 재처리에 필요하지 않은지 확인한 뒤 정리합니다.

상세 옵션은 tagmetaimport 명령 사전을,
SQL 등록·변경 규칙은 TAG 메타데이터를 참고하십시오.
