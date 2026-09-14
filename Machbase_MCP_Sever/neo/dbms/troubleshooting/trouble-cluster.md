# Cluster 문제

## Cluster 노드 상태가 비정상일 때

토폴로지 변경이나 재시작 전에 전체 상태와 최초 오류를 수집합니다.

```bash
machcoordinatoradmin --cluster-status
machclusterctl status
```

1. Coordinator, Broker, Warehouse 중 어느 역할이 처음 비정상이 되었는지 확인합니다.
2. 해당 노드와 선행 역할의 로그 시각을 맞춰 비교합니다.
3. 호스트, 프로세스, 디스크, 네트워크와 설정 파일 변경 이력을 확인합니다.
4. 복제·재배치 상태와 클라이언트 영향 범위를 기록합니다.
5. 13장의 승인된 복구 절차로 한 노드씩 조치하고 전체 상태를 다시 검증합니다.

노드 이름, 서비스 포트와 노드 간 통신 포트를 추측해 start/add/remove 명령을 실행하지
마십시오. 실제 `cluster.yaml`과 배포 도구 도움말을 기준으로 합니다. 자세한 안전 제한은
Cluster 운영을 참고하십시오.

## Cluster Edition 제한 오류

```sql
SELECT * FROM V$VERSION;
```

오류가 Edition 제한인지 판단할 때는 현재 Edition과
Edition별 지원 범위를 대조합니다. Standard 전용
기능을 우회하는 비공식 절차를 사용하지 말고, 같은 요구를 충족하는 Cluster 지원 기능 또는
별도 Standard 환경을 검토합니다.
