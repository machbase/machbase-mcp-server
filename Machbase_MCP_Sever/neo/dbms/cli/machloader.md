# machloader 명령/옵션 사전

`machloader`는 텍스트 파일(CSV 등)과 Machbase 서버 간에 데이터를 가져오거나 내보내는 범용 데이터 로딩 도구입니다. APPEND 모드를 기본으로 지원하며 스키마 파일을 통해 복잡한 변환도 처리할 수 있습니다.

## 옵션 목록

```bash
machloader -h
```

| 옵션 | 설명 |
|------|------|
| `-s`, `--server=SERVER` | 서버 IP 주소 (기본값: 127.0.0.1) |
| `-P`, `--port=PORT` | 서버 포트 번호 (기본값: 5656) |
| `-u`, `--user=USER` | 사용자 이름 (기본값: SYS) |
| `-p`, `--password=PASSWORD` | 사용자 비밀번호 (기본값: MANAGER) |
| `-i`, `--import` | 가져오기 모드 |
| `-o`, `--export` | 내보내기 모드 |
| `-c`, `--schema` | 스키마 파일 생성 모드 |
| `-t`, `--table=TABLE_NAME` | 대상 테이블 이름 |
| `-f`, `--form=SCHEMA_FILE` | 스키마 파일 이름 |
| `-d`, `--data=DATA_FILE` | 데이터 파일 이름 |
| `-m`, `--mode=MODE` | 가져오기 모드. `append`(기본값) 또는 `replace` |
| `-H`, `--header` | 헤더 행 존재 여부. 가져오기 시 첫 행을 헤더로 인식, 내보내기 시 컬럼명을 헤더로 생성 |
| `-D`, `--delimiter=DELIMITER` | 필드 구분자 (기본값: `,`) |
| `-n`, `--newline=NEWLINE` | 레코드 구분자 (기본값: `\n`) |
| `-e`, `--enclosure=ENCLOSURE` | 필드 인클로저 문자 |
| `-r`, `--format=FORMAT` | 파일 포맷 (기본값: csv) |
| `-E`, `--encoding=CHARSET` | 파일 인코딩. UTF8(기본값), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16 |
| `-F`, `--dateformat=DATEFORMAT` | datetime 컬럼 날짜 형식. `unixtimestamp` 또는 `nanotimestamp` 지정 가능 |
| `-z`, `--timezone` | 타임존 설정. 예: `+0900`, `-1230` |
| `-a`, `--atime` | `_ARRIVAL_TIME` 컬럼 포함 여부 (기본값: 미포함) |
| `-C`, `--create` | 가져오기 시 테이블이 없으면 자동 생성 |
| `-l`, `--log=LOG_FILE` | 실행 로그 파일 |
| `-b`, `--bad=BAD_FILE` | 가져오기 실패 행을 기록하는 bad 파일 |
| `--first=FIRST_ROW` | 처리를 시작할 첫 번째 행 번호 |
| `-I`, `--silent` | 배너 및 진행 상태 출력 없이 실행 |
| `-S`, `--slash` | 백슬래시 구분자 지정 |
| `--summary` | 선택된 옵션 값을 출력하고 종료 (실제 처리 안 함) |
| `-h`, `--help` | 옵션 목록 출력 |

## CSV 파일 가져오기

기본 가져오기:

```bash
machloader -i -d data.csv -t sensor_data
```

서버 접속 정보 지정:

```bash
machloader -i -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -d data.csv -t sensor_data
```

헤더 행이 있는 CSV 가져오기:

```bash
machloader -i -d data.csv -t sensor_data -H
```

기존 데이터 삭제 후 가져오기 (replace 모드):

```bash
machloader -i -d data.csv -t sensor_data -m replace
```

특정 행부터 시작:

```bash
machloader -i -d data.csv -t sensor_data --first=10
```

## CSV 파일 내보내기

```bash
machloader -o -d output.csv -t sensor_data
machloader -o -d output.csv -t sensor_data -H
```

`_ARRIVAL_TIME` 컬럼 포함 내보내기:

```bash
machloader -o -d output.csv -t sensor_data -a
```

### ARRAY 컬럼

Machbase DBMS 8.7.0의 ARRAY 컬럼은 `[value,null,value]` 형식으로 가져오고 내보냅니다.
쉼표가 ARRAY 내부에 포함되므로 CSV 필드를 enclosure로 감쌉니다.

```csv
1,"[1.5,null,3.5,4.5]"
```

NULL field는 whole NULL이고 `"[null,null]"`은 모든 요소가 NULL인 non-NULL ARRAY입니다.
`-C` 자동 테이블 생성은 ARRAY 타입을 추론하지 않으므로 ARRAY 컬럼이 필요한 테이블은
먼저 명시적으로 생성합니다. 자세한 타입과 NULL 규칙은
숫자 ARRAY 타입을 참고하십시오.

## 인코딩 및 구분자 설정

EUC-KR 인코딩, 탭 구분자:

```bash
machloader -i -d data.txt -t table_name -E MS949 -D '\t'
```

파이프(`|`) 구분자:

```bash
machloader -i -d data.txt -t table_name -D '|'
machloader -o -d data.txt -t table_name -D '|'
```

## 타임존 지정

```bash
machloader -i -d data.csv -t sensor_data -z +0900
machloader -i -d data.csv -t sensor_data -z -1230
```

## datetime 형식 지정

커맨드라인에서 직접 지정:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "_arrival_time YYYY-MM-DD HH24:MI:SS"
```

Unix 타임스탬프로 입력:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column unixtimestamp"
```

나노초 타임스탬프로 입력:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column nanotimestamp"
```

## 스키마 파일 사용

스키마 파일을 생성합니다:

```bash
machloader -c -t sensor_data -f sensor_data.fmt
```

스키마 파일로 가져오기/내보내기:

```bash
machloader -i -f sensor_data.fmt -d data.csv
machloader -o -f sensor_data.fmt -d output.csv
```

스키마 파일 형식 예시 (`sensor_data.fmt`):

```
table sensor_data
{
    name   varchar(64);
    time   datetime;
    value  double;
}
DATEFORMAT time "YYYY-MM-DD HH24:MI:SS"
```

특정 컬럼 무시:

```
table sensor_data
{
    id     integer;
    name   varchar(64);
    extra  varchar(32) IGNORE;
}
```

## 로그 및 bad 파일

```bash
machloader -i -d data.csv -t sensor_data \
    -l import.log -b import.bad
```

- `-l`: 가져오기 실행 로그(성공/실패 통계)
- `-b`: 실패한 행 데이터를 원본 형식으로 기록

## 자동 테이블 생성

테이블이 없을 때 자동으로 생성합니다. 컬럼명은 `c0`, `c1`, ... 순서로, 타입은 `varchar(32767)`로 생성됩니다.

```bash
machloader -i -d data.csv -t new_table -C
machloader -i -d data.csv -t new_table -C -H   # 헤더를 컬럼명으로 사용
```

## 사용 예시

```bash
# 실제 가져오기 전 설정 확인 (--summary)
machloader -i -d data.csv -t sensor_data --summary

# 대용량 파일 가져오기 (로그 및 bad 파일 지정)
machloader -i -d bigdata.csv -t sensor_data \
    -H -z +0900 \
    -l import_20240101.log -b import_20240101.bad

# 전체 테이블 내보내기
machloader -o -d export_20240101.csv -t sensor_data -H -a
```
