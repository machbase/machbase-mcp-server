# Machbase Neo JavaScript Zip Module

The `archive/zip` module creates and extracts ZIP archives in JSH.
It provides in-memory helpers, stream-style APIs, and a file-based `Zip` class.

```js
const zip = require('archive/zip');
```

## zipSync()

Creates a ZIP archive synchronously.

<h6>Syntax</h6>

```js
zipSync(data)
```

<h6>Parameters</h6>

- `data` `String | ArrayBuffer | Uint8Array | Number[] | Object[]`

If `data` is an array, each item should be an entry object such as `{ name, data }`.

<h6>Return value</h6>

Returns an `ArrayBuffer` that contains ZIP archive bytes.

<h6>Usage example</h6>

```js
const zip = require('archive/zip');
const archive = zip.zipSync([
    { name: 'alpha.txt', data: 'Alpha' },
    { name: 'dir/beta.txt', data: 'Beta' }
]);
```

## unzipSync()

Extracts ZIP archive bytes synchronously and returns entry objects.

Each entry can include `name`, `data`, `comment`, `method`, `compressedSize`, `size`, `isDir`, and `modified`.

## zip() / unzip()

Callback-style asynchronous wrappers. Callback signature: `(err, result) => {}`.

## createZip()

Creates a stream-style ZIP writer. Accepts entry objects through `write()` and emits archive bytes through the `data` event when `end()` is called.

## createUnzip()

Creates a stream-style ZIP reader. Write archive bytes with `write()`, then call `end()` to emit one `entry` event per extracted item.

<h6>Usage example</h6>

```js
const zip = require('archive/zip');
const writer = zip.createZip();
let archive = null;

writer.on('data', function(chunk) { archive = chunk; });
writer.on('end', function() {
    const reader = zip.createUnzip();
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

## Zip

File-oriented helper class for building, saving, loading, and extracting ZIP archives.

<h6>Constructor</h6>

```js
new zip.Zip(filePath?)
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

Appends an archive entry object directly. Supported fields: `name`, `data`, `comment`, `method`.

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
const zip = require('archive/zip');

const z = new zip.Zip();
z.addBuffer('hello world', 'app.log');
z.addEntry({ name: 'config.json', data: '{"enabled":true}' });
z.writeTo('/tmp/data.zip');

const saved = new zip.Zip('/tmp/data.zip');
saved.extractAllTo('/tmp/out', {
    overwrite: true,
    filter: function(entry) { return entry.name === 'app.log'; }
});
```

## Notes

- `filter` may be a callback, `RegExp`, string match, or array of entry names.
- `extractAllTo()` throws an error if the destination file already exists and `overwrite` is `false`.
- ZIP entries do not support TAR link metadata such as `symlink` or `linkname`.
