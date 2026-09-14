# Machbase Neo Shell Run Guide

`machbase-neo shell run <file>`은 주어진 파일의 여러 명령을 실행합니다.

## 스크립트 파일 만들기

아래와 같이 예제 스크립트 파일을 만듭니다.

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

## 스크립트 파일 실행

```sh
machbase-neo shell run batch.sh
```

**Result:**

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

## 대화형 모드에서 스크립트 실행

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

## 실행 가능한 스크립트 만들기

아래처럼 스크립트 파일의 첫 줄에 shebang(`#!`)을 추가합니다.

```sql
#!/usr/bin/env /path/to/machbase-neo shell run

-- Count 1
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.cos';

-- Count 2
SELECT count(*) FROM EXAMPLE WHERE name = 'wave.sin';
```

그리고 `chmod`로 실행 권한을 부여합니다.

```sh
$ chmod +x batch.sh
```

스크립트를 실행합니다.

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

## 빠른 참조

| 방법 | 명령 | 설명 |
|--------|---------|-------------|
| **직접 실행** | `machbase-neo shell run <file>` | SQL 스크립트 파일 직접 실행 |
| **대화형 모드** | `run ./script.sh` | 셸 세션 안에서 스크립트 실행 |
| **실행 가능 스크립트** | `./script.sh` | shebang 헤더가 있는 스크립트 실행 |
| **주석** | `#` 또는 `--` | 스크립트 파일에 주석 추가 |
| **문 종결** | `;` | 모든 문은 세미콜론으로 끝나야 함 |
