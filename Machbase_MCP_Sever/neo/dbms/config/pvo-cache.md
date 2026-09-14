# PVO Cache 프로퍼티 사전

PVO Statement Cache는 SQL 파싱·검증·최적화 결과와 실행 계획을 재사용하여 반복 SQL의
처리 비용을 줄입니다. 공개 근거가 없는 약어 확장을 문서에서 정의하지 않습니다. Standard
Edition에서만 동작합니다.

## 프로퍼티 목록

| 프로퍼티 | 기본값 | 범위 | 동적 변경 | 설명 |
|----------|--------|------|----------|------|
| `PVO_CACHE_ENABLE` | 1 | 0~1 | 가능 | PVO Cache 활성화 여부. 0=비활성, 1=활성 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 268435456 | 32768~2^64-1 | 가능 | PVO Cache 전체 최대 메모리(바이트). 기본 256MB |
| `PVO_CACHE_SHARD_COUNT` | 16 | 1~256 | 불가 | Cache 샤드 수. 변경 시 서버 재시작 필요 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 | 0~2^64-1 | 가능 | Cache에 보관할 최대 SQL 엔트리 수. 0=무제한 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | 1~512 | 가능 | SQL 1개당 최대 플랜(핸들) 수 |

## 프로퍼티 상세

### PVO_CACHE_ENABLE

PVO Statement Cache 사용 여부를 설정합니다.

```
PVO_CACHE_ENABLE = 1
```

### PVO_CACHE_MAX_MEMORY_SIZE

PVO Cache 전체가 사용할 최대 메모리 크기(바이트)입니다. 설정된 값은 `PVO_CACHE_SHARD_COUNT`에 따라 균등 분배됩니다.

```
PVO_CACHE_MAX_MEMORY_SIZE = 536870912   # 512MB
```

### PVO_CACHE_SHARD_COUNT

Cache 내부 샤드 수입니다. 초기화 시점에만 적용되므로 변경 시 서버 재시작이 필요합니다. 동시 접속이 많은 환경에서 샤드 수를 늘리면 잠금 경합을 줄일 수 있습니다.

```
PVO_CACHE_SHARD_COUNT = 32
```

### PVO_CACHE_MAX_SQL_ENTRIES

PVO Cache에 보관할 수 있는 SQL 엔트리의 최대 개수입니다. 0은 무제한을 의미합니다. 값이 설정된 경우 샤드 수에 따라 분배되어 적용됩니다.

```
PVO_CACHE_MAX_SQL_ENTRIES = 10000
```

### PVO_CACHE_MAX_PLANS_PER_SQL

하나의 SQL에 대해 보관할 수 있는 최대 플랜 수입니다. 동일 SQL이라도 바인드 파라미터 타입에 따라 다른 플랜이 생성될 수 있습니다.

```
PVO_CACHE_MAX_PLANS_PER_SQL = 256
```

## 동적 변경

서버 재시작 없이 변경 가능한 프로퍼티는 `ALTER SYSTEM SET`으로 적용합니다.

```sql
-- PVO Cache 활성화
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;

-- 최대 메모리 512MB로 변경
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;

-- SQL 엔트리 수 제한
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 5000;
```

## 캐시 초기화

PVO Cache를 강제로 초기화하려면 다음 명령을 사용합니다.

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```

## 캐시 상태 확인

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'PVO_CACHE%'
 ORDER BY name;
```
