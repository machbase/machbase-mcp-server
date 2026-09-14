# Machbase Neo SQL Backup and Mount

## 소개

흔히 "산업 빅데이터"라 부르거나 Smart-X 사업과 함께 언급되는 시계열 데이터의 폭발적 증가는 기존 데이터 관리 전략에 큰 부담을 줍니다. 방대한 센서 측정값을 지속적으로 저장하려면 데이터 보관, 재해 복구, 이력 분석을 위한 견고한 수단이 필요합니다. 일반적인 데이터베이스 백업·복원 절차는 필수적이긴 하지만 범위 지정의 유연성이 떨어지고 복원 시간이 길며, 전체 복원 없이는 백업 내용을 볼 수 없다는 한계가 있어 운영에 지장을 주고 자원을 많이 소모합니다.

Machbase는 시계열 데이터 작업에 맞춘 포괄적이고 유연한 백업·마운트 기능으로 이 문제를 해결합니다. 여러 백업 전략(전체, 증분, 시간 기준, 테이블 단위)을 제공하며, 특히 시간이 오래 걸리는 복원 없이 백업 데이터를 온라인으로 읽을 수 있는 **마운트** 기능을 제공합니다.

## 핵심 개념

*   **백업(Backup):** 데이터베이스 데이터(전체 또는 특정 테이블/시간 범위)를 외부 저장소에 물리적으로 복사하는 작업입니다. Machbase 백업은 필요한 데이터와 메타데이터 파일을 담은 디렉토리 구조로 저장됩니다.
*   **복원(Restore):** 백업의 데이터를 다시 운영 중인 Machbase 인스턴스로 복사하는 작업입니다. 보통 기존 데이터를 덮어쓰며 주로 재해 복구나 복제 환경 구축에 사용합니다.
*   **마운트(Mount):** 백업 디렉토리 구조를 실행 중인 Machbase 인스턴스에 임시 읽기 전용 데이터베이스로 붙이는 Machbase 고유 기능입니다. 긴 복원 작업 없이도 백업에 담긴 "화석화된" 과거 데이터를 곧바로 조회할 수 있습니다.
*   **언마운트(Unmount):** 마운트한 백업 데이터베이스를 분리하는 작업입니다. 연결만 해제하며 백업 파일은 삭제하지 않습니다.
*   **라이브 데이터(Live Data):** 운영 중인 Machbase 인스턴스의 현재 활성 데이터로, 실시간 읽기·쓰기의 대상입니다.
*   **화석화된 데이터(Fossilized Data):** 백업에 담긴 데이터로, 특정 시점(또는 시간 범위)의 변경 불가능한 스냅샷입니다. 마운트하면 읽기만 가능합니다.

## 백업 작업

Machbase는 백업 과정을 세밀하게 제어할 수 있어 요구 사항에 맞는 범위와 방식을 고를 수 있습니다.

### 전체 백업(데이터베이스 또는 테이블)

실행 시점의 데이터베이스 인스턴스 전체 또는 지정한 테이블의 완전한 사본을 만듭니다.

**Syntax:**

데이터베이스 백업:

```sql
BACKUP DATABASE INTO DISK = 'path/to/backup_directory_name';
```

테이블 백업:

```sql
BACKUP TABLE table_name INTO DISK = 'path/to/backup_directory_name';
```

*   `DATABASE`: 데이터베이스 인스턴스 전체를 백업합니다.
*   `TABLE table_name`: 지정한 테이블만 백업합니다.
*   `INTO DISK = 'path/...'`: 백업 파일을 만들 대상 디렉토리를 지정합니다. 절대 경로이거나 `$MACHBASE_HOME/dbs` 기준 상대 경로일 수 있습니다. 지정한 디렉토리가 없으면 새로 만듭니다.

**고려 사항:**
*   전체 백업은 백업 작업이 시작된 시점의 데이터 상태를 담습니다.
*   결과물은 데이터베이스 구조를 나타내는 여러 파일과 하위 디렉토리가 담긴 디렉토리입니다.

### 증분 백업(데이터베이스 또는 테이블)

이전 백업(보통 전체 백업 또는 앞선 증분 백업) 이후 변경된 데이터만 담습니다. 이후 백업의 소요 시간과 저장 공간을 크게 줄여 줍니다.

**Syntax:**

데이터베이스 증분 백업:

```sql
BACKUP DATABASE AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';
```

테이블 증분 백업:

```sql
BACKUP TABLE table_name AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';
```

*   `AFTER 'path/...'`: 백업 사슬에서 *바로 앞* 백업(전체 또는 증분)의 디렉토리 경로를 지정합니다. 이 경로는 반드시 존재하고 접근 가능해야 **합니다**.
*   `INTO DISK = 'path/...'`: *새* 증분 백업 파일이 저장될 대상 디렉토리를 지정합니다.

**고려 사항:**
*   주로 데이터가 추가되기만 하는 Log·Tag 테이블에 적용됩니다.
*   Lookup 테이블은 추가 외의 수정이 일어날 수 있으므로 증분 작업 중에도 **항상** 전체 백업됩니다.
*   이전 백업 디렉토리가 온전히 존재해야 합니다.

### 시간 기준 백업(데이터베이스 또는 테이블)

특정 시간 구간의 데이터만 백업할 수 있습니다. 날짜 범위 기준으로 과거 시계열 데이터를 보관할 때 특히 유용합니다.

**Syntax:**

데이터베이스 시간 범위 백업:

```sql
BACKUP DATABASE
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';
```

테이블 시간 범위 백업:

```sql
BACKUP TABLE table_name
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';
```

*   `FROM time_expression_start`: 백업 구간의 시작 시각을 지정합니다(경계 포함, 예: `TO_DATE('YYYY-MM-DD HH24:MI:SS')`).
*   `TO time_expression_end`: 백업 구간의 끝 시각을 지정합니다(경계 포함).

**고려 사항:**
*   큰 시계열 테이블을 다루기 쉬운 백업 단위(예: 월별, 분기별)로 나눌 때 적합합니다.

## 마운트 작업

마운트 기능은 복원 없이 백업 데이터를 읽기 전용으로 접근하게 해 줍니다.

### 백업 마운트하기

백업 디렉토리를 실행 중인 Machbase 인스턴스에 조회 가능한 읽기 전용 데이터베이스로 붙입니다.

**Syntax:**

```sql
MOUNT DATABASE 'path/to/backup_directory' TO mount_name;
```

*   `'path/to/backup_directory'`: Machbase 백업 파일이 담긴 디렉토리의 전체 경로입니다(`BACKUP ... INTO DISK`로 생성).
*   `mount_name`: 마운트한 데이터베이스에 사용자가 붙이는 별칭입니다. 마운트한 데이터를 조회할 때 객체 이름 앞에 이 이름을 씁니다.

**고려 사항:**
*   Machbase 서버 프로세스가 백업 디렉토리 경로에 읽기 권한을 가지고 있어야 합니다.
*   여러 백업을 동시에 마운트할 수 있으며, 각각 고유한 `mount_name`을 사용합니다.

### 마운트한 데이터 조회

마운트한 백업의 테이블에 접근하려면 테이블 이름 앞에 마운트 이름과 원래 스키마/사용자 이름(일반 테이블은 보통 `sys`)을 붙여야 합니다.

**Syntax:**

```sql
SELECT column_list
FROM mount_name.user_name.table_name
WHERE [conditions];
```

*   `mount_name`: `MOUNT DATABASE` 명령에서 지정한 별칭입니다.
*   `user_name`: 원래 테이블의 스키마 소유자입니다(보통 `sys`).
*   `table_name`: 백업 안의 테이블 이름입니다.

**Example:**

```sql
-- Querying table 'sensor_data' (owned by 'sys') from a backup mounted as 'backup_jan'
SELECT *
FROM backup_jan.sys.sensor_data
WHERE time BETWEEN TO_DATE('2024-01-05') AND TO_DATE('2024-01-06');
```

### 백업 언마운트하기

마운트한 백업 데이터베이스를 분리해 마운트 지점으로 더 이상 접근할 수 없게 합니다. 백업 파일 자체는 디스크에 그대로 남습니다.

**Syntax:**

```sql
UNMOUNT DATABASE mount_name;
```

*   `mount_name`: 분리할 마운트 데이터베이스의 별칭입니다.

## 복원 작업

복원은 현재 데이터베이스 상태를 백업에 담긴 상태로 대체합니다. 주로 재해 복구나 동일한 인스턴스를 구축할 때 사용합니다.

**문법(`machbase-neo` 유틸리티 사용):**

```bash
machbase-neo restore --data <machbase_home_dir> <path/to/backup_directory>
```

*   `--data <machbase_home_dir>`: 복원을 수행할 대상 Machbase 인스턴스의 `$MACHBASE_HOME` 디렉토리를 지정합니다. **주의: 이 작업은 보통 대상 인스턴스의 기존 데이터를 덮어씁니다.**
*   `<path/to/backup_directory>`: 복원에 사용할 백업 디렉토리의 경로입니다.
    *   전체 복원이면 전체 백업의 디렉토리입니다.
    *   증분 백업이 포함된 복원이면 사슬의 **마지막** 증분 백업 디렉토리 경로여야 **합니다**. `restore` 과정이 사슬의 앞선 백업들(전체 백업과 중간 증분 백업)을 자동으로 찾아 사용합니다.

**고려 사항:**
*   복원은 오프라인 작업이며, 기존 데이터베이스 상태를 덮어쓰므로 운영 중인 인스턴스에서는 신중히 다뤄야 합니다.
*   의도치 않은 데이터 손실을 막기 위해 대상 `$MACHBASE_HOME`이 올바른지 확인하세요.
*   백업 데이터에 읽기·쓰기가 필요하면 전체 복원을 해야 합니다. 마운트 기능은 읽기 전용 접근만 제공합니다.

## 마운트의 장점과 고려 사항

### Advantages

*   **빠른 데이터 접근:** 백업 안의 과거 데이터에 거의 즉시 접근할 수 있어, 특히 수 테라바이트 규모에서 오래 걸리던 기존 복원 과정을 생략할 수 있습니다.
*   **인덱스 보존:** 백업은 원래의 시계열 인덱스 구조를 그대로 유지합니다. 마운트한 데이터베이스는 이 인덱스를 활용하므로 과거 데이터도 라이브 데이터에 준하는 성능으로 조회할 수 있습니다.
*   **롤업 구조 보존:** 백업 대상 테이블에 연결된 롤업 테이블도 백업에 함께 보존되어 마운트 지점을 통해 조회할 수 있습니다. 덕분에 라이브 데이터와 과거("화석화된") 데이터에 대해 일관된 통계 분석이 가능합니다.
*   **온라인 작업:** 마운트와 언마운트는 주 데이터베이스 인스턴스가 온라인으로 동작하는 중에 수행됩니다.
*   **자원 효율:** 과거 데이터를 조회하려고 전체 복원을 수행할 때 드는 막대한 디스크 I/O와 CPU 자원을 아낄 수 있습니다.

### 고려 사항

*   **읽기 전용 접근:** 마운트한 데이터베이스는 엄격히 읽기 전용입니다. `INSERT`, `UPDATE`, `DELETE`와 DDL 작업은 금지됩니다. 백업 상태를 수정해야 한다면 `RESTORE`가 필요합니다.
*   **`v$mount_table_STAT` 미제공:** 실시간 통계를 제공하는 시스템 뷰(`v$sys_table_STAT`에 대응하는 `v$mount_table_STAT` 같은 것)는 정적으로 마운트된 백업 데이터에는 일반적으로 적용되지 않거나 제공되지 않습니다. 건수나 집계가 필요하면 데이터를 직접 조회하세요.
*   **파일 시스템 접근:** Machbase 서버는 백업 디렉토리 위치에 파일 시스템 수준의 읽기 권한이 필요합니다.

## 예제

이 절에서는 백업과 마운트 흐름을 보여 주는 실전 시나리오를 다룹니다.

**준비:** `EQPT_A`와 `EQPT_B` 두 TAG 테이블이 있고 시계열 데이터가 들어 있다고 가정합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS EQPT_A (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) tag_partition_count=1;
```

```sql
CREATE TAG TABLE IF NOT EXISTS EQPT_B (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) tag_partition_count=1;
```

EQPT_A와 EQPT_B에 2024-01-01부터 2024-06-30까지의 데이터가 적재되어 있다고 가정합니다. 라이브 데이터 범위를 확인합니다:

```sql
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM EQPT_A;
```

```sql
SELECT COUNT(*) FROM EQPT_A;
```

### 예제 1: 데이터베이스 전체 백업과 마운트

**1단계.** 데이터베이스 전체 백업을 수행합니다:

```sql
BACKUP DATABASE INTO DISK = '/backup/full_db_20240630';
```

**2단계.** 별칭 'mount_fulldb'로 백업을 마운트합니다:

```sql
MOUNT DATABASE '/backup/full_db_20240630' TO mount_fulldb;
```

**3단계.** 마운트한 백업에서 데이터를 조회합니다. 시간 범위 확인:

```sql
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_fulldb.sys.EQPT_A;
```

행 수를 확인합니다:

```sql
SELECT COUNT(*) FROM mount_fulldb.sys.EQPT_A;
```

마운트한 EQPT_B에서 특정 데이터를 조회합니다:

```sql
SELECT name, TO_CHAR(time), value FROM mount_fulldb.sys.EQPT_B LIMIT 5;
```

**4단계.** 더 이상 접근이 필요 없으면 백업을 언마운트합니다:

```sql
UNMOUNT DATABASE mount_fulldb;
```

### 예제 2: 시간 범위 데이터베이스 백업과 마운트

**1단계.** 2024년 1월 1일부터 3월 31일까지의 데이터만 백업합니다:

```sql
BACKUP DATABASE
    FROM TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/db_2024Q1';
```

**2단계.** (선택) 라이브 테이블에서 오래된 데이터를 삭제해 데이터 노후화를 흉내 냅니다:

```sql
DELETE FROM EQPT_A BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

```sql
DELETE FROM EQPT_B BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

라이브 데이터 건수가 줄었는지 확인합니다:

```sql
SELECT COUNT(*) FROM EQPT_A;
```

**3단계.** 시간 범위 백업을 마운트합니다:

```sql
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;
```

**4단계.** 마운트한 백업을 조회합니다(1분기 원본 데이터가 들어 있어야 합니다):

```sql
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
```

```sql
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_q1.sys.EQPT_A;
```

라이브(삭제 후)와 마운트(삭제 전)의 건수를 비교합니다:

```sql
SELECT COUNT(*) AS live_count FROM EQPT_A;
```

```sql
SELECT COUNT(*) AS mounted_q1_count FROM mount_q1.sys.EQPT_A;
```

**5단계.** 백업을 언마운트합니다:

```sql
UNMOUNT DATABASE mount_q1;
```

### 예제 3: 테이블 단위 시간 범위 백업과 마운트

**1단계.** 2024년 4월 1일부터 5월 15일까지 EQPT_A 테이블만 백업합니다:

```sql
BACKUP TABLE EQPT_A
    FROM TO_DATE('2024-04-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-05-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/eqpta_20240401_20240515';
```

**2단계.** 테이블 단위 백업을 마운트합니다:

```sql
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;
```

**3단계.** 마운트한 백업을 조회합니다. 시간 범위를 확인합니다:

```sql
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_eqpta_partial.sys.EQPT_A;
```

Check count:

```sql
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
```

원본 데이터 샘플을 조회합니다:

```sql
SELECT name, TO_CHAR(time), value FROM mount_eqpta_partial.sys.EQPT_A LIMIT 5;
```

> 참고: 이 마운트에서 EQPT_B를 조회하려 하면 실패합니다(백업에 포함되지 않았습니다).

**4단계.** 백업을 언마운트합니다:

```sql
UNMOUNT DATABASE mount_eqpta_partial;
```

### 예제 4: 여러 백업을 동시에 마운트하기

앞선 예제의 백업들이 있다고 가정합니다: '/backup/db_2024Q1'(전체 DB, 1분기), '/backup/full_db_20240630'(전체 DB, 6월 30일까지), '/backup/eqpta_20240401_20240515'(EQPT_A만, 4월 1일~5월 15일).

**1단계.** 세 백업을 각각 고유한 별칭으로 마운트합니다:

```sql
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;
```

```sql
MOUNT DATABASE '/backup/full_db_20240630' TO mount_jun30;
```

```sql
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;
```

**2단계.** 여러 마운트에 걸쳐 데이터를 조회합니다. 1분기 백업의 EQPT_A 건수:

```sql
SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
```

전체 백업의 EQPT_B 건수:

```sql
SELECT COUNT(*) FROM mount_jun30.sys.EQPT_B;
```

부분 테이블 백업의 EQPT_A 건수:

```sql
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
```

**3단계.** 작업이 끝나면 모든 백업을 언마운트합니다:

```sql
UNMOUNT DATABASE mount_q1;
```

```sql
UNMOUNT DATABASE mount_jun30;
```

```sql
UNMOUNT DATABASE mount_eqpta_partial;
```
