#!/bin/bash

# UTF-8 인코딩 설정
export LANG=ko_KR.UTF-8

# 함수 정의들 (사용하기 전에 먼저 정의)
setup_path() {
    echo "PATH에 등록되지 않은 Anaconda를 설정 중..."
    export PATH="$ANACONDA_PATH/bin:$PATH"
    
    # conda 초기화
    echo "conda 초기화 중..."
    "$ANACONDA_PATH/bin/conda" init bash
    
    # conda 프로필 로드
    source "$ANACONDA_PATH/etc/profile.d/conda.sh"
    
    echo "기존 Anaconda 설정 완료. MCP 환경 설정을 시작합니다..."
    setup_mcp
}

setup_mcp() {
    echo "========================================"
    echo "MCP 환경 설정 시작"
    echo "========================================"
    
    # conda가 설치되어 있는지 다시 확인
    if ! command -v conda &> /dev/null; then
        echo "conda 명령을 찾을 수 없습니다. PATH를 수동으로 설정합니다..."
        export PATH="$ANACONDA_PATH/bin:$PATH"
    fi
    
    echo "1. conda 명령줄 환경 초기화 중..."
    source "$ANACONDA_PATH/etc/profile.d/conda.sh"
    
    echo "2. 'mcp' 가상 환경 생성 중... (Python 3.11)"
    conda create -n mcp python=3.11 -y
    if [ $? -ne 0 ]; then
        echo "오류: 가상 환경 생성에 실패했습니다."
        echo "conda 설치가 완전히 완료되지 않았을 수 있습니다."
        exit 1
    fi
    
    echo "3. 'mcp' 가상 환경 활성화 중..."
    conda activate mcp
    if [ $? -ne 0 ]; then
        echo "오류: 가상 환경 활성화에 실패했습니다."
        echo "새 터미널을 열어서 다시 시도해주세요."
        exit 1
    fi
    
    echo "4. pip 업그레이드 및 기본 패키지 설치 중..."
    python -m pip install --upgrade pip
    pip install aiohttp
    pip install httpx
    pip install fastmcp
    pip install beautifulsoup4
    
    echo "5. requirements.txt 파일 확인 중..."
    if [ ! -f "requirements.txt" ]; then
        echo "경고: requirements.txt 파일이 현재 디렉토리에 없습니다."
        echo "기본 패키지만 설치되었습니다."
        create_config
    else
        echo "6. requirements.txt에서 라이브러리 설치 중..."
        pip install -r requirements.txt --ignore-installed --no-deps
        create_config
    fi
}

create_config() {
    echo "========================================"
    echo "Claude Desktop 파일 설정 중..."
    echo "========================================"
    
    # Claude 설정 디렉토리 생성
    if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
        echo "7. Claude 설정 디렉토리 생성 중..."
        mkdir -p "$CLAUDE_CONFIG_DIR"
    fi
    
    # Machbase.py 파일이 현재 디렉토리에 있는지 확인
    if [ ! -f "Machbase.py" ]; then
        echo "경고: Machbase.py 파일이 현재 디렉토리에 없습니다."
        echo "Machbase.py 파일을 현재 디렉토리에 넣고 다시 실행해주세요."
        exit 1
    fi
    
    # Machbase.py를 Claude 설정 디렉토리로 복사
    echo "8. Machbase.py 파일을 Claude 설정 디렉토리로 복사 중..."
    cp "Machbase.py" "$CLAUDE_CONFIG_DIR/Machbase.py"
    
    if [ ! -f "$CLAUDE_CONFIG_DIR/Machbase.py" ]; then
        echo "오류: Machbase.py 복사에 실패했습니다."
        exit 1
    fi
    
    # JSON 파일의 경로 설정 (Claude 설정 디렉토리 기준)
    JSON_PYTHON_PATH="$MCP_PYTHON_PATH"
    JSON_MACHBASE_PATH="$CLAUDE_CONFIG_DIR/Machbase.py"
    
    echo "9. claude_desktop_config.json 파일 생성 중..."
    cat > "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" << EOF
{
    "mcpServers": {
      "machbase": {
        "command": "$JSON_PYTHON_PATH",
        "args": ["$JSON_MACHBASE_PATH"],
        "env": {
          "MACHBASE_HOST": "localhost",
          "MACHBASE_PORT": "5654"
        }
      }
    }
}
EOF
    
    if [ -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
        echo "claude_desktop_config.json 파일이 성공적으로 생성되었습니다."
    else
        echo "오류: config 파일 생성에 실패했습니다."
        exit 1
    fi
    
    complete
}

complete() {
    echo
    echo "========================================"
    echo "모든 설치 및 설정이 완료되었습니다!"
    echo "========================================"
    echo
    echo "설치된 프로그램:"
    echo "- Claude Desktop"
    echo "- Anaconda Python"
    echo "- MCP 환경 (Python 3.11)"
    echo
    echo "현재 사용자: $CURRENT_USER"
    echo "Python 실행 파일 경로: $MCP_PYTHON_PATH"
    echo
    echo "파일 위치:"
    echo "- Machbase.py: $CLAUDE_CONFIG_DIR/Machbase.py"
    echo "- claude_desktop_config.json: $CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    echo
    echo "설정 파일 내용:"
    cat "$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    echo
    echo "다음 명령어로 MCP 환경을 활성화할 수 있습니다:"
    echo "conda activate mcp"
    echo
    echo "설치된 패키지 확인:"
    pip list
    echo
    echo "사용 방법:"
    echo "1. Claude Desktop을 실행하세요 (Applications 폴더 또는 Launchpad에서)"
    echo "2. 새 터미널에서 'conda activate mcp' 실행"
    echo "3. Machbase 서버가 실행 중인지 확인하세요"
    echo "4. Claude Desktop에서 MCP 기능을 사용할 수 있습니다"
    echo
    echo "주의사항:"
    echo "1. Claude Desktop을 재시작하여 새 설정을 적용하세요"
    echo "2. Anaconda를 새로 설치한 경우 새 터미널을 열어서 conda 명령 확인"
    echo "3. 모든 파일이 Claude 설정 디렉토리로 이동되었습니다"
    echo
}

# 메인 실행 부분 (함수 정의 후에 위치)
echo "========================================"
echo "Claude Desktop + Anaconda 완전 설치 시작"
echo "========================================"

# 현재 사용자명과 경로 동적 설정
CURRENT_USER=$(whoami)
ANACONDA_PATH="$HOME/anaconda3"
MCP_PYTHON_PATH="$ANACONDA_PATH/envs/mcp/bin/python"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"

echo "현재 사용자: $CURRENT_USER"
echo "Anaconda 설치 경로: $ANACONDA_PATH"
echo "MCP Python 경로: $MCP_PYTHON_PATH"
echo "현재 디렉토리: $CURRENT_DIR"
echo "Claude 설정 디렉토리: $CLAUDE_CONFIG_DIR"
echo

# 0단계: Claude Desktop 설치 확인 및 다운로드
echo "========================================"
echo "Claude Desktop 설치 확인 중..."
echo "========================================"

# Claude Desktop이 이미 설치되어 있는지 확인
CLAUDE_INSTALLED=0
if [ -d "/Applications/Claude.app" ]; then
    echo "Claude Desktop이 이미 설치되어 있습니다."
    CLAUDE_INSTALLED=1
fi

if [ $CLAUDE_INSTALLED -eq 0 ]; then
    echo "1. Claude Desktop이 설치되어 있지 않습니다. 다운로드를 진행합니다..."
    
    # macOS 아키텍처 확인하여 적절한 DMG 파일 다운로드
    if [[ $(uname -m) == "arm64" ]]; then
        CLAUDE_URL="https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest/Claude.dmg"
        echo "2. Claude Desktop (Apple Silicon) 다운로드 중..."
    else
        CLAUDE_URL="https://storage.googleapis.com/claude-desktop/claude-desktop-latest-x64.dmg"
        echo "2. Claude Desktop (Intel) 다운로드 중..."
    fi
    
    curl -L -o Claude-Desktop.dmg "$CLAUDE_URL"
    
    if [ ! -f "Claude-Desktop.dmg" ]; then
        echo "다운로드에 실패했습니다. 수동으로 다운로드해주세요."
        echo "https://claude.ai/download 에서 다운로드 후 설치해주세요."
        echo "계속 진행하려면 Enter를 누르세요..."
        read
    else
        echo "3. Claude Desktop 설치 중..."
        echo "DMG 파일을 마운트합니다..."
        
        # DMG 파일 마운트
        hdiutil attach Claude-Desktop.dmg -quiet

        # /Volumes/ 아래에서 Claude.app 경로 자동 탐색
        APP_PATH=$(find /Volumes/ -maxdepth 2 -type d -name "Claude.app" | head -n 1)

        if [ -d "$APP_PATH" ]; then
            echo "Claude.app을 Applications 폴더로 복사 중..."
            cp -R "$APP_PATH" "/Applications/"
            # 볼륨 경로 추출
            VOLUME_PATH=$(dirname "$APP_PATH")
            echo "DMG 파일을 언마운트합니다..."
            hdiutil detach "$VOLUME_PATH" -quiet
        else
            echo "오류: Claude.app을 /Volumes/에서 찾을 수 없습니다."
            exit 1
        fi
        
        # 다운로드한 DMG 파일 삭제
        echo "4. 설치 파일 삭제 중..."
        rm Claude-Desktop.dmg
        
        echo "Claude Desktop 설치가 완료되었습니다."
        echo "Applications 폴더 또는 Launchpad에서 실행할 수 있습니다."
        echo
    fi
else
    echo "Claude Desktop 설치 확인 완료."
    echo
fi

# 1단계: Anaconda 설치 확인 및 진행
echo "========================================"
echo "Anaconda 설치 확인 중..."
echo "========================================"

# Anaconda가 이미 설치되어 있는지 확인
if command -v conda &> /dev/null; then
    echo "Anaconda/Miniconda가 이미 설치되어 있습니다."
    setup_mcp
else
    echo "1. Anaconda가 설치되어 있지 않습니다. 설치를 진행합니다..."
    
    # 기존 설치 파일이 있는지 확인
    if [ -f "$ANACONDA_PATH/bin/python" ]; then
        echo "Anaconda가 이미 설치되어 있지만 PATH에 등록되지 않았습니다."
        setup_path
    else
        echo "2. Anaconda 다운로드 중... (시간이 좀 걸릴 수 있습니다)"
        
        # macOS 아키텍처 확인
        if [[ $(uname -m) == "arm64" ]]; then
            DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-arm64.sh"
        else
            DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-x86_64.sh"
        fi
        
        curl -L -o Anaconda3-installer.sh "$DOWNLOAD_URL"
        
        if [ ! -f "Anaconda3-installer.sh" ]; then
            echo "다운로드에 실패했습니다. 네트워크 연결을 확인해주세요."
            exit 1
        fi
        
        echo "3. Anaconda 설치 중... (무음 설치)"
        chmod +x Anaconda3-installer.sh
        bash Anaconda3-installer.sh -b -p "$ANACONDA_PATH"
        
        # 설치 완료 확인
        if [ ! -f "$ANACONDA_PATH/bin/python" ]; then
            echo "오류: Anaconda 설치에 실패했습니다."
            exit 1
        fi
        
        echo "4. Anaconda 설치가 완료되었습니다."
        echo "5. 설치 파일 삭제 중..."
        rm Anaconda3-installer.sh
        
        # PATH 설정 및 초기화
        echo "6. PATH 환경변수 설정 중..."
        export PATH="$ANACONDA_PATH/bin:$PATH"
        
        echo "7. conda 초기화 중..."
        "$ANACONDA_PATH/bin/conda" init bash
        
        echo "8. conda 초기화 완료. MCP 환경 설정을 시작합니다..."
        
        # conda 프로필 로드
        source "$ANACONDA_PATH/etc/profile.d/conda.sh"
        
        setup_mcp
    fi
fi