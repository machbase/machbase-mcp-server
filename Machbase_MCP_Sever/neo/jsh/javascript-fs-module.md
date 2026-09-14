# Machbase Neo JavaScript FS Module

`fs` 모듈은 JSH 애플리케이션을 위한 동기식 Node.js 호환 파일 시스템 API를 제공합니다.

## readFile()

파일을 읽어 내용을 문자열(기본값 `utf8`) 또는 바이트로 반환합니다.

<h6>문법</h6>

```js
readFile(path[, options])
```

<h6>사용 예제</h6>

```js
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile()

파일에 데이터를 씁니다. 파일을 만들거나 기존 내용을 덮어씁니다.

<h6>문법</h6>

```js
writeFile(path, data[, options])
```

<h6>사용 예제</h6>

```js
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile()

파일에 데이터를 덧붙입니다. 파일이 없으면 만듭니다.

<h6>문법</h6>

```js
appendFile(path, data[, options])
```

## countLines()

파일에서 개행으로 구분된 줄 수를 셉니다.

<h6>문법</h6>

```js
countLines(path)
```

## exists()

파일이나 디렉터리가 있으면 `true`를 반환합니다.

<h6>문법</h6>

```js
exists(path)
```

## stat()

파일 또는 디렉터리의 메타데이터를 반환합니다.

<h6>문법</h6>

```js
stat(path)
```

<h6>반환 필드</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>사용 예제</h6>

```js
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

파일 메타데이터를 반환합니다. 현재 구현은 `stat()`과 동일하게 동작합니다.

## readdir()

디렉터리 항목을 읽습니다.

- 기본: `string[]`을 반환합니다
- `withFileTypes: true`: `name`과 타입 메서드를 가진 항목 객체를 반환합니다
- `recursive: true`: 하위까지 재귀적으로 항목을 반환합니다

<h6>문법</h6>

```js
readdir(path[, options])
```

<h6>사용 예제</h6>

```js
const fs = require('fs');
const names = fs.readdir('/lib');
const entries = fs.readdir('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdir()

디렉터리를 만듭니다. 재귀 생성을 지원합니다.

<h6>문법</h6>

```js
mkdir(path[, options])
```

<h6>사용 예제</h6>

```js
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
```

## rmdir()

디렉터리를 삭제합니다. `{ recursive: true }`이면 하위 항목부터 삭제합니다.

## rm()

파일 또는 디렉터리를 삭제합니다. `force: true`이면 오류를 무시합니다.

## unlink()

파일을 삭제합니다.

## rename()

같은 마운트 파일시스템 안에서 파일·디렉터리의 이름을 바꾸거나 이동합니다.

## copyFile()

파일 하나를 복사합니다. `COPYFILE_EXCL`은 대상이 이미 있으면 실패합니다.

## cp()

파일 또는 디렉터리를 복사합니다. 디렉터리 복사에는 `{ recursive: true }`가 필요합니다.

## symlink()

심볼릭 링크를 만듭니다.

## readlink()

심볼릭 링크의 대상을 읽습니다.

## realpath()

심볼릭 링크를 따라 해석된 경로를 반환합니다.

## access()

경로 접근 가능 여부를 확인합니다. 모드 상수 `F_OK`, `R_OK`, `W_OK`, `X_OK`를 지원합니다.

## truncate()

파일 내용을 잘라냅니다.

## open()

파일을 열고 숫자형 파일 디스크립터를 반환합니다.
`r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+` 같은 문자열 플래그를 지원합니다.

## close()

파일 디스크립터를 닫습니다.

## read()

파일 디스크립터에서 버퍼로 읽습니다.

```js
read(fd, buffer, offset, length[, position])
```

## write()

파일 디스크립터에 문자열 또는 버퍼 데이터를 씁니다.

```js
write(fd, buffer, offset, length[, position])
```

## fstat()

파일 디스크립터에서 메타데이터를 반환합니다.

## fchmod(), fchown()

파일 디스크립터로 모드·소유자를 변경합니다.

## fsync(), fdatasync()

대기 중인 파일 데이터를 저장소에 플러시합니다.

## chmod(), chown()

경로로 모드·소유자를 변경합니다. Windows에서는 아무 동작도 하지 않는 호환 동작입니다.

## createReadStream(), createWriteStream()

EventEmitter 기반 사용과 호환되는 스트림 객체를 만듭니다.

<h6>사용 예제</h6>

```js
const fs = require('fs');
const rs = fs.createReadStream('/work/in.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/out.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## platform(), arch()

런타임 플랫폼과 아키텍처 문자열을 반환합니다.

## constants

접근·복사·열기 플래그를 위한 상수 객체입니다.

- Access: `F_OK`, `R_OK`, `W_OK`, `X_OK`
- Copy: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- Open: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

## Aliases

Node.js 호환을 위해 이 모듈은 `Sync` 접미가 붙은 별칭도 내보냅니다:
`readFileSync`, `writeFileSync`, `appendFileSync`, `readdirSync`, `mkdirSync`, `rmSync`, `statSync`, `openSync`, `closeSync`, `readSync`, `writeSync`, `fstatSync`, `fsyncSync`, `fdatasyncSync`.

## 예제

### JSON 파일 읽고 파싱하기

```js
const fs = require('fs');

try {
    const content = fs.readFile('/path/to/config.json', 'utf8');
    const config = JSON.parse(content);
    console.println('Config loaded:', config);
} catch (e) {
    console.println('Error reading config:', e);
}
```

### 디렉터리 트리 순회

```js
const fs = require('fs');

function walkDir(dir, callback, indent) {
    indent = indent || '';
    const entries = fs.readdir(dir, { withFileTypes: true });
    entries.forEach(entry => {
        const fullPath = dir + '/' + entry.name;
        if (entry.isDirectory()) {
            console.println(indent + '[DIR] ' + entry.name);
            walkDir(fullPath, callback, indent + '  ');
        } else {
            console.println(indent + entry.name);
            callback(fullPath);
        }
    });
}
```

### 안전한 파일 쓰기

```js
const fs = require('fs');

function safeWriteFile(path, data) {
    const tempPath = path + '.tmp';
    try {
        fs.writeFile(tempPath, data, 'utf8');
        fs.rename(tempPath, path);
        console.println('File written safely');
    } catch (e) {
        if (fs.exists(tempPath)) {
            fs.unlink(tempPath);
        }
        throw e;
    }
}
```
