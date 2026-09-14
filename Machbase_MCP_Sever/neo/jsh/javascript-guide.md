# Machbase Neo JavaScript Guide

**BETA Notice**  
JSH는 현재 베타입니다. API와 명령은 향후 릴리스에서 바뀔 수 있습니다.

JSH를 사용하면 Machbase Neo용 JavaScript 애플리케이션을 작성할 수 있습니다.
Machbase Neo는 `.js` 확장자를 가진 단독 파일과
`index.js` 진입 파일을 포함한 디렉터리를 모두 실행 가능한 JSH 애플리케이션으로 인식합니다.

## Hello World 예제

다음 코드를 복사해 `hello.js`로 저장합니다.

```js
console.print("Hello World?\n")
```

"New..." 페이지에서 "JSH"를 선택합니다.

`.js` 파일을 실행하는 간단한 명령행 인터프리터로 동작합니다.

저장한 스크립트를 실행하려면 다음 명령을 사용합니다:

```
/work > ./hello.js
Hello World? 
```

## 데이터베이스 예제

Machbase 데이터를 조회하고 입력하는 애플리케이션을 손쉽게 작성할 수 있습니다.

```js
'use strict';
// Load machbase client module.
const machcli = require('machcli');
// Create database client instance.
const db = new machcli.Client({
    host: '127.0.0.1',
    port: 5656, // machbase native port
    username:'sys',
    password: 'manager'
})

var conn, rows;
try {
    // Create a database connection.
    conn = db.connect();
    // Execute query.
    rows = conn.query('SELECT NAME, TYPE, COLCOUNT FROM m$sys_tables LIMIT 5');
    // Iterates result set.
    for (const row of rows) {
        console.println(row.NAME, row.TYPE, row.COLCOUNT);
    }
} finally {
    // Release resources
    rows && rows.close();
    conn && conn.close();
}
```

## 외부 실행

작성한 JavaScript 애플리케이션을 machbase-neo 서버 프로세스 밖에서도 실행할 수 있습니다.
machbase-neo 실행 파일만 있으면 됩니다.
`machbase-neo jsh`를 실행하면 JSH 인터프리터가 주어진 스크립트를 실행합니다.
이 방식으로 machbase-neo 실행 파일만으로 데이터베이스 조회·입력 애플리케이션을 만들 수 있습니다.
추가 도구가 필요 없습니다.

```sh
$ /path/to/the/machbase-neo jsh ./hello.js
Hello World?
```

## Commands

- `exit` 현재 JSH 세션을 종료합니다.
- `ls` 현재 작업 디렉터리의 파일 목록을 보여줍니다.
- `cd` 작업 디렉터리를 바꾸거나 `/work`로 이동합니다.

기능은 기본적이지만 스크립트를 검증하기에는 충분합니다.

## Modules
JSH에는 TQL의 `SCRIPT()`와 `*.js` 애플리케이션에서 사용할 수 있는 다양한 JavaScript 모듈이 포함되어 있습니다.
다만 `$.yield()` 같은 유틸리티 메서드를 제공하는 TQL 컨텍스트 객체 `$`는 TQL 전용이며 `*.js` 애플리케이션에서는 사용할 수 없습니다.

자세한 내용은 각 모듈 문서를 참고하세요.
