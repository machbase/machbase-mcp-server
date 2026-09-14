# ALTER SYSTEM 운영

`ALTER SYSTEM`은 인스턴스 전체에 영향을 줄 수 있는 관리자 명령입니다. 실행 전 대상
인스턴스, 권한, 진행 중 작업, 롤백 또는 해제 명령을 확인합니다. 전체 구문은
system·세션 ALTER 구문을
참고합니다.

## 공통 절차

1. 현재 서버와 데이터베이스, 릴리스를 확인합니다.
2. 관련 세션·문장·백업·체크포인트 상태를 기록합니다.
3. 명령의 blocking·I/O·메모리 영향을 확인합니다.
4. 유지보수 창과 실패 시 조치를 정합니다.
5. 실행 직후 결과와 관련 가상 테이블·로그를 확인합니다.

## CHECKPOINT

```text
ALTER SYSTEM CHECKPOINT;
```

체크포인트는 스토리지 I/O를 증가시킬 수 있습니다. 백업·종료 전 필요성을 검토하고
동시 대량 입력과 쿼리 영향을 관찰합니다. 단순히 “느리다”는 이유로 반복 실행하지 않습니다.

## CHECK DISK_USAGE

```text
ALTER SYSTEM CHECK DISK_USAGE;
```

파일 시스템 상태와 데이터베이스 스토리지 메타데이터의 점검이 필요한 경우 사용합니다. 실행 전
여유 공간과 마운트 상태를 확인하고 결과 로그를 검토합니다. 내부 파일을 직접 수정해 수치를
맞추지 않습니다.

## INSTALL LICENSE

```text
ALTER SYSTEM INSTALL LICENSE;
ALTER SYSTEM INSTALL LICENSE = '/absolute/path/license.dat';
```

라이선스 파일의 출처, 대상 인스턴스, 에디션, 만료일을 확인합니다. 파일 내용은 문서·로그에
복사하지 않고 권한을 제한합니다. 설치 뒤 `V$LICENSE_INFO`와 새 연결로
적용을 확인합니다.

## KILL과 CANCEL SESSION

```text
ALTER SYSTEM CANCEL SESSION session_id;
ALTER SYSTEM KILL SESSION session_id;
```

먼저 `V$SESSION`과 `V$STMT`에서 사용자, 클라이언트 IP, SQL, 상태를 확인합니다. `CANCEL`은 실행
중 문장 중단을 우선 시도할 때, `KILL`은 연결 자체를 종료해야 할 때
검토합니다. 트랜잭션·Appender·애플리케이션 재시도가 만드는 중복과 롤백 영향을
확인합니다.

## FREEZE와 UNFREEZE

```text
ALTER SYSTEM FREEZE;
ALTER SYSTEM UNFREEZE;
```

freeze는 공개 백업 기능으로 대체할 수 없는 파일 시스템 스냅샷 절차에서만 검토합니다.
실행 전 허용되는 읽기·쓰기 범위와 최대 freeze 시간을 정하고, 어떤 오류 경로에서도
`UNFREEZE`를 실행할 담당자와 확인 절차를 준비합니다. 세션을 freeze 상태로 방치하지
않습니다.

## FLUSH AGER

```text
ALTER SYSTEM FLUSH AGER;
```

삭제된 공간의 정리 지연을 조사할 때 사용 여부를 검토합니다. 보존 정책·DELETE 상태와
스토리지 여유를 먼저 확인하고, 정상 백그라운드 작업을 반복 강제하지 않습니다.

## FLUSH PVO_CACHE

```text
ALTER SYSTEM FLUSH PVO_CACHE;
```

캐시된 실행 계획을 비우면 이후 쿼리가 다시 파싱·최적화됩니다. 스키마·실행 계획 문제를
분리 진단할 때만 실행하고, 동시 쿼리의 지연 시간 일시적 급증을 관찰합니다. 캐시 flush를
지속적인 성능 문제의 해결책으로 사용하지 않습니다.

## FLUSH SYS_STAT

```text
ALTER SYSTEM FLUSH SYS_STAT;
```

누적 통계를 초기화하기 전에 필요한 기준값을 저장합니다. 초기화 시각을 모니터링에
기록해 변화율 계산과 장애 분석이 왜곡되지 않게 합니다.

## FLUSH PAGE_CACHE

```text
ALTER SYSTEM FLUSH PAGE_CACHE;
```

페이지 캐시 flush는 후속 쿼리의 I/O와 지연 시간을 크게 바꿀 수 있습니다. cold-cache
비교나 제한된 진단에서만 사용하고 운영 최대 부하에는 실행하지 않습니다.

## 권한과 감사

최소 관리자 계정으로 실행하고 명령, 대상, 시각, 실행자, 사유, 결과를 감사 기록에
남깁니다. 예제의 세션 ID, 경로, 설정 속성 값을 그대로 운영 명령으로 사용하지 않습니다.
