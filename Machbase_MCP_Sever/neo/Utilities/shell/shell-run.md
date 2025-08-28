---
title: Run sql file
type: docs
weight: 20
---

`machbase-neo shell run <file>` executes multiple commands in the given file.

## Make a script file

Make an example script file like below.

- `cat batch.sh`

```sql
#
# comments starts with `#` or `--`
# A statement should be ends with semi-colon `;`
#

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE 
  WHERE name = 'wave.sin'
;
```

## Run the script file

```sh
machbase-neo shell run batch.sh
```

- result

```
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
 ROWNUM  COUNT(*)
──────────────────
      1  2175
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
 ROWNUM  COUNT(*)
──────────────────
      1  8175
a row fetched.
```

## Run the script in interactive mode

```sh
$ machbase-neo shell

machbase-neo» run ./b.sh;
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
╭────────┬──────────╮
│ ROWNUM │ COUNT(*) │
├────────┼──────────┤
│      1 │ 2175     │
╰────────┴──────────╯
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
╭────────┬──────────╮
│ ROWNUM │ COUNT(*) │
├────────┼──────────┤
│      1 │ 8175     │
╰────────┴──────────╯
a row fetched.
```

## Make an executable script

Add shebang(`#!`) as the first line of script file like below.

```sql
#!/usr/bin/env /path/to/machbase-neo shell run

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin';
```

Then `chmod` allowing executable permission.

```sh
$ chmod +x batch.sh
```

Execute the script.

```sh
$ ./batch.sh

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos'
 ROWNUM  COUNT(*)
──────────────────
      1  2175
a row fetched.

SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin'
 ROWNUM  COUNT(*)
──────────────────
      1  8175
a row fetched.
```