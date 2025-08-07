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
    if [ -f "$ANACONDA_PATH/etc/profile.d/conda.sh" ]; then
        . "$ANACONDA_PATH/etc/profile.d/conda.sh"
    fi
    
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
    if [ -f "$ANACONDA_PATH/etc/profile.d/conda.sh" ]; then
        . "$ANACONDA_PATH/etc/profile.d/conda.sh"
    else
        echo "Error: conda.sh not found at $ANACONDA_PATH/etc/profile.d/conda.sh"
        echo "Please check your Anaconda installation."
        exit 1
    fi
    
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
    echo "1. Launch Claude Desktop (from Applications menu or command line)"
    echo "2. Run 'conda activate mcp' in new terminal"
    echo "3. Make sure Machbase server is running"
    echo "4. You can now use MCP features in Claude Desktop"
    echo
    echo "Important notes:"
    echo "1. Restart Claude Desktop to apply new configuration"
    echo "2. If you newly installed Anaconda, open new terminal to check conda command"
    echo "3. All files have been moved to Claude configuration directory"
    echo "4. On Linux, you may need to add Anaconda to your PATH manually"
    echo "5. If conda command is not found, run: source ~/.bashrc"
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
# Linux-specific Claude config directory
if [ -d "$HOME/.config/Claude" ]; then
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
elif [ -d "$HOME/.config/claude" ]; then
    CLAUDE_CONFIG_DIR="$HOME/.config/claude"
else
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi

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
if command -v claude &> /dev/null; then
    echo "Claude Desktop is already installed."
    CLAUDE_INSTALLED=1
else
    echo "Claude Desktop is not installed."
    echo "Please install Claude Desktop from https://claude.ai/download"
    echo "After installation, run this script again."
    CLAUDE_INSTALLED=0
fi

# Step 1: Check and proceed with Anaconda installation
echo "========================================"
echo "Checking Anaconda installation..."
echo "========================================"

# Check if Anaconda is already installed
if command -v conda &> /dev/null; then
    echo "Anaconda/Miniconda is already installed and available in PATH."
    setup_mcp
elif [ -f "$ANACONDA_PATH/bin/conda" ]; then
    echo "Anaconda is installed but not in PATH. Setting up PATH..."
    setup_path
elif [ -f "$ANACONDA_PATH/bin/python" ]; then
    echo "Anaconda Python is installed but conda may not be properly set up."
    echo "Attempting to fix conda setup..."
    setup_path
else
    echo "1. Anaconda is not installed. Proceeding with installation..."
    
    echo "2. Downloading Anaconda... (This may take some time)"
    
    # Check Linux architecture
    if [[ $(uname -m) == "aarch64" ]]; then
        DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-aarch64.sh"
    else
        DOWNLOAD_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"
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
        
        echo "8. conda initialization complete."
        echo "9. Adding Anaconda to PATH permanently..."
        
        # Add Anaconda to .bashrc for permanent PATH setup
        if ! grep -q "anaconda3" ~/.bashrc; then
            echo "" >> ~/.bashrc
            echo "# Anaconda PATH setup" >> ~/.bashrc
            echo "export PATH=\"$ANACONDA_PATH/bin:\$PATH\"" >> ~/.bashrc
        fi
        
        # Load conda profile
        if [ -f "$ANACONDA_PATH/etc/profile.d/conda.sh" ]; then
            . "$ANACONDA_PATH/etc/profile.d/conda.sh"
        fi
        
        echo "10. Starting MCP environment setup..."
        setup_mcp
    fi