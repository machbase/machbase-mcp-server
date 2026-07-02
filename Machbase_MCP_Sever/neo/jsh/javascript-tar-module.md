# Machbase Neo JavaScript Tar Module

The `archive/tar` module creates and extracts TAR archives in JSH.
It supports simple in-memory helpers, stream-style APIs, and a file-based `Tar` class.

```js
const tar = require('archive/tar');
```

## tarSync()

Creates a TAR archive synchronously.

<h6>Syntax</h6>

```js
tarSync(data)
```

<h6>Parameters</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

If `data` is an array, each item should be an entry object such as `{ name, data }`.

<h6>Return value</h6>

Returns an `ArrayBuffer` that contains TAR archive bytes.

<h6>Usage example</h6>

```js
const tar = require('archive/tar');
const archive = tar.tarSync([
    { name: 'alpha.txt', data: 'Alpha' },
    { name: 'dir/beta.txt', data: 'Beta' }
]);
```

## untarSync()

Extracts TAR archive bytes synchronously and returns entry objects.

<h6>Syntax</h6>

```js
untarSync(buffer)
```

Each entry can include `name`, `data`, `mode`, `size`, `isDir`, `modified`, `typeflag`, `type`, and `linkname`.

## tar() / untar()

Callback-style asynchronous wrappers. Callback signature: `(err, result) => {}`.

## createTar()

Creates a stream-style TAR writer. Accepts entry objects through `write()` and emits archive bytes through the `data` event when `end()` is called.

## createUntar()

Creates a stream-style TAR reader. Write archive bytes with `write()`, then call `end()` to emit one `entry` event per extracted item.

<h6>Usage example</h6>

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

File-oriented helper class for building, saving, loading, and extracting TAR archives.

<h6>Constructor</h6>

```js
new tar.Tar(filePath?)
```

If `filePath` is provided, the archive is loaded from that file.

### addFile()

Reads a file from the filesystem and appends it as an archive entry.

```js
addFile(filePath[, entryName])
```

### addBuffer()

Appends a string or byte buffer as an archive entry.

```js
addBuffer(data, entryName[, options])
```

### addEntry()

Appends an archive entry object directly. Supported fields: `name`, `data`, `mode`, `modified`, `type` (`file`, `dir`, `symlink`, `link`), `typeflag`, `linkname`, `isDir`.

### getEntries()

Returns a shallow copy of the current archive entries.

### writeTo()

Writes the archive to a file.

```js
writeTo(filePath)
```

### extractAllTo()

Extracts entries to a directory.

```js
extractAllTo(outputDir[, overwrite])
extractAllTo(outputDir, options)
```

`options` supports `overwrite` (Boolean) and `filter` (Function | RegExp | String | String[]).

<h6>Usage example</h6>

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
