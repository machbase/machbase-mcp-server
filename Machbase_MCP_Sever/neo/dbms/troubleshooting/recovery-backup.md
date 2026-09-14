# 백업과 복구 문제

## 백업과 복원이 실패할 때

백업 실패 시 서버 프로세스 OS 계정의 경로 권한, 사용 가능 공간, 동일 경로의 기존 백업,
서버 로그를 확인합니다.

```sql
SELECT * FROM V$STORAGE_USAGE;
```

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

복원은 기존 물리 데이터베이스를 교체하는 파괴적 작업입니다. 실행 중인 서버를 정지하는 것만으로
충분하지 않으며, 현재 데이터베이스가 존재하면 복원이 거부됩니다. 다음 순서는 개념적 점검표이며
운영 명령으로 그대로 복사하지 마십시오.

```text
1. 복구 대상·백업 경로·버전·체크섬을 확인한다.
2. 현재 database의 보존 방법과 되돌림 조건을 승인받는다.
3. 서버를 정상 종료한다.
4. 현재 물리 database를 제거하는 승인된 절차를 수행한다.
5. machadmin restore를 실행한다.
6. 서버를 시작하고 업무 검증 쿼리를 수행한다.
```

`machadmin -d`는 현재 데이터베이스를 파기하므로 백업과 명시적 승인 없이 실행해서는 안 됩니다.
정확한 복원 구문과 제약은
BACKUP/RESTORE/MOUNT 문법을
참고하십시오.

백업 이미지 확인이나 MOUNT 성공은 1차 검증일 뿐 완전한 복구 가능성을 보장하지 않습니다.
별도 환경에서 복원과 애플리케이션 검증까지 정기적으로 수행합니다.

## 마운트가 실패할 때

현재 MOUNT 목록, 고유한 별칭, 백업 경로와 서버 프로세스의 읽기 권한을 확인합니다.

```sql
SELECT * FROM V$STORAGE_MOUNT_DATABASES;
```

현행 구문은 백업 경로 뒤에 별칭을 지정합니다.

```sql
MOUNT DATABASE '/backup/sc15_snapshot' TO backup_check;
SELECT COUNT(*) FROM backup_check.sys.target_table;
UMOUNT DATABASE backup_check;
```

동일 별칭 충돌, 지원하지 않는 Edition, 호환되지 않는 백업, 사용 중인 마운트된 데이터베이스를
구분해 처리합니다. 강제로 파일을 삭제하거나 서버 메타데이터를 수정하지 마십시오.
