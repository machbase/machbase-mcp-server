# 설정 레퍼런스

Machbase 서버는 `$MACHBASE_HOME/conf/machbase.conf` 파일에 정의된 프로퍼티를 통해 동작을 제어합니다. 이 섹션은 각 프로퍼티의 허용 범위와 기본값을 빠르게 찾아볼 수 있는 레퍼런스입니다.

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| 설정 프로퍼티 사전 | 서버 기본 설정, 성능, 보안, 로그 등 Standard Edition 전체 프로퍼티 목록 |
| 클러스터 설정 프로퍼티 사전 | Cluster Edition 전용 Coordinator, Broker, Warehouse 설정 |
| PVO Cache 프로퍼티 사전 | SQL 실행 계획 캐시(PVO Statement Cache) 관련 프로퍼티 |
| Timezone 설정 사전 | 타임존 프로퍼티 및 클라이언트별 타임존 설정 방법 |

## 프로퍼티 확인 방법

서버 실행 중에 현재 프로퍼티 값을 확인하려면 `v$property` 시스템 뷰를 조회합니다.

```sql
-- 전체 프로퍼티 조회
SELECT name, value, type FROM v$property ORDER BY name;

-- 특정 프로퍼티 조회
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'PORT_NO';
```

## 동적 변경 가능 프로퍼티

서버 재시작 없이 `ALTER SYSTEM SET` 명령으로 변경할 수 있는 프로퍼티도 있습니다.

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;
```

변경 후 `v$property`를 조회하면 적용 여부를 확인할 수 있습니다. 재시작이 필요한 프로퍼티를 동적으로 변경하면 오류가 반환됩니다.
