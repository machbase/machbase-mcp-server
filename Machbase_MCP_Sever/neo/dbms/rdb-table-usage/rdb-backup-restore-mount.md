# TRANSACTION 백업, 복원, 마운트

백업 명령이 성공했다고 복구 준비가 끝난 것은 아닙니다.
특히 운영 테이블과 백업 테이블의 이름이 같으면 잘못된 쪽을 조회하고도 검증이 끝났다고
생각하기 쉽습니다. 백업 이후 운영 값을 바꾸어 두 결과가 다른지 확인하는 방법으로
검증해 보겠습니다.

## 백업·복원 지원 범위

| 작업 | TRANSACTION 관련 기준 |
|---|---|
| BACKUP DATABASE | 대상 범위의 영속 TRANSACTION 데이터 포함 |
| BACKUP TABLE | 지정한 테이블과 필요한 메타데이터 백업 |
| 증분 백업 | TRANSACTION 저장소는 그 백업 시점의 전체 스냅샷으로 포함 |
| MOUNT DATABASE | 백업을 읽기 전용으로 조회 |
| 오프라인 인스턴스 복원 | 서버를 중단하고 machadmin -r 사용 |
| 온라인 논리 데이터베이스 복원 | 지원되는 논리 백업을 RESTORE DATABASE로 복원 |

증분 백업의 TRANSACTION 데이터를 변경 행만의 델타라고 계산하지 마세요.
내부 파일을 직접 복사하는 대신 지원되는 백업 명령을 사용해야 합니다.
TRANSACTION이 포함된 백업을 Cluster에서 사용하기 위한 우회 경로로 삼을 수도 없습니다.

## 백업과 마운트 검증

이 실습은 검증용 Standard 환경의 SYS 계정을 기준으로 합니다.
백업·마운트 권한과 서버 파일 접근 권한이 필요합니다.
경로는 서버 기준 예시이며 실행할 때마다 존재하지 않는 새 경로로 바꾸세요.
상위 디렉터리와 여유 공간을 확인하고, 경로를 재사용하려고 기존 백업을 삭제하지 마세요.

```sql
CREATE TRANSACTION TABLE ch8_backup (
    id     LONG PRIMARY KEY,
    code   VARCHAR(32) NOT NULL,
    amount DECIMAL(18,2)
);
CREATE UNIQUE INDEX ch8_backup_code ON ch8_backup(code);
INSERT INTO ch8_backup VALUES (1, 'A', 10.25);
INSERT INTO ch8_backup VALUES (2, 'B', 20.50);

BACKUP TABLE ch8_backup INTO DISK = '/backup/ch8_table_20260907_a';

UPDATE ch8_backup SET amount = 99.00 WHERE id = 1;

MOUNT DATABASE '/backup/ch8_table_20260907_a' TO ch8_bak;

SELECT id, code, amount FROM ch8_bak.SYS.ch8_backup ORDER BY id;
SELECT id, code, amount FROM ch8_backup ORDER BY id;
```

백업 쪽은 10.25·20.50, 운영 쪽은 99.00·20.50입니다.
마운트 조회는 `마운트명.소유자.테이블명`의 세 부분 이름을 사용합니다.
다른 소유 계정으로 실습했다면 SYS 부분도 실제 소유자에 맞춰야 합니다.

실수하기 쉬운 부분은 `SELECT ... FROM ch8_backup`만 실행하는 것입니다.
이것은 마운트 백업 검증이 아니라 현재 연결의 운영 테이블 조회입니다.
백업에 포함하지 않은 다른 테이블이 당연히 있어야 한다고 기대하지도 마세요.

마운트는 읽기 전용이며 UPDATE·DDL을 수행하는 복구 환경이 아닙니다.
검증을 마치고 열린 커서를 정리한 뒤 마운트를 해제합니다.

```sql
UMOUNT DATABASE ch8_bak;
DROP TABLE ch8_backup;
```

이 정리는 실습 테이블과 마운트만 제거합니다.
백업 디렉터리는 남겨 두었으므로 이후 보관 정책에 따라 별도로 관리하세요.

## 복원 검증 항목

격리된 복원 환경에서는 소유자, 행 수, 업무 키, 금액 합계와 대표 JSON 값을 확인하세요.
PRIMARY KEY·UNIQUE INDEX가 남아 있는지, 필요한 권한과 애플리케이션의
COMMIT·ROLLBACK 흐름이 정상인지도 점검합니다.
마운트 조회만으로 실제 쓰기 복구 검증까지 완료한 것은 아닙니다.

온라인 RESTORE DATABASE는 논리 백업과 대상 데이터베이스 조건을 따릅니다.
여러 데이터베이스를 포함한 전체 인스턴스 이미지와 혼동하지 마세요.
기존 인스턴스를 지우는 오프라인 복원이나 REPLACE는 이 실습에 포함하지 않습니다.
복원 문법과
운영 절차에서
권한·중단·대상 교체 조건을 확인한 뒤 별도로 실행하세요.

여러 테이블의 업무 일관성까지 검증해야 한다면 백업 명령의 성공만으로 판단하지 마세요.
쓰기 중단·업무 기준 시점과 교차 테이블 검증 기준을 함께 정하는 것이 좋습니다.
