@echo off
setlocal
chcp 65001 >nul

echo ========================================
echo Starting installation
echo ========================================

:: Dynamic setup of current username and paths
:: Get actual user directory instead of relying on %USERNAME%
for /f "tokens=*" %%i in ('echo %USERPROFILE%') do set USER_DIR=%%i
for /f "tokens=3 delims=\" %%i in ("%USER_DIR%") do set CURRENT_USER=%%i
set ANACONDA_PATH=%USER_DIR%\anaconda3
set MCP_PYTHON_PATH=%ANACONDA_PATH%\envs\mcp\python.exe
set CURRENT_DIR=%~dp0
set CLAUDE_CONFIG_DIR=%APPDATA%\Claude

echo Current user: %CURRENT_USER%
echo Anaconda installation path: %ANACONDA_PATH%
echo MCP Python path: %MCP_PYTHON_PATH%
echo Current directory: %CURRENT_DIR%
echo Claude configuration directory: %CLAUDE_CONFIG_DIR%
echo.

:check_anaconda
:: Step 1: Check if Anaconda is already installed
echo ========================================
echo Checking Anaconda installation...
echo ========================================

where conda >nul 2>nul
if %errorlevel% equ 0 (
    echo Anaconda/Miniconda is already installed.
    goto :setup_mcp
)

echo 1. Anaconda is not installed. Proceeding with installation...

:: Check if existing installation files exist
if exist "%ANACONDA_PATH%\python.exe" (
    echo Anaconda is already installed but not registered in PATH.
    goto :setup_path
)

echo 2. Downloading Anaconda... (This may take some time)
powershell -Command "Invoke-WebRequest -Uri 'https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Windows-x86_64.exe' -OutFile 'Anaconda3-installer.exe'"

if not exist "Anaconda3-installer.exe" (
    echo Download failed. Please check your network connection.
    pause
    exit /b 1
)

echo 3. Installing Anaconda... (silent installation)
Anaconda3-installer.exe /InstallationType=JustMe /RegisterPython=1 /S /D=%ANACONDA_PATH%

:: Check installation completion
echo 4. Waiting for installation completion...
timeout /t 10 /nobreak >nul

if not exist "%ANACONDA_PATH%\python.exe" (
    echo Error: Anaconda installation failed.
    echo Please check the installation manually.
    pause
    exit /b 1
)

echo 5. Anaconda installation completed.
echo 6. Deleting installation file...
del Anaconda3-installer.exe

:setup_path
echo 7. Setting PATH environment variable...
set PATH=%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\condabin;%PATH%

:: Initialize conda
echo 8. Initializing conda...
"%ANACONDA_PATH%\Scripts\conda.exe" init cmd.exe

echo 9. conda setup complete. Starting MCP environment setup...

:setup_mcp
echo ========================================
echo Starting MCP environment setup
echo ========================================

:: Check if conda is installed again
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Cannot find conda command. Setting PATH manually...
    set PATH=%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\condabin;%PATH%
)

echo 1. Initializing conda command line environment...
call conda init cmd.exe

echo 2. Creating 'mcp' virtual environment... (Python 3.11)
call conda create -n mcp python=3.11 -y

echo 3. Activating 'mcp' virtual environment...
call conda activate mcp

if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    echo Please open a new command prompt and try again.
    pause
    exit /b 1
)

echo 4. Upgrading pip and installing basic packages...
python -m pip install --upgrade pip
pip install aiohttp
pip install httpx
pip install fastmcp
pip install beautifulsoup4

echo 5. Checking requirements.txt file...
if not exist requirements.txt (
    echo Warning: requirements.txt file not found in current directory.
    echo Only basic packages have been installed.
    goto :create_config
)

echo 6. Installing libraries from requirements.txt...
pip install -r requirements.txt --ignore-installed --no-deps

:create_config
echo ========================================
echo Setting up Claude Desktop files...
echo ========================================

:: Create Claude configuration directory
if not exist "%CLAUDE_CONFIG_DIR%" (
    echo 7. Creating Claude configuration directory...
    mkdir "%CLAUDE_CONFIG_DIR%"
)

:: Check if Machbase.py file exists in current directory
if not exist "Machbase.py" (
    echo Warning: Machbase.py file not found in current directory.
    echo Please place Machbase.py file in current directory and run again.
    pause
    exit /b 1
)

:: Copy Machbase.py to Claude configuration directory
echo 8. Copying Machbase.py file to Claude configuration directory...
copy "Machbase.py" "%CLAUDE_CONFIG_DIR%\Machbase.py"

if not exist "%CLAUDE_CONFIG_DIR%\Machbase.py" (
    echo Error: Failed to copy Machbase.py.
    pause
    exit /b 1
)

:: ========================================
:: NEW SECTION: Move neo folder
:: ========================================
echo 9. Checking neo folder...
if exist "neo" (
    echo Found neo folder in current directory.
    
    :: Check if destination neo folder already exists
    if exist "%CLAUDE_CONFIG_DIR%\neo" (
        echo Warning: %CLAUDE_CONFIG_DIR%\neo folder already exists.
        set /p choice="Do you want to overwrite it? (y/n): "
        if /i "!choice!" equ "y" (
            echo Removing existing neo folder...
            rmdir /s /q "%CLAUDE_CONFIG_DIR%\neo"
            if errorlevel 1 (
                echo Error: Failed to remove existing neo folder.
                pause
                exit /b 1
            )
        ) else (
            echo Skipping neo folder move...
            goto :create_json
        )
    )
    
    echo Moving neo folder to %CLAUDE_CONFIG_DIR%\neo...
    move "neo" "%CLAUDE_CONFIG_DIR%\neo"
    
    if errorlevel 1 (
        echo Error: Failed to move neo folder.
        pause
        exit /b 1
    ) else (
        echo Neo folder successfully moved to %CLAUDE_CONFIG_DIR%\neo
    )
) else (
    echo Warning: neo folder not found in current directory.
    echo Neo documentation will not be available.
)

:create_json
:: Set JSON file paths (relative to Claude configuration directory)
set JSON_PYTHON_PATH=%MCP_PYTHON_PATH:\=/%
set JSON_MACHBASE_PATH=%CLAUDE_CONFIG_DIR%\Machbase.py
set JSON_MACHBASE_PATH=%JSON_MACHBASE_PATH:\=/%

echo 10. Creating claude_desktop_config.json file...
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
    echo claude_desktop_config.json file created successfully.
) else (
    echo Error: Failed to create config file.
    pause
    exit /b 1
)

:complete
echo.
echo ========================================
echo All installation and setup completed!
echo ========================================
echo.
echo Installed programs:
echo - Anaconda Python
echo - MCP environment (Python 3.11)
echo.
echo Current user: %CURRENT_USER%
echo Python executable path: %MCP_PYTHON_PATH%
echo.
echo File locations:
echo - Machbase.py: %CLAUDE_CONFIG_DIR%\Machbase.py
echo - claude_desktop_config.json: %CLAUDE_CONFIG_DIR%\claude_desktop_config.json
if exist "%CLAUDE_CONFIG_DIR%\neo" (
echo - Machbase docs: %CLAUDE_CONFIG_DIR%\neo
) else (
echo - Machbase docs: NOT FOUND
)
echo.
echo Configuration file contents:
type "%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"
echo.
echo You can activate MCP environment with the following command:
echo conda activate mcp
echo.
echo Installed packages check:
pip list
echo.
echo Important notes:
echo 1. Restart Claude Desktop to apply new configuration
echo 2. If you newly installed Anaconda, open new command prompt to check conda command
echo 3. All files have been moved to Claude configuration directory
if exist "%CLAUDE_CONFIG_DIR%\neo" (
echo 4. Neo documentation is available at %CLAUDE_CONFIG_DIR%\neo
) else (
echo 4. Neo documentation was not found - please check if neo folder exists
)
echo.
pause