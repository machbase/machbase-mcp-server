# 보안 설정 체크리스트

운영 배포 전과 정기 감사 때 다음 항목을 점검합니다.

## 계정과 인증

- 설치 직후 `SYS`의 초기 비밀번호를 조직의 비밀 관리 절차에 따라 변경합니다.
- 애플리케이션별 전용 계정을 만들고 `SYS`를 일반 접속에 사용하지 않습니다.
- 비밀번호를 소스 코드, 문서, 명령 이력에 저장하지 않습니다.
- 사용하지 않는 계정과 만료 예정 계정을 검토합니다.
- AUTH KEY를 사용하면 개인키의 보관 위치, 교체, 폐기 담당자를 지정합니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT USER_NAME, KEY_ID, KEY_ALGO, KEY_PARAM, ACTIVATED, VALID_BEFORE
  FROM V$USER_AUTH_KEYS
 ORDER BY USER_NAME, KEY_ID;
```

## 권한

- 각 논리 데이터베이스에 필요한 `CONNECT` 권한만 부여합니다.
- 읽기 계정에 쓰기·DDL·백업 권한이 없는지 확인합니다.
- 임시 권한의 만료와 회수 책임자를 기록합니다.
- 사용자나 테이블을 다시 만든 뒤 권한을 재검증합니다.

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

`PRIV`는 비트 마스크입니다. 숫자를 권한명처럼 표시하는 자체 도구는 사용 중인 배포 버전의
정의와 대조해 검증하십시오. 권한 부여·회수 절차는 권한 관리를 참고합니다.

## 네트워크 접속

- 원격 접속이 필요한지 먼저 결정합니다.
- `BIND_IP_ADDRESS`를 필요한 IPv4 인터페이스로 제한합니다.
- 방화벽 또는 보안 그룹의 소스 주소 허용 목록을 검토합니다.
- 설정 변경은 재시작과 접속 검증을 포함한 유지보수 절차로 수행합니다.

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

## 변경 후 증거

보안 변경 후에는 다음 결과를 변경 기록에 남깁니다.

1. 사용자와 만료일 조회 결과
2. 대상 사용자와 데이터베이스·테이블 권한 조회 결과
3. 허용한 주소에서의 정상 접속과 허용하지 않은 주소에서의 차단 결과
4. AUTH KEY를 변경했다면 새 키 접속 성공과 이전 키 차단 결과

운영 중인 공유 서버에서 `SYS` 비밀번호, 리스너, 방화벽을 시험 목적으로 변경하지 마십시오.
별도 검증 환경에서 복구 경로까지 확인한 뒤 운영 변경을 승인합니다.
