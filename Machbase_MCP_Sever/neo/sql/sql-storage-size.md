# Machbase Neo SQL Automatic Storage Management

## 소개

시계열 데이터베이스, 특히 다수의 소스에서 고빈도 데이터를 다루는 경우 데이터가 계속 쌓이는 문제에 직면합니다. 초당 수백만 건에 이를 수 있는 데이터 적재에는 상당한 저장 용량이 필요합니다. 시간이 지나면 디스크 사용량을 수동으로 모니터링하고 주기적으로 `DELETE`를 실행해 공간을 확보해야 하는데, 이는 운영 복잡도와 오류 가능성을 높입니다. 또한 많은 애플리케이션은 특정 기간 동안만 데이터를 보관하면 되고 그 이후의 오래된 데이터는 불필요해집니다.

이러한 문제를 해결하기 위해 Machbase는 **Retention Policy** 기능으로 자동 저장 용량 관리 메커니즘을 제공합니다. 정의된 보관 기간을 넘긴 데이터를 자동으로 삭제하는 선언적 방식으로, 저장 사용량을 예측 가능하게 유지하고 장기 데이터 수명 주기 관리를 단순화합니다.

## 핵심 개념: Retention Policy

Machbase의 Retention Policy는 지정한 테이블에서 시간 기준으로 데이터를 자동 삭제하는 규칙을 정의합니다. 두 가지 주요 파라미터로 동작합니다:

*   **Duration:** 테이블에 보관할 데이터의 최대 나이를 지정합니다. 정책 검사 시점의 시스템 시간을 기준으로 이 기간보다 오래된 데이터가 삭제 대상이 됩니다. 단위는 `MONTH` 또는 `DAY`로 지정합니다.
*   **Interval:** 정의된 `DURATION`에 따라 삭제 대상 데이터를 Machbase가 얼마나 자주 검사할지 결정합니다. 보관 정책 적용 프로세스의 실행 주기이며 `DAY` 또는 `HOUR` 단위로 설정합니다.

Retention Policy가 테이블에 적용되면 백그라운드 프로세스가 `INTERVAL`에 따라 주기적으로 테이블을 스캔합니다. 타임스탬프(구체적으로 `BASETIME` 컬럼의 값)가 현재 시스템 시간에서 지정한 `DURATION`을 뺀 시점보다 오래된 행을 찾아 자동으로 삭제합니다.

이 기능으로 데이터 보관을 관리하는 수명 주기는 다음과 같습니다:
1.  `DURATION`과 `INTERVAL`을 지정해 이름 있는 Retention Policy 객체를 생성합니다.
2.  생성한 Retention Policy를 하나 이상의 대상 테이블에 적용합니다.
3.  Machbase가 정책 일정에 따라 삭제 프로세스를 자동 실행합니다.
4.  해당 테이블에 자동 삭제가 더 이상 필요 없으면 정책을 분리합니다(선택).
5.  어떤 테이블에도 적용되어 있지 않으면 Retention Policy 객체 자체를 삭제합니다(선택).

## Retention Policy 생성

Retention Policy는 `CREATE RETENTION` 문으로 독립적인 데이터베이스 객체로 정의합니다.

**Syntax:**

```sql
CREATE RETENTION policy_name
    DURATION duration_value { MONTH | DAY }
    INTERVAL interval_value { DAY | HOUR };
```

*   `policy_name`: 이 보관 정책을 위해 사용자가 정하는 고유 식별자입니다.
*   `duration_value`: 데이터 보관 기간의 길이를 나타내는 정수입니다.
*   `MONTH | DAY`: `duration_value`의 시간 단위입니다.
*   `interval_value`: 삭제 검사 주기를 나타내는 정수입니다.
*   `DAY | HOUR`: `interval_value`의 시간 단위입니다.

**Examples:**

데이터를 1일 보관하고 1시간마다 검사하는 정책:

```sql
CREATE RETENTION policy_1d_1h
    DURATION 1 DAY
    INTERVAL 1 HOUR;
```

데이터를 1개월(근사) 보관하고 3일마다 검사하는 정책:

```sql
CREATE RETENTION policy_1m_3d
    DURATION 1 MONTH
    INTERVAL 3 DAY;
```

## 테이블에 Retention Policy 적용

Retention Policy를 생성한 뒤에는 `ALTER TABLE ... ADD RETENTION` 문으로 대상 테이블에 명시적으로 연결해야 합니다. 테이블 하나에는 한 번에 하나의 Retention Policy만 적용할 수 있습니다.

**Syntax:**

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

*   `table_name`: 정책을 적용할 테이블 이름입니다.
*   `policy_name`: 앞서 생성한 Retention Policy 객체의 이름입니다.

**Example:**

```sql
CREATE TAG TABLE sensor_data ( name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED );
```

sensor_data 테이블에 policy_1d_1h를 적용합니다:

```sql
ALTER TABLE sensor_data ADD RETENTION policy_1d_1h;
```

## Retention Policy 모니터링

정의된 Retention Policy와 적용 상태 정보는 시스템 카탈로그 뷰로 조회할 수 있습니다.

*   **`M$RETENTION`:** 데이터베이스에 정의된 모든 Retention Policy 객체와 그 이름, 설정된 `DURATION`·`INTERVAL` 값(내부적으로 초 단위)을 보여줍니다.

    ```sql
    -- View all defined retention policies
    SELECT * FROM M$RETENTION;
    ```

*   **`V$RETENTION_JOB`:** 어떤 정책이 어떤 테이블에 적용되어 있는지, 보관 작업의 상태(예: `WAITING`), 마지막 삭제 실행 시각(`LAST_DELETED_TIME`)을 보여줍니다.

    ```sql
    -- View retention policies currently applied to tables
    SELECT * FROM V$RETENTION_JOB;
    ```

## 정책 분리 및 제거

Retention Policy를 테이블에서 분리하면 해당 테이블의 자동 삭제가 중지됩니다. 이후 다른 테이블에도 적용되어 있지 않고 더 이상 필요 없다면 정책 객체 자체를 삭제할 수 있습니다.

### 테이블에서 분리

`ALTER TABLE ... DROP RETENTION` 문으로 테이블에서 정책 연결을 해제합니다.

**Syntax:**

```sql
ALTER TABLE table_name DROP RETENTION;
```

*   `table_name`: 현재 적용된 정책을 분리할 테이블 이름입니다.

### 정책 객체 제거

`DROP RETENTION` 문으로 정책 정의 자체를 삭제합니다. 정책이 아직 어떤 테이블에 적용되어 있으면 실패합니다.

**Syntax:**

```sql
DROP RETENTION policy_name;
```

*   `policy_name`: 삭제할 Retention Policy 객체의 이름입니다.

**의존성 예제:**

'policy_1d_1h'가 'sensor_data'에 적용되어 있다고 가정합니다. 사용 중인 정책을 삭제하려 하면 실패합니다:

```sql
DROP RETENTION policy_1d_1h;
```

> 예상 오류: `[ERR-02702: Policy (POLICY_1D_1H) is in use.]`

먼저 테이블에서 정책을 분리합니다:

```sql
ALTER TABLE sensor_data DROP RETENTION;
```

이제 정책 객체 삭제가 성공합니다:

```sql
DROP RETENTION policy_1d_1h;
```

## 예제

이 절에서는 Retention Policy 기능을 단계별로 사용하는 예제를 보여줍니다.

**1. 스키마 준비:**

```sql
DROP TABLE IF EXISTS ret_tag CASCADE;
```

샘플 TAG 테이블을 만듭니다(맥락상 Rollup을 포함했지만 Retention에는 필수가 아닙니다):

```sql
CREATE TAG TABLE ret_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(MIN) TAG_PARTITION_COUNT=1;
```

**2. Retention Policy 생성:**

데이터를 1일 보관하고 매시간 검사하는 정책을 정의합니다:

```sql
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
```

정책 생성을 확인합니다:

```sql
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
```

**3. 테이블에 정책 적용:**

생성한 정책을 'ret_tag' 테이블에 적용합니다:

```sql
ALTER TABLE ret_tag ADD RETENTION policy_1d_1h;
```

정책 적용을 확인합니다(예상: RET_TAG, POLICY_1D_1H, 상태 WAITING, 초기 last_deleted_time은 NULL인 행):

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
```

**4. 데이터 적재(오래된 데이터 포함):**

```tql
-- Use TQL FAKE function to simulate loading 150,000 records
-- spanning roughly the last 2 days (some older than 1 day).
-- Adjust timeAdd parameters as needed to ensure data older than DURATION exists.
FAKE(range(1, 150000, 1))
MAPVALUE(1, sin((2*PI*value(0)/100))) -- Sample value generation
MAPVALUE(0, timeAdd("now-2d", strSprintf("+%.fs", value(0)*100))) -- Generate timestamps over ~2 days ending now
PUSHVALUE(0, "sensor-a") -- Assign a tag name
APPEND(table("ret_tag")) -- Append to the target table
```

**5. 초기 적재 확인:**

입력된 전체 레코드 수를 확인합니다(예상: 150000 또는 그에 근접):

```sql
SELECT COUNT(*) FROM ret_tag;
```

**6. 보관 정책 실행 대기:**

정책의 `INTERVAL`(이 경우 1시간)보다 긴 시간을 기다립니다. 백그라운드 보관 작업이 자동으로 실행됩니다.

**7. 데이터 삭제 확인:**

보관 작업 상태를 다시 확인합니다(LAST_DELETED_TIME이 갱신되었을 수 있습니다):

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
```

레코드 수를 다시 확인합니다(예상: 1일보다 오래된 레코드가 삭제되어 150000보다 작은 수):

```sql
SELECT COUNT(*) FROM ret_tag;
```

**8. 정책 분리 및 삭제:**

'ret_tag'의 자동 삭제를 중지합니다:

```sql
ALTER TABLE ret_tag DROP RETENTION;
```

분리를 확인합니다(ret_tag 행이 사라져야 합니다):

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
```

정책 정의 자체를 제거합니다:

```sql
DROP RETENTION policy_1d_1h;
```

제거를 확인합니다(예상: 반환 행 없음):

```sql
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_1D_1H';
```
