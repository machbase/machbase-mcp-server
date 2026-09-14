# 클러스터 설정 프로퍼티 사전

Cluster Edition에서는 `$MACHBASE_COORDINATOR_HOME/conf/`, `$MACHBASE_BROKER_HOME/conf/`, `$MACHBASE_WAREHOUSE_HOME/conf/` 각 노드의 설정 파일을 통해 클러스터 동작을 제어합니다.

이 페이지는 운영 시 자주 확인하는 주요 클러스터 프로퍼티를 정리합니다.

## Coordinator 설정

Coordinator는 클러스터 전체 메타데이터와 노드 상태를 관리합니다.

| 프로퍼티 | 기본값 | 설명 |
|----------|--------|------|
| `CLUSTER_LINK_HOST` | - | Coordinator가 바인드할 IP 주소 |
| `CLUSTER_LINK_PORT_NO` | 3868 | 클러스터 내부 통신 포트 |
| `CLUSTER_LINK_THREAD_COUNT` | 16 | 클러스터 링크 처리 스레드 수 |
| `CLUSTER_LINK_MAX_LISTEN` | 512 | 클러스터 링크 최대 listen 연결 수 |
| `CLUSTER_LINK_MAX_POLL` | 4096 | 클러스터 링크 최대 poll 이벤트 수 |
| `CLUSTER_LINK_BUFFER_SIZE` | 33554432 | 클러스터 링크 버퍼 크기(바이트). 기본 32MB |
| `HTTP_ADMIN_PORT` | 5779 | Coordinator/Deployer 관리 REST 포트 |
| `HTTP_THREAD_COUNT` | 2 | 관리 REST 요청 처리 스레드 수 |

`HTTP_ADMIN_PORT`는 환경 변수 `MACHBASE_HTTP_ADMIN_PORT`로도 지정할 수 있습니다. 이 포트는
SQL 조회나 데이터 입력을 위한 포트가 아니라 클러스터 관리 요청에만 사용합니다.

## 클러스터 링크 타임아웃 설정

모든 값의 단위는 마이크로초(μs)입니다.

| 프로퍼티 | 기본값(μs) | 설명 |
|----------|-----------|------|
| `CLUSTER_LINK_ACCEPT_TIMEOUT` | 5000000 | accept 타임아웃 (5초) |
| `CLUSTER_LINK_CHECK_INTERVAL` | 1000000 | 연결 상태 확인 주기 (1초) |
| `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` | 60000000 | 연결 재시도 최대 시간 (60초) |
| `CLUSTER_LINK_CONNECT_TIMEOUT` | 5000000 | 연결 타임아웃 (5초) |
| `CLUSTER_LINK_HANDSHAKE_TIMEOUT` | 5000000 | 핸드셰이크 타임아웃 (5초) |
| `CLUSTER_LINK_RECEIVE_TIMEOUT` | 30000000 | 수신 타임아웃 (30초) |
| `CLUSTER_LINK_SEND_TIMEOUT` | 30000000 | 송신 타임아웃 (30초) |
| `CLUSTER_LINK_REQUEST_TIMEOUT` | 60000000 | 요청 타임아웃 (60초) |
| `CLUSTER_LINK_SESSION_TIMEOUT` | 3600000000 | 세션 타임아웃 (1시간) |
| `CLUSTER_LINK_LONG_WAIT_INTERVAL` | 1000000 | 장시간 대기 간격 (1초) |
| `CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL` | 1000000 | 장기 콜백 주기 (1초) |

## Broker 설정

Broker는 클라이언트의 쿼리를 받아 Warehouse로 분산 처리합니다. Broker의 `machbase.conf`에는
서버 공통 설정과 클러스터 설정을 지정합니다. 지원 프로퍼티와 기본값은 Edition과 노드
역할에 따라 다르므로 Standard Edition의 설정 파일을 그대로 적용하지 마십시오.

| 프로퍼티 | 기본값 | 설명 |
|----------|--------|------|
| `PORT_NO` | 5656 | 클라이언트 연결 포트 |
| `QUERY_PARALLEL_FACTOR` | 4 | 병렬 쿼리 처리 스레드 수 (Cluster 기본값) |
| `CLUSTER_LINK_HOST` | - | Broker가 클러스터 통신에 바인드할 IP |
| `CLUSTER_LINK_PORT_NO` | - | Broker 클러스터 통신 포트 |

## Warehouse 설정

Warehouse는 실제 데이터를 저장하고 처리하는 노드입니다. 저장 관련 설정과 함께 다음
클러스터 설정을 사용합니다. `DDL_LOCK_TIMEOUT`처럼 Standard Edition 전용인 프로퍼티는
Cluster Edition에서 지원하지 않습니다.

| 프로퍼티 | 기본값 | 설명 |
|----------|--------|------|
| `PORT_NO` | 5656 | Warehouse 서비스 포트 |
| `CLUSTER_LINK_HOST` | - | Warehouse가 클러스터 통신에 바인드할 IP |
| `CLUSTER_LINK_PORT_NO` | - | Warehouse 클러스터 통신 포트 |
| `DBS_PATH` | ?/dbs | Warehouse 데이터 파일 저장 경로 |

## 클러스터 상태 확인

클러스터 설정값은 `machcoordinatoradmin --configure` 명령으로 출력할 수 있습니다.

```bash
machcoordinatoradmin --configure
```

특정 설정값만 확인하려면 `--configuration=name` 옵션을 사용합니다.

```bash
machcoordinatoradmin --configuration=decision
```

## 클러스터 포트 구성 예시

단일 호스트에 클러스터를 구성할 때의 포트 할당 예시입니다.

| 노드 | 서비스 포트 | HTTP 포트 | 클러스터 링크 포트 |
|------|------------|-----------|------------------|
| Coordinator | - | 5102 | 5101 |
| Deployer | - | - | 5201 |
| Broker | 5757 | 5302 | 5301 |
| Warehouse-A1 | 5400 | 5402 | 5401 |
| Warehouse-A2 | 5500 | 5502 | 5501 |
