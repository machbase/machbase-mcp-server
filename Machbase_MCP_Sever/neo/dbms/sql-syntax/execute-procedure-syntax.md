# EXEC procedure와 ROLLUPGAP

Machbase가 공개하는 table·ROLLUP 제어 procedure와 machsql 상태 명령을 설명합니다.

## 공통 EXEC 형식

```text
execute_procedure_stmt ::=
    'EXEC' procedure_name [ '(' argument_list ')' ]
```

procedure별 인자 수는 고정됩니다. 이름이 없거나, 인자 수·타입이 다르거나, 대상 객체가
존재하지 않으면 오류를 반환합니다.

## TABLE_FLUSH

```sql
EXEC TABLE_FLUSH(table_name);
```

| 항목 | 계약 |
|---|---|
| 인자 | table 이름 1개 |
| Edition | Standard, Cluster |
| 동작 | table의 pending storage/input buffer를 명시적으로 flush |
| 반환 | ResultSet 없이 statement 성공 또는 오류 반환 |
| 오류 | table 없음, 접근 불가, flush 처리 실패 |

검증이나 운영상 명시적인 storage flush가 필요할 때 사용합니다. transaction commit 또는 조회
가시성을 보장하는 수단은 아닙니다. 입력 row마다 호출하면 flush 비용이 증가하므로 반복 호출하지
않습니다.

## INDEX_FLUSH

```sql
EXEC INDEX_FLUSH(table_name);
EXEC INDEX_FLUSH(table_name, index_name);
```

table 이름만 지정하면 그 table의 모든 index build가 끝날 때까지 기다립니다. index 이름도
지정하면 해당 index만 대상으로 하며, 지정한 index가 해당 table에 속하지 않으면 오류입니다.
ResultSet은 반환하지 않습니다.

## TABLE_REFRESH

```sql
EXEC TABLE_REFRESH(lookup_table_name);
```

| 항목 | 계약 |
|---|---|
| 인자 | LOOKUP table 이름 1개 |
| Edition | Standard, Cluster |
| 동작 | 영속 LOOKUP 내용을 runtime memory table에 다시 반영 |
| 이름 범위 | 현재 database의 table, `owner.table` 허용 |
| 권한 | table owner 또는 허용된 관리 사용자 |
| 쓰기 제한 | READ ONLY database에서는 실행할 수 없음 |
| 반환 | ResultSet 없이 statement 성공 또는 오류 반환 |
| 오류 | LOOKUP 이외의 table, table 없음, write admission 실패 |

실행 전 진행 중인 LOOKUP 변경과 조회 영향을 확인하고, 완료 후 row 수와 대표 key를 다시
조회합니다.

## FREEZE_TAG_INDEX와 UNFREEZE_TAG_INDEX

```sql
EXEC FREEZE_TAG_INDEX(tag_table_name);
EXEC UNFREEZE_TAG_INDEX(tag_table_name);
```

TAG table의 tag index를 freeze하거나 다시 해제하는 1인자 procedure입니다. TAG 이외의 table에는
사용할 수 없습니다. index 유지보수 경계를 직접 제어하는 운영 명령이므로 일반 입력 경로에서
상시 사용하지 말고, 실패 시 반드시 `UNFREEZE_TAG_INDEX` 실행 여부를 확인합니다. 두 명령 모두
ResultSet 없이 statement 성공 또는 오류를 반환합니다.

## ROLLUP_START와 ROLLUP_STOP

```sql
EXEC ROLLUP_START;
EXEC ROLLUP_START(rollup_name);

EXEC ROLLUP_STOP;
EXEC ROLLUP_STOP(rollup_name);
```

두 procedure 모두 0인자와 rollup 이름 1인자 형식을 지원합니다. 이름을 지정하면 해당
ROLLUP을, 생략하면 현재 사용자 범위의 ROLLUP을 제어합니다. SYS의 무인자 실행은 전체 사용자
범위에 적용될 수 있으므로 대상 확인과 변경 승인이 필요합니다.

존재하지 않는 ROLLUP, 이미 시작한 대상의 START, 이미 중지한 대상의 STOP은 오류입니다.
`V$ROLLUP.RUN_STATE`로 변경 결과를 확인합니다.

## ROLLUP_FORCE

```sql
EXEC ROLLUP_FORCE;
EXEC ROLLUP_FORCE(rollup_name);
```

0인자 형식은 현재 사용자 범위의 기본 SEC→MIN→HOUR 계층을 처리합니다. 이름을 지정하면 해당
ROLLUP source의 현재 END_RID까지 따라잡도록 기다리는 동기 경로입니다. 중지된 ROLLUP은 먼저
START 상태인지 확인합니다.

완료 뒤 `V$ROLLUP`과 `SHOW ROLLUPGAP`으로 모든 관련 source 단계의 gap을 확인합니다.

## ROLLUP_REBUILD

태그와 시간 범위를 받는 4인자 Standard 전용 procedure입니다. 자세한 계약은
ROLLUP_REBUILD를 정본으로 사용합니다.

## SHOW ROLLUPGAP

```sql
SHOW ROLLUPGAP;
```

`SHOW ROLLUPGAP`은 서버 SQL이 아니라 **machsql 전용 client 명령**입니다. JDBC, ODBC와 SDK의
일반 SQL 실행 API에 같은 문자열을 보내지 마십시오.

Standard 출력에는 source·ROLLUP table, source END_RID, ROLLUP END_RID, `GAP`, 상태와 wakeup
시간이 포함됩니다. Cluster 출력에는 `HOSTNAME`이 추가되어 노드별 상태를 표시합니다.
`GAP = SRC_END_RID - ROLLUP_END_RID`이며, 계층의 모든 source→ROLLUP 행이 0인지 확인해야
전체 계층이 따라잡았다고 판단할 수 있습니다.

## 관련 문서

- ROLLUP 운영과 상태
- V$ROLLUP 사전
- machsql 명령
