# csvimport / csvexport 명령/옵션 사전

`csvimport`와 `csvexport`는 CSV 파일 전용 간편 가져오기/내보내기 래퍼 도구입니다. `machloader`의 CSV 관련 옵션을 단순화하여 제공하며, 아래에서 명시되지 않은 옵션은 `machloader`와 동일하게 사용할 수 있습니다.

## csvimport

CSV 파일을 Machbase 테이블로 가져옵니다.

### csvimport 옵션 목록

| 옵션 | 설명 |
|------|------|
| `-t`, `--table=TABLE_NAME` | 대상 테이블 이름 |
| `-d`, `--data=DATA_FILE` | 가져올 CSV 파일 이름 |
| `-s`, `--server=SERVER` | 서버 IP 주소 (기본값: 127.0.0.1) |
| `-P`, `--port=PORT` | 서버 포트 번호 (기본값: 5656) |
| `-u`, `--user=USER` | 사용자 이름 (기본값: SYS) |
| `-p`, `--password=PASSWORD` | 사용자 비밀번호 (기본값: MANAGER) |
| `-H` | CSV 파일의 첫 번째 행을 헤더로 인식하고 가져오기에서 제외 |
| `-C` | 테이블이 없을 때 자동 생성 (`-H`와 함께 사용 시 헤더를 컬럼명으로 사용) |
| `-m`, `--mode=MODE` | 가져오기 모드. `append`(기본값) 또는 `replace` |
| `-a`, `--atime` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-F`, `--dateformat=DATEFORMAT` | datetime 컬럼 날짜 형식 |
| `-l`, `--log=LOG_FILE` | 실행 로그 파일 |
| `-b`, `--bad=BAD_FILE` | 가져오기 실패 행을 기록하는 bad 파일 |
| `-I`, `--silent` | 배너 및 상태 출력 없이 실행 |

### csvimport 기본 사용법

테이블 이름과 파일 이름을 지정합니다.

```bash
csvimport -t table_name -d data.csv
```

옵션 없이 인수만으로도 실행할 수 있습니다 (순서 무관).

```bash
csvimport table_name data.csv
csvimport data.csv table_name
```

### 헤더 행 처리

CSV 파일의 첫 번째 행을 헤더로 인식하고 데이터에서 제외합니다.

```bash
csvimport -t table_name -d data.csv -H
```

### 자동 테이블 생성

테이블이 없을 때 자동으로 생성합니다.

```bash
# 컬럼명을 c0, c1, ... 으로 자동 생성
csvimport -t table_name -d data.csv -C

# CSV 헤더를 컬럼명으로 사용
csvimport -t table_name -d data.csv -C -H
```

자동 생성된 컬럼의 타입은 모두 `varchar(32767)`입니다.

### replace 모드

기존 데이터를 삭제하고 CSV 파일로 다시 채웁니다.

```bash
csvimport -t table_name -d data.csv -m replace
```

### 서버 접속 정보 지정

```bash
csvimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d data.csv
```

## csvexport

Machbase 테이블 데이터를 CSV 파일로 내보냅니다.

### csvexport 옵션 목록

| 옵션 | 설명 |
|------|------|
| `-t`, `--table=TABLE_NAME` | 내보낼 테이블 이름 |
| `-d`, `--data=DATA_FILE` | 저장할 CSV 파일 이름 |
| `-s`, `--server=SERVER` | 서버 IP 주소 (기본값: 127.0.0.1) |
| `-P`, `--port=PORT` | 서버 포트 번호 (기본값: 5656) |
| `-u`, `--user=USER` | 사용자 이름 (기본값: SYS) |
| `-p`, `--password=PASSWORD` | 사용자 비밀번호 (기본값: MANAGER) |
| `-H` | 컬럼 이름을 CSV 헤더로 생성 |
| `-a`, `--atime` | `_ARRIVAL_TIME` 컬럼 포함 |
| `-F`, `--dateformat=DATEFORMAT` | datetime 컬럼 날짜 형식 |
| `-l`, `--log=LOG_FILE` | 실행 로그 파일 |
| `-I`, `--silent` | 배너 및 상태 출력 없이 실행 |

### csvexport 기본 사용법

```bash
csvexport -t table_name -d output.csv
```

옵션 없이 인수만으로도 실행할 수 있습니다.

```bash
csvexport table_name output.csv
csvexport output.csv table_name
```

### 헤더 포함 내보내기

컬럼 이름을 CSV 파일의 첫 번째 행(헤더)으로 출력합니다.

```bash
csvexport -t table_name -d output.csv -H
```

### `_ARRIVAL_TIME` 포함 내보내기

```bash
csvexport -t table_name -d output.csv -a
```

## 사용 예시

```bash
# 기본 가져오기
csvimport -t sensor_data -d sensor_20240101.csv

# 헤더가 있는 CSV 가져오기
csvimport -t sensor_data -d sensor_20240101.csv -H

# 전체 내보내기 (헤더 포함)
csvexport -t sensor_data -d export_20240101.csv -H

# 로그 파일 지정하여 가져오기
csvimport -t sensor_data -d data.csv -H \
    -l import.log -b import.bad

# 원격 서버에서 내보내기
csvexport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d remote_export.csv -H -a
```
