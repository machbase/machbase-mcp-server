# machcoordinatoradmin 명령/옵션 사전

`machcoordinatoradmin`은 Machbase Cluster Edition의 Coordinator 노드를 관리하고 클러스터 구성을 제어하는 도구입니다. Cluster Edition 패키지에만 포함됩니다.

## 옵션 목록

```bash
machcoordinatoradmin -h
```

### 기본 관리 옵션

| 옵션 | 설명 |
|------|------|
| `-u`, `--startup` | Coordinator 프로세스 시작 |
| `-s`, `--shutdown` | Coordinator 프로세스 정상 종료 |
| `-k`, `--kill` | Coordinator 프로세스 강제 중지 |
| `-c`, `--createdb` | Coordinator 메타데이터 생성 |
| `-d`, `--destroydb` | Coordinator 메타데이터 및 패키지 파일 삭제 |
| `-e`, `--check` | Coordinator 프로세스 실행 여부 확인 |
| `-i`, `--silent` | 배너 출력 없이 실행 |
| `--home-path=path` | Machbase 홈 경로 지정 |

### 설정 조회 옵션

| 옵션 | 설명 |
|------|------|
| `--configuration[=name]` | 설정 키와 값 출력. 특정 키만 출력 가능 |
| `--configure` | 시스템 속성 목록 전체 출력 |

### 클러스터 상태 제어

| 옵션 | 설명 |
|------|------|
| `--activate` | 클러스터 상태를 Service로 전환 |
| `--deactivate` | 클러스터 상태를 Deactivate로 전환 |
| `--cluster-status` | 클러스터 각 노드 상태 요약 출력 |
| `--cluster-status-full` | 클러스터 각 노드 상태 상세 출력 |
| `--cluster-node` | 클러스터 정보 출력 |
| `--verbose` | 상태 출력 시 Deployer 상태 포함 |

### 패키지 관리

| 옵션 | 설명 |
|------|------|
| `--list-package[=package]` | 등록된 패키지 목록 출력. 특정 패키지만 출력 가능 |
| `--add-package=package` | 패키지 추가 |
| `--remove-package=package` | 패키지 삭제 |

### 노드 관리

| 옵션 | 설명 |
|------|------|
| `--list-node[=node]` | 노드 정보 목록 출력 |
| `--add-node=node` | 노드 추가 |
| `--remove-node=node` | 노드 삭제 |
| `--attach-node=node` | 기존 노드를 클러스터 메타에 연결 |
| `--detach-node=node` | 노드를 클러스터 메타에서 분리 |
| `--upgrade-node=node` | 노드 업그레이드 |
| `--startup-node=node` | 특정 노드 시작 |
| `--shutdown-node=node` | 특정 노드 정상 종료 |
| `--kill-node=node` | 특정 노드 강제 중지 |

### Lookup 노드 관리

| 옵션 | 설명 |
|------|------|
| `--startup-lookup` | Lookup 노드 시작 |
| `--shutdown-lookup` | Lookup 노드 종료 |
| `--set-lookup-master=node` | Lookup master 노드 지정 |

### 웨어하우스 그룹/상태 관리

| 옵션 | 설명 |
|------|------|
| `--set-group-state=[normal\|readonly]` | 특정 웨어하우스 그룹 상태 변경 |
| `--set-warehouse-state=[normal\|scrapped]` | `--node`로 지정한 Warehouse 노드 상태 변경 |
| `--force-restore-warehouse=node` | scrapped Warehouse 노드 강제 복구 |

### 브로커 관리

| 옵션 | 설명 |
|------|------|
| `--deactivate-broker=node` | 지정 노드를 inactive 상태로 전환 |
| `--activate-broker=node` | 지정 노드를 normal 상태로 전환 |

### 스냅샷 관리

| 옵션 | 설명 |
|------|------|
| `--snapshot-interval=sec` | 스냅샷 실행 주기(초) 설정 |
| `--exec-snapshot` | 스냅샷 즉시 실행 (`--group` 필요) |
| `--snapshot-recover=node` | 지정 노드 스냅샷 복구 |
| `--exec-sync=node` | 지정 노드 동기화 실행 |
| `--snapshot-clean` | 스냅샷 정리 |

### 옵션 목록 호스트 리소스 모니터링

| 옵션 | 설명 |
|------|------|
| `--get-host-resource` | 각 노드의 호스트 리소스 정보 출력 |
| `--host-resource-enable` | 호스트 리소스 정보 수집 시작 |
| `--host-resource-disable` | 호스트 리소스 정보 수집 중지 |

### 추가 옵션 (다른 옵션과 함께 사용)

| 추가 옵션 | 필수 옵션 | 설명 |
|----------|----------|------|
| `--file-name=filename` | `--add-package` | 패키지 파일 이름 |
| `--port-no=portno` | `--add-node`, `--attach-node` | 서비스 포트 번호 |
| `--http-admin-port=portno` | Coordinator/Deployer `--add-node`, `--attach-node` | 관리 REST 포트 번호 |
| `--deployer=node` | `--add-node` | Deployer 노드 이름 |
| `--package-name=name` | `--add-node`, `--upgrade-node` | 설치 소스 패키지 이름 |
| `--home-path=path` | `--add-node`, `--attach-node` | 노드 설치 경로 |
| `--node-type=[broker\|warehouse\|lookup]` | `--add-node`, `--attach-node` | 노드 유형 |
| `--lookup-type=[master\|slave\|monitor]` | `--add-node`, `--attach-node` | Lookup 노드 유형 |
| `--node=node` | `--set-warehouse-state` | 상태 변경 대상 노드 |
| `--alias=alias` | `--add-node`, `--attach-node` | 노드 별칭 |
| `--dbs-path=path` | `--add-node` (Broker/Warehouse) | 데이터베이스 파일 경로 |
| `--group=groupname` | `--add-node`, `--attach-node`, `--set-group-state`, `--exec-snapshot` | 노드 그룹 이름 |
| `--replication=host:port` | `--add-node`, `--attach-node` | 복제 대상 host:port |
| `--no-replicate` | `--add-node`, `--attach-node` | 복제 사용 안 함 |
| `--primary=host:port` | `-u`, `--startup` | Secondary Coordinator의 Primary 지정 |
| `--host=host` | `--get-host-resource` | 특정 호스트 지정 |
| `--metric=[cpu\|memory\|disk\|network]` | `--get-host-resource` | 출력할 메트릭 종류 |

## 사용 예시

### 실행 상태 확인

```bash
machcoordinatoradmin -e
```

### 클러스터 상태 확인

```bash
machcoordinatoradmin --cluster-status
machcoordinatoradmin --cluster-status-full
```

### 클러스터 활성화/비활성화

```bash
machcoordinatoradmin --activate
machcoordinatoradmin --deactivate
```

### Warehouse 노드 추가

```bash
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --group=Group1 \
  --alias=warehouse-a1 \
  --dbs-path=/data/machbase/warehouse_a1_dbs
```

### 노드 목록 확인

```bash
machcoordinatoradmin --list-node
machcoordinatoradmin --list-node=192.168.0.32:5401
```

### 웨어하우스 그룹 읽기 전용 전환

```bash
machcoordinatoradmin --set-group-state=readonly --group=Group1
```

### 설정 조회

```bash
machcoordinatoradmin --configuration
machcoordinatoradmin --configuration=decision
```

### 사용 예시 호스트 리소스 모니터링

```bash
machcoordinatoradmin --host-resource-enable
machcoordinatoradmin --get-host-resource
machcoordinatoradmin --get-host-resource --metric=cpu
machcoordinatoradmin --get-host-resource --host=192.168.0.33
machcoordinatoradmin --host-resource-disable
```
