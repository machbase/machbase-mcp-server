#!/bin/bash

# UTF-8 encoding setup
export LANG=en_US.UTF-8

# Function definitions (define before use)
setup_path() {
    echo "Setting up Anaconda not registered in PATH..."
    export PATH="$ANACONDA_PATH/bin:$PATH"
    
    # Initialize conda
    echo "Initializing conda..."
    "$ANACONDA_PATH/bin/conda" init bash
    
    # Load conda profile
    source "$ANACONDA_PATH/etc/profile.d/conda.sh"
    
    echo "Existing Anaconda setup complete. Starting MCP environment setup..."
    setup_mcp
}

setup_mcp() {
    echo "========================================"
    echo "Starting MCP environment setup"
    echo "========================================"
    
    # Check if conda is installed again
    if ! command -v conda &> /dev/null; then
        echo "Cannot find conda command. Setting PATH manually..."
        export PATH="$ANACONDA_PATH/bin:$PATH"
    fi
    
    echo "1. Initializing conda command line environment..."
    source "$ANACONDA_PATH/etc/profile.d/conda.sh"
    
    echo "2. Creating 'mcp' virtual environment... (Python 3.11)"
    conda create -n mcp python=3.11 -y
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        echo "Conda installation may not be completely finished."
        exit 1
    fi
    
    echo "3. Activating 'mcp' virtual environment..."
    conda activate mcp
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate virtual environment."
        echo "Please open a new terminal and try again."
        exit 1
    fi
    
    echo "4. Upgrading pip and installing basic packages..."
    python -m pip install --upgrade pip
    pip install aiohttp
    pip install httpx
    pip install fastmcp
    pip install beautifulsoup4
    
    echo "5. Checking requirements.txt file..."
    if [ ! -f "requirements.txt" ]; then
        echo "Warning: requirements.txt file not found in current directory."
        echo "Only basic packages have been installed."
        create_config
    else
        echo "6. Installing libraries from requirements.txt..."
        pip install -r requirements.txt --ignore-installed --no-deps
        create_config
    fi
}

create_config() {
    echo "========================================"
    echo "Setting up Claude Desktop files..."
    echo "========================================"
    
    # Create Claude configuration directory
    if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
        echo "7. Creating Claude configuration directory..."
        mkdir -p "$CLAUDE_CONFIG_DIR"
    fi
    
    # Check if Machbase.py file exists in current directory
    if [ ! -f "Machbase.py" ]; then
        echo "Warning: Machbase.py file not found in current directory."
        echo "Please place Machbase.py file in current directory and run again."
        exit 1
    fi
    
    # Copy Machbase.py to Claude configuration directory
    echo "8. Copying Machbase.py file to Claude configuration directory..."
    cp "Machbase.py" "$CLAUDE_CONFIG_DIR/Machbase.py"
    
    if [ ! -f "$CLAUDE_CONFIG_DIR/Machbase.py" ]; then
        echo "Error: Failed to copy Machbase.py."
        exit 1
    fi
    
    # Set JSON file paths (relative to Claude configuration directory)
    JSON_PYTHON_PATH="$MCP_PYTHON_PATH"
    JSON_MACHBASE_PATH="$CLAUDE_CONFIG_DIR/Machbase.py"
    
    echo "9. Creating claude_desktop_config.json file..."
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
        echo "claude_desktop_config.json file created successfully."
    else
        echo "Error: Failed to create config file."
        exit 1
    fi
    
    complete
}

complete() {
    echo
    echo "========================================"
    echo "All installation and setup completed!"
    echo "========================================"
    echo
    echo "Installed programs:"
    echo "- Claude Desktop"
    echo "- Anaconda Python"
    echo "- MCP environment (Python 3.11)"
    echo
    echo "Current user: $CURRENT_USER"
    echo "Python executable path: $MCP_PYTHON_PATH"
    echo
    echo "File locations:"
    echo "- Machbase.py: $CLAUDE_CONFIG_DIR/Machbase.py"
    echo "- claude_desktop_config.json: $CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    echo
    echo "Configuration file contents:"
    cat "$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
    echo
    echo "You can activate MCP environment with the following command:"
    echo "conda activate mcp"
    echo
    echo "Installed packages check:"
    pip list
    echo
    echo "Usage instructions:"
    echo "1. Launch Claude Desktop (from Applications folder or Launchpad)"
    echo "2. Run 'conda activate mcp' in new terminal"
    echo "3. Make sure Machbase server is running"
    echo "4. You can now use MCP features in Claude Desktop"
    echo
    echo "Important notes:"
    echo "1. Restart Claude Desktop to apply new configuration"
    echo "2. If you newly installed Anaconda, open new terminal to check conda command"
    echo "3. All files have been moved to Claude configuration directory"
    echo
}

# Main execution section (placed after function definitions)
echo "========================================"
echo "Starting Claude Desktop + Anaconda complete installation"
echo "========================================"

# Dynamic setup of current username and paths
CURRENT_USER=$(whoami)
ANACONDA_PATH="$HOME/anaconda3"
MCP_PYTHON_PATH="$ANACONDA_PATH/envs/mcp/bin/python"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"

echo "Current user: $CURRENT_USER"
echo "Anaconda installation path: $ANACONDA_PATH"
echo "MCP Python path: $MCP_PYTHON_PATH"
echo "Current directory: $CURRENT_DIR"
echo "Claude configuration directory: $CLAUDE_CONFIG_DIR"
echo

# Step 0: Check and download Claude Desktop
echo "========================================"
echo "Checking Claude Desktop installation..."
echo "========================================"

# Check if Claude Desktop is already installed
CLAUDE_INSTALLED=0
if [ -d "/Applications/Claude.app" ]; then
    echo "Claude Desktop is already installed."
    CLAUDE_INSTALLED=1
fi

if [ $CLAUDE_INSTALLED -eq 0 ]; then
    echo "1. Claude Desktop is not installed. Proceeding with download..."
    
    # Check macOS architecture and download appropriate DMG file
    if [[ $(uname -m) == "arm64" ]]; then
        CLAUDE_URL="https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest/Claude.dmg"
        echo "2. Downloading Claude Desktop (Apple Silicon)..."
    else
        CLAUDE_URL="https://storage.googleapis.com/claude-desktop/claude-desktop-latest-x64.dmg"
        echo "2. Downloading Claude Desktop (Intel)..."
    fi
    
    curl -L -o Claude-Desktop.dmg "$CLAUDE_URL"
    
    if [ ! -f "Claude-Desktop.dmg" ]; then
        echo "Download failed. Please download manually."
        echo "Download from https://claude.ai/download and install."
        echo "Press Enter to continue..."
        read
    else
        echo "3. Installing Claude Desktop..."
        echo "Mounting DMG file..."
        
        # Mount DMG file
        hdiutil attach Claude-Desktop.dmg -quiet

        # Automatically search for Claude.app path under /Volumes/
        APP_PATH=$(find /Volumes/ -maxdepth 2 -type d -name "Claude.app" | head -n 1)

        if [ -d "$APP_PATH" ]; then
            echo "Copying Claude.app to Applications folder..."
            cp -R "$APP_PATH" "/Applications/"
            # Extract volume path
            VOLUME_PATH=$(dirname "$APP_PATH")
            echo "Unmounting DMG file..."
            hdiutil detach "$VOLUME_PATH" -quiet
        else
            echo "Error: Cannot find Claude.app in /Volumes/."
            exit 1
        fi
        
        # Delete downloaded DMG file
        echo "4. Deleting installation file..."
        rm Claude-Desktop.dmg
        
        echo "Claude Desktop installation completed."
        echo "You can run it from Applications folder or Launchpad."
        echo
    fi
else
    echo "Claude Desktop installation check completed."
    echo
fi

# Step 1: Check and proceed with Anaconda installation
echo "========================================"
echo "Checking Anaconda installation..."
echo "========================================"

# Check if Anaconda is already installed
if command -v conda &> /dev/null; then
    echo "Anaconda/Miniconda is already installed."
    setup_mcp
else
    echo "1. Anaconda is not installed. Proceeding with installation..."
    
    # Check if existing installation files exist
    if [ -f "$ANACONDA_PATH/bin/python" ]; then
        echo "Anaconda is already installed but not registered in PATH."
        setup_path
    else
        echo "2. Downloading Anaconda... (This may take some time)"
        
        # Check macOS architecture
        if [[ $(uname -m) == "arm64" ]]; then
            DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-arm64.sh"
        else
            DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-MacOSX-x86_64.sh"
        fi
        
        curl -L -o Anaconda3-installer.sh "$DOWNLOAD_URL"
        
        if [ ! -f "Anaconda3-installer.sh" ]; then
            echo "Download failed. Please check your network connection."
            exit 1
        fi
        
        echo "3. Installing Anaconda... (silent installation)"
        chmod +x Anaconda3-installer.sh
        bash Anaconda3-installer.sh -b -p "$ANACONDA_PATH"
        
        # Check installation completion
        if [ ! -f "$ANACONDA_PATH/bin/python" ]; then
            echo "Error: Anaconda installation failed."
            exit 1
        fi
        
        echo "4. Anaconda installation completed."
        echo "5. Deleting installation file..."
        rm Anaconda3-installer.sh
        
        # PATH setup and initialization
        echo "6. Setting PATH environment variable..."
        export PATH="$ANACONDA_PATH/bin:$PATH"
        
        echo "7. Initializing conda..."
        "$ANACONDA_PATH/bin/conda" init bash
        
        echo "8. conda initialization complete. Starting MCP environment setup..."
        
        # Load conda profile
        source "$ANACONDA_PATH/etc/profile.d/conda.sh"
        
        setup_mcp
    fi
fi