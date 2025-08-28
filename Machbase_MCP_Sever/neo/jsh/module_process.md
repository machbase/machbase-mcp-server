---
title: "@jsh/process"
type: docs
weight: 3
---

{{< neo_since ver="8.0.52" />}}

The `@jsh/process` module is specifically designed for use in JSH applications 
and is not available in the `SCRIPT()` function within TQL, unlike other JSH modules.

## pid()

Get the process id of the current process.

<h6>Syntax</h6>

```js
pid()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

A number value that represents the process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("my pid =", m.pid())
```

## ppid()

Get the process id of the parent process.

<h6>Syntax</h6>

```js
ppid()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

A number value that represents the parent process ID.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const m = require("@jsh/process")
console.log("parent pid =", m.ppid())
```

## args()

Get command line arguments

<h6>Syntax</h6>

```js
args()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

`String[]`

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
args = p.args();
x = parseInt(args[1]);
console.log(`x = ${x}`);
```

## cwd()

Get the current working directory

<h6>Syntax</h6>

```js
cwd()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
console.log("cwd :", p.cwd());
```

## cd()

Change the current working directory.

<h6>Syntax</h6>

```js
cd(path)
```

<h6>Parameters</h6>

`path` : directory path to move

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process");
p.cd('/dir/path');
console.log("cwd :", p.cwd());
```

## readDir()

Read files and sub-directories of the given directory.

<h6>Syntax</h6>

```js
readDir(path, callback)
```

<h6>Parameters</h6>

- `path`: `String` path to the directory
- `callback`: function ([DirEntry](#DirEntry)) [undefined|Boolean] callback function. if it returns false, the iteration will stop.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}

```

## DirEntry

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| name               | String     |                    |
| isDir              | Boolean    |                    |
| readOnly           | Boolean    |                    |
| type               | String     |                    |
| size               | Number     |                    |
| virtual            | Boolean    |                    |

<!-- ## readLine()

...

<h6>Syntax</h6>

```js
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
``` -->

## print()

Write arguments into the output, the default output is the log file or stdout if log filename is not set.

<h6>Syntax</h6>

```js
print(...args)
```

<h6>Parameters</h6>

`args` `...any` Variable length of argument to write.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.print("Hello", "World!", "\n")
```

## println()

Write arguments into the output, the default output is the log file or stdout if log filename is not set.

<h6>Syntax</h6>

```js
print(...args)
```

<h6>Parameters</h6>

`args` `...any` Variable length of argument to write.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.println("Hello", "World!")
```

## exec()

Run another JavaScript application.

<h6>Syntax</h6>

```js
exec(cmd, ...args)
```

<h6>Parameters</h6>

`cmd` `String` .js file path to run
`args` `...String` arguments to pass to the cmd.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.exec("/sbin/hello.js")
```

## daemonize()

Run the current script file as a daemon process with its parent process ID set to `1`.

<h6>Syntax</h6>

```js
daemonize(opts)
```

<h6>Parameters</h6>

- `opts` `Object` Options

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| reload             | Boolean    | enable hot-reload  |

If `reload` is set to `true`, the daemon process starts with a source code change watcher.
When the main source code file is modified, the current daemon process is stopped and restarted immediately to apply the changes.
This feature is useful during development and testing
but should not be enabled in production environments, as it requires an additional system resources to monitor file changes.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const p = require("@jsh/process")
if( p.ppid() == 1) {
    doBackgroundJob()
} else {
    p.daemonize()
    p.print("daemonize self, then exit")
}

function doBackgroundJob() {
    for(true){
        p.sleep(1000);
    }
}
```

## isDaemon()

Returns `true` if the parent process ID (`ppid()`) is `1`. This is equivalent to the condition `ppid() == 1`.

<h6>Syntax</h6>

```js
isDaemon()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Boolean

## isOrphan()

Returns `true` if the parent process ID is not assigned. This is equivalent to the condition `ppid() == 0xFFFFFFFF`.

<h6>Syntax</h6>

```js
isOrphan()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Boolean


## schedule()

Run the callback function according to the specified schedule.
The control flow remains blocked until the token's `stop()` method is invoked.

<h6>Syntax</h6>

```js
schedule(spec, callback)
```

<h6>Parameters</h6>

- `spec` `String` schedule spec. Refer to [Timer Schedule Spec.](/neo/timer/#timer-schedule-spec).
- `callback` `(time_epoch, token) => {}` The first parameter, `time_epoch`, is UNIX epoch timestamp in milliseconds unit.
    A callback function where the second parameter, `token`, can be used to stop the schedule.
    

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const {schedule} = require("@jsh/process");

var count = 0;
schedule("@every 2s", (ts, token)=>{
    count++;
    console.log(count, new Date(ts));
    if(count >= 5) token.stop();
})

// 1 2025-05-02 16:45:48
// 2 2025-05-02 16:45:50
// 3 2025-05-02 16:45:52
// 4 2025-05-02 16:45:54
// 5 2025-05-02 16:45:56
```

## sleep()

Pause the current control flow.

<h6>Syntax</h6>

```js
sleep(duration)
```

<h6>Parameters</h6>

`duration` `Number` sleep duration in milliseconds.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.sleep(1000) // 1 sec.
```

## kill()

Terminate a process using the specified process ID (pid).

<h6>Syntax</h6>

```js
kill(pid)
```

<h6>Parameters</h6>

`pid` `Number` pid of target process.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
p.kill(123)
```

## ps()

List all currently running processes.

<h6>Syntax</h6>

```js
ps()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

`Object[]`: Array of [Process](#Process) objects.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
p = require("@jsh/process")
list = p.ps()
for( const x of list ) {
    console.log(
        p.pid, 
        p.isOrphan() ? "-" : p.ppid,
        p.user, 
        p.name, 
        p.uptime)
}
```

## Process

Process information that returned by `ps()`.

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| pid                | Number     | process ID         |
| ppid               | Number     | process ID of the parent |
| user               | String     | username (e.g: `sys`)    |
| name               | String     | Script file name         |
| uptime             | String     | Elapse duration since started  |


## addCleanup()
Add a function to execute when the current JavaScript VM terminates.

<h6>Syntax</h6>

```js
addCleanup(fn)
```

<h6>Parameters</h6>

`fn` `()=>{}` callback function

<h6>Return value</h6>

`Number` A token for remove the cleanup callback.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
p = require("@jsh/process")
p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}

// run - 0
// run - 1
// run - 2
// terminated
```

## removeCleanup()

Remove a previously registered cleanup callback using the provided token.

<h6>Syntax</h6>

```js
removeCleanup(token)
```

<h6>Parameters</h6>

`token` `Number` token that returned by `addCleanup()`.

<h6>Return value</h6>

None.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,6]}
p = require("@jsh/process")
token = p.addCleanup(()=>{ console.log("terminated") })
for(i = 0; i < 3; i++) {
    console.log("run -", i)
}
p.removeCleanup(token)

// run - 0
// run - 1
// run - 2
```
