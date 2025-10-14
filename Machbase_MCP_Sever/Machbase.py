#!/usr/bin/env python3
"""
Enhanced Machbase Neo MCP Server with FULL DOCUMENT CONTENT ACCESS and TQL EXECUTION
- Added full document content retrieval capability
- Added exact code block extraction
- Added section-by-section content access
- Added TQL file execution with automatic error cleanup
- Added version information tool
- Removed legacy search functions for cleaner interface
"""

import asyncio
import httpx
import json
import time
import logging
import re
import os
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlencode
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict, Counter

from fastmcp import FastMCP

# Version information
VERSION = "0.5.1"
BUILD_DATE = "2025-10-13"
DESCRIPTION = "Machbase Neo MCP Server"

# Machbase Neo default configuration
DEFAULT_MACHBASE_HOST = "localhost"
DEFAULT_MACHBASE_PORT = 5654

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("Machbase Neo")

def get_machbase_url(host: str = None, port: int = None) -> str:
    """Generate Machbase Neo server URL."""
    actual_host = host or DEFAULT_MACHBASE_HOST
    actual_port = port or DEFAULT_MACHBASE_PORT
    return f"http://{actual_host}:{actual_port}"

# =============================================================================
# Version and info tools
# =============================================================================

@mcp.tool()
async def get_version() -> str:
    """Get version information of the Machbase Neo MCP Server."""
    return f"""# Machbase Neo MCP Server Version Information

**Version**: {VERSION}
**Build Date**: {BUILD_DATE}
**Description**: {DESCRIPTION}

## Features
✓ Database table and tag management
✓ SQL execution
✓ TQL execution
✓ User Manual
✓ Error handling and debugging tools

## Tool Categories
- **Database Tools**: list_tables, list_table_tags, execute_sql_query
- **TQL Tools**: execute_tql_script
- **Document Tools**: get_full_document_content, extract_code_blocks, get_document_sections, list_available_documents
- **Utility Tools**: get_version, debug_mcp_status

For detailed usage information, use `debug_mcp_status()` tool.
"""

# =============================================================================
# Database related tools
# =============================================================================
@mcp.tool()
async def list_tables(
    host: str = None,
    port: int = None
) -> str:
    """Query available table list in Machbase Neo."""
    machbase_url = get_machbase_url(host, port)
    
    try:
        params = urlencode({
            "q": "SELECT name FROM M$SYS_TABLES WHERE name NOT LIKE 'M$%' AND name NOT LIKE '\_%' ORDER BY name",
            "format": "csv"
        })
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{params}",
                timeout=10.0
            )
            
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            if len(lines) < 2:
                return "No tables found."
            
            tables_info = []
            for line in lines[1:]:
                if line.strip():
                    table_name = line.strip()
                    tables_info.append(f"• {table_name}")
            
            if tables_info:
                table_list = "\n".join(tables_info)
                return f"Machbase Neo table list ({machbase_url}):\n\n{table_list}"
            else:
                return "No tables found."
        else:
            return f"Failed to retrieve table list: HTTP {response.status_code}\n{response.text}"
                
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})"
    except Exception as e:
        return f"Error occurred while retrieving table list: {str(e)}"

@mcp.tool()
async def list_table_tags(
    table_name: str,
    limit: int = 100,
    host: str = None,
    port: int = None
) -> str:
    """Get tag list from a specific table in Machbase Neo."""
    if not table_name:
        return "Please specify table name."
    
    table_name = table_name.upper()
    machbase_url = get_machbase_url(host, port)
    
    try:
        check_table_query = f"SELECT name FROM M$SYS_TABLES WHERE name NOT LIKE 'M$%' AND name NOT LIKE '\_%' AND name = '{table_name}' ORDER BY name"
        params = urlencode({
            "q": check_table_query,
            "format": "csv"
        })
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{params}",
                timeout=30.0
            )
            
            if response.status_code != 200:
                return f"Failed to check table existence: HTTP {response.status_code}"
            
            lines = response.text.strip().split('\n')
            if len(lines) < 2:
                return f"Table '{table_name}' does not exist."
        
        if limit > 0:
            tags_query = f"SELECT DISTINCT NAME FROM {table_name} ORDER BY NAME LIMIT {limit}"
        else:
            tags_query = f"SELECT DISTINCT NAME FROM {table_name} ORDER BY NAME"
            
        params = urlencode({
            "q": tags_query,
            "format": "csv"
        })
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{params}",
                timeout=30.0
            )
        
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            if len(lines) < 2:
                return f"No tags found in table '{table_name}' (NAME column)."
            
            tags = []
            for line in lines[1:]:
                if line.strip():
                    tag = line.strip()
                    tags.append(f"• {tag}")
            
            if tags:
                tag_count = len(tags)
                tag_list = "\n".join(tags)
                result = f"Tags in table '{table_name}' ({machbase_url}) :\n"
                result += f"Tag column: NAME\n"
                result += f"Found {tag_count} tags:\n\n{tag_list}"
                
                if limit > 0 and tag_count >= limit:
                    result += f"\n\n(Limited to {limit} tags. Use higher limit to see more.)"
                
                return result
            else:
                return f"No tags found in table '{table_name}' (NAME column)."
        else:
            return f"Failed to retrieve tags from table '{table_name}': HTTP {response.status_code}\n{response.text}"
            
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})"
    except httpx.TimeoutException:
        return f"Query timeout while getting tags from table '{table_name}'"
    except Exception as e:
        return f"Error occurred while retrieving tags from table '{table_name}': {str(e)}"

@mcp.tool()
async def execute_sql_query(
    sql_query: str,
    format: str = "csv",
    timeformat: str = "default",
    timezone: str = "Local",
    transpose: bool = False,
    host: str = None,
    port: int = None
) -> str:
    """
        Execute SQL query directly. 

        **IMPORTANT: Always check table structure first to understand column names, data types, and time intervals before execution.**
        **MANDATORY: Must use Machbase Neo documentation only. Use get_full_document_content or get_document_sections to find exact syntax before writing any queries. General SQL knowledge must not be used - only documented Machbase Neo syntax and functions are allowed.**
        **EXECUTION POLICY: Must test and verify all SQL queries before providing them as answers. Only provide successfully executed and validated code to users.**

        If no data is returned, it will be treated as a failure.
    """
    
    if not sql_query or not sql_query.strip():
        return "Please enter SQL query."
    
    machbase_url = get_machbase_url(host, port)
    
    try:
        params = {
            "q": sql_query,
            "format": "csv",
            "timeformat": timeformat,
            "timezone": timezone
        }
        if transpose:
            params["transpose"] = "true"
        encoded_params = urlencode(params)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{encoded_params}",
                timeout=30.0
            )
        
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            row_count = max(0, len(lines) - 1)
            
            if row_count == 0:
                return f"SQL query execution failed (no data returned)\nServer: {machbase_url}\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"
            
            if format.lower() == "json":
                headers = [h.strip() for h in lines[0].split(',')]
                rows = []
                for line in lines[1:]:
                    if line.strip():
                        row_data = [col.strip() for col in line.split(',')]
                        row_dict = {headers[i]: row_data[i] if i < len(row_data) else '' for i in range(len(headers))}
                        rows.append(row_dict)
                
                result = {
                    "query": sql_query,
                    "count": len(rows),
                    "data": rows
                }
                formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
                return f"SQL query execution result (JSON):\n\n```json\n{formatted_json}\n```"
            
            else:
                return f"SQL query execution result (CSV), {row_count} rows:\n\n```csv\n{response.text}\n```"
        
        else:
            return f"SQL query execution failed: HTTP {response.status_code}\n{response.text}\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"
    
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"
    except httpx.TimeoutException:
        return f"SQL query execution timeout (30 seconds)\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"
    except Exception as e:
        return f"Error occurred during SQL query execution: {str(e)}\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"

# =============================================================================
# TQL execution tools
# =============================================================================

@mcp.tool()
async def execute_tql_script(
    tql_content: str,
    host: str = None,
    port: int = None,
    timeout_seconds: int = 60
    
) -> str:
    """
        Execute TQL script via HTTP API. 

        **CRITICAL: Before executing, analyze target table structure and time intervals (minute/hour/daily data) as TQL operations heavily depend on correct time-based aggregations.**
        **MANDATORY: TQL syntax is unique to Machbase Neo. Must reference documentation using get_full_document_content or extract_code_blocks before writing any TQL scripts. Only use syntax and examples found in official documentation - no assumptions or general query language knowledge allowed.**
        **EXECUTION POLICY: Must test and verify all TQL scripts before providing them as answers. Only provide successfully executed and validated code to users.**

        Args:
            tql_content: TQL script content to execute
            host: Machbase Neo host (optional)
            port: Machbase Neo port (optional)
            timeout_seconds: HTTP request timeout in seconds (default: 60)
    """
    if not tql_content or not tql_content.strip():
        return "Please provide TQL script content to execute."
    
    machbase_url = get_machbase_url(host, port)
    execution_id = str(uuid.uuid4())[:8]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{machbase_url}/db/tql",
                content=tql_content,
                headers={"Content-Type": "text/plain"},
                timeout=timeout_seconds
            )

            if response.status_code == 200:
                if response.text.strip():
                    result = f"TQL execution completed successfully (ID: {execution_id})\n"
                    result += f"Server: {machbase_url}\n"
                    result += f"Status: HTTP {response.status_code}\n\n"
                    result += "=== RESPONSE ===\n"
                    result += response.text + "\n"
                else:
                    result = f"TQL execution failed (no data returned) (ID: {execution_id})\n"
                    result += f"Server: {machbase_url}\n"
                    result += f"Status: HTTP {response.status_code}\n\n"
                    result += "=== ERROR ===\n"
                    result += "Query executed successfully, but returned no data.\n"
                    result += "\n=== TQL CONTENT (for debugging) ===\n"
                    result += f"```tql\n{tql_content}\n```"
            else:
                result = f"TQL execution failed (ID: {execution_id})\n"
                result += f"Server: {machbase_url}\n"
                result += f"Status: HTTP {response.status_code}\n\n"
                if response.text.strip():
                    result += "=== ERROR RESPONSE ===\n"
                    result += response.text + "\n"
                result += "\n=== TQL CONTENT (for debugging) ===\n"
                result += f"```tql\n{tql_content}\n```"

            return result
                
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})\n" + \
               f"Execution ID: {execution_id}\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"
               
    except httpx.TimeoutException:
        return f"TQL execution timeout after {timeout_seconds} seconds (ID: {execution_id})\n" + \
               f"Server: {machbase_url}\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"
               
    except Exception as e:
        logger.error(f"TQL execution error: {e}")
        return f"TQL execution error (ID: {execution_id}): {str(e)}\n" + \
               f"Server: {machbase_url}\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"
               
# =============================================================================
# Document content access tools
# =============================================================================

@dataclass
class DocumentSection:
    """Document section representation"""
    title: str
    level: int  # Header level (1-6)
    content: str
    line_start: int
    line_end: int

@dataclass
class CodeBlock:
    """Code block representation"""
    language: str
    code: str
    line_start: int
    line_end: int

@dataclass
class FullDocument:
    """Complete document representation"""
    file_path: str
    relative_path: str
    title: str
    category: str
    full_content: str
    sections: List[DocumentSection]
    code_blocks: List[CodeBlock]
    word_count: int

class DocumentContentExtractor:
    """Extract complete document content with structure"""
    
    def __init__(self, docs_folder: str = None):
        script_dir = os.path.dirname(__file__) if '__file__' in globals() else "."
        
        # Find documentation folder
        possible_folders = [
            docs_folder,
            os.path.join(script_dir, "neo"),
            os.path.join(script_dir, "../neo"),
            "neo"
        ]
        
        self.docs_folder = None
        for folder in possible_folders:
            if folder and os.path.exists(folder):
                self.docs_folder = folder
                break
        
        if not self.docs_folder:
            self.docs_folder = os.path.join(script_dir, "neo")
        
        # Document cache
        self.document_cache: Dict[str, FullDocument] = {}
        self.file_index: Dict[str, str] = {}  # filename -> full_path
        
        self._build_file_index()

    def _build_file_index(self):
        """Build index of all markdown files"""
        if not os.path.exists(self.docs_folder):
            return
        
        for root, dirs, files in os.walk(self.docs_folder):
            for filename in files:
                if filename.endswith('.md'):
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, self.docs_folder)
                    
                    # Primary key: relative path only
                    self.file_index[relative_path] = full_path
                    
                    # Alias only if unique filename
                    if filename not in [os.path.basename(p) for p in self.file_index.values()]:
                        self.file_index[filename] = full_path

    def get_full_document(self, file_identifier: str) -> Optional[FullDocument]:
        """Get complete document content by filename or path"""
        # Try to find the file
        full_path = None
        
        if file_identifier in self.file_index:
            full_path = self.file_index[file_identifier]
        else:
            # Try case-insensitive search
            for key, path in self.file_index.items():
                if key.lower() == file_identifier.lower():
                    full_path = path
                    break
        
        if not full_path or not os.path.exists(full_path):
            return None
        
        # Check cache first
        if full_path in self.document_cache:
            return self.document_cache[full_path]
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content.strip()) < 10:
                return None
            
            # Extract document structure
            relative_path = os.path.relpath(full_path, self.docs_folder)
            title = self._extract_title(content, os.path.basename(full_path))
            category = self._detect_category(relative_path, content)
            sections = self._extract_sections(content)
            code_blocks = self._extract_code_blocks_detailed(content)
            
            doc = FullDocument(
                file_path=full_path,
                relative_path=relative_path,
                title=title,
                category=category,
                full_content=content,
                sections=sections,
                code_blocks=code_blocks,
                word_count=len(content.split())
            )
            
            # Cache the document
            self.document_cache[full_path] = doc
            
            return doc
            
        except Exception as e:
            logger.error(f"Error reading document {full_path}: {e}")
            return None
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract document title"""
        lines = content.split('\n')
        for line in lines[:10]:
            if line.startswith('# '):
                return line[2:].strip()
        
        # Fallback to filename
        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
        return ' '.join(word.capitalize() for word in title.split())
    
    def _detect_category(self, path: str, content: str) -> str:
        """Detect document category"""
        path_lower = path.lower()
        content_sample = content[:1000].lower()
        
        if "tql" in path_lower and "chart" in path_lower:
            return "tql_charts"
        elif "api" in path_lower and "example" in path_lower:
            return "api_examples"
        elif "tql" in path_lower:
            return "tql"
        elif "api" in path_lower:
            return "api"
        elif "sql" in path_lower:
            return "sql"
        elif "install" in path_lower or "setup" in content_sample:
            return "installation"
        elif "jsh" in path_lower:
            return "jsh"
        elif "bridge" in path_lower:
            return "bridges"
        elif "operation" in path_lower:
            return "operations"
        else:
            return "utilities"
    
    def _extract_sections(self, content: str) -> List[DocumentSection]:
        """Extract document sections with headers"""
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content_lines = []
        
        for i, line in enumerate(lines):
            header_match = re.match(r'^(#{1,6})\s+(.+)', line)
            
            if header_match:
                # Save previous section
                if current_section:
                    current_section.content = '\n'.join(current_content_lines)
                    current_section.line_end = i - 1
                    sections.append(current_section)
                
                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                current_section = DocumentSection(
                    title=title,
                    level=level,
                    content="",
                    line_start=i,
                    line_end=i
                )
                current_content_lines = []
            else:
                if current_section:
                    current_content_lines.append(line)
        
        # Add final section
        if current_section:
            current_section.content = '\n'.join(current_content_lines)
            current_section.line_end = len(lines) - 1
            sections.append(current_section)
        
        return sections
    
    def _extract_code_blocks_detailed(self, content: str) -> List[CodeBlock]:
        """Extract code blocks with detailed information"""
        code_blocks = []
        lines = content.split('\n')
        
        in_code_block = False
        current_language = ""
        current_code_lines = []
        start_line = 0
        
        for i, line in enumerate(lines):
            if line.startswith('```'):
                if not in_code_block:
                    # Starting code block
                    in_code_block = True
                    current_language = line[3:].strip()
                    current_code_lines = []
                    start_line = i
                else:
                    # Ending code block
                    in_code_block = False
                    code = '\n'.join(current_code_lines)
                    
                    if code.strip():
                        code_blocks.append(CodeBlock(
                            language=current_language,
                            code=code,
                            line_start=start_line,
                            line_end=i
                        ))
                    
                    current_language = ""
                    current_code_lines = []
            elif in_code_block:
                current_code_lines.append(line)
        
        return code_blocks
    
    def search_files(self, pattern: str) -> List[str]:
        """Search for files matching pattern"""
        pattern_lower = pattern.lower()
        matching_files = []
        
        for key in self.file_index.keys():
            if pattern_lower in key.lower():
                matching_files.append(key)
        
        return matching_files[:10]  # Limit results

# Global document extractor
document_extractor = DocumentContentExtractor()

# =============================================================================
# Document access tools
# =============================================================================
@mcp.tool()
async def list_available_documents() -> str:
    """List all available documentation files."""
    global document_extractor
    
    try:
        if not document_extractor.file_index:
            return "No documentation files found."
        
        # Group by category/directory
        files_by_dir = defaultdict(list)
        
        for filename, full_path in document_extractor.file_index.items():
            if filename.endswith('.md'):  # Only show .md files in main listing
                relative_path = os.path.relpath(full_path, document_extractor.docs_folder)
                directory = os.path.dirname(relative_path) if os.path.dirname(relative_path) else "root"
                files_by_dir[directory].append(filename)
        
        result = "# Available Documentation Files\n\n"
        result += f"**Documentation folder**: {document_extractor.docs_folder}\n"
        result += f"**Total files**: {len([f for f in document_extractor.file_index.keys() if f.endswith('.md')])}\n\n"
        
        for directory in sorted(files_by_dir.keys()):
            result += f"## {directory}/\n"
            for filename in sorted(set(files_by_dir[directory])):
                result += f"• {filename}\n"
            result += "\n"
        
        result += "---\n\n"
        result += "**Usage examples**:\n"
        result += "• `get_full_document_content('rollup.md')`\n"
        result += "• `extract_code_blocks('sql/rollup.md', 'sql')`\n"
        result += "• `get_document_sections('rollup.md', 'create')`\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return f"Error listing documents: {str(e)}"
    
@mcp.tool()
async def get_full_document_content(file_identifier: str) -> str:
    """Get complete content of a specific document file.
    
    **MANDATORY RESTRICTION**: 
    ALWAYS search non-dbms folders (operations/, sql/, tql/, api/, utilities/, etc.) FIRST for all questions.

    Use paths starting with "dbms/" ONLY when:
    - The user's question explicitly mentions "DBMS" keyword, OR
    - You have already searched at least one relevant non-dbms folder and found no information

    Before using dbms/, briefly state which non-dbms folder you searched.
    
    Args:
        file_identifier: relative path (e.g., "sql/rollup.md")
    """
    global document_extractor
    
    try:
        file_identifier = os.path.normpath(file_identifier)
        
        doc = document_extractor.get_full_document(file_identifier)
        
        if not doc:
            # Try to find similar files
            similar_files = document_extractor.search_files(file_identifier)
            if similar_files:
                return f"File '{file_identifier}' not found. Did you mean:\n" + \
                       "\n".join(f"• {f}" for f in similar_files) + \
                       "\n\nUse get_full_document_content() with exact filename."
            else:
                return f"File '{file_identifier}' not found in documentation."
        
        result = f"# {doc.title}\n\n"
        result += f"**File**: {doc.relative_path}\n"
        result += f"**Category**: {doc.category}\n"
        result += f"**Word Count**: {doc.word_count}\n\n"
        
        if doc.sections:
            result += f"**Sections**: {len(doc.sections)} sections found\n"
            for section in doc.sections[:5]:  # Show first 5 sections
                result += f"  • {section.title} (Level {section.level})\n"
            if len(doc.sections) > 5:
                result += f"  • ... and {len(doc.sections) - 5} more sections\n"
            result += "\n"
        
        if doc.code_blocks:
            result += f"**Code Blocks**: {len(doc.code_blocks)} code blocks found\n"
            languages = list(set(block.language for block in doc.code_blocks if block.language))
            if languages:
                result += f"  Languages: {', '.join(languages)}\n"
            result += "\n"
        
        result += "---\n\n"
        result += "## FULL DOCUMENT CONTENT\n\n"
        result += doc.full_content
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting full document content: {e}")
        return f"Error reading document: {str(e)}"

@mcp.tool()
async def extract_code_blocks(file_identifier: str, language: str = None) -> str:
    """Extract all code blocks from a document.
    
    **MANDATORY RESTRICTION**: 
    ALWAYS search non-dbms folders (operations/, sql/, tql/, api/, utilities/, etc.) FIRST for all questions.

    Use paths starting with "dbms/" ONLY when:
    - The user's question explicitly mentions "DBMS" keyword, OR
    - You have already searched at least one relevant non-dbms folder and found no information

    Before using dbms/, briefly state which non-dbms folder you searched.
    
    Args:
        file_identifier: Filename or path
        language: Filter by programming language (optional)
    """
    global document_extractor
    
    try:
        file_identifier = os.path.normpath(file_identifier)
        
        doc = document_extractor.get_full_document(file_identifier)
        
        if not doc:
            return f"File '{file_identifier}' not found."
        
        if not doc.code_blocks:
            return f"No code blocks found in '{file_identifier}'."
        
        # Filter by language if specified
        code_blocks = doc.code_blocks
        if language:
            code_blocks = [block for block in code_blocks if block.language.lower() == language.lower()]
            if not code_blocks:
                available_langs = list(set(block.language for block in doc.code_blocks if block.language))
                return f"No {language} code blocks found. Available languages: {', '.join(available_langs)}"
        
        result = f"# Code Blocks from {doc.title}\n\n"
        result += f"**File**: {doc.relative_path}\n"
        result += f"**Found**: {len(code_blocks)} code blocks"
        
        if language:
            result += f" (filtered by language: {language})"
        
        result += "\n\n---\n\n"
        
        for i, block in enumerate(code_blocks, 1):
            result += f"## Code Block {i}"
            
            if block.language:
                result += f" ({block.language})"
            
            result += f"\n**Lines**: {block.line_start + 1} - {block.line_end + 1}\n\n"
            
            result += f"```{block.language}\n{block.code}\n```\n\n---\n\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error extracting code blocks: {e}")
        return f"Error extracting code blocks: {str(e)}"

@mcp.tool()
async def get_document_sections(file_identifier: str, section_filter: str = None) -> str:
    """Get document content organized by sections.
    
    **MANDATORY RESTRICTION**: 
    ALWAYS search non-dbms folders (operations/, sql/, tql/, api/, utilities/, etc.) FIRST for all questions.

    Use paths starting with "dbms/" ONLY when:
    - The user's question explicitly mentions "DBMS" keyword, OR
    - You have already searched at least one relevant non-dbms folder and found no information

    Before using dbms/, briefly state which non-dbms folder you searched.
    
    Args:
        file_identifier: Filename or path
        section_filter: Filter sections containing this text (optional)
    """
    global document_extractor
    
    try:
        file_identifier = os.path.normpath(file_identifier)
        
        doc = document_extractor.get_full_document(file_identifier)
        
        if not doc:
            return f"File '{file_identifier}' not found."
        
        if not doc.sections:
            return f"No sections found in '{file_identifier}'."
        
        # Filter sections if specified
        sections = doc.sections
        if section_filter:
            sections = [s for s in sections if section_filter.lower() in s.title.lower() or section_filter.lower() in s.content.lower()]
            if not sections:
                return f"No sections found matching '{section_filter}'."
        
        result = f"# Sections from {doc.title}\n\n"
        result += f"**File**: {doc.relative_path}\n"
        result += f"**Found**: {len(sections)} sections"
        
        if section_filter:
            result += f" (filtered by: {section_filter})"
        
        result += "\n\n---\n\n"
        
        for i, section in enumerate(sections, 1):
            result += f"## Section {i}: {section.title}\n"
            result += f"**Level**: H{section.level}\n"
            result += f"**Lines**: {section.line_start + 1} - {section.line_end + 1}\n\n"
            result += f"{section.content}\n\n---\n\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting document sections: {e}")
        return f"Error getting document sections: {str(e)}"

@mcp.tool()
async def debug_mcp_status() -> str:
    """Check current status and performance of MCP server."""
    global document_extractor
    
    # Version information
    version_info = f"=== Machbase Neo MCP Server Status ===\n"
    version_info += f"Version: {VERSION}\n"
    version_info += f"Build Date: {BUILD_DATE}\n"
    version_info += f"Description: {DESCRIPTION}\n\n"
    
    # Database connection status
    db_status = ""
    try:
        machbase_url = get_machbase_url()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?q=SELECT 1 FROM M$SYS_TABLES LIMIT 1&format=csv", 
                timeout=5.0
            )
            if response.status_code == 200:
                db_status = f"[OK] Machbase Neo connection successful ({machbase_url})"
            else:
                db_status = f"[ERROR] Machbase Neo connection failed: HTTP {response.status_code}"
    except Exception as e:
        db_status = f"[ERROR] Machbase Neo connection error: {str(e)}"
    
    # Document extractor status
    doc_status = f"\n=== Document Content Access Status ===\n"
    doc_status += f"Documentation folder: {document_extractor.docs_folder}\n"
    doc_status += f"Folder exists: {os.path.exists(document_extractor.docs_folder)}\n"
    doc_status += f"Indexed files: {len(document_extractor.file_index)}\n"
    doc_status += f"Cached documents: {len(document_extractor.document_cache)}\n"
    
    doc_status += f"\n=== Available Tools ===\n"
    doc_status += f"Database Tools (3):\n"
    doc_status += f"  • list_tables() - Get all database tables\n"
    doc_status += f"  • list_table_tags() - Get tags from specific table\n"
    doc_status += f"  • execute_sql_query() - Execute SQL queries\n\n"
    
    doc_status += f"TQL Tools (1):\n"
    doc_status += f"  • execute_tql_script() - Execute TQL via HTTP API\n\n"
    
    doc_status += f"Document Tools (4):\n"
    doc_status += f"  • get_full_document_content() - Get complete document\n"
    doc_status += f"  • extract_code_blocks() - Extract code examples\n"
    doc_status += f"  • get_document_sections() - Get document sections\n"
    doc_status += f"  • list_available_documents() - List all files\n\n"
    
    doc_status += f"Utility Tools (2):\n"
    doc_status += f"  • get_version() - Show version information\n"
    doc_status += f"  • debug_mcp_status() - Check server status\n"
    
    return f"{version_info}{db_status}\n{doc_status}"

# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":
    logger.info(f"Starting Machbase Neo MCP server v{VERSION}")
    logger.info("Available tools:")
    logger.info("  Database: list_tables, list_table_tags, execute_sql_query")
    logger.info("  TQL: execute_tql_script")
    logger.info("  Documents: get_full_document_content, extract_code_blocks, get_document_sections, list_available_documents")
    logger.info("  Utility: get_version, debug_mcp_status")
    
    try:
        # Build file index
        document_extractor._build_file_index()
        logger.info(f"Document index ready: {len(document_extractor.file_index)} files indexed")
            
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
    
    mcp.run()