# ROLLUP 지원 범위

## Edition과 테이블 범위

| 기능 | Standard | Cluster |
|---|:---:|:---:|
| 시간축 TAG의 일반·조건·확장 ROLLUP 생성·조회·제어 | O | O |
| WITH ROLLUP 자동 생성 | O | O |
| 지원 JSON 경로·문서 전체 집계 | O | O |
| Custom INTO...AS | O | X |
| ROLLUP_REBUILD | 제한된 대상·인수에서 지원 | X |

거리축 TAG, LOG, TRANSACTION, VOLATILE, LOOKUP에 시간축 ROLLUP을 적용하지 않습니다.
Cluster의 상태는 관련 노드와 계층별로 확인합니다.

## 생성 유형과 컬럼

| 유형 | 필요한 조건 |
|---|---|
| 일반 숫자 | 지원 숫자 DATA 컬럼; 명시 생성 시 SUMMARIZED는 필수가 아님 |
| JSON 경로 | JSON DATA 컬럼과 집계할 숫자 경로 |
| JSON 문서 전체 | JSON SUMMARIZED 컬럼 |
| WITH ROLLUP | 시간축 TAG의 세 번째 SUMMARIZED 컬럼 |
| FROM 계층 | 더 큰 정수배 간격과 동일한 확장·모드 조건 |
| Custom | 소스 시간축 TAG 하나, 사전 생성한 호환 대상 TAG |

## 집계와 선택

일반 숫자 ROLLUP은 MIN/MAX/SUM/COUNT/AVG/SUMSQ, 확장은 FIRST/LAST를 추가로
제공합니다. Custom의 부분 결과는 사용자가 재집계합니다. 평균은 합계와 유효 건수로,
FIRST/LAST는 대응 시각을 함께 유지해 합칩니다.
JSON 문서 전체의 COUNT는 저장된 집계 건수이며 원본 COUNT(value)와 무조건 같지 않습니다.

후보 선택은 조건·컬럼·경로·모드·간격에 따릅니다. 일반/확장만으로 우선순위를 단정하거나,
일 버킷에 24 HOUR ROLLUP이 자동 적용된다고 가정하지 않습니다.
조회 규칙을 확인합니다.

## REBUILD는 생성 지원과 다름

완전한 자동 SEC/MIN/HOUR 계층과 지원 Custom 경로를 대상으로 합니다. 임의 수동 이름,
부분 자동 계층, 10 MIN Custom 등 생성 가능한 모든 구성을 재구성할 수 있는 것은 아닙니다.
현재 Custom 시간 경계 처리 간격은 1 SEC·1 MIN·1 HOUR이며 SELECT의 버킷과도 맞아야 합니다.
상수 시각 인수, 버킷 전체 확장, 상태 전환과 오류 후 확인은
REBUILD 레퍼런스를 따릅니다.

## 권한

작업 계정에는 대상 데이터베이스 접속과 생성·삭제·조회 등 필요한 권한을 부여합니다.
다음은 존재하는 작업 계정에 생성·삭제 권한을 부여하는 예시이며 모든 필요 권한을
한 번에 구성하는 스크립트는 아닙니다.

```sql
GRANT CREATE, DROP ON DATABASE MACHBASEDB TO rollup_user;
```

권한 관리에서 소유자와 작업 범위를
확인하십시오.
