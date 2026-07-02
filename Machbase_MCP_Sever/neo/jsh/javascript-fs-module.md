# Machbase Neo JavaScript FS Module

The `fs` module provides synchronous, Node.js-compatible file system APIs for JSH applications.

## readFile()

Reads a file and returns its content as a string (default: `utf8`) or as bytes.

<h6>Syntax</h6>

```js
readFile(path[, options])
```

<h6>Usage example</h6>

```js
const fs = require('fs');
const content = fs.readFile('/lib/fs.js', 'utf8');
console.println(content.length);
```

## writeFile()

Writes data to a file. Creates the file or overwrites existing content.

<h6>Syntax</h6>

```js
writeFile(path, data[, options])
```

<h6>Usage example</h6>

```js
const fs = require('fs');
fs.writeFile('/work/test.txt', 'Hello', 'utf8');
```

## appendFile()

Appends data to a file. Creates the file when it does not exist.

<h6>Syntax</h6>

```js
appendFile(path, data[, options])
```

## countLines()

Counts newline-separated lines in a file.

<h6>Syntax</h6>

```js
countLines(path)
```

## exists()

Returns `true` if a file or directory exists.

<h6>Syntax</h6>

```js
exists(path)
```

## stat()

Returns file or directory metadata.

<h6>Syntax</h6>

```js
stat(path)
```

<h6>Returned fields</h6>

- `name`, `size`, `mode`, `mtime`, `atime`, `ctime`, `birthtime`
- `isFile()`, `isDirectory()`, `isSymbolicLink()`
- `isBlockDevice()`, `isCharacterDevice()`, `isFIFO()`, `isSocket()`

<h6>Usage example</h6>

```js
const fs = require('fs');
const st = fs.stat('/work/test.txt');
console.println(st.isFile(), st.size);
console.println(st.name);
```

## lstat()

Returns file metadata. Current implementation behaves the same as `stat()`.

## readdir()

Reads directory entries.

- Default: returns `string[]`
- `withFileTypes: true`: returns entry objects with `name` and type methods
- `recursive: true`: returns recursive entries

<h6>Syntax</h6>

```js
readdir(path[, options])
```

<h6>Usage example</h6>

```js
const fs = require('fs');
const names = fs.readdir('/lib');
const entries = fs.readdir('/lib', { withFileTypes: true });
console.println(names.length, entries.length);
```

## mkdir()

Creates a directory. Supports recursive creation.

<h6>Syntax</h6>

```js
mkdir(path[, options])
```

<h6>Usage example</h6>

```js
const fs = require('fs');
fs.mkdir('/work/a/b/c', { recursive: true });
```

## rmdir()

Removes a directory. With `{ recursive: true }`, removes children first.

## rm()

Removes a file or directory. `force: true` suppresses errors.

## unlink()

Removes a file.

## rename()

Renames or moves a file/directory in the same mounted filesystem.

## copyFile()

Copies a single file. `COPYFILE_EXCL` fails when destination exists.

## cp()

Copies a file or directory. Directory copy requires `{ recursive: true }`.

## symlink()

Creates a symbolic link.

## readlink()

Reads a symbolic link target.

## realpath()

Returns a resolved path with symlink resolution behavior.

## access()

Checks path accessibility. Supports mode constants: `F_OK`, `R_OK`, `W_OK`, `X_OK`.

## truncate()

Truncates file content.

## open()

Opens a file and returns a numeric file descriptor.
Supports string flags such as `r`, `r+`, `w`, `w+`, `a`, `a+`, `wx`, `wx+`, `ax`, `ax+`.

## close()

Closes a file descriptor.

## read()

Reads from a file descriptor into a buffer.

```js
read(fd, buffer, offset, length[, position])
```

## write()

Writes string or buffer data to a file descriptor.

```js
write(fd, buffer, offset, length[, position])
```

## fstat()

Returns metadata from a file descriptor.

## fchmod(), fchown()

Changes mode/owner via file descriptor.

## fsync(), fdatasync()

Flushes pending file data to storage.

## chmod(), chown()

Changes mode/owner by path. On Windows, these are no-op compatible behaviors.

## createReadStream(), createWriteStream()

Creates stream objects compatible with EventEmitter-based usage.

<h6>Usage example</h6>

```js
const fs = require('fs');
const rs = fs.createReadStream('/work/in.txt', { encoding: 'utf8' });
const ws = fs.createWriteStream('/work/out.txt', { encoding: 'utf8' });
rs.pipe(ws);
```

## platform(), arch()

Returns runtime platform and architecture strings.

## constants

Constant object for access, copy, and open flags.

- Access: `F_OK`, `R_OK`, `W_OK`, `X_OK`
- Copy: `COPYFILE_EXCL`, `COPYFILE_FICLONE`, `COPYFILE_FICLONE_FORCE`
- Open: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_EXCL`, `O_TRUNC`, `O_APPEND`

## Aliases

For Node.js compatibility, the module also exports `Sync`-suffixed aliases:
`readFileSync`, `writeFileSync`, `appendFileSync`, `readdirSync`, `mkdirSync`, `rmSync`, `statSync`, `openSync`, `closeSync`, `readSync`, `writeSync`, `fstatSync`, `fsyncSync`, `fdatasyncSync`.

## Examples

### Read and Parse JSON File

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

### Directory Tree Walker

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

### Safe File Write

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
