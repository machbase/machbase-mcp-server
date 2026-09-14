# Document Catalog

| path | title_ko | keywords |
|------|----------|----------|
| api/api-http/http-guide.md | HTTP API 엔드포인트 | HTTP API,엔드포인트,REST,/db/query,/db/write,/db/tql,엔드포인트목록,기본URL,포트 | HTTP로 외부에서 닿을 수 있는 진입점이 몇 갈래인지 — 조회·쓰기·저장한 스크립트 실행 |
| api/api-http/http-query.md | HTTP 조회 API | HTTP조회,쿼리,format,transpose,rowsFlatten,timeformat,ndjson,csv,box,출력형식지정,전치,평탄화,시간형식 | HTTP로 조회할 때 엔드포인트와 파라미터, 응답을 JSON·CSV·표 형식으로 받는 방법 |
| api/api-http/http-write.md | HTTP 데이터 입력 API | HTTP입력,데이터쓰기,method=append,header,gzip,csv입력,json입력,header=columns,header=skip,heading,timeformat,tz,컬럼매핑,헤더처리,시간형식지정,압축전송,대량입력 | HTTP로 데이터를 넣을 때 엔드포인트와 CSV·JSON 형식, 헤더 처리와 대량 입력 파라미터 |
| api/api-http/http-create-drop-table.md | HTTP DDL 테이블 생성·삭제 | HTTP DDL,테이블생성,테이블삭제,CREATE TAG TABLE,DROP TABLE | HTTP로 테이블을 만들고 지우기 — 이미 있으면 실패하지 않게 하기 |
| api/api-http/http-lineprotocol.md | InfluxDB 라인 프로토콜 호환 | 라인프로토콜,influx,ILP,telegraf,메트릭입력,메트릭수집,텔레그라프연동 | telegraf 같은 도구가 쏘는 라인 프로토콜 메시지를 그대로 받아 넣기 |
| api/api-http/http-watch-data.md | HTTP 최신 데이터 감시(SSE) | 실시간감시,SSE,server-sent events,최신값,스트리밍,최신값구독,실시간수신 | 새 값이 들어올 때마다 화면이 알아서 받아보게 하기 — 끊기면 다시 붙는 스트리밍 방식 |
| api/api-http/http-upload-files.md | HTTP 파일 업로드 | 파일업로드,멀티파트,파일읽기 | 파일을 올려 레코드에 붙여 보관하기 — 저장 폴더 지정과 실제 파일 이름 규칙 |
| api/api-http/http-ui.md | HTTP UI·관리 API | 관리API,사용자인증,셸,터미널,서버이벤트,워크스페이스,RPC | 화면이 내부적으로 쓰는 경로로 목록을 받고 인증이 만료되면 토큰을 이어붙이기 |
| api/api-http/http-python.md | HTTP Python 클라이언트 | 파이썬,python,requests,pandas,matplotlib | 파이썬에서 HTTP로 조회·입력하고 압축된 응답을 바로 데이터프레임으로 읽기 |
| api/api-http/http-go.md | HTTP Go 클라이언트 | go언어,golang,net/http,고랭 | Go에서 HTTP로 조회·입력하는 클라이언트 코드와 URL 이스케이프 처리 |
| api/api-http/http-javascript.md | HTTP JavaScript 클라이언트 | 자바스크립트,javascript,fetch | 브라우저 자바스크립트에서 fetch로 HTTP 조회하고 응답을 텍스트나 객체로 받기 |
| api/api-http/http-csharp.md | HTTP C# 클라이언트 | csharp,C#,HttpClient,닷넷,닷넷,콘솔,CSV전송,헤더없이,heading | C#·닷넷에서 HttpClient로 HTTP 조회하고 CSV 본문을 그대로 POST해 넣기 |
| api/api-mqtt/mqtt-guide.md | MQTT API 개요 | MQTT,엠큐티티,발행,구독,쓰기흐름,조회흐름 | MQTT로 넣는 것뿐 아니라 조회까지 하려면 각각 어디로 보내고 어디로 받는지 |
| api/api-mqtt/mqtt-write.md | MQTT v3.1 데이터 입력 | MQTT입력,v3.1,토픽,append,insert,메시지크기,토픽구성,대량입력,메시지크기제한 | MQTT로 데이터를 넣을 때 토픽 이름은 테이블명을 쓰고 CSV·JSON·압축으로 보내는 방법 |
| api/api-mqtt/mqtt-writev5.md | MQTT v5 데이터 입력 | MQTT v5,토픽,append,insert,프로퍼티,토픽구성,v5프로퍼티 | MQTT v5에서 메시지에 속성을 붙여 넣기 — 구버전과 달라지는 점 |
| api/api-mqtt/mqtt-query.md | MQTT 조회 | MQTT조회,쿼리,JSON응답 | MQTT로 조회한 결과를 기본 응답 자리 말고 내가 정한 곳으로 받기 |
| api/api-mqtt/mqtt-python.md | MQTT Python 클라이언트 | 파이썬,python,paho | 파이썬에서 MQTT로 붙어 배열을 한 번에 밀어 넣고 접속을 콜백으로 확인하기 |
| api/api-mqtt/mqtt-go.md | MQTT Go 클라이언트 | go,golang,발행자 | Go에서 MQTT 발행자를 만들어 데이터를 넣는 라이브러리와 코드 |
| api/api-mqtt/mqtt-javascript-websocket.md | MQTT JavaScript·WebSocket 클라이언트 | 자바스크립트,websocket,웹소켓,nodejs | 브라우저에서 일반 소켓 대신 웹소켓으로 MQTT에 붙기 — 주소와 지원 버전 |
| api/api-mqtt/mqtt-csharp.md | MQTT C# 클라이언트 | csharp,C#,닷넷,TLS | C#에서 MQTT로 붙어 데이터를 넣는 클라이언트 코드 |
| bridges/bridge-overview.md | 브리지와 구독자 개요 | 브리지,bridge,subscriber,구독자,외부연동 | 외부 DB·메시지 브로커를 브리지로 등록해 TQL에서 붙여 쓰고 구독자로 자동 입력받기 |
| bridges/bridge-mqtt.md | MQTT 브리지 | MQTT브리지,외부브로커,메시지전송,메시지수신 | 외부 MQTT 브로커와 메시지를 주고받는 브리지 등록과 구독자로 자동 입력받기 |
| bridges/bridge-nats.md | NATS 브리지 | NATS브리지,메시지수신,구독자,NATS,구독,subscribe,발행,에코차단,NoEcho,NoRandomize,서버목록,되돌아옴방지,브리지등록,쓰기서술자 | NATS 서버와 메시지를 주고받는 브리지 — 등록, 구독자, 내가 발행한 게 되돌아오는 것 막기 |
| bridges/bridge-sqlite.md | SQLite 브리지 | SQLite브리지,sqlite3,외부DB | SQLite 파일을 브리지로 등록해 조회·입력하고 TQL에서 함께 쓰기 |
| bridges/bridge-postgresql.md | PostgreSQL 브리지 | PostgreSQL브리지,postgres,외부DB | PostgreSQL을 브리지로 등록해 외부 DB 데이터를 조회하고 주고받기 |
| bridges/bridge-mysql.md | MySQL 브리지 | MySQL브리지,외부DB,MySQL,연결문자열,DSN,parseTime,시간컬럼깨짐,TIMESTAMP파싱,외부DB읽기,외부DB쓰기,TQL로쓰기 | MySQL을 브리지로 붙일 때 연결 문자열과 시각 컬럼이 깨지지 않게 하는 설정 |
| bridges/bridge-mssql.md | MSSQL 브리지 | MSSQL브리지,SQL Server,외부DB | MSSQL을 브리지로 등록해 외부 DB 데이터를 조회하고 주고받기 |
| installation/installation.md | 설치와 시작하기 | 설치,install,다운로드,도커,docker,시작,정지,웹UI,배포모드,포트 | 지원 하드웨어와 운영체제, 설치 방법, 화면 없이 돌리는 Headless·Head Only 모드 |
| operations/command-line.md | 명령행 도구와 서버 실행 플래그 | 명령행,CLI,serve,shell,restore,gen-config,플래그,옵션,--host,--data,--port,--http-port,--mqtt-port,--config,--pid,--preset,외부접속,원격허용,서버실행,서버시작,포트변경,데이터디렉터리,설정파일지정,대화형셸,셸접속,백업복원 | 서버를 띄우고 멈추는 명령과 포트·데이터 경로·외부 접속 허용 같은 실행 플래그 |
| operations/server-config.md | 설정 파일 | 설정파일,config,HCL,리스너,데이터디렉토리,로깅설정,설정템플릿,gen-config,프로퍼티,포트설정,바인드설정 | 설정 파일을 뽑아 쓰는 방법과 데이터·환경설정 디렉터리 기본 위치, 수신 설정 |
| operations/address-ports.md | 바인드 주소와 포트 | 주소,포트,바인드,원격접속,5654,5653,5652,5656,포트변경,외부접속,원격허용,방화벽 | 기본은 로컬에서만 받는데 원격에서 붙게 하려면 바꿀 바인드 주소와 포트 |
| operations/metrics.md | 서버 지표 | 지표,메트릭,statz,모니터링,성능지표,지표조회,성능확인,상태확인 | 서버 상태 지표를 1분·5분·15분 주기로 보고 무엇을 확인할지 |
| operations/service-linux.md | 리눅스 서비스 등록 | 리눅스서비스,systemd,supervisord,PM2,자동시작,서비스등록,부팅자동실행,데몬등록 | 리눅스에서 시스템 서비스로 등록해 자동 실행·관리하기 |
| operations/service-windows.md | 윈도우 서비스 등록 | 윈도우서비스,windows,service install,자동시작,서비스등록,서비스제거,부팅자동실행 | 윈도우에서 서비스로 설치·제거하고 시작·중지하기 |
| sdk-go/machgo.md | Go 클라이언트 SDK | go SDK,golang,appender,대량입력 | Go에서 네이티브 프로토콜로 붙는 순수 Go 클라이언트 — 설치와 시작 |
| sdk-go/machcli.md | CGo 클라이언트 SDK | cgo,C클라이언트,네이티브 | Go에서 C 라이브러리를 감싼 래퍼로 붙기 — 사전 준비와 설정 |
| sdk-go/sqldriver.md | Go SQL 드라이버 | sql드라이버,database/sql,커넥션 | Go 표준 database/sql 인터페이스로 붙을 때 등록되는 드라이버 이름과 연결 문자열 |
| security/security.md | 보안과 인증 | 보안,인증,토큰,X.509,인증서,키생성,TLS,비밀번호 | 접속에 쓸 키와 토큰을 만들고 화면·셸·HTTP에서 인증하기 |
| sql/sql-guide.md | SQL 사용 가이드 | SQL,쿼리,예제,테이블생성,입력,조회,집계,백업,모니터링,SQL예제,쿼리작성,실습,화면실행,웹UI,SQL편집기,결과그래프,CHART,CSV내려받기,파일내려받기,show tags,desc,비표준명령,Non-SQL | 웹 화면에서 SQL을 실행하고 결과를 그래프로 보거나 CSV로 내려받기, 표준이 아닌 명령 |
| sql/sql-tag-table.md | 태그 테이블 데이터 모델 | 태그테이블,tag table,메타데이터,BASETIME,SUMMARIZED,PIVOT,인덱스,태그테이블만들기,메타데이터설정,태그조회 | 센서 시계열을 담는 태그 테이블이 어떤 구조이고 일반 테이블과 뭐가 다른지 |
| sql/sql-rollup.md | ROLLUP 사전집계 | 롤업,rollup,사전집계,집계테이블,ROLLUP_FORCE,롤업갭,롤업만들기,롤업조회,롤업삭제,사전집계설정 | 넓은 시간 범위를 빠르게 집계하려고 미리 계산해 두기 — 지원 함수와 시간 단위 |
| sql/sql-tag-statistics.md | 태그별 통계 뷰 | 태그통계,통계뷰,v$stat,최소값,최대값,행수 | 태그별 최신 시각·건수 같은 통계를 통계 뷰에서 빠르게 보기 |
| sql/sql-backup-mount.md | 백업과 마운트 | 백업,backup,마운트,mount,복원,restore,증분백업,백업하기,복원하기,마운트하기,경로해석,증분백업,AFTER,기준경로 | 데이터를 파일로 떠 두고 나중에 붙여서 조회하다 떼는 방법 |
| sql/sql-storage-size.md | 저장 공간 관리와 보존 정책 | 저장공간,용량,retention,보존정책,자동삭제,용량관리,자동삭제설정,보관기간 | 데이터가 계속 쌓일 때 저장 공간을 관리하고 오래된 걸 자동으로 지우는 보존 정책 |
| sql/sql-duplicate-removal.md | 중복 데이터 제거 | 중복제거,중복데이터,duplicate,first-write-wins | 같은 데이터가 중복으로 들어올 때 자동으로 걸러내는 설정과 제약 |
| sql/sql-outlier-removal.md | 이상치 자동 제거 | 이상치,아웃라이어,LSL,USL,규격한계,필터링 | 센서 값이 규격 한계를 벗어나면 자동으로 걸러내기 — 테이블 생성 시와 기존 테이블에 추가 |
| utilities/dashboard.md | 대시보드 사용법 | 대시보드,dashboard,차트패널,시간범위,변수,TQL차트 | 화면을 구성해 저장할 때 파일 확장자와 시간 범위 적는 법 |
| utilities/tag-analyzer.md | 태그 분석기 | 태그분석기,tag analyzer,차트,FFT,오버랩차트,롤업차트 | 태그 데이터를 롤업으로 차트에 띄워 분석하는 화면 사용법 |
| utilities/timer.md | 타이머 | 타이머,timer,스케줄,cron,주기실행,자동실행,일정,예약실행,정기실행,웹UI등록,화면등록,특수문자,CRON특수문자,사전정의스케줄,간격지정,날짜필드 | 주기적으로 돌 작업을 화면에서 등록하기 — 날짜 필드 특수 문자와 지원 버전 |
| utilities/timer-templates.md | 타이머 TQL 템플릿 | 타이머템플릿,스케줄옵션,타이머TQL | 타이머로 돌릴 스크립트를 짤 때 일정 표현식과 작성 규칙 |
| utilities/import-export.md | 데이터 가져오기·내보내기 | 임포트,익스포트,import,export,CSV,테이블복사,대량입력 | 원격에 있는 압축 파일을 임시 파일 없이 바로 밀어 넣고 이어 붙이기 |
| utilities/timeformat-tz.md | 시간 형식과 시간대 | 시간형식,timeformat,시간대,timezone,tz,RFC3339,epoch | 조회할 때 시간 형식과 시간대를 지정하는 옵션 — 지역 이름으로 줘도 되는지 |
| utilities/shell/shell-access.md | 셸 원격 접속 | 셸접속,SSH,원격접속,웹터미널,SSH키 | 웹 화면에서 대화형 셸을 열어 명령을 실행하는 방법 |
| utilities/shell/shell-run.md | 셸 스크립트 실행 | 셸스크립트,스크립트실행,배치 | 여러 명령을 파일에 담아 실행하기 — 그냥 실행되게 만들기와 주석 달기 |
| utilities/shell/shell-custom.md | 사용자 정의 셸 | 사용자셸,커스텀셸,셸등록 | 다른 프로그램을 셸로 등록해 웹 UI에서 바로 띄우고 목록·삭제로 관리 |
| tql/tql-guide.md | TQL 개요와 개념 | TQL,티큐엘,파이프라인,SRC,SINK,MAP,데이터변환,TQL이란,TQL작성법,TQL시작하기,파이프라인작성 | TQL이 무엇이고 SQL과 어떻게 다른지, 스크립트를 어떻게 구성하는지 |
| tql/tql-reference.md | TQL 문법 레퍼런스 | TQL문법,기본타입,statement,param,연산자,pragma | 여러 줄 SQL과 덩어리 값을 escape 없이 쓰는 법, 실행 방식을 지시하는 것 |
| tql/tql-src.md | TQL 소스 함수 | TQL소스,SRC,SQL(),CSV(),SCRIPT(),HTTP(),FAKE(),ARGS(),데이터읽기,데이터읽기,소스지정,쿼리결과가져오기 | TQL 스크립트를 무엇으로 시작하는지 — SQL·CSV·FAKE 등 데이터 소스 함수 |
| tql/tql-sink.md | TQL 싱크 함수 | TQL싱크,SINK,INSERT(),APPEND(),CSV(),JSON(),CHART(),출력,결과출력,파일저장,차트출력,테이블입력 | TQL 스크립트를 무엇으로 끝내는지 — 화면 출력·파일 저장·테이블 입력·결과 버리기 |
| tql/tql-map.md | TQL MAP 변환 함수 | TQL MAP,변환,MAPVALUE,PUSHVALUE,POPVALUE,TAKE,DROP,FILTER,GROUP,TRANSPOSE,값변환,컬럼추가,컬럼제거,필터링,그룹화 | TQL 중간에서 값을 바꾸고 거르고 묶는 변환 함수들 |
| tql/tql-group.md | TQL GROUP 집계 | TQL집계,GROUP,by(),평균,합계,분산,공분산,백분위 | TQL에서 데이터를 묶어 집계할 때 기준 지정과 제곱평균 같은 집계 방법 |
| tql/tql-script.md | TQL SCRIPT 함수 | TQL스크립트,SCRIPT(),자바스크립트,JSH모듈,컨텍스트,스크립트작성,자바스크립트사용 | TQL 안에서 자바스크립트로 값을 직접 계산하고 변환하기 |
| tql/tql-utilities.md | TQL 유틸리티 함수 | TQL함수,문자열함수,시간함수,수학함수,리스트,상수 | TQL 어디서나 쓰는 공통 함수 — 문자열 다듬기, 패턴 맞추기, 미리 정해진 상수 |
| tql/tql-time-examples.md | TQL 시간 처리 예제 | TQL시간,시간변환,시간포맷,시간대,parseTime,timeformat,시간변환,시간계산,시간대변환 | TQL에서 시간을 다루는 예제 — 시간 계산과 형식 지정 |
| tql/tql-filters.md | TQL 신호 필터 | TQL필터,이동평균,저역통과,칼만필터,노이즈제거,신호처리 | 측정 신호에 섞인 잡음을 걷어내는 필터들 — 평균 필터 등 종류와 차이 |
| tql/tql-fft.md | TQL FFT 주파수 분석 | FFT,푸리에,주파수분석,진동분석,스펙트럼 | TQL로 주파수 분석(FFT)을 돌려 신호 성분을 보는 예제 |
| tql/tql-reading.md | TQL 조회 출력 API | TQL조회,출력형식,CSV,JSON,NDJSON,MARKDOWN,결과캐시 | TQL 결과를 CSV·JSON 등 어떤 형식으로 내보낼지와 구분자·헤더 지정 |
| tql/tql-writing.md | TQL 데이터 입력 API | TQL입력,쓰기,INSERT CSV,APPEND CSV,사용자정의 | HTTP나 MQTT로 TQL을 호출해 데이터를 넣기 — INSERT와 APPEND 방식 |
| tql/tql-http.md | TQL HTTP 요청 처리 | TQL HTTP,쿼리문자열,요청헤더,요청본문,multipart,폼데이터 | TQL에서 외부 HTTP를 호출해 데이터를 가져오거나 보내기 |
| tql/tql-html.md | TQL HTML 생성 | TQL HTML,템플릿,이스케이핑,웹페이지 | TQL 결과를 내 서식대로 문서로 뽑기 — 값 참조와 자동 escape |
| tql/tql-chart-conventions.md | TQL 차트 작성 규칙 | 차트규칙,차트컨벤션,대시보드차트,시계열차트,롤업차트 | 대시보드 차트를 직접 짤 때 지킬 골격 — 롤업 유무에 따른 데이터 구성 |
| tql/tql-chart-validation.md | TQL 차트 검증 | 차트검증,빈차트,차트디버깅,컬럼참조,차트오류 | 차트가 비어 보이거나 오류가 날 때 실행 전에 검증하는 절차와 문제 유형 구분 |
| tql/chart/line-chart.md | 선·영역 차트 | 선차트,라인차트,영역차트,area,누적,step line,다중축 | 시간에 따른 값 변화를 선으로 그리기 |
| tql/chart/bar-chart.md | 막대 차트 | 막대차트,bar,카테고리,극좌표막대,누적막대,대규모막대 | 값을 막대로 그리고 순위 변화를 애니메이션으로 보이거나 대량 데이터를 확대·축소하기 |
| tql/chart/scatter-chart.md | 산점도 | 산점도,scatter,앤스컴,대량포인트 | 두 값의 관계를 점으로 뿌려 그리기 |
| tql/chart/pie-chart.md | 파이·도넛 차트 | 파이차트,도넛,나이팅게일,원형차트 | 비중을 원형으로 그리고 가운데를 비우거나 조각 길이를 값에 따라 바꾸기 |
| tql/chart/gauge-chart.md | 게이지 차트 | 게이지,gauge,속도계,실시간갱신 | 단일 값을 계기판 모양으로 보이기 |
| tql/chart/heatmap-chart.md | 히트맵 차트 | 히트맵,heatmap,캘린더히트맵,색상매핑 | 두 축의 교차 구간별 밀도를 색으로 그리기 |
| tql/chart/boxplot-chart.md | 박스플롯 차트 | 박스플롯,boxplot,사분위,분포 | 분포를 상자 모양으로 그리고 갈래별로 묶어 순서 정하기 |
| tql/chart/candlestick-chart.md | 캔들스틱 차트 | 캔들스틱,candlestick,주가,OHLC,이동평균,거래량 | 시가·종가 형태를 그릴 때 배열 순서와 이동평균선 얹기 |
| tql/chart/radar-chart.md | 레이더 차트 | 레이더차트,radar,방사형 | 여러 항목 점수를 방사형으로 그리기 |
| tql/chart/liquidfill-chart.md | 리퀴드필 차트 | 리퀴드필,liquidfill,물결,파형 | 비율을 물이 차오르는 모양으로 그리기 |
| tql/chart/geojson-chart.md | GeoJSON 지도 차트 | GeoJSON,지도차트,행정구역,지역별 | 지리 경계 데이터를 지도 위에 색으로 그리기 |
| tql/chart/3d-bar-chart.md | 3D 막대 차트 | 3D막대,bar3d,입체막대,dataset | 입체 막대를 그리고 바깥 파일을 데이터로 물려 값에 따라 색 입히기 |
| tql/chart/3d-line-chart.md | 3D 선 차트 | 3D선,line3d,정사영 | 입체 선을 그릴 때 데이터 형식과 원근 없이 평행하게 보이기 |
| tql/chart/3d-globe-chart.md | 3D 지구본 차트 | 지구본,globe,3D지구,항공노선 | 구 위에 지리 데이터를 얹고 지형 높낮이 표현하기 |
| tql/chart/others-chart.md | 생키·워드클라우드 등 기타 차트 | 생키,sankey,워드클라우드,wordcloud,SVG경로 | 생키·워드클라우드 등 그 밖의 차트 종류 |
| tql/chart/chart-html-embedding.md | 차트 HTML 삽입 | 차트삽입,iframe,HTML embed,동적TQL | TQL로 만든 차트를 웹 페이지에 끼워 넣기 — iframe과 JSON 응답, 로딩 순서 |
| tql/geomap/geomap-guide.md | GEOMAP 지도 | 지도,geomap,마커,타일,위경도,circle | 지도 위에 마커·경로를 그리는 GEOMAP 사용법과 지원 버전 |
| tql/geomap/geomap-html-embedding.md | 지도 HTML 삽입 | 지도삽입,iframe,HTML embed | TQL로 만든 지도를 웹 페이지에 끼워 넣기 |
| jsh/javascript-guide.md | JSH 자바스크립트 개요 | JSH,자바스크립트,스크립트,모듈,명령,시작하기,스크립트작성,JSH시작하기 | JSH가 무엇이고 스크립트를 어떻게 시작하는지 — 첫 예제와 모듈 구조 |
| jsh/javascript-examples.md | JSH 예제 모음 | JSH예제,HTTP서버,MQTT발행,MQTT구독,DB클라이언트,append | JSH로 HTTP 서버·정적 콘텐츠·REST API를 만드는 예제 모음 |
| jsh/javascript-commands.md | JSH 셸 명령 | JSH명령,파일시스템명령,환경명령,시스템명령,메시징명령 | JSH 셸 명령들 — 가상 파일시스템에서 동작하며 servicectl로 서비스 제어 |
| jsh/javascript-global.md | JSH 전역 함수 | 전역함수,setTimeout,setInterval,console,타이머 | 모듈을 안 불러도 쓰는 전역 함수 — 다음 차례 실행, 화면에 찍기, 타이머 |
| jsh/javascript-packages.md | JSH 패키지 관리 | 패키지,package.json,pkg install,pkg run,의존성 | 의존성을 설치해 쓰기 — 명령과 잠금 파일, 기준 디렉터리 |
| jsh/javascript-db-module.md | DB 모듈 | DB모듈,데이터베이스,Client,Conn,Rows,Appender,쿼리,DB접속,쿼리실행,대량입력 | 스크립트에서 데이터베이스에 붙어 쿼리를 실행하고 대량 입력(Appender)하기 |
| jsh/javascript-machcli-module.md | MachCLI 모듈 | machcli,네이티브접속,테이블타입,데이터베이스ID | 스크립트에서 네이티브 클라이언트로 붙어 쿼리하고 테이블 종류 확인하기 |
| jsh/javascript-http-module.md | HTTP 모듈 | HTTP모듈,요청,응답,서버,클라이언트,라우팅,HTTP요청,서버만들기,라우팅 | 스크립트에서 외부 HTTP 요청을 보내고 응답 받기 |
| jsh/javascript-mqtt-module.md | MQTT 모듈 | MQTT모듈,발행,구독,브로커,페이로드 | 스크립트에서 MQTT 브로커에 붙어 발행·구독하기 |
| jsh/javascript-nats-module.md | NATS 모듈 | NATS모듈,발행,구독,요청응답 | 스크립트에서 NATS로 발행·구독하기 |
| jsh/javascript-ws-module.md | WebSocket 모듈 | 웹소켓,websocket,WebSocketServer,실시간통신 | 스크립트에서 웹소켓 클라이언트·서버를 만들기 — 상태 값과 메시지 타입 |
| jsh/javascript-net-module.md | Net 소켓 모듈 | 네트워크,소켓,TCP,서버,IP검증 | TCP 서버를 열고 받은 주소가 v4인지 v6인지 판별하기 |
| jsh/javascript-opcua-module.md | OPC UA 모듈 | OPCUA,산업프로토콜,노드읽기,노드쓰기,browse | 산업용 OPC UA 서버 노드를 훑고 값을 읽기 |
| jsh/javascript-dbus-module.md | D-Bus 모듈 | dbus,디버스,리눅스IPC,객체프록시 | 리눅스 데스크톱 서비스와 메시지를 주고받는 D-Bus — 버스 종류와 다른 운영체제에서의 동작 |
| jsh/javascript-fs-module.md | 파일시스템 모듈 | 파일시스템,fs,파일읽기,파일쓰기,디렉터리,파일읽기,파일쓰기,디렉터리조회 | 파일을 읽고 쓰고 줄 수를 세고 심볼릭 링크 정보를 보기 |
| jsh/javascript-path-module.md | 경로 모듈 | 경로,path,join,resolve,dirname,basename | 경로를 다룰 때 윈도우 규칙으로 강제하기 — 기본값과 구분자 |
| jsh/javascript-os-module.md | OS 정보 모듈 | 운영체제,os,CPU,메모리,디스크,네트워크인터페이스,시그널상수 | 시스템 정보 얻기 — 바이트 순서와 디스크 입출력 횟수, 지원 버전 |
| jsh/javascript-process-module.md | 프로세스 제어 모듈 | 프로세스,daemonize,데몬,schedule,ps,프로세스실행,데몬만들기,주기실행,프로세스목록 | Machbase 고유 프로세스 제어 — 데몬으로 띄우기, 예약 실행, 프로세스 목록 |
| jsh/javascript-process-node-module.md | 프로세스 모듈(Node 호환) | 프로세스,argv,환경변수,exit,시그널,메모리사용량,종료훅 | 노드 방식 프로세스 다루기 — 강제 종료 때 정리 콜백이 도는지와 두 모듈의 구분 |
| jsh/javascript-psutil-module.md | 시스템 자원 모니터링 | psutil,CPU사용률,메모리,디스크,부팅시각,자원모니터링 | 시스템 자원을 자세히 보기 — CPU·메모리·스왑·프로토콜별 네트워크 카운터 |
| jsh/javascript-system-module.md | 시스템 유틸 모듈 | 시스템,현재시각,시간파싱,로그,location | 프로세스 id 등 시스템 정보를 얻는 유틸 |
| jsh/javascript-service-module.md | 서비스 모듈 | 서비스,service,서비스등록,servicectl,설치,시작,정지 | 장시간 도는 서비스를 스크립트로 만들고 등록·제어하기 |
| jsh/javascript-service-proxy.md | 서비스 프록시 | 서비스프록시,리버스프록시,라우트등록,프리픽스 | 내가 띄운 서버를 별도 포트 없이 밖에서 닿게 하기 — 주소 형식과 옵션 |
| jsh/javascript-events-module.md | 이벤트 모듈 | 이벤트,EventEmitter,리스너,on,once | 이벤트 리스너를 붙였다 떼기 — 개수 제한과 오류 이벤트 처리 |
| jsh/javascript-stream-module.md | 스트림 모듈 | 스트림,Readable,Writable,Transform,파이프,흘려보내기,데이터변환,변환클래스,이벤트,pipe,스트리밍,흐름처리 | 데이터를 스트림으로 흘려보내며 변환하는 클래스와 이벤트 |
| jsh/javascript-readline-module.md | 입력 읽기 모듈 | readline,입력받기,프롬프트,히스토리,대화형입력 | 대화형으로 여러 줄 입력받기 — 엔터에 바로 제출되지 않게 하기 |
| jsh/javascript-parser-module.md | 파서 모듈 | 파서,CSV파싱,NDJSON파싱 | 흘려보내며 CSV를 읽을 때 앞줄 건너뛰기와 헤더 직접 지정, 다른 형식 지원 |
| jsh/javascript-parseargs-module.md | 인자 파싱 모듈 | 인자파싱,명령행인자,parseArgs,플래그,도움말 | 명령행 인자 파싱 — 참/거짓 플래그의 부정 접두와 위치 인자 |
| jsh/javascript-splitfields-module.md | 필드 분리 모듈 | 필드분리,splitFields,구분자 | 공백으로 나누되 따옴표로 묶인 부분은 하나로 유지하기 |
| jsh/javascript-pretty-module.md | 출력 서식 모듈 | 표출력,pretty,테이블,진행률,바이트포맷 | 결과를 터미널에 표로 찍기 — 테두리 모양 고르기와 오래 걸리는 작업 표시 |
| jsh/javascript-tail-module.md | 파일 tail 모듈 | tail,로그추적,파일감시,SSE | 커지는 파일을 계속 따라 읽기 — 처음부터 읽게 하는 옵션 |
| jsh/javascript-zlib-module.md | 압축 모듈 | 압축,zlib,gzip,deflate,해제 | 데이터 압축 — 동기·콜백·스트림 세 방식과 헤더 없는 원시 방식 |
| jsh/javascript-zip-module.md | ZIP 모듈 | zip,압축,아카이브,해제 | 압축 묶음을 만들고 풀 때 항목마다 딸려 나오는 정보 |
| jsh/javascript-tar-module.md | TAR 모듈 | tar,압축,아카이브,해제 | 여러 파일을 하나로 묶고 푸는 것을 메모리에서 바로 하기 |
| jsh/javascript-semver-module.md | 버전 비교 모듈 | 버전비교,semver,버전범위 | 버전 제약을 비교하기 — 비어 있거나 최신을 뜻하는 값의 처리 |
| jsh/javascript-uuid-module.md | UUID 모듈 | UUID,고유식별자 | 고유 식별자(UUID)를 만들 때 고를 수 있는 버전과 생성 방법 |
| jsh/javascript-vizspec-module.md | VizSpec 시각화 모듈 | vizspec,ADVN,시각화,차트생성,SVG,PNG,ECharts변환 | 분석 결과를 렌더러에 안 매인 형식으로 남기고 여러 출력으로 바꾸기 |
| jsh/javascript-mathx-module.md | mathx 수학 모듈 | 수학,mathx,생성기,분석,통계 | 합성 파형 샘플 만들기 — 성분 지정과 최근 추가된 도우미 |
| jsh/javascript-analysis-module.md | 통계 분석 모듈 | 통계,평균,상관,공분산,분위수,누적분포 | 배열을 정렬·합산하고 평균·누적분포 같은 통계를 내는 함수, 각도의 순환성을 고려한 평균과 보간 곡선 |
| jsh/javascript-filter-module.md | 신호 필터 모듈 | 필터,이동평균,저역통과,칼만필터,스무더 | 신호에서 잡음을 걷어내는 필터 종류와 차이 |
| jsh/javascript-generator-module.md | 데이터 생성 모듈 | 데이터생성,arrange,linspace,meshgrid,난수,simplex | 균등 간격 수열·격자·노이즈·고유 식별자를 만드는 함수 |
| jsh/javascript-mat-module.md | 행렬 모듈 | 행렬,matrix,벡터,QR분해,선형대수 | 행렬 연산과 최소제곱 풀이, 제공하는 분해와 벡터 타입 |
| jsh/javascript-simplex-module.md | Simplex 노이즈 모듈 | simplex,노이즈,잡음생성 | 시드를 주고 노이즈 만들기 — 차원 한계와 같은 값의 재현성 |
| jsh/javascript-spatial-module.md | 공간 계산 모듈 | 공간,거리계산,haversine,위경도 | 두 좌표 사이의 지표면 거리를 구하는 계산 방식 |
| dbms/core-concepts/concepts-edition.md | Edition 개념 | 에디션,edition,standard,cluster,차이 | 한 대짜리와 여러 대짜리 구성에서 쓸 수 있는 기능이 어떻게 갈리는지 |
| dbms/core-concepts/concepts.md | 데이터 모델 개념 | 데이터모델,시계열,append-only,arrival_time,쓰기중심 | 시계열 데이터가 일반 관계형과 무엇이 다르고 테이블 타입이 왜 나뉘는지 |
| dbms/core-concepts/features-concepts.md | 주요 기능과 용어 구분 | 기능비교,용어,롤업역할,retention역할,백업관계,입력경로,용어구분,ROLLUP역할,Retention역할,백업마운트관계,입력경로비교,선택기준 | 롤업·보존정책·백업마운트가 각각 무슨 역할이고 입력 경로를 어떻게 고르는지 |
| dbms/core-concepts/storage-execution-architecture.md | 저장·실행 구조 | 아키텍처,저장구조,컬럼형,압축,인덱싱원리,실행계획,캐시 | 데이터가 내부에서 어떻게 저장되고 SQL이 어떻게 실행되는지 구조 |
| dbms/data-modeling-table-design/alter-data-mutation-policy.md | 데이터 변경 정책 | 데이터변경,UPDATE정책,DELETE정책,TRUNCATE,변경가능여부 | 테이블 종류별로 고치기·지우기·통째로 비우기가 되는지 안 되는지와 그 정책 |
| dbms/data-modeling-table-design/patterns-modeling.md | 모델링 패턴 | 모델링패턴,시간축,거리축,상태캐시,이벤트로그,마스터 | 운영에서 자주 쓰는 테이블 설계 패턴과 고르는 기준 |
| dbms/data-modeling-table-design/schema-objects-definition.md | 스키마 객체 정의 | 스키마설계,테이블생성,컬럼,데이터타입,제약조건,인덱스설계 | 테이블·컬럼·인덱스·뷰를 설계할 때 결정할 항목 |
| dbms/data-modeling-table-design/table-types-patterns-type-anti.md | 테이블 설계 안티패턴 | 안티패턴,잘못된설계,센서별테이블,타입오용,피해야할 | 테이블 설계에서 피해야 할 패턴과 올바른 대안 |
| dbms/data-modeling-table-design/table-types-selection-type.md | 테이블 타입 선택 | 테이블타입선택,타입비교,어떤테이블,TAG,LOG,LOOKUP,VOLATILE,TRANSACTION | 데이터 성격에 맞는 테이블 타입을 고르는 결정 흐름과 비교표 |
| dbms/development-tools-integration/cli-odbc.md | SQLCLI와 ODBC | ODBC,SQLCLI,C연동,연결문자열,헤더,라이브러리,고정소수점,행오류콜백,DECIMAL입력,C클라이언트,ARRAY,희소배열 | C/C++에서 SQLCLI나 표준 ODBC 드라이버로 붙을 때 고르는 기준과 헤더·라이브러리·연결 문자열 |
| dbms/development-tools-integration/concepts-common.md | 공통 연동 개념 | 연결문자열,인증,타임존,prepared statement,파라미터바인딩 | 어떤 드라이버를 쓰든 공통으로 챙길 것 — 연결 문자열, 시간대, 바인딩, 대량 입력, 오류 처리 |
| dbms/development-tools-integration/data-input-load-export.md | 데이터 입력과 반출 | 데이터입력,반출,LOAD DATA,입력방식선택,입력경로,반출경로,넣는방법,빼는방법,SAVE DATA INTO,Append API,machloader,csvimport,경로비교,도구비교,ARRAY | 데이터를 넣는 방법과 파일로 빼내는 방법이 여러 가지일 때 언제 뭘 쓰고 뭘 확인할지 |
| dbms/development-tools-integration/array-append.md | Sparse ARRAY와 선택 컬럼 Append | ARRAY_SPARSE,희소배열,일부위치입력,선택컬럼Append,부분입력,배열대량입력,요소위치,0-based | 배열의 일부 위치만 채워 넣기와 컬럼 일부만 골라 대량 입력하기 — 위치를 세는 기준과 언어별 방법 |
| dbms/development-tools-integration/go.md | Go 연동 (neo-client v2) | go연동,golang,neo-client,database/sql드라이버,machgo폐지,v2마이그레이션,ARRAY,희소배열 | Go에서 붙기 — v2는 표준 database/sql 드라이버 중심이고 v1의 machgo 패키지는 제공하지 않으므로 옮겨야 함 |
| dbms/development-tools-integration/jdbc.md | JDBC 연동 | JDBC,자바,java,드라이버설치,AUTH KEY | 자바에서 붙기 — 드라이버 설치와 빌드 도구 설정 |
| dbms/development-tools-integration/append-api.md | Append API | append,대량입력,고속입력,flush,close,세션,연속입력,행오류,오류콜백,Appender,ARRAY,희소배열 | 여러 행을 연속으로 빠르게 밀어 넣는 대량 입력 방식과 오류 콜백·마무리 처리 |
| dbms/development-tools-integration/database-metadata.md | DatabaseMetaData | 메타데이터API,테이블목록,컬럼정보,인덱스정보 | 드라이버로 테이블·컬럼·키·인덱스 정보를 조회하기 |
| dbms/development-tools-integration/migration-troubleshooting.md | 연동 마이그레이션과 문제 해결 | 드라이버전환,미지원기능,No suitable driver,연동오류 | 옛 드라이버에서 옮길 때 안 되는 기능과 자주 나는 오류 |
| dbms/development-tools-integration/prepared-types.md | PreparedStatement와 타입 | prepared,파라미터메타,바인드,재실행,자리표시자,플레이스홀더,이름바인드,Named Bind,named parameter,MachPreparedStatement,setObject,파라미터번호,ParameterMetaData | 바인드 변수에 번호 대신 이름을 붙여 쓰기와 타입별 바인딩 |
| dbms/development-tools-integration/resultset-lob.md | ResultSet와 LOB | ResultSet,BLOB,CLOB,스트림,메타데이터 | 조회 결과를 타입별로 읽기와 큰 이진·문자 데이터 다루기 |
| dbms/development-tools-integration/transaction-pooling.md | 트랜잭션과 커넥션 풀 | 커넥션풀,commit,rollback,격리수준,cursor | 자동으로 확정되는 상태에서 확정 명령을 부르면 어떻게 되는지와 쓸 수 있는 격리 수준 |
| dbms/development-tools-integration/net-connector.md | .NET Connector | 닷넷,dotnet,C#연동,net connector,ARRAY,희소배열 | 닷넷에서 붙기 — 설치와 연결 문자열 |
| dbms/development-tools-integration/node-js-typescript.md | Node.js·TypeScript 연동 | nodejs연동,typescript,npm,자바스크립트SDK,ARRAY,희소배열 | 노드 백엔드에서 쓸 패키지 이름과 설치, 브라우저에서도 되는지 |
| dbms/development-tools-integration/python.md | Python 연동 | 파이썬연동,python SDK,설치,예제,ARRAY,희소배열 | 파이썬에서 붙는 패키지 이름과 설치, 조회·입력 코드 |
| dbms/development-tools-integration/sdk-support-scope.md | SDK 기능 지원 범위 | SDK지원범위,nullable,ROWID반환,append지원,ARRAY | SDK별로 되는 기능과 진입점 비교 |
| dbms/development-tools-integration/selection-integration-method.md | 연동 방식 선택 | 연동선택,SDK선택,드라이버선택,결정순서 | 언어와 배포 환경에 맞는 연동 방식을 고르는 기준과 결정 순서 |
| dbms/getting-started/choose-next-doc.md | 다음 문서 선택 안내 | 문서선택,학습경로,다음문서,어디부터,무엇을먼저,문서선택,실습용입력,실제수집 | 빠른 시작을 마친 뒤 목적에 맞는 다음 문서 고르기 |
| dbms/getting-started/command-cheatsheet.md | 기본 명령 치트시트 | 치트시트,기본명령,요약 | 가장 자주 쓰는 명령만 모은 치트시트 — 접속, 테이블 확인, SQL 파일 실행 |
| dbms/getting-started/overview.md | Machbase DBMS 개요 | DBMS개요,머신베이스,시계열DB,소개,테이블구분 | 제품이 무엇이고 어떤 테이블 종류가 있으며 어디서부터 읽을지 |
| dbms/getting-started/quick-start.md | 10분 빠른 시작 | 빠른시작,quick start,첫실행,입문 | 서버에 붙어 테이블을 만들고 데이터를 넣고 조회하는 첫 실행 예제 |
| dbms/installation-deployment-upgrade/cluster-edition.md | Cluster Edition 설치와 배포 | 클러스터설치,노드역할,배포방식,구성 | 여러 대로 나눠 설치할 때 노드 역할과 배포 방식, 설치 순서 |
| dbms/installation-deployment-upgrade/pre-install-preparation.md | 설치 전 준비 | 설치준비,요구사항,패키지구성,라이선스 | 설치 전에 점검할 운영체제·자원·포트·커널 파라미터 |
| dbms/installation-deployment-upgrade/standard-edition.md | Standard Edition 설치 | 설치,리눅스설치,윈도우설치,설치경로 | 한 대에 설치할 때 압축 풀고 나서의 순서와 컨테이너로 하는 법 |
| dbms/installation-deployment-upgrade/upgrade.md | 업그레이드 | 업그레이드,버전올리기,업그레이드경로,확인사항 | 운영 중인 서버를 새 버전으로 올리는 절차와 사전 점검 |
| dbms/installation-deployment-upgrade/validation-checklist.md | 설치 검증 체크리스트 | 설치검증,체크리스트,설치확인 | 설치나 업그레이드를 끝낸 뒤 순서대로 확인할 항목 |
| dbms/log-table-usage/arrival-time-model.md | _arrival_time 시간 모델 | arrival_time,도착시각,시간모델 | 로그 테이블은 서버가 받은 시각으로 줄이 세워지는데 지난 시각을 끼워 넣을 수 있는지와 정밀도 |
| dbms/log-table-usage/log-constraints-errors-troubleshooting.md | LOG 제약과 오류 해결 | LOG제약,LOG오류,문제해결 | 로그 테이블에서 아예 안 되는 것과 대신 무엇을 써야 하는지 |
| dbms/log-table-usage/log-create-alter-drop.md | LOG 테이블 생성·변경·삭제 | LOG생성,LOG변경,LOG삭제,컬럼변경,ADD COLUMN,RENAME COLUMN,로그테이블만들기,로그테이블삭제,컬럼추가,ARRAY,배열 | 로그 테이블을 만들 때 종류를 안 적으면 무엇이 생기고 비면 안 되는 컬럼 선언 |
| dbms/log-table-usage/log-data-input-mutation.md | LOG 데이터 입력 | LOG입력,INSERT,append,파일적재,입력경로,로그입력,로그적재 | 로그 테이블에 넣는 경로 세 가지와 고를 기준 |
| dbms/log-table-usage/log-index-performance.md | LOG 인덱스와 성능 | LOG인덱스,인덱스선택,성능 | 로그 테이블에서 조회 조건별로 어떤 색인을 붙일지 |
| dbms/log-table-usage/log-operations-lifecycle.md | LOG 운영과 생명주기 | LOG운영,데이터삭제,OLDEST ROWS,EXCEPT ROWS,보존정책,백업후삭제,오래된행삭제,최근행만남기기,행수기준삭제,로그정리,로그삭제방법 | 로그 테이블에서 오래된 것부터 비우는 방법을 목적별로 |
| dbms/log-table-usage/log-overview-use-criteria.md | LOG 테이블 개요와 사용 기준 | LOG개요,로그테이블,사용기준,특성,설계순서 | 로그 테이블이 어떤 데이터에 맞는지 — 이벤트·패킷처럼 계속 추가되는 기록 |
| dbms/log-table-usage/log-patterns-scenarios.md | LOG 활용 패턴 | LOG활용,로그저장,텍스트검색사례 | 로그 테이블에 쌓인 기록을 시간대별로 묶고 본문 검색까지 거는 흐름 |
| dbms/log-table-usage/log-query-analysis.md | LOG 조회와 분석 | LOG조회,DURATION,스캔방향,실행계획,LOOKUP조인,로그조회,기간조회 | 로그 테이블을 상대 시간으로 범위 걸어 조회하고 결과 순서를 뒤집기 |
| dbms/log-table-usage/regex-network-query.md | 네트워크 타입 조회 | 네트워크타입,IPv4,IPv6,IP조회 | 주소를 문자로 넣으면 정렬이 엉키는 문제와 전용 타입으로 바꿨을 때 쓸 수 있는 비교 |
| dbms/log-table-usage/log-table-structure-schema.md | LOG 테이블 구조와 스키마 | LOG구조,LOG스키마,LOG설계 | 로그 테이블 컬럼을 짤 때 주소·포트를 어떤 타입으로 두고 왜 그런지 |
| dbms/log-table-usage/text-search-keyword-index.md | 텍스트 검색과 KEYWORD 인덱스 | 텍스트검색,전문검색,KEYWORD인덱스,SEARCH,REGEXP,정규식검색 | 본문에서 단어로 빨리 찾기와 패턴 검색의 차이 |
| dbms/lookup-table-usage/lookup-constraints-errors-troubleshooting.md | LOOKUP 제약과 오류 해결 | LOOKUP제약,LOOKUP오류,문제해결,여러줄변경,키로못쓰는,조건변경범위,PK불가오류 | 룩업 테이블에서 조건으로 고치면 여러 줄이 한꺼번에 바뀌는 것과 키로 못 쓰는 컬럼 오류 |
| dbms/lookup-table-usage/lookup-create-alter-drop.md | LOOKUP 테이블 생성·변경·삭제 | LOOKUP생성,AUTO_INCREMENT,SEQUENCE,LOOKUP삭제,룩업테이블만들기,룩업삭제,ARRAY,배열 | 룩업 테이블에서 키를 서버가 자동으로 만들게 하는 두 방법과 여러 컬럼이 업무 키일 때 |
| dbms/lookup-table-usage/lookup-data-input-mutation.md | LOOKUP 데이터 입력과 변경 | LOOKUP입력,UPDATE,중복키,TABLE_REFRESH,기준정보입력,기준정보수정 | 룩업 테이블에 같은 키가 또 들어올 때와 고친 값이 조회에 반영되게 하기 |
| dbms/lookup-table-usage/lookup-index-performance.md | LOOKUP 인덱스와 성능 | LOOKUP인덱스,튜닝,성능 | 룩업 테이블에서 키가 아닌 컬럼으로 찾을 때 붙어 있는 색인과 더 붙일 수 있는 것 |
| dbms/lookup-table-usage/json-column-query.md | JSON 컬럼과 조회 | JSON컬럼,JSON조회,JSON조건,JSON기본키,유동속성,속성덩어리,값종류,숫자조건,JSON_TYPEOF | 룩업 테이블에서 덩어리 값(JSON) 컬럼을 쓰고 경로 조건으로 조회하는 범위 |
| dbms/lookup-table-usage/lookup-operations-lifecycle.md | LOOKUP 운영과 생명주기 | LOOKUP운영,기준데이터변경,백업복구,점검 | LOOKUP 테이블의 백업·복구와 데이터 영속성을 다룹니다. |
| dbms/lookup-table-usage/lookup-overview-use-criteria.md | LOOKUP 테이블 개요와 사용 기준 | LOOKUP개요,룩업테이블,사용기준,특성,설계순서 | 룩업 테이블이 어떤 데이터에 맞는지 — 코드·임계값처럼 작고 자주 보는 기준 정보 |
| dbms/lookup-table-usage/lookup-patterns-scenarios.md | LOOKUP 활용 패턴 | LOOKUP활용,코드테이블,설비마스터,기준정보 | LOOKUP 테이블의 활용 패턴과 시나리오를 다룹니다. |
| dbms/lookup-table-usage/predicate-update-delete.md | 조건 UPDATE·DELETE | 조건업데이트,조건삭제,predicate,WHERE조건 | 룩업 테이블을 조건으로 고치고 지우기 — 조건 없이 지우면 어떻게 되는지와 권한 |
| dbms/lookup-table-usage/primary-key-policy.md | PRIMARY KEY 정책 | 기본키,PRIMARY KEY,키설계,키정책 | 룩업 테이블에서 업무 키가 두 컬럼 조합일 때와 나중에 키 값을 바꾸는 것 |
| dbms/lookup-table-usage/lookup-query-analysis.md | LOOKUP 조회와 분석 | LOOKUP조회,기본키조회,조인,JOIN | 룩업 테이블을 키·조건으로 조회하고 태그 데이터와 엮어 분석하기 |
| dbms/lookup-table-usage/sequence-column.md | SEQUENCE 컬럼 | 시퀀스,SEQUENCE,NEXTVAL,자동번호 | 같은 시각에 여러 건이 들어와 구분이 안 될 때 순번을 자동으로 붙이기 |
| dbms/lookup-table-usage/lookup-table-structure-schema.md | LOOKUP 테이블 구조와 스키마 | LOOKUP구조,LOOKUP스키마,LOOKUP설계 | 룩업 테이블은 디스크에 남는데 조회는 메모리에서 하고 서버를 켜면 무슨 일이 일어나는지 |
| dbms/operations-configuration-recovery/alter-system.md | ALTER SYSTEM 운영 | ALTER SYSTEM,CHECKPOINT,디스크사용량,라이선스설치,문장만끊기,접속유지,CANCEL,KILL,세션종료 | 서버 전체에 영향을 주는 관리 명령 — 오래 붙잡은 문장만 끊기, 접속 끊기, 체크포인트 |
| dbms/operations-configuration-recovery/ops-backup-restore-mount.md | 백업·복원·마운트 운영 | 백업운영,전체백업,증분백업,복원,마운트,AFTER,보관방식,백업종류,운영중조회,마운트조회,예전데이터조회,테이블백업,기간백업,증분,오프라인복원 | 백업 방식이 목적별로 어떻게 갈리고 서비스 중에 예전 백업을 들여다보는 방법 |
| dbms/operations-configuration-recovery/checklist-schema-alter.md | 스키마 변경 체크리스트 | 스키마변경점검,컬럼추가,컬럼삭제,인덱스변경 | 운영 중 스키마를 바꾸기 전에 순서대로 확인할 항목 |
| dbms/operations-configuration-recovery/ops-cluster.md | Cluster 운영 | 클러스터운영,노드시작,노드종료,상태확인 | 노드를 내리기 전에 확인할 것과 붙을 때 어디로 붙고 무엇으로 확인하는지 |
| dbms/operations-configuration-recovery/ops-configuration.md | 설정 운영 | 설정운영,설정파일,런타임변경,프로퍼티,메모리설정 | 설정을 바꿀 때의 절차 — 돌아가는 중에 반영되는 것과 재시작이 필요한 것 |
| dbms/operations-configuration-recovery/diagnosis-observability.md | 관측과 진단 | 진단,로그확인,trace log,서버로그,관측 | 문제가 났을 때 볼 로그와 상태 — 추적 로그 설정과 세션·저장소 확인 |
| dbms/operations-configuration-recovery/multi-database.md | 다중 데이터베이스 | 다중DB,데이터베이스분리,권한경계 | 한 서버에 논리 데이터베이스를 여럿 두고 운영할 때의 절차와 주의 |
| dbms/operations-configuration-recovery/policy-data-retention.md | 데이터 보존 정책 | 보존정책,retention,자동삭제,데이터수명 | 오래된 걸 알아서 지우게 하기 — 보존 기간과 실행 주기를 주고 달 단위 계산 |
| dbms/operations-configuration-recovery/server-database.md | 서버와 데이터베이스 운영 | 서버시작,서버종료,데이터베이스운영,라이선스 | 서버를 시작·종료하고 데이터베이스를 만들고 라이선스를 설치하기 |
| dbms/performance-tuning/index-tuning.md | 인덱스 튜닝 | 인덱스튜닝,인덱스성능,적용순서,접근경로,인덱스종류,REDBLACK,LSM,BITMAP,KEYWORD,EXPLAIN,실행계획,테이블별인덱스 | 테이블 종류별 기본 인덱스가 뭐고 뭘 더 붙일 수 있는지, 붙이는 순서와 실행 계획 확인 |
| dbms/performance-tuning/performance-approach.md | 성능 문제 접근 순서 | 성능접근,병목확인,진단순서,성능분석 | 성능 문제를 좁혀 가는 순서 — 재현 조건부터 한 번에 하나씩 바꾸기 |
| dbms/performance-tuning/performance-query-tuning.md | 조회 성능 튜닝 | 조회성능,쿼리튜닝,느린쿼리,EXPLAIN,실행계획 | 조회를 빠르게 하기 — 읽는 양과 정렬·집계 작업을 줄이는 방법과 실행 계획 보기 |
| dbms/performance-tuning/performance-tuning-modeling.md | 모델링 성능 튜닝 | 모델링튜닝,타입선택,스키마기준,집계설계 | 설계 단계에서 수명·조회 키·변경 방식에 맞는 테이블 종류와 스키마 고르기 |
| dbms/performance-tuning/perf-input-tuning.md | 입력 성능 튜닝 | 입력성능,적재속도,처리량측정,배치크기,동시성,병목분류 | 데이터를 넣는 속도를 올리기 — 무엇을 어떤 순서로 재고 어디가 막혔는지 가르기 |
| dbms/performance-tuning/tuning-storage-cluster.md | 스토리지·Cluster 튜닝 | 스토리지튜닝,checkpoint,용량,클러스터측정 | 노드마다 들어오는 양이 쏠릴 때 분산에 관여하는 설정과 함께 볼 것 |
| dbms/rdb-table-usage/rdb-backup-restore-mount.md | TRANSACTION 백업·복원·마운트 | TRANSACTION백업,복원,마운트,지원범위 | 관계형 테이블의 백업·복원·마운트 지원 범위와 검증 항목 |
| dbms/rdb-table-usage/rdb-constraints-errors-troubleshooting.md | TRANSACTION 제약과 오류 해결 | TRANSACTION제약,에디션제한,문제해결 | 관계형 테이블에서 안 되는 것과 자주 나는 오류 해결 |
| dbms/rdb-table-usage/rdb-create-alter-drop.md | TRANSACTION 테이블 생성·변경·삭제 | TRANSACTION생성,UNIQUE INDEX,AUTO_INCREMENT,변경,트랜잭션테이블만들기,인덱스생성,ARRAY,배열 | 관계형 테이블을 만드는 문법이 여러 가지일 때 결과가 같은지와 컬럼 변경 되돌리기 |
| dbms/rdb-table-usage/rdb-data-input-mutation.md | TRANSACTION 데이터 입력과 변경 | TRANSACTION입력,UPDATE,DELETE,INSERT SELECT,대량입력,행수정,행삭제,대량입력 | 관계형 테이블에 고속 입력을 쓸 수 있는지와 배치로 밀어 넣기 |
| dbms/rdb-table-usage/rdb-index-performance.md | TRANSACTION 인덱스와 성능 | TRANSACTION인덱스,JSON path인덱스,조회성능 | 관계형 테이블에서 키와 유일 색인이 개수·빈 값 처리에서 어떻게 다른지 |
| dbms/rdb-table-usage/insert-on-duplicate-key-update.md | 중복 키 갱신 입력 | ON DUPLICATE KEY UPDATE,중복키,upsert,덮어쓰기 | 없으면 넣고 있으면 고치기를 한 문장으로 — 어디서 되고 어떤 충돌에 반응하는지 |
| dbms/rdb-table-usage/join-relational-query.md | JOIN과 관계형 조회 설계 | 조인,JOIN설계,관계형조회 | 관계형 표를 다른 종류와 엮는 조합별 패턴과 빠르게 하려면 챙길 것 |
| dbms/rdb-table-usage/locking-conflict-timeout.md | 잠금·충돌·타임아웃 | 잠금,lock,충돌,busy timeout,동시성 | 서로 다른 줄을 고치는데도 부딪히는 이유와 뜨는 오류, 대기 시간 주기 |
| dbms/rdb-table-usage/rdb-operations-lifecycle.md | TRANSACTION 운영과 생명주기 | TRANSACTION운영,데이터정리,백업복구 | 관계형 테이블에 배치를 한 덩어리로 돌려 다른 쪽이 밀릴 때 나누는 방법 |
| dbms/rdb-table-usage/rdb-overview-use-criteria.md | TRANSACTION 테이블 개요와 사용 기준 | TRANSACTION개요,TXN,관계형테이블,RDB,사용기준,CREATE TXN TABLE,TRX,구버전이름,이름변경,테이블종류키워드,VOLATILE대체,사용가능이름,설계순서 | 관계형 테이블을 언제 쓰는지와 지금 쓸 수 있는 종류 키워드 |
| dbms/rdb-table-usage/rdb-query-analysis.md | TRANSACTION 조회와 분석 | TRANSACTION조회,SELECT,정렬,JOIN조회,집계,집계테이블,사전집계,업무조회,JSON경로,덩어리값,JSON path,LIMIT,필터링 | 관계형 테이블에서 원본을 집계해 따로 담고 덩어리 값 경로 조건 걸기 |
| dbms/rdb-table-usage/rdb-table-structure-schema.md | TRANSACTION 테이블 구조와 스키마 | TRANSACTION구조,스키마,설계 | 관계형 테이블이 언제 생겼고 컬럼은 최소 몇 개인지, 쓸 수 있는 타입 |
| dbms/rdb-table-usage/transaction.md | 트랜잭션 | 트랜잭션,COMMIT,ROLLBACK,트랜잭션경계 | 여러 변경을 하나로 묶는 시작 구문과 중간 지점 저장 후 되돌리기 |
| dbms/reference/command-line-tools.md | 명령행 도구 레퍼런스 | 명령행도구,CLI도구,도구목록,접속옵션,설치본,도구목록,단일노드,에디션별도구,사용불가 | 서버 관리·데이터 가져오기·쿼리 실행에 쓰는 명령행 도구 목록과 공통 접속 옵션 |
| dbms/cli/csvimport-csvexport.md | csvimport·csvexport 명령·옵션 | csvimport,csvexport,CSV입출력 | 파일 첫 줄을 컬럼 이름으로 삼고 테이블이 없으면 만들어 가며 넣기 |
| dbms/cli/machadmin.md | machadmin 명령·옵션 | machadmin,서버시작,서버종료,DB생성,DB삭제 | 비정상 종료 후 복구 방식을 고르고 백업 이미지 안을 들여다보는 관리 명령 |
| dbms/cli/machclusterctl.md | machclusterctl 명령·옵션 | machclusterctl,클러스터제어,YAML설정 | 여러 대 구성을 명령 하나로 관리하기 — 검증·설치·접속 |
| dbms/cli/machcoordinatoradmin.md | machcoordinatoradmin 명령·옵션 | machcoordinatoradmin,코디네이터 | 여러 대 구성에서 조정자 노드를 명령행으로 관리하는 옵션 |
| dbms/cli/machdeployeradmin.md | machdeployeradmin 명령·옵션 | machdeployeradmin,디플로이어,메타데이터관리 | 배포를 맡는 노드를 직접 시작·종료·강제 중지하기 |
| dbms/cli/machloader.md | machloader 명령·옵션 | machloader,CSV가져오기,CSV내보내기,대량적재,인코딩,ARRAY | 변환 규칙을 파일로 두고 데이터를 넣고 빼기 — 기존 걸 갈아엎는 모드 포함 |
| dbms/cli/machsql.md | machsql 명령·옵션 | machsql,SQL셸,대화형SQL,접속,공개키인증,ARRAY | 터미널에서 SQL을 대화형으로 실행하는 도구 — 접속 옵션과 스크립트 파일 실행 |
| dbms/cli/cli-tagmetaimport.md | tagmetaimport 명령·옵션 | tagmetaimport,메타가져오기,입력파일형식 | 이름표를 파일로 무더기 등록하기 — 탭 구분과 실패한 줄 모으기 |
| dbms/reference/configuration-reference.md | 설정 레퍼런스 | 설정레퍼런스,프로퍼티확인,동적변경 | 설정 자료가 어떻게 나뉘어 있는지와 껐다 켜지 않고 바꿀 수 있는 항목 |
| dbms/config/cluster-configuration.md | 클러스터 설정 프로퍼티 사전 | 클러스터설정,coordinator설정,broker설정,warehouse설정,클러스터포트 | 여러 대 구성에서 노드별 설정 파일의 주요 프로퍼티와 포트 구성 예 |
| dbms/config/configuration-timezone.md | Timezone 설정 사전 | 타임존설정,시간대설정,타임존우선순위 | Machbase는 클라이언트 접속 옵션으로 타임존을 지정할 수 있습니다. datetime 값은 내부적으로 나노초 값으로 처리되며, 타임존 옵션은 문자열 입출력 변환에 영향을 줍니다. |
| dbms/config/configuration-properties.md | 설정 프로퍼티 사전 | 설정프로퍼티,property,CPU설정,메모리설정,디스크설정,서버설정 | 한 대짜리 구성의 주요 설정 프로퍼티 — CPU·스레드·메모리·디스크·인덱스 |
| dbms/config/pvo-cache.md | PVO Cache 프로퍼티 사전 | PVO캐시,statement cache,캐시설정 | 실행 계획을 재사용하는 캐시의 프로퍼티와 조정 기준 |
| dbms/catalog/error-dictionary-codes.md | 오류 코드 사전 | 오류코드,에러코드,ERR,에러메시지,오류조회,MACH-ERR | 오류 번호로 원인을 찾는 사전 — 파서·테이블·입력 데이터·시스템 자원별 |
| dbms/catalog/log-logs-system-catalog.md | 시스템 카탈로그 레퍼런스 | 시스템카탈로그,카탈로그개요 | 서버 내부 메타데이터와 운영 상태를 SQL로 조회하는 읽기 전용 카탈로그 안내 |
| dbms/catalog/meta.md | 메타 테이블 사전 | 메타테이블,M$SYS_TABLES,M$SYS_COLUMNS,M$SYS_INDEXES,M$SYS_USERS,M$RETENTION,스키마정보 | M$ 접두 메타 테이블로 테이블 정의·컬럼·인덱스·사용자를 조회하기와 다중 데이터베이스에서 조인할 때의 식별자 규칙 |
| dbms/catalog/virtual-table-full.md | 전체 가상 테이블 레퍼런스 | 가상테이블전체,V$전체,세션뷰,스토리지뷰,통계뷰,V$PVO_CACHE_LIST,실행계획캐시,플랜캐시,페이지캐시,LRU,캐시목록,V$SESSION,V$STMT,V$SYSSTAT | 서버 상태를 보는 모든 가상 테이블 레퍼런스 — 세션·실행 계획 캐시·페이지 캐시 목록 |
| dbms/catalog/virtual.md | 가상 테이블 사전 | 가상테이블,V$VERSION,V$DATABASES,V$SESSION,V$STMT,V$PROPERTY,V$STORAGE_USAGE,실시간상태 | V$ 접두 동적 뷰로 서버 실시간 상태를 보기 — 버전·세션·문장·프로퍼티·저장소 사용량 |
| dbms/catalog/vrollup.md | V$ROLLUP 사전 | V$ROLLUP,롤업상태,RUN_STATE | 롤업이 꺼졌는지 돌고 있는지 상태를 보는 시스템 뷰 |
| dbms/catalog/vstorage-mount.md | V$STORAGE_MOUNT_DATABASES 사전 | 마운트조회,V$STORAGE_MOUNT_DATABASES | 읽기 전용으로 붙여 둔 백업이 어느 시점 데이터이고 별칭이 뭔지 보는 뷰 |
| dbms/reference/sql.md | SQL 레퍼런스 개요 | SQL레퍼런스,SQL특징,구문개요,SQL개요,구문안내 | SQL 문법·함수·타입·힌트를 어디서 찾는지 안내 |
| dbms/functions/functions-dictionary.md | 함수 사전 안내 | 함수사전,함수카테고리,함수공통규칙 | 내장 함수가 어떤 갈래로 나뉘고 공통으로 적용되는 규칙 |
| dbms/functions/aggregation.md | 집계 함수 | 집계함수,AVG,SUM,COUNT,MIN,MAX,STDDEV,백분위,APPROX_PERCENTILE,평균구하기,합계구하기,개수세기,최대최소,곱선아래넓이,면적,기울기,변화횟수,AREA,SLOPE,TS_CHANGE_COUNT | 집계 함수 — 평균·합계·개수와 분위값 근사 |
| dbms/functions/datetime.md | 날짜·시간 함수 | 시간함수,날짜함수,SYSDATE,NOW,TO_TIMESTAMP,FROM_UNIXTIME,DAYOFWEEK | 날짜·시간을 다루는 함수 — 요일, 구간 자르기, 형식 변환 |
| dbms/functions/functions-full.md | 전체 함수 레퍼런스 | 전체함수,함수전체목록,ABS,AVG,GROUP_CONCAT,SUBSTR,TO_CHAR,CAST,ARRAY_LENGTH,ARRAY_SPARSE,함수인자,함수반환 | 모든 내장 함수를 알파벳 순으로 모은 정본 — 인자·반환·예제와 오류 조건 |
| dbms/functions/nextval.md | NEXTVAL 함수 | NEXTVAL,시퀀스함수,자동번호 | 자동으로 하나씩 늘어나는 번호 붙이기 — 어디서만 되고 어느 문장에서 쓰는지 |
| dbms/functions/operators-json.md | JSON 함수와 dot 표기법 | JSON함수,JSONdot,점표기법,JSON_EXTRACT,JSON_TYPEOF,JSON_SET,JSON_REMOVE,JSON경로 | 덩어리 값(JSON)을 다루는 함수와 컬럼 뒤에 점을 찍어 멤버에 접근하는 문법 |
| dbms/functions/regex.md | 정규식 함수 | 정규식함수,REGEXP_LIKE,REGEXP_SUBSTR,REGEXP_REPLACE,정규식매칭,패턴추출,패턴치환 | 정규식으로 일치 검사·위치 찾기·추출·치환하기 |
| dbms/functions/series.md | 윈도우·시리즈 함수 | ROWNUM,SERIESNUM,SERIES BY,연속구간,행번호 | 결과 행에 번호를 붙이고 조건을 연속으로 만족하는 구간을 묶어 분석하기 |
| dbms/sql-syntax/relative-time-dictionary.md | 상대 시간 표현 | 상대시간,now,sysdate,시간연산,ADD_TIME,TO_DATE,몇시간전,몇일전,최근N시간 | 지금으로부터 얼마 전처럼 상대 시간을 SQL에 직접 적는 표현 |
| dbms/sql-syntax/rowid.md | ROWID | ROWID,행식별자,행위치 | 방금 넣은 행을 다시 찾을 때 쓰는 내부 식별자와 조회·계산 가능 여부 |
| dbms/sql-syntax/syntax-dictionary-sql.md | SQL 문법 사전 | 문법사전,지원구문목록,BNF,구문찾기,문법목록 | SQL 구문을 종류별로 찾아보는 사전 |
| dbms/sql-syntax/auto-increment-syntax.md | AUTO_INCREMENT | 자동증가,AUTO_INCREMENT,자동번호,자동번호부여,순번자동 | 서버가 정수 키를 자동으로 만들어 주기 — 테이블별 차이와 넣은 뒤 값 확인 |
| dbms/sql-syntax/backup-restore-mount-syntax.md | 백업·복원·마운트 문법 | 백업문법,BACKUP,RESTORE,MOUNT DATABASE,UMOUNT,백업하기,복원하기,마운트하기,언마운트 | 백업·복원·마운트 구문 — 전체·증분·기간 백업 구분 |
| dbms/sql-syntax/cte-syntax.md | WITH·CTE 문법 | CTE,WITH,공통테이블식,서브쿼리,임시결과,중간결과,서브쿼리대체,이름붙이기,재사용,별칭,재귀,임시이름 | 한 SQL 안에서 조회 결과에 이름을 붙여 재사용하는 WITH 절과 지원 범위 |
| dbms/sql-syntax/database-syntax.md | DATABASE 문법 — 데이터베이스 생성·삭제 | 데이터베이스,CREATE DATABASE,USE,다중데이터베이스,DB만들기,DB삭제,DB전환,논리단위,삭제옵션,RESTRICT,CASCADE,FORCE | 논리 데이터베이스를 만들고 지우고 바꿔 쓰는 구문과 삭제할 때 딸린 것을 함께 지우는 옵션 |
| dbms/sql-syntax/ddl-syntax.md | DDL 문법 — 테이블 생성·삭제·변경 | DDL,테이블생성,CREATE TABLE,DROP TABLE,ALTER TABLE,ADD COLUMN,RENAME COLUMN,TRUNCATE,IF NOT EXISTS,테이블만들기,테이블삭제,테이블변경,컬럼추가,컬럼삭제,컬럼이름변경,데이터비우기,전부비우기,스키마변경,ARRAY,배열컬럼 | 테이블을 만들 때 앞에 붙이는 종류 말과 안 붙였을 때 기본값, 저장 공간 정의와 색인 |
| dbms/sql-syntax/dml-syntax.md | DML 문법 — 데이터 입력·수정·삭제 | DML,INSERT,INSERT SELECT,UPDATE,DELETE,BEFORE,데이터입력,데이터삭제,데이터입력,데이터수정,데이터삭제,행삭제,컬럼지정입력,조회결과입력,날짜이전삭제,값변경,ARRAY,배열위치 | 테이블 종류별로 넣기·고치기·지우기가 되는지 표로 정리하고 이름표만 지우는 구문 |
| dbms/sql-syntax/lookup-predicate-delete-syntax.md | LOOKUP 조건 DELETE 문법 | LOOKUP삭제,조건삭제,조건으로삭제 | 룩업 테이블을 조건으로 지우기와 조건 없이 지웠을 때 |
| dbms/sql-syntax/lookup-predicate-update-syntax.md | LOOKUP 조건 UPDATE 문법 | LOOKUP업데이트,조건갱신,조건으로수정 | 룩업 테이블을 조건으로 고치기 — 지금 값을 기준으로 계산해 넣기와 못 바꾸는 컬럼 |
| dbms/sql-syntax/tag-data-update-syntax.md | TAG 데이터 UPDATE 문법 | TAG업데이트문법,METADATA UPDATE,태그수정,태그값수정,메타수정 | 태그 데이터를 고칠 때 쓸 수 있는 조건과 바꿀 수 있는 컬럼 |
| dbms/sql-syntax/tag-data-update-where-set-constraints.md | TAG UPDATE WHERE·SET 제약 | TAG업데이트제약,WHERE제약,SET제약,오류사례 | 태그 데이터를 고칠 때 조건이 거부되는 이유 — 이름 조건만 주면 왜 안 되는지와 뜨는 오류 번호 |
| dbms/sql-syntax/execute-procedure-syntax.md | EXEC 프로시저 | 프로시저실행,EXEC,TABLE_FLUSH,INDEX_FLUSH,TABLE_REFRESH,ROLLUPGAP,롤업갭확인,강제반영,캐시갱신,즉시적용 | 테이블과 롤업을 제어하는 EXEC 프로시저 — 반영 강제, 색인 정리 |
| dbms/sql-syntax/index-syntax.md | INDEX 문법 — 인덱스 생성·삭제 | 인덱스,CREATE INDEX,INDEX_TYPE,LSM,KEYWORD인덱스,TAG인덱스,인덱스만들기,인덱스생성방법,인덱스삭제,컬럼인덱스,값컬럼인덱스 | 색인을 만들고 지우는 구문과 테이블 종류별로 쓸 수 있는 색인 |
| dbms/sql-syntax/load-data-infile-syntax.md | LOAD DATA INFILE | 파일적재,LOAD DATA,대량적재,machloader비교,파일가져오기,CSV적재,파일입력 | 서버가 직접 파일을 읽어 넣기 — 첫 줄 컬럼명에 예약어나 특수문자가 섞였을 때 옵션 |
| dbms/sql-syntax/named-bind-parameter-syntax.md | 이름 바인드 파라미터 | 바인드파라미터,named parameter,파라미터바인딩,파라미터이름,바인딩방법 | 바인드 자리에 번호 대신 이름을 붙여 쓰기 — 쓸 수 있는 위치와 번호 방식과의 관계 |
| dbms/sql-syntax/pivot-syntax.md | PIVOT 문법 | 피벗,PIVOT,행열변환,행을열로,열로변환 | 행을 열로 돌려 요약표 만들기 — 조회문에 바로 붙일 수 있는지 |
| dbms/sql-syntax/retention-syntax.md | RETENTION 문법 — 보관 정책 생성·적용 | 보존정책,RETENTION,ADD RETENTION,자동삭제정책,보관정책,보존기간설정,정책적용,정책해제,자동정리 | 오래된 데이터를 자동으로 지우는 정책을 만들고 테이블에 붙이고 떼는 구문 |
| dbms/sql-syntax/rollup-rebuild-syntax.md | ROLLUP_REBUILD 문법 | 롤업재생성문법,ROLLUP_REBUILD,롤업다시만들기,롤업복구 | 원본이 수정됐을 때 지정한 시간 범위의 롤업 집계를 다시 계산하는 구문 |
| dbms/sql-syntax/rollup-syntax.md | ROLLUP 문법 — 롤업 생성·조회·제어 | 롤업문법,ROLLUP생성,ROLLUP조회,ROLLUP집계함수,롤업만들기,롤업삭제,롤업시작,롤업중지 | 롤업을 만들고 조회하고 제어하는 구문과 쓸 수 있는 집계 함수 |
| dbms/sql-syntax/save-data-into-syntax.md | SAVE DATA INTO | 파일저장,SAVE DATA,내보내기,파일내보내기,결과저장 | 조회 결과를 서버 파일로 내보내기 |
| dbms/sql-syntax/search-esearch-regexp-syntax.md | SEARCH·ESEARCH·REGEXP | 검색문법,SEARCH,ESEARCH,REGEXP,전문검색,문자열검색,단어검색,패턴검색 | 텍스트를 찾는 세 가지 방식의 차이와 성능 권장 |
| dbms/sql-syntax/select-hint-syntax.md | SELECT 힌트 | 힌트,hint,실행계획제어,실행계획지정,스캔방향 | 옵티마이저 동작을 주석으로 지시하기 — 실행 계획 제어와 태그 테이블 전용 힌트 |
| dbms/sql-syntax/interpolation-hint.md | INTERPOLATION 힌트 | 보간,INTERPOLATION,결측보정,빈값채우기,결측채우기 | 시계열에서 빠진 시간 구간을 계산으로 채워 반환하기 |
| dbms/sql-syntax/sampling-hint.md | SAMPLING 힌트 | 샘플링,SAMPLING,표본추출,표본조회,일부만조회 | 많은 데이터에서 일부만 골라 빠르게 훑는 샘플링 지시 |
| dbms/sql-syntax/select-syntax.md | SELECT 문법 — 데이터 조회 | SELECT,조회,WHERE,GROUP BY,HAVING,ORDER BY,LIMIT,데이터조회,정렬,필터,그룹화,상위N건 | 데이터를 조회·거르기·집계하는 SELECT 전체 문법과 각 절의 쓰임 |
| dbms/sql-syntax/series-syntax.md | SERIES BY 문법 | SERIES BY,시리즈,구간생성,구간나누기,시계열구간 | SERIES BY 절은 정렬된 결과 집합에서 특정 조건을 만족하는 연속적인 행의 구간(series)을 추출합니다. 연속된 구간에서 시작/종료 시각과 패턴을 분석할 때 사용합니다. |
| dbms/sql-syntax/set-operator-syntax.md | 집합 연산자 | UNION ALL,집합연산,합집합,결과합치기,합집합 | 두 조회 결과를 합치거나 교집합·차집합 구하기와 타입 호환 규칙 |
| dbms/sql-syntax/system-session-alter-syntax.md | SYSTEM·SESSION 설정 | ALTER SYSTEM,ALTER SESSION,시스템설정,세션설정,설정변경,세션설정변경 | 서버 전역 설정과 현재 세션 설정 바꾸기 — 세션 끊기, 문장만 취소, 체크포인트 |
| dbms/sql-syntax/user-auth-syntax.md | 사용자·권한 문법 | 사용자,계정,USER,GRANT,REVOKE,권한,비밀번호변경,계정만들기,계정삭제,권한부여,권한회수,비밀번호변경 | 사용자를 만들고 지우고 권한을 주고 회수하기, 공개키 기반 인증 키 관리 |
| dbms/sql-syntax/view-syntax.md | VIEW 문법 — 뷰 생성·삭제 | 뷰,VIEW,CREATE VIEW,DROP VIEW,뷰만들기,뷰삭제,뷰조회 | 저장해둔 조회 정의를 만들고 통째로 바꾸기, 실행할 때 조건 값 넘기기 |
| dbms/sql-syntax/window-function-over-syntax.md | 윈도우 함수와 OVER | 윈도우함수,OVER,파티션,순위,누적,순위매기기,누적합,이전값,다음값 | 윈도우 함수(Window Function)는 결과 행을 그룹으로 축소하지 않고 각 행에 대해 집계 또는 순위 계산을 수행하는 함수입니다. OVER() 절을 사용해 계산 범위(윈도우)를 정의합니다. |
| dbms/sql-types/type-data-types-dictionary.md | 데이터 타입 사전 | 데이터타입,타입목록,정수,부동소수점,문자열,날짜시간,IP,ARRAY,배열타입 | 쓸 수 있는 데이터 타입과 각각의 범위·용도 |
| dbms/sql-types/array.md | 숫자 ARRAY 타입 | ARRAY,배열타입,배열컬럼,고정길이배열,요소조회,ARRAY_LENGTH,cardinality,배열컬럼추가,배열CAST,배열NULL | 한 행에 같은 숫자 타입 값을 정해진 개수만큼 담는 배열 — 만들기와 나중에 추가하기, 요소 하나씩 꺼내기, 통째로 바꾸기, 배열이 아예 없는 것과 요소만 없는 것의 구분 |
| dbms/sql-types/decimal-numeric-fixed-point.md | DECIMAL·NUMERIC 고정소수점 | 고정소수점,DECIMAL,NUMERIC,정밀도,반올림 | 10진수를 오차 없이 담는 고정소수점 타입 — 반올림과 범위 초과, 테이블별 지원 |
| dbms/sql-types/table-types-type-support-scope-json.md | JSON 타입 지원 범위 | JSON지원,JSON타입,테이블별JSON | 덩어리 값(JSON) 컬럼을 어느 테이블에 만들 수 있고 경로 색인은 어디까지 되는지 |
| dbms/reference/support-scope-constraints.md | 지원 범위와 제약 개요 | 지원범위,제약,표기규칙 | 구성별·테이블별·SDK별로 무엇이 되고 안 되는지 빠르게 보는 안내 |
| dbms/reference/backup-mount.md | 백업·마운트 지원표 | 백업지원,마운트지원,테이블별백업,구성별지원,오프라인복구,붙이기떼기,지원표 | 떠 놓은 걸 붙였다 떼는 기능이 구성별·테이블 종류별로 되는지 표 |
| dbms/reference/compatibility-version.md | 버전 호환성 | 버전호환,하위호환,업그레이드,8.7.0,ARRAY | 옛날 드라이버로 새 서버에 붙으면 어떻게 되는지와 새로 생긴 구문, 제거된 기능 |
| dbms/reference/compatibility-xma-protocol.md | 서버·SDK 호환성 | SDK호환,프로토콜호환,버전확인,ARRAY | 서버와 SDK 버전이 다를 때 되는 것과 안 되는 것 — 인증·메타데이터·이름 바인드 |
| dbms/reference/edition.md | Edition별 기능 지원표 | 에디션비교,standard,cluster,기능지원,선택기준 | 한 대짜리와 여러 대짜리 구성의 기능 비교와 고르는 기준 |
| dbms/reference/lookup-sql-json.md | LOOKUP SQL·JSON 지원표 | LOOKUP JSON지원,지원현황 | 룩업 테이블에서 덩어리 값에 쓸 수 있는 SQL 범위 표 |
| dbms/reference/support-scope-privileges.md | 권한별 기능 지원표 | 권한지원,GRANT,REVOKE,권한필요작업 | 권한을 묶어서 한 번에 주는 이름과 작업별로 필요한 권한 |
| dbms/reference/rdb.md | TRANSACTION 기능 지원표 | TRANSACTION지원,기능지원여부 | 관계형 테이블에서 어떤 SQL 기능이 되는지 정리한 표 |
| dbms/reference/support-scope-rollup.md | ROLLUP 지원 범위 | 롤업지원범위,롤업제약 | 롤업이 구성별·테이블별로 되는지와 손으로 돌리거나 멈추는 명령 |
| dbms/reference/table-types-type.md | 테이블 타입별 기능 지원표 | 테이블타입지원,기능지원표,타입별제약,비교표,ARRAY | 다섯 가지 테이블 유형이 각각 무엇을 지원하는지 종합 표 |
| dbms/reference/tag-data-update.md | TAG UPDATE 지원표 | TAG업데이트지원,WHERE지원,SET지원,계측값수정,UPDATE조건,조건절지원,메타데이터수정,이름표수정,SET컬럼,값보정 | 이미 쌓인 계측값을 고칠 때 쓸 수 있는 조건과 이름표 정보 수정 |
| dbms/security-access-control/access-control.md | 접속 제어 | 접속제어,원격접속,BIND_IP_ADDRESS,네트워크노출 | 원격에서 붙을 수 있게 허용하고 어느 주소로 받을지 제한하는 접속 제어 설정 |
| dbms/security-access-control/account.md | 계정 관리 | 계정,사용자생성,사용자삭제,비밀번호정책,계정삭제,활성세션,비밀번호규칙,비밀번호길이,비밀번호조건,패스워드,DROP USER,CREATE USER | 사용자를 만들고 지우기, 활성 세션이 있는 계정 삭제, 비밀번호 규칙 |
| dbms/security-access-control/authentication-auth-key.md | AUTH KEY 인증 | AUTH KEY,키인증,키롤오버,challenge | 비밀번호 대신 공개키로 인증하기 — 등록·활성화와 클라이언트 설정 |
| dbms/security-access-control/checklist-configuration.md | 보안 설정 체크리스트 | 보안체크리스트,보안점검,설정확인 | 운영 배포 전과 정기 감사 때 점검할 보안 설정 항목 |
| dbms/security-access-control/security-privileges.md | 권한 관리 | 권한관리,GRANT,REVOKE,데이터베이스권한,테이블권한,CONNECT권한,권한진단 | 데이터베이스 범위 관리 권한과 테이블 권한을 주고 회수하기, 권한이 모자랄 때 점검 순서 |
| dbms/security-access-control/security-model.md | 보안 모델 개요 | 보안모델,보안구조,SYS계정,최소권한 | 계정·권한·접속 제어가 어떻게 맞물리는지와 기본 계정 |
| dbms/tag-rollup-usage/conditional-rollup.md | 조건 ROLLUP | 조건롤업,조건부집계,이상치제외,튀는값,이상치제외,판정컬럼,조건집계 | 튀는 값을 빼고 통계만 미리 만들기 — 판정에 쓴 컬럼이 결과에 남는지와 조회 방법 |
| dbms/tag-rollup-usage/create-delete-rollup.md | ROLLUP 생성과 삭제 | 롤업생성,롤업삭제,WITH ROLLUP,CREATE ROLLUP | 롤업을 만들고 지우기 — 자동으로 만들어질 때 이름이 어떻게 붙고 딸린 것을 한꺼번에 지우기 |
| dbms/tag-rollup-usage/custom-rollup.md | Custom ROLLUP | 커스텀롤업,사용자정의롤업,다중센서,비율집계 | 내가 쓴 집계식을 주기적으로 돌려 결과를 따로 쌓는 롤업(Standard Edition 전용) |
| dbms/tag-rollup-usage/extension-rollup.md | 확장 ROLLUP과 FIRST/LAST | 확장롤업,EXTENSION,FIRST,LAST | 구간의 첫 값과 마지막 값이 필요할 때 만들 롤업과 같은 주기에 둘 다 있을 때 |
| dbms/tag-rollup-usage/ingestion-control-rollup.md | ROLLUP 제어와 상태 확인 | 롤업제어,롤업시작,롤업중지,V$ROLLUP,ROLLUPGAP,롤업갭,즉시집계,즉시수집,WAKEUP,FORCE,트리거,대기,동기,비동기,로드후집계,WAKEUP INTERVAL | 넣자마자 집계 결과를 보기 — 트리거만 하는 것과 끝날 때까지 기다리는 것의 차이 |
| dbms/tag-rollup-usage/json-summarized-rollup.md | JSON SUMMARIZED ROLLUP | JSON롤업,SUMMARIZED,json집계 | 덩어리 값 안의 숫자 필드를 미리 집계하기 — 경로 적는 법과 문자열이 섞였을 때 |
| dbms/tag-rollup-usage/rollup-overview-use-criteria.md | ROLLUP 개요와 사용 기준 | 롤업개요,롤업이란,사용기준,기본동작,설계순서 | 롤업을 쓸지 말지와 어떤 종류를 고를지 기준 — 거리 기준으로 쌓는 표에도 되는지 |
| dbms/tag-rollup-usage/rollup-patterns-scenarios.md | ROLLUP 활용 시나리오 | 롤업시나리오,롤업활용,센서분석 | 롤업을 만들고 상태를 확인한 뒤 구간 집계를 조회하는 흐름을 단계로 |
| dbms/tag-rollup-usage/performance-tuning-rollup.md | ROLLUP 성능 튜닝 | 롤업성능,롤업튜닝,최적화 | 롤업으로 얼마나 빨라지는지와 계층 설계, 조회 힌트 |
| dbms/tag-rollup-usage/query-syntax-rollup.md | ROLLUP 조회 문법 | 롤업조회,조회문법,시간단위,주월연,origin | 미리 집계한 값을 꺼내 쓰는 함수 인자와 주 단위로 볼 때 경계 기준 |
| dbms/tag-rollup-usage/rollup-rebuild.md | ROLLUP 재생성 | 롤업재생성,ROLLUP_REBUILD,재구축,정의변경 | 원본을 보정한 뒤 영향받은 구간만 다시 계산할지 통째로 다시 만들지 정하기 |
| dbms/tag-rollup-usage/target-tag-table-design.md | ROLLUP 대상 테이블 설계 | 롤업대상,롤업설계,SUMMARIZED설계 | 롤업 계층을 어떻게 쌓고 위쪽은 무엇을 소스로 삼으며 저장 공간을 어림하기 |
| dbms/tag-table-usage/tag-constraints-errors-troubleshooting.md | TAG 제약과 오류 해결 | TAG오류,TAG제약,문제해결,WHERE오류,SET오류 | WHERE 절에 태그 선택 조건과 BASETIME 조건이 모두 있어야 합니다. 조건이 모호하거나 허용되지 않는 형태이면 UPDATE가 거부됩니다. |
| dbms/tag-table-usage/tag-create-alter-drop.md | TAG 테이블 생성·변경·삭제 | TAG생성,CREATE TAG TABLE,TAG변경,TAG삭제,태그테이블만들기,태그테이블삭제,기준축,축컬럼,BASEDISTANCE,거리축,속성저장위치,ARRAY,배열 | 태그 테이블을 만들 때 기준 축을 몇 개 잡는지, 태그마다 한 번만 저장하는 속성은 어디에 두는지 |
| dbms/tag-table-usage/tag-data-input-mutation.md | TAG 데이터 입력과 변경 | TAG입력,INSERT,입력경로,데이터정정,태그입력,센서값입력 | 태그 테이블에 넣는 방법과 이름표를 함께 등록하기 |
| dbms/tag-table-usage/tag-index-performance.md | TAG 인덱스와 성능 | TAG인덱스,조회경로,secondary index,성능 | 태그 테이블 색인과 조회 성능 |
| dbms/tag-table-usage/tag-operations-lifecycle.md | TAG 운영과 생명주기 | TAG운영,데이터삭제,중복제거,점검순서,태그데이터삭제,오래된데이터정리 | 태그 계측값을 지우는 조건과 같은 값이 또 들어올 때의 처리 |
| dbms/tag-table-usage/tag-overview-use-criteria.md | TAG 테이블 개요와 사용 기준 | TAG개요,태그테이블이란,사용기준,설계순서,특성 | 이름으로 구분되는 대상의 계측값을 담을 때 태그 테이블 특성 |
| dbms/tag-table-usage/tag-patterns-scenarios.md | TAG 활용 패턴 | TAG활용,활용사례,시나리오 | 태그 테이블을 실제로 어디에 쓰는지 사례와 맞지 않는 경우 |
| dbms/tag-table-usage/tag-query-analysis.md | TAG 조회와 분석 | TAG조회,시간범위조회,거리축조회,다중태그,통계뷰,실행계획 | 태그 테이블을 구간으로 조회할 때 색인을 타는지 실행 계획에서 확인 |
| dbms/tag-table-usage/tag-table-structure-schema.md | TAG 테이블 구조와 스키마 | TAG구조,TAG스키마,설계,binary컬럼,LSL,USL,허용범위,규격한계,범위위반,TRACE로그,위반기록,자동중복제거,값컬럼설계,VARCHAR최적화,시간축,거리축,ARRAY | 태그 테이블 컬럼 설계 — 시간축·거리축 고르기, 값 범위를 벗어나면 흔적 남기기, 이진 데이터 |
| dbms/tag-table-usage/tag-data-update-correction.md | TAG 데이터 UPDATE와 보정 | TAG업데이트,데이터보정,대량정정,UPDATE성능 | 값을 고치되 원본 흔적을 남기는 설계와 양이 많을 때 주의 |
| dbms/tag-table-usage/tag-metadata.md | TAG 메타데이터 | 태그메타데이터,METADATA,메타컬럼,메타입력,메타수정,메타삭제,메타등록,메타조회,메타변경,ARRAY | 태그 속성을 넣고 고치는 구문과 마지막으로 바뀐 시각이 어디 남는지 |
| dbms/tag-table-usage/tag-tagmetaimport.md | 메타데이터 일괄 등록 | tagmetaimport,메타일괄등록,메타가져오기 | 태그 이름표를 CSV로 무더기 등록하거나 갱신하는 도구와 파일 형식 |
| dbms/troubleshooting/trouble-cluster.md | Cluster 문제 | 클러스터문제,노드비정상,에디션제한오류 | 클러스터가 이상할 때 토폴로지 변경·재시작 전에 무엇을 수집하고 어디를 보는지 |
| dbms/troubleshooting/item.md | 입력·적재 문제 | 입력실패,적재실패,CSV실패,컬렉터실패,파일입력실패,업로드실패,인코딩,문자셋,EUCJP,KSC5601,UTF8,import실패,적재오류,확인순서,machloader실패 | 파일로 밀어 넣는 게 실패할 때 확인 순서와 인코딩 이름을 어디서 대조하는지 |
| dbms/troubleshooting/performance.md | 쿼리·성능 문제 | 쿼리느림,성능문제,검색결과이상,메모리부족 | 결과가 예상과 다르거나 느릴 때 확인 순서 — 시간대 설정 포함 |
| dbms/troubleshooting/recovery-backup.md | 백업·복구 문제 | 백업실패,복원실패,마운트실패 | 백업이나 복원이 실패할 때 볼 것 — 경로 권한, 남은 공간, 기존 백업 |
| dbms/troubleshooting/trouble-rollup.md | ROLLUP 문제 | 롤업문제,롤업갭,롤업불일치,롤업보정 | 롤업 결과가 늦거나 원본과 다를 때 상태·gap 확인부터 재구성까지 |
| dbms/troubleshooting/server-connection.md | 서버·연결 문제 | 서버시작실패,연결실패,접속불가,인증실패 | 연결이 안 될 때 서버 시작·TCP 연결·인증 순서로 나눠 확인 |
| dbms/troubleshooting/trouble-approach.md | 문제 해결 접근법 | 문제해결절차,5단계,진단명령,증상확인,오류코드로원인찾기 | 문제를 좁혀 가는 5단계와 진단 명령·로그·오류 코드로 원인 찾기 |
| dbms/volatile-table-usage/volatile-constraints-errors-troubleshooting.md | VOLATILE 제약과 오류 해결 | VOLATILE제약,메모리부족,재시작소실,문제해결 | 휘발성 테이블에서 못 쓰는 것과 메모리 부족·키 오류·재시작 후 데이터가 사라지는 문제 해결 |
| dbms/volatile-table-usage/volatile-create-alter-drop.md | VOLATILE 테이블 생성·변경·삭제 | VOLATILE생성,VOLATILE삭제,영속성차이,휘발성테이블만들기,ARRAY,배열 | 휘발성 테이블을 껐다 켜면 데이터만 사라지는지 구조까지 사라지는지 |
| dbms/volatile-table-usage/volatile-data-input-mutation.md | VOLATILE 데이터 입력과 변경 | VOLATILE입력,갱신,삭제 | 휘발성 테이블에 같은 키로 또 넣을 때 바꿀 컬럼을 안 적으면 어떻게 되는지 |
| dbms/volatile-table-usage/volatile-index-performance.md | VOLATILE 인덱스와 성능 | VOLATILE인덱스,성능,설계기준 | 휘발성 테이블에 붙일 수 있는 색인과 안 되는 것 |
| dbms/volatile-table-usage/volatile-operations-lifecycle.md | VOLATILE 운영과 생명주기 | VOLATILE운영,세션공유,재시작,데이터소실 | VOLATILE 테이블의 생성·적재·사용·소멸·재구성 절차를 정리합니다. |
| dbms/volatile-table-usage/volatile-overview-use-criteria.md | VOLATILE 테이블 개요와 사용 기준 | VOLATILE개요,휘발성테이블,메모리테이블,사용기준 | 휘발성 테이블이 어떤 데이터에 맞는지 — 껐다 켜면 사라져도 되는 최신 상태 |
| dbms/volatile-table-usage/volatile-query-analysis.md | VOLATILE 조회와 분석 | VOLATILE조회,기본키조회,임시집계 | 휘발성 테이블에서 낸 임시 집계와 키가 아닌 컬럼으로 찾기 |
| dbms/volatile-table-usage/volatile-table-structure-schema.md | VOLATILE 테이블 구조와 스키마 | VOLATILE구조,VOLATILE스키마,기본키설계 | 휘발성 테이블을 키 없이 만들어도 되는지와 그때 못 쓰게 되는 동작 |
