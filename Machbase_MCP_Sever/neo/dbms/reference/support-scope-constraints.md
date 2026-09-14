# 지원 범위와 제약

Machbase의 Edition별, 테이블 타입별, SDK별 기능 지원 범위와 알려진 제약 사항을 정리한 빠른 참조 모음입니다. 기능의 동작 원리나 사용 예시는 각 기능 장을, 특정 환경에서의 지원 여부 확인에는 이 섹션을 활용하십시오.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| Edition별 기능 지원표 | Standard Edition vs Cluster Edition 기능 비교 |
| 테이블 타입별 기능 지원표 | TAG / LOG / LOOKUP / VOLATILE / TRANSACTION 테이블별 지원 기능 |
| SDK별 기능 지원표 | JDBC, Python, Go, .NET, Node.js 지원 범위 |
| ROLLUP 지원 범위 | Edition별·테이블 타입별 ROLLUP 지원 범위 |
| 백업/마운트 지원표 | BACKUP / MOUNT 기능의 Edition별 지원 여부 |
| 권한별 기능 지원표 | 데이터베이스 권한 및 테이블 권한 목록 |
| TRANSACTION 기능 지원표 | TRANSACTION 테이블 지원 SQL 기능 및 제약 |
| 버전 및 호환성 | 업그레이드 시 주의사항, 지원 OS/플랫폼 |
| 서버와 SDK 호환성 | 서버와 SDK 버전 조합별 기능 지원 범위 |
| LOOKUP SQL/JSON 지원표 | LOOKUP 테이블 SQL/JSON 기능 지원 현황과 제약 |
| TAG data UPDATE 지원표 | TAG UPDATE 조건 및 대상 컬럼 지원 현황 |

지원표에 없는 내부 object·flag·protocol 동작에 의존하지 말고, SDK 기능은 server와 client
version을 함께 확인합니다. 기능별 오류 진단은 문제 해결을
참고하십시오.

## 표기 규칙

이 섹션의 지원 여부 표에서 사용하는 기호는 다음과 같습니다.

| 기호 | 의미 |
|:----:|------|
| O | 완전 지원 |
| X | 미지원 |
| △ | 일부 지원 또는 제약 있음 |
