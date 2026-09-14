# 백업/마운트 지원표

백업은 데이터를 파일로 저장하고, 마운트는 저장된 백업 파일을 데이터베이스에 연결하여 조회하는 기능입니다.

## Edition별 지원 여부

| 기능 | Standard | Cluster | 비고 |
|------|:--------:|:-------:|------|
| 논리 다중 데이터베이스 | O | X | Standard Edition 전용 |
| BACKUP DATABASE | O | O | 전체 데이터베이스 백업 |
| BACKUP TABLE | O | O | 특정 테이블만 백업 |
| MOUNT DATABASE | O | X | Cluster Edition 미지원 |
| UMOUNT DATABASE | O | X | Cluster Edition 미지원 |
| machadmin -r 복구 | O | X | Cluster Edition 미지원 |

`BACKUP DATABASE database_name INTO DISK`는 하나의 active logical database를 백업합니다.
여러 active database가 포함된 full-instance image는 logical `MOUNT`/`RESTORE DATABASE`의
입력으로 사용할 수 없습니다. mounted database 조회에는 `USAGE`와 table `SELECT`가
필요하며 `USE`와 쓰기는 지원하지 않습니다.

## 테이블 타입별 백업 지원

| 테이블 유형 | BACKUP 지원 | MOUNT 후 조회 | 비고 |
|------------|:-----------:|:------------:|------|
| TAG 테이블 | O | O | |
| LOG 테이블 | O | O | |
| LOOKUP 테이블 | O | O | |
| TRANSACTION 테이블 | O | O | |
| VOLATILE 테이블 | X | X | 메모리 기반으로 백업 불가 |

## 정본

- 문법: BACKUP · RESTORE · MOUNT
- 운영 절차: 백업, 복원, 마운트
