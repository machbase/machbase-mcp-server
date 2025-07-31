#!/usr/bin/env python3
"""
Integrated Machbase Neo MCP Server
- Machbase Neo database connection and query execution
- Machbase official documentation search (smart category-based)
- Table management and SQL execution
"""

import asyncio
import aiohttp
import httpx
import json
import time
import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urljoin, urlparse
from dataclasses import dataclass
from bs4 import BeautifulSoup

from fastmcp import FastMCP

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("Machbase Neo")

# Machbase Neo default configuration
DEFAULT_MACHBASE_HOST = "localhost"
DEFAULT_MACHBASE_PORT = 5654

def get_machbase_url(host: str = None, port: int = None) -> str:
    """Generate Machbase Neo server URL."""
    actual_host = host or DEFAULT_MACHBASE_HOST
    actual_port = port or DEFAULT_MACHBASE_PORT
    return f"http://{actual_host}:{actual_port}"

# =============================================================================
# Database related tools
# =============================================================================

@mcp.tool()
async def list_tables(
    host: str = None,
    port: int = None
) -> str:
    """Query available table list in Machbase Neo.
    
    Args:
        host: Machbase server host (default: localhost)
        port: Machbase server port (default: 5654)
    """
    machbase_url = get_machbase_url(host, port)
    
    try:
        # Construct query parameters
        params = urlencode({
            "q": "SELECT name, type FROM M$SYS_TABLES WHERE name NOT LIKE 'M$%' ORDER BY name",
            "format": "csv"
        })
        
        start = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{params}",
                timeout=10.0
            )
        end = time.time()
        query_time = round((end - start) * 1000, 2)
            
        if response.status_code == 200:
            # Parse CSV data (manual)
            lines = response.text.strip().split('\n')
            if len(lines) < 2:
                return "No tables found."
            
            tables_info = []
            for line in lines[1:]:  # Skip header
                if line.strip():
                    columns = line.split(',')
                    if len(columns) >= 2:
                        table_name = columns[0].strip()
                        table_type = columns[1].strip()
                        tables_info.append(f"• {table_name} ({table_type})")
            
            if tables_info:
                table_list = "\n".join(tables_info)
                return f"Machbase Neo table list ({machbase_url}) - {query_time}ms:\n\n{table_list}"
            else:
                return "No tables found."
        else:
            return f"Failed to retrieve table list: HTTP {response.status_code}\n{response.text}"
                
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})"
    except Exception as e:
        return f"Error occurred while retrieving table list: {str(e)}"

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
    """Execute SQL query directly. Provides efficient data processing using Query API.
    
    Args:
        sql_query: SQL query to execute
        format: Output format (csv, json)
        timeformat: Time format (default: default)
        timezone: Timezone (default: Local)
        transpose: Whether to transpose data
        host: Machbase server host (default: localhost)
        port: Machbase server port (default: 5654)
    """
    if not sql_query:
        return "Please enter SQL query."
    
    machbase_url = get_machbase_url(host, port)
    
    try:
        # Construct query parameters
        params = {
            "q": sql_query,
            "format": "csv",
            "timeformat": timeformat,
            "timezone": timezone
        }
        
        if transpose:
            params["transpose"] = "true"
        
        encoded_params = urlencode(params)
        
        # Start performance measurement
        start = time.time()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?{encoded_params}",
                timeout=30.0
            )
            
        end = time.time()
        query_time = round((end - start) * 1000, 2)
            
        if response.status_code == 200:
            if format.lower() == "json":
                # Convert CSV data to JSON (manual parsing)
                lines = response.text.strip().split('\n')
                
                if len(lines) < 2:
                    return f"SQL query execution completed - {query_time}ms (no results)"
                
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
                    "query_time_ms": query_time,
                    "data": rows
                }
                
                formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
                return f"SQL query execution result (JSON) - {query_time}ms:\n\n```json\n{formatted_json}\n```"
            else:
                # Calculate number of rows in CSV data
                lines = response.text.strip().split('\n')
                row_count = max(0, len(lines) - 1)  # Exclude header
                
                return f"SQL query execution result (CSV) - {query_time}ms, {row_count} rows:\n\n```csv\n{response.text}\n```"
        else:
            return f"SQL query execution failed: HTTP {response.status_code}\n{response.text}"
                
    except httpx.ConnectError:
        return f"Cannot connect to Machbase Neo server ({machbase_url})"
    except httpx.TimeoutException:
        return f"SQL query execution timeout (30 seconds)"
    except Exception as e:
        return f"Error occurred during SQL query execution: {str(e)}"

# =============================================================================
# Documentation search related classes and tools
# =============================================================================

@dataclass
class DocumentPage:
    """Document page information"""
    url: str
    title: str
    content: str
    category: Optional[str] = None

class MachbaseDocSearcher:
    """Machbase documentation searcher (category-based)"""
    
    def __init__(self):
        self.base_url = "https://docs.machbase.com"
        self.documents: List[DocumentPage] = []
        self.indexed_categories: set = set()
        self.debug_info = []
        
        # Category-based URL classification
        self.categories = {
            "installation": [
                "https://docs.machbase.com/neo/getting-started/",
                "https://docs.machbase.com/neo/getting-started/installation/",
                "https://docs.machbase.com/neo/getting-started/installation-docker/",
                "https://docs.machbase.com/neo/getting-started/start-stop/",
                "https://docs.machbase.com/neo/getting-started/webui/",
                "https://docs.machbase.com/neo/operations/",
                "https://docs.machbase.com/neo/operations/command-line/",
                "https://docs.machbase.com/neo/operations/server-config/",
                "https://docs.machbase.com/neo/operations/deploy/",
                "https://docs.machbase.com/neo/operations/service-windows/",
                "https://docs.machbase.com/neo/operations/service-linux/",
            ],
            "tql": [
                "https://docs.machbase.com/neo/tql/",
                "https://docs.machbase.com/neo/tql/glance/",
                "https://docs.machbase.com/neo/tql/basic/",
                "https://docs.machbase.com/neo/tql/writing/",
                "https://docs.machbase.com/neo/tql/reading/",
                "https://docs.machbase.com/neo/tql/src/",
                "https://docs.machbase.com/neo/tql/sink/",
                "https://docs.machbase.com/neo/tql/map/",
                "https://docs.machbase.com/neo/tql/utilities/",
                "https://docs.machbase.com/neo/tql/http/",
                "https://docs.machbase.com/neo/tql/html/",
                "https://docs.machbase.com/neo/tql/chart/",
                "https://docs.machbase.com/neo/tql/chart/embed_in_html/",
                "https://docs.machbase.com/neo/tql/geomap/",
                "https://docs.machbase.com/neo/tql/geomap/embed_in_html/",
                "https://docs.machbase.com/neo/tql/script/",
                "https://docs.machbase.com/neo/tql/group/",
                "https://docs.machbase.com/neo/tql/fft/",
                "https://docs.machbase.com/neo/tql/filters/",
                "https://docs.machbase.com/neo/tql/example-time/",
            ],
            "api": [
                "https://docs.machbase.com/neo/api-mqtt/",
                "https://docs.machbase.com/neo/api-mqtt/query/",
                "https://docs.machbase.com/neo/api-mqtt/write/",
                "https://docs.machbase.com/neo/api-mqtt/writev5/",
                "https://docs.machbase.com/neo/api-mqtt/mqtt-websocket/",
                "https://docs.machbase.com/neo/api-mqtt/examples/",
                "https://docs.machbase.com/neo/api-mqtt/examples/mqtt-csharp/",
                "https://docs.machbase.com/neo/api-mqtt/examples/mqtt-python/",
                "https://docs.machbase.com/neo/api-mqtt/examples/mqtt-go/",
                "https://docs.machbase.com/neo/api-http/",
                "https://docs.machbase.com/neo/api-http/query/",
                "https://docs.machbase.com/neo/api-http/write/",
                "https://docs.machbase.com/neo/api-http/watch/",
                "https://docs.machbase.com/neo/api-http/file-upload/",
                "https://docs.machbase.com/neo/api-http/create-drop/",
                "https://docs.machbase.com/neo/api-http/lineprotocol/",
                "https://docs.machbase.com/neo/api-http/ui-api/",
                "https://docs.machbase.com/neo/api-http/examples/",
                "https://docs.machbase.com/neo/api-http/examples/http-js/",
                "https://docs.machbase.com/neo/api-http/examples/http-python/",
                "https://docs.machbase.com/neo/api-http/examples/http-go/",
                "https://docs.machbase.com/neo/api-http/examples/http-csharp/",
                "https://docs.machbase.com/neo/api-grpc/",
                "https://docs.machbase.com/neo/api-grpc/api_exec/",
                "https://docs.machbase.com/neo/api-grpc/api_queryrow/",
                "https://docs.machbase.com/neo/api-grpc/api_query/",
            ],
            "sql": [
                "https://docs.machbase.com/neo/sql/",
                "https://docs.machbase.com/neo/sql/tag-table/",
                "https://docs.machbase.com/neo/sql/rollup/",
                "https://docs.machbase.com/neo/sql/tag-stat/",
                "https://docs.machbase.com/neo/sql/remove-duplicate/",
                "https://docs.machbase.com/neo/sql/ourlier-remove/",
                "https://docs.machbase.com/neo/sql/storage-size/",
                "https://docs.machbase.com/neo/sql/backup-mount/",
            ],
            "tutorials": [
                "https://docs.machbase.com/neo/tutorials/",
                "https://docs.machbase.com/neo/tutorials/shellscript-waves/",
                "https://docs.machbase.com/neo/tutorials/webapp-http/",
                "https://docs.machbase.com/neo/tutorials/webapp-random/",
                "https://docs.machbase.com/neo/tutorials/webapp-grid/",
                "https://docs.machbase.com/neo/tutorials/webapp-mermaid-gantt/",
                "https://docs.machbase.com/neo/tutorials/raspi-iot-server/",
                "https://docs.machbase.com/neo/tutorials/mqtt-bridge-sqlite/",
            ],
            "tools": [
                "https://docs.machbase.com/neo/shell/",
                "https://docs.machbase.com/neo/shell/user-shell/",
                "https://docs.machbase.com/neo/shell/shell-run/",
                "https://docs.machbase.com/neo/dashboard/",
                "https://docs.machbase.com/neo/tag-analyzer/",
                "https://docs.machbase.com/neo/jsh/",
                "https://docs.machbase.com/neo/jsh/examples/",
                "https://docs.machbase.com/neo/jsh/module_process/",
                "https://docs.machbase.com/neo/jsh/module_system/",
                "https://docs.machbase.com/neo/jsh/module_db/",
                "https://docs.machbase.com/neo/jsh/module_mqtt/",
                "https://docs.machbase.com/neo/jsh/module_http/",
                "https://docs.machbase.com/neo/jsh/module_generator/",
                "https://docs.machbase.com/neo/jsh/module_filter/",
                "https://docs.machbase.com/neo/jsh/module_analysis/",
                "https://docs.machbase.com/neo/jsh/module_spatial/",
                "https://docs.machbase.com/neo/jsh/module_opcua/",
                "https://docs.machbase.com/neo/jsh/module_psutil/",
                "https://docs.machbase.com/neo/import-export/",
            ],
            "general": [
                "https://docs.machbase.com/neo/",
                "https://docs.machbase.com/neo/releases/",
                "https://docs.machbase.com/neo/options/",
                "https://docs.machbase.com/neo/options/timeformat/",
                "https://docs.machbase.com/neo/options/tz/",
                "https://docs.machbase.com/neo/security/",
                "https://docs.machbase.com/neo/timer/",
                "https://docs.machbase.com/neo/bridges/",
                "https://docs.machbase.com/neo/bridges/11.sqlite/",
                "https://docs.machbase.com/neo/bridges/12.postgresql/",
                "https://docs.machbase.com/neo/bridges/13.mysql/",
                "https://docs.machbase.com/neo/bridges/15.mssql/",
                "https://docs.machbase.com/neo/bridges/21.mqtt/",
                "https://docs.machbase.com/neo/bridges/31.nats/",
                "https://docs.machbase.com/neo/operations/address-ports/",
                "https://docs.machbase.com/neo/operations/metrics/",
            ]
        }
        
        # Search keyword to category mapping
        self.query_patterns = {
            "installation": [
                "install", "installation", "docker", "start", "setup", "deploy", "server",
                "config", "configuration", "windows", "linux", "service", "getting-started"
            ],
            "tql": [
                "tql", "geomap", "chart", "map", "script", "time-series", "data-transform", 
                "html", "http", "filter", "group", "fft", "visualization", "webpage", "embed"
            ],
            "api": [
                "api", "http", "mqtt", "grpc", "client", "rest", "websocket", "protocol", 
                "request", "response", "communication", "library", "sdk", "example"
            ],
            "sql": [
                "sql", "query", "select", "insert", "create", "drop", "table", "rollup", 
                "tag", "backup", "mount", "duplicate", "outlier", "storage"
            ],
            "tutorials": [
                "tutorial", "example", "guide", "webapp", "practice", "step-by-step", 
                "bridge", "iot", "raspberry", "mqtt-bridge", "grid", "mermaid", "gantt"
            ],
            "tools": [
                "shell", "jsh", "dashboard", "analyzer", "tool", "module", "timer", 
                "import", "export", "spatial", "opcua", "psutil", "generator"
            ]
        }
    
    def detect_category(self, query: str) -> str:
        """Analyze search query to detect appropriate category"""
        query_lower = query.lower()
        
        category_scores = {}
        
        # Calculate score for each category
        for category, keywords in self.query_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in query_lower:
                    # Weight based on keyword length (longer keywords are more accurate)
                    score += len(keyword) * query_lower.count(keyword)
            
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Return category with highest score
            best_category = max(category_scores.items(), key=lambda x: x[1])[0]
            logger.info(f"Detected category '{best_category}' for query '{query}' (scores: {category_scores})")
            return best_category
        
        logger.info(f"No specific category detected for '{query}', using 'general'")
        return "general"
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content"""
        logger.info(f"Fetching: {url}")
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(url) as response:
                    status = response.status
                    logger.info(f"Response status for {url}: {status}")
                    
                    if status == 200:
                        content = await response.text()
                        logger.info(f"Successfully fetched {len(content)} characters from {url}")
                        return content
                    elif status == 404:
                        logger.warning(f"Page not found (404): {url}")
                        self.debug_info.append(f"HTTP 404 for {url}")
                        return None
                    else:
                        logger.warning(f"HTTP {status} for {url}")
                        self.debug_info.append(f"HTTP {status} for {url}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            self.debug_info.append(f"Timeout for {url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            self.debug_info.append(f"Error fetching {url}: {str(e)}")
            return None
    
    def extract_content(self, html: str, url: str, category: str = None) -> Optional[DocumentPage]:
        """Extract document content from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            logger.debug(f"Parsing HTML for {url}")
            
            # Extract title (with priority)
            title = "Untitled"
            title_selectors = [
                'h1.page-title', 'h1#title', 'h1.title', 'h1.doc-title',
                '.page-header h1', '.content h1:first-child', 'h1', 'title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title_text = title_elem.get_text(strip=True)
                    if title_text and len(title_text) > 2:  # Check if meaningful title
                        title = title_text
                        logger.debug(f"Found title with '{selector}': {title}")
                        break
            
            # Find main content area (more specific selectors)
            content_selectors = [
                '.doc-content', '.docs-content', '.documentation-content',
                '.markdown-body', '.post-content', '.entry-content',
                'main .content', 'main', '.main-content', '.page-content',
                'article', '.container .content', '#content', 
                '[role="main"]', '.documentation'
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    logger.debug(f"Found content with selector: {selector}")
                    break
            
            # If content not found, use body but remove unnecessary parts first
            if not content_elem:
                content_elem = soup.find('body')
                logger.debug("Using body as content element")
            
            if not content_elem:
                logger.warning(f"No content found for {url}")
                return None
            
            # Remove unwanted elements (more comprehensive)
            unwanted_selectors = [
                'nav', 'footer', 'script', 'style', 'noscript', 'meta',
                '.sidebar', '.toc', '.table-of-contents', '.navigation', '.nav',
                '.breadcrumb', '.breadcrumbs', '.header', '.site-header',
                '.footer', '.site-footer', '.menu', '.navbar', '.topbar',
                '.advertisement', '.ads', '.social-share', '.comments',
                '.related-posts', '.tags', '.categories', '#disqus_thread',
                '.edit-page', '.improve-page', '.github-link',
                '.search-box', '.search-form', '.search-container'
            ]
            
            for selector in unwanted_selectors:
                for unwanted in content_elem.select(selector):
                    unwanted.decompose()
            
            # Extract and clean text
            content = content_elem.get_text(separator='\n', strip=True)
            
            # Clean text
            content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Remove excessive blank lines
            content = re.sub(r'[ \t]+', ' ', content)  # Remove excessive spaces
            content = re.sub(r'\n ', '\n', content)  # Remove leading spaces on lines
            
            # Exclude content that's too short
            if len(content.strip()) < 100:
                logger.warning(f"Content too short ({len(content)} chars) for {url}")
                return None
            
            logger.info(f"Extracted {len(content)} characters from {url}")
            
            return DocumentPage(
                url=url,
                title=title,
                content=content,
                category=category
            )
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            self.debug_info.append(f"Error extracting content from {url}: {str(e)}")
            return None
    
    async def index_category(self, category: str, max_docs: int = 20):
        """Index documents of specific category"""
        if category in self.indexed_categories:
            logger.info(f"Category '{category}' already indexed")
            return
        
        logger.info(f"Indexing category: {category}")
        
        urls = self.categories.get(category, [])
        if not urls:
            logger.warning(f"No URLs found for category: {category}")
            return
        
        success_count = 0
        
        for i, url in enumerate(urls[:max_docs], 1):
            logger.info(f"Processing {category} ({i}/{min(max_docs, len(urls))}): {url}")
            try:
                html = await self.fetch_page(url)
                if html:
                    doc = self.extract_content(html, url, category)
                    if doc and len(doc.content) > 100:
                        self.documents.append(doc)
                        success_count += 1
                        logger.info(f"Index completed: {doc.title} ({len(doc.content)} chars)")
                    else:
                        logger.warning(f"Insufficient content: {url}")
                else:
                    logger.warning(f"Page load failed: {url}")
                    
            except Exception as e:
                logger.error(f"Index failed {url}: {e}")
                self.debug_info.append(f"Index failed {url}: {str(e)}")
            
            # Prevent server load
            await asyncio.sleep(0.5)
        
        self.indexed_categories.add(category)
        logger.info(f"Category '{category}' indexing completed: {success_count} documents")
    
    async def smart_index(self, query: str):
        """Smart indexing of related categories based on search query"""
        # 1. Detect category from search query
        primary_category = self.detect_category(query)
        
        # 2. Index the category if not already indexed
        if primary_category not in self.indexed_categories:
            await self.index_category(primary_category, 15)
        
        # 3. Always partially index general category (for basic information)
        if "general" not in self.indexed_categories and primary_category != "general":
            await self.index_category("general", 5)
        
        # 4. If still insufficient indexed documents, add related categories
        if len(self.documents) < 10:
            # TQL and API are often used together
            related_categories = {
                "tql": ["api", "sql"],
                "api": ["tql", "tutorials"],
                "sql": ["tql", "api"],
                "tutorials": ["tql", "api"],
                "installation": ["general", "tools"],
                "tools": ["installation", "general"]
            }
            
            for related_cat in related_categories.get(primary_category, []):
                if related_cat not in self.indexed_categories and len(self.documents) < 15:
                    await self.index_category(related_cat, 5)
    
    def search_documents(self, query: str, max_results: int = 5) -> List[DocumentPage]:
        """Search documents (improved search algorithm)"""
        logger.info(f"Searching for: '{query}' in {len(self.documents)} documents")
        
        if not self.documents:
            logger.warning("No indexed documents")
            return []
        
        query_lower = query.lower()
        scored_docs = []
        
        # Split search query into words
        query_words = [word.strip() for word in re.split(r'[\s,]+', query_lower) if len(word.strip()) > 2]
        
        # Category of search query
        query_category = self.detect_category(query)
        
        for doc in self.documents:
            score = 0
            content_lower = doc.content.lower()
            title_lower = doc.title.lower()
            
            # 1. Category matching bonus
            if doc.category == query_category:
                score += 200
                logger.debug(f"Category match bonus for: {doc.title}")
            
            # 2. Complete phrase match (highest score)
            if query_lower in title_lower:
                score += 1000
                logger.debug(f"Full phrase match in title: {doc.title}")
            elif query_lower in content_lower:
                score += 500
                logger.debug(f"Full phrase match in content: {doc.title}")
            
            # 3. Individual word matching
            for word in query_words:
                title_count = title_lower.count(word)
                content_count = content_lower.count(word)
                
                score += title_count * 100  # High score for title words
                score += content_count * 10  # Medium score for content words
                
                if title_count > 0:
                    logger.debug(f"Word '{word}' found {title_count} times in title: {doc.title}")
                if content_count > 0:
                    logger.debug(f"Word '{word}' found {content_count} times in content: {doc.title}")
            
            # 4. URL-based relevance (bonus if specific keywords are in URL)
            url_keywords = ['install', 'tutorial', 'guide', 'quick-start', 'api', 'tql', 'geomap', 'chart']
            for keyword in url_keywords:
                if keyword in query_lower and keyword in doc.url.lower():
                    score += 150
                    logger.debug(f"URL relevance bonus for '{keyword}': {doc.title}")
            
            if score > 0:
                scored_docs.append((score, doc))
                logger.debug(f"Final score {score} for: {doc.title}")
        
        # Sort by score
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        logger.info(f"Found {len(scored_docs)} matching documents")
        
        return [doc for _, doc in scored_docs[:max_results]]
    
    def format_answer(self, query: str, search_results: List[DocumentPage]) -> str:
        """Format answer based on search results"""
        if not search_results:
            debug_msg = ""
            if self.debug_info:
                debug_msg = f"\n\nDebug information:\n" + "\n".join(self.debug_info[-3:])
            
            return f"Could not find information about '{query}' in Machbase documentation.\n" + \
                   f"Indexed documents: {len(self.documents)} (categories: {', '.join(self.indexed_categories)})\n" + \
                   f"Try searching with different keywords or visit https://docs.machbase.com directly." + debug_msg
        
        detected_category = self.detect_category(query)
        answer = f"Found information about '{query}':\n\n"
        
        for i, doc in enumerate(search_results, 1):
            # Extract relevant content (smarter approach)
            content = doc.content
            query_words = [word.strip() for word in re.split(r'[\s,]+', query.lower()) if len(word.strip()) > 2]
            
            # Find most relevant section
            best_excerpt = ""
            best_score = 0
            
            # Split document into sentences
            sentences = re.split(r'[.!?]\s+', content)
            
            for j in range(len(sentences)):
                # Review consecutive 3 sentences as one section
                section = ' '.join(sentences[j:j+3]).lower()
                section_score = 0
                
                for word in query_words:
                    section_score += section.count(word) * 10
                
                if section_score > best_score and len(section) > 50:
                    best_score = section_score
                    best_excerpt = ' '.join(sentences[j:j+3]).strip()
            
            # If no good section found, use beginning of document
            if not best_excerpt:
                best_excerpt = content[:300].strip()
            
            # Truncate if too long
            if len(best_excerpt) > 400:
                best_excerpt = best_excerpt[:400] + "..."
            
            answer += f"**{i}. {doc.title}**\n"
            answer += f"{best_excerpt}\n"
            answer += f"Source: {doc.url}\n\n"
        
        return answer.strip()

    def get_debug_status(self) -> str:
        """Return debugging status"""
        status = f"=== Integrated MCP Server Status ===\n"
        status += f"Indexed categories: {', '.join(self.indexed_categories) if self.indexed_categories else 'None'}\n"
        status += f"Indexed documents: {len(self.documents)}\n"
        status += f"Base URL: {self.base_url}\n"
        
        # Number of URLs per category
        status += f"\nAvailable URLs by category:\n"
        for category, urls in self.categories.items():
            indexed_mark = "[OK]" if category in self.indexed_categories else "[WAIT]"
            status += f"  {indexed_mark} {category}: {len(urls)} URLs\n"
        
        if self.documents:
            status += f"\nIndexed documents:\n"
            category_counts = {}
            for doc in self.documents:
                cat = doc.category or "unknown"
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            for category, count in category_counts.items():
                status += f"  [{category}]: {count} documents\n"
            
            status += f"\nDocument details:\n"
            for i, doc in enumerate(self.documents, 1):
                status += f"  {i}. {doc.title} ({len(doc.content)} chars)\n"
                status += f"     Category: {doc.category}\n"
                status += f"     URL: {doc.url}\n"
        else:
            status += "No indexed documents.\n"
        
        if self.debug_info:
            status += f"\nDebug information ({len(self.debug_info)} items):\n"
            for info in self.debug_info[-5:]:
                status += f"  - {info}\n"
        
        return status


# Global searcher instance
searcher = MachbaseDocSearcher()

# =============================================================================
# Documentation search tools
# =============================================================================

@mcp.tool()
async def search_machbase_docs(query: str) -> str:
    """Search information in Machbase official documentation. Enter questions or keywords to find related documents and get answers.
    
    Args:
        query: Question or keywords to search (e.g., "geomap usage", "installation method", "TQL examples")
    """
    global searcher
    
    try:
        # Smart indexing based on search query
        await searcher.smart_index(query)
        
        # Perform search
        results = searcher.search_documents(query)
        answer = searcher.format_answer(query, results)
        
        return answer
        
    except Exception as e:
        logger.error(f"Error occurred during search: {e}", exc_info=True)
        return f"An error occurred during search: {str(e)}\n{searcher.get_debug_status()}"

@mcp.tool()
async def debug_mcp_status() -> str:
    """Check current status and debugging information of MCP server."""
    global searcher
    
    # Also check database connection status
    db_status = ""
    try:
        machbase_url = get_machbase_url()
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{machbase_url}/db/query?q=SELECT 1&format=csv", timeout=5.0)
            if response.status_code == 200:
                db_status = f"[OK] Machbase Neo connection successful ({machbase_url})"
            else:
                db_status = f"[ERROR] Machbase Neo connection failed: HTTP {response.status_code}"
    except Exception as e:
        db_status = f"[ERROR] Machbase Neo connection error: {str(e)}"
    
    return f"{db_status}\n\n{searcher.get_debug_status()}"

@mcp.tool()
def hello(name: str) -> str:
    """Return a simple greeting message.
    
    Args:
        name: Name to greet
    """
    return f"Hello, {name}! This is the Machbase Neo integrated server.\n" + \
           "We support both database query execution and documentation search."

# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting integrated Machbase Neo MCP server")
    logger.info("Database functions: table lookup, SQL execution")
    logger.info("Documentation search: smart category-based search")
    mcp.run()