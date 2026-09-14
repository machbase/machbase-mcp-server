# TAG data UPDATE 지원표

TAG 테이블의 실제 시계열 데이터는 `UPDATE table_name SET ... WHERE ...` 구문으로
수정할 수 있습니다. 이 페이지는 TAG data UPDATE에서 허용되는 WHERE 조건과 SET 대상을
정리합니다. 메타데이터 수정은 별도의 `UPDATE ... METADATA` 구문을 사용합니다.

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서만 지원합니다. Cluster Edition과
내부 raw component table에 대한 직접 UPDATE는 지원하지 않습니다.

## WHERE 조건별 지원 현황

TAG data UPDATE에는 하나의 태그 선택 조건과 하나 이상의 BASETIME 축 조건이 필요합니다.

| WHERE 조건 | 지원 | 비고 |
|-----------|:---:|------|
| `name = 'tag-01'` | O | 단일 태그 선택 |
| `name = ?`, `name = :tag_name` | O | positional/named bind로 단일 태그 선택 |
| `? = name`, `:tag_name = name` | O | 역방향 등치도 지원하며 컬럼-왼쪽 형식을 권장 |
| `name IN ('tag-01', 'tag-02')` | O | 리터럴/바인드 값 목록 지원, 서브쿼리 `IN`은 미지원 |
| `name LIKE 'tag-%'` | O | 패턴에 맞는 태그를 대상으로 확장 |
| `time = t1` | O | BASETIME 컬럼 등치 조건 |
| `time = ?`, `time = :base_time` | O | positional/named bind로 기준 시간 지정 |
| `? = time`, `:base_time = time` | O | 역방향 등치 지원 |
| `time BETWEEN t1 AND t2` | O | 양 끝 포함 |
| `time >= t1 AND time < t2` | O | `>`, `>=`, `<`, `<=` 조합 지원 |
| `time >= ? AND time < ?` | O | 범위 값에도 bind marker 사용 가능 |
| 한쪽 시간 조건 | O | 예: `time >= t1` |
| 데이터 컬럼 predicate | O | 예: `value > 100`, 태그/시간 조건과 함께 사용 |
| 조건 없는 UPDATE | X | 전체 TAG data UPDATE는 허용하지 않음 |
| 태그 선택 없는 시간 조건만 사용 | X | 대상 태그를 지정해야 함 |
| 시간 조건 없는 태그 조건만 사용 | X | BASETIME 범위를 지정해야 함 |
| `OR` 조건 | X | TAG data UPDATE 조건에서는 허용하지 않음 |
| 서브쿼리/집계식 | X | UPDATE 대상 결정 조건으로 사용할 수 없음 |
| 태그/축 컬럼을 함수·연산식으로 감싼 표현식 | X | 태그 선택자와 BASETIME은 해당 컬럼을 직접 지정해야 함 |

Bind parameter는 값만 대체합니다. 태그 선택 조건과 BASETIME 조건의 필수 여부, 허용되는
조건 구조와 SET 대상은 변경하지 않습니다. prepared statement 재실행은 최신 bind 값으로
대상을 다시 선택하며, 일치하는 행이 없으면 affected rows `0`으로 성공합니다.

## SET 대상 컬럼별 지원 현황

| SET 대상 | 지원 | 비고 |
|---------|:---:|------|
| 데이터 컬럼 | O | `value`, 보조 컬럼 등 사용자 데이터 컬럼 |
| `SUMMARIZED` 데이터 컬럼 | O | 원본 TAG 데이터가 갱신됨 |
| 여러 데이터 컬럼 | O | 같은 UPDATE 문에서 함께 지정 가능 |
| `name` (PRIMARY KEY) | X | 태그 이름은 변경할 수 없음 |
| `time` (BASETIME) | X | 시간 축 컬럼은 변경할 수 없음 |
| 메타데이터 컬럼 | X | `UPDATE table_name METADATA SET ...` 사용 |
| 숨김/시스템 컬럼 | X | 내부 컬럼은 UPDATE 대상이 아님 |

SET 표현식에는 상수, bind 변수, 기존 행 컬럼을 참조하지 않는 산술식·함수·`CASE`
표현식·문자열 연결, NULL 값(컬럼 제약이 허용하는 경우)을 사용할 수 있습니다. SET
우변에서 기존 행 컬럼을 참조할 수 없으며, 서브쿼리와 집계식도 사용할 수 없습니다.

## 정본

실행 문법과 parameter metadata는
TAG data UPDATE를,
SDK별 marker API는
Named Bind Parameter를,
진단은 TAG 제약과 문제 해결을
참고하십시오.
