@echo off
setlocal
chcp 65001 >nul

echo ========================================
echo 설치 시작
echo ========================================

:: 현재 사용자명과 경로 동적 설정
set CURRENT_USER=%USERNAME%
set ANACONDA_PATH=C:\Users\%CURRENT_USER%\anaconda3
set MCP_PYTHON_PATH=%ANACONDA_PATH%\envs\mcp\python.exe
set CURRENT_DIR=%~dp0
set CLAUDE_CONFIG_DIR=%APPDATA%\Claude

echo 현재 사용자: %CURRENT_USER%
echo Anaconda 설치 경로: %ANACONDA_PATH%
echo MCP Python 경로: %MCP_PYTHON_PATH%
echo 현재 디렉토리: %CURRENT_DIR%
echo Claude 설정 디렉토리: %CLAUDE_CONFIG_DIR%
echo.

:check_anaconda
:: 1단계: Anaconda가 이미 설치되어 있는지 확인
echo ========================================
echo Anaconda 설치 확인 중...
echo ========================================

where conda >nul 2>nul
if %errorlevel% equ 0 (
    echo Anaconda/Miniconda가 이미 설치되어 있습니다.
    goto :setup_mcp
)

echo 1. Anaconda가 설치되어 있지 않습니다. 설치를 진행합니다...

:: 기존 설치 파일이 있는지 확인
if exist "%ANACONDA_PATH%\python.exe" (
    echo Anaconda가 이미 설치되어 있지만 PATH에 등록되지 않았습니다.
    goto :setup_path
)

echo 2. Anaconda 다운로드 중... (시간이 좀 걸릴 수 있습니다)
powershell -Command "Invoke-WebRequest -Uri 'https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Windows-x86_64.exe' -OutFile 'Anaconda3-installer.exe'"

if not exist "Anaconda3-installer.exe" (
    echo 다운로드에 실패했습니다. 네트워크 연결을 확인해주세요.
    pause
    exit /b 1
)

echo 3. Anaconda 설치 중... (무음 설치)
Anaconda3-installer.exe /InstallationType=JustMe /RegisterPython=1 /S /D=%ANACONDA_PATH%

:: 설치 완료 확인
echo 4. 설치 완료 대기 중...
timeout /t 10 /nobreak >nul

if not exist "%ANACONDA_PATH%\python.exe" (
    echo 오류: Anaconda 설치에 실패했습니다.
    echo 수동으로 설치를 확인해주세요.
    pause
    exit /b 1
)

echo 5. Anaconda 설치가 완료되었습니다.
echo 6. 설치 파일 삭제 중...
del Anaconda3-installer.exe

:setup_path
echo 7. PATH 환경변수 설정 중...
set PATH=%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\condabin;%PATH%

:: conda 초기화
echo 8. conda 초기화 중...
"%ANACONDA_PATH%\Scripts\conda.exe" init cmd.exe

echo 9. conda 설정 완료. MCP 환경 설정을 시작합니다...

:setup_mcp
echo ========================================
echo MCP 환경 설정 시작
echo ========================================

:: conda가 설치되어 있는지 다시 확인
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo conda 명령을 찾을 수 없습니다. PATH를 수동으로 설정합니다...
    set PATH=%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\condabin;%PATH%
)

echo 1. conda 명령줄 환경 초기화 중...
call conda init cmd.exe

echo 2. 'mcp' 가상 환경 생성 중... (Python 3.11)
call conda create -n mcp python=3.11 -y

echo 3. 'mcp' 가상 환경 활성화 중...
call conda activate mcp
if %errorlevel% neq 0 (
    echo 오류: 가상 환경 활성화에 실패했습니다.
    echo 새 명령 프롬프트를 열어서 다시 시도해주세요.
    pause
    exit /b 1
)

echo 4. pip 업그레이드 및 기본 패키지 설치 중...
python -m pip install --upgrade pip
pip install aiohttp
pip install httpx
pip install fastmcp
pip install beautifulsoup4

echo 5. requirements.txt 파일 확인 중...
if not exist requirements.txt (
    echo 경고: requirements.txt 파일이 현재 디렉토리에 없습니다.
    echo 기본 패키지만 설치되었습니다.
    goto :create_config
)

echo 6. requirements.txt에서 라이브러리 설치 중...
pip install -r requirements.txt --ignore-installed --no-deps

:create_config
echo ========================================
echo Claude Desktop 파일 설정 중...
echo ========================================

:: Claude 설정 디렉토리 생성
if not exist "%CLAUDE_CONFIG_DIR%" (
    echo 7. Claude 설정 디렉토리 생성 중...
    mkdir "%CLAUDE_CONFIG_DIR%"
)

:: Machbase.py 파일이 현재 디렉토리에 있는지 확인
if not exist "Machbase.py" (
    echo 경고: Machbase.py 파일이 현재 디렉토리에 없습니다.
    echo Machbase.py 파일을 현재 디렉토리에 넣고 다시 실행해주세요.
    pause
    exit /b 1
)

:: Machbase.py를 Claude 설정 디렉토리로 복사
echo 8. Machbase.py 파일을 Claude 설정 디렉토리로 복사 중...
copy "Machbase.py" "%CLAUDE_CONFIG_DIR%\Machbase.py"

if not exist "%CLAUDE_CONFIG_DIR%\Machbase.py" (
    echo 오류: Machbase.py 복사에 실패했습니다.
    pause
    exit /b 1
)

:: JSON 파일의 경로 설정 (Claude 설정 디렉토리 기준)
set JSON_PYTHON_PATH=%MCP_PYTHON_PATH:\=/%
set JSON_MACHBASE_PATH=%CLAUDE_CONFIG_DIR%\Machbase.py
set JSON_MACHBASE_PATH=%JSON_MACHBASE_PATH:\=/%

echo 9. claude_desktop_config.json 파일 생성 중...
(
echo {
echo     "mcpServers": {
echo       "machbase": {
echo         "command": "%JSON_PYTHON_PATH%",
echo         "args": ["%JSON_MACHBASE_PATH%"],
echo         "env": {
echo           "MACHBASE_HOST": "localhost",
echo           "MACHBASE_PORT": "5654"
echo         }
echo       }
echo     }
echo }
) > "%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"

if exist "%CLAUDE_CONFIG_DIR%\claude_desktop_config.json" (
    echo claude_desktop_config.json 파일이 성공적으로 생성되었습니다.
) else (
    echo 오류: config 파일 생성에 실패했습니다.
    pause
    exit /b 1
)

:complete
echo.
echo ========================================
echo 모든 설치 및 설정이 완료되었습니다!
echo ========================================
echo.
echo 설치된 프로그램:
echo - Anaconda Python
echo - MCP 환경 (Python 3.11)
echo.
echo 현재 사용자: %CURRENT_USER%
echo Python 실행 파일 경로: %MCP_PYTHON_PATH%
echo.
echo 파일 위치:
echo - Machbase.py: %CLAUDE_CONFIG_DIR%\Machbase.py
echo - claude_desktop_config.json: %CLAUDE_CONFIG_DIR%\claude_desktop_config.json
echo.
echo 설정 파일 내용:
type "%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"
echo.
echo 다음 명령어로 MCP 환경을 활성화할 수 있습니다:
echo conda activate mcp
echo.
echo 설치된 패키지 확인:
pip list
echo.
echo 주의사항:
echo 1. Claude Desktop을 재시작하여 새 설정을 적용하세요
echo 2. Anaconda를 새로 설치한 경우 새 명령 프롬프트를 열어서 conda 명령 확인
echo 3. 모든 파일이 Claude 설정 디렉토리로 이동되었습니다
echo.
pause