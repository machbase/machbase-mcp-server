# 접속 제어

네트워크 접속 범위는 `GRANT_REMOTE_ACCESS`, `BIND_IP_ADDRESS`, 운영체제 또는 클라우드
방화벽을 함께 사용해 제한합니다. 현재 값은 다음처럼 확인합니다.

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

리스너 설정은 서버가 시작할 때 적용됩니다. 운영 중인 리스너가 자동으로 다시 바인드된다고
가정하지 말고 `machbase.conf`를 변경한 뒤 승인된 재시작 절차를 수행하십시오.

## 원격 접속 설정

`GRANT_REMOTE_ACCESS`는 원격 클라이언트 접속 허용 여부를 제어합니다.

```ini
# 원격 접속 허용
GRANT_REMOTE_ACCESS = 1

# 원격 접속 차단
GRANT_REMOTE_ACCESS = 0
```

값을 바꾸기 전에 다음을 확인합니다.

1. 애플리케이션, 모니터링, 백업 클라이언트의 접속 위치
2. 로컬 관리 접속을 유지할 방법
3. 재시작 후 원격·비상 접속을 모두 시험할 점검 순서

`GRANT_REMOTE_ACCESS=1`만으로 모든 원격 주소를 허용하지 않도록 방화벽 허용 목록을 함께
구성하십시오.

## BIND_IP_ADDRESS와 네트워크 노출 제어

`BIND_IP_ADDRESS`는 IPv4 리스너가 바인드할 주소입니다.

```ini
# 모든 IPv4 인터페이스
BIND_IP_ADDRESS = 0.0.0.0

# 로컬 IPv4 인터페이스
BIND_IP_ADDRESS = 127.0.0.1

# 지정한 내부 IPv4 인터페이스
BIND_IP_ADDRESS = 10.0.0.5
```

서버에 존재하지 않는 주소를 지정하면 시작에 실패할 수 있습니다. 설정 변경 전 현재 인터페이스
주소를 확인하고, 재시작 후 실제 수신 주소와 포트를 운영체제 도구로 검증하십시오.

`0.0.0.0`이 필요하면 방화벽이나 보안 그룹에서 허용할 소스 주소와 포트를 제한합니다. 구체적인
방화벽 명령은 배포 운영체제와 네트워크 정책에 따라 다르므로 이 매뉴얼의 고정 명령을 그대로
적용하지 마십시오.
