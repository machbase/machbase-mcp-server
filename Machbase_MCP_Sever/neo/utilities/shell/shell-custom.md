# Machbase Neo Custom Shell Guide

사용자는 명령행 셸을 직접 구성해 웹 UI에서 열 수 있습니다.

웹 UI에서 *SHELL*을 열거나 터미널에서 `machbase-neo shell`을 실행한 뒤, `shell` 명령으로 사용자 정의 셸을 추가·제거합니다.

이 예제에서는 *nix 사용자를 위해 `/bin/bash`(또는 `/bin/zsh`)를, Windows 사용자를 위해 `cmd.exe`를 실행하는 사용자 정의 셸을 추가하는 방법을 보여줍니다. 프로그래밍 언어의 REPL, 다른 데이터베이스의 명령행 인터페이스, 서버에 접속하는 ssh 명령 등도 추가할 수 있습니다.

## 사용자 정의 셸 추가

### 사용자 정의 셸 등록

1. 가장 왼쪽의 메뉴 아이콘을 선택합니다.

2. 그리고 좌측 상단 창에서 `+` 아이콘을 클릭합니다.

3. 원하는 "Display name"을 정하고 "Command" 칸에 절대 경로와 플래그를 입력합니다. 예를 들어 macOS에서 'zsh'를 명령행으로 설정하려면 프로그램의 절대 경로를 넣고 "Save"를 클릭합니다.

**설정 옵션:**
- **Name**: 표시 이름. (machbase-neo가 향후 사용을 위해 예약한 일부 단어를 제외하면 어떤 텍스트든 가능합니다)
- **Command**: 인자를 포함한 실행 파일의 전체 경로
- **Theme**: 터미널 색상 테마

**사용자 정의 명령 예시:**
- Windows Cmd.exe: `C:\Windows\System32\cmd.exe`
- Linux bash: `/bin/bash`
- macOS의 PostgreSQL 클라이언트: `/opt/homebrew/bin/psql postgres`

### 사용자 정의 셸 사용

- 메인 에디터 영역에서 사용자 정의 셸을 엽니다.

- 콘솔 영역에서 사용자 정의 셸을 엽니다.

## 명령행 관리

사용자 정의 셸은 machbase-neo shell 명령행 인터페이스로 관리할 수 있습니다.

### 새 사용자 정의 셸 추가

`shell add <name> <command and args>`를 사용합니다. 이름과 인자를 포함한 실행 명령을 자유롭게 지정할 수 있지만 기본 셸 이름 `SHELL`은 예약되어 있습니다.

```sh
machbase-neo» shell add bashterm /bin/bash;
added
```

```sh
machbase-neo» shell add terminal /bin/zsh -il;
added
```

```sh
machbase-neo» shell add console C:\Windows\System32\cmd.exe;
added
```

### 등록된 셸 목록 보기

```sh
machbase-neo» shell list;
┌────────┬────────────────────────────┬────────────┬──────────────┐
│ ROWNUM │ ID                         │ NAME       │ COMMAND      │
├────────┼────────────────────────────┼────────────┼──────────────┤
│      1 │ 11F4AFFD-2A9B-4FC5-BB20-637│ BASHTERM   │ /bin/bash    │
│      2 │ 11F4AFFD-2A9B-4FC5-BB20-638│ TERMINAL   │ /bin/zsh -il │
└────────┴────────────────────────────┴────────────┴──────────────┘
```

### 사용자 정의 셸 삭제

```sh
machbase-neo» shell del 11F4AFFD-2A9B-4FC5-BB20-637;
deleted
```

## 빠른 참조

| 방법 | 명령 | 설명 |
|--------|---------|-------------|
| **웹 UI 등록** | UI 메뉴 → `+` 아이콘 | 웹 인터페이스로 사용자 정의 셸 등록 |
| **명령행 추가** | `shell add <name> <command>` | 명령행으로 사용자 정의 셸 추가 |
| **셸 목록** | `shell list` | 등록된 모든 사용자 정의 셸 표시 |
| **셸 삭제** | `shell del <id>` | ID로 사용자 정의 셸 제거 |
| **예약된 이름** | `SHELL` | 기본 셸 이름은 사용할 수 없음 |
