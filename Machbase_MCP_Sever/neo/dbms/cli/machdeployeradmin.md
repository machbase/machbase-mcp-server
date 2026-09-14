# machdeployeradmin 명령/옵션 사전

`machdeployeradmin`은 Machbase Cluster Edition의 Deployer 노드를 직접 관리하는 도구입니다. Deployer는 Coordinator의 지시에 따라 각 노드에 패키지를 배포하고 설치 작업을 수행합니다.

일반적으로 Deployer 제어는 `machcoordinatoradmin`을 통하는 것이 권장됩니다. `machcoordinatoradmin`으로 제어가 불가능한 경우에 `machdeployeradmin`을 직접 사용합니다.

Cluster Edition 패키지에만 포함됩니다.

## 옵션 목록

```bash
machdeployeradmin -h
```

| 옵션 | 설명 |
|------|------|
| `-u`, `--startup` | Deployer 프로세스 시작 |
| `-s`, `--shutdown` | Deployer 프로세스 정상 종료 |
| `-k`, `--kill` | Deployer 프로세스 강제 중지 |
| `-c`, `--createdb` | Deployer 메타데이터 생성 |
| `-d`, `--destroydb` | Deployer 메타데이터 삭제 |
| `-e`, `--check` | Deployer 프로세스 실행 여부 확인 |
| `-i`, `--silent` | 배너 출력 없이 실행 |

## 프로세스 관리

### 시작

```bash
machdeployeradmin -u
```

### 정상 종료

```bash
machdeployeradmin -s
```

### 강제 중지

```bash
machdeployeradmin -k
```

### 실행 상태 확인

```bash
machdeployeradmin -e
```

실행 중이면 PID를 출력합니다.

```
Machbase Deployer is running with pid(29373)!
```

## 메타데이터 관리

Deployer 메타데이터를 새로 생성합니다.

```bash
machdeployeradmin -c
```

Deployer 메타데이터를 삭제합니다.

```bash
machdeployeradmin -d
```

## Deployer 역할

Deployer는 다음 작업을 Coordinator의 지시에 따라 수행합니다.

- Broker, Warehouse, Lookup 노드에 Machbase 패키지 배포 및 설치
- 노드 설정 파일 생성 및 관리
- 노드 시작/종료 지시 전달
- 노드 업그레이드 지원

## 사용 예시

```bash
# Deployer 초기 설정
machdeployeradmin -c
machdeployeradmin -u

# 실행 상태 확인
machdeployeradmin -e

# 정상 종료
machdeployeradmin -s

# 문제 발생 시 강제 중지
machdeployeradmin -k
```

## 참고

클러스터 구성 및 노드 관리의 대부분은 `machcoordinatoradmin`을 통해 수행합니다. `machdeployeradmin`은 Coordinator와의 통신이 불가능하거나 Deployer 자체에 문제가 있을 때 직접 개입하는 용도로 사용합니다.

자세한 클러스터 관리 방법은 machcoordinatoradmin을 참고하십시오.
