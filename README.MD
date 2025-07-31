## Overview

This project is an **MCP (Model Context Protocol)** based server that enables natural language-based database operations through integration between **Claude Desktop** and **Machbase Neo**.

When users request database operations in natural language through Claude Desktop's MCP connection, the MCP server converts these requests into Machbase Neo commands and executes them.

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

### Usage Examples

You can make natural language requests in Claude Desktop like these:

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
