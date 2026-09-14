# Machbase Neo JavaScript Tar Module

`archive/tar` 모듈은 JSH에서 TAR 아카이브를 만들고 풉니다.
간단한 메모리 기반 도우미, 스트림 방식 API, 파일 기반 `Tar` 클래스를 지원합니다.

```js
const tar = require('archive/tar');
```

## tarSync()

TAR 아카이브를 동기적으로 만듭니다.

<h6>문법</h6>

```js
tarSync(data)
```

<h6>파라미터</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

`data`가 배열이면 각 항목은 `{ name, data }` 같은 항목 객체여야 합니다.

<h6>반환값</h6>

TAR 아카이브 바이트를 담은 `ArrayBuffer`를 반환합니다.

<h6>사용 예제</h6>

```js
const tar = require('archive/tar');
const archive = tar.tarSync([
    { name: 'alpha.txt', data: 'Alpha' },
    { name: 'dir/beta.txt', data: 'Beta' }
]);
```

## untarSync()

TAR 아카이브 바이트를 동기적으로 풀어 항목 객체를 반환합니다.

<h6>문법</h6>

```js
untarSync(buffer)
```

각 항목은 `name`, `data`, `mode`, `size`, `isDir`, `modified`, `typeflag`, `type`, `linkname`을 포함할 수 있습니다.

## tar() / untar()

콜백 방식의 비동기 래퍼입니다. 콜백 시그니처: `(err, result) => {}`.

## createTar()

스트림 방식 TAR writer를 만듭니다. `write()`로 항목 객체를 받고 `end()` 호출 시 `data` 이벤트로 아카이브 바이트를 내보냅니다.

## createUntar()

스트림 방식 TAR reader를 만듭니다. `write()`로 아카이브 바이트를 쓰고 `end()`를 호출하면 추출된 항목마다 `entry` 이벤트를 내보냅니다.

<h6>사용 예제</h6>

```js
const tar = require('archive/tar');
const writer = tar.createTar();
let archive = null;

writer.on('data', function(chunk) { archive = chunk; });
writer.on('end', function() {
    const reader = tar.createUntar();
    reader.on('entry', function(entry) {
        const text = String.fromCharCode.apply(null, new Uint8Array(entry.data));
        console.println(entry.name + '=' + text);
    });
    reader.write(archive);
    reader.end();
});

writer.write({ name: 'one.txt', data: 'One' });
writer.write({ name: 'two.txt', data: 'Two' });
writer.end();
```

## Tar

TAR 아카이브를 만들고 저장·로드·추출하는 파일 중심 도우미 클래스입니다.

<h6>생성자</h6>

```js
new tar.Tar(filePath?)
```

`filePath`를 주면 해당 파일에서 아카이브를 불러옵니다.

### addFile()

파일 시스템에서 파일을 읽어 아카이브 항목으로 추가합니다.

```js
addFile(filePath[, entryName])
```

### addBuffer()

문자열 또는 바이트 버퍼를 아카이브 항목으로 추가합니다.

```js
addBuffer(data, entryName[, options])
```

### addEntry()

아카이브 항목 객체를 직접 추가합니다. 지원 필드: `name`, `data`, `mode`, `modified`, `type`(`file`, `dir`, `symlink`, `link`), `typeflag`, `linkname`, `isDir`.

### getEntries()

현재 아카이브 항목들의 얕은 복사본을 반환합니다.

### writeTo()

아카이브를 파일에 씁니다.

```js
writeTo(filePath)
```

### extractAllTo()

항목들을 디렉터리에 풉니다.

```js
extractAllTo(outputDir[, overwrite])
extractAllTo(outputDir, options)
```

`options`는 `overwrite`(Boolean)와 `filter`(Function | RegExp | String | String[])를 지원합니다.

<h6>사용 예제</h6>

```js
const tar = require('archive/tar');

const t = new tar.Tar();
t.addEntry({ name: 'docs', isDir: true, type: 'dir' });
t.addEntry({ name: 'docs/readme.txt', data: 'hello tar' });
t.writeTo('/tmp/bundle.tar');

const saved = new tar.Tar('/tmp/bundle.tar');
saved.extractAllTo('/tmp/out', {
    overwrite: true,
    filter: function(entry) { return entry.name.endsWith('.txt'); }
});
```
