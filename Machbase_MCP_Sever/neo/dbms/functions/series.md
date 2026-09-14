# 윈도우/시리즈 함수

이 페이지는 결과 행에 번호를 붙이는 `ROWNUM()`과 연속 구간을 구분하는 `SERIESNUM()`을
설명합니다. `SERIES BY`는 정렬된 데이터에서 조건을 연속으로 만족하는 구간을 분석할 때
사용합니다. `LAG()`와 `LEAD()`처럼 `OVER` 절을 사용하는 함수는
윈도우 함수 문법을 참고하십시오.

## 빠른 참조

| 함수 | 문법 | 설명 |
|------|------|------|
| ROWNUM | `ROWNUM()` | SELECT 결과 행 번호 부여 |
| SERIESNUM | `SERIESNUM()` | 행이 속한 연속 구간의 번호 (같은 구간의 행은 같은 번호) |

---

## ROWNUM

`SELECT` 결과 행에 순서 번호를 부여합니다. 서브쿼리나 인라인 뷰 내부에서도 사용할 수 있습니다. 인라인 뷰의 Target List에서 사용할 경우 외부에서 참조할 수 있도록 Alias를 지정해야 합니다.

```sql
ROWNUM()
```

### 사용 가능 절

| 사용 가능 | 사용 불가 |
|-----------|----------|
| SELECT Target List, GROUP BY, ORDER BY | WHERE, HAVING |

`WHERE` / `HAVING`에서 행 번호로 필터링하려면 인라인 뷰에서 `ROWNUM()`을 계산한 뒤 외부 쿼리에서 참조합니다.

```sql
-- 상위 2개 행만 선택
Mach> SELECT INNER_RANK, c3 AS NAME
        FROM (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
       WHERE INNER_RANK < 3;
INNER_RANK           NAME
--------------------------
1                    Fourth Row
2                    Third Row
```

### ORDER BY와 함께 사용

`ORDER BY`를 포함한 쿼리를 인라인 뷰로 만들고 외부 `SELECT`에서 `ROWNUM()`을 호출하면 정렬된 순서로 번호가 부여됩니다.

```sql
Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
        FROM (SELECT * FROM rownum_table ORDER BY c3);
ROWNUM()    SORT    NAME
--------------------------
1           1       NULL
2           2       John
3           4.3     Micheal
4           3.3     Sarah
```

---

## SERIESNUM

`SERIES BY` 절로 그룹화된 시리즈에서 각 레코드가 몇 번째 시리즈에 속하는지 나타내는 번호를 반환합니다. `SERIES BY` 절을 사용하지 않으면 항상 1을 반환합니다. 반환 타입은 `BIGINT`입니다.

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Mach> INSERT INTO T1 VALUES (0, 1);
Mach> INSERT INTO T1 VALUES (1, 2);
Mach> INSERT INTO T1 VALUES (2, 3);
Mach> INSERT INTO T1 VALUES (3, 2);
Mach> INSERT INTO T1 VALUES (4, 1);
Mach> INSERT INTO T1 VALUES (5, 2);
Mach> INSERT INTO T1 VALUES (6, 3);
Mach> INSERT INTO T1 VALUES (7, 1);

-- C2 > 1 조건을 만족하는 연속 구간을 시리즈로 분리
Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM()  C1  C2
--------------------
1            1   2
1            2   3
1            3   2
2            5   2
2            6   3
[5] row(s) selected.
```

- `C1=1,2,3` (C2>1 조건 만족 연속 구간) → 시리즈 1
- `C1=4` (C2=1, 조건 불만족) → 시리즈 구분
- `C1=5,6` (C2>1 조건 만족 연속 구간) → 시리즈 2

---

## SERIES BY 절 개요

`SERIES BY` 절은 `ORDER BY`와 함께 사용하며, 지정한 조건을 연속으로 만족하는 행들을 하나의 시리즈로 묶습니다. `SERIESNUM()`으로 각 시리즈를 구분하고, 집계 함수와 조합하면 연속 구간별 통계를 계산할 수 있습니다.

구간별 통계는 내부 쿼리에서 구간 번호를 생성한 뒤 외부 쿼리에서 집계합니다.
아래 예제의 `threshold`는 비교할 임계값으로 바꾸어 사용합니다.

```sql
SELECT series_id, COUNT(*), AVG(value)
  FROM (
      SELECT value, SERIESNUM() AS series_id
        FROM sensor_log
       ORDER BY ts
       SERIES BY value > threshold
  )
 GROUP BY series_id
 ORDER BY series_id;
```
