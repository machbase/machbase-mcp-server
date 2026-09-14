# 오류 코드 사전

Machbase 오류는 machsql, 드라이버 예외 메시지와 서버 trace 로그에 표시됩니다. 이 페이지는
Machbase 8.7.0의 대표 오류와 전체 오류 메시지 목록을 제공합니다.

오류 메시지는 실행 경로에 따라 `ERR-02010: ...` 형식의 문자열 또는 드라이버별 예외로
노출됩니다. 메시지 문구는 제품 개선 과정에서 바뀔 수 있으므로 애플리케이션에서는 문자열이
아니라 오류 코드를 기준으로 처리합니다.

## SQL 파서와 함수 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-02009` | `Insufficient parser memory.` | SQL 파서 메모리 부족 |
| `ERR-02010` | `Syntax error: near token (%s).` | SQL 문법 오류 |
| `ERR-02011` | `Unrecognized token (%s).` | 인식할 수 없는 토큰 사용 |
| `ERR-02034` | `Invalid format of time expression.` | 시간 표현식 형식 오류 |
| `ERR-02035` | `Function [%s] does not exist.` | 존재하지 않는 함수 호출 |
| `ERR-02036` | `Function [%s] has an invalid argument.` | 함수 인자 개수 또는 값 오류 |
| `ERR-02037` | `Function [%s] argument data type does not match.` | 함수 인자 타입 불일치 |
| `ERR-02040` | `Invalid time range.` | 허용되지 않는 시간 범위 |

## 테이블, 컬럼, 입력 데이터 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-02014` | `Column name is duplicated: (%s).` | 중복 컬럼명 사용 |
| `ERR-02015` | `Invalid column type: (%s).` | 지원하지 않는 컬럼 타입 지정 |
| `ERR-02024` | `Table %s already exists.` | 같은 이름의 테이블이 이미 존재 |
| `ERR-02025` | `Table %s does not exist.` | 대상 테이블이 존재하지 않음 |
| `ERR-02026` | `The number of insert values and that of columns are mismatched.` | INSERT 컬럼 수와 값 수 불일치 |
| `ERR-02030` | `Column name (%s) does not exist.` | 존재하지 않는 컬럼 지정 |

## 시스템 리소스 오류

| 코드 | 메시지 | 대표 원인 |
|------|--------|-----------|
| `ERR-01007` | `There is no available disk space for writing <%lld>bytes to the file<%s>, errno = %d.` | 데이터 파일을 기록할 디스크 공간 부족 |
| `ERR-01346` | `Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu), increase PROCESS_MAX_SIZE property and restart.` | `PROCESS_MAX_SIZE` 한도 초과 |

## 전체 목록 사용 방법

아래 전체 목록은 제품 오류 카탈로그의 영문 메시지를 표시합니다. `KEY`는 소스 코드에서
오류를 구분하는 식별자이며, `%s`, `%d`, `%llu` 같은 자리표시자는 오류가 발생할 때
객체 이름이나 숫자 등 실제 값으로 바뀝니다. 메시지를 대조할 때는 자리표시자의 차이를
고려하고, 가능한 경우 `ERR-xxxxx` 코드를 기준으로 검색하십시오.

목록은 같은 페이지에서 1,000번 단위 범위로 나뉩니다. 브라우저 찾기 기능으로 오류 코드,
오류 식별자 또는 메시지 일부를 검색할 수 있습니다. 메시지만으로 원인이나 재시도 가능
여부를 판단하기 어려우면 문제 해결과 해당 기능 문서의 제약을
함께 확인하십시오.

<!-- BEGIN GENERATED NFX ERROR CATALOG -->

## 전체 오류 메시지

다음 1,062개 항목은 Machbase 8.7.0 NFX 오류 카탈로그에서 제거된 기능의 항목을 제외한 결과입니다.

### `ERR-00000`–`ERR-00999` (157)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-00001</code> | <code>ERR_FILE_CREATE</code> | <code>Failed to create file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00002</code> | <code>ERR_FILE_TRUNCATE</code> | <code>Failed to truncate file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00003</code> | <code>ERR_FILE_DUP</code> | <code>Failed to duplicate file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00004</code> | <code>ERR_FILE_COPY</code> | <code>Failed to copy file&lt;%s&gt; to file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00005</code> | <code>ERR_FILE_RENAME</code> | <code>Failed to rename file&lt;%s&gt; to file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00006</code> | <code>ERR_FILE_REMOVE</code> | <code>Failed to remove file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00007</code> | <code>ERR_FILE_GETKEY</code> | <code>Failed to get key file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00008</code> | <code>ERR_FILE_PIPE</code> | <code>Failed to create pipe&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00009</code> | <code>ERR_FILE_STAT</code> | <code>Failed to stat file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00010</code> | <code>ERR_FILE_OPEN</code> | <code>Failed to open file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00011</code> | <code>ERR_FILE_CLOSE</code> | <code>Failed to close file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00012</code> | <code>ERR_FILE_SEEK</code> | <code>Failed to seek file&lt;%s&gt;, offset:%lld, Whence:%d, errno = %d.</code> |
| <code>ERR-00013</code> | <code>ERR_FILE_READ</code> | <code>Failed to read file&lt;%s&gt;, size:%llu, errno = %d.</code> |
| <code>ERR-00014</code> | <code>ERR_FILE_WRITE</code> | <code>Failed to write file&lt;%s&gt;, size:%llu, errno = %d.</code> |
| <code>ERR-00015</code> | <code>ERR_FILE_READ_SIZE</code> | <code>Failed to read file&lt;%s&gt; (offset:%llu, req size:%llu, read size: %llu), errno = %d.</code> |
| <code>ERR-00016</code> | <code>ERR_FILE_WRITE_SIZE</code> | <code>Failed to write file&lt;%s&gt; (offset:%llu, req size:%llu, read size: %llu), errno = %d.</code> |
| <code>ERR-00017</code> | <code>ERR_FILE_SYNC</code> | <code>Failed to sync file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00018</code> | <code>ERR_FILE_LOCK</code> | <code>Failed to lock file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00019</code> | <code>ERR_FILE_TRYLOCK</code> | <code>Failed to trylock file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00020</code> | <code>ERR_FILE_UNLOCK</code> | <code>Failed to unlock file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00021</code> | <code>ERR_FILE_NO_EXTENSION</code> | <code>There is no file extension.</code> |
| <code>ERR-00022</code> | <code>ERR_FILE_RENAME_RETRY</code> | <code>Failed to rename file&lt;%s&gt; to file&lt;%s&gt;, retry count&lt;%d&gt;, msec&lt;%d&gt;, errno = %d.</code> |
| <code>ERR-00031</code> | <code>ERR_STRING_SNPRINTF</code> | <code>Error occurred during snprintf: buffer size&lt;%d&gt;, errno = %d.</code> |
| <code>ERR-00061</code> | <code>ERR_ENV_GET</code> | <code>Failed to getenv variable&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00062</code> | <code>ERR_ENV_SET</code> | <code>Failed to setenv variable&lt;%s&gt; to value&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00067</code> | <code>ERR_DIR_OPEN</code> | <code>Failed to opendir &lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00068</code> | <code>ERR_DIR_CLOSE</code> | <code>Failed to closedir, errno = %d.</code> |
| <code>ERR-00069</code> | <code>ERR_DIR_READ</code> | <code>Failed to readdir, errno = %d.</code> |
| <code>ERR-00070</code> | <code>ERR_DIR_REWIND</code> | <code>Failed to rewinddir, errno = %d.</code> |
| <code>ERR-00071</code> | <code>ERR_DIR_MAKE</code> | <code>Failed to makedir &lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00072</code> | <code>ERR_DIR_REMOVE</code> | <code>Failed to removedir, errno = %d.</code> |
| <code>ERR-00073</code> | <code>ERR_DIR_SETCWD</code> | <code>Failed to setcwd, errno = %d.</code> |
| <code>ERR-00074</code> | <code>ERR_DIR_GETCWD</code> | <code>Failed to getcwd, errno = %d.</code> |
| <code>ERR-00075</code> | <code>ERR_DIR_GETHOME</code> | <code>Failed to gethome, errno = %d.</code> |
| <code>ERR-00076</code> | <code>ERR_DIR_PATH_TOO_LONG1</code> | <code>Path&lt;%s&gt; is too long, errno = %d.</code> |
| <code>ERR-00077</code> | <code>ERR_DIR_PATH_TOO_LONG2</code> | <code>Path&lt;%s/%s&gt; is too long, errno = %d.</code> |
| <code>ERR-00078</code> | <code>ERR_DIR_PATH_TOO_LONG3</code> | <code>Path&lt;%s/%s/%s&gt; is too long, errno = %d.</code> |
| <code>ERR-00079</code> | <code>ERR_DIR_NOT_EXIST</code> | <code>The directory does not exist in this path&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-00080</code> | <code>ERR_DIR_REMOVE_WITH_INFO</code> | <code>Failed to call removedir (%s), errno = %d.</code> |
| <code>ERR-00091</code> | <code>ULL_ERR_PMD_SQLITE3_ERROR</code> | <code>%1$s failed: &#91;%2$d: %3$s&#93;.</code> |
| <code>ERR-00092</code> | <code>ULL_ERR_PMD_SQLITE3_DISK_FULL</code> | <code>%1$s failed because the metadata store is full: &#91;%2$d: %3$s&#93;.</code> |
| <code>ERR-00121</code> | <code>ERR_STACK_CREATE</code> | <code>Stack create failed, errno = %d.</code> |
| <code>ERR-00122</code> | <code>ERR_STACK_PUSH</code> | <code>Stack push failed, errno = %d.</code> |
| <code>ERR-00123</code> | <code>ERR_STACK_POP</code> | <code>Stack pop failed, errno = %d.</code> |
| <code>ERR-00131</code> | <code>ERR_MEMORY_ALLOC</code> | <code>Failed to allocate memory(%lu bytes), errno = %d.</code> |
| <code>ERR-00132</code> | <code>ERR_MEMORY_ALLOC_BOUND</code> | <code>Memory allocation error (alloc&#x27;d: %llu, max: %llu).</code> |
| <code>ERR-00133</code> | <code>ERR_PM_PROCESS_MEMORY_LIMIT</code> | <code>Failed to allocate memory (ID = %d) (Request Size = %llu) : (Current Allocated Size / PROCESS_MAX_SIZE (%llu/%llu)).</code> |
| <code>ERR-00141</code> | <code>ERR_MEMPOOL_CREATE</code> | <code>Failed to create memory pool, errno = %d.</code> |
| <code>ERR-00142</code> | <code>ERR_MEMPOOL_ALLOC</code> | <code>Failed to allocate memory from memory pool, errno = %d.</code> |
| <code>ERR-00151</code> | <code>ERR_MUTEX_CREATE</code> | <code>Failed to create mutex, errno = %d.</code> |
| <code>ERR-00152</code> | <code>ERR_MUTEX_DESTROY</code> | <code>Failed to destroy mutex, errno = %d.</code> |
| <code>ERR-00153</code> | <code>ERR_MUTEX_LOCK</code> | <code>Failed to lock mutex, errno = %d.</code> |
| <code>ERR-00154</code> | <code>ERR_MUTEX_TRYLOCK</code> | <code>Failed to trylock mutex, errno = %d.</code> |
| <code>ERR-00155</code> | <code>ERR_MUTEX_UNLOCK</code> | <code>Failed to unlock mutex, errno = %d.</code> |
| <code>ERR-00161</code> | <code>ERR_QUEUE_CREATE</code> | <code>Failed to create queue, errno = %d.</code> |
| <code>ERR-00162</code> | <code>ERR_QUEUE_DESTROY</code> | <code>Failed to destroy queue, errno = %d.</code> |
| <code>ERR-00163</code> | <code>ERR_QUEUE_ENQUEUE</code> | <code>Failed to enqueue queue, errno = %d.</code> |
| <code>ERR-00164</code> | <code>ERR_QUEUE_DEQUEUE</code> | <code>Failed to dequeue queue, errno = %d.</code> |
| <code>ERR-00171</code> | <code>ERR_THR_ATTR_CREATE</code> | <code>Failed to create thread_attr, errno = %d.</code> |
| <code>ERR-00172</code> | <code>ERR_THR_ATTR_DESTROY</code> | <code>Failed to destroy thread_attr, errno = %d.</code> |
| <code>ERR-00173</code> | <code>ERR_THR_ATTR_SET_BOUND</code> | <code>Failed to set thread_attr bound, errno = %d.</code> |
| <code>ERR-00174</code> | <code>ERR_THR_ATTR_SET_DETACH</code> | <code>Failed to set thread_attr detach, errno = %d.</code> |
| <code>ERR-00175</code> | <code>ERR_THR_ATTR_SET_STACK_SIZE</code> | <code>Failed to set thread_attr stack size, errno = %d.</code> |
| <code>ERR-00176</code> | <code>ERR_THR_CREATE</code> | <code>Failed to create thread, errno = %d.</code> |
| <code>ERR-00177</code> | <code>ERR_THR_DETACH</code> | <code>Failed to detach thread, errno = %d.</code> |
| <code>ERR-00178</code> | <code>ERR_THR_JOIN</code> | <code>Failed to join thread, errno = %d.</code> |
| <code>ERR-00179</code> | <code>ERR_THR_GETID</code> | <code>Failed to get id of thread, errno = %d.</code> |
| <code>ERR-00191</code> | <code>ERR_THR_CV_CREATE</code> | <code>Failed to create thread condition variable, errno = %d.</code> |
| <code>ERR-00192</code> | <code>ERR_THR_CV_DESTROY</code> | <code>Failed to destroy thread condition variable, errno = %d.</code> |
| <code>ERR-00193</code> | <code>ERR_THR_CV_TIMEDWAIT</code> | <code>Failed to call cond_timedwait, errno = %d.</code> |
| <code>ERR-00194</code> | <code>ERR_THR_CV_SIGNAL</code> | <code>Failed to call cond_signal, errno = %d.</code> |
| <code>ERR-00195</code> | <code>ERR_THR_CV_BROADCAST</code> | <code>Failed to call cond_broadcast, errno = %d.</code> |
| <code>ERR-00196</code> | <code>ERR_THR_CV_WAIT</code> | <code>Failed to call cond_wait, errno = %d.</code> |
| <code>ERR-00201</code> | <code>ERR_RWMUTEX_CREATE</code> | <code>Failed to create rwlock, errno = %d.</code> |
| <code>ERR-00202</code> | <code>ERR_RWMUTEX_DESTROY</code> | <code>Failed to destroy rwlock, errno = %d.</code> |
| <code>ERR-00203</code> | <code>ERR_RWMUTEX_LOCK_READ</code> | <code>Failed to call rwlock_lock_read, errno = %d.</code> |
| <code>ERR-00204</code> | <code>ERR_RWMUTEX_TRYLOCK_READ</code> | <code>Failed to call rwlock_trylock_read, errno = %d.</code> |
| <code>ERR-00205</code> | <code>ERR_RWMUTEX_LOCK_WRITE</code> | <code>Failed to call rwlock_lock_write, errno = %d.</code> |
| <code>ERR-00206</code> | <code>ERR_RWMUTEX_TRYLOCK_WRITE</code> | <code>Failed to call rwlock_trylock_write, errno = %d.</code> |
| <code>ERR-00211</code> | <code>ERR_RBTREE_TOO_SMALL_BUFFER</code> | <code>RBTREE buffer&lt;%d&gt; is too small for value&lt;%d&gt;, errno = %d.</code> |
| <code>ERR-00212</code> | <code>ERR_RBTREE_CURSOR_OP_NOT_APPLICABLE</code> | <code>RBTREE cursor op not applicable. errno = %d.</code> |
| <code>ERR-00213</code> | <code>ERR_RBTREE_ALREADY_FREE_NODE</code> | <code>RBTREE node is already freed, errno = %d.</code> |
| <code>ERR-00216</code> | <code>ERR_TREEMAP_KEY_EXISTS</code> | <code>Key already exists.</code> |
| <code>ERR-00221</code> | <code>ERR_LZO_COMPRESS</code> | <code>LZO compress failed, errno = %d.</code> |
| <code>ERR-00222</code> | <code>ERR_LZO_DECOMPRESS</code> | <code>LZO decompress failed, errno = %d.</code> |
| <code>ERR-00231</code> | <code>ERR_GET_CPU_COUNT</code> | <code>Failed to get CPU count, errno = %d.</code> |
| <code>ERR-00232</code> | <code>ERR_CONF_NO_FILE</code> | <code>Configuration file does not exist(%S).</code> |
| <code>ERR-00251</code> | <code>ERR_TLSF_MEL_INITIALIZE</code> | <code>Tlsf memory manager initialization failed, errno = %d.</code> |
| <code>ERR-00252</code> | <code>ERR_TLSF_MEL_FINALIZE</code> | <code>Tlsf memory manager finalization failed, errno = %d.</code> |
| <code>ERR-00253</code> | <code>ERR_TLSF_MEL_ALLOC</code> | <code>Tlsf memory manager allocation(%lld) failed, errno = %d.</code> |
| <code>ERR-00254</code> | <code>ERR_TLSF_MEL_FREE</code> | <code>Tlsf memory manager free failed, errno = %d.</code> |
| <code>ERR-00255</code> | <code>ERR_TLSF_MEL_CONTROL</code> | <code>Tlsf memory manager control failed, errno = %d.</code> |
| <code>ERR-00256</code> | <code>ERR_TLSF_MEL_SHRINK</code> | <code>Tlsf memory manager shrink failed, errno = %d.</code> |
| <code>ERR-00257</code> | <code>ERR_TLSF_MEL_GETSTATISTICS</code> | <code>Tlsf memory manager getstatistics failed, errno = %d.</code> |
| <code>ERR-00271</code> | <code>ERR_SESSION_CLOSED</code> | <code>The session is closed.</code> |
| <code>ERR-00272</code> | <code>ERR_SESSION_CANCELED</code> | <code>The session is canceled.</code> |
| <code>ERR-00291</code> | <code>ERR_LICENSE_INVALID</code> | <code>The license is invalid or expired.</code> |
| <code>ERR-00292</code> | <code>ERR_LICENSE_NOTEXIST_VALUE</code> | <code>The value&lt;%s&gt; does not exist in the license file.</code> |
| <code>ERR-00293</code> | <code>ERR_LICENSE_GET_HARDWARE_KEY</code> | <code>Failed to get hardware key, errno =%d</code> |
| <code>ERR-00294</code> | <code>ERR_LICENSE_VERIFY</code> | <code>Failed to verify the license, errno = %d</code> |
| <code>ERR-00300</code> | <code>ERR_INVALID_DATE_VALUE</code> | <code>Invalid date value.(%s)</code> |
| <code>ERR-00301</code> | <code>ERR_INVALID_NETWORK_TYPE</code> | <code>Invalid network string.(%s)</code> |
| <code>ERR-00321</code> | <code>ERR_SHA_SHA1_INIT_ERROR</code> | <code>Error in initializing sha1, errno = %d</code> |
| <code>ERR-00322</code> | <code>ERR_SHA_SHA1_UPDATE_ERROR</code> | <code>Error in updating sha1, errno = %d</code> |
| <code>ERR-00323</code> | <code>ERR_SHA_SHA1_FINAL_ERROR</code> | <code>Error in finalizing sha1, errno = %d</code> |
| <code>ERR-00324</code> | <code>ERR_SHA_INVALID_TYPE_ERROR</code> | <code>Invalid SHA type.(%d)</code> |
| <code>ERR-00325</code> | <code>ERR_SHA_INVALID_HEX_STRING</code> | <code>Invalid SHA hex string.(%s)</code> |
| <code>ERR-00341</code> | <code>ERR_PARALLEL_JOB_MANAGER_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Parallel job thread abnormally terminated</code> |
| <code>ERR-00342</code> | <code>ERR_PARALLEL_JOB_MANAGER_INVALID_THREAD_COUNT</code> | <code>The thread count should be between %d and %d</code> |
| <code>ERR-00361</code> | <code>ERR_RESFILE_BUFFER_SET_LOG_ERROR</code> | <code>Error in setting a log to the buffer of the result file: %s, errno = %d</code> |
| <code>ERR-00381</code> | <code>ERR_PCRE_COMPILE_ERROR</code> | <code>Regular expression error: an error occurred at offset %d of (%s).</code> |
| <code>ERR-00400</code> | <code>ERR_VERSION_NO_META</code> | <code>This DB file is older than binary (no meta-version table). Check database image and binary.</code> |
| <code>ERR-00401</code> | <code>ERR_VERSION_MISMATCH</code> | <code>Version mismatched. In Executable DB(%d.%d) META(%d.%d) CM(%d.%d) But, In File DB(%d.%d) META(%d.%d) CM(%d.%d)</code> |
| <code>ERR-00402</code> | <code>ERR_META_VERSION_TOO_HIGH</code> | <code>Incompatible meta version. File Meta Version(%d.%d) is higher than Executable Version(%d.%d)</code> |
| <code>ERR-00420</code> | <code>ERR_GET_SYS_INFO</code> | <code>Error in getting system information by the sysinfo, errno = %d</code> |
| <code>ERR-00421</code> | <code>ERR_GET_STACK_SIZE</code> | <code>Error in getting stack information by the pmuSysSetStackSize, errno = %d</code> |
| <code>ERR-00422</code> | <code>ERR_SET_STACK_SIZE</code> | <code>Error in setting stack information by the pmuSysSetStackSize, errno = %d</code> |
| <code>ERR-00431</code> | <code>ERR_MEM_MMAP</code> | <code>mmap (size&lt;%u&gt;) error, errno = %d</code> |
| <code>ERR-00432</code> | <code>ERR_MEM_UNMMAP</code> | <code>unmap (address&lt;%p&gt;, size&lt;%u&gt;) error, errno = %d</code> |
| <code>ERR-00451</code> | <code>ERR_CPU_AFFINITY_SET</code> | <code>Failed to set the CPU affinity &#91;%u, %u), errno = %d</code> |
| <code>ERR-00452</code> | <code>ERR_CPU_AFFINITY_INVALID_CPUID</code> | <code>The IDs of CPUs should be between &#91;0, %u), but &#91;%u, %u) given.</code> |
| <code>ERR-00453</code> | <code>ERR_CPU_AFFINITY_INVALID_CPURANGE</code> | <code>Maximum abs value of CPU_AFFINITY_COUNT(%d) should be less than CPU count(%u).</code> |
| <code>ERR-00461</code> | <code>ERR_SYSCONF_CPUCNT</code> | <code>Failed to get the number of CPUs in sysconf, errno = %d</code> |
| <code>ERR-00471</code> | <code>ERR_PM_HEAP_INIT</code> | <code>Failed to initialize a heap.</code> |
| <code>ERR-00472</code> | <code>ERR_PM_HEAP_PUSH</code> | <code>Heap push failed, errno = %d</code> |
| <code>ERR-00481</code> | <code>ERR_PM_AUTH_NONCE_GENERATE</code> | <code>Failed to generate auth nonce.</code> |
| <code>ERR-00482</code> | <code>ERR_PM_AUTH_SIGN</code> | <code>Failed to sign auth challenge.</code> |
| <code>ERR-00483</code> | <code>ERR_PM_AUTH_VERIFY</code> | <code>Failed to verify auth signature.</code> |
| <code>ERR-00484</code> | <code>ERR_PM_AUTH_INVALID_KEY</code> | <code>Invalid auth key.</code> |
| <code>ERR-00485</code> | <code>ERR_PM_AUTH_INVALID_SIG_SCHEME</code> | <code>Invalid auth signature scheme.</code> |
| <code>ERR-00486</code> | <code>ERR_PM_AUTH_INVALID_SIGNATURE</code> | <code>Invalid auth signature.</code> |
| <code>ERR-00487</code> | <code>ERR_PM_AUTH_INVALID_NONCE</code> | <code>Invalid auth nonce.</code> |
| <code>ERR-00488</code> | <code>ERR_PM_AUTH_KEY_FILE_TOO_LARGE</code> | <code>Auth key file is too large. path=&#91;%s&#93;, size=&#91;%llu&#93;, limit=&#91;%llu&#93;</code> |
| <code>ERR-00491</code> | <code>ERR_JSON_DUMP</code> | <code>Error in json dump.</code> |
| <code>ERR-00492</code> | <code>ERR_JSON_LOAD</code> | <code>Error in json load.</code> |
| <code>ERR-00493</code> | <code>ERR_JSON_OBJ</code> | <code>json object error: %s</code> |
| <code>ERR-00494</code> | <code>ERR_JSON_ARR</code> | <code>Error in json-array.</code> |
| <code>ERR-00495</code> | <code>ERR_JSON_STR</code> | <code>Error in json-string (%s).</code> |
| <code>ERR-00496</code> | <code>ERR_JSON_INT</code> | <code>Error in json-integer (%lld).</code> |
| <code>ERR-00497</code> | <code>ERR_JSON_REAL</code> | <code>Error in json-real (%lf).</code> |
| <code>ERR-00498</code> | <code>ERR_JSON_COPY</code> | <code>Error in json copy.</code> |
| <code>ERR-00499</code> | <code>ERR_JSON_PACK</code> | <code>Error in json pack.</code> |
| <code>ERR-00500</code> | <code>ERR_JSON_UPACK</code> | <code>Error in json unpack.</code> |
| <code>ERR-00501</code> | <code>ERR_JSON_EXTR_PATH</code> | <code>No data matches for the json path (%s)</code> |
| <code>ERR-00502</code> | <code>ERR_JSON_PATH_LEN</code> | <code>Json path is too long.</code> |
| <code>ERR-00503</code> | <code>ERR_JSON_OBJECT_VALUE_SET</code> | <code>Error json object set (%s).</code> |
| <code>ERR-00504</code> | <code>ERR_JSON_OBJECT_ARRAY_APPEND</code> | <code>Error json array append.</code> |
| <code>ERR-00505</code> | <code>ERR_JSON_ENCODE</code> | <code>Error encode base64.</code> |
| <code>ERR-00506</code> | <code>ERR_JSON_DECODE</code> | <code>Error decode base64.</code> |
| <code>ERR-00507</code> | <code>ERR_JSON_OBJECT_VALUE_DEL</code> | <code>Error json object del (%s).</code> |
| <code>ERR-00600</code> | <code>ERR_INVALID_PROPERTY_VALUE</code> | <code>Invalid property value: %s.</code> |
| <code>ERR-00601</code> | <code>ERR_PM_CONVERSION_UTF8</code> | <code>Failed to convert %s to UTF8. (%s, errno=%d)</code> |
| <code>ERR-00602</code> | <code>ERR_PM_CONVERTSION_STRING_LENGTH</code> | <code>Buffer size is not enough for code conversion. (%d &gt; %d)</code> |
| <code>ERR-00611</code> | <code>ERR_INVALID_PROPERTY_EXPRESSION</code> | <code>Invalid property expression for %s: %s.</code> |
| <code>ERR-00701</code> | <code>ERR_PM_GEOHASH_INVALID_PRECISION</code> | <code>Geohash invalid precision (%u)</code> |
| <code>ERR-00702</code> | <code>ERR_PM_GEOHASH_INVALID_LENGTH</code> | <code>Geohash invalid length</code> |
| <code>ERR-00703</code> | <code>ERR_PM_GEOHASH_INVALID_DIRECTION</code> | <code>Geohash invalid direction</code> |

### `ERR-01000`–`ERR-01999` (191)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-01000</code> | <code>ERR_SM_INVALID_DISK_FILE</code> | <code>File&lt;%s&gt; is invalid.</code> |
| <code>ERR-01001</code> | <code>ERR_SM_INVALID_OBJ_STORAGE_ID</code> | <code>Invalid object storage id, errno = %d.</code> |
| <code>ERR-01002</code> | <code>ERR_SM_INVALID_ALREADY_FREE_OBJECT_STORAGE</code> | <code>Object storage&lt;%d&gt; already freed, errno = %d.</code> |
| <code>ERR-01003</code> | <code>ERR_SM_DBS_DIR_ALREADY_EXIST</code> | <code>Group storage dir&lt;%s&gt; already exists, errno = %d.</code> |
| <code>ERR-01004</code> | <code>ERR_SM_DBS_INVALID_OBJECT_FILENAME</code> | <code>Object filename&lt;%s&gt; is invalid, errno = %d.</code> |
| <code>ERR-01005</code> | <code>ERR_SM_DISK_FILE_IN_USE</code> | <code>Disk file&lt;%s&gt; is in use, errno = %d.</code> |
| <code>ERR-01006</code> | <code>ERR_SM_NOT_SUPPORT_FUNCTION</code> | <code>Functionality is not supported yet.</code> |
| <code>ERR-01007</code> | <code>ERR_SM_FILE_NO_AVAILABLE_DISK_SPACE</code> | <code>There is no available disk space for writing &lt;%lld&gt;bytes to the file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-01008</code> | <code>ERR_SM_FILE_DUPLICATE</code> | <code>Error in the duplicating file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-01009</code> | <code>ERR_SM_WRONG_READ_SIZE</code> | <code>Error in the read file size.(&lt;io: %u&gt;, &lt;disk: %u&gt;)</code> |
| <code>ERR-01010</code> | <code>ERR_SM_SPACE_NOT_AVAILABLE_4_APPEND</code> | <code>Used media space is reached to threshold. (%4.1lf%% cap &lt; %4.1lf%% used)</code> |
| <code>ERR-01011</code> | <code>ERR_SM_FILE_WRITE_SIZE_MISMATCH</code> | <code>Error in the write file size.(&lt;write: %u&gt;, &lt;written: %u&gt;)</code> |
| <code>ERR-01031</code> | <code>ERR_SM_DB_ALREADY_MOUNTED</code> | <code>The database in &lt;%s&gt; has already been mounted.</code> |
| <code>ERR-01032</code> | <code>ERR_SM_DB_NOT_MOUNTED</code> | <code>The database in &lt;%s&gt; is not mounted.</code> |
| <code>ERR-01033</code> | <code>ERR_SM_DB_MOUNTING</code> | <code>The mount operation of database in &lt;%s&gt; is not completed.</code> |
| <code>ERR-01034</code> | <code>ERR_SM_DB_MOUNT_BUSY</code> | <code>The mounted database&lt;%s&gt; is busy.</code> |
| <code>ERR-01035</code> | <code>ERR_SM_DB_ALREADY_EXIST</code> | <code>The database creation is not complete. Destroy it and create a new one.</code> |
| <code>ERR-01036</code> | <code>ERR_SM_DB_CREATE_NOT_COMPLETE</code> | <code>The database creation is not complete. Destroy it and create a new one.</code> |
| <code>ERR-01037</code> | <code>ERR_SM_DB_MOUNT_INVALIDE_BASEDB</code> | <code>The mount database&lt;%s&gt; is not backed up from the primary database</code> |
| <code>ERR-01038</code> | <code>ERR_SM_DB_COULD_NOT_FIND_MOUNTDB</code> | <code>Cannot find MountDB with &lt;TBSID: %lld&gt;.</code> |
| <code>ERR-01039</code> | <code>ERR_SM_DB_STATE_OF_MOUNTDB_IS_ABNORMAL</code> | <code>Mount DB&lt;%s&gt;&#x27;s state is invalid.</code> |
| <code>ERR-01101</code> | <code>ERR_SM_COLUMN_PARTITION_CACHE_READ_BLOCK</code> | <code>Error in reading column partition cache block. Reading block of RID&lt;%lld&gt; in the column partition&lt;%lld&gt; failed, errno = %d.</code> |
| <code>ERR-01102</code> | <code>ERR_SM_INVALID_CACHE_OBJECT</code> | <code>Invalid cache object.</code> |
| <code>ERR-01103</code> | <code>ERR_SM_CHECKPOINT_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Error occurred in checkpoint thread. Processing abnormal shutdown.</code> |
| <code>ERR-01104</code> | <code>ERR_SM_CACHE_WAIT_READ_PAGE</code> | <code>Error in waiting to read a page.</code> |
| <code>ERR-01105</code> | <code>ERR_SM_CACHE_PAGE_CLEAR_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Error in clear thread of the page cache.</code> |
| <code>ERR-01106</code> | <code>ERR_SM_CACHE_PAGE_MAX_SET_SMALLER_SIZE</code> | <code>It&lt;%llu&gt; is smaller than the max size value of the page cache currently set&lt;%llu&gt;.</code> |
| <code>ERR-01107</code> | <code>ERR_SM_CACHE_PAGE_MAX_SET_IMPOSSIBLE_SIZE</code> | <code>It&lt;%llu&gt; is impossible to set a value larger than the memory size set in the current process&lt;%llu&gt;.</code> |
| <code>ERR-01108</code> | <code>ERR_SM_CP_INVALID_PAGE_ID</code> | <code>Invalid page id in column partition. Page id&lt;%d&gt; is greater than the page max id&lt;%d&gt;.</code> |
| <code>ERR-01201</code> | <code>ERR_SM_ALREADY_EXIST_TABLE_ID_TABLES</code> | <code>Duplicated table id&lt;%llu&gt; in SYS_STORAGE_TABLES, errno = %d.</code> |
| <code>ERR-01202</code> | <code>ERR_SM_ALREADY_EXIST_TABLE_ID_COLUMNS</code> | <code>Duplicated table id&lt;%llu&gt;, column id&lt;%u&gt; in the SYS_STORAGE_COLUMNS, errno = %d.</code> |
| <code>ERR-01203</code> | <code>ERR_SM_NOT_EXIST_TABLE_ID_IN_TABLES</code> | <code>Table id&lt;%lld&gt; does not exist in SYS_STORAGE_TABLES, errno = %d.</code> |
| <code>ERR-01204</code> | <code>ERR_SM_ALREADY_EXIST_INDEX_ID_INDEXES</code> | <code>Duplicated (table id&lt;%llu&gt;, index id&lt;%llu&gt;) in SYS_STORAGE_INDEXES, errno = %d.</code> |
| <code>ERR-01205</code> | <code>ERR_SM_ALREADY_EXIST_INDEX_ID_COLUMNS</code> | <code>Duplicated (table id&lt;%llu&gt;, index id&lt;%llu&gt;, column id&lt;%u&gt;) in SYS_STORAGE_INDEXES_COLUMNS, errno = %d.</code> |
| <code>ERR-01206</code> | <code>ERR_SM_NOT_EXIST_INDEX_ID_IN_INDEXES</code> | <code>Index ID&lt;%llu&gt; of table ID&lt;%llu&gt; does not exist in SYS_STORAGE_INDEXES, errno = %d.</code> |
| <code>ERR-01207</code> | <code>ERR_SM_INVALID_RECOVERY_MODE_STRING</code> | <code>Available recovery modes: simple, complex, reset</code> |
| <code>ERR-01301</code> | <code>ERR_SM_NOT_EXIST_PARTION_RANGE</code> | <code>Partition range does not exist. Partition id is less than &lt;%lld&gt; in the table(id&lt;%lld&gt;) with partitions between &lt;%lld&gt; and &lt;%lld&gt;.</code> |
| <code>ERR-01302</code> | <code>ERR_SM_NOT_EXIST_RECORD_RANGE</code> | <code>Invalid record range. No such record whose id is less than &lt;%llu&gt; in the table(id&lt;%llu&gt;) with records between &lt;%llu&gt; and &lt;%llu&gt;.</code> |
| <code>ERR-01303</code> | <code>ERR_SM_TOO_MANY_COLUMNS_FOR_TABLE</code> | <code>Maximum number of columns in a table is %d.</code> |
| <code>ERR-01304</code> | <code>ERR_SM_INVALID_COLUMN_ID</code> | <code>Invalid column ID (&lt;%d&gt;).</code> |
| <code>ERR-01305</code> | <code>ERR_SM_TABLE_NOT_EXIST</code> | <code>Invalid table ID (&lt;%llu&gt;).</code> |
| <code>ERR-01306</code> | <code>ERR_SM_TABLE_ALREADY_DROPPED</code> | <code>Table has been dropped.</code> |
| <code>ERR-01307</code> | <code>ERR_SM_TABLE_STRUCTURE_MODIFIED</code> | <code>Table structure was modified.</code> |
| <code>ERR-01308</code> | <code>ERR_SM_TABLE_INVALID_FIXED_COLUMN_SIZE</code> | <code>Invalid fixed column size. Invalid value size(&lt;%u&gt;) for the fixed column.</code> |
| <code>ERR-01309</code> | <code>ERR_SM_TABLE_VAR_COLUMN_SIZE_TOO_BIG</code> | <code>Invalid varying column size. Value size(&lt;%u&gt;) for the variable column is greater than the max size (&lt;%u&gt;).</code> |
| <code>ERR-01310</code> | <code>ERR_SM_TABLE_FLUSH_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Table flush thread terminated abnormally.</code> |
| <code>ERR-01311</code> | <code>ERR_SM_TABLE_COLUMN_PARTITION_PREPARE_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Table column partition prepare thread terminated abnormally.</code> |
| <code>ERR-01312</code> | <code>ERR_SM_TABLE_COLUMN_PARTITION_FILE_READ_HEAD</code> | <code>Failed to read the head of the table column partition file (&lt;%s&gt;).</code> |
| <code>ERR-01313</code> | <code>ERR_SM_TABLE_COLUMN_PARTITION_FILE_READ</code> | <code>Failed to read the table column partition file (&lt;%s&gt;).</code> |
| <code>ERR-01314</code> | <code>ERR_SM_TABLE_INDEX_BUILD_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Index build thread terminated abnormally.</code> |
| <code>ERR-01315</code> | <code>ERR_SM_TABLE_INVALID_TYPE</code> | <code>Invalid table type&lt;%d&gt;.</code> |
| <code>ERR-01316</code> | <code>ERR_SM_TABLE_COLUMN_SIZE_TOO_BIG</code> | <code>Column size&lt;%u&gt; is too big.</code> |
| <code>ERR-01317</code> | <code>ERR_SM_TABLE_COLUMN_INVALID_TIME_VALUE</code> | <code>Value of the time column(&lt;%lld&gt;) is less than the last time value(&lt;%lld&gt;).</code> |
| <code>ERR-01318</code> | <code>ERR_SM_TABLE_COLUMN_INVALID_VARCHAR_SIZE</code> | <code>The size of VARCHAR column must be less than (&lt;%llu&gt;).</code> |
| <code>ERR-01319</code> | <code>ERR_SM_TABLE_COLUMN_INVALID_VALUE_SIZE</code> | <code>The size of column value must be less than (&lt;%u&gt;).</code> |
| <code>ERR-01320</code> | <code>ERR_SM_TABLE_COLUMN_REFERENCED_BY_INDEX</code> | <code>There is an index on the column(&lt;%u&gt;) of the table(&lt;%llu&gt;)</code> |
| <code>ERR-01321</code> | <code>ERR_SM_TABLE_NOT_SUPPORT_FUNCTION</code> | <code>This feature is not supported on this table type.</code> |
| <code>ERR-01322</code> | <code>ERR_SM_TABLE_COLUMN_INVALID_NEWSIZE</code> | <code>The new column size(&lt;%u&gt;) should be greater than the old one(&lt;%u&gt;)</code> |
| <code>ERR-01323</code> | <code>ERR_SM_TABLE_COLUMN_MAX</code> | <code>The table(%llu) reached max column count limit (%u) already.</code> |
| <code>ERR-01324</code> | <code>ERR_SM_TABLE_COLUMN_PARTITION_FILE_ADJUST_END_RID</code> | <code>An error occurred adjusting end rid of the table&lt;%llu&gt; column partition(&lt;%llu&gt;), errno = %d.</code> |
| <code>ERR-01325</code> | <code>ERR_SM_TABLE_COLUMN_TOO_SMALL_END_RID</code> | <code>The end RID&lt;%lld&gt; of the column&lt;%d&gt; is less than the end RID&lt;%llu&gt; of the table&lt;%llu&gt;</code> |
| <code>ERR-01330</code> | <code>ERR_SM_TABLE_COLUMN_NOT_FOUND</code> | <code>The column with ID&lt;%hu&gt; does not exist in the table with ID&lt;%llu&gt;</code> |
| <code>ERR-01331</code> | <code>ERR_SM_TABLE_CHECKPOINT_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Table checkpoint thread terminated abnormally.</code> |
| <code>ERR-01332</code> | <code>ERR_SM_TABLE_NOT_EXIST_PARTION</code> | <code>Partition ID &lt;%llu&gt; of the table(id&lt;%llu&gt;) does not exist between &lt;%llu&gt; and &lt;%llu&gt;.</code> |
| <code>ERR-01333</code> | <code>ERR_SM_TABLE_MOUNT_ALREADY</code> | <code>The table&lt;%llu&gt; in the backup database&lt;%s&gt; has been mounted already.</code> |
| <code>ERR-01334</code> | <code>ERR_SM_TABLE_MOUNT_BUSY_WITH_MOUNTING</code> | <code>The table is busy with mounting.</code> |
| <code>ERR-01335</code> | <code>ERR_SM_TABLE_MOUNT_BUSY_WITH_UNMOUNTING</code> | <code>The mounted table is busy with unmounting.</code> |
| <code>ERR-01336</code> | <code>ERR_SM_TABLE_MOUNT_INVALID_STATE</code> | <code>The mounted table is invalid.</code> |
| <code>ERR-01337</code> | <code>ERR_SM_TABLE_MOUNT_IS_BUSY</code> | <code>The mounted table is busy.</code> |
| <code>ERR-01338</code> | <code>ERR_SM_TABLE_MOUNT_NOT_EXIST</code> | <code>The table is not mounted.</code> |
| <code>ERR-01339</code> | <code>ERR_SM_TABLE_MOUNT_TABLE_NOT_SAME_WITH_TABLE</code> | <code>The table&lt;%llu&gt; of the backup tablespace&lt;%s&gt; is different from the table in main database.</code> |
| <code>ERR-01340</code> | <code>ERR_SM_TABLE_MOUNT_TABLE_DROPPED_IN_MAIN_DATABASE</code> | <code>The table&lt;%llu&gt; of the backup tablespace&lt;%s&gt; is dropped from the main database.</code> |
| <code>ERR-01341</code> | <code>ERR_SM_TABLE_HAS_MOUNTED_TABLE</code> | <code>There is a mounted table in the table&lt;%llu&gt;.</code> |
| <code>ERR-01342</code> | <code>ERR_SM_TABLE_MOUNT_HAS_FUTURE_DATA</code> | <code>The mount table&lt;end_rid:%llu&gt; has more furture data than the base table&lt;end_rid:%llu.</code> |
| <code>ERR-01343</code> | <code>ERR_SM_TABLE_UPDATE_COLUMN_INDEX_CREATED</code> | <code>Cannot update columns with indexes in VOLATILE / LOOKUP table.</code> |
| <code>ERR-01344</code> | <code>ERR_SM_TABLE_VOLITILE_MEMORY_LIMIT</code> | <code>The memory size&lt;%llu bytes&gt; of VOLATILE / LOOKUP tables exceeds &lt;%llu bytes&gt;.</code> |
| <code>ERR-01345</code> | <code>ERR_SM_TABLE_COLUMN_VALUE_NOT_NULL</code> | <code>The value of the column&lt;%u&gt; must not be NULL</code> |
| <code>ERR-01346</code> | <code>ERR_SM_PROCESS_MEMORY_LIMIT</code> | <code>Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu), increase PROCESS_MAX_SIZE property and restart.</code> |
| <code>ERR-01401</code> | <code>ERR_SM_INDEX_INVALID_TYPE</code> | <code>Invalid index type. Index type&lt;%d&gt; does not exist.</code> |
| <code>ERR-01402</code> | <code>ERR_SM_INDEX_NOT_EXIST_IN_TABLE</code> | <code>Index id(&lt;%llu&gt;) does not exist in table id &lt;%llu&gt;.</code> |
| <code>ERR-01403</code> | <code>ERR_SM_INDEX_INVALID_COLUMN_COUNT</code> | <code>Index has invalid column count(&lt;%d&gt;).</code> |
| <code>ERR-01404</code> | <code>ERR_SM_INDEX_INVALID_KEYVALUE_COUNT</code> | <code>Index has invalid key value count(&lt;%d&gt;).</code> |
| <code>ERR-01405</code> | <code>ERR_SM_INDEX_INVALID_KEYVALUE_SIZE</code> | <code>Index has invalid key value size(&lt;%d&gt;).</code> |
| <code>ERR-01406</code> | <code>ERR_SM_INDEX_INVALID_FILE</code> | <code>Index column file(&lt;%s&gt;) is invalid.</code> |
| <code>ERR-01407</code> | <code>ERR_SM_INDEX_COLUMN_PARTITION_FILE_READ_HEAD</code> | <code>Failed to read the head of the index column partition file(&lt;%s&gt;).</code> |
| <code>ERR-01408</code> | <code>ERR_SM_INDEX_COLUMN_PARTITION_FILE_READ</code> | <code>Failed to read the index column partition file(&lt;%s&gt;).</code> |
| <code>ERR-01409</code> | <code>ERR_SM_INDEX_COLUMN_INVALID_COLUMN_TYPE</code> | <code>Type of the column for the index is invalid.</code> |
| <code>ERR-01410</code> | <code>ERR_SM_INDEX_FLUSH_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Index flush thread terminated abnormally.</code> |
| <code>ERR-01411</code> | <code>ERR_SM_INDEX_BUILD_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Index build thread terminated abnormally.</code> |
| <code>ERR-01412</code> | <code>ERR_SM_KDW_INDEX_INVALID_KEY_SIZE</code> | <code>The keyword size&lt;%d&gt; should be less than the max size&lt;%d&gt;.</code> |
| <code>ERR-01413</code> | <code>ERR_SM_INDEX_INVALID_WORDBITCNT</code> | <code>The word bit count(%d) is over than %d in the partition&lt;%lld&gt; of the index &lt;%lld&gt;</code> |
| <code>ERR-01414</code> | <code>ERR_SM_INDEX_INVALID_KEYVALCNT</code> | <code>Invalid key count &lt;%u&gt; is not equal to the count &lt;%u&gt; in partition &lt;%lld&gt; of index &lt;%lld&gt;.</code> |
| <code>ERR-01415</code> | <code>ERR_SM_INDEX_INVALID_LEVEL</code> | <code>The level&lt;%u&gt; of the index is bigger than the max level&lt;%u&gt;</code> |
| <code>ERR-01416</code> | <code>ERR_SM_INDEX_INVALID_LEVEL_PART_SIZE</code> | <code>The partition size&lt;%u&gt; of level&lt;%u&gt; is bigger than the max level&lt;%u&gt;</code> |
| <code>ERR-01417</code> | <code>ERR_SM_INDEX_ALREADY_DROPPED</code> | <code>The index has been dropped.</code> |
| <code>ERR-01418</code> | <code>ERR_SM_INDEX_UNIQUE_VIOLATION</code> | <code>The key already exists in the unique index.</code> |
| <code>ERR-01419</code> | <code>ERR_SM_INDEX_PRIMARY_INDEX_ALREADY_CREATED</code> | <code>The primary index is already created on the table.</code> |
| <code>ERR-01420</code> | <code>ERR_SM_INDEX_INVALID_KEYVALUE_N_BITVECTOR_COUNT</code> | <code>The number&lt;%llu&gt; of key values is different from the number&lt;%llu&gt; of bitvectors.</code> |
| <code>ERR-01421</code> | <code>ERR_SM_INDEX_LSM_INVALID_PART_FILE</code> | <code>The partition file&lt;%llu&gt; on the level&lt;%u&gt; of the index&lt;%llu&gt; is invalid.(KPC:%u, BPC:%u)</code> |
| <code>ERR-01422</code> | <code>ERR_SM_INDEX_PRAIMARY_INDEX_NOT_NULL</code> | <code>NULL value is not allowed for the primary index column</code> |
| <code>ERR-01423</code> | <code>ERR_SM_KEYVALUE_CACHE_EXHAUSTED</code> | <code>TAG cache exhausted, increase TAG_CACHE_MAX_MEMORY_SIZE(%llu)</code> |
| <code>ERR-01424</code> | <code>ERR_SM_KEYVALUE_CACHE_TIMEOUT</code> | <code>Could not allocate TAG cache: (Table,part=%llu,%llu) offset/size=%llu/%llu</code> |
| <code>ERR-01425</code> | <code>ERR_SM_KEYVALUE_INDEX_MEMORY_LIMIT</code> | <code>Failed to allocate index memory (Current Allocated Size / Threshold size (%llu/%llu)).</code> |
| <code>ERR-01426</code> | <code>ERR_SM_KEYVALUE_NOT_READY_TO_BUILD_INDEX</code> | <code>Not ready to build keyvalue index (Current Count / Target Count (%llu/%llu) in File).</code> |
| <code>ERR-01501</code> | <code>ERR_SM_CPFILE_INVALID_PAGE_ID</code> | <code>Invalid page id in cpfile. Page id&lt;%d&gt; for the column partition file&lt;%s&gt; is greater than the page max id.</code> |
| <code>ERR-01502</code> | <code>ERR_SM_CPFILE_INVALID_PAGE_TIMESTAMP</code> | <code>Error in reading page&lt;%d&gt; in the column partition file&lt;%s&gt;. Page timestamps &lt;head:%lld, tail:%lld&gt; are invalid.</code> |
| <code>ERR-01503</code> | <code>ERR_SM_CPFILE_INVALID_PAGE_CHECKSUM</code> | <code>Error in reading page&lt;%d&gt; in the column partition file&lt;%s&gt;. Page checksum &lt;write:%#X, read:%#X&gt; are invalid</code> |
| <code>ERR-01504</code> | <code>ERR_SM_CPFILE_FILE_INVALID_SIZE</code> | <code>The size&lt;%u&gt; of the column partition file&lt;%s&gt; is too small. It is supposed to be greater than the size&lt;%u&gt;</code> |
| <code>ERR-01505</code> | <code>ERR_SM_CPFILE_FILE_INVALID_PAGE_UPDATE</code> | <code>The offset&lt;%u&gt; and size&lt;%u&gt; of the update value for the page&lt;id:%u, offset:%u, size:%u&gt; in the column partition file&lt;%s&gt; is invalid</code> |
| <code>ERR-01506</code> | <code>ERR_SM_CPFILE_INVALIDE_FILE_HEAD_CRC</code> | <code>The checksum&lt;write:%#X, read:%#X&gt; of the head of the column partition file&lt;%s&gt; is invalid.</code> |
| <code>ERR-01551</code> | <code>ERR_SM_FDCACHE_GET_FD_FOR_FILE</code> | <code>Error in getting the fd of the file&lt;%s&gt; from the fd cache.</code> |
| <code>ERR-01601</code> | <code>ERR_SM_AGER_THREAD_ABNORMAL_SHUTDOWN</code> | <code>Ager thread terminated abnormally.</code> |
| <code>ERR-01631</code> | <code>ERR_SM_BACKUP_NOT_EXIST_BACKUP_ROOT_DIR</code> | <code>There is no root dir&lt;%s&gt; for the database backup.</code> |
| <code>ERR-01632</code> | <code>ERR_SM_BACKUP_NOT_DATABASE_DESTROYED</code> | <code>The database is not destroyed.</code> |
| <code>ERR-01633</code> | <code>ERR_SM_BACKUP_STATFILE_WRITE</code> | <code>Failed to write data&lt;%u&gt; of the backup stat file&lt;%s&gt;.</code> |
| <code>ERR-01634</code> | <code>ERR_SM_BACKUP_STATFILE_READ</code> | <code>Failed to read data&lt;%u&gt; of the backup stat file&lt;%s&gt;.</code> |
| <code>ERR-01635</code> | <code>ERR_SM_BACKUP_STATFILE_INVALID</code> | <code>The backup statfile&lt;%s&gt; is invalid(CRC&lt;H:%u, B:%u, T:%u).</code> |
| <code>ERR-01636</code> | <code>ERR_SM_BACKUP_NOT_COMPLETE</code> | <code>The backup &lt;%s&gt; is not completed.</code> |
| <code>ERR-01637</code> | <code>ERR_SM_BACKUP_DIR_ALREADY_EXIST</code> | <code>The backup &lt;%s&gt; has already exist.</code> |
| <code>ERR-01638</code> | <code>ERR_SM_BACKUP_INVALID_END_RID</code> | <code>The end rid&lt;%llu&gt; of the table&lt;%llu&gt; in the restored database is invalid.</code> |
| <code>ERR-01639</code> | <code>ERR_SM_BACKUP_NAME_TOO_LONG</code> | <code>The name&lt;%s&gt; of backup is too long, errno = %d.</code> |
| <code>ERR-01640</code> | <code>ERR_SM_BACKUP_FILE_ALREADY_EXIST</code> | <code>The backup file&lt;%s&gt; already exists.</code> |
| <code>ERR-01641</code> | <code>ERR_SM_BACKUP_FILE_INVALID_MAGIC_STRING</code> | <code>The backup file&lt;%s&gt; has the invalid magic string&lt;%s&gt;.</code> |
| <code>ERR-01642</code> | <code>ERR_SM_BACKUP_FILE_HEAD_INVALID_CRC32</code> | <code>The header of backup file&lt;%s&gt; has the invalid crc32&lt;%u&gt;.</code> |
| <code>ERR-01643</code> | <code>ERR_SM_BACKUP_FILE_INVALID_FILENAME_LEN</code> | <code>Length&lt;%u&gt; of backup file&lt;%s&gt; is too long.</code> |
| <code>ERR-01644</code> | <code>ERR_SM_BACKUP_FILE_INVALID_PAGESIZE</code> | <code>The page size &lt;%u&gt; of backup file&lt;%s&gt; is invalid.</code> |
| <code>ERR-01645</code> | <code>ERR_SM_BACKUP_FILE_INVALID_SIZE</code> | <code>The file size &lt;%llu&gt; of the head is different from the size&lt;%llu&gt; on the disk.</code> |
| <code>ERR-01646</code> | <code>ERR_SM_BACKUP_FILE_INVALID_STATE</code> | <code>The backup file is invalid since the backup is not completed.</code> |
| <code>ERR-01647</code> | <code>ERR_SM_INC_BACKUP_NOT_LATEST</code> | <code>An incremental backup requires a previous backup.</code> |
| <code>ERR-01648</code> | <code>ERR_SM_INC_BACKUP_TARGET_NOT_SAME</code> | <code>Backup targets are different from that of previous target.</code> |
| <code>ERR-01701</code> | <code>ERR_SM_TBS_REFERENCED_BY_OBJECTS</code> | <code>The tablespace&lt;%s&gt; is still referenced by other objects such as tables and indexes.</code> |
| <code>ERR-01702</code> | <code>ERR_SM_TBS_NOT_EXIST</code> | <code>The tablespace&lt;%s&gt; does not exist in the database.</code> |
| <code>ERR-01703</code> | <code>ERR_SM_TBS_CANNOT_DROP_SYSTEM_TBS</code> | <code>The SYSTEM_TABLESPACE cannot be dropped.</code> |
| <code>ERR-01704</code> | <code>ERR_SM_TBS_ALEADY_EXIST</code> | <code>Tablespace already exists. &lt;%s&gt;</code> |
| <code>ERR-01705</code> | <code>ERR_SM_TBS_DISKDIR_ALEADY_EXIST</code> | <code>The dir&lt;%s&gt; for the tablespace&lt;%s&gt; of datadisk&lt;%s&gt; already exists.</code> |
| <code>ERR-01706</code> | <code>ERR_SM_TBS_PHYDISK_NOT_EXIST</code> | <code>Disk&lt;%s&gt; does not exist in the tablespace&lt;%s&gt;.</code> |
| <code>ERR-01707</code> | <code>ERR_SM_TBS_PHYDISK_INVALID_PARALLEL_IO</code> | <code>The parallel I/O of a disk should be between %d and %d.</code> |
| <code>ERR-01708</code> | <code>ERR_SM_TBS_FILE_READ</code> | <code>Failed to read &lt;%ld&gt; bytes from the file&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-01709</code> | <code>ERR_SM_TBS_FILE_PAGE_INVALID_TIMESTAMP</code> | <code>The page&lt;offset:%u, size:%u&gt; of the file&lt;%s&gt; is invalid because it has the invalid timestamp&lt;head:%lld, tail:%lld&gt;</code> |
| <code>ERR-01710</code> | <code>ERR_SM_TBS_FILE_PAGE_INVALID_CRC32</code> | <code>The page&lt;offset:%u, size:%u&gt; of the file&lt;%s&gt; is invalid because it has the invalid crc&lt;memory:%u, disk:%u&gt;</code> |
| <code>ERR-01711</code> | <code>ERR_SM_TBS_VIRDISK_DIR_CREATE</code> | <code>Failed to create directory&lt;%s&gt; for virtual disk.</code> |
| <code>ERR-01712</code> | <code>ERR_SM_TBS_MEMORY_DIR_SHORTAGE</code> | <code>Failed to allocate memory for directory to be removed.</code> |
| <code>ERR-01801</code> | <code>ERR_SM_EXTCP_WAIT_READ_VALUE</code> | <code>Error in waiting to read value: value offset&lt;%lld&gt;, value size&lt;%u&gt;, and file&lt;%s&gt;</code> |
| <code>ERR-01821</code> | <code>ERR_SM_DWFILE_INVALID_IMAGE</code> | <code>The image in the DWFile&lt;%s&gt; is invalid.</code> |
| <code>ERR-01841</code> | <code>ERR_SM_ART_ABORT</code> | <code>The operation is aborted by ART.</code> |
| <code>ERR-01851</code> | <code>ERR_SM_NO_VAR_IN_TAG</code> | <code>Variable length columns are not allowed in tag table.</code> |
| <code>ERR-01852</code> | <code>ERR_SM_DELETE_IN_PROGRESS</code> | <code>Another deletion is in progress for table &lt;%llX&gt;.</code> |
| <code>ERR-01853</code> | <code>ERR_SM_KEYVALUE_CREATE_APPENDFILE</code> | <code>Cannot create append file for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01854</code> | <code>ERR_SM_KEYVALUE_SYNC_APPENDFILE</code> | <code>Cannot sync append file for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01855</code> | <code>ERR_SM_KEYVALUE_CLOSE_APPENDFILE</code> | <code>Cannot close append file for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01856</code> | <code>ERR_SM_KEYVALUE_CREATE_DATAFILE</code> | <code>Cannot create data file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01857</code> | <code>ERR_SM_KEYVALUE_OPEN_DATAFILE</code> | <code>Cannot open data file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01858</code> | <code>ERR_SM_KEYVALUE_READ_DATAFILE</code> | <code>Cannot read data file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01859</code> | <code>ERR_SM_KEYVALUE_WRITE_DATAFILE</code> | <code>Cannot write data file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01860</code> | <code>ERR_SM_KEYVALUE_CORRUPTED_DATAFILE</code> | <code>Data file &lt;%llX&gt; is corrupted for Key-Value table &lt;%llX&gt;.</code> |
| <code>ERR-01861</code> | <code>ERR_SM_KEYVALUE_CREATE_INDEXFILE</code> | <code>Cannot create index file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01862</code> | <code>ERR_SM_KEYVALUE_OPEN_INDEXFILE</code> | <code>Cannot open index file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01863</code> | <code>ERR_SM_KEYVALUE_READ_INDEXFILE</code> | <code>Cannot read &lt;.%s&gt; file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01864</code> | <code>ERR_SM_KEYVALUE_WRITE_INDEXFILE</code> | <code>Cannot write &lt;.%s&gt; file &lt;%llX&gt; for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01865</code> | <code>ERR_SM_KEYVALUE_CORRUPTED_INDEXFILE</code> | <code>Index file &lt;%llX&gt; is corrupted for Key-Value table &lt;%llX&gt;.</code> |
| <code>ERR-01866</code> | <code>ERR_SM_KEYVALUE_IOERROR</code> | <code>Cannot perform I/O for Key-Value table &lt;%llX&gt;.</code> |
| <code>ERR-01867</code> | <code>ERR_SM_KEYVALUE_INVALID_PATH_APPENDFILE</code> | <code>Invalid path to append file for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01868</code> | <code>ERR_SM_KEYVALUE_OPEN_APPENDFILE</code> | <code>Cannot open append file for Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01869</code> | <code>ERR_SM_KEYVALUE_NO_DATAFILE</code> | <code>RID-based SELECT is not allowed without datafile, Table&lt;%llX&gt;/RID&lt;%llu&gt;.</code> |
| <code>ERR-01870</code> | <code>ERR_SM_KEYVALUE_OPEN_MOUNTED_APPENDFILE</code> | <code>Cannot open append file for mounted Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01871</code> | <code>ERR_SM_KEYVALUE_READ_MOUNTED_APPENDFILE</code> | <code>Cannot read append file for mounted Key-Value table &lt;%llX&gt;, errno = %d.</code> |
| <code>ERR-01872</code> | <code>ERR_SM_BACKUP_IN_PROGRESS</code> | <code>Another backup is in progress for table &lt;%llX&gt;.</code> |
| <code>ERR-01873</code> | <code>ERR_SM_KEYVALUE_NO_INDEXFILE</code> | <code>No index-file &lt;%llx&gt; for Key-Value table Table&lt;%llX&gt;.</code> |
| <code>ERR-01874</code> | <code>ERR_SM_KEYVALUE_OPEN_FILE</code> | <code>Cannot open file &lt;%llX&gt; for Key-Value table &lt;%llX&gt; path&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-01875</code> | <code>ERR_SM_KEYVALUE_NO_UNPURGED_NODE</code> | <code>Cannot find unpurged node for Key-Value table &lt;%llX&gt;.</code> |
| <code>ERR-01876</code> | <code>ERR_SM_KEYVALUE_FILE_DECOMPRESS</code> | <code>Failed to use %s to decompress file &lt;%llX&gt; for key-value table &lt;%llx&gt;, error = %d.</code> |
| <code>ERR-01877</code> | <code>ERR_SM_KEYVALUE_NOT_FOUND_STAT_DATA</code> | <code>Tag stat for id&#91;%llu&#93; is not found.</code> |
| <code>ERR-01878</code> | <code>ERR_SM_STAT_WRITE_FILE</code> | <code>Cannot write stat file for Key-Value table &lt;%llX&gt; path&lt;%s&gt; errno = %d.</code> |
| <code>ERR-01879</code> | <code>ERR_SM_STAT_READ_FILE</code> | <code>Cannot read stat file for Key-Value table &lt;%llX&gt; path&lt;%s&gt; errno = %d.</code> |
| <code>ERR-01880</code> | <code>ERR_SM_STAT_OPEN_FILE</code> | <code>Cannot open stat file for Key-Value table &lt;%llX&gt; path&lt;%s&gt;, errno = %d.</code> |
| <code>ERR-01881</code> | <code>ERR_SM_STAT_INVALID_FILE</code> | <code>Stat File Invalid TableID&#91;%llu&#93;, TablePath&#91;%s&#93;.</code> |
| <code>ERR-01882</code> | <code>ERR_SM_KEYVALUE_NO_KVINDEXFILE</code> | <code>No kvindex-file &lt;%llx&gt; for Key-Value table Table&lt;%llX&gt;.</code> |
| <code>ERR-01883</code> | <code>ERR_SM_KEYVALUE_INVALID_TIME_VALUE</code> | <code>Value of the time column(&lt;%lld&gt;) must be greater than or equal to &lt;%lld&gt;.</code> |
| <code>ERR-01884</code> | <code>ERR_SM_KEYVALUE_THREAD_STOPPED</code> | <code>keyvalue table&lt;%llx&gt; thread for &#91;%s&#93; stopped.</code> |
| <code>ERR-01885</code> | <code>ERR_SM_KEYVALUE_DATA_CORRUPTED</code> | <code>Data row value is corrupted: required RID&lt;%llu&gt;, value RID&lt;%llu&gt;.</code> |
| <code>ERR-01886</code> | <code>ERR_SM_KEYVALUE_VDATA_CORRUPTED</code> | <code>%s varchar data is corrupted: required VRID&lt;%u&gt;, value VRID&lt;%u&gt;.</code> |
| <code>ERR-01887</code> | <code>ERR_SM_UPDATE_IN_PROGRESS</code> | <code>Another update is in progress for table &lt;%llX&gt;.</code> |
| <code>ERR-01900</code> | <code>ERR_SM_SNAPSHOT_NOT_VALID</code> | <code>Snapshot ID &lt;%s&gt; is invalid.</code> |
| <code>ERR-01901</code> | <code>ERR_SM_SNAPSHOT_NO_TABLE</code> | <code>Cannot snapshot with no table.</code> |
| <code>ERR-01902</code> | <code>ERR_SM_SNAPSHOT_TIMEOUT</code> | <code>Snapshot timed out.</code> |
| <code>ERR-01903</code> | <code>ERR_SM_SNAPSHOT_NOT_EXISTS</code> | <code>Snapshot ID &lt;%s&gt; does not exist.</code> |
| <code>ERR-01904</code> | <code>ERR_SM_SNAPSHOT_ALREADY_EXISTS</code> | <code>Snapshot ID &lt;%s&gt; already exists.</code> |
| <code>ERR-01910</code> | <code>ERR_SM_FREEZE_NO_TABLE</code> | <code>Cannot freeze with no table.</code> |
| <code>ERR-01911</code> | <code>ERR_SM_ALREADY_FROZEN</code> | <code>Snapshot already frozen.</code> |
| <code>ERR-01951</code> | <code>ERR_SM_FUNCTION_CALL</code> | <code>Failed to call function &lt;%s&gt;, errno=%d</code> |
| <code>ERR-01952</code> | <code>ERR_SM_TABLE_RESOURCE_BUSY</code> | <code>Table (0x%llx) resource busy (%s).</code> |

### `ERR-02000`–`ERR-02999` (420)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-02000</code> | <code>QPE_TEST</code> | <code>Memory allocation error, Error code = %d</code> |
| <code>ERR-02001</code> | <code>ERR_QP_OPEN_META</code> | <code>Error in opening meta.</code> |
| <code>ERR-02002</code> | <code>ERR_QP_EXEC_META</code> | <code>Error in executing meta.</code> |
| <code>ERR-02003</code> | <code>ERR_QP_CLOSE_META</code> | <code>Error in closing meta.</code> |
| <code>ERR-02004</code> | <code>ERR_QP_CRT_HASH</code> | <code>Error in creating hash. (errno=%d)</code> |
| <code>ERR-02005</code> | <code>ERR_QP_ALLOC_MEM</code> | <code>Error in allocating memory.</code> |
| <code>ERR-02006</code> | <code>ERR_QP_HASH_ADD</code> | <code>Error in adding hash. (errno=%d)</code> |
| <code>ERR-02007</code> | <code>ERR_QP_FETCH_META</code> | <code>Error in fetching meta.</code> |
| <code>ERR-02008</code> | <code>ERR_QP_HASH_TRAV</code> | <code>Error in traversing hash.</code> |
| <code>ERR-02009</code> | <code>ERR_QP_MEMORY_INSUFFICIENT</code> | <code>Insufficient parser memory.</code> |
| <code>ERR-02010</code> | <code>ERR_QP_PARSE_ERROR</code> | <code>Syntax error: near token (%s).</code> |
| <code>ERR-02011</code> | <code>ERR_QP_TOKEN_ERROR</code> | <code>Unrecognized token (%s).</code> |
| <code>ERR-02012</code> | <code>ERR_QP_SINGLE_ROW_ERROR</code> | <code>Single row error. Single-row subquery returns more than one row. (NOT USED)</code> |
| <code>ERR-02013</code> | <code>ERR_QP_NEED_GROUPBY_ERROR</code> | <code>A GROUP BY clause is required before HAVING.</code> |
| <code>ERR-02014</code> | <code>ERR_QP_COLUMN_NAME_DUPLICATED</code> | <code>Column name is duplicated: (%s).</code> |
| <code>ERR-02015</code> | <code>ERR_QP_COLUMN_TYPE_INVALID</code> | <code>Invalid column type: (%s).</code> |
| <code>ERR-02016</code> | <code>ERR_QP_NO_TABLE_PROPETY_FOUND</code> | <code>Table property (%s) does not exist.</code> |
| <code>ERR-02017</code> | <code>ERR_QP_NO_TABLE_PROPETY_CONVERT</code> | <code>Error in converting table property. Cannot convert string (%s) to integer.</code> |
| <code>ERR-02018</code> | <code>ERR_QP_NO_TABLE_PROPETY_VALUE_RANGE</code> | <code>Table property value is out of range: (%s).</code> |
| <code>ERR-02019</code> | <code>ERR_QP_VARCHAR_TYPE_SIZE_ERROR</code> | <code>Column size must be specified for a variable-length column type.</code> |
| <code>ERR-02020</code> | <code>ERR_QP_TYPE_SIZE_ZERO</code> | <code>Invalid size specified. Cannot specify type size to (%s).</code> |
| <code>ERR-02021</code> | <code>ERR_QP_CREATE_INDEX_INVALID_BITMAP_DATATYPE</code> | <code>Cannot create bitmap index on data type (%s)</code> |
| <code>ERR-02022</code> | <code>ERR_QP_CREATE_INDEX_INVALID_KEYWORD_DATATYPE</code> | <code>Cannot create keyword index on data type (%s)</code> |
| <code>ERR-02023</code> | <code>ERR_QP_SNPRINTF_ERROR</code> | <code>snprintf function error (%d).</code> |
| <code>ERR-02024</code> | <code>ERR_QP_TABLE_CREATE_DUPLICATE</code> | <code>Table %s already exists.</code> |
| <code>ERR-02025</code> | <code>ERR_QP_TABLE_NO_EXISTS</code> | <code>Table %s does not exist.</code> |
| <code>ERR-02026</code> | <code>ERR_QP_TABLE_INSERT_COLUMN_MISMATCH</code> | <code>The number of insert values does not match the number of columns.</code> |
| <code>ERR-02027</code> | <code>ERR_QP_TABLE_INSERT_COLUMN_INT_CONVERSION</code> | <code>Error in table insert column integer conversion. Insert value conversion to integer error (%s).</code> |
| <code>ERR-02028</code> | <code>ERR_QP_TABLE_INSERT_COLUMN_DOUBLE_CONVERSION</code> | <code>Error in table insert column double conversion. Insert value conversion to double error (%s)</code> |
| <code>ERR-02029</code> | <code>ERR_QP_TABLE_INSERT_COLUMN_TIME_FORMAT</code> | <code>Error in table insert column time format. Insert _arrival_time value conversion error.</code> |
| <code>ERR-02030</code> | <code>ERR_QP_TABLE_INSERT_NO_COLUMN</code> | <code>Column name (%s) does not exist.</code> |
| <code>ERR-02031</code> | <code>ERR_QP_TABLE_RESOURCE_BUSY</code> | <code>Resource busy (%s).</code> |
| <code>ERR-02032</code> | <code>ERR_QP_TYPE_COMPARE_CONVERSION</code> | <code>Type conversion error: error occurred while comparing the values of type (%s) and type (%s).</code> |
| <code>ERR-02033</code> | <code>ERR_QP_TYPE_CONCAT</code> | <code>Cannot concatenate non varchar types.</code> |
| <code>ERR-02034</code> | <code>ERR_QP_TIME_FORMAT</code> | <code>Invalid format of time expression.</code> |
| <code>ERR-02035</code> | <code>ERR_QP_FUNCTION_NO_EXISTS</code> | <code>Function &#91;%s&#93; does not exist.</code> |
| <code>ERR-02036</code> | <code>ERR_QP_FUNCTION_ARG</code> | <code>Function &#91;%s&#93; has an invalid argument.</code> |
| <code>ERR-02037</code> | <code>ERR_QP_FUNCTION_ARG_TYPE</code> | <code>Function &#91;%s&#93; argument data type does not match.</code> |
| <code>ERR-02038</code> | <code>ERR_QP_TABLE_NO_SUCH_FOR_STAR</code> | <code>Table &#91;%s&#93; does not exist.</code> |
| <code>ERR-02039</code> | <code>ERR_QP_TABLE_NO_SPECIFIED_FOR_STAR</code> | <code>No table specified in the target list.</code> |
| <code>ERR-02040</code> | <code>ERR_QP_TIME_RANGE_ERROR</code> | <code>Invalid time range.</code> |
| <code>ERR-02041</code> | <code>ERR_QP_TIME_NEGATIVE_ERROR</code> | <code>Time value must be positive.</code> |
| <code>ERR-02042</code> | <code>ERR_QP_NULL_EXPRESSION</code> | <code>Expression cannot have a NULL value.</code> |
| <code>ERR-02043</code> | <code>ERR_QP_AGGR_WHERE</code> | <code>Group function is not allowed here.</code> |
| <code>ERR-02044</code> | <code>ERR_QP_NO_GROUPBY</code> | <code>Not a GROUP BY expression.</code> |
| <code>ERR-02045</code> | <code>ERR_QP_TYPE_UNKNOWN</code> | <code>Type is not supported(typecode is %u). Internal error.</code> |
| <code>ERR-02046</code> | <code>ERR_QP_BUFFER_SHORTAGE</code> | <code>String buffer is not enough.</code> |
| <code>ERR-02047</code> | <code>ERR_QP_LOCK_BUFFER_SHORTAGE</code> | <code>Lock buffer is not enough. Table counts are too many.</code> |
| <code>ERR-02048</code> | <code>ERR_QP_BIND_COUNT_OVERFLOW</code> | <code>Bind parameter count is overflowed. (max=%u)</code> |
| <code>ERR-02049</code> | <code>ERR_QP_BIND_UNABLE</code> | <code>Cannot apply bind parameter.</code> |
| <code>ERR-02050</code> | <code>ERR_QP_BIND_BUFFER_CORRUPTED</code> | <code>Bind data from client is corrupted.</code> |
| <code>ERR-02051</code> | <code>ERR_QP_BIND_TYPE_UNKNOWN</code> | <code>Bind data type unknown (typecode is %u).</code> |
| <code>ERR-02052</code> | <code>ERR_QP_INSERT_UNABLE_TABLE</code> | <code>Cannot insert data into this table (%s).</code> |
| <code>ERR-02053</code> | <code>ERR_QP_TYPE_VALUE_CONVERSION</code> | <code>Failed to convert type (%s) to type (%s).</code> |
| <code>ERR-02054</code> | <code>ERR_QP_AGGR_ERROR_ON_FUNCTION</code> | <code>Aggregation error on function usage (NOT USED)</code> |
| <code>ERR-02055</code> | <code>ERR_QP_ERROR_ON_INSERT_VALUE</code> | <code>Invalid insert value.</code> |
| <code>ERR-02056</code> | <code>ERR_QP_COLUMN_NAME_NOT_FOUND</code> | <code>Column name (%s) not found.</code> |
| <code>ERR-02057</code> | <code>ERR_QP_SEARCH_STRING_ERROR</code> | <code>Only literal type can be used in SEARCH keyword.</code> |
| <code>ERR-02058</code> | <code>ERR_QP_INDEX_CREATE_DUPLICATE</code> | <code>Index %s already exists</code> |
| <code>ERR-02059</code> | <code>ERR_QP_INDEX_NO_EXISTS</code> | <code>Index %s does not exist</code> |
| <code>ERR-02060</code> | <code>ERR_QP_INDEX_ONLY_ONE_COLUMN</code> | <code>Composite index is not supported.</code> |
| <code>ERR-02061</code> | <code>ERR_QP_DIVIDE_BY_ZERO</code> | <code>Cannot divide a value by zero.</code> |
| <code>ERR-02062</code> | <code>ERR_QP_DATE_CALC_INVALID</code> | <code>Cannot calculate date type.</code> |
| <code>ERR-02063</code> | <code>ERR_QP_SEARCH_TYPE_INVALID</code> | <code>Invalid search type. Search type must be VARCHAR.</code> |
| <code>ERR-02064</code> | <code>ERR_QP_ADD_TIME_FORMAT_ERROR</code> | <code>Invalid time format. (format: &quot;year/mon/day hour:min:sec&quot;)</code> |
| <code>ERR-02065</code> | <code>ERR_QP_NO_INDEX_PROPETY_FOUND</code> | <code>Index property (%s) does not exist.</code> |
| <code>ERR-02066</code> | <code>ERR_QP_INDEX_PROPETY_VALUE_INVALID</code> | <code>Invalid index property value: (%s).</code> |
| <code>ERR-02067</code> | <code>ERR_QP_TO_ADDR4_FUNCTION_ARG</code> | <code>Error in TO_ADDR4 function aggregate. Argument type to TO_ADDR4 function must be an integer.</code> |
| <code>ERR-02068</code> | <code>ERR_QP_IPV4_FORMAT</code> | <code>Invalid IPv4 address format (%s).</code> |
| <code>ERR-02069</code> | <code>ERR_QP_INDEX_FOR_INVALID_TABLE</code> | <code>%s index can only be created for %s table.</code> |
| <code>ERR-02070</code> | <code>ERR_QP_INDEX_NEEDED_FOR_SEARCH</code> | <code>Search predicate needs keyword index.</code> |
| <code>ERR-02071</code> | <code>ERR_QP_INDEX_COUNT</code> | <code>Only one index is allowed for a single column.</code> |
| <code>ERR-02072</code> | <code>ERR_QP_DELETE_UNABLE_TABLE</code> | <code>Cannot delete data from this table (%s).</code> |
| <code>ERR-02073</code> | <code>ERR_QP_TABLE_DELETE_CONDITION</code> | <code>Invalid DELETE condition. %s</code> |
| <code>ERR-02074</code> | <code>ERR_QP_TABLE_DELETE_TIME_RANGE</code> | <code>Invalid delete time range. BEFORE time range should be older than present.</code> |
| <code>ERR-02075</code> | <code>ERR_QP_TABLE_DROP_NO_INFO_IN_DB</code> | <code>Table(%s) record does not exist in meta database.</code> |
| <code>ERR-02076</code> | <code>ERR_QP_TABLEID_DROP_NO_INFO_IN_DB</code> | <code>Table(%lld) record does not exist in meta database.</code> |
| <code>ERR-02077</code> | <code>ERR_QP_VARCHAR_SIZE_MAX</code> | <code>Invalid %s size. %s type size cannot be more than %d.</code> |
| <code>ERR-02078</code> | <code>ERR_QP_UNKNOWN_STMT_TYPE</code> | <code>Invalid statement type. Statement type(%d) is unsupported.</code> |
| <code>ERR-02079</code> | <code>ERR_QP_FUNCTION_ARG_COUNT</code> | <code>The number of arguments for function (%s) does not match.</code> |
| <code>ERR-02080</code> | <code>ERR_QP_USER_NOT_EXIST</code> | <code>User (%s) does not exist.</code> |
| <code>ERR-02081</code> | <code>ERR_QP_USER_PASSWORD_ERROR</code> | <code>Invalid username/password.</code> |
| <code>ERR-02082</code> | <code>ERR_QP_USER_ALREADY_EXISTS</code> | <code>User (%s) already exists.</code> |
| <code>ERR-02083</code> | <code>ERR_QP_USER_SELF_DROP</code> | <code>You cannot drop yourself(%s).</code> |
| <code>ERR-02084</code> | <code>ERR_QP_USER_TABLE_EXIST</code> | <code>User drop error. This user&#x27;s tables still exist. Drop those tables first.</code> |
| <code>ERR-02085</code> | <code>ERR_QP_USER_NO_ALTER_PRIV</code> | <code>The user(%s) does not have alter privileges.</code> |
| <code>ERR-02086</code> | <code>ERR_QP_USER_NO_CONNECT_PRIV</code> | <code>The user(%s) does not have connect privileges.</code> |
| <code>ERR-02087</code> | <code>ERR_QP_USER_NO_PRIV_TABLE_ACCESS</code> | <code>The user does not have access privileges on table(%s.%s).</code> |
| <code>ERR-02088</code> | <code>ERR_QP_ALTER_TABLE_NO_RIGHT</code> | <code>Error in altering table. Only the LOG table can be altered.</code> |
| <code>ERR-02089</code> | <code>ERR_QP_ALTER_TABLE_SAME_COLUMN_EXISTS</code> | <code>Error in altering table. Column name(%s) already exists.</code> |
| <code>ERR-02090</code> | <code>ERR_QP_ALTER_TABLE_MODIFY_TYPE</code> | <code>Error in altering table. Only varchar type can be modified.</code> |
| <code>ERR-02091</code> | <code>ERR_QP_ALTER_TABLE_MODIFY_VARCHAR_SIZE</code> | <code>Error in altering table. Varchar length should be greater than previous value length</code> |
| <code>ERR-02092</code> | <code>ERR_QP_ALTER_TABLE_DROP_BUILTIN_COLUMN</code> | <code>Error in altering table. Column (%s) cannot be dropped.</code> |
| <code>ERR-02093</code> | <code>ERR_QP_ALTER_TABLE_DROP_COLUMN_ON_INDEX</code> | <code>Error in altering table. Column (%s) having index cannot be dropped.</code> |
| <code>ERR-02094</code> | <code>ERR_QP_ALTER_TABLE_DUP_COLUMN</code> | <code>Error in altering table. Column (%s) already exists.</code> |
| <code>ERR-02095</code> | <code>ERR_QP_TRUNCATE_NON_LOG_TABLE</code> | <code>Error in truncating table. Only the LOG table can be truncated.</code> |
| <code>ERR-02096</code> | <code>ERR_QP_TABLE_TRUNCATE_NO_EXISTS</code> | <code>Error in truncating table. Table %s does not exist.</code> |
| <code>ERR-02097</code> | <code>ERR_QP_TABLE_DROP_COLUMN_LIMIT</code> | <code>Error in altering table. The table must have at least one column.</code> |
| <code>ERR-02098</code> | <code>ERR_QP_NOT_EQUJOIN</code> | <code>Error in joining tables. Only equi-join is allowed.</code> |
| <code>ERR-02099</code> | <code>ERR_QP_JOIN_OR</code> | <code>Error in joining tables. The OR condition for a join predicate is not allowed.</code> |
| <code>ERR-02100</code> | <code>ERR_QP_JOIN_FUNCTION_EXPR</code> | <code>Error in joining tables. The join predicate cannot use functions.</code> |
| <code>ERR-02101</code> | <code>ERR_QP_JOIN_PERMUTATION</code> | <code>Error in joining tables. Cannot join without join predicate.</code> |
| <code>ERR-02104</code> | <code>ERR_QP_COLLECTOR_NO_TEMPLATE_EXISTS</code> | <code>The template file (%s) does not exist.</code> |
| <code>ERR-02105</code> | <code>ERR_QP_COLLECTOR_TEMPLATE_FORMAT_INVALID</code> | <code>The template format (%s : %s : %d) is invalid.</code> |
| <code>ERR-02109</code> | <code>ERR_QP_JOIN_LOG_LOG</code> | <code>Cannot join two or more LOG tables.</code> |
| <code>ERR-02110</code> | <code>ERR_QP_KEYWD_MIN_LENGTH</code> | <code>Search condition argument is too short. It needs more than (%d) characters.</code> |
| <code>ERR-02111</code> | <code>ERR_QP_NO_SUCH_COMMAND</code> | <code>Invalid option.</code> |
| <code>ERR-02112</code> | <code>ERR_QP_NO_DISTINCT_GRBY</code> | <code>Cannot use DISTINCT with GROUP BY clause.</code> |
| <code>ERR-02113</code> | <code>ERR_QP_NO_DISTINCT_AGGR</code> | <code>Cannot use DISTINCT with aggregation function.</code> |
| <code>ERR-02114</code> | <code>ERR_QP_FUNCTION_DISTINCT</code> | <code>DISTINCT clause is not allowed here.</code> |
| <code>ERR-02115</code> | <code>ERR_QP_INVALID_COL_NAME</code> | <code>Internal column cannot be modified.</code> |
| <code>ERR-02116</code> | <code>ERR_QP_SEARCH_FILTER</code> | <code>Search predicate must use an index.</code> |
| <code>ERR-02117</code> | <code>ERR_QP_TABLE_NAME_INVALID</code> | <code>DDL on table (%s) is forbidden.</code> |
| <code>ERR-02118</code> | <code>ERR_QP_TABLE_LOCK_ALREADY_INIT</code> | <code>Lock object was already initialized. (Do not use select and append simultaneously in single session.)</code> |
| <code>ERR-02119</code> | <code>ERR_QP_NOT_IMPLEMENTED</code> | <code>This functionality has not been implemented.</code> |
| <code>ERR-02120</code> | <code>ERR_QP_SESSION_ID_INVALID</code> | <code>Invalid session ID (%s).</code> |
| <code>ERR-02121</code> | <code>ERR_QP_SESSION_PRIV_OF_KILL</code> | <code>No privileges to kill the session.</code> |
| <code>ERR-02122</code> | <code>ERR_QP_SESSION_PRIV_OF_CANCEL</code> | <code>No privileges to cancel the session.</code> |
| <code>ERR-02123</code> | <code>ERR_QP_NOT_EXIST_TABLE_ID_META</code> | <code>Table id (%lld) does not exist in meta database.</code> |
| <code>ERR-02124</code> | <code>ERR_QP_NOT_EXIST_COLUMN_ID_META</code> | <code>Column id (%llu) does not exist in table (%llu).</code> |
| <code>ERR-02125</code> | <code>ERR_QP_VARCHAR_TO_DATE_HEURISTIC</code> | <code>Error in converting string (%s) to datetime with heuristic method. Check the default date string format in this session.</code> |
| <code>ERR-02126</code> | <code>ERR_QP_NO_ORDERBY_SUBQ</code> | <code>ORDER BY clause is not allowed in a subquery</code> |
| <code>ERR-02127</code> | <code>ERR_QP_ORDERBY_TERMS</code> | <code>Only integer constants must be used for ORDER BY column position.</code> |
| <code>ERR-02128</code> | <code>ERR_QP_ORDERBY_OOR</code> | <code>ORDER BY column position %d is out of range - should be between 1 and %d.</code> |
| <code>ERR-02129</code> | <code>ERR_QP_GRBY_INT</code> | <code>GROUP BY terms must be integer constants</code> |
| <code>ERR-02130</code> | <code>ERR_QP_NO_GRBY_HAVING</code> | <code>A GROUP BY clause is required before HAVING</code> |
| <code>ERR-02131</code> | <code>ERR_QP_SUBQ_NOT_SINGLE</code> | <code>Single row error. Single-row subquery returns more than one row.</code> |
| <code>ERR-02132</code> | <code>ERR_QP_SUBQ_NOT_ALLOWED</code> | <code>Cannot use subquery on HAVING, ORDER BY and GROUP BY clauses.</code> |
| <code>ERR-02133</code> | <code>ERR_QP_INVALID_SUBQ</code> | <code>Invalid subquery.</code> |
| <code>ERR-02134</code> | <code>ERR_QP_REGEX_MAX_COUNT</code> | <code>Too many REGEXP in WHERE clause. No more than %d REGEXP in WHERE clause.</code> |
| <code>ERR-02135</code> | <code>ERR_QP_WHERE_TYPE</code> | <code>WHERE clause has to return a boolean result.</code> |
| <code>ERR-02136</code> | <code>ERR_QP_TBS_INVALID_TYPE</code> | <code>Invalid tablespace type.</code> |
| <code>ERR-02137</code> | <code>ERR_QP_TBS_TOO_MANY_DISKS</code> | <code>There are too many disks&lt;%ud&gt; for tablespace %s.</code> |
| <code>ERR-02138</code> | <code>ERR_QP_TBS_DISK_INVALID_PARALLEL_IO_VALUE</code> | <code>The PARALLEL_IO value&lt;%d&gt; for the disk&lt;%s&gt; must be higher than &lt;%d&gt;.</code> |
| <code>ERR-02139</code> | <code>ERR_QP_NO_MINMAX_ON_VARCHAR</code> | <code>MINMAX CACHE is not allowed for VARCHAR column(%s).</code> |
| <code>ERR-02140</code> | <code>ERR_QP_TABLE_NOT_SUPPORT_TABLESPACE</code> | <code>This type of tables do not support the tablespace functionality.</code> |
| <code>ERR-02141</code> | <code>ERR_QP_TYPE_COMPARE_NOT_APPLICABLE</code> | <code>Type comparison error.</code> |
| <code>ERR-02142</code> | <code>ERR_QP_NO_AGGR_LOB</code> | <code>Cannot use lob type in the GROUP BY clause.</code> |
| <code>ERR-02143</code> | <code>ERR_QP_NO_ORDER_LOB</code> | <code>Cannot use lob type in the ORDER BY clause.</code> |
| <code>ERR-02144</code> | <code>ERR_QP_OUTERJOIN_LIMIT</code> | <code>Outerjoin permits only 2 tables.</code> |
| <code>ERR-02145</code> | <code>ERR_QP_NOT_NUMBER_STRING</code> | <code>The string cannot be converted to number value.(%s)</code> |
| <code>ERR-02146</code> | <code>ERR_QP_TS_JOIN_LIMIT</code> | <code>Cannot join tables with timeseries function.</code> |
| <code>ERR-02147</code> | <code>ERR_QP_TS_VIEW_LIMIT</code> | <code>Cannot use inline view with timeseries function.</code> |
| <code>ERR-02148</code> | <code>ERR_QP_IPV6_FORMAT</code> | <code>Invalid IPv6 address format.(%s)</code> |
| <code>ERR-02149</code> | <code>ERR_QP_CONTAINS_TYPE_INVALID</code> | <code>Error in executing CONTAINS. Cannot convert from type(%d) to type(%d).</code> |
| <code>ERR-02150</code> | <code>ERR_QP_IP_NETWORK_TYPE_CLASS_MISMATCHED</code> | <code>Network type error. Network Mask length does not match with the column&#x27;s length.(mask=%s, column=%s)</code> |
| <code>ERR-02151</code> | <code>ERR_QP_NO_MORE_DISK_FOR_EVALUATION</code> | <code>Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.</code> |
| <code>ERR-02152</code> | <code>ERR_QP_PARTITION_PROPERTY_NOT_COMPLETE</code> | <code>Error in setting column property. You should specify a positive value of column property PARTITION_PAGE_COUNT as well as PAGE_VALUE_COUNT.</code> |
| <code>ERR-02153</code> | <code>ERR_QP_UNKNOWN_COLUMN_PROPERTY</code> | <code>Invalid column property name (%s). Specify a valid property name.</code> |
| <code>ERR-02154</code> | <code>ERR_QP_SET_OP_NO_SELECT</code> | <code>Select set operator parsing error.</code> |
| <code>ERR-02155</code> | <code>ERR_QP_UNSURPPORTED_SET_OP</code> | <code>Only UNION ALL set operator is supported.</code> |
| <code>ERR-02156</code> | <code>ERR_QP_SET_OP_TARGET_MISMATCH</code> | <code>Set operator column types do not match at column (%d).</code> |
| <code>ERR-02157</code> | <code>ERR_QP_VALIDATE_INTERNAL</code> | <code>Internal error on validating query</code> |
| <code>ERR-02158</code> | <code>ERR_QP_INVALID_TYPE</code> | <code>Error in evaluating data type. You must specify a valid data type.</code> |
| <code>ERR-02159</code> | <code>ERR_QP_INVALID_BACKUP_RANGE</code> | <code>&#x27;FROM DATETIME&#x27; must be earlier than &#x27;TO DATETIME&#x27;.</code> |
| <code>ERR-02160</code> | <code>ERR_QP_UNMOUNT_NOT_MOUNTED_TABLE</code> | <code>Error in doing unmount table(%s). You can unmount only mounted tables.</code> |
| <code>ERR-02161</code> | <code>ERR_QP_NO_DDL_ON_MOUTE_MODE</code> | <code>Error in executing DDL. You cannot execute DDL with mounted DB. (&#42;NOT USED&#42;)</code> |
| <code>ERR-02162</code> | <code>ERR_QP_NO_UNMOUTE_DB</code> | <code>Error in doing unmount DB. You cannot umount database which is not mounted.</code> |
| <code>ERR-02163</code> | <code>ERR_QP_WRONG_RESTORE_PATH</code> | <code>Invalid directory path (%s). You should specify a valid path.</code> |
| <code>ERR-02164</code> | <code>ERR_QP_INVALID_ALTER_INDEX_PROPETY</code> | <code>Invalid index property. Property (%s) for index cannot be altered.</code> |
| <code>ERR-02165</code> | <code>ERR_QP_FUNCTION_POS</code> | <code>Function (%s) is not allowed here.</code> |
| <code>ERR-02166</code> | <code>ERR_QP_FUNCTION_ORDER_BY</code> | <code>Cannot use ORDER BY clause with aggregation function.</code> |
| <code>ERR-02167</code> | <code>ERR_QP_FUNCTION_GROUP_CONCAT_WRONG_SEPARATOR</code> | <code>GROUP_CONCAT function error. Separator should be a string constant.</code> |
| <code>ERR-02168</code> | <code>ERR_QP_OPERATOR_ARG_ERROR</code> | <code>Operator argument count or type does not match.</code> |
| <code>ERR-02169</code> | <code>ERR_QP_WRONG_COLUMN_PROPERTY_VALUE</code> | <code>Invalid column property value: (%s)</code> |
| <code>ERR-02170</code> | <code>ERR_QP_NO_ALIAS_IN_TABLE_INLINE_VIEW</code> | <code>Every specified table or inline view in FROM clause must have its own alias.</code> |
| <code>ERR-02171</code> | <code>ERR_QP_PRIMARY_KEY_DUPLICATE_PK_DECL</code> | <code>VOLATILE / LOOKUP / TRANSACTION table cannot have more than one primary key.</code> |
| <code>ERR-02172</code> | <code>ERR_QP_PRIMARY_KEY_INVALID_TABLE</code> | <code>Primary key is allowed only for VOLATILE / LOOKUP / TRANSACTION table.</code> |
| <code>ERR-02173</code> | <code>ERR_QP_VOLATILE_TABLE_INVALID_TYPE</code> | <code>Cannot create columns with data type (%s) in VOLATILE / LOOKUP table.</code> |
| <code>ERR-02174</code> | <code>ERR_QP_INDEX_TARGET_COLUMN_DUPLICATE</code> | <code>The index already exists in the column(%s).</code> |
| <code>ERR-02175</code> | <code>ERR_QP_VTABLE_UPDATE_INVALID_FORM</code> | <code>SET clause must be written as a list of &#x27;column = value&#x27; expression.</code> |
| <code>ERR-02176</code> | <code>ERR_QP_VTABLE_UPDATE_TO_PRIMARY_KEY</code> | <code>Cannot update primary key column in SET clause.</code> |
| <code>ERR-02177</code> | <code>ERR_QP_VTABLE_UPDATE_NOT_IN_VOLATILE</code> | <code>ON DUPLICATE UPDATE clause is allowed only in LOOKUP / VOLATILE / TRANSACTION table.</code> |
| <code>ERR-02178</code> | <code>ERR_QP_TABLE_UPDATE_NO_COLUMN</code> | <code>Error in updating table. Column name (%s) does not exist in this table.</code> |
| <code>ERR-02179</code> | <code>ERR_QP_VTABLE_INSERT_WITHOUT_PRIMARY_KEY_VAL</code> | <code>INSERT on a %s table without primary key value cannot be proceeded.</code> |
| <code>ERR-02180</code> | <code>ERR_QP_VTABLE_UPDATE_ON_NO_PRIMARY_KEY</code> | <code>Primary key is mandatory for UPDATE.</code> |
| <code>ERR-02181</code> | <code>ERR_QP_INDEX_WITH_PRIMARY_KEY_PREFIX</code> | <code>Invalid index name starting with (%s) which is the same as primary key index.</code> |
| <code>ERR-02182</code> | <code>ERR_QP_PRIMARY_KEY_INDEX_DROP</code> | <code>You cannot drop the primary key index (%s).</code> |
| <code>ERR-02183</code> | <code>ERR_QP_APPEND_TO_VTABLE_UNSUPPORTED</code> | <code>Append mode for table (%s) is not supported.</code> |
| <code>ERR-02184</code> | <code>ERR_QP_PROPERTY_ON_INVALID_TABLE_TYPE</code> | <code>Specified property value is invalid in %s table.</code> |
| <code>ERR-02185</code> | <code>ERR_QP_MOUNT_DB_DUPLICATED</code> | <code>Invalid database name. This database name is already used for mount.</code> |
| <code>ERR-02186</code> | <code>ERR_QP_MOUNT_DB_INVALID</code> | <code>Invalid database name.</code> |
| <code>ERR-02187</code> | <code>ERR_QP_UNMOUNT_TABLE_IN_ACCESS</code> | <code>Error in unmounting database. Some tables in mounted database are accessed by other transactions</code> |
| <code>ERR-02188</code> | <code>ERR_QP_MOUNT_DB_NOT_FOUND</code> | <code>The database is not mounted.</code> |
| <code>ERR-02189</code> | <code>ERR_QP_DELETE_WHERE_INVALID_TABLE</code> | <code>Error in deleting rows. Only rows in VOLATILE / LOOKUP table can be deleted.</code> |
| <code>ERR-02190</code> | <code>ERR_QP_UPDATE_DELETE_WHERE_INVALID_CONDITION</code> | <code>Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)</code> |
| <code>ERR-02191</code> | <code>ERR_QP_DELETE_WHERE_UNSUPPORTED</code> | <code>WHERE clause in DELETE statement is not supported yet.</code> |
| <code>ERR-02192</code> | <code>ERR_QP_KEYWORD_INDEX_TYPE</code> | <code>Index type for keyword index only supports keyword bitmap or keyword LSM.</code> |
| <code>ERR-02195</code> | <code>ERR_QP_BUFFER_OVERFLOW</code> | <code>Buffer size insufficient.</code> |
| <code>ERR-02196</code> | <code>ERR_QP_NO_FILE_TO_LOAD</code> | <code>Error in loading data. File (%s) does not exist.</code> |
| <code>ERR-02197</code> | <code>ERR_QP_LOAD_TABLE_ALREADY_EXISTS</code> | <code>Error in loading data with automatic mode. The table (%s) already exists.</code> |
| <code>ERR-02198</code> | <code>ERR_QP_LOAD_TABLE_NON_EXISTS</code> | <code>Error loading data. Table (%s) does not exist.</code> |
| <code>ERR-02199</code> | <code>ERR_QP_LOAD_TABLE_PARSING_ERROR</code> | <code>CSV parsing error on line %d: &#91;%s&#93;.</code> |
| <code>ERR-02200</code> | <code>ERR_QP_LOAD_TABLE_DELIMITOR_ERROR</code> | <code>&#91;%s&#93; is not a valid string terminator or enclosure.</code> |
| <code>ERR-02201</code> | <code>ERR_QP_LOAD_TABLE_UNKNOWN_AUTOMODE</code> | <code>The automatic loading mode is invalid.</code> |
| <code>ERR-02202</code> | <code>ERR_QP_LOAD_TABLE_HEADER_DETECT_ERROR</code> | <code>Automatic column detection failed because the data is empty or the headers are invalid.</code> |
| <code>ERR-02203</code> | <code>ERR_QP_LOAD_TABLE_UNKNOWN_ENCODINGMODE</code> | <code>Invalid encoding.</code> |
| <code>ERR-02204</code> | <code>ERR_QP_LOAD_TABLE_CHAR_CONVERSION_ERROR</code> | <code>Failed to convert %s to UTF8.</code> |
| <code>ERR-02205</code> | <code>ERR_QP_NO_SUPPORT_DOUBLE_MOD</code> | <code>A modulo operator can be applied only for integer types.</code> |
| <code>ERR-02206</code> | <code>ERR_QP_NO_SUPPORT_TBS_NON_AUTO</code> | <code>Tablespace name cannot be specified in non automode</code> |
| <code>ERR-02207</code> | <code>ERR_QP_SAVE_FILE_ALREADY_EXISTS</code> | <code>Error in saving table into file (%s). File already exists.</code> |
| <code>ERR-02208</code> | <code>ERR_QP_EXPR_TYPE</code> | <code>Expression argument type does not match.</code> |
| <code>ERR-02221</code> | <code>ERR_QP_NO_MANAGER_NAME_SETTED</code> | <code>Manager name is not specified.</code> |
| <code>ERR-02222</code> | <code>ERR_QP_RECEIVE_DIFF_PROTOCOL</code> | <code>Error in read protocol. Send %s protocol, but received %d protocol.</code> |
| <code>ERR-02223</code> | <code>ERR_QP_COLLECTORMANAGER_CONNECT</code> | <code>Unable to establish connection with collectormanager (%s).</code> |
| <code>ERR-02224</code> | <code>ERR_QP_NO_COLLECTOR_NAME_SETTED</code> | <code>Manager name is not specified.</code> |
| <code>ERR-02225</code> | <code>ERR_QP_SET_COLUMN_UNIT_ERROR</code> | <code>Invalid set column unit.</code> |
| <code>ERR-02226</code> | <code>ERR_QP_INVALID_CHARACTER</code> | <code>Invalid character (&#x27;%c&#x27;).</code> |
| <code>ERR-02228</code> | <code>ERR_QP_UNSUPPORT_PROCEDURE</code> | <code>Invalid procedure (%s).</code> |
| <code>ERR-02229</code> | <code>ERR_QP_INVALID_ARG_VALUE</code> | <code>Invalid argument value for function (%s).</code> |
| <code>ERR-02230</code> | <code>ERR_QP_PROCEDURE_WRONG_NUMBER_OF_ARGUMENTS</code> | <code>Wrong number of arguments in call to &#x27;%s&#x27;.</code> |
| <code>ERR-02231</code> | <code>ERR_QP_STRCPY_ERROR</code> | <code>strcpy function error (%d).</code> |
| <code>ERR-02232</code> | <code>ERR_QP_CALC_TYPE</code> | <code>Calculation argument type (%s), (%s) error.</code> |
| <code>ERR-02233</code> | <code>ERR_QP_INSERT_VALUE_LOCATION</code> | <code>Error occurred at column (%u): (%s)</code> |
| <code>ERR-02234</code> | <code>ERR_QP_SET_OP_COUNT</code> | <code>Set operator column counts do not match (%d and %d).</code> |
| <code>ERR-02235</code> | <code>ERR_QP_SERIES_BY</code> | <code>SERIES BY clause is not allowed here.</code> |
| <code>ERR-02236</code> | <code>ERR_QP_TOO_MANY_TABLES_IN_JOIN</code> | <code>For a table list in FROM clause, The number of tables should be less than 32.</code> |
| <code>ERR-02237</code> | <code>ERR_QP_INDEX_NOT_CREATED_ON_TABLE</code> | <code>The index &lt;%s&gt; is not an index for the table &lt;%s&gt;.</code> |
| <code>ERR-02238</code> | <code>ERR_QP_NO_JOIN_TYPE</code> | <code>This type of join is not allowed.</code> |
| <code>ERR-02239</code> | <code>ERR_QP_INVALID_USE_AGGR_FUNC</code> | <code>Invalid use of aggregation function.</code> |
| <code>ERR-02240</code> | <code>ERR_QP_INVALID_COLUMN_TYPE_FOR_FETCH</code> | <code>Cannot fetch column with type (%s).</code> |
| <code>ERR-02241</code> | <code>ERR_QP_UNSUPPORTED_JOIN_TABLES</code> | <code>Join between LOG table and fixed table is not supported in Cluster Edition.</code> |
| <code>ERR-02242</code> | <code>ERR_QP_EQUIJOIN_WITH_LOGTABLE_JOIN</code> | <code>Only equality predicates are supported when joining LOG tables in Cluster Edition.</code> |
| <code>ERR-02243</code> | <code>ERR_QP_UNSUPPORTED_ROW_BASED_DELETE</code> | <code>DELETE statement with the number of rows is not supported in Cluster Edition.</code> |
| <code>ERR-02246</code> | <code>ERR_QP_IDENTIFIER_TOO_LONG</code> | <code>Identifier %.&#42;s is too long.</code> |
| <code>ERR-02247</code> | <code>ERR_QP_DATETIME_NOT_PROPER</code> | <code>DATETIME earlier than 1970-01-01 00:00:00 (UTC) is not valid.</code> |
| <code>ERR-02248</code> | <code>ERR_QP_INSUFFICIENT_COLUMN_DEF</code> | <code>Insufficient column definitions.</code> |
| <code>ERR-02249</code> | <code>ERR_QP_TABLE_DELETE_INVALID_COND</code> | <code>Invalid DELETE condition.</code> |
| <code>ERR-02250</code> | <code>ERR_QP_TAGDATA_COMPONENT_DDL_BLOCKED</code> | <code>You cannot execute DDL on compoment table/index of TAGDATA table explictly.</code> |
| <code>ERR-02251</code> | <code>ERR_QP_TAGDATA_DUPLICATE_FLAG</code> | <code>You cannot define columns with duplicate flag (%s) in TAGDATA table.</code> |
| <code>ERR-02252</code> | <code>ERR_QP_TAGDATA_INVALID_TYPE_FOR_FLAG</code> | <code>Invalid column type (%s) for flag (%s) in TAGDATA table.</code> |
| <code>ERR-02253</code> | <code>ERR_QP_TAGDATA_INSUFFICIENT_MANDATORY</code> | <code>Mandatory column definition (PRIMARY KEY / BASE TIME) is missing.</code> |
| <code>ERR-02254</code> | <code>ERR_QP_INVALID_TAGDATA_FLAG_ON_OTHER_TABLE</code> | <code>Column flag (%s) is only allowed for TAG table.</code> |
| <code>ERR-02255</code> | <code>ERR_QP_TAGDATA_INSERT_META_NO_PK</code> | <code>Primary key of TAGDATA table is not defined in metadata.</code> |
| <code>ERR-02256</code> | <code>ERR_QP_TAGDATA_INVALID_META_COLUMN_CLAUSE</code> | <code>Metadata column definition is allowed only in TAGDATA table.</code> |
| <code>ERR-02257</code> | <code>ERR_QP_TAGDATA_INSERT_META_INVALID_TYPE</code> | <code>Metadata insertion is allowed only in TAGDATA table.</code> |
| <code>ERR-02258</code> | <code>ERR_QP_TAGDATA_ALREADY_INSERTED</code> | <code>Metadata key (%.&#42;s) for the TAG table has already been inserted.</code> |
| <code>ERR-02259</code> | <code>ERR_QP_TAGDATA_NOT_FOUND</code> | <code>Metadata of TAGDATA table is not found. (Key = %s)</code> |
| <code>ERR-02260</code> | <code>ERR_QP_TAGDATA_ALLOC_FAILURE</code> | <code>Failed to allocate new metadata of TAGDATA table (Current Size=%llu).</code> |
| <code>ERR-02261</code> | <code>ERR_QP_NO_TAGDATA_METADATA_INSERT_UPDATE</code> | <code>You cannot insert metadata into TAGDATA table with ON DUPLICATE KEY UPDATE clause.</code> |
| <code>ERR-02262</code> | <code>ERR_QP_TAGDATA_DIRECT_DML_BLOCKED</code> | <code>Direct DML on component tables of TAGDATA table is not allowed.</code> |
| <code>ERR-02263</code> | <code>ERR_QP_TAGDATA_MORE_TAGDATA_TABLE</code> | <code>You can create only one TAGDATA table.</code> |
| <code>ERR-02264</code> | <code>ERR_QP_TAGDATA_SCAN_OTHER_COLUMN_IN_ROLLUP</code> | <code>Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP column.</code> |
| <code>ERR-02265</code> | <code>ERR_QP_TAGDATA_SCAN_WITHOUT_KEY_CONDITION</code> | <code>Reading TAGDATA table without primary key condition is not allowed.</code> |
| <code>ERR-02266</code> | <code>ERR_QP_TAGDATA_DELETE_RAW_CONDITION</code> | <code>You cannot delete raw data of TAGDATA table with WHERE condition.</code> |
| <code>ERR-02267</code> | <code>ERR_QP_TAGDATA_UNSUPPORTED_KEY_PREDICATE</code> | <code>Primary key in TAGDATA table should be compared by &#x27;=&#x27; or &#x27;IN&#x27; operation.</code> |
| <code>ERR-02268</code> | <code>ERR_QP_TAGDATA_COMPARE_KEY_ONLY_CONSTANT</code> | <code>Primary key in TAGDATA table should be compared with constant value.</code> |
| <code>ERR-02269</code> | <code>ERR_QP_TAGDATA_OUTERJOIN</code> | <code>Outerjoin on TAGDATA table is not allowed.</code> |
| <code>ERR-02270</code> | <code>ERR_QP_TAGDATA_NAME_VIOLATION</code> | <code>TAGDATA table&#x27;s name should be &#x27;TAG&#x27;.</code> |
| <code>ERR-02271</code> | <code>ERR_QP_TAGDATA_NOT_CONSTANT_PK_VALUE</code> | <code>You must insert key value of TAGDATA table as constant.</code> |
| <code>ERR-02272</code> | <code>ERR_QP_NOT_EXIST_INDEX_ID_META</code> | <code>Index id (%llu) does not exist in meta database.</code> |
| <code>ERR-02273</code> | <code>ERR_QP_TAGDATA_USER_NO_PRIV_DDL</code> | <code>The user does not have privileges on TAGDATA DDL.</code> |
| <code>ERR-02274</code> | <code>ERR_QP_TAGDATA_FREE_FAILURE</code> | <code>Failed to free new metadata of TAGDATA table.</code> |
| <code>ERR-02275</code> | <code>ERR_QP_TAGDATA_INSERT_SELECT_IN_EE</code> | <code>The INSERT SELECT statement to the TAGDATA table is not allowed in enterprise edition.</code> |
| <code>ERR-02276</code> | <code>ERR_QP_TAGDATA_COMPONENT_EXISTS</code> | <code>Component table (%s) of TAGDATA table already exists.</code> |
| <code>ERR-02277</code> | <code>ERR_QP_TAGDATA_COMPONENT_NAME_RESERVED</code> | <code>Table or index name that starts with &#x27;_TAG&#x27; is reserved.</code> |
| <code>ERR-02278</code> | <code>ERR_QP_UPDATE_INVALID_TABLE_TYPE</code> | <code>UPDATE statement is not allowed for %s.</code> |
| <code>ERR-02279</code> | <code>ERR_QP_TAGDATA_INVALID_PRIMARY_NAME</code> | <code>Invalid tag name insertion to TAGDATA table (name = &#x27;%s&#x27;).</code> |
| <code>ERR-02280</code> | <code>ERR_QP_TAGDATA_INVALID_BIND_TAGNAME</code> | <code>Invalid tag name insertion due to wrong bind variable.</code> |
| <code>ERR-02281</code> | <code>ERR_QP_DURATION_NOT_APPLICABLE</code> | <code>DURATION clause is not applicable on %s.</code> |
| <code>ERR-02282</code> | <code>ERR_QP_DELETE_ALREADY_DOING</code> | <code>The DELETE statement for table &#x27;%s&#x27; is already been executed.</code> |
| <code>ERR-02283</code> | <code>ERR_QP_TAGDATA_IN_SUBQUERY_NOT_ALLOWED</code> | <code>IN subquery on TAGDATA table is not allowed.</code> |
| <code>ERR-02284</code> | <code>ERR_QP_INTERNAL_NULL_EXIST</code> | <code>Internal NULL value exists in the condition expression.</code> |
| <code>ERR-02285</code> | <code>ERR_QP_INTERNAL_ERROR</code> | <code>Internal error: %s.</code> |
| <code>ERR-02286</code> | <code>ERR_QP_KV_TABLE_MEMORY_ALLOC</code> | <code>Memory allocation failed while creating TAGDATA table. You may need to decrease TAG_DATA_PART_SIZE in machbase.conf.</code> |
| <code>ERR-02287</code> | <code>ERR_QP_TAGDATA_NAME_TRUNCATED</code> | <code>TAGDATA name value (%s) is too long.</code> |
| <code>ERR-02288</code> | <code>ERR_QP_AGGR_EXPECTED</code> | <code>Aggregate function is expected at (%.&#42;s).</code> |
| <code>ERR-02289</code> | <code>ERR_QP_NON_CONST</code> | <code>Non-constant expression is not allowed for PIVOT values.</code> |
| <code>ERR-02290</code> | <code>ERR_QP_CANNOT_ALTER</code> | <code>%s cannot be altered.</code> |
| <code>ERR-02291</code> | <code>ERR_QP_INVALID_TABLE_NAME_TAG</code> | <code>Table name &#x27;TAG&#x27; must be used for TAGDATA table.</code> |
| <code>ERR-02292</code> | <code>ERR_QP_TAGDATA_INVALID_CONSTRAINT_ORDER</code> | <code>The order of columns in TAGDATA table must be (PRIMARY, BASE TIME, SUMMARIZED, other columns, .. ).</code> |
| <code>ERR-02293</code> | <code>ERR_QP_NO_BIND_PARAM_COLUMN</code> | <code>Column meta for bind param&#91;%d&#93; is not available.</code> |
| <code>ERR-02294</code> | <code>ERR_QP_TAGDATA_JOIN</code> | <code>Joining more than one TAGDATA table is not supported.</code> |
| <code>ERR-02295</code> | <code>ERR_QP_INVALID_ORDINAL_NUMBER</code> | <code>Invalid ordinal number ID_COLUMN (%lld) and TIME_COLUMN (%lld).</code> |
| <code>ERR-02296</code> | <code>ERR_QP_INTERPOLATION_ONE_BETWEEN</code> | <code>Interpolation requires only one BETWEEN expression.</code> |
| <code>ERR-02297</code> | <code>ERR_QP_BETWEEN_HAS_INVALID_EXPR</code> | <code>BETWEEN has invalid expression (%s).</code> |
| <code>ERR-02298</code> | <code>ERR_QP_NOT_FACTOR_OF_INTERPOLATION_INTERVAL</code> | <code>FREQUENCE must be a factor of INTERPOLATION_INTERVAL (%lld).</code> |
| <code>ERR-02299</code> | <code>ERR_QP_ONLY_BETWEEN_SUPPORTED</code> | <code>Only BETWEEN condition is supported.</code> |
| <code>ERR-02300</code> | <code>ERR_QP_INSUFFICIENT_COLUMN_FOR_INTERPOLATION</code> | <code>Interpolation column is missing. (%s)</code> |
| <code>ERR-02301</code> | <code>ERR_QP_INSUFFICIENT_PROPERTIES_FOR_INTERPOLATION</code> | <code>Some properties are missing for interpolation.</code> |
| <code>ERR-02302</code> | <code>ERR_QP_INVALID_INTERVAL_INTERPOLATION_PROPERTY</code> | <code>Invalid interpolation interval property: %lld.</code> |
| <code>ERR-02303</code> | <code>ERR_QP_INVALID_ROLLUP_UNIT</code> | <code>You must use higher ROLLUP unit.</code> |
| <code>ERR-02304</code> | <code>ERR_QP_INTERPOLATION_VIEW_LIMIT</code> | <code>Interpolation is not applicable on (%s).</code> |
| <code>ERR-02305</code> | <code>ERR_QP_INTERPOLATION_ONE_TARGET</code> | <code>JOIN is not applicable for interpolation.</code> |
| <code>ERR-02306</code> | <code>ERR_QP_CHEKPOINT_INVALID_SIZE</code> | <code>Interpolation interval value(%lld) should be less than checkpoint interval value(%lld).</code> |
| <code>ERR-02307</code> | <code>ERR_QP_ROLLUPUNIT_INTERVALVALUE</code> | <code>Interpolation interval value(%lld) should be less than ROLLUP unit (%s).</code> |
| <code>ERR-02308</code> | <code>ERR_QP_ROLLUPUNIT_CHECKPOINTVALUE</code> | <code>Checkpoint interval value(%lld) should be less than ROLLUP unit (%s).</code> |
| <code>ERR-02309</code> | <code>ERR_QP_INVALID_INTERPOLATION_DIVIDE</code> | <code>Checkpoint interval value(%lld) should be divide by interpolation value(%lld).</code> |
| <code>ERR-02310</code> | <code>ERR_QP_INVALID_CHECKPOINT_INTERPOLATION_PROPERTY</code> | <code>Invalid interpolation checkpoint property: %lld.</code> |
| <code>ERR-02311</code> | <code>ERR_QP_INVALID_KEYWORD_INTERPOLATION</code> | <code>%s cannot be used in interpolation query.</code> |
| <code>ERR-02312</code> | <code>ERR_QP_NOT_INTERPOLATION_TABLE</code> | <code>Rollup delete can only be done on the Interpolation Tag table.</code> |
| <code>ERR-02313</code> | <code>ERR_QP_ROLLUP_REBUILD_RANGE_ERROR</code> | <code>Unable to execute ROLLUP DELETE with the given range.</code> |
| <code>ERR-02314</code> | <code>ERR_QP_TAG_UNSUPPORT_DURATION_BACKUP</code> | <code>Regular duration backup does not support a backup of the TAG table (Try incremental backup which permits the action on the TAG table).</code> |
| <code>ERR-02315</code> | <code>ERR_QP_FOG_SNAPSHOT_NOT_SUPPORTED</code> | <code>Snapshot is not supported.</code> |
| <code>ERR-02316</code> | <code>ERR_QP_INVALID_EXPR_IN_DURATION</code> | <code>Invalid expression in DURATION clause: %.&#42;s</code> |
| <code>ERR-02317</code> | <code>ERR_QP_FUNCTION_EXECUTION</code> | <code>Function execution failed: %s</code> |
| <code>ERR-02318</code> | <code>ERR_QP_LOOKUP_NODE_CONNECT_FAIL</code> | <code>Cannot connect to the lookup node.</code> |
| <code>ERR-02319</code> | <code>ERR_QP_LOOKUP_NODE_ERROR</code> | <code>Error on Lookup Node</code> |
| <code>ERR-02320</code> | <code>ERR_QP_LOOKUP_NODE_PENDING</code> | <code>Lookup Node is not ready</code> |
| <code>ERR-02321</code> | <code>ERR_QP_LOOKUP_NODE_NIL</code> | <code>No data was found in the lookup node.</code> |
| <code>ERR-02322</code> | <code>ERR_QP_LOOKUP_TABLE_MISSING_PRIMARY_KEY</code> | <code>Mandatory column definition (PRIMARY KEY) is missing.</code> |
| <code>ERR-02323</code> | <code>ERR_QP_EXEC_FUNCTION_NOT_SUPPORTED_TABLE_TYPE</code> | <code>EXEC %s is not supported for %s table type.</code> |
| <code>ERR-02324</code> | <code>ERR_QP_USED_TAG_ID_DATA</code> | <code>Cannot delete tagmeta. there exist data with deleted_tag key.</code> |
| <code>ERR-02325</code> | <code>ERR_QP_INTEGER_OVERFLOW</code> | <code>Integer %s type overflow.</code> |
| <code>ERR-02326</code> | <code>ERR_QP_EDGE_BACKUP_MOUNT_NOT_SUPPORTED</code> | <code>Backup/Mount is not supported.</code> |
| <code>ERR-02327</code> | <code>ERR_QP_PIVOT_IN_ROLLUP_NOT_SUPPORTED</code> | <code>Pivot is not supported in rollup query.</code> |
| <code>ERR-02328</code> | <code>ERR_QP_TAGMETA_INSERT_COUNT_EXCEEDED</code> | <code>Cannot insert a new tag since the number of tags has exceeded MAX_TAG_COUNT(%lld).</code> |
| <code>ERR-02329</code> | <code>ERR_QP_TAGMETA_INSERT_COUNT_EXCEEDED_LIMIT</code> | <code>Cannot insert a new tag since the number of tags has exceeded TAG_COUNT_LIMIT(%lld).</code> |
| <code>ERR-02330</code> | <code>ERR_QP_KV_INSUFFICIENT_MANDATORY</code> | <code>Mandatory column definition (ULONG / DATETIME) is missing.</code> |
| <code>ERR-02331</code> | <code>ERR_QP_RANGE_EXPR</code> | <code>RANGE expression is not applicable on the table (%s).</code> |
| <code>ERR-02332</code> | <code>ERR_QP_UNABLE_CREATE_INDEX_ON_COLUMN</code> | <code>Unable to create an index on the column (%s).</code> |
| <code>ERR-02333</code> | <code>ERR_QP_KV_TABLE_PREDICATE_MAX_OVER</code> | <code>Column (%s) cannot exceed %d.</code> |
| <code>ERR-02334</code> | <code>ERR_QP_TAG_INDEX_NOT_YET_SUPPORTED</code> | <code>Tag Index is not yet supported.</code> |
| <code>ERR-02335</code> | <code>ERR_QP_FAILED_TO_DELETE_ALL</code> | <code>Failed to delete all on this table. It is recommended to use EXEC TABLE_REFRESH(%s).</code> |
| <code>ERR-02336</code> | <code>ERR_QP_CASCADE_ONLY_TAG_TABLE</code> | <code>CASCADE option is not applicable on %s.</code> |
| <code>ERR-02337</code> | <code>ERR_QP_TAGMETA_DUPLICATE_FLAG</code> | <code>Unable to define more than one column attribute (%s).</code> |
| <code>ERR-02339</code> | <code>ERR_QP_TAGMETA_DIFFERENT_SUMMARY_TYPE</code> | <code>The type of %s column (%s) is different from that of VALUE column (%s).</code> |
| <code>ERR-02340</code> | <code>ERR_QP_TAGMETA_NOT_FOUND_SUMMARY_VALUE</code> | <code>SUMMARIZED column does not exist for %s.</code> |
| <code>ERR-02341</code> | <code>ERR_QP_SUMMARY_GREATER_THAN_USL</code> | <code>SUMMARIZED value is greater than UPPER LIMIT.</code> |
| <code>ERR-02342</code> | <code>ERR_QP_SUMMARY_LESS_THAN_LSL</code> | <code>SUMMARIZED value is less than LOWER LIMIT.</code> |
| <code>ERR-02343</code> | <code>ERR_QP_LSL_GREATER_THAN_USL</code> | <code>LOWER LIMIT must not be greater than UPPER LIMIT.</code> |
| <code>ERR-02344</code> | <code>ERR_QP_NOT_NUMERIC_TYPE</code> | <code>Not numeric type. (%s)</code> |
| <code>ERR-02345</code> | <code>ERR_QP_INVALID_TAGMETA_FLAG_ON_OTHER_TABLE</code> | <code>Column flag (%s) is only allowed for TAGMETA table.</code> |
| <code>ERR-02346</code> | <code>ERR_QP_DEFAULT_ONLY_FOR_TYPE_DATETIME</code> | <code>Column type (%s) is not allowed for default value.</code> |
| <code>ERR-02347</code> | <code>ERR_QP_DEFAULT_ONLY_FOR_FLAG_SYSDATE</code> | <code>SYSDATE is only allowed for default value.</code> |
| <code>ERR-02348</code> | <code>ERR_QP_ALTER_SET_PROP_NOT_SUPPORT_ON_CLUSTER</code> | <code>Alter table set %s not support on cluster.</code> |
| <code>ERR-02349</code> | <code>ERR_QP_BIND_VARIABLE_NOT_SUPPORTED_NEW_TAG</code> | <code>Bind variable is not supported for new tag.</code> |
| <code>ERR-02350</code> | <code>ERR_QP_WINDOW_FUNCTION_OVER_EXISTS</code> | <code>The function (%s) requires OVER clause.</code> |
| <code>ERR-02351</code> | <code>ERR_QP_NO_WINDOW_CONTEXT</code> | <code>Window function is allowed only in SELECT list.</code> |
| <code>ERR-02352</code> | <code>ERR_QP_FUNCTION_OVER</code> | <code>OVER clause is not applicable on (%s).</code> |
| <code>ERR-02353</code> | <code>ERR_QP_OVER_INVALID_TYPE</code> | <code>Invalid data type (%s) in OVER clause.</code> |
| <code>ERR-02354</code> | <code>ERR_QP_OVER_CONSTANT</code> | <code>Constant is not allowed in OVER clause.</code> |
| <code>ERR-02355</code> | <code>ERR_QP_TYPE_UNSUPPORTED</code> | <code>Type (%s) is not supported.</code> |
| <code>ERR-02356</code> | <code>ERR_QP_FIRST_DAY_OF_THE_MONTH</code> | <code>Origin must be the first day of the month.</code> |
| <code>ERR-02357</code> | <code>ERR_QP_JOIN_NOT_APPLICABLE</code> | <code>JOIN is not applicable on the table (%s).</code> |
| <code>ERR-02358</code> | <code>ERR_QP_INVALID_METADATA_ALTER_TABLE</code> | <code>When altering a table, the METADATA keyword is only applied to the tag table.</code> |
| <code>ERR-02359</code> | <code>ERR_QP_TAG_TABLE_ONLY_META_CHANGE</code> | <code>Tag table (%s) can only be modified in the metadata area.</code> |
| <code>ERR-02360</code> | <code>ERR_QP_WINDOW_FUNCTION_NOT_ALLOWED</code> | <code>Window function is not allowed with %s.</code> |
| <code>ERR-02361</code> | <code>ERR_QP_TABLE_STRUCTURE_MODIFIED</code> | <code>Table (%d) structure was modified.</code> |
| <code>ERR-02362</code> | <code>ERR_QP_STATEMENT_NOT_SUPPORTED</code> | <code>This statement is not supported.</code> |
| <code>ERR-02600</code> | <code>ERR_QP_WRONG_SEQUENCE_TABLE_TYPE</code> | <code>SEQUENCE property is not applicable in the table.</code> |
| <code>ERR-02601</code> | <code>ERR_QP_INVALID_FUNCTION_IN_SEQUENCE_COLUMN</code> | <code>Invalid function in a SEQUENCE column. NEXTVAL must be used.</code> |
| <code>ERR-02602</code> | <code>ERR_QP_INVALID_NEXTVAL_FUNCTION_QUERY</code> | <code>NEXTVAL is applicable only in INSERT statement.</code> |
| <code>ERR-02603</code> | <code>ERR_QP_INVALID_COLUMN_NEXTVAL</code> | <code>NEXTVAL is applicable only in SEQUENCE columns.</code> |
| <code>ERR-02604</code> | <code>ERR_QP_INVALID_SEQUENCE_COLUMN_DATA_TYPE</code> | <code>Sequence column must be LONG type.</code> |
| <code>ERR-02651</code> | <code>ERR_QP_EXIST_DEPENDENT_ROLLUP_TABLE</code> | <code>Dependent ROLLUP (%s) exists.</code> |
| <code>ERR-02652</code> | <code>ERR_QP_NOT_ROLLUP_TABLE</code> | <code>Not a ROLLUP table. (%s)</code> |
| <code>ERR-02653</code> | <code>ERR_QP_ROLLUP_INTERVAL_GREATER_THAN_SRC_ROLLUP</code> | <code>Rollup interval must be greater than source rollup interval.</code> |
| <code>ERR-02654</code> | <code>ERR_QP_ROLLUP_NOT_FOUND</code> | <code>ROLLUP (%s) is not found.</code> |
| <code>ERR-02655</code> | <code>ERR_QP_ROLLUP_INTERVAL_DIVIDE_REMAINDER_ZERO</code> | <code>Rollup interval source rollup interval Must Divide Zero.</code> |
| <code>ERR-02656</code> | <code>ERR_QP_ROLLUP_INTERVAL_POSITIVE_INTEGER</code> | <code>Rollup interval must positive integer.</code> |
| <code>ERR-02657</code> | <code>ERR_QP_ROLLUP_INTERVAL_SMALLER_THAN_YEAR</code> | <code>Rollup interval must be smaller than year.</code> |
| <code>ERR-02658</code> | <code>ERR_QP_ROLLUP_NOT_ENABLE</code> | <code>ROLLUP is not enabled for %s.</code> |
| <code>ERR-02659</code> | <code>ERR_QP_ROLLUP_MAX_COUNT</code> | <code>Rollup maximum count is 100.</code> |
| <code>ERR-02670</code> | <code>ERR_QP_ROLLUP_SOURCE_USERID</code> | <code>Rollup user ID(%d) is not equal to Source user ID(%d)</code> |
| <code>ERR-02671</code> | <code>ERR_QP_ROLLUP_COLUMN_INVALID_TYPE</code> | <code>Invalid type for ROLLUP column (%s).</code> |
| <code>ERR-02672</code> | <code>ERR_QP_ROLLUP_JSON_PATH_NOT_EXISTS</code> | <code>Json path is not specified on %s.</code> |
| <code>ERR-02673</code> | <code>ERR_QP_ROLLUP_JSON_PATH_EXISTS</code> | <code>Json path is not applicable on %s.</code> |
| <code>ERR-02674</code> | <code>ERR_QP_ROLLUP_NOT_FOUND_COLUMN</code> | <code>ROLLUP query must have a target column.</code> |
| <code>ERR-02675</code> | <code>ERR_QP_CAN_SCAN_ONE_ROLLUP_COLUMN</code> | <code>Cannot use more than one ROLLUP column in a ROLLUP query.</code> |
| <code>ERR-02676</code> | <code>ERR_QP_NOT_TAG_TABLE</code> | <code>Not a TAG table.</code> |
| <code>ERR-02677</code> | <code>ERR_QP_INVALID_ROLLUP_TIME_UNIT</code> | <code>Invalid rollup time unit (%s).</code> |
| <code>ERR-02678</code> | <code>ERR_QP_NEED_SUMMARIZED_COLUMN</code> | <code>WITH ROLLUP requires a SUMMARIZED column.</code> |
| <code>ERR-02679</code> | <code>ERR_QP_AUTO_GENERATE_ROLLUP_FAIL</code> | <code>Failed to create ROLLUP by WITH ROLLUP option.</code> |
| <code>ERR-02680</code> | <code>ERR_QP_PROCESS_ALREADY_START</code> | <code>PROCESS %s (%s) is already started.</code> |
| <code>ERR-02681</code> | <code>ERR_QP_PROCESS_ALREADY_STOP</code> | <code>PROCESS %s (%s) is already stopped.</code> |
| <code>ERR-02682</code> | <code>ERR_QP_ROLLUP_EXT_TYPE_DIFFER</code> | <code>ROLLUP extension type is different.</code> |
| <code>ERR-02683</code> | <code>ERR_QP_TAGDATA_SCAN_OTHER_TIME_COLUMN_IN_ROLLUP</code> | <code>Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP time column.</code> |
| <code>ERR-02684</code> | <code>ERR_QP_NOT_EXIST_DEPENDENT_ROLLUP_TABLE</code> | <code>Dependent ROLLUP table does not exist.</code> |
| <code>ERR-02685</code> | <code>ERR_QP_NO_APPLICABLE_ROLLUP_TABLE</code> | <code>There are no applicable ROLLUP tables.</code> |
| <code>ERR-02686</code> | <code>ERR_QP_RENAME_NO_APPLICABLE_ROLLUP_TABLE</code> | <code>The names of column(%s) associated with ROLLUP cannot be changed.</code> |
| <code>ERR-02687</code> | <code>ERR_QP_ROLLUP_WAKEUP_INTERVAL_SMALLER_THAN_SRC_ROLLUP</code> | <code>Rollup wakeup interval must be same or smaller than rollup interval.</code> |
| <code>ERR-02688</code> | <code>ERR_QP_ROLLUP_WAKEUP_INTERVAL_DIVIDE_REMAINDER_ZERO</code> | <code>Rollup wakeup interval must exactly divide the rollup interval.</code> |
| <code>ERR-02689</code> | <code>ERR_QP_CUSTOM_ROLLUP_FROM_ALIAS_NOT_ALLOWED</code> | <code>Cannot use alias in custom ROLLUP SELECT FROM clause.</code> |
| <code>ERR-02690</code> | <code>ERR_QP_CUSTOM_ROLLUP_OWNER_MISMATCH</code> | <code>Custom ROLLUP source and destination table owners must be same. (source:%s, destination:%s)</code> |
| <code>ERR-02691</code> | <code>ERR_QP_INDEX_TABLE_OWNER_MISMATCH</code> | <code>Index owner and table owner must be same. (index owner:%s, table owner:%s)</code> |
| <code>ERR-02692</code> | <code>ERR_QP_CIRCULAR_VIEW_DEFINITION</code> | <code>Circular view definition is not allowed: (%s).</code> |
| <code>ERR-02700</code> | <code>ERR_QP_DUPLICATE_RETENTION</code> | <code>Policy (%s) already exists.</code> |
| <code>ERR-02701</code> | <code>ERR_QP_NOT_EXISTS_RETENTION</code> | <code>Policy (%s) does not exist.</code> |
| <code>ERR-02702</code> | <code>ERR_QP_EXIST_DEPENDENT_RETENTION_TABLE</code> | <code>Policy (%s) is in use.</code> |
| <code>ERR-02703</code> | <code>ERR_QP_NOT_EXISTS_RETENTIONJOB</code> | <code>Table (%s) has no retention policy.</code> |
| <code>ERR-02704</code> | <code>ERR_QP_DUPLICATE_RETENTIONJOB</code> | <code>Table (%s) already has a retention policy.</code> |
| <code>ERR-02705</code> | <code>ERR_QP_RETENTION_DURATION_RANGE</code> | <code>Retention duration must be longer than 1 day.</code> |
| <code>ERR-02706</code> | <code>ERR_QP_RETENTION_INTERVAL_RANGE</code> | <code>Retention interval must be longer than 1 hour.</code> |
| <code>ERR-02707</code> | <code>ERR_QP_RETENTION_TABLE_TYPE</code> | <code>Retention is not applicable on the table (%s).</code> |
| <code>ERR-02708</code> | <code>ERR_QP_RETENTION_PRIVILEGE</code> | <code>Only SYS user can create or drop RETENTION.</code> |
| <code>ERR-02813</code> | <code>ERR_QP_INVALID_ROLLUP_EXPR</code> | <code>Invalid ROLLUP expression. (Token = %s, Unit = %ld)</code> |
| <code>ERR-02814</code> | <code>ERR_QP_INVALID_ROLLUP_TARGET</code> | <code>Invalid ROLLUP target. BASETIME column of TAGDATA table is the only target.</code> |
| <code>ERR-02815</code> | <code>ERR_QP_DIFFERENT_ROLLUP_EXPR</code> | <code>Different ROLLUP expressions are used in a single SELECT query.</code> |
| <code>ERR-02816</code> | <code>ERR_QP_INVALID_USE_IN_ROLLUP</code> | <code>Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.</code> |
| <code>ERR-02817</code> | <code>ERR_QP_INVALID_ROLLUP_NOT_SELECT</code> | <code>ROLLUP expression must be used in SELECT query.</code> |
| <code>ERR-02818</code> | <code>ERR_QP_UNSUPPORT_ROLLUP_TARGET</code> | <code>Invalid ROLLUP target (%s).</code> |
| <code>ERR-02819</code> | <code>ERR_QP_ROLLUP_RUNNING</code> | <code>ROLLUP thread is running.</code> |
| <code>ERR-02820</code> | <code>ERR_QP_ROLLUP_NOT_RUNNING</code> | <code>ROLLUP thread is not running.</code> |
| <code>ERR-02821</code> | <code>ERR_QP_OPERATION_IN_PROGRESS</code> | <code>Another DDL/DELETE/SNAPSHOT is in progress.</code> |
| <code>ERR-02822</code> | <code>ERR_QP_INVALID_EXPRESSION_IN_ROLLUP_QUERY</code> | <code>Invalid expression in ROLLUP query : %.&#42;s</code> |
| <code>ERR-02823</code> | <code>ERR_QP_ROLLUP_SELECT_FROM</code> | <code>Invalid table in ROLLUP query: %s</code> |
| <code>ERR-02824</code> | <code>ERR_QP_CUSTOM_ROLLUP_FIRST_COLUMN_NOT_TAGNAME</code> | <code>In custom ROLLUP SELECT, first column must be TAG key column (%s).</code> |
| <code>ERR-02825</code> | <code>ERR_QP_INVALID_EXTENDED_COLUMN_ROLLUP_QUERY</code> | <code>Extended column(%s) cannot be used in ROLLUP query.</code> |
| <code>ERR-02826</code> | <code>ERR_QP_CANT_REVOKE</code> | <code>User (%s) can&#x27;t revoke from table (%s.%s).</code> |
| <code>ERR-02827</code> | <code>ERR_QP_USER_NO_GRANT_PRIV</code> | <code>User does not have grant privileges.</code> |
| <code>ERR-02828</code> | <code>ERR_QP_USER_NO_REVOKE_PRIV</code> | <code>User does not have revoke privileges.</code> |
| <code>ERR-02829</code> | <code>ERR_QP_USER_ONLY_SYS_CAN_DO_CREATE_DROP</code> | <code>Only SYS user can create or drop user.</code> |
| <code>ERR-02830</code> | <code>ERR_QP_USER_NO_PRIV_TABLE_FOR_EACH_CASE</code> | <code>The user does not have (%s) privilege on table(%s.%s).</code> |
| <code>ERR-02831</code> | <code>ERR_QP_USER_NO_GRANT_UPDATE_PRIV_FOR_LOG_TABLE</code> | <code>You can&#x27;t grant UPDATE privilege on Log Table.</code> |
| <code>ERR-02832</code> | <code>ERR_QP_USER_NO_REVOKE_UPDATE_PRIV_FOR_LOG_TABLE</code> | <code>You can&#x27;t revoke UPDATE privilege on Log Table.</code> |
| <code>ERR-02833</code> | <code>ERR_QP_USER_SELECT_ONLY_FOR_MOUNT_TABLE</code> | <code>You can only grant SELECT privileges on Mounted database.</code> |
| <code>ERR-02834</code> | <code>ERR_QP_PASSWORD_REUSED</code> | <code>Cannot use new password as previously used.</code> |
| <code>ERR-02835</code> | <code>ERR_QP_USER_NO_PRIV_DATABASE_FOR_EACH_CASE</code> | <code>The user does not have (%s) privilege on database(%s).</code> |
| <code>ERR-02837</code> | <code>ERR_QP_CUSTOM_ROLLUP_NOT_SUPPORTED_IN_CLUSTER</code> | <code>Custom rollup is not supported in cluster edition.</code> |
| <code>ERR-02838</code> | <code>ERR_QP_USER_NO_MOUNT_PRIV</code> | <code>The user(%s) does not have mount privileges.</code> |
| <code>ERR-02839</code> | <code>ERR_QP_DATABASE_NOT_FOUND</code> | <code>Database (%s) does not exist.</code> |
| <code>ERR-02840</code> | <code>ERR_QP_DATABASE_NOT_ACTIVE</code> | <code>Database (%s) is not an active database.</code> |
| <code>ERR-02841</code> | <code>ERR_QP_DATABASE_USE_IN_TRANSACTION</code> | <code>Cannot change the current database while a transaction is active.</code> |
| <code>ERR-02842</code> | <code>ERR_QP_DATABASE_ALREADY_EXISTS</code> | <code>Database (%s) already exists.</code> |
| <code>ERR-02843</code> | <code>ERR_QP_DATABASE_SELF_DROP</code> | <code>Cannot drop current database (%s).</code> |
| <code>ERR-02844</code> | <code>ERR_QP_DATABASE_DEFAULT_DROP</code> | <code>Default database (%s) cannot be dropped.</code> |
| <code>ERR-02845</code> | <code>ERR_QP_DATABASE_READ_ONLY</code> | <code>Database (%s) is read only.</code> |
| <code>ERR-02846</code> | <code>ERR_QP_DATABASE_RESERVED_NAME</code> | <code>Database name (%s) is reserved and cannot be used.</code> |
| <code>ERR-02847</code> | <code>ERR_QP_PREPARED_CATALOG_CHANGED</code> | <code>Prepared statement target database (%s) changed.</code> |

### `ERR-03000`–`ERR-03999` (65)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-03000</code> | <code>MMP_STMT_OVERFLOWS</code> | <code>Statement ID overflow (Limit = %u, Curr = %u).</code> |
| <code>ERR-03001</code> | <code>MMP_STMT_QUERY_ZERO</code> | <code>Statement query length is zero.</code> |
| <code>ERR-03002</code> | <code>MMT_TASK_POOL_INITIALIZE_ERROR</code> | <code>Task pool initialization error.</code> |
| <code>ERR-03003</code> | <code>MMS_STMT_POOL_INITIALIZE_ERROR</code> | <code>Statement pool initialization error.</code> |
| <code>ERR-03004</code> | <code>MMT_QUEUE_CREATE_ERROR</code> | <code>Queue creation error.</code> |
| <code>ERR-03005</code> | <code>MMS_STMT_ALLOC_ERROR</code> | <code>Statement allocation error.</code> |
| <code>ERR-03006</code> | <code>MMP_META_UNKNOWN_TYPE_ERROR</code> | <code>Unknown meta type error (typecode is %u). Internal error.</code> |
| <code>ERR-03007</code> | <code>MMP_PROTOCOL_BUFFER_INSUFFICIENT</code> | <code>Insufficient protocol buffer size. Increase it.</code> |
| <code>ERR-03008</code> | <code>MMP_PROTOCOL_STATE_INVALID</code> | <code>Invalid protocol state. Check your application again. (Protocol = %s, State = %s)</code> |
| <code>ERR-03009</code> | <code>MMP_EXECUTE_PROTOCOL_DATA_INVALID</code> | <code>Invalid execute protocol data (%s).</code> |
| <code>ERR-03010</code> | <code>MMS_FETCH_PROTOCOL_INSUFFICIENT</code> | <code>Error in fetch protocol: not enough buffer size to execute it. Increase the size.</code> |
| <code>ERR-03011</code> | <code>MMP_SEND_ERROR</code> | <code>Send error.</code> |
| <code>ERR-03012</code> | <code>MMP_MEMORY_ALLOC_ERROR</code> | <code>Memory allocation error.</code> |
| <code>ERR-03013</code> | <code>MMP_STMT_APPEND_TABLE_ZERO</code> | <code>Invalid table name for append table. Table name is omitted.</code> |
| <code>ERR-03014</code> | <code>MMP_APPEND_PROTOCOL_DATA_INVALID</code> | <code>Invalid append protocol data (%s).</code> |
| <code>ERR-03015</code> | <code>MMP_STMT_APPEND_NO_ENDIAN</code> | <code>Endian is not specified for append. Check endian information.</code> |
| <code>ERR-03016</code> | <code>MMP_STMT_APPEND_MAX_COLUMN</code> | <code>Too many columns are specified for append. Cannot append more than %d columns</code> |
| <code>ERR-03017</code> | <code>MMP_STMT_APPEND_MAX_RECORD_SIZE</code> | <code>Too large record size for append. Cannot append more than %d bytes per record.</code> |
| <code>ERR-03018</code> | <code>MMP_STMT_APPEND_MAX_BLOCK_SIZE</code> | <code>The specified maximum block size (%d) was exceeded. Check the application&#x27;s append data structure.</code> |
| <code>ERR-03019</code> | <code>MMP_STMT_EXPLAIN_PLAN_ERROR</code> | <code>Explain plan error. Use it for SELECT statement only.</code> |
| <code>ERR-03020</code> | <code>MMP_STMT_EXPLAIN_ONLY_DIRECT_EXECUTE</code> | <code>Explain plan is not allowed in prepared mode.</code> |
| <code>ERR-03021</code> | <code>MMP_CONNECT_VERSION_MISMATCHED</code> | <code>Protocol versions do not match: server (%d.%d.%d), client (%d.%d.%d).</code> |
| <code>ERR-03022</code> | <code>MMP_OS_GET_HANDLE_LIMIT_ERROR</code> | <code>Failed to get handle limit from the system.</code> |
| <code>ERR-03023</code> | <code>MMP_OS_CHECK_HANDLE_LIMIT_ERROR</code> | <code>Handle limit(%d) from the system is less than that of property(%d). Tune system handle limit or decrease the property &#x27;HANDLE_LIMIT&#x27;</code> |
| <code>ERR-03024</code> | <code>ERR_MM_SESSION_ID_NOT_FOUND</code> | <code>Invalid session ID (%llu).</code> |
| <code>ERR-03025</code> | <code>ERR_MM_SESSION_SELF_OP_ERROR</code> | <code>Not enough privileges to manipulate the session. (%llu)</code> |
| <code>ERR-03026</code> | <code>ERR_MM_SESSION_DIFF_USER_CANCEL</code> | <code>You should log in with the same user name in the target session. Now (%d) Target(%d)</code> |
| <code>ERR-03027</code> | <code>ERR_MM_SESSION_CANCELLED</code> | <code>This statement has been canceled.</code> |
| <code>ERR-03028</code> | <code>ERR_MM_NO_SESSION_PROPETY</code> | <code>Invalid session property name. Name (%s) does not exist.</code> |
| <code>ERR-03029</code> | <code>ERR_MM_SESSION_PROPETY_CONVERT</code> | <code>Error in converting session property (%s). Cannot convert string (%s) to integer.</code> |
| <code>ERR-03030</code> | <code>ERR_MM_SESSION_PROPETY_VALUE_RANGE</code> | <code>Invalid session property value. Check the session value (%s)</code> |
| <code>ERR-03031</code> | <code>ERR_MM_PROTOCOL_BROKEN</code> | <code>Protocol error.</code> |
| <code>ERR-03032</code> | <code>ERR_MM_LICENSE_NO_META</code> | <code>Error in getting license meta. Check DB image and binary.</code> |
| <code>ERR-03033</code> | <code>ERR_MM_LICENSE_OPEN_META</code> | <code>Error in opening meta.</code> |
| <code>ERR-03034</code> | <code>ERR_MM_LICENSE_EXEC_META</code> | <code>Error in executing meta.</code> |
| <code>ERR-03035</code> | <code>ERR_MM_LICENSE_CLOSE_META</code> | <code>Error in closing meta.</code> |
| <code>ERR-03036</code> | <code>ERR_MM_LICENSE_EXPIRED</code> | <code>The license is expired(%s).</code> |
| <code>ERR-03037</code> | <code>ERR_MM_LICENSE_INVALID</code> | <code>The license is invalid or the license file does not exist(%s).</code> |
| <code>ERR-03038</code> | <code>ERR_MM_LICENSE_VIOLATION</code> | <code>License violation detected (%s). contact sales@machbase.com</code> |
| <code>ERR-03039</code> | <code>ERR_MM_SESSION_COUNT_EXCEED</code> | <code>Session count exceeded the maximum (%llu).</code> |
| <code>ERR-03040</code> | <code>ERR_MM_SHUTDOWN_FAIL</code> | <code>Unable to shutdown since the server is busy.</code> |
| <code>ERR-03041</code> | <code>ERR_MM_APPEND_BATCH</code> | <code>AppendBatch error: %s.</code> |
| <code>ERR-03042</code> | <code>ERR_MM_RECOVERY_BEGUN</code> | <code>Recovery in progress.</code> |
| <code>ERR-03043</code> | <code>ERR_MM_EXECARRAY_NOT_FOR_SELECT</code> | <code>Array Execute is not applicable for SELECT query.</code> |
| <code>ERR-03044</code> | <code>MMP_CONNECT_WRONG_TIMEZONE</code> | <code>Invalid TIMEZONE string: %s.</code> |
| <code>ERR-03045</code> | <code>ERR_MM_INVALID_CONTEXT</code> | <code>Invalid context at %s.</code> |
| <code>ERR-03046</code> | <code>ERR_MM_CM_ERROR</code> | <code>Communication module error (rc=%d): &#91;%s&#93;.</code> |
| <code>ERR-03047</code> | <code>ERR_MM_FUNCTION</code> | <code>Failed to call function %s (rc=%d)</code> |
| <code>ERR-03048</code> | <code>ERR_MM_PREPARED_STMT_USER_CHANGED</code> | <code>Prepared statement cannot be used after CONNECT USER.</code> |
| <code>ERR-03200</code> | <code>ERR_MM_SERVER_NOT_RUNNING</code> | <code>Server is not running.</code> |
| <code>ERR-03201</code> | <code>ERR_MM_INVALID_STMT_STATE</code> | <code>Invalid statement state: (%d)</code> |
| <code>ERR-03202</code> | <code>ERR_MM_COLUMN_RANGE</code> | <code>Column index is out of range.</code> |
| <code>ERR-03203</code> | <code>ERR_MM_BUFFER_SIZE_EXCEEDED</code> | <code>The data length exceeded the buffer size.</code> |
| <code>ERR-03204</code> | <code>ERR_MM_APPEND_PARAM_IP_STRING_NULL</code> | <code>Append data ip string is null.</code> |
| <code>ERR-03205</code> | <code>ERR_MM_APPEND_PARAM_DATETIME_STRING_NULL</code> | <code>Append data datetime string(%s) is null.</code> |
| <code>ERR-03206</code> | <code>ERR_MM_INVALID_COLUMN_TYPE</code> | <code>Invalid column type (%d).</code> |
| <code>ERR-03207</code> | <code>ERR_MM_INVALID_STMT_TYPE</code> | <code>Invalid statement type (%d).</code> |
| <code>ERR-03208</code> | <code>ERR_MM_SERVER_THREAD_ERR</code> | <code>Server thread error: %d - %s</code> |
| <code>ERR-03209</code> | <code>ERR_MM_BUSY_STMT_STATE</code> | <code>statement is busy. (%d)</code> |
| <code>ERR-03210</code> | <code>ERR_MM_CONN_INVALID_STATE</code> | <code>This connection already has been already disconnected</code> |
| <code>ERR-03211</code> | <code>ERR_MM_DB_EXIST</code> | <code>Database already exists.</code> |
| <code>ERR-03212</code> | <code>ERR_MM_DB_NOT_EXIST</code> | <code>Database does not exist.</code> |
| <code>ERR-03213</code> | <code>ERR_MM_SERVER_RUNNING</code> | <code>Server is running.</code> |
| <code>ERR-03214</code> | <code>ERR_MM_DBS_OPEN_FAIL</code> | <code>Failed to open dbs(%s) directory.</code> |
| <code>ERR-03215</code> | <code>ERR_MM_ALTER_SESSION</code> | <code>ALTER SESSION statement is not supported.</code> |

### `ERR-04000`–`ERR-04999` (23)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-04000</code> | <code>CMI_PROTOCOL_MSG_ERROR_IN_CONNECTION</code> | <code>Protocol message error in connection.</code> |
| <code>ERR-04001</code> | <code>CMI_PROTOCOL_LENGTH_ERROR_IN_CONNECTION</code> | <code>Protocol length error in connection (%llu but %llu).</code> |
| <code>ERR-04002</code> | <code>CMI_DOUBLE_CREATE_COMMUNICATION_CHANNEL</code> | <code>Cannot create duplicate communication channels.</code> |
| <code>ERR-04003</code> | <code>CMI_SOCKET_CREATION_ERROR</code> | <code>Socket creation error (%d).</code> |
| <code>ERR-04004</code> | <code>CMI_BIND_ERROR</code> | <code>Socket bind error. Errorcode is (%d)</code> |
| <code>ERR-04005</code> | <code>CMI_LISTEN_ERROR</code> | <code>Listen error (%d).</code> |
| <code>ERR-04006</code> | <code>CMI_POLL_CREATION_ERROR</code> | <code>Poll creation error (%d).</code> |
| <code>ERR-04007</code> | <code>CMI_POLL_ADD_ERROR</code> | <code>Poll add error (%d).</code> |
| <code>ERR-04008</code> | <code>CMI_CONNECTION_ERROR</code> | <code>Creation error (%d).</code> |
| <code>ERR-04009</code> | <code>CMI_SEND_ERROR</code> | <code>Send error (%d).</code> |
| <code>ERR-04010</code> | <code>CMI_RECV_ERROR</code> | <code>Receive error (%d).</code> |
| <code>ERR-04011</code> | <code>CMI_DISPATCH_ERROR</code> | <code>Dispatch error (%d).</code> |
| <code>ERR-04012</code> | <code>CMI_SETSOCKOPT_ERROR</code> | <code>nbp_sock_set_opt() error (%d).</code> |
| <code>ERR-04013</code> | <code>CMI_RECV_RETRY_ERROR</code> | <code>Failed to receive accept data repeatedly in %u milliseconds.</code> |
| <code>ERR-04014</code> | <code>CMI_MEMORY_ALLOC_ERROR</code> | <code>Memory allocation error.</code> |
| <code>ERR-04015</code> | <code>CMI_INVALID_PROTOCOL_ERROR</code> | <code>Receive invalid protocol (%d).</code> |
| <code>ERR-04016</code> | <code>CMI_TIMEDOUT_ERROR</code> | <code>Communication timed out error. (%d)</code> |
| <code>ERR-04017</code> | <code>CMI_SOCKET_CLOSED</code> | <code>Remote socket closed.</code> |
| <code>ERR-04018</code> | <code>CMI_INVALID_BIND_IP_ADDR</code> | <code>BIND_IP_ADDRESS &#91;%s&#93; is invalid</code> |
| <code>ERR-04019</code> | <code>CMI_BIND_ADDR_NOT_AVAILABLE</code> | <code>BIND_IP_ADDRESS &#91;%s&#93; is not available. Errorcode is&#91;%d&#93;</code> |
| <code>ERR-04020</code> | <code>CMI_BIND_PORT_INUSE</code> | <code>Port&#91;%d&#93; is already in use. Errorcode is &#91;%d&#93;</code> |
| <code>ERR-04021</code> | <code>CMI_OS_NOT_SUPPORT_FUNCTION</code> | <code>Function&#91;%s&#93; is not supported in this OS&#91;%s&#93;</code> |
| <code>ERR-04999</code> | <code>ERR_QP_ROLLUP_NOT_SUPPORTED_ON_DISTANCE_AXIS</code> | <code>ROLLUP is not supported on DISTANCE axis TAG table.</code> |

### `ERR-05000`–`ERR-05999` (1)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-05002</code> | <code>AD_MANAGER_GENERATE_ERROR</code> | <code>msg does not used</code> |

### `ERR-06000`–`ERR-06999` (35)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-06000</code> | <code>ERR_LM_FUNCTION_EXECUTION</code> | <code>Function execution failed: &quot;%s&quot;.</code> |
| <code>ERR-06001</code> | <code>ERR_LM_RESPONSE_FAILED</code> | <code>Response failed: %s</code> |
| <code>ERR-06002</code> | <code>ERR_LM_ACCEPT_TIMEOUT</code> | <code>Accept timeout: &quot;%s:%u&quot;.</code> |
| <code>ERR-06003</code> | <code>ERR_LM_SEND_BUFFER_OVERFLOW</code> | <code>Send buffer overflow: &quot;%s&quot;.</code> |
| <code>ERR-06004</code> | <code>ERR_LM_COMMAND_EXECUTION_FAILED</code> | <code>Command execution failed: Application-Id = %u, Command-Code = %u.</code> |
| <code>ERR-06005</code> | <code>ERR_LM_UNSUPPORTED_COMMAND</code> | <code>Unsupported command: Application-Id = %u, Command-Code = %u.</code> |
| <code>ERR-06006</code> | <code>ERR_LM_ALREADY_CONNECTED</code> | <code>Already connected: &quot;%s&quot;.</code> |
| <code>ERR-06007</code> | <code>ERR_LM_CSTR_TO_INT32_FAILED</code> | <code>Failed to convert string &quot;%s&quot; to int.</code> |
| <code>ERR-06008</code> | <code>ERR_LM_DESTINATION_HOST_TOO_LONG</code> | <code>Destination-Host too long: &quot;%s&quot;.</code> |
| <code>ERR-06009</code> | <code>ERR_LM_DISCONNECTED</code> | <code>Disconnected: &quot;%s&quot;.</code> |
| <code>ERR-06010</code> | <code>ERR_LM_HOST_NOT_FOUND</code> | <code>Host not found: &quot;%s&quot;.</code> |
| <code>ERR-06011</code> | <code>ERR_LM_GROUPED_AVP_TOO_DEEP</code> | <code>Grouped AVP too deep: %d.</code> |
| <code>ERR-06012</code> | <code>ERR_LM_HANDSHAKE_TIMEOUT</code> | <code>Handshake timeout: &quot;%s&quot;.</code> |
| <code>ERR-06013</code> | <code>ERR_LM_INITIALIZED</code> | <code>Link manager already initialized.</code> |
| <code>ERR-06014</code> | <code>ERR_LM_INVALID_HEADER</code> | <code>Invalid header: &quot;%s&quot;.</code> |
| <code>ERR-06015</code> | <code>ERR_LM_INVALID_HOST</code> | <code>Invalid host: &quot;%s&quot; and &quot;%s&quot;.</code> |
| <code>ERR-06016</code> | <code>ERR_LM_INVALID_PORT_NO</code> | <code>Invalid port no: %d.</code> |
| <code>ERR-06017</code> | <code>ERR_LM_MESSAGE_TOO_LONG</code> | <code>Message too long: %d</code> |
| <code>ERR-06018</code> | <code>ERR_LM_MISSING_AVP</code> | <code>Missing AVP: &quot;%s&quot;</code> |
| <code>ERR-06019</code> | <code>ERR_LM_NOT_INITIALIZED</code> | <code>Link manager not initialized.</code> |
| <code>ERR-06020</code> | <code>ERR_LM_NO_OPENED_GROUPED_AVP_FOUND</code> | <code>No opened grouped AVP found.</code> |
| <code>ERR-06021</code> | <code>ERR_LM_NULL_POINTER_ACCESS</code> | <code>NULL pointer access: &quot;%s&quot;.</code> |
| <code>ERR-06022</code> | <code>ERR_LM_ORIGIN_HOST_TOO_LONG</code> | <code>Origin-Host too long: &quot;%s&quot;.</code> |
| <code>ERR-06023</code> | <code>ERR_LM_REQUIRE_REQUEST_MESSAGE</code> | <code>Require request message.</code> |
| <code>ERR-06024</code> | <code>ERR_LM_SESSION_ID_TOO_LONG</code> | <code>Session-Id too long: &quot;%s&quot;.</code> |
| <code>ERR-06025</code> | <code>ERR_LM_CONNECTION_TIMEOUT</code> | <code>Connection timeout: &quot;%s&quot;.</code> |
| <code>ERR-06026</code> | <code>ERR_LM_UNABLE_TO_BIND_ADDRESS</code> | <code>Unable to bind address: &quot;%s&quot;.</code> |
| <code>ERR-06027</code> | <code>ERR_LM_ABORT_CALLBACK_TIMEOUT</code> | <code>Abort callback: &quot;Timeout&quot;.</code> |
| <code>ERR-06028</code> | <code>ERR_LM_ABORT_CALLBACK_DISCONNECTED</code> | <code>Abort callback: &quot;Disconnected&quot;.</code> |
| <code>ERR-06029</code> | <code>ERR_LM_ABORT_CALLBACK_SHUTDOWN</code> | <code>Abort callback: &quot;Shutdown&quot;.</code> |
| <code>ERR-06030</code> | <code>ERR_LM_NO_MORE_ADDRESS</code> | <code>No more address: &quot;%s&quot;.</code> |
| <code>ERR-06031</code> | <code>ERR_LM_HANDSHAKE_FAILED</code> | <code>Handshake failed: &quot;%s&quot;.</code> |
| <code>ERR-06032</code> | <code>ERR_LM_PROCESS_MEMORY_LIMIT</code> | <code>Failed to allocate connection (Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu)).</code> |
| <code>ERR-06033</code> | <code>ERR_LM_ABORT_CONN_FREED</code> | <code>connection object for (%s) has been freed. please retry.</code> |
| <code>ERR-06034</code> | <code>ERR_LM_ABORT_SEND_RETRY_COUNT_EXHAUSETED</code> | <code>The number of send repetitions has been exhausted.</code> |

### `ERR-07000`–`ERR-07999` (50)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-07000</code> | <code>ERR_XM_CREATE_HASH</code> | <code>Error in creating hashtable for global metadata.</code> |
| <code>ERR-07001</code> | <code>ERR_XM_OPEN_META</code> | <code>Error in opening meta. Cannot open meta database.</code> |
| <code>ERR-07002</code> | <code>ERR_XM_EXEC_META</code> | <code>Error in executing meta. Cannot execute meta database</code> |
| <code>ERR-07003</code> | <code>ERR_XM_CLOSE_META</code> | <code>Error in closing meta. Cannot close meta database.</code> |
| <code>ERR-07004</code> | <code>ERR_XM_FETCH_META</code> | <code>Error in fetching meta.</code> |
| <code>ERR-07005</code> | <code>ERR_XM_GLOB_OBJECT_NOT_EXISTS_BY_LOID</code> | <code>No global object found. (Local Object ID=%llu, Host=%s)</code> |
| <code>ERR-07006</code> | <code>ERR_XM_GLOB_OBJECT_NOT_EXISTS_BY_GOID</code> | <code>No global object found. (Global Object ID=%llu, Host=%s)</code> |
| <code>ERR-07007</code> | <code>ERR_XM_GLOB_OBJECT_EXISTS</code> | <code>Global object already exists. (Global Object ID=%llu, Host=%s)</code> |
| <code>ERR-07008</code> | <code>ERR_XM_HASH_ADD_FAILURE</code> | <code>Error in hash add (Memory allocation failed).</code> |
| <code>ERR-07009</code> | <code>ERR_XM_STATEMENT_ALREADY_EXISTS</code> | <code>Failed to add query statement due to unfinished one.</code> |
| <code>ERR-07010</code> | <code>ERR_XM_STATEMENT_NO_EXISTS</code> | <code>Failed to find query statement.</code> |
| <code>ERR-07011</code> | <code>ERR_XM_NOT_SUPPORTED_YET</code> | <code>This query type is not supported yet.</code> |
| <code>ERR-07012</code> | <code>ERR_XM_NOT_SUPPORTED_PLANNODE_YET</code> | <code>This plan node (%s) is not supported yet.</code> |
| <code>ERR-07013</code> | <code>ERR_XM_STATEMENT_CANCELLED</code> | <code>Statement is canceled by the broker.</code> |
| <code>ERR-07014</code> | <code>ERR_XM_NODE_INFO_EXISTS</code> | <code>Node information already exists.</code> |
| <code>ERR-07015</code> | <code>ERR_XM_INVALID_MESSAGE</code> | <code>Invalid message from XM: %u</code> |
| <code>ERR-07016</code> | <code>ERR_XM_DDL_ON_WAREHOUSE_NOT_SUPPORTED</code> | <code>DDL/DELETE statement on warehouse node is not supported.</code> |
| <code>ERR-07017</code> | <code>ERR_XM_NOT_SUPPORTED_AGG_FUNC_YET</code> | <code>This aggregate function (%s) is not supported yet.</code> |
| <code>ERR-07018</code> | <code>ERR_XM_STANDBY_INSERT</code> | <code>INSERT/APPEND to warehouse standby is not available.</code> |
| <code>ERR-07019</code> | <code>ERR_XM_UNSUPPORTED_STMT_TYPE</code> | <code>Unsupported query statement type in the Cluster Edition.</code> |
| <code>ERR-07020</code> | <code>ERR_XM_INTERNAL_ERROR</code> | <code>XM internal error (XMART_POINT:%s)</code> |
| <code>ERR-07021</code> | <code>ERR_XM_XMART_TARGET_NOT_NODE_ID</code> | <code>&#91;XM-ART&#93; Targeted node is not valid. (%s)</code> |
| <code>ERR-07022</code> | <code>ERR_XM_ERROR_VIA_ANSWER_MSG</code> | <code>An error occurred after processing a %s message. &#91;Src=&#x27;%s&#x27;&#93;: %s</code> |
| <code>ERR-07023</code> | <code>ERR_XM_ERROR_STAFF_ALREADY_GONE</code> | <code>Execution unit from remote note is already gone.</code> |
| <code>ERR-07024</code> | <code>ERR_XM_INVALID_APPEND_ON_WAREHOUSE</code> | <code>APPEND operation on warehouse node is not supported.</code> |
| <code>ERR-07025</code> | <code>ERR_XM_INVALID_NODE_HOSTS</code> | <code>Host information from broker is invalid. Please check coordinator&#x27;s status.</code> |
| <code>ERR-07026</code> | <code>ERR_XM_CLUSTER_INVALID</code> | <code>Cluster node information is invalid.</code> |
| <code>ERR-07027</code> | <code>ERR_XM_CLUSTER_CHANGED</code> | <code>Cluster node information has changed during query execution.</code> |
| <code>ERR-07028</code> | <code>ERR_XM_CANNOT_EXPLAIN_STAGE</code> | <code>This execution plan does not need to generate stage(s).</code> |
| <code>ERR-07029</code> | <code>ERR_XM_CLUSTER_CONNECTION_ABORT_TIMEOUT</code> | <code>Cluster connection aborted: Time-out</code> |
| <code>ERR-07030</code> | <code>ERR_XM_CLUSTER_CONNECTION_ABORT_LINK_BROKEN</code> | <code>Cluster connection aborted: Disconnected by warehouse.</code> |
| <code>ERR-07031</code> | <code>ERR_XM_BLOCKED_BY_DEACTIVATED_MODE</code> | <code>DML/DDL is disabled in DEACTIVATED mode.</code> |
| <code>ERR-07032</code> | <code>ERR_XM_DELETE_NOT_AVAILABLE</code> | <code>DELETE is not available since a read-only group exists.</code> |
| <code>ERR-07033</code> | <code>ERR_XM_WAREHOUSE_DROPPED_OUT</code> | <code>Participating warehouse has been dropped out.</code> |
| <code>ERR-07034</code> | <code>ERR_XM_INVALID_BROKER_STORED</code> | <code>Broker info has been changed. Please free statement and initalize again.</code> |
| <code>ERR-07035</code> | <code>ERR_XM_WAREHOUSE_DIRECT_DML_NOW_ALLOWED</code> | <code>Direct DML on warehouse is not allowed.</code> |
| <code>ERR-07036</code> | <code>ERR_XM_WAREHOUSE_NOT_AVAILABLE</code> | <code>Warehouse is not available.</code> |
| <code>ERR-07037</code> | <code>ERR_XM_STAGE_MEMORY_LIMIT</code> | <code>Execution stage memory usage exceeded the limit. (used: %llu, maximum: %llu)</code> |
| <code>ERR-07038</code> | <code>ERR_XM_ARCHIVE_INTERNAL_ERROR</code> | <code>XM archiving error occurred. (%s)</code> |
| <code>ERR-07039</code> | <code>ERR_XM_BROKER_DISCONN</code> | <code>Broker (%s) is disconnected.</code> |
| <code>ERR-07040</code> | <code>ERR_XM_BROKER_NOT_LEADER</code> | <code>Only leader broker can execute DML on LOOKUP table.</code> |
| <code>ERR-07041</code> | <code>ERR_XM_BROKER_REMOTE_ERROR</code> | <code>Remote error. (%s)</code> |
| <code>ERR-07042</code> | <code>ERR_XM_RESTORE_LOOKUP_TIMEOUT</code> | <code>LOOKUP table restore timeout: (%s)</code> |
| <code>ERR-07043</code> | <code>ERR_XM_BROKER_NOT_ACTIVE</code> | <code>Broker is not ACTIVE.</code> |
| <code>ERR-07044</code> | <code>ERR_XM_VERSION_NOT_MATCH</code> | <code>XM version does not match. (%s - %s)</code> |
| <code>ERR-07045</code> | <code>ERR_XM_SNAPSHOT_FAIL</code> | <code>Snapshot failed: %s.</code> |
| <code>ERR-07046</code> | <code>ERR_XM_MESSAGE_EXPIRED</code> | <code>Message %d is expired.</code> |
| <code>ERR-07047</code> | <code>ERR_XM_SNAPSHOT_RECOVER_IN_PROGRESS</code> | <code>Snapshot recover is in progress.</code> |
| <code>ERR-07048</code> | <code>ERR_XM_QUEUE_TIMEOUT</code> | <code>Queue timeout.</code> |
| <code>ERR-07049</code> | <code>ERR_XM_VERSION_UNMATCHED</code> | <code>XM version does not match. (%d - %d)</code> |

### `ERR-08000`–`ERR-08999` (109)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-08000</code> | <code>ERR_CC_FUNCTION_EXECUTION</code> | <code>Function execution failed: &quot;%s&quot;.</code> |
| <code>ERR-08001</code> | <code>ERR_CC_BUFFER_OVERRUN</code> | <code>Buffer overrun.</code> |
| <code>ERR-08002</code> | <code>ERR_CC_END_OF_FILE</code> | <code>End of file.</code> |
| <code>ERR-08003</code> | <code>ERR_CC_HEADER_OCCURS_TOO_MANY_TIMES</code> | <code>Header occurs too many times: &quot;%s&quot;.</code> |
| <code>ERR-08004</code> | <code>ERR_CC_JSON_DEPTH_OUT_OF_RANGE</code> | <code>JSON depth: Out of range.</code> |
| <code>ERR-08005</code> | <code>ERR_CC_CONNECTION_TIMEOUT</code> | <code>Connection timeout.</code> |
| <code>ERR-08006</code> | <code>ERR_CC_PACKAGE_NOT_FOUND</code> | <code>Package not found: &quot;%s&quot;.</code> |
| <code>ERR-08007</code> | <code>ERR_CC_FILE_NAME_MISMATCH</code> | <code>File name mismatch: &quot;%s&quot; and &quot;%s&quot;</code> |
| <code>ERR-08008</code> | <code>ERR_CC_BLOCK_SIZE_OVERRUN</code> | <code>Block size overrun: %llu and %llu</code> |
| <code>ERR-08009</code> | <code>ERR_CC_FILE_SIZE_MISMATCH</code> | <code>File size mismatch: %llu and %llu</code> |
| <code>ERR-08010</code> | <code>ERR_CC_FILE_READ_SIZE_MISMATCH</code> | <code>File read size mismatch: %llu and %llu</code> |
| <code>ERR-08011</code> | <code>ERR_CC_FILE_WRITE_SIZE_MISMATCH</code> | <code>File write size mismatch: %llu and %llu</code> |
| <code>ERR-08012</code> | <code>ERR_CC_NODE_NOT_FOUND</code> | <code>Node not found: &quot;%s&quot;</code> |
| <code>ERR-08013</code> | <code>ERR_CC_NODE_EXIST</code> | <code>Node exist: &quot;%s&quot;</code> |
| <code>ERR-08014</code> | <code>ERR_CC_INVALID_PACKAGE_FILE_SIZE</code> | <code>Invalid package file size: &quot;%s&quot; = %llu / %llu</code> |
| <code>ERR-08015</code> | <code>ERR_CC_UNMATCHED_HOST</code> | <code>Unmatched host: &quot;%s&quot; and &quot;%s&quot;</code> |
| <code>ERR-08016</code> | <code>ERR_CC_DASHBOARD_INITIALIZED</code> | <code>Dashboard initialized</code> |
| <code>ERR-08017</code> | <code>ERR_CC_DASHBOARD_NOT_INITIALIZED</code> | <code>Dashboard is not initialized</code> |
| <code>ERR-08018</code> | <code>ERR_CC_NULL_POINTER_ACCESS</code> | <code>NULL pointer access: &quot;%s&quot;.</code> |
| <code>ERR-08019</code> | <code>ERR_CC_STATUS_NOT_FOUND</code> | <code>Status not found: &quot;%s&quot;</code> |
| <code>ERR-08020</code> | <code>ERR_CC_HASH_INSERT_FAILED</code> | <code>Hash insert failed: &quot;%s&quot;</code> |
| <code>ERR-08021</code> | <code>ERR_CC_HASH_DELETE_FAILED</code> | <code>Hash delete failed: &quot;%s&quot;</code> |
| <code>ERR-08022</code> | <code>ERR_CC_HOST_TOO_LONG</code> | <code>Host too long: &quot;%s&quot;</code> |
| <code>ERR-08023</code> | <code>ERR_CC_ACTIVE_TOO_LONG</code> | <code>Active too long: &quot;%s&quot;</code> |
| <code>ERR-08024</code> | <code>ERR_CC_COORDINATOR_HOST_TOO_LONG</code> | <code>Coordinator-Host too long: &quot;%s&quot;</code> |
| <code>ERR-08025</code> | <code>ERR_CC_SPIN_TIMEOUT</code> | <code>Spin timeout</code> |
| <code>ERR-08026</code> | <code>ERR_CC_DDL_DISABLED</code> | <code>DDL disabled: %s</code> |
| <code>ERR-08027</code> | <code>ERR_CC_STATUS_UNINITALIZED</code> | <code>Status uninitialized</code> |
| <code>ERR-08028</code> | <code>ERR_CC_UNSUPPORTED_NODE_TYPE</code> | <code>Unsupported Node-Type: %u</code> |
| <code>ERR-08029</code> | <code>ERR_CC_SEQUENCE_NUMBER_UNINITIALIZED</code> | <code>Sequence number uninitialized</code> |
| <code>ERR-08030</code> | <code>ERR_CC_SEQUENCE_NUMBER_UNMATCHED</code> | <code>Sequence number unmatched: %lld and %lld</code> |
| <code>ERR-08031</code> | <code>ERR_CC_DDL_INCOMPLETED</code> | <code>DDL&#91;%lld&#93; incomplete: &#91;%s&#93;</code> |
| <code>ERR-08032</code> | <code>ERR_CC_INVALID_BROKER_COUNT</code> | <code>Invalid broker count: %lld</code> |
| <code>ERR-08033</code> | <code>ERR_CC_DDL_FAILED</code> | <code>DDL failed</code> |
| <code>ERR-08034</code> | <code>ERR_CC_DDL_SEQUENCE_NOT_FOUND</code> | <code>DDL sequence not found</code> |
| <code>ERR-08035</code> | <code>ERR_CC_INVALID_DDL_STATE</code> | <code>Invalid DDL state: %lld</code> |
| <code>ERR-08036</code> | <code>ERR_CC_INVALID_DDL_RETURNED</code> | <code>Invalid DDL returned: %lld and %lld</code> |
| <code>ERR-08037</code> | <code>ERR_CC_STANDBY_TOO_LONG</code> | <code>Standby too long: &quot;%s&quot;</code> |
| <code>ERR-08038</code> | <code>ERR_CC_INVALID_STATE_CHANGE</code> | <code>Invalid state change: %u =&gt; %u</code> |
| <code>ERR-08039</code> | <code>ERR_CC_INVALID_STATE</code> | <code>Invalid state: %u</code> |
| <code>ERR-08040</code> | <code>ERR_CC_INVALID_NODE_TYPE</code> | <code>Invalid Node-Type: %u</code> |
| <code>ERR-08041</code> | <code>ERR_CC_COORDINATOR_INACTIVE</code> | <code>Coordinator inactive</code> |
| <code>ERR-08042</code> | <code>ERR_CC_NOT_LEADER</code> | <code>Only leader can execute DDL.</code> |
| <code>ERR-08043</code> | <code>ERR_CC_DDL_TIMEOUT</code> | <code>DDL timeout</code> |
| <code>ERR-08044</code> | <code>ERR_CC_DDL_ERROR_MESSAGE</code> | <code>%s</code> |
| <code>ERR-08045</code> | <code>ERR_CC_DDL_NOT_FOUND</code> | <code>DDL not found: %llu</code> |
| <code>ERR-08046</code> | <code>ERR_CC_DDL_INCOMPLETNESS</code> | <code>DDL incompleteness: &quot;%s&quot;</code> |
| <code>ERR-08047</code> | <code>ERR_CC_UNSUPPORTED_PACKAGE</code> | <code>Unsupported package: &quot;%s&quot;</code> |
| <code>ERR-08048</code> | <code>ERR_CC_DDL_DISABLED_BY_MODE_CHANGE</code> | <code>DDL disabled by mode change</code> |
| <code>ERR-08049</code> | <code>ERR_CC_FAILED_TO_FORKED_COMMAND</code> | <code>Failed to fork and execute command: %s. Please check deployer&#x27;s trace log.</code> |
| <code>ERR-08050</code> | <code>ERR_CC_FUNCTION_EXECUTION_WITH_RC</code> | <code>Function execution failed: &quot;%s&quot; (errno=%d).</code> |
| <code>ERR-08051</code> | <code>ERR_CC_DDL_DISABLED_READONLY_GROUP</code> | <code>DDL disabled because a part of group is not normal.</code> |
| <code>ERR-08052</code> | <code>ERR_CC_DDLSYNC_EXECUTE_FAILED_AFTER_RETRY</code> | <code>DDL&#91;%llu&#93; execution during DDL-Sync failed after several attempts.</code> |
| <code>ERR-08053</code> | <code>ERR_CC_INVALID_OPTION</code> | <code>Invalid option (%s).</code> |
| <code>ERR-08054</code> | <code>ERR_CC_GROUP_NOT_FOUND</code> | <code>Group (%s) is not found.</code> |
| <code>ERR-08055</code> | <code>ERR_CC_PORT_CHECK_REQUIRED</code> | <code>Check %s port number (%d).</code> |
| <code>ERR-08056</code> | <code>ERR_CC_DEPLOYER_DISABLED</code> | <code>Deployer is disabled: &quot;%s&quot;.</code> |
| <code>ERR-08057</code> | <code>ERR_CC_ONLY_PRIMARY_COORDINATOR_AVAILABLE</code> | <code>Command is not available in the secondary coordinator.</code> |
| <code>ERR-08058</code> | <code>ERR_CC_CLUSTER_SYNC_FAILURE</code> | <code>Cluster synchronization failed.</code> |
| <code>ERR-08059</code> | <code>ERR_CC_INVALID_DECISION_STATE</code> | <code>Invaid decision state: %s</code> |
| <code>ERR-08060</code> | <code>ERR_CC_MISSING_ATTRIBUTE</code> | <code>Missing attribute: %s</code> |
| <code>ERR-08061</code> | <code>ERR_CC_ATTRIBUTE_OCCURS_TOO_MANY_TIMES</code> | <code>Attribute occurs too many times: %s</code> |
| <code>ERR-08062</code> | <code>ERR_CC_EXECUTE_COMMAND_FAILURE</code> | <code>Failed to execute command (%s).</code> |
| <code>ERR-08063</code> | <code>ERR_CC_PACKAGE_ALREADY_EXISTS</code> | <code>Package name or file name already exists (%s = %s).</code> |
| <code>ERR-08064</code> | <code>ERR_CC_HOST_RES_INFO_NOT_FOUND</code> | <code>Host resource info not found: &quot;%s&quot;</code> |
| <code>ERR-08065</code> | <code>ERR_CC_DISK_INFO_NOT_FOUND</code> | <code>Disk info not found: &quot;%s&quot;</code> |
| <code>ERR-08066</code> | <code>ERR_CC_INTEGER_OVERFLOW</code> | <code>Integer overflow.</code> |
| <code>ERR-08067</code> | <code>ERR_CC_COORDINATOR_COUNT_EXCEEDED</code> | <code>The number of coordinators exceeded %d.</code> |
| <code>ERR-08068</code> | <code>ERR_CC_DDL_DISABLED_BY_INITIAL_STATE</code> | <code>DDL disabled since some of nodes are in initial states.</code> |
| <code>ERR-08069</code> | <code>ERR_CC_COORD_ROLE_HANDSHAKE</code> | <code>Coordinator role handshake failed: &#91;%s&#93;</code> |
| <code>ERR-08070</code> | <code>ERR_CC_HOST_RESOURCE_DISABLED</code> | <code>Collecting host resource is disabled.</code> |
| <code>ERR-08071</code> | <code>ERR_CC_REQUEST_FAILED</code> | <code>Request to execute command %s failed. (code=%d)</code> |
| <code>ERR-08072</code> | <code>ERR_CC_CLUSTER_ACTIVATION_FAILED</code> | <code>Cluster activation failed: %lld / %lld.</code> |
| <code>ERR-08073</code> | <code>ERR_CC_ENVIRONMENT_VARIABLE_NOT_SET</code> | <code>Environment (%s) is not set.</code> |
| <code>ERR-08074</code> | <code>ERR_CC_OPTION_DUPLICATED</code> | <code>Option duplicated.</code> |
| <code>ERR-08075</code> | <code>ERR_CC_OPTION_REQUIRED</code> | <code>Option required (%s).</code> |
| <code>ERR-08076</code> | <code>ERR_CC_LOCK_FAILED</code> | <code>Cannot read Lock File! Check $MACHBASE_COORDINATOR_HOME/conf/machbasecoordinator.lock&#42; and Tracelog in $MACHBASE_COORDINATOR_HOME/trc.</code> |
| <code>ERR-08077</code> | <code>ERR_CC_COORDINATOR_RUNNING</code> | <code>Machbase coordinator is running.</code> |
| <code>ERR-08078</code> | <code>ERR_CC_COORDINATOR_NOT_RUNNING</code> | <code>Machbase coordinator is not running.</code> |
| <code>ERR-08079</code> | <code>ERR_CC_COORDINATOR_PHASE1_FAILED</code> | <code>Machbase Coordinator %s Phase1 failed: %s</code> |
| <code>ERR-08080</code> | <code>ERR_CC_COORDINATOR_PHASE2_FAILED</code> | <code>Machbase Coordinator %s Phase2 failed: %s</code> |
| <code>ERR-08081</code> | <code>ERR_CC_COORDINATOR_DEAD</code> | <code>Machbase Coordinator has been DEAD! Check Tracelog in $MACHBASE_COORDINATOR_HOME/trc.</code> |
| <code>ERR-08082</code> | <code>ERR_CC_METADATA_NOT_CREATED</code> | <code>Machbase Coordinator metadata is not created. Check Tracelog in $MACHBASE_COORDINATOR_HOME/trc.</code> |
| <code>ERR-08083</code> | <code>ERR_CC_METADATA_ALREADY_CREATED</code> | <code>Machbase Coordinator metadata is already created. Check Tracelog in $MACHBASE_COORDINATOR_HOME/trc.</code> |
| <code>ERR-08084</code> | <code>ERR_CC_INVALID_PROCESS_ID</code> | <code>Invalid process id.</code> |
| <code>ERR-08085</code> | <code>ERR_CC_OPTION_INIT_FAILED</code> | <code>Option initialization error: %d.</code> |
| <code>ERR-08086</code> | <code>ERR_CC_OPTION_CHECK_FAILED</code> | <code>Option check error: %d.</code> |
| <code>ERR-08087</code> | <code>ERR_CC_OPTION_GET_FAILED</code> | <code>Option retrieval error: %d (%s).</code> |
| <code>ERR-08088</code> | <code>ERR_CC_COMMAND_OPTION_NOT_FOUND</code> | <code>Command option is not found.</code> |
| <code>ERR-08089</code> | <code>ERR_CC_COLLECTING_HOST_RES_FAILED</code> | <code>Failed to collect &#x27;%s&#x27;: %s.</code> |
| <code>ERR-08090</code> | <code>ERR_CC_INVALID_ATTRIBUTE</code> | <code>Invalid attribute: %s</code> |
| <code>ERR-08091</code> | <code>ERR_CC_DDL_RECOVERY_FAILED</code> | <code>DDL recovery failed: %s.</code> |
| <code>ERR-08092</code> | <code>ERR_CC_DESIRED_STATE_NOT_APPLICABLE</code> | <code>Desired state (%s) is not applicable.</code> |
| <code>ERR-08093</code> | <code>ERR_CC_NODE_STILL_RUNNING</code> | <code>%s is still running.</code> |
| <code>ERR-08094</code> | <code>ERR_CC_SNAPSHOT_NOT_EXIST</code> | <code>SNAPSHOT on %s does not exist.</code> |
| <code>ERR-08095</code> | <code>ERR_CC_RECOVER_NON_READONLY</code> | <code>Group %s is not readonly mode. Snapshot recovery works only for a readonly group</code> |
| <code>ERR-08096</code> | <code>ERR_CC_SNAPSHOT_NOT_AVAILABLE</code> | <code>Snapshot is not available: %s</code> |
| <code>ERR-08097</code> | <code>ERR_CC_NOT_SCRAPPED</code> | <code>Warehouse %s is not scrapped. %s only works on a scrapped warehouse.</code> |
| <code>ERR-08098</code> | <code>ERR_CC_MASTER_NOT_FOUND</code> | <code>Cannot add lookup node %s (%s) before adding the lookup master node.</code> |
| <code>ERR-08099</code> | <code>ERR_CC_MASTER_NOT_MONITOR</code> | <code>Lookup monitor node (%s) cannot change the lookup master node.</code> |
| <code>ERR-08100</code> | <code>ERR_CC_SNAPSHOT_FAIL_PUBLISH</code> | <code>Failed to publish SnapshotID to warehouse.</code> |
| <code>ERR-08101</code> | <code>ERR_CC_NOT_READONLY</code> | <code>Group (%s) is not readonly.</code> |
| <code>ERR-08102</code> | <code>ERR_CC_NODE_FIX</code> | <code>Fix node (%s) failed. (refcnt=%d)</code> |
| <code>ERR-08103</code> | <code>ERR_CC_LOOKUP_ALREADY_RUNNING</code> | <code>Lookup node running already. (%s:%d)</code> |
| <code>ERR-08104</code> | <code>ERR_CC_LOOKUP_CONNECT_FAILED</code> | <code>Connect to lookup node failed. (%s:%d)</code> |
| <code>ERR-08105</code> | <code>ERR_CC_LOOKUP_STARTUP_FAILED</code> | <code>Startup lookup node failed. (%s:%d)</code> |
| <code>ERR-08106</code> | <code>ERR_CC_NORMAL_SHUTDOWN</code> | <code>Unable to shutdown warehouse (%s) since it is not INACTIVE status.</code> |
| <code>ERR-08107</code> | <code>ERR_CC_MESSAGE_EXPIRED</code> | <code>Expired message (%llu) received.</code> |
| <code>ERR-08108</code> | <code>ERR_CC_SNAPSHOT_FAIL</code> | <code>Snapshot failed: %s</code> |

### `ERR-09000`–`ERR-09999` (11)

| 코드 | 심볼 | 메시지 원문 |
|------|------|------|
| <code>ERR-09000</code> | <code>ERR_RP_BUFFER_POOL_ITEM_ALLOC_FAIL</code> | <code>Failed to allocate buffer pool item.</code> |
| <code>ERR-09001</code> | <code>ERR_RP_TARGET_FILE_OPEN_FAIL</code> | <code>Failed to open replication target file &lt;Table %llu, FileID %llu, PartID %llu - Level %d Type %d&gt;</code> |
| <code>ERR-09002</code> | <code>ERR_RP_PROTOCOL_ERROR</code> | <code>Invalid protocol received.</code> |
| <code>ERR-09003</code> | <code>ERR_RP_SOCKET_ERROR</code> | <code>Socket write failed.</code> |
| <code>ERR-09004</code> | <code>ERR_RP_APPEND_VALUE_ERROR</code> | <code>Failed to append target table&lt;%llu&gt;.</code> |
| <code>ERR-09005</code> | <code>ERR_RP_VALUE_BUFFER_ALLOC_MEM_FAIL</code> | <code>Failed to allocate value buffer.</code> |
| <code>ERR-09006</code> | <code>ERR_RP_TABLE_CURSOR_OPEN_FAIL</code> | <code>Failed to open table &lt;%llu&gt;&#x27;s cursor.</code> |
| <code>ERR-09007</code> | <code>ERR_RP_POLL_REMOVE</code> | <code>Failed to remove poll socket. (%d)</code> |
| <code>ERR-09008</code> | <code>ERR_RP_POLL_DESTROY</code> | <code>Failed to destroy poll socket. (%d)</code> |
| <code>ERR-09009</code> | <code>ERR_RP_CANNOT_REPLICATE2_LARGER</code> | <code>Cannot replicate to larger dbs.</code> |
| <code>ERR-09010</code> | <code>ERR_RP_HOST_NOT_FOUND</code> | <code>Host not found: &quot;%s&quot;.</code> |

<!-- END GENERATED NFX ERROR CATALOG -->

## 오류 코드 확인 방법

- machsql 또는 드라이버에서 반환하는 오류 문자열을 확인합니다.
- 서버 로그는 `$MACHBASE_HOME/trc/` 아래의 trace 로그를 확인합니다.

오류 발생 후 원인을 파악하기 어렵다면 서버 로그 분석과 장애 징후 확인 섹션을 참고하십시오.
