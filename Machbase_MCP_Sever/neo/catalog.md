# Document Catalog

| path | title_ko | keywords |
|------|----------|----------|
| api/api-grpc/grpc-csharp.md | C# gRPC 클라이언트 | protobuf,X.509,TLS handshake,MachRpc stub |
| api/api-grpc/grpc-exec.md | gRPC Exec 쿼리 실행 | DDL DML,parameter binding,success failure |
| api/api-grpc/grpc-guide.md | gRPC API 개요 | proto file,protobuf,low-level API |
| api/api-grpc/grpc-java.md | Java gRPC 클라이언트 | protoc code generation,Maven,stream blocking stub |
| api/api-grpc/grpc-python.md | Python gRPC 클라이언트 | grpc_tools protoc,gRPC channel,streaming writer |
| api/api-grpc/grpc-query.md | gRPC Query 다중 레코드 | result handle,rows close,rows fetch loop |
| api/api-grpc/grpc-queryrow.md | gRPC QueryRow 단일 레코드 | single record fetch,count aggregate |
| api/api-http/http-create-drop-table.md | HTTP DDL 테이블 관리 | tag table creation,summarized statistics |
| api/api-http/http-csharp.md | HTTP C# 클라이언트 | HttpClient,URL encoding,CSV JSON format |
| api/api-http/http-go.md | HTTP Go 클라이언트 | net/http,URL escape,JSON POST body |
| api/api-http/http-guide.md | HTTP API 엔드포인트 | /db/query,/db/write,TQL endpoints,REST |
| api/api-http/http-javascript.md | HTTP JavaScript 클라이언트 | fetch API,encodeURIComponent,text JSON response |
| api/api-http/http-lineprotocol.md | InfluxDB Line Protocol 호환 | telegraf,measurement translation,field value mapping |
| api/api-http/http-python.md | HTTP Python 클라이언트 | requests,pandas dataframe,gzip compression |
| api/api-http/http-query.md | HTTP Query API | format parameter,transpose,rowsFlatten,timeformat |
| api/api-http/http-ui.md | HTTP 웹 UI API | JWT authentication,token refresh,WebSocket terminal |
| api/api-http/http-upload-files.md | HTTP 파일 업로드 | multipart form data,X-Store-Dir,JSON metadata |
| api/api-http/http-watch-data.md | HTTP SSE 실시간 감시 | Server-Sent Events,keep-alive,period parameter |
| api/api-http/http-write.md | HTTP Write API | INSERT APPEND,timeformat zone,CSV JSON NDJSON |
| api/api-mqtt/mqtt-csharp.md | MQTT C# 클라이언트 | MQTTnet,QoS,TCP socket |
| api/api-mqtt/mqtt-go.md | MQTT Go 클라이언트 | paho mqtt,protocol version,topic subscription |
| api/api-mqtt/mqtt-guide.md | MQTT API 개요 | write flow,query flow,append mode,reply topic |
| api/api-mqtt/mqtt-javascript-websocket.md | MQTT JavaScript WebSocket | mqtt.js,event handler,WebSocket address |
| api/api-mqtt/mqtt-python.md | MQTT Python 클라이언트 | paho-mqtt,callback,publish QoS |
| api/api-mqtt/mqtt-query.md | MQTT Query | db/query topic,reply field,JSON CSV box format |
| api/api-mqtt/mqtt-write.md | MQTT v3.1 Write | append write method,payload format,gzip compression |
| api/api-mqtt/mqtt-writev5.md | MQTT v5 Write | user properties,method format compress,header skip columns |
| bridges/bridge-mqtt.md | MQTT Bridge 외부 브로커 | publish subscribe,TQL script,mosquitto,topic subscription |
| bridges/bridge-mssql.md | MSSQL Bridge | server user password,encryption mode,bridge exec query |
| bridges/bridge-mysql.md | MySQL Bridge | parseTime option,AUTO INCREMENT,bridge exec INSERT |
| bridges/bridge-nats.md | NATS Bridge 메시지 | NATS server,subject name,queue group,fire-and-forget |
| bridges/bridge-overview.md | Bridge Subscriber 개요 | bridge definition,subscriber registration,TQL pipeline |
| bridges/bridge-postgresql.md | PostgreSQL Bridge | host port dbname,sslmode verify,table creation |
| bridges/bridge-sqlite.md | SQLite Bridge | memory mode,file connection,bridge test |
| dbms/advanced-features/advanced-features-backup-restore.md | 백업과 복원 | full-backup,incremental-backup,time-range-backup,restore,offline-restore |
| dbms/advanced-features/advanced-features-create-delete.md | 스트림 생성 및 삭제 | STREAM_CREATE,STREAM_DROP,INSERT-SELECT,aggregation |
| dbms/advanced-features/advanced-features-database-mount.md | 데이터베이스 마운트 | MOUNT,UNMOUNT,read-only,mounted-database |
| dbms/advanced-features/advanced-features-overview.md | 고급 기능 개요 | BACKUP,MOUNT,online-backup,cold-backup,data-retention |
| dbms/advanced-features/advanced-features-retention.md | 데이터 보관 정책 | CREATE-RETENTION,retention-policy,DURATION,INTERVAL,auto-delete |
| dbms/advanced-features/advanced-features-sample.md | 스트림 사용 샘플 | STREAM_START,STREAM_EXECUTE,V$STREAMS,real-time-insert |
| dbms/advanced-features/advanced-features-startup-shutdown.md | 스트림 시작 및 중지 | STREAM_START,STREAM_STOP,STREAM_EXECUTE,BY-USER |
| dbms/common-tasks/common-tasks-backup-recovery.md | 백업 및 복구 전략 | offline-backup,online-backup,CSV-export,disaster-recovery |
| dbms/common-tasks/common-tasks-connecting.md | Machbase 연결 방법 | machsql,ODBC,JDBC,REST-API,connection-pooling |
| dbms/common-tasks/common-tasks-importing-data.md | 데이터 임포트 방법 비교 | machloader,APPEND-API,CSV-import,bulk-insert,data-validation |
| dbms/common-tasks/common-tasks-querying.md | 데이터 쿼리 기법 | DURATION,rollup-query,aggregation,text-search,JOIN |
| dbms/common-tasks/common-tasks-user-management.md | 사용자 관리 | CREATE-USER,GRANT,password-policy,permission-levels |
| dbms/configuration/configuration-meta-table.md | 메타 테이블 | M$SYS_TABLES,M$SYS_COLUMNS,M$SYS_INDEXES,table-metadata |
| dbms/configuration/configuration-property-cl.md | 클러스터 프로퍼티 | command-line-properties,machadmin,configuration-parameter |
| dbms/configuration/configuration-property.md | 서버 프로퍼티 | CPU_AFFINITY,DISK_IO_THREAD,INDEX_BUILD,memory-tuning |
| dbms/configuration/configuration-timezone.md | 타임존 설정 | TIMEZONE-format,session-timezone,UTC-conversion |
| dbms/configuration/configuration-virtual-table.md | 가상 테이블 | V$SESSION,V$PROPERTY,V$STORAGE,monitoring,system-info |
| dbms/core-concepts/core-concepts-indexing.md | 인덱싱과 성능 | LSM-index,tag-table-index,3-level-partitioned,query-optimization |
| dbms/core-concepts/core-concepts-table-types-overview.md | 테이블 타입 비교 | tag-table,log-table,volatile-table,lookup-table,table-selection |
| dbms/core-concepts/core-concepts-time-series-data.md | 시계열 데이터 이해 | append-only,columnar-storage,compression,write-heavy |
| dbms/getting-started/getting-started-concepts.md | 기본 개념 | Machbase 특성,write-heavy,table_types,DURATION |
| dbms/getting-started/getting-started-first-steps.md | machsql 첫 단계 | machsql,SHOW-commands,CREATE-TABLE,INSERT |
| dbms/getting-started/getting-started-installation.md | 설치 가이드 | Linux-tarball,Docker,Windows-MSI |
| dbms/getting-started/getting-started-quick-start.md | 빠른 시작 | database-creation,_arrival_time,첫쿼리 |
| dbms/installation/cluster/installation-cluster-cluster-env.md | 클러스터 환경 준비 | file_limit,ulimit,NTP-sync |
| dbms/installation/cluster/installation-cluster-command-line-coordinator-deployer-install.md | Coordinator/Deployer 설치 | Coordinator,Deployer,클러스터설정 |
| dbms/installation/cluster/installation-cluster-command-line-lookup-broker-warehouse-install.md | Lookup/Broker/Warehouse 설치 | lookup_node,broker,warehouse,노드추가 |
| dbms/installation/cluster/installation-cluster-command-line.md | 클러스터 설치 명령어 | 클러스터설치,command_line,노드관리 |
| dbms/installation/installation-license.md | 라이선스 설치 | license-key,license-limitations,APPEND-protocol |
| dbms/installation/installation-package.md | 패키지 개요 | package-structure,edition-types,version-format |
| dbms/installation/installation-upgrade.md | 클러스터 업그레이드 | coordinator-upgrade,deployer-upgrade,package-registration |
| dbms/installation/linux/installation-linux-docker-install.md | Docker 설치 | docker-pull,docker-run,container-setup,volume-mount |
| dbms/installation/linux/installation-linux-linux-env.md | Linux 환경 준비 | ulimit,port-reservation,NTP-sync |
| dbms/installation/linux/installation-linux-tgz-install.md | Tarball 설치 | tar-extract,environment-variables,MACHBASE_HOME |
| dbms/installation/windows/installation-windows-msi-install.md | Windows MSI 설치 | installer-wizard,installation-directory,shortcut |
| dbms/installation/windows/installation-windows-windows-env.md | Windows 환경 준비 | firewall-port,port-5656,port-5001,inbound-rules |
| dbms/sdk-integration/sdk-integration-cli-odbc.md | CLI/ODBC | C/C++,ODBC-API,SQLAllocEnv,SQLConnect,prepared-statements |
| dbms/sdk-integration/sdk-integration-cli-odbc-example.md | CLI/ODBC 예제 | ODBC-example,allocation,connection-string |
| dbms/sdk-integration/sdk-integration-dotnet.md | .NET/C# 커넥터 | MachConnection,MachCommand,MachDataReader |
| dbms/sdk-integration/sdk-integration-jdbc.md | JDBC 드라이버 | MachDriver,jdbc-url,connection-properties,ResultSet |
| dbms/sdk-integration/sdk-integration-nodejs.md | Node.js 연동 | npm-package,node-driver,SQL-execution |
| dbms/sdk-integration/sdk-integration-npm.md | NPM 패키지 | @machbase/ts-client,npm-install,module-export |
| dbms/sdk-integration/sdk-integration-python.md | Python SDK | machbaseAPI,pip-install,execute-query |
| dbms/sql-reference/sql-reference-datatypes.md | 데이터 타입 | short,integer,long,double,varchar,datetime,IPv4,IPv6 |
| dbms/sql-reference/sql-reference-ddl.md | DDL 데이터 정의 | CREATE-TABLE,DROP-TABLE,ALTER-TABLE,CREATE-INDEX |
| dbms/sql-reference/sql-reference-dml.md | DML 데이터 조작 | INSERT,UPDATE,DELETE,APPEND |
| dbms/sql-reference/sql-reference-functions.md | SQL 함수 목록 | ABS,AVG,COUNT,SUM,DATE_TRUNC,EXTRACT,TO_CHAR,JSON |
| dbms/sql-reference/sql-reference-select-hint.md | SELECT 힌트 | PARALLEL,FULL,NO_INDEX,ROLLUP_TABLE,SCAN_FORWARD |
| dbms/sql-reference/sql-reference-select.md | SELECT 구문 | FROM,WHERE,GROUP-BY,ORDER-BY,JOIN,UNION,DURATION,PIVOT |
| dbms/sql-reference/sql-reference-sys-session-manage.md | 세션 관리 | ALTER_SYSTEM,KILL_SESSION,SET,query-timeout |
| dbms/sql-reference/sql-reference-time-expressions.md | 상대시간 표현식 | INTERVAL,date-arithmetic,time-function,duration-clause |
| dbms/sql-reference/sql-reference-user-manage.md | 사용자 관리 SQL | CREATE-USER,ALTER-USER,DROP-USER,GRANT,REVOKE |
| dbms/table-types/log-tables/table-types-log-tables-creating-log-tables.md | 로그 테이블 생성 | CREATE-TABLE,_arrival_time,flexible-schema |
| dbms/table-types/log-tables/table-types-log-tables-deleting-data.md | 로그 데이터 삭제 | DELETE-oldest,DELETE-except,time-based-deletion |
| dbms/table-types/log-tables/table-types-log-tables-insert.md | 로그 데이터 입력 방법 | INSERT,APPEND,IMPORT,LOAD,입력방식비교 |
| dbms/table-types/log-tables/table-types-log-tables-insert-append-data.md | APPEND 고속입력 | append_API,batch-insert,high-volume |
| dbms/table-types/log-tables/table-types-log-tables-insert-import-data.md | 로그 데이터 임포트 | machloader,CSV-import,data-validation |
| dbms/table-types/log-tables/table-types-log-tables-insert-insert-data.md | INSERT 단건입력 | INSERT-statement,single-insert |
| dbms/table-types/log-tables/table-types-log-tables-insert-load-data.md | LOAD DATA 벌크로드 | LOAD-data,bulk-operation,auto_headuse,AUTO_CREATE |
| dbms/table-types/log-tables/table-types-log-tables-log-indexes.md | 로그 인덱스 | BITMAP,KEYWORD,LSM,CREATE_INDEX,텍스트검색 |
| dbms/table-types/log-tables/table-types-log-tables-select.md | 로그 데이터 추출 | SEARCH,text-search,aggregation |
| dbms/table-types/log-tables/table-types-log-tables-select-network-type.md | 네트워크 데이터타입 | IPv4,IPv6,network-mask,CIDR |
| dbms/table-types/log-tables/table-types-log-tables-select-select-data.md | 로그 데이터 조회 | WHERE절,조건검색,기본조회 |
| dbms/table-types/log-tables/table-types-log-tables-select-select-time-data.md | 시간 기반 조회 | DURATION,BEFORE,AFTER,시간범위검색 |
| dbms/table-types/log-tables/table-types-log-tables-select-simple-join.md | 테이블 조인 | INNER_JOIN,volatile_table,lookup_table |
| dbms/table-types/log-tables/table-types-log-tables-select-text-search.md | 텍스트 검색 | SEARCH keyword,full-text-search,역색인,REGEXP |
| dbms/table-types/lookup-tables/table-types-lookup-tables-creating-lookup-tables.md | 룩업 테이블 생성 | CREATE-LOOKUP-TABLE,reference-data,persistent |
| dbms/table-types/lookup-tables/table-types-lookup-tables-deleting-data.md | 룩업 데이터 삭제 | DELETE-by-key,TRUNCATE |
| dbms/table-types/lookup-tables/table-types-lookup-tables-inserting-data.md | 룩업 데이터 입력 | INSERT,UPDATE,LOOKUP_APPEND_UPDATE_ON_DUPKEY,TABLE_REFRESH |
| dbms/table-types/lookup-tables/table-types-lookup-tables-lookup-indexes.md | 룩업 인덱스 | red-black-tree,primary-key-index |
| dbms/table-types/lookup-tables/table-types-lookup-tables-querying-data.md | 룩업 데이터 조회 | SELECT,JOIN,reference-data-query |
| dbms/table-types/table-types.md | 테이블 타입 참조 | tag-table,log-table,volatile-table,lookup-table,생성문법 |
| dbms/table-types/tag-tables/table-types-tag-tables-binary-columns.md | 바이너리 컬럼 | BINARY-type,고정길이,16진수입력,센서프레임 |
| dbms/table-types/tag-tables/table-types-tag-tables-creating-tag-tables.md | 태그 테이블 생성 | CREATE-TAG-TABLE,BASETIME,SUMMARIZED,필수컬�� |
| dbms/table-types/tag-tables/table-types-tag-tables-deleting-data.md | 태그 데이터 삭제 | DELETE-oldest,before_time,특정태그삭제 |
| dbms/table-types/tag-tables/table-types-tag-tables-duplication-removal.md | 중복 자동제거 | TAG_DUPLICATE_CHECK_DURATION,센서데이터정제 |
| dbms/table-types/tag-tables/table-types-tag-tables-inserting-data.md | 태그 데이터 입력 | INSERT,METADATA,append,고속입력 |
| dbms/table-types/tag-tables/table-types-tag-tables-lsl-usl-limits.md | LSL/USL 데이터품질 | LSL,USL,specification_limit,범위제한 |
| dbms/table-types/tag-tables/table-types-tag-tables-querying-data.md | 태그 데이터 조회 | 시계열쿼리,시간범위,tag_id검색,고속검색 |
| dbms/table-types/tag-tables/table-types-tag-tables-rollup-conditional.md | 조건부 롤업 | conditional-rollup,outlier_filtering,predicate,노이즈제거 |
| dbms/table-types/tag-tables/table-types-tag-tables-rollup-custom.md | 사용자 정의 롤업 (Custom Rollup) | custom_rollup,user_defined_aggregation,INTO_AS_SELECT,re_aggregation,OHLCV,hierarchical_pipeline,DATE_BIN,FIRST_LAST |
| dbms/table-types/tag-tables/table-types-tag-tables-rollup-tables.md | 롤업 테이블 | rollup-statistics,MIN-MAX-AVG,hourly-rollup,CREATE_ROLLUP |
| dbms/table-types/tag-tables/table-types-tag-tables-tag-indexes.md | 태그 인덱스 | TAG_INDEX,3-level-index,json_path,추가컬럼인덱싱 |
| dbms/table-types/tag-tables/table-types-tag-tables-tag-metadata.md | 태그 메타데이터 | _META-table,metadata-management,센서레지스트리 |
| dbms/table-types/tag-tables/table-types-tag-tables-varchar-storage.md | VARCHAR 저장소 최적화 | VARCHAR_FIXED_LENGTH_MAX,고정영역,가변영역,저장효율 |
| dbms/table-types/volatile-tables/table-types-volatile-tables-creating-volatile-tables.md | 휘발성 테이블 생성 | CREATE-VOLATILE,in-memory,PRIMARY-KEY |
| dbms/table-types/volatile-tables/table-types-volatile-tables-deleting-data.md | 휘발성 데이터 삭제 | DELETE-by-key,WHERE조건 |
| dbms/table-types/volatile-tables/table-types-volatile-tables-insert-update.md | 휘발성 데이터 입력/수정 | INSERT,UPDATE,temporary-data |
| dbms/table-types/volatile-tables/table-types-volatile-tables-querying-data.md | 휘발성 데이터 조회 | real-time,in-memory-query |
| dbms/table-types/volatile-tables/table-types-volatile-tables-volatile-indexes.md | 휘발성 인덱스 | red-black-tree,primary-key-index,유일성 |
| dbms/tools-reference/tools-reference-csv.md | CSV 임포트/내보내기 도구 | csvimport,csvexport,데이터교환 |
| dbms/tools-reference/tools-reference-machadmin.md | machadmin 서버 관리 | startup,shutdown,createdb,recovery_mode |
| dbms/tools-reference/tools-reference-machcoordinatoradmin.md | 코디네이터 관리도구 | Coordinator,cluster_edition,package_관리 |
| dbms/tools-reference/tools-reference-machdeployeradmin.md | 배포자 관리도구 | Deployer,cluster_edition,프로세스관리 |
| dbms/tools-reference/tools-reference-machloader.md | machloader 벌크 로드 | 데이터임포트,스키마파일,bulk_load,datetime |
| dbms/tools-reference/tools-reference-machsql.md | machsql CLI 도구 | interactive_SQL,script,timezone,출력형식 |
| dbms/troubleshooting/troubleshooting-common-issues.md | 일반 문제 해결 | connection-error,memory-error,disk-space,slow-query |
| dbms/troubleshooting/troubleshooting-error-code.md | 오류 코드 목록 | error-code-reference,PIVOT오류,메모리오류 |
| dbms/troubleshooting/troubleshooting-memory-error.md | 메모리 부족 오류 | MAX_QPX_MEM,메모리제한,out-of-memory |
| dbms/troubleshooting/troubleshooting-trace-log.md | 추적 로그 설정 | TRACE_LOG_LEVEL,로그레벨,module_logging,trc파일 |
| dbms/tutorials/tutorials-application-logs.md | 애플리케이션 로그 튜토리얼 | 로그저장,풀텍스트검색,SEARCH,로그관리 |
| dbms/tutorials/tutorials-iot-sensor-data.md | IoT 센서 데이터 튜토리얼 | 창고모니터링,온습도센서,롤업,데이터보유 |
| dbms/tutorials/tutorials-realtime-analytics.md | 실시간 분석 튜토리얼 | factory_monitoring,Volatile_table,상태보드 |
| dbms/tutorials/tutorials-reference-data.md | 참조 데이터 튜토리얼 | IoT_플랫폼,device_registry,Lookup_table,마스터데이터 |
| installation/installation.md | Machbase Neo 설치 및 시작 | Docker,direct install,platform support,web UI,login |
| jsh/javascript-analysis-module.md | JavaScript 통계분석 | sort,cdf,quantile,correlation,covariance,entropy,linearRegression,FFT,spline |
| jsh/javascript-db-module.md | JavaScript DB 클라이언트 | db.Client,connection,query,appender,rows,result |
| jsh/javascript-examples.md | JSH 실행 예제 | HTTP server,routing,daemonize,RESTful |
| jsh/javascript-filter-module.md | JavaScript 필터링 | Kalman,MovAvg,Lowpass,signal processing |
| jsh/javascript-generator-module.md | JavaScript 데이터생성 | arrange,linspace,meshgrid,Simplex noise,UUID |
| jsh/javascript-guide.md | JSH 인터프리터 기본 | daemon,service,JSH modules,background process,SCRIPT |
| jsh/javascript-http-module.md | JSH HTTP 서버/클라이언트 | HTTP server,request,response,route,SSL,middleware |
| jsh/javascript-mat-module.md | JavaScript 행렬 계산 | Dense matrix,QR factorization,transpose,inverse,linear algebra |
| jsh/javascript-mqtt-module.md | JSH MQTT 클라이언트 | mqtt.Client,publish,subscribe,QoS,callback |
| jsh/javascript-opcua-module.md | OPC-UA 클라이언트 | opcua.Client,read,write,nodes,TimestampsToReturn |
| jsh/javascript-process-module.md | 프로세스 관리 | pid,daemonize,schedule,sleep,process list,cleanup |
| jsh/javascript-psutil-module.md | 시스템 정보 조회 | CPU,memory,disk,network,host info,uptime |
| jsh/javascript-spatial-module.md | 공간정보 계산 | haversine distance,coordinate,GPS,geographic |
| jsh/javascript-system-module.md | 시스템 유틸리티 | Log,parseTime,timezone,location,now |
| operations/address-ports.md | 바인드주소 및 포트 | bind address,listening port,shell,mqtt,http,grpc |
| operations/command-line.md | 명령줄 옵션 | machbase-neo serve,flags,--host,--config,session limit |
| operations/metrics.md | 성능 메트릭 수집 | statz,latency percentile,HTTP metrics,MQTT,query time |
| operations/server-config.md | 서버 설정 파일 | machbase-neo.conf,HCL,listeners,logging,preferences |
| operations/service-linux.md | Linux 서비스 관리 | systemd,supervisord,PM2,auto-start,startup script |
| operations/service-windows.md | Windows 서비스 등록 | service install,service remove,Administrator |
| security/security.md | 보안 인증 및 토큰 | key generation,X.509 certificate,HTTP token,MQTT TLS,private key |
| sql/sql-backup-mount.md | 백업 및 마운트 | backup,mount,incremental_backup,restore,time-range |
| sql/sql-duplicate-removal.md | 중복 데이터 자동 제거 | TAG_DUPLICATE_CHECK_DURATION,lookback_window,first-write-wins |
| sql/sql-guide.md | SQL 기본 시작 | DDL,DML,CREATE,INSERT,SELECT,집계함수 |
| sql/sql-outlier-removal.md | 이상치 자동 제거 | outlier,LSL,USL,specification_limits,metadata |
| sql/sql-rollup.md | ROLLUP 사전집계 | rollup,MIN,MAX,AVG,SUM,SUMSQ,time_granularity,ROLLUP_FORCE |
| sql/sql-storage-size.md | 자동 스토리지 관리 | retention_policy,DURATION,INTERVAL,data_lifecycle,automatic_purge |
| sql/sql-tag-statistics.md | 태그 통계 조회 | v$tag_stat,TAG_STAT_ENABLE,per-tag_statistics,SUMMARIZED |
| sql/sql-tag-table.md | 태그 테이블 데이터 모델 | tall/narrow_format,BASETIME,PIVOT,wide_format변환,schema_flexibility |
| tql/tql-analysis-templates.md | TQL 분석 템플릿 모음 | 분석패턴,금융,센서,진동,statistical_analysis |
| tql/tql-chart-validation.md | TQL 차트 검증 | validation,column_reference,NO_DATA,INVALID_COLUMN |
| tql/tql-fft.md | FFT 푸리에 변환 | FFT,frequency_domain,signal_processing,spectrum_analysis |
| tql/tql-filters.md | 신호처리 필터링 | moving_average,low_pass_filter,kalman_filter,noise_removal |
| tql/tql-group.md | GROUP 집계 및 윈도우 | GROUP_BY,aggregator,timewindow,lazy,predict,interpolation |
| tql/tql-guide.md | TQL 핵심 개념 | SRC_MAP_SINK,데이터파이프라인,format_conversion |
| tql/tql-html.md | TQL HTML 생성 | HTML(),Go_template,template_syntax,dynamic_HTML |
| tql/tql-http.md | TQL HTTP 요청 | HTTP(),RFC_2616,external_API,remote_fetch |
| tql/tql-map.md | MAP 변환 함수 | MAPVALUE,PUSHVALUE,POPVALUE,FILTER,DROP,TAKE,FLATTEN |
| tql/tql-reading.md | TQL 읽기 API | CSV output,tql file,curl,data_input |
| tql/tql-reference.md | TQL 문법 레퍼런스 | primitive_types,연산자,param,pragma,nil_coalescing |
| tql/tql-script.md | SCRIPT JavaScript 함수 | $.payload,$.yield,$.db,$.request,ECMAscript,context_object |
| tql/tql-sink.md | SINK 출력 함수 | INSERT(),CHART(),JSON(),CSV(),NDJSON,MARKDOWN |
| tql/tql-src.md | SRC 데이터소스 함수 | SQL(),FAKE(),CSV(),BYTES(),SQL_SELECT,bridge |
| tql/tql-time-examples.md | 시간 함수 예제 | time(),now,epoch,nanoseconds,timeAdd,parseTime |
| tql/tql-utilities.md | 유틸리티 함수 | 문자열함수,시간함수,수학함수,random,list,dict |
| tql/tql-writing.md | TQL 쓰기 API | INSERT CSV,HTTP POST,data_ingestion,append_operation |
| tql/chart/3d-bar-chart.md | 3D 막대 그래프 | CHART_3D_BAR,bar3D,3D_coordinate |
| tql/chart/3d-globe-chart.md | 3D 글로브 지도 | CHART_3D_GLOBE,world_map,coordinates,geo_spatial |
| tql/chart/3d-line-chart.md | 3D 선형 그래프 | CHART_3D_LINE,grid3D,EGL_rendering |
| tql/chart/bar-chart.md | 막대 그래프 | CHART_BAR,category,polar_bar,stacked_bar |
| tql/chart/boxplot-chart.md | 박스플롯 | CHART_BOXPLOT,quartile,box_and_whisker,outlier_detection |
| tql/chart/candlestick-chart.md | 캔들스틱 금융 차트 | CHART_CANDLESTICK,OHLC,open_high_low_close,stock_data |
| tql/chart/chart-html-embedding.md | 차트 HTML 임베딩 | script_tag,echarts_library,standalone_chart |
| tql/chart/gauge-chart.md | 게이지 차트 | CHART_GAUGE,pointer,progress,threshold |
| tql/chart/geojson-chart.md | GeoJSON 지도 차트 | CHART_GEOJSON,map_data,geographic_regions,boundary |
| tql/chart/heatmap-chart.md | 히트맵 | CHART_HEATMAP,grid_color,visualMap,density |
| tql/chart/line-chart.md | 라인 차트 | CHART_LINE,area_style,smooth_curve,multiple_y_axis |
| tql/chart/liquidfill-chart.md | 액체 충전 차트 | CHART_LIQUIDFILL,percentage,wave_animation |
| tql/chart/others-chart.md | 기타 차트 유형 | CHART_OTHER,custom_chart,composition |
| tql/chart/pie-chart.md | 파이/도넛 차트 | CHART_PIE,doughnut,rose_chart,roseType,proportion |
| tql/chart/radar-chart.md | 레이더 차트 | CHART_RADAR,polar_coordinate,multi_axis,area_fill |
| tql/chart/scatter-chart.md | 산점도 | CHART_SCATTER,coordinate_pairs,large_dataset,million_points |
| tql/geomap/geomap-html-embedding.md | GeoMap HTML 임베딩 | GeoMap_embed,web_integration,WGS84 |
| tql/geomap/geomap_guide.md | GEOMAP 지도 함수 | GEOMAP(),tile_server,coordinates,markers,shapes |
| utilities/dashboard.md | 대시보드 UI | chart panel,time range,auto-refresh,TQL chart,overlay |
| utilities/import-export.md | 데이터 임포트/익스포트 | CSV,gzip,--input,--timeformat,--compress,pipe |
| utilities/shell/shell-access.md | SSH 셸 원격 접속 | SSH key,public key auth,fingerprint,remote command |
| utilities/shell/shell-custom.md | 커스텀 셸 등록 | bash,zsh,cmd.exe,REPL,theme,executable_path |
| utilities/shell/shell-run.md | 셸 스크립트 실행 | batch.sh,run command,shebang,semicolon |
| utilities/tag-analyzer.md | 태그 분석기 도구 | rollup table,FFT chart,stat query,RAW data,slider |
| utilities/timeformat-tz.md | 시간 포맷 및 타임존 | RFC3339,Unix epoch,custom format,IANA timezone |
| utilities/timer.md | 타이머 스케줄링 | CRON expression,@every,@daily,@hourly,auto-start |
| utilities/timer-templates.md | 타이머 TQL 스크립트 패턴 | CSV pattern,FAKE source,SQL pattern,MAPVALUE,배치 INSERT |
| report/general-report-templates.md | 범용 분석 리포트 템플릿 | HTML_report,시계열통계,태그별통계,AI분석,LLM생성 |
| report/finance-report-templates.md | 금융 분석 리포트 템플릿 | OHLCV,캔들스틱,볼린저밴드,이동평균,거래량,주가환율 |
| report/vibration-report-templates.md | 진동 분석 리포트 템플릿 | RMS,FFT,ISO_10816,Crest_Factor,가속도파형,진동분석 |
| report/driving-report-templates.md | 운전행동 분석 리포트 템플릿 | IMU,안전점수,급가속급제동,자이로,Class분포,운전행동 |
| sdk-go/machcli.md | Go CGo 네이티브 클라이언트 | machcli,CGo,C-library-wrapper,native-port-5656,NewDatabase,MaxOpenConn |
| sdk-go/machrpc.md | Go gRPC 클라이언트 패키지 | machrpc,gRPC-client,TLS-certificate,client-cert,Appender,BulkInsert |
| sdk-go/machgo.md | Go Pure 네이티브 클라이언트 | machgo,pure-Go,no-CGo,neo-client,native-port-5656,cross-platform |
| sdk-go/sqldriver.md | Go 표준 sql 패키지 드라이버 | machbase-driver,go-database/sql,neo-client,DSN,sql.Open,native-TCP-5656 |
