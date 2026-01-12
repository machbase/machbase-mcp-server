# TRACE_LOG_LEVEL

When issues occur in Machbase server, detailed operations can be checked through log files.
You can control the log level output for each module by setting TRACE_LOG_LEVEL.

- **Default**: 277 (MM_1 + QP_1 + SM_1 + XM_1)
- **Range**: 0 ~ 524287
- **Dynamic**: Yes
- **Log File**: `$MACHBASE_HOME/trc/machbase.trc`

## Level Values

| Level | Value | Module |
|------|-----|------|
| MM_1 | 1 | Main Module log level 1 |
| MM_2 | 2 | Main Module log level 2 |
| QP_1 | 4 | Query Processor log level 1 |
| QP_2 | 8 | Query Processor log level 2 |
| SM_1 | 16 | Storage Manager log level 1 |
| SM_2 | 32 | Storage Manager log level 2 |
| CC_1 | 64 | Cluster coordinator log level 1 |
| CC_2 | 128 | Cluster coordinator log level 2 |
| XM_1 | 256 | Cluster query distribution log level 1 |
| XM_2 | 512 | Cluster query distribution log level 2 |
| LM_1 | 1024 | Cluster link management log level 1 |
| LM_2 | 2048 | Cluster link management log level 2 |
| RP_1 | 4096 | Cluster replication log level 1 |
| RP_2 | 8192 | Cluster replication log level 2 |
| MISC_1 | 65536 | Miscellaneous log level 1 |
| MISC_2 | 131072 | Miscellaneous log level 2 |
| DEBUG | 262144 | Debug |

## Configuration
```sql
-- Check current value
select name, value from v$property where name = 'TRACE_LOG_LEVEL';

-- Combine multiple levels (add values)
alter system set TRACE_LOG_LEVEL = {level1 + level2 + ...};
```