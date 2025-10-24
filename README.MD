


![Diagram](./Machbase_MCP_Sever/Machbase.png)




## Overview (Version 0.6.0)
[블로그 읽기 : 클로드 MCP를 Machbase Neo에 연동하고, AI스럽게 사용해보기](https://www.machbase.com/post/machbase)

This project is an **MCP (Model Context Protocol)** based server that enables natural language-based database operations through integration between **Claude Desktop** and **Machbase Neo**.

When users request database operations in natural language through Claude Desktop's MCP connection, the MCP server converts these requests into Machbase Neo commands and executes them.

[![Youtube Link](https://static.wixstatic.com/media/5583e0_7223d0cf33094256ad6c7e133136b144~mv2.png)](https://youtu.be/8cpaMTNHHiI?si=MX4tQK6Enh16hIUA)

### Key Features

* **Machbase Neo Official Documentation Search & AI-powered Explanations**
  * Claude directly searches Machbase documentation to provide accurate information
* **Real-time Database Integration** 
  * Table creation, data manipulation, complex query execution
  * Natural language → SQL conversion through Claude
* **Time Series Data Analysis & Querying**
  * Analysis of IoT sensor data, log data, and other time series data
* **Native Claude Desktop Integration**
  * No additional API keys required, leverages Claude Desktop's built-in capabilities

### How It Works

| Step | Component | Role | Communication |
|------|-----------|------|---------------|
| 1 | User | Input natural language request | Chat interface |
| 2 | Claude Desktop | Parse request & call MCP tools | MCP Protocol |
| 3 | MCP Server | Generate SQL & connect to Machbase | HTTP/REST API |
| 4 | Machbase Neo | Execute database operations | SQL queries |

**Data Flow:**

```
User Request → Claude Desktop → MCP Server → Machbase Neo
↑                                                      ↓
Response ← Claude Interpretation ← MCP Response ← Query Results
```

## Installation

### Quick Setup

#### Windows
1. **Install Claude Desktop** (if you don't have it yet)
    * https://claude.ai/download

2. **Download project from Git**
   ```bash
   git clone https://github.com/your-org/Machbase_MCP_Server.git
   cd Machbase_MCP_Server

3. **Run automatic installation**
   ```bash
   MCP_Install.bat

#### MacOS
1. **Download project from Git**
   ```bash
   git clone https://github.com/your-org/Machbase_MCP_Server.git
   cd Machbase_MCP_Server

2. **Run automatic installation**
   ```bash
   ./MCP_Install_mac.sh
    
> **After installation**: Restart Claude Desktop and test with "Show me the Machbase table list!"

### Manual Setup

For manual installation or if errors occur during the above installation process:

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-org/Machbase_MCP_Server.git
   cd Machbase_MCP_Server

2. **Python Environment Setup**
   ```bash
   # Using Conda
   conda create -n mcp python=3.11
   conda activate mcp
   
   # Using venv
   python -m venv mcp-env
   source mcp-env/bin/activate  # Linux/macOS
   # mcp-env\Scripts\activate   # Windows

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Claude Desktop and MCP Server Configuration**
   ```bash
   # Create C:/Users/Username/AppData/Roaming/Claude/claude_desktop_config.json
   # Machbase.py to C:/Users/Username/AppData/Roaming/Claude/

   {
       "mcpServers": {
         "machbase": {
           "command": "C:/Users/Username/anaconda3/envs/mcp/python.exe",
           "args": ["C:/Users/Username/AppData/Roaming/Claude/Machbase.py"],
           "env": {
             "MACHBASE_HOST": "localhost",
             "MACHBASE_PORT": "5654"
             }
         }
      }
   }
       
### Usage Examples ###

You can make natural language requests in Claude Desktop like these:

```text
"Create a table for temperature logs"
"Insert today's temperature: 28.4°C at 9am"
"Show me the latest 10 rows from temperature_log"
"Search the Machbase documentation for 'data insertion'"
"Drop the table named old_sensor_data"
"Show average temperature over the past 3 days"
"What tables exist in my Machbase database?"
"List all columns in sensor_data"
"Generate a trend report for device_001"
```

### Machbase MCP Server Evaluation Score ###

| Update Date| Version | Score | Average Response Time | Overall Evaluation | Model | 
|:------:|:----:|:----:|:--------:|-------------| :-------------:|
| 2025-08-28| v0.2.0 | 96 / 100 | 22 second | The quality of responses has improved compared to previous versions; <br> however, performance regarding TQL-related questions still appears to be less than perfect. | Claude Sonnet 4 |
| 2025-09-03| v0.3.0 | 99 / 100 | 61.5 second | The response time is much longer, but the explanation is far more accurate and detailed than the previous version. | Claude Sonnet 4 | 
| 2025-09-09| v0.4.0 | 141 / 150   | 45.29 second | The speed has improved compared to before, but the script and TQL parts are still somewhat lacking| Claude Sonnet 4 |
| 2025-10-14| v0.5.0 | 185 / 200   | 3 second | Thinking time significantly improved compared to before, but TQL and HTML-related areas still need improvement. | Claude Sonnet 4.5 |
| 2025-10-24| v0.6.0 | 196 / 200   | 2.6 second | Improved accuracy compared to version 0.5.0. DBMS-related content needs re-verification. Overall performance and response time have improved significantly. | Claude Sonnet 4.5 |





















