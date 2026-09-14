# Edition별 기능 지원표

Machbase는 단일 서버용 **Standard Edition**과 다중 노드 수평 확장용 **Cluster Edition**을 제공합니다. 핵심 시계열 기능은 공유하지만, 확장성과 고가용성 요구에 따라 지원 기능 범위가 다릅니다.

## Edition별 기능 비교

| 기능 | Standard | Cluster | 비고 |
|------|:--------:|:-------:|------|
| **테이블 유형** | | | |
| TAG 테이블 | O | O | |
| LOG 테이블 | O | O | |
| LOOKUP 테이블 | O | O | |
| TRANSACTION 테이블 | O | X | Cluster Edition 미지원 |
| VOLATILE 테이블 | O | O | 메모리 데이터의 node·restart lifecycle은 배포 구성에서 확인 |
| **데이터 관리** | | | |
| ROLLUP (기본) | O | O | |
| Custom ROLLUP | O | X | Cluster Edition 미지원 |
| ROLLUP_REBUILD | O | X | Cluster Edition 미지원 |
| **백업 및 복구** | | | |
| 논리 다중 데이터베이스 | O | X | Standard Edition 전용. DB별 CPU·메모리·디스크 물리 quota는 제공하지 않음 |
| BACKUP DATABASE | O | O | |
| BACKUP TABLE | O | O | |
| MOUNT DATABASE | O | X | Cluster Edition 미지원 |
| UMOUNT DATABASE | O | X | Cluster Edition 미지원 |
| machadmin -r 복구 | O | X | Cluster Edition 미지원 |
| **확장성 및 HA** | | | |
| 수평 확장 | X | O | Warehouse 노드 추가로 확장 |
| HA (고가용성) | X | O | Broker/Warehouse 이중화 |
| AUTH KEY 인증 | O | O | |

## Cluster Edition 제약 사항 요약

Cluster Edition은 단일 노드 중심의 로컬 파일 작업과 TRANSACTION 기능에 제약이 있습니다.

- **TRANSACTION 테이블**: 분산 환경에서 ACID 트랜잭션을 보장하는 TRANSACTION 테이블은 미지원. 트랜잭션이 필요한 데이터는 외부 RDBMS와 연동하십시오.
- **VOLATILE 테이블**: 생성·DML은 지원하지만 메모리 데이터는 node-local이며 노드 간 공유되지
  않습니다. 접속 Broker·routing과 node restart에 따른 데이터 범위를 검증해야 합니다.
- **MOUNT/UMOUNT**: 로컬 파일 시스템 기반 백업 마운트는 분산 환경에서 미지원.
- **Custom ROLLUP / ROLLUP_REBUILD**: 분산 집계 구조 차이로 커스텀 롤업 재정의 및 재구축 미지원.

## Edition 선택 기준

| 요구 사항 | 권장 Edition |
|-----------|-------------|
| 단일 서버의 처리량과 저장 용량으로 운영 가능한 워크로드 | Standard Edition |
| 단일 서버 범위를 넘어 수평 확장이 필요한 워크로드 | Cluster Edition |
| 고가용성 (장애 자동 복구) 필요 | Cluster Edition |
| TRANSACTION 테이블 또는 MOUNT 기능 필요 | Standard Edition |
| 실시간 수집량이 단일 서버 용량을 넘어 노드 추가가 필요한 경우 | Cluster Edition |
