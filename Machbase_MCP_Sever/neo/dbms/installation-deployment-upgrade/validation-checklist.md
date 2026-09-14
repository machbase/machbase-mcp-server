# 설치 검증 체크리스트

설치 검증은 프로세스가 살아 있는지 확인하는 것에서 끝나지 않습니다. 올바른 버전과 설정의
서버에 실제 클라이언트가 접속하고, 권한 범위에서 데이터를 기록·조회할 수 있어야 합니다.
아래 항목을 서버 상태 → 접속 → 버전·라이선스 → SQL → Cluster 복제 순서로 확인합니다.

각 결과에 실행 호스트, 설치 홈, 접속 주소·포트, 시각과 오류를 기록합니다. 업그레이드라면
변경 전 기록과 비교하십시오. `SYS`/`MANAGER`는 초기 실습 접속 예시이며 실제 계정으로
바꾸어야 합니다. 실습 테이블 이름이 기존 업무 객체와 겹치지 않는지도 먼저 확인합니다.

## Standard Edition 체크리스트

### 1. 서버 프로세스 확인

```bash
machadmin -e
# Machbase server is running with PID(<pid>).
```

프로세스를 직접 확인할 수도 있지만 다른 설치 홈에서 실행된 서버인지 구분해야 합니다.
`MACHBASE_HOME`이 검사할 인스턴스를 가리키는지 확인합니다.

```bash
ps -ef | grep machbased | grep -v grep
```

### 2. 포트 리스닝 확인

```bash
ss -tlnp | grep 5656
# LISTEN 0 128 0.0.0.0:5656 ...
```

현재 운영체제에 맞는 포트 확인 도구를 사용합니다. 예시의 `5656`은 실제 SQL 포트로 바꾸고,
수신 주소가 의도한 인터페이스인지 확인합니다. 리스너 확인과 원격 클라이언트의 접속 성공은
별개의 검사이므로 애플리케이션이 실행될 호스트에서도 접속을 시험합니다.

### 3. machsql 접속 테스트

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

로컬 접속은 성공하고 원격 접속만 실패하면 주소·포트, 리스너 설정과 방화벽을 확인합니다.
인증 오류는 사용자명·인증 방식·만료 상태를 확인하며, 접속 성공 뒤 객체 접근 오류는
현재 데이터베이스와 SQL 권한을 별도로 점검합니다.

### 4. 버전 확인

```sql
SELECT * FROM V$VERSION;
SELECT CURRENT_DATABASE();
```

### 5. 라이선스 확인

```sql
SELECT ID, ISSUE_DATE, TYPE, VIOLATE_STATUS FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`가 0인지 확인하고 설치된 라이선스 유형·기간이 운영 계획과 맞는지 봅니다.
위반 상태라면 `VIOLATE_MSG`와 서버 로그에서 원인을 확인합니다.

### 6. 기본 쿼리 테스트

```sql
CREATE LOG TABLE check_test (id INTEGER, ts DATETIME);
INSERT INTO check_test (id, ts) VALUES (1, NOW);
SELECT id, ts FROM check_test;
DROP TABLE check_test;
```

입력한 `id=1` 한 행과 시각이 반환되고 DROP이 성공하는지 확인합니다. 이 검사는 기본
LOG 입력 경로만 확인합니다. 실제 서비스에서 TAG·TRANSACTION·Append 등을 사용한다면
해당 테이블과 SDK로 대표 입력·조회도 수행합니다.

## Cluster Edition 추가 체크리스트

### 7. 클러스터 노드 상태 확인

```bash
machcoordinatoradmin --cluster-status
# 배포 기록의 노드 수와 역할별 상태를 비교
```

### 8. Broker 접속 테스트

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT * FROM V$NODE_STATUS;
```

Coordinator의 `primary`, Broker의 `leader`, Warehouse의 복제 상태처럼 역할마다 정상
상태 표기가 다릅니다. 모든 노드를 단일 문자열과 비교하지 말고 목표 상태와 실제 상태,
그룹 구성과 주소가 배포 기록과 맞는지 확인합니다.

### 9. 데이터 복제 확인

먼저 Broker를 통한 입력·조회를 확인한 뒤 Warehouse 그룹의 복제 상태를 확인합니다.
Broker에서 한 행이 조회된다는 사실만으로 모든 복제본의 동기화를 증명할 수는 없습니다.

```sql
-- Broker를 통해 데이터 입력
CREATE LOG TABLE cluster_check_test (id INTEGER, ts DATETIME);
INSERT INTO cluster_check_test (id, ts) VALUES (1, NOW);

-- Broker에서 입력 결과 확인
SELECT COUNT(*) FROM cluster_check_test;
```

Warehouse 직접 SQL 접속은 일반 애플리케이션 경로가 아니라 복제 진단용 관리 절차입니다.
`machcoordinatoradmin --cluster-status`에서 같은 복제 그룹의 active·standby peer를
확인한 뒤, 필요한 경우에만 각 peer의 네이티브 포트에 관리 계정으로 접속해 동일한 조회 결과를
비교합니다. 서로 다른 Warehouse 그룹의 모든 노드가 같은 행을 가진다고 가정하지 마십시오.

검증이 끝나면 Broker 연결에서 테이블을 정리합니다.

```sql
DROP TABLE cluster_check_test;
```

---

## 완료 기준과 문제 발생 시

서버·접속·권한·대표 SQL과 필요한 복제 검사가 모두 통과하면 서비스 인수를 진행합니다.
영속성을 검증해야 한다면 별도 검증 환경에서 데이터를 남긴 뒤 정상 재시작 전후 결과를
비교합니다. 업무 데이터가 있는 서버를 단순 설치 점검 목적으로 재초기화하지 마십시오.

실패하면 최초 오류와 관련 로그를 보존하고 실패한 단계부터 원인을 좁힙니다.

- 서버 로그: `$MACHBASE_HOME/trc/machbase.trc`
- 운영·장애 진단 참고
