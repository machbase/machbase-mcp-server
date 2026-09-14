# Machbase Neo Timer Guide

> **중요**: Machbase Neo 명령은 세미콜론( ; )으로 끝납니다

## 개요
타이머는 특정 시각에 실행하거나 정해진 간격으로 반복 실행할 작업을 정의하는 기능입니다.

## 새 타이머 추가

지정한 스케줄에 따라 실행되는 작업을 등록할 수 있습니다. 타이머 관리용 웹 UI는 8.0.20 버전부터 제공됩니다.

### 웹 UI로 추가하기
1. 좌측 메뉴 바에서 타이머 아이콘을 선택합니다
2. 좌측 상단의 `+` 버튼을 클릭합니다
3. Timer ID(이름), Timer Spec, TQL 스크립트 경로를 설정합니다
4. "Create" 버튼을 클릭합니다

### 타이머 시작/정지/삭제
- 토글 버튼으로 타이머를 시작/정지합니다
- 상세 페이지에서 편집, 시작, 정지, 삭제가 가능합니다

## 타이머 스케줄 지정

타이머 스케줄을 정의하는 방법은 세 가지입니다:

### 예제
```
0 30 * * * *           Every hour at 30 minutes
@every 1h30m           Every 1 hour 30 minutes
@daily                 Daily
```

## CRON 표현식

| 필드 | 필수 | 허용 값 | 특수 문자 |
|-------|----------|----------------|-------------------|
| Seconds | Yes | 0-59 | * / , - |
| Minutes | Yes | 0-59 | * / , - |
| Hours | Yes | 0-23 | * / , - |
| Day | Yes | 1-31 | * / , - ? |
| 월(Month) | 예 | 1-12 또는 JAN-DEC | * / , - |
| 요일(Day of Week) | 예 | 0-6 또는 SUN-SAT | * / , - ? |

### 특수 문자 설명

- **별표 `*`**: 해당 필드의 모든 값에 매칭됩니다
- **슬래시 `/`**: 범위의 증가 간격을 나타냅니다(예: 3-59/15는 3분부터 15분 간격)
- **쉼표 `,`**: 목록 항목을 구분합니다(예: "MON,WED,FRI"는 월·수·금)
- **하이픈 `-`**: 범위를 정의합니다(예: 9-17은 오전 9시부터 오후 5시)
- **물음표 `?`**: 일 또는 요일 필드를 비워 둘 때 `*` 대신 사용합니다

## 사전 정의된 스케줄

| 표현식 | 설명 | Equivalent CRON |
|------------|-------------|-----------------|
| @yearly (또는 @annually) | 1년에 한 번, 1월 1일 자정 | 0 0 0 1 1 * |
| @monthly | 한 달에 한 번, 매월 1일 자정 | 0 0 0 1 * * |
| @weekly | 일주일에 한 번, 토/일 사이 자정 | 0 0 0 * * 0 |
| @daily (또는 @midnight) | 하루에 한 번, 자정 | 0 0 0 * * * |
| @hourly | 한 시간에 한 번, 정각 | 0 0 * * * * |

## 간격 지정

`@every <duration>` 형식을 사용하며, duration은 "300ms", "-1.5h", "2h45m" 같은 형식입니다.
사용 가능한 시간 단위: "ms", "s", "m", "h"

### 예제
```
@every 10h
@every 1h10m30s
```

## 명령행 사용법

### Add Timer
```bash
timer add [--autostart] <name> <timer_spec> <tql-path>;
```
- `--autostart`: machbase-neo 시작 시 자동 시작
- `<name>`: Task name
- `<timer_spec>`: 실행 스케줄
- `<tql-path>`: 작업으로 실행할 TQL 스크립트

### List Timers
```bash
timer list;
```

### 타이머 시작/정지
```bash
timer [start | stop] <name>;
```

### 타이머 삭제
```bash
timer del <name>;
```

## Hello World 예제

### 1. TQL 스크립트 만들기
`helloworld.tql` 파일을 만들고 다음 코드를 저장합니다:

```js
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

### 2. Test Script
스크립트를 실행해 EXAMPLE 테이블에 레코드 한 건이 입력되는지 확인합니다:

```sql
select * from example where name = 'helloworld';
```

예상 결과:
```
┌────────┬────────────┬─────────────────────────┬────────────────────┐
│ ROWNUM │ NAME       │ TIME(LOCAL)             │ VALUE              │
├────────┼────────────┼─────────────────────────┼────────────────────┤
│      1 │ helloworld │ 2024-06-19 18:20:07.001 │ 0.6132387755535856 │
└────────┴────────────┴─────────────────────────┴────────────────────┘
```

### 3. 타이머 등록
명령행에서 타이머를 등록합니다:

```bash
timer add helloworld "@every 5s" helloworld.tql;
```

"Auto Start" 옵션을 켜거나 토글 버튼으로 직접 시작합니다.

### 4. 결과 확인
5초마다 새 레코드가 입력되는지 확인합니다:

```sql
select * from example where name = 'helloworld';
```

결과 예시:
```
┌────────┬────────────┬─────────────────────────┬─────────────────────┐
│ ROWNUM │ NAME       │ TIME(LOCAL)             │ VALUE               │
├────────┼────────────┼─────────────────────────┼─────────────────────┤
│      1 │ helloworld │ 2024-07-03 09:49:47.002 │ 0.14047743934840562 │
│      2 │ helloworld │ 2024-07-03 09:49:42.002 │ 0.7656153597963373  │
│      3 │ helloworld │ 2024-07-03 09:49:37.002 │ 0.11713331640146182 │
│      4 │ helloworld │ 2024-07-03 09:49:32.002 │ 0.5351642943247759  │
│      5 │ helloworld │ 2024-07-03 09:49:27.001 │ 0.6588127185612987  │
└────────┴────────────┴─────────────────────────┴─────────────────────┘
```

### 5. 대시보드 만들기
자동 갱신 대시보드를 만들어 타이머 동작을 모니터링할 수 있습니다.

## 타이머 관리

### 명령행에서 타이머 상태 확인
```bash
timer list;
```

결과 예시:
```
┌────────────┬───────────┬────────────────┬───────────┬─────────┐
│ NAME       │ SPEC      │ TQL            │ AUTOSTART │ STATE   │
├────────────┼───────────┼────────────────┼───────────┼─────────┤
│ HELLOWORLD │ @every 5s │ helloworld.tql │ false     │ RUNNING │
└────────────┴───────────┴────────────────┴───────────┴─────────┘
```

### 타이머 제어
```bash
# Start timer
timer start helloworld;

# Stop timer
timer stop helloworld;
```

---

## 빠른 참조

| 동작 | 명령 | 예 |
|-----------|---------|---------|
| Add Timer | `timer add <name> <spec> <tql-path>;` | `timer add daily_task "@daily" task.tql;` |
| 타이머 목록 | `timer list;` | 모든 타이머와 상태를 표시 |
| Start Timer | `timer start <name>;` | `timer start daily_task;` |
| Stop Timer | `timer stop <name>;` | `timer stop daily_task;` |
| 타이머 삭제 | `timer del <name>;` | `timer del daily_task;` |
