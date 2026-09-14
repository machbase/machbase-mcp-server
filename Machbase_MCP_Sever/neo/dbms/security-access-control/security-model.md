# 보안 모델 개요

Machbase의 보안 모델은 **사용자 계정**, **권한(GRANT/REVOKE)**, **접속 제어(IP/인증)** 세 요소가 계층적으로 결합된 구조입니다.

## Machbase 보안 구조

```
클라이언트 연결 요청
        │
        ▼
┌─────────────────────┐
│   접속 제어           │  BIND_IP_ADDRESS, GRANT_REMOTE_ACCESS
│   (네트워크 레이어)     │
└────────┬────────────┘
         │ 허용된 경우
         ▼
┌─────────────────────┐
│   인증               │  비밀번호 인증 또는 AUTH KEY (공개키) 인증
│   (사용자 식별)        │
└────────┬────────────┘
         │ 인증 성공
         ▼
┌─────────────────────┐
│   권한 검사           │  GRANT/REVOKE로 부여된 권한 확인
│   (작업 허용 여부)     │  테이블 권한 + 데이터베이스 권한
└─────────────────────┘
```

연결 요청은 먼저 네트워크 접속 제어를 통과해야 하고, 이후 사용자 인증을 거쳐, 마지막으로 해당 작업에 필요한 권한이 부여되어 있는지 확인하는 순서로 진행됩니다.

## 기본 계정: SYS

Machbase를 설치하면 `SYS` 계정이 자동으로 생성됩니다. SYS는 슈퍼유저로서 모든 데이터베이스 작업을 수행할 수 있고, 다른 사용자를 생성하고 권한을 부여합니다.

| 항목 | 내용 |
|------|------|
| 계정명 | `SYS` |
| 기본 비밀번호 | `MANAGER` |
| 권한 | 모든 권한 보유 (슈퍼유저) |
| 삭제 가능 여부 | 불가 |

> **운영 환경 필수 조치**: SYS 계정의 기본 비밀번호(`MANAGER`)는 설치 후 즉시 변경해야 합니다.
>
> ```sql
> ALTER USER SYS IDENTIFIED BY '새_비밀번호';
> ```

## 관련 문서

- 사용자 생명 주기와 비밀번호 정책: 계정 관리
- 데이터베이스·테이블 권한과 GRANT/REVOKE: 권한 관리
- 공개키 등록·롤오버: AUTH KEY 인증
- 원격 접속과 listener: 접속 제어

계정 생성, 권한 부여와 인증 설정은 각각 별도의 작업입니다. 아래 예제의 계정과 테이블을
준비한 뒤, 각 계정으로 다시 접속하여 허용한 작업과 제한한 작업을 확인하십시오.

## 최소 권한 원칙

운영 환경에서는 다음 원칙을 적용하십시오.

- **SYS는 관리 작업 전용**: 일상적인 데이터 조회나 입력에는 SYS 계정을 사용하지 않습니다.
- **용도별 계정 분리**: 읽기 전용 계정, 데이터 입력 계정, 배포(DDL) 계정, 백업 계정을 분리합니다.
- **테이블 단위 권한 제한**: 계정이 접근해야 하는 테이블에만 필요한 DML 권한을 부여합니다.
- **정기 점검**: 불필요한 계정을 제거하고 권한이 과도하게 부여된 계정을 확인합니다.

```sql
-- 읽기 전용 계정
CREATE USER reader IDENTIFIED BY 'Reader#Strong123';
GRANT SELECT ON sys.sensor_log TO reader;

-- 데이터 입력 전용 계정
CREATE USER writer IDENTIFIED BY 'Writer#Strong123';
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- DDL 전용 계정 (테이블 생성/삭제)
CREATE USER deploy IDENTIFIED BY 'Deploy#Strong123';
GRANT CONNECT ON DATABASE factory_a TO deploy;
GRANT DDL ON DATABASE factory_a TO deploy;
```
