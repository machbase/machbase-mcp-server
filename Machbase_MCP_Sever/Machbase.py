#!/usr/bin/env python3
"""
Machbase Neo Unified MCP Server v0.7.0

Single MCP server providing complete Machbase Neo control:
- Database queries and TQL execution (via /db/ API, no auth)
- File management and TQL file saving (via /web/api/, JWT auth)
- Dashboard creation and chart management (via /web/api/, JWT auth)
- Machbase Neo documentation access (local file system)
"""

import asyncio
import httpx
import json
import time
import logging
import re
import os
import uuid
import csv
import io
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlencode, quote
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict, Counter

from fastmcp import FastMCP


# ═══════════════════════════════════════════════════════════════
# [Section 1] Configuration & Constants
# ═══════════════════════════════════════════════════════════════

VERSION = "0.7.3"
BUILD_DATE = "2026-03-04"
DESCRIPTION = "Machbase Neo Unified MCP Server"

# ── Server Connection ──
DEFAULT_MACHBASE_HOST = os.environ.get("MACHBASE_HOST", "127.0.0.1")
DEFAULT_MACHBASE_PORT = int(os.environ.get("MACHBASE_PORT", "5654"))

# ── JWT Authentication (for Web API) ──
MACHBASE_USER = os.environ.get("MACHBASE_USER", "sys")
MACHBASE_PASSWORD = os.environ.get("MACHBASE_PASSWORD", "manager")

# ── Dashboard Grid Constants ──
GRID_COLS = 36
CHART_W_LARGE = 17   # Line, Bar, Scatter, Tql chart
CHART_W_SMALL = 7    # Pie, Gauge, Liquid fill
CHART_H_DEFAULT = 7
_LARGE_CHART_TYPES = ("Line", "Bar", "Scatter", "Adv scatter", "Tql chart")

# JWT token cache
_jwt_token: Optional[str] = None
_jwt_expire: float = 0

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ── MCP Server Instance ──
mcp = FastMCP("Machbase Neo")


# ═══════════════════════════════════════════════════════════════
# [Section 2] HTTP Helpers - DB API (/db/, No Auth)
# ═══════════════════════════════════════════════════════════════

def get_machbase_url(host: Optional[str] = None, port: Optional[int] = None) -> str:
    """Generate Machbase Neo server base URL (for /db/ endpoints)."""
    actual_host = host or DEFAULT_MACHBASE_HOST
    actual_port = port or DEFAULT_MACHBASE_PORT
    return f"http://{actual_host}:{actual_port}"


def validate_table_name(table_name: str) -> Tuple[bool, str]:
    """
    Validate table name to prevent SQL injection.

    Simple whitespace check is effective because:
    - All SQL keywords are separated by whitespace (UNION, SELECT, WHERE, etc.)
    - Tab and newline characters are used to bypass space filters

    Args:
        table_name: Table name to validate

    Returns:
        (is_valid, error_message): Tuple of validation result and error message
    """
    if not table_name:
        return False, "Table name is required"
    if ' ' in table_name:
        return False, "Table name cannot contain spaces"
    if '\t' in table_name:
        return False, "Table name cannot contain tabs"
    if '\n' in table_name or '\r' in table_name:
        return False, "Table name cannot contain newlines"
    return True, ""


# ═══════════════════════════════════════════════════════════════
# [Section 3] HTTP Helpers - Web API (/web/api/, JWT Auth)
# ═══════════════════════════════════════════════════════════════

def _get_base_url(host: Optional[str] = None, port: Optional[int] = None) -> str:
    """Generate Machbase Neo Web API base URL (for /web/api/ endpoints)."""
    h = host or DEFAULT_MACHBASE_HOST
    p = port or DEFAULT_MACHBASE_PORT
    return f"http://{h}:{p}/web/api"


async def _get_jwt_token(host: Optional[str] = None, port: Optional[int] = None) -> str:
    """Login to Neo Web UI and get JWT access token. Token is cached until expired."""
    global _jwt_token, _jwt_expire

    if _jwt_token and time.time() < (_jwt_expire - 60):
        return _jwt_token

    base = _get_base_url(host, port)
    url = f"{base}/login"

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        resp = await client.post(
            url,
            json={"loginName": MACHBASE_USER, "password": MACHBASE_PASSWORD},
        )
        resp.raise_for_status()
        data = resp.json()

    if not data.get("success"):
        raise Exception(f"Login failed: {data.get('reason', 'unknown')}")

    _jwt_token = data["accessToken"]
    _jwt_expire = time.time() + 290

    return _jwt_token


async def _get_auth_headers(host: Optional[str] = None, port: Optional[int] = None) -> dict:
    """Build authentication headers with JWT token."""
    token = await _get_jwt_token(host, port)
    return {"Authorization": f"Bearer {token}"}


async def _request(
    method: str,
    path: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
    json_data: Optional[dict] = None,
    params: Optional[dict] = None,
) -> dict:
    """Send HTTP request to Neo Web API (authenticated)."""
    base = _get_base_url(host, port)
    url = f"{base}{path}"
    headers = await _get_auth_headers(host, port)
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        resp = await client.request(method, url, json=json_data, params=params, headers=headers)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {"status": "ok", "text": resp.text}


# ═══════════════════════════════════════════════════════════════
# [Section 4] File & Folder Helpers
# ═══════════════════════════════════════════════════════════════

def _build_folder_api_path(parent_path: str) -> str:
    """Build the correct API path for folder operations.

    Neo Web API expects:
      - Root level:  POST /web/api/files/?action=mkDir&name=XXX  (trailing slash required)
      - Sub-folder:  POST /web/api/files/parent?action=mkDir&name=XXX
    """
    clean = parent_path.strip("/") if parent_path else ""
    if clean:
        return f"/files/{clean}/"
    return "/files/"


async def _create_single_folder(
    folder_name: str,
    parent_api_path: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> dict:
    """Create a single folder via Neo Web API.

    Returns:
        {"success": True/False, "reason": str, "already_exists": bool}
    """
    base = _get_base_url(host, port)
    encoded_name = quote(folder_name, safe="")
    url = f"{base}{parent_api_path}{encoded_name}/"
    headers = await _get_auth_headers(host, port)

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.post(url, headers=headers)

            body = {}
            if resp.content:
                try:
                    body = resp.json()
                except Exception:
                    body = {"reason": resp.text}

            if resp.status_code == 200 and body.get("success"):
                return {"success": True, "reason": "created", "already_exists": False}

            reason = body.get("reason", resp.text or "").lower()
            if "already exist" in reason:
                return {"success": True, "reason": "already exists", "already_exists": True}

            return {
                "success": False,
                "reason": body.get("reason", f"HTTP {resp.status_code}: {resp.text[:200]}"),
                "already_exists": False,
            }

    except Exception as e:
        return {"success": False, "reason": str(e), "already_exists": False}


async def _verify_folder_exists(
    folder_path: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> bool:
    """Verify a folder actually exists by listing it."""
    base = _get_base_url(host, port)
    url = f"{base}/files/{folder_path}"
    headers = await _get_auth_headers(host, port)

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                body = resp.json()
                return body.get("success", False)
            return False
    except Exception:
        return False


async def _file_exists(
    filepath: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> bool:
    """Check if a specific file exists by trying to GET it."""
    base = _get_base_url(host, port)
    url = f"{base}/files/{filepath}"
    headers = await _get_auth_headers(host, port)
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                body = resp.json()
                # Folder listings have "children"; actual files don't
                if "children" in body:
                    return False
                return True
            return False
    except Exception:
        return False


async def _get_unique_filename(
    filename: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Check if filename exists; if so, append _v2, _v3, etc."""
    # If no conflict, return original
    if not await _file_exists(filename, host, port):
        return filename

    # Split folder and base
    if "/" in filename:
        folder, base_name = filename.rsplit("/", 1)
    else:
        folder, base_name = "", filename

    # Split name and extension
    if "." in base_name:
        name_part, ext = base_name.rsplit(".", 1)
    else:
        name_part, ext = base_name, ""

    # Generate unique name: name_v2.ext, name_v3.ext, ...
    counter = 2
    while counter <= 100:
        new_name = f"{name_part}_v{counter}.{ext}" if ext else f"{name_part}_v{counter}"
        candidate = f"{folder}/{new_name}" if folder else new_name
        if not await _file_exists(candidate, host, port):
            return candidate
        counter += 1

    return f"{folder}/{name_part}_v{counter}.{ext}" if folder else f"{name_part}_v{counter}.{ext}"


# ═══════════════════════════════════════════════════════════════
# [Section 5] Dashboard Template Helpers
# ═══════════════════════════════════════════════════════════════

def _generate_id() -> str:
    return str(int(time.time() * 1000000))


def _generate_panel_id() -> str:
    return str(uuid.uuid4())


def _calculate_next_position(
    existing_panels: list,
    needed_w: int,
) -> Tuple[int, int]:
    """Calculate next (x, y) position for auto-layout on the grid.

    Places panels left-to-right, wrapping to next row when full.
    Returns (x, y) tuple.
    """
    if not existing_panels:
        return 0, 0

    max_bottom = max(p.get("y", 0) + p.get("h", CHART_H_DEFAULT) for p in existing_panels)
    last_row_y = max(p.get("y", 0) for p in existing_panels)
    last_row_panels = [p for p in existing_panels if p.get("y", 0) == last_row_y]
    last_row_right = max(
        p.get("x", 0) + p.get("w", CHART_W_LARGE) for p in last_row_panels
    ) if last_row_panels else 0

    if last_row_right + needed_w <= GRID_COLS:
        return last_row_right, last_row_y
    else:
        return 0, max_bottom


_CHART_TYPE_DEFAULTS = {
    "Line": {
        "areaStyle": False, "smooth": False, "isStep": False, "isStack": False,
        "connectNulls": True, "isSymbol": False, "symbol": "circle", "symbolSize": 4,
        "isSampling": False, "fillOpacity": 0.3, "tagLimit": 12,
        "markLine": {"symbol": ["none", "none"], "label": {"show": False}, "data": []},
        "visualMap": {"type": "piecewise", "show": False, "dimension": 0, "seriesIndex": 0, "pieces": []},
    },
    "Bar": {
        "isStack": False, "isLarge": False, "isPolar": False, "polarRadius": 30,
        "polarSize": 80, "startAngle": 90, "maxValue": 100, "tagLimit": 12, "polarAxis": "time",
    },
    "Scatter": {
        "isLarge": False, "symbol": "circle", "symbolSize": 4, "tagLimit": 12,
    },
    "Pie": {
        "doughnutRatio": 50, "roseType": False, "tagLimit": 12,
    },
    "Gauge": {
        "isAxisTick": True, "axisLabelDistance": 25, "valueFontSize": 15,
        "valueAnimation": False, "alignCenter": 30, "isAnchor": True, "anchorSize": 25,
        "min": 0, "max": 100, "tagLimit": 1, "digit": 0,
        "axisLineStyleWidth": 10, "isAxisLineStyleColor": False,
        "axisLineStyleColor": [[0.5, "#c2c2c2"], [1, "#F44E3B"]],
    },
    "Liquid fill": {
        "shape": "circle", "amplitude": 20, "waveAnimation": False, "isOutline": False,
        "minData": 0, "maxData": 1, "fontSize": 30, "tagLimit": 1, "unit": "%", "digit": 0,
        "backgroundColor": "#E3F7FF",
    },
    "Text": {
        "tagLimit": 2, "fontSize": 100, "symbol": "circle", "isSymbol": True, "symbolSize": 1,
        "color": [["default", "#FFFFFF"]], "chartType": "line", "chartColor": "#367FEB",
        "fillOpacity": 0.1, "digit": 3, "unit": "", "textSeries": [0], "chartSeries": [0],
    },
    "Geomap": {
        "tooltipTime": True, "tooltipCoor": False, "intervalType": "none", "intervalValue": "",
        "coorLat": [0], "coorLon": [1], "marker": [{"shape": "circle", "radius": 150}],
        "useZoomControl": False, "useAutoRefresh": True,
    },
    "Tql chart": {
        "theme": "white",
    },
}


def _get_dashboard_url(filename: str, host: Optional[str] = None, port: Optional[int] = None) -> str:
    """Generate Neo Web UI URL for a dashboard."""
    base = get_machbase_url(host, port)
    name = filename[:-4] if filename.endswith(".dsh") else filename
    return f"{base}/web/ui/board/{name}"


def _parse_time_value(val: str):
    if val and val.isdigit():
        return int(val)
    return val


def _make_empty_dashboard(title: str = "New dashboard", time_start: str = "now-1h", time_end: str = "now", dsh_path: str = "/", dsh_name: str = "DASHBOARD") -> dict:
    return {
        "id": _generate_id(),
        "type": "dsh",
        "name": dsh_name,
        "path": dsh_path,
        "code": "",
        "panels": [],
        "range_bgn": "",
        "range_end": "",
        "savedCode": False,
        "sheet": [],
        "shell": {"icon": "dashboard", "theme": "", "id": "DSH"},
        "dashboard": {
            "variables": [],
            "timeRange": {"start": _parse_time_value(time_start), "end": _parse_time_value(time_end), "refresh": "Off"},
            "title": title,
            "panels": [],
        },
    }


def _make_block(
    table: str,
    tag: str,
    column: str = "VALUE",
    color: str = "#367FEB",
    user_name: str = "sys",
    is_visible: bool = True,
    aggregator: str = "value",
) -> dict:
    """Create a single blockList entry matching Neo UI structure."""
    return {
        "id": _generate_panel_id(),
        "table": table,
        "userName": user_name,
        "color": color,
        "type": "tag",
        "filter": [
            {
                "id": _generate_panel_id(),
                "column": "NAME",
                "operator": "in",
                "value": tag,
                "useFilter": True,
                "useTyping": False,
                "typingValue": f'NAME in ("{tag}")',
            }
        ],
        "values": [
            {
                "id": _generate_panel_id(),
                "alias": "",
                "value": column,
                "aggregator": aggregator,
            }
        ],
        "useRollup": False,
        "name": "NAME",
        "time": "TIME",
        "useCustom": False,
        "aggregator": aggregator,
        "diff": "none",
        "tag": tag,
        "value": column,
        "alias": "",
        "math": "",
        "isValidMath": True,
        "duration": {"from": "", "to": ""},
        "customFullTyping": {"use": False, "text": ""},
        "isVisible": is_visible,
        "tableInfo": [],
    }


def _make_chart_panel(
    title: str = "New chart",
    chart_type: str = "Line",
    table: str = "",
    user_name: str = "sys",
    tag: str = "",
    color: str = "#367FEB",
    column: str = "VALUE",
    tql_path: str = "",
    x: int = -1,
    y: int = -1,
    w: int = 0,
    h: int = 0,
    time_start: str = "",
    time_end: str = "",
    smooth: bool = False,
    area_style: bool = False,
    is_stack: bool = False,
) -> dict:
    """Create a chart panel dict. x/y=-1 means auto-layout (caller sets position)."""
    panel_id = _generate_panel_id()

    # ── TQL chart: override type, use tqlInfo only ──
    if tql_path:
        chart_type = "Tql chart"

    # ── Auto-width/height based on chart type ──
    if w <= 0:
        w = CHART_W_LARGE if chart_type in _LARGE_CHART_TYPES else CHART_W_SMALL
    if h <= 0:
        h = CHART_H_DEFAULT

    # ── Chart type-specific options from defaults ──
    chart_options = dict(_CHART_TYPE_DEFAULTS.get(chart_type, _CHART_TYPE_DEFAULTS["Line"]))

    # Apply user overrides for common options
    if chart_type == "Line":
        chart_options["smooth"] = smooth
        chart_options["areaStyle"] = area_style
        chart_options["isStack"] = is_stack
    elif chart_type == "Bar":
        chart_options["isStack"] = is_stack

    # ── Build panel ──
    panel = {
        "id": panel_id,
        "title": title,
        "titleColor": "",
        "type": chart_type,
        "x": max(x, 0),
        "y": max(y, 0),
        "w": w,
        "h": h,
        "theme": "white",
        "useCustomTime": False,
        "isAxisInterval": False,
        "timeRange": {"start": _parse_time_value(time_start), "end": _parse_time_value(time_end), "refresh": "Off"},
        "blockList": [],
        "transformBlockList": [],
        "chartInfo": chart_options,
        "chartOptions": dict(chart_options),
        "commonOptions": {
            "isLegend": True,
            "legendTop": "bottom",
            "legendLeft": "center",
            "legendOrient": "horizontal",
            "isTooltip": True,
            "tooltipTrigger": "axis",
            "tooltipBgColor": "#FFFFFF",
            "tooltipTxtColor": "#333",
            "tooltipDecimals": 3,
            "tooltipUnit": "",
            "isInsideTitle": True,
            "isDataZoom": False,
            "title": title,
            "gridTop": 50,
            "gridBottom": 50,
            "gridLeft": 35,
            "gridRight": 35,
        },
        "xAxisOptions": [
            {
                "type": "time",
                "axisTick": {"alignWithLabel": True},
                "axisLabel": {"hideOverlap": True},
                "axisLine": {"onZero": False},
                "scale": True,
                "useMinMax": False,
                "useBlockList": [0],
                "label": {
                    "name": "value",
                    "key": "value",
                    "title": "",
                    "unit": "",
                    "decimals": None,
                    "squared": 0,
                },
            }
        ],
        "yAxisOptions": [
            {
                "type": "value",
                "position": "left",
                "offset": "",
                "alignTicks": True,
                "scale": True,
                "useMinMax": False,
                "axisLine": {"onZero": False},
                "label": {
                    "name": "value",
                    "key": "value",
                    "title": "",
                    "unit": "",
                    "decimals": None,
                    "squared": 0,
                },
            }
        ],
        "axisInterval": {"IntervalType": "", "IntervalValue": ""},
    }

    # ── TQL chart: set tqlInfo + default block ──
    if tql_path:
        # Ensure leading / for API path resolution
        if not tql_path.startswith("/"):
            tql_path = "/" + tql_path
        panel["tqlInfo"] = {
            "path": tql_path,
            "params": [{"name": "", "value": "", "format": ""}],
            "chart_id": "",
        }
        panel["blockList"] = [_make_block(table="", tag="", column="VALUE", user_name=user_name)]
    else:
        # ── Table-based: build blockList ──
        # Support multiple tags (comma-separated) for Pie/Gauge/etc.
        if table and tag:
            _SERIES_COLORS = [
                "#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de",
                "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc", "#FADE2A",
            ]
            # NAME_VALUE charts need a real aggregator, not "value"
            if chart_type == "Pie":
                agg = "count"
            elif chart_type in ("Gauge", "Liquid fill"):
                agg = "last"
            else:
                agg = "value"

            tags = [t.strip() for t in tag.split(",") if t.strip()]
            blocks = []
            for i, t in enumerate(tags):
                c = color if len(tags) == 1 else _SERIES_COLORS[i % len(_SERIES_COLORS)]
                blocks.append(_make_block(table, t, column, c, user_name, aggregator=agg))
            panel["blockList"] = blocks

    return panel


# ═══════════════════════════════════════════════════════════════
# [Section 6] Document System
# ═══════════════════════════════════════════════════════════════

@dataclass
class DocumentSection:
    """Document section representation"""
    title: str
    level: int
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

    def __init__(self, docs_folder: Optional[str] = None):
        script_dir = os.path.dirname(__file__) if '__file__' in globals() else "."

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

        self.document_cache: Dict[str, FullDocument] = {}
        self.file_index: Dict[str, str] = {}
        self._build_file_index()

    def _build_file_index(self) -> None:
        if not os.path.exists(self.docs_folder):
            return
        for root, dirs, files in os.walk(self.docs_folder):
            for filename in files:
                if filename.endswith('.md'):
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, self.docs_folder)
                    self.file_index[relative_path] = full_path
                    if filename not in [os.path.basename(p) for p in self.file_index.values()]:
                        self.file_index[filename] = full_path

    def get_full_document(self, file_identifier: str) -> Optional[FullDocument]:
        full_path = None
        if file_identifier in self.file_index:
            full_path = self.file_index[file_identifier]
        else:
            for key, path in self.file_index.items():
                if key.lower() == file_identifier.lower():
                    full_path = path
                    break

        if not full_path or not os.path.exists(full_path):
            return None

        if full_path in self.document_cache:
            return self.document_cache[full_path]

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if len(content.strip()) < 10:
                return None

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
            self.document_cache[full_path] = doc
            return doc

        except Exception as e:
            logger.error(f"Error reading document {full_path}: {e}")
            return None

    def _extract_title(self, content: str, filename: str) -> str:
        lines = content.split('\n')
        for line in lines[:10]:
            if line.startswith('# '):
                return line[2:].strip()
        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
        return ' '.join(word.capitalize() for word in title.split())

    def _detect_category(self, path: str, content: str) -> str:
        path_lower = path.lower()
        content_sample = content[:1000].lower()

        if "tql" in path_lower and "chart" in path_lower:
            return "tql_charts"
        elif "api" in path_lower and "example" in path_lower:
            return "api_examples"
        elif "dbms" in path_lower:
            return "dbms"
        elif "security" in path_lower:
            return "security"
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
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content_lines = []

        for i, line in enumerate(lines):
            header_match = re.match(r'^(#{1,6})\s+(.+)', line)
            if header_match:
                if current_section:
                    current_section.content = '\n'.join(current_content_lines)
                    current_section.line_end = i - 1
                    sections.append(current_section)
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = DocumentSection(
                    title=title, level=level, content="",
                    line_start=i, line_end=i
                )
                current_content_lines = []
            else:
                if current_section:
                    current_content_lines.append(line)

        if current_section:
            current_section.content = '\n'.join(current_content_lines)
            current_section.line_end = len(lines) - 1
            sections.append(current_section)

        return sections

    def _extract_code_blocks_detailed(self, content: str) -> List[CodeBlock]:
        code_blocks = []
        lines = content.split('\n')
        in_code_block = False
        current_language = ""
        current_code_lines = []
        start_line = 0

        for i, line in enumerate(lines):
            if line.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    current_language = line[3:].strip()
                    current_code_lines = []
                    start_line = i
                else:
                    in_code_block = False
                    code = '\n'.join(current_code_lines)
                    if code.strip():
                        code_blocks.append(CodeBlock(
                            language=current_language, code=code,
                            line_start=start_line, line_end=i
                        ))
                    current_language = ""
                    current_code_lines = []
            elif in_code_block:
                current_code_lines.append(line)

        return code_blocks

    def search_files(self, pattern: str) -> List[str]:
        pattern_lower = pattern.lower()
        matching_files = []
        for key in self.file_index.keys():
            if pattern_lower in key.lower():
                matching_files.append(key)
        return matching_files[:10]

# Global document extractor
document_extractor = DocumentContentExtractor()


# ═══════════════════════════════════════════════════════════════
#                      MCP TOOLS
# ═══════════════════════════════════════════════════════════════


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 1] Database Tools                                   │
# │  API: /db/query  |  Auth: None                              │
# └─────────────────────────────────────────────────────────────┘

@mcp.tool()
async def list_tables(
    host: Optional[str] = None,
    port: Optional[int] = None
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
    host: Optional[str] = None,
    port: Optional[int] = None
) -> str:
    """Get tag list from a specific table in Machbase Neo."""
    if not table_name:
        return "Please specify table name."

    table_name = table_name.upper()

    is_valid, error_msg = validate_table_name(table_name)
    if not is_valid:
        logger.warning(f"Invalid table name detected: '{table_name}'")
        return f"Invalid table name: {error_msg}"

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

        tags_query = f"SELECT * FROM _{table_name}_meta"

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
            csv_reader = csv.reader(io.StringIO(response.text.strip()))
            rows = list(csv_reader)

            if len(rows) < 2:
                return f"No tags found in table '{table_name}' (NAME column)."

            tags = []
            for row in rows[1:]:
                if row and len(row) > 0 and row[1].strip():
                    tags.append(f"• {row[1]}")

            if tags:
                tag_count = len(tags)
                tag_list = "\n".join(tags)
                result = f"Tags in table '{table_name}' ({machbase_url}) :\n"
                result += f"Tag column: NAME\n"
                result += f"Found {tag_count} tags:\n\n{tag_list}"

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
    host: Optional[str] = None,
    port: Optional[int] = None
) -> str:
    """
        Execute SQL query directly.

        **IMPORTANT: Always check table structure first to understand column names, data types, and time intervals before execution.**
        **MANDATORY: Must use Machbase Neo documentation only. Use get_full_document_content or get_document_sections to find exact syntax before writing any queries. General SQL knowledge must not be used - only documented Machbase Neo syntax and functions are allowed.**
        **EXECUTION POLICY: Must test and verify all SQL queries before providing them as answers. Only provide successfully executed and validated code to users.**

        **DATA RANGE POLICY (CRITICAL - DEFAULT BEHAVIOR):**
        - ALWAYS use the FULL data range by default. Do NOT add WHERE time filters or LIMIT unless the user explicitly requests a specific time range or sample size.
        - For large datasets, use ROLLUP to aggregate the full range rather than sampling a small time window.
        - Only narrow down the time range or apply LIMIT when the user explicitly specifies it.
        - WRONG: Arbitrarily picking 1-second or small windows to "sample" the data.
        - CORRECT: Use ROLLUP('sec', N, TIME) or similar aggregation to cover the entire dataset.

        **MATH FUNCTION LIMITATION:**
        Machbase Neo SQL does NOT support: SQRT(), POW(), LOG(), LOG2(), LOG10(), EXP(), SIN(), COS(), TAN(), CEIL(), FLOOR()
        Supported SQL math functions: ABS(), ROUND(), TRUNC(), SUMSQ(), STDDEV(), VARIANCE()
        For unsupported math functions, use TQL with MAPVALUE instead:
            SQL(`SELECT NAME, TIME, VALUE FROM table WHERE ...`)
            MAPVALUE(2, sqrt(value(2)))
            CHART() or CSV()

        **RMS CALCULATION (CRITICAL):**
        - RMS = sqrt(SUMSQ(VALUE) / COUNT(VALUE)). SUMSQ alone is NOT RMS.
        - SQL cannot compute RMS directly (no SQRT). Use TQL:
            SQL(`SELECT ROLLUP(...) as rtime, SUMSQ(VALUE) as SS, COUNT(VALUE) as CNT FROM ... GROUP BY rtime`)
            MAPVALUE(1, sqrt(value(1)/value(2)))
            POPVALUE(2)
            SCRIPT({
                $.yield([$.values[0], $.values[1]])
            })
            CHART(
                tz('Asia/Seoul'),
                chartOption({
                    xAxis: { type: "time" },
                    yAxis: { type: "value" },
                    series: [{ type: "line", data: column(0) }]
                })
            )

        If no data is returned, it will be treated as a failure.
    """

    if not sql_query or not sql_query.strip():
        return "Please enter SQL query."

    # ── Detect unsupported SQL math functions → suggest TQL workaround ──
    _TQL_ONLY_MATH_FUNCS = {
        "SQRT": "sqrt",
        "POW": "pow",
        "LOG": "log",
        "LOG2": "log2",
        "LOG10": "log10",
        "EXP": "exp",
        "SIN": "sin",
        "COS": "cos",
        "TAN": "tan",
        "CEIL": "ceil",
        "FLOOR": "floor",
    }
    detected = []
    for sql_fn, tql_fn in _TQL_ONLY_MATH_FUNCS.items():
        if re.search(rf'\b{sql_fn}\s*\(', sql_query, re.IGNORECASE):
            detected.append((sql_fn, tql_fn))

    if detected:
        fn_list = ", ".join(f"{s}()" for s, _ in detected)
        tql_examples = "\n".join(
            f"  MAPVALUE(N, {t}(value(N)))" for _, t in detected
        )
        return (
            f"UNSUPPORTED SQL FUNCTION\n\n"
            f"Machbase Neo SQL does not support: {fn_list}\n"
            f"Supported SQL math functions: ABS(), ROUND(), TRUNC(), SUMSQ(), STDDEV(), VARIANCE()\n\n"
            f"WORKAROUND: Use TQL with MAPVALUE instead.\n"
            f"TQL supports these math functions via MAPVALUE:\n"
            f"  sqrt, pow, log, log2, log10, exp, sin, cos, tan, ceil, floor, etc.\n\n"
            f"Example TQL pattern:\n"
            f"  SQL(`SELECT NAME, TIME, VALUE FROM table_name WHERE ...`)\n"
            f"{tql_examples}\n"
            f"  CHART() or CSV()\n\n"
            f"Use execute_tql_script() to run TQL scripts."
        )

    machbase_url = get_machbase_url(host, port)

    try:
        params = {
            "q": sql_query,
            "format": "csv",
            "timeformat": timeformat,
            "tz": timezone
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
                csv_reader = csv.reader(io.StringIO(response.text.strip()))
                rows_list = list(csv_reader)

                if len(rows_list) < 1:
                    return f"SQL query execution failed (no data returned)\nServer: {machbase_url}\n\n=== SQL CONTENT ===\n```sql\n{sql_query}\n```"

                headers = rows_list[0]
                rows = [dict(zip(headers, row)) for row in rows_list[1:]]

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


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 2] TQL Tools                                        │
# │  API: /db/tql  |  Auth: None                                │
# └─────────────────────────────────────────────────────────────┘

@mcp.tool()
async def execute_tql_script(
    tql_content: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
    timeout_seconds: int = 60

) -> str:
    """
    **MANDATORY EXECUTION WORKFLOW - MUST FOLLOW IN ORDER:**

    0. **DATA RANGE POLICY (CRITICAL - DEFAULT BEHAVIOR):**
    - ALWAYS analyze and chart the FULL data range by default.
    - Do NOT arbitrarily sample small time windows (e.g., 1-second snippets). This misrepresents the data.
    - For high-frequency data, use ROLLUP to aggregate the entire dataset into a reasonable number of points.
    - Only narrow down to a specific time range when the user explicitly requests it.
    - WRONG: `WHERE TIME BETWEEN ... AND ...` with arbitrary small window for "sampling"
    - CORRECT: `ROLLUP('sec', N, TIME)` covering the full dataset without time filter

    1. **PRE-EXECUTION VALIDATION (REQUIRED BEFORE CALLING THIS FUNCTION):**
    - Use execute_sql_query to verify table exists and has data
    - Check actual data samples: SELECT * FROM table LIMIT 10
    - Identify column names, data types, and time ranges
    - For tag tables: use list_table_tags to verify tag names
    - NEVER call this function without verifying data exists first
    - **NEW: For CHART() functions, use validate_chart_tql() FIRST to check column references**

    2. **DOCUMENTATION CHECK (REQUIRED):**
    - TQL syntax is unique to Machbase Neo
    - MUST use get_full_document_content('tql/tql-*.md') before writing TQL
    - MUST use extract_code_blocks('tql/tql-*.md') to see exact syntax
    - Only use syntax and examples from official documentation
    - NO assumptions or general query language knowledge allowed

    3. **CHART VALIDATION (NEW - FOR CHART() FUNCTIONS):**
    - **ALWAYS use validate_chart_tql() before executing charts**
    - Common error: column(N) where N >= actual column count
    - HTTP 200 + chartID does NOT guarantee chart renders correctly
    - Blank charts usually mean column reference errors
    - Workflow for charts:
        a) validate_chart_tql(tql_script) - Check for issues
        b) If INVALID_COLUMN status, use the fixed TQL
        c) execute_tql_script(fixed_tql) - Execute validated code

    4. **EXECUTION BEFORE RESPONSE (CRITICAL - MUST EXECUTE FIRST):**
    **NEVER create artifacts or provide code without executing TQL first**
    **ALWAYS call execute_tql_script() BEFORE responding to user**
    **Test at least ONE complete example before creating any artifact**

    Workflow:
    a) Write TQL code
    b) For CHART(): validate_chart_tql() first
    c) Execute with execute_tql_script()
    d) Verify execution success
    e) Only then provide code to user or create artifact

    If execution fails:
    - Fix the code
    - Execute again
    - Repeat until successful
    - NEVER give users code that hasn't been successfully executed

    5. **TQL CHART SYNTAX (CRITICAL - STRICT VALIDATION):**
    - SQL returns columns: value(0), value(1), value(2)...
    - column(N) collects ALL records' Nth value as array
    - **FORBIDDEN SYNTAX: column(N, M) does NOT exist in TQL**
    - **ONLY VALID: column(N) where N is a single integer**
    - **USE validate_chart_tql() to verify column indices are valid**
    - For time-series charts, use SCRIPT to create [time, value] pairs:
        * SCRIPT({ $.yield([$.values[0], $.values[1]]) })
        * xAxis: { type: "time" }  // NO data property
        * series: [{ data: column(0) }]  // column(0) contains [time, value] pairs
    - Machbase TIME is nanoseconds (10^18) which overflows JS MAX_SAFE_INTEGER
    - tz('Asia/Seoul') converts nanoseconds to milliseconds for proper display
    - ALWAYS use tz('Asia/Seoul') in CHART() for KST display

    6. **EXECUTION & RESULT VALIDATION:**
    - This function executes TQL and validates the response
    - HTTP 200 + empty response = FAILURE (no data)
    - HTTP 200 + chartID only = UNVERIFIED (cannot confirm data)
    - **For UNVERIFIED charts, use validate_chart_tql() to diagnose**
    - Must contain actual data or explicit success indicators

    7. **POST-EXECUTION POLICY:**
    - NEVER provide TQL code to user if this function returns FAILURE
    - If result says "no data returned", DO NOT give code to user
    - If result is "UNVERIFIED", run additional SQL checks to confirm
    - **For charts: If UNVERIFIED, run validate_chart_tql() immediately**
    - Only provide successfully validated code to users

    8. **CHART TIMEZONE (CRITICAL - MUST USE tz()):**
    - For time-series charts, ALWAYS use tz('Asia/Seoul') inside CHART() to display KST time.
    - xAxis type MUST be "time" (NOT "category") for proper timezone conversion.
    - NEVER use MAPVALUE(0, list(value(0)/1000000, value(1))) for time conversion. Use tz() instead.

    WRONG - separate xAxis.data and series.data (nanoseconds overflow JS MAX_SAFE_INTEGER):
        SQL(`SELECT TIME, VALUE FROM SENSOR WHERE NAME = 'tag-01'`)
        CHART(
            tz('Asia/Seoul'),
            chartOption({
                xAxis: { type: "time", data: column(0) },
                series: [{ type: "line", data: column(1) }]
            })
        )

    CORRECT - use SCRIPT to create [time, value] pairs, then tz() in CHART():
        SQL(`SELECT TIME, VALUE FROM SENSOR WHERE NAME = 'tag-01'`)
        SCRIPT({
            $.yield([$.values[0], $.values[1]])
        })
        CHART(
            tz('Asia/Seoul'),
            chartOption({
                xAxis: { type: "time" },
                yAxis: { type: "value" },
                series: [{ type: "line", data: column(0) }]
            })
        )

    - SCRIPT creates [time, value] pairs so column(0) contains the paired data
    - tz('Asia/Seoul') converts nanosecond timestamps to milliseconds for display
    - xAxis type MUST be "time" with NO data property when using paired data

    9. **TQL COMMENT SYNTAX:**
    - ONLY use single-line comments with //
    - Block comments /* */ are NOT supported in TQL
    - All comments must use // syntax only

    10. **HTTP() FUNCTION RESTRICTIONS:**
    - NEVER use SCRIPT() function inside HTTP() function calls
    - HTTP() must only contain direct HTTP endpoint URLs or string values
    - For dynamic content generation, use QUERY() or CSV() functions instead
    - SCRIPT() should be used separately, not nested in HTTP()

    Example:
    WRONG: HTTP(SCRIPT({...some logic...}))
    CORRECT: HTTP("http://example.com/data")
    CORRECT: QUERY("sql", "SELECT ...", ...) | HTTP()

    WRONG: Write code → Create artifact → Hope it works
    CORRECT: Write code → Validate (if CHART) → Execute → Verify → Create artifact

    11. **MATH FUNCTIONS (MUST USE MAPVALUE):**
    TQL provides math functions NOT available in SQL: sqrt, pow, log, log2, log10, exp, sin, cos, tan, ceil, floor, etc.
    These functions MUST be used inside MAPVALUE(), NOT inside SQL().

    **CRITICAL: NEVER apply math to TIME column. Only apply to VALUE columns.**

    MAPVALUE index MUST match the VALUE column index from SQL SELECT:
        SQL SELECT columns → value(0), value(1), value(2)...
        Apply math ONLY to VALUE columns, NEVER to TIME or NAME columns.

    WRONG - math on TIME column (index 0):
        SQL(`SELECT TIME, VALUE FROM SENSOR WHERE NAME = 'tag-01'`)
        MAPVALUE(0, value(0)*1000000)     // WRONG! This corrupts TIME

    WRONG - math function inside SQL():
        SQL(`SELECT sqrt(VALUE) FROM SENSOR WHERE ...`)

    CORRECT - 2 columns (TIME=0, VALUE=1) → math on index 1:
        SQL(`SELECT TIME, VALUE FROM SENSOR WHERE NAME = 'tag-01'`)
        MAPVALUE(1, sqrt(value(1)))       // CORRECT: sqrt on VALUE (index 1)
        CSV()

    CORRECT - 3 columns (NAME=0, TIME=1, VALUE=2) → math on index 2:
        SQL(`SELECT NAME, TIME, VALUE FROM SENSOR WHERE ...`)
        MAPVALUE(2, sqrt(value(2)))       // CORRECT: sqrt on VALUE (index 2)
        CSV()

    With CHART:
        SQL(`SELECT TIME, VALUE FROM SENSOR WHERE NAME = 'tag-01'`)
        MAPVALUE(1, sqrt(value(1)))       // sqrt on VALUE, not TIME
        SCRIPT({
            $.yield([$.values[0], $.values[1]])
        })
        CHART(
            tz('Asia/Seoul'),
            chartOption({
                xAxis: { type: "time" },
                yAxis: { type: "value" },
                series: [{ type: "line", data: column(0) }]
            })
        )

    Available TQL math functions:
        sqrt(x), pow(x,y), log(x), log2(x), log10(x), exp(x), exp2(x),
        sin(x), cos(x), tan(x), sinh(x), cosh(x), tanh(x),
        ceil(x), floor(x), round(x), trunc(x), abs(x), mod(x,y)

    **RMS CALCULATION (CRITICAL):**
    - RMS = sqrt(SUMSQ(VALUE) / COUNT(VALUE)). SUMSQ alone is NOT RMS.
    - Example TQL pattern:
        SQL(`SELECT ROLLUP(...) as rtime, SUMSQ(VALUE) as SS, COUNT(VALUE) as CNT FROM ... GROUP BY rtime`)
        MAPVALUE(1, sqrt(value(1)/value(2)))
        POPVALUE(2)
        SCRIPT({
            $.yield([$.values[0], $.values[1]])
        })
        CHART(
            tz('Asia/Seoul'),
            chartOption({
                xAxis: { type: "time" },
                yAxis: { type: "value" },
                series: [{ type: "line", data: column(0) }]
            })
        )
    """

    if not tql_content or not tql_content.strip():
        return "ERROR: Please provide TQL script content to execute."

    machbase_url = get_machbase_url(host, port)
    execution_id = str(uuid.uuid4())[:8]

    # Syntax validation: column() must have single argument only
    if re.search(r'column\s*\([^)]*,[^)]*\)', tql_content):
        return (
            "INVALID TQL SYNTAX\n\n"
            "Error: column() accepts ONLY ONE argument\n\n"
            "WRONG: column(0, 1)\n"
            "CORRECT: column(0) and column(1) separately\n\n"
            "Example (time-series):\n"
            "  SCRIPT({ $.yield([$.values[0], $.values[1]]) })\n"
            "  CHART(tz('Asia/Seoul'), chartOption({\n"
            "    xAxis: { type: 'time' },\n"
            "    series: [{ data: column(0) }]\n"
            "  }))\n"
        )

    # Detect unsupported math functions inside SQL() blocks in TQL
    sql_block_match = re.search(r'SQL\s*\(\s*`([^`]*)`\s*\)', tql_content, re.IGNORECASE | re.DOTALL)
    if sql_block_match:
        sql_inner = sql_block_match.group(1)
        _TQL_ONLY_MATH = ["SQRT", "POW", "LOG", "LOG2", "LOG10", "EXP", "EXP2",
                          "SIN", "COS", "TAN", "SINH", "COSH", "TANH", "CEIL", "FLOOR"]
        found_in_sql = [fn for fn in _TQL_ONLY_MATH
                        if re.search(rf'\b{fn}\s*\(', sql_inner, re.IGNORECASE)]
        if found_in_sql:
            fn_list = ", ".join(f"{f}()" for f in found_in_sql)
            return (
                "INVALID TQL SYNTAX\n\n"
                f"Error: {fn_list} cannot be used inside SQL(). "
                "These are TQL math functions, not SQL functions.\n\n"
                "WRONG:\n"
                f"  SQL(`SELECT {found_in_sql[0]}(VALUE) FROM table WHERE ...`)\n\n"
                "CORRECT: Use MAPVALUE after SQL():\n"
                "  SQL(`SELECT NAME, TIME, VALUE FROM table WHERE ...`)\n"
                f"  MAPVALUE(2, {found_in_sql[0].lower()}(value(2)))\n"
                "  CSV()\n"
            )

    # Detect math operations applied to TIME column via MAPVALUE
    if sql_block_match and re.search(r'SELECT\s+TIME\b', sql_block_match.group(1), re.IGNORECASE):
        if re.search(r'MAPVALUE\s*\(\s*0\s*,\s*value\s*\(\s*0\s*\)\s*[*/+-]', tql_content):
            return (
                "INVALID TQL: Math operation on TIME column\n\n"
                "MAPVALUE(0, value(0)*...) modifies the TIME column. "
                "Math must target VALUE columns only.\n\n"
                "WRONG:\n"
                "  SQL(`SELECT TIME, VALUE FROM table WHERE ...`)\n"
                "  MAPVALUE(0, value(0)*1000000)\n\n"
                "CORRECT:\n"
                "  SQL(`SELECT TIME, VALUE FROM table WHERE ...`)\n"
                "  MAPVALUE(1, value(1)*1000000)   // math on VALUE (index 1)\n"
                "  CSV()\n"
            )

    # Detect time() function usage with TIME columns
    if re.search(r'MAPVALUE\s*\([^)]*,\s*time\s*\(\s*value\s*\(\s*\d+\s*\)', tql_content):
        return (
            "INVALID TQL SYNTAX\n\n"
            "Error: time() function is not valid for formatting in MAPVALUE\n\n"
            "WRONG: MAPVALUE(0, time(value(1), \"DEFAULT\", \"Local\"))\n"
            "CORRECT: MAPVALUE(0, strTime(value(1), \"15:04:05\", tz(\"Local\")))\n"
        )

    # Warn if value(N) is used without formatting
    if re.search(r'MAPVALUE\s*\(\s*\d+\s*,\s*value\s*\(\s*\d+\s*\)\s*\)', tql_content):
        return (
            "POTENTIAL TQL ISSUE\n\n"
            "If the value is a TIME column, use strTime() for formatting:\n"
            "  MAPVALUE(0, strTime(value(N), \"15:04:05\", tz(\"Local\")))\n"
        )

    # Detect HTTP() followed by SCRIPT() pattern - FORBIDDEN
    if re.search(r'HTTP\s*\([^)]*\)\s*SCRIPT\s*\(', tql_content, re.IGNORECASE | re.DOTALL):
        return (
            "INVALID TQL SYNTAX\n\n"
            "Error: SCRIPT() cannot be placed immediately after HTTP()\n\n"
            "WRONG:\n"
            "  HTTP({...})\n"
            "  SCRIPT({...})\n\n"
            "CORRECT:\n"
            "  HTTP({...})\n"
            "  TEXT() or CSV() or other output function\n\n"
            "SCRIPT() must be used in a separate pipeline, not directly after HTTP().\n"
        )

    # ── CHART pre-validation: auto-call validate_chart_tql for CHART() scripts ──
    if re.search(r'CHART\s*\(', tql_content, re.IGNORECASE):
        try:
            chart_report = await validate_chart_tql(tql_content, auto_fix=True, host=host, port=port)
            if "STATUS: NO_DATA" in chart_report:
                return (
                    f"FAILURE: Chart validation failed - query returns no data (ID: {execution_id})\n"
                    f"Server: {machbase_url}\n\n"
                    "    DO NOT PROVIDE CODE TO USER - FIX THE ISSUE FIRST\n\n"
                    f"=== VALIDATION REPORT ===\n{chart_report}\n\n"
                    f"=== TQL CONTENT (for debugging) ===\n```tql\n{tql_content}\n```"
                )
            if "STATUS: ERROR" in chart_report:
                return (
                    f"FAILURE: Chart validation failed (ID: {execution_id})\n"
                    f"Server: {machbase_url}\n\n"
                    "    DO NOT PROVIDE CODE TO USER - FIX THE ISSUE FIRST\n\n"
                    f"=== VALIDATION REPORT ===\n{chart_report}\n\n"
                    f"=== TQL CONTENT (for debugging) ===\n```tql\n{tql_content}\n```"
                )
            if "STATUS: INVALID_COLUMN" in chart_report or "STATUS: NEGATIVE_INDEX" in chart_report:
                fixed_match = re.search(r'=== FIXED TQL ===\s*```tql\s*\n(.*?)```', chart_report, re.DOTALL)
                if fixed_match:
                    tql_content = fixed_match.group(1).strip()
                    logger.info(f"[{execution_id}] Chart validation auto-fixed column references")
                else:
                    return (
                        f"FAILURE: Chart has invalid column references and auto-fix failed (ID: {execution_id})\n"
                        f"Server: {machbase_url}\n\n"
                        "    DO NOT PROVIDE CODE TO USER - FIX THE ISSUE FIRST\n\n"
                        f"=== VALIDATION REPORT ===\n{chart_report}\n\n"
                        f"=== TQL CONTENT (for debugging) ===\n```tql\n{tql_content}\n```"
                    )
        except Exception as e:
            logger.warning(f"[{execution_id}] Chart pre-validation failed, proceeding with execution: {e}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{machbase_url}/db/tql",
                content=tql_content,
                headers={"Content-Type": "text/plain"},
                timeout=timeout_seconds
            )

            if response.status_code == 200:
                response_text = response.text.strip()

                if not response_text:
                    result = f"FAILURE: TQL execution returned no data (ID: {execution_id})\n"
                    result += f"Server: {machbase_url}\n"
                    result += f"Status: HTTP {response.status_code}\n\n"
                    result += "=== FAILURE REASON ===\n"
                    result += "Query executed successfully, but returned no data.\n"
                    result += "Possible causes:\n"
                    result += "  1. Table is empty (verify with: SELECT COUNT(*) FROM table)\n"
                    result += "  2. WHERE condition filters out all data\n"
                    result += "  3. Tag name is incorrect (verify with: list_table_tags)\n"
                    result += "  4. Time range has no data\n\n"
                    result += "    DO NOT PROVIDE THIS CODE TO USER - FIX THE ISSUE FIRST\n\n"
                    result += "=== TQL CONTENT (for debugging) ===\n"
                    result += f"```tql\n{tql_content}\n```"
                    return result

                result = f"Server: {machbase_url}\n"
                result += f"Status: HTTP {response.status_code}\n"
                result += f"Execution ID: {execution_id}\n\n"

                if '"chartID"' in response_text or 'chartID' in response_text:
                    result = f"REQUIRES_VERIFICATION: TQL returned chart response (ID: {execution_id})\n" + result
                    result += "=== RESPONSE ===\n"
                    result += response_text + "\n\n"
                    result += "DO NOT PROVIDE CODE TO USER - VERIFICATION REQUIRED\n\n"
                    result += "Reason: Chart ID returned but data presence unconfirmed (empty charts can have valid IDs)\n\n"

                    table_match = re.search(r'FROM\s+([A-Z_][A-Z0-9_]*)', tql_content, re.IGNORECASE)
                    if table_match:
                        table_name = table_match.group(1)
                        where_match = re.search(r'WHERE\s+(.+?)(?:LIMIT|GROUP|ORDER|$)', tql_content, re.IGNORECASE | re.DOTALL)
                        where_clause = where_match.group(1).strip() if where_match else "1=1"
                        result += f"Verify data exists:\n"
                        result += f"  execute_sql_query(\"SELECT COUNT(*) FROM {table_name} WHERE {where_clause}\")\n\n"
                    else:
                        result += "Manually verify: SELECT COUNT(*) FROM your_table WHERE your_conditions\n\n"
                    result += "Only provide code to user after confirming COUNT > 0\n"

                elif 'csv' in response_text.lower() or '\n' in response_text[:200]:
                    result = f"   SUCCESS: TQL execution completed with data (ID: {execution_id})\n" + result
                    result += "=== RESPONSE ===\n"
                    result += response_text + "\n\n"
                    result += "   Code verified and safe to provide to user.\n"

                else:
                    result = f"    UNVERIFIED: TQL returned unknown response format (ID: {execution_id})\n" + result
                    result += "=== RESPONSE ===\n"
                    result += response_text + "\n\n"
                    result += "    Cannot determine if execution was successful.\n"
                    result += "    Verify result manually before providing code to user.\n"

                return result

            else:
                result = f"FAILURE: TQL execution failed (ID: {execution_id})\n"
                result += f"Server: {machbase_url}\n"
                result += f"Status: HTTP {response.status_code}\n\n"

                if response.text.strip():
                    result += "=== ERROR RESPONSE ===\n"
                    result += response.text + "\n\n"

                result += "DO NOT PROVIDE THIS CODE TO USER - FIX THE ERROR FIRST\n\n"
                result += "=== TQL CONTENT (for debugging) ===\n"
                result += f"```tql\n{tql_content}\n```"

                return result

    except httpx.ConnectError:
        return f"FAILURE: Cannot connect to Machbase Neo server\n" + \
               f"Server: {machbase_url}\n" + \
               f"Execution ID: {execution_id}\n\n" + \
               "    DO NOT PROVIDE CODE TO USER - Server connection failed\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"

    except httpx.TimeoutException:
        return f"FAILURE: TQL execution timeout after {timeout_seconds} seconds\n" + \
               f"Server: {machbase_url}\n" + \
               f"Execution ID: {execution_id}\n\n" + \
               "    DO NOT PROVIDE CODE TO USER - Query timeout\n" + \
               "    Possible causes: Query too complex, large data, or server overload\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"

    except Exception as e:
        logger.error(f"TQL execution error: {e}")
        return f"FAILURE: TQL execution error (ID: {execution_id})\n" + \
               f"Server: {machbase_url}\n" + \
               f"Error: {str(e)}\n\n" + \
               "    DO NOT PROVIDE CODE TO USER - Unexpected error occurred\n\n" + \
               "=== TQL CONTENT (for debugging) ===\n" + \
               f"```tql\n{tql_content}\n```"


@mcp.tool()
async def validate_chart_tql(
    tql_script: str,
    auto_fix: bool = True,
    add_validation_script: bool = False,
    host: Optional[str] = None,
    port: Optional[int] = None
) -> str:
    """
    Validate TQL chart script for data existence and column reference errors.

    **4-STEP VALIDATION PROCESS:**

    1. **DATA EXISTENCE CHECK**
       - Extracts SQL query from TQL script
       - Executes query to verify data exists
       - Counts rows and columns in result set
       - For FAKE() data, analyzes dimensions

    2. **COLUMN REFERENCE VALIDATION**
       - Finds all column(N) references in CHART() sections
       - Validates each column index against actual data dimensions
       - Identifies out-of-range column references
       - Detects negative column indices

    3. **EMPTY CHART OPTION CHECK**
       - Detects empty chartOption({})
       - Detects missing series in chartOption
       - Applies default time-series chart template

    4. **AUTO-FIX CAPABILITY**
       - Replaces invalid column references with nearest valid column
       - Fixes negative indices to 0
       - Generates complete time-series chart for empty options
       - Adds data transformation (MAPVALUE) when needed
       - Adds comments showing original invalid references

    Args:
        tql_script: TQL script containing CHART() function
        auto_fix: Automatically fix invalid column references
        add_validation_script: Add runtime validation code
        host: Machbase server host
        port: Machbase server port

    Returns:
        Validation report with optional fixed TQL code
    """

    machbase_url = get_machbase_url(host, port)

    def extract_sql(tql: str) -> Optional[str]:
        patterns = [
            r'SQL\s*\(\s*["\']([^"\']+)["\']',
            r'SQL\s*\(\s*`([^`]+)`',
            r'SQL_SELECT\s*\([^)]+from\s*\(["\']([^"\']+)["\']',
        ]
        for pattern in patterns:
            match = re.search(pattern, tql, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return None

    def get_fake_dimensions(tql: str) -> Tuple[int, int]:
        rows, cols = 0, 1
        arrange_match = re.search(r'arrange\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', tql)
        if arrange_match:
            start = int(arrange_match.group(1))
            end = int(arrange_match.group(2))
            step = int(arrange_match.group(3))
            rows = (end - start) // step
        linspace_match = re.search(r'linspace\s*\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*(\d+)\s*\)', tql)
        if linspace_match:
            rows = int(linspace_match.group(1))
        mapvalue_matches = re.findall(r'MAPVALUE\s*\(\s*(\d+)\s*,', tql)
        if mapvalue_matches:
            max_col = max(int(m) for m in mapvalue_matches)
            cols = max_col + 1
        return rows, cols

    def find_column_refs(tql: str) -> Tuple[List[int], List[int]]:
        column_matches = re.findall(r'column\s*\(\s*(-?\d+)\s*\)', tql)
        refs = [int(m) for m in column_matches]
        positive_refs = sorted(set(r for r in refs if r >= 0))
        negative_refs = sorted(set(r for r in refs if r < 0))
        return positive_refs, negative_refs

    def is_empty_chart_option(tql: str) -> bool:
        if re.search(r'chartOption\s*\(\s*\{\s*\}\s*\)', tql):
            return True
        chart_match = re.search(r'chartOption\s*\(\s*\{([^}]+)\}\s*\)', tql, re.DOTALL)
        if chart_match:
            content = chart_match.group(1)
            if 'series' not in content:
                return True
        return False

    def generate_default_chart(col_count: int) -> str:
        if col_count == 2:
            transformation = "SCRIPT({\n    $.yield([$.values[0], $.values[1]])\n})\n"
        elif col_count == 3:
            transformation = "SCRIPT({\n    $.yield([$.values[1], $.values[2]])\n})\n"
        else:
            transformation = "SCRIPT({\n    $.yield([$.values[0], $.values[1]])\n})\n"

        chart_template = """CHART(
    tz('Asia/Seoul'),
    chartOption({
        title: { text: "Time Series Chart" },
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Value" },
        tooltip: { trigger: "axis" },
        series: [{ type: "line", data: column(0), smooth: true }]
    }))
"""
        return transformation + chart_template

    result_lines = []
    result_lines.append("=== TQL CHART VALIDATION REPORT ===\n")
    issues = []

    # Step 1: Data Existence Check
    result_lines.append("[STEP 1] DATA EXISTENCE CHECK")

    sql = extract_sql(tql_script)
    row_count = 0
    col_count = 0

    if sql is None:
        rows, cols = get_fake_dimensions(tql_script)
        if rows > 0:
            row_count, col_count = rows, cols
            result_lines.append(f"✓ FAKE data detected: {row_count} rows × {col_count} columns")
        else:
            result_lines.append("✗ Cannot determine FAKE data dimensions")
            result_lines.append("\nSTATUS: ERROR")
            result_lines.append("REASON: Unable to analyze FAKE data structure")
            return "\n".join(result_lines)
    else:
        try:
            count_sql = re.sub(
                r'SELECT\s+.*?\s+FROM',
                'SELECT COUNT(*) as cnt FROM',
                sql,
                flags=re.IGNORECASE | re.DOTALL
            )
            count_sql = re.sub(r'LIMIT\s+\d+', '', count_sql, flags=re.IGNORECASE)

            params = urlencode({"q": count_sql, "format": "json"})

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{machbase_url}/db/query?{params}",
                    timeout=10.0
                )

                if response.status_code == 200:
                    result = json.loads(response.text)
                    row_count = result.get('data', {}).get('rows', [[0]])[0][0]

                    if row_count == 0:
                        result_lines.append(f"✗ Query returned no data")
                        result_lines.append("\nSTATUS: NO_DATA")
                        result_lines.append("REASON: SQL query returned 0 rows")
                        result_lines.append(f"SQL: {sql}")
                        return "\n".join(result_lines)

                    sample_sql = sql if 'LIMIT' in sql.upper() else f"{sql} LIMIT 1"
                    params = urlencode({"q": sample_sql, "format": "json"})

                    response = await client.get(
                        f"{machbase_url}/db/query?{params}",
                        timeout=10.0
                    )

                    if response.status_code == 200:
                        result = json.loads(response.text)
                        col_count = len(result.get('data', {}).get('columns', []))
                        result_lines.append(f"✓ Query data: {row_count} rows × {col_count} columns")
                else:
                    result_lines.append(f"✗ Query execution failed: HTTP {response.status_code}")
                    result_lines.append("\nSTATUS: ERROR")
                    result_lines.append(f"REASON: {response.text}")
                    return "\n".join(result_lines)

        except Exception as e:
            result_lines.append(f"✗ Query execution error: {str(e)}")
            result_lines.append("\nSTATUS: ERROR")
            result_lines.append(f"REASON: {str(e)}")
            return "\n".join(result_lines)

    # Step 2: Column Reference Validation
    result_lines.append("\n[STEP 2] COLUMN REFERENCE VALIDATION")

    positive_refs, negative_refs = find_column_refs(tql_script)
    invalid_columns = [col for col in positive_refs if col >= col_count]

    if negative_refs:
        result_lines.append(f"✗ Negative column indices found: {negative_refs}")
        issues.append(f"Negative indices: {negative_refs}")

    if not positive_refs and not negative_refs:
        result_lines.append("✓ No column() references found in CHART")
    elif invalid_columns:
        result_lines.append(f"✗ Invalid column references found: {invalid_columns}")
        result_lines.append(f"  Valid range: column(0) to column({col_count-1})")
        issues.append(f"Out of range: {invalid_columns}")
    elif not negative_refs:
        result_lines.append(f"✓ All column references valid: {positive_refs}")
        result_lines.append(f"  Valid range: column(0) to column({col_count-1})")

    # Step 3: Empty Chart Option Check
    result_lines.append("\n[STEP 3] EMPTY CHART OPTION CHECK")

    is_empty = is_empty_chart_option(tql_script)
    if is_empty:
        result_lines.append("✗ Empty chartOption detected")
        issues.append("Empty chartOption (no series or completely empty)")
    else:
        result_lines.append("✓ Chart options present")

    # Generate status
    if issues:
        if "Empty chartOption" in str(issues):
            status = "EMPTY_CHART"
        elif negative_refs:
            status = "NEGATIVE_INDEX"
        elif invalid_columns:
            status = "INVALID_COLUMN"
        else:
            status = "WARNING"
    else:
        status = "OK"

    result_lines.append(f"\n=== VALIDATION RESULT ===")
    result_lines.append(f"STATUS: {status}")
    result_lines.append(f"DATA: {row_count} rows × {col_count} columns")

    if issues:
        result_lines.append(f"ISSUES: {', '.join(issues)}")

    # Auto-fix if needed
    fixed_tql = None
    if auto_fix and issues:
        result_lines.append(f"FIXED: Yes")
        fixed_tql = tql_script

        if negative_refs:
            for neg_col in negative_refs:
                pattern = rf'column\s*\(\s*{neg_col}\s*\)'
                replacement = f'column(0)  // Fixed: was column({neg_col})'
                fixed_tql = re.sub(pattern, replacement, fixed_tql)

        if invalid_columns:
            for invalid_col in sorted(invalid_columns, reverse=True):
                valid_col = min(invalid_col, col_count - 1)
                pattern = rf'column\s*\(\s*{invalid_col}\s*\)'
                replacement = f'column({valid_col})  // Fixed: was column({invalid_col})'
                fixed_tql = re.sub(pattern, replacement, fixed_tql)

        if is_empty:
            chart_pattern = r'CHART\s*\(\s*chartOption\s*\(\s*\{[^}]*\}\s*\)\s*\)'
            default_chart = generate_default_chart(col_count)
            fixed_tql = re.sub(chart_pattern, default_chart, fixed_tql, flags=re.DOTALL)

        if add_validation_script:
            validation_code = f"""// === Auto-generated validation script ===
SCRIPT({{
    console.log("Validating chart data dimensions...");
    console.log("Expected columns: {col_count}");
}}, {{
    if ($.values.length < {col_count}) {{
        console.warn("Data has only " + $.values.length + " columns, expected {col_count}");
    }}
    $.yield.apply($, $.values);
}})

"""
            fixed_tql = validation_code + fixed_tql
    elif auto_fix:
        result_lines.append(f"FIXED: No (no issues to fix)")

    result_lines.append(f"\n=== ORIGINAL TQL ===")
    result_lines.append(f"```tql")
    result_lines.append(tql_script)
    result_lines.append(f"```")

    if fixed_tql:
        result_lines.append(f"\n=== FIXED TQL ===")
        result_lines.append(f"```tql")
        result_lines.append(fixed_tql)
        result_lines.append(f"```")
        result_lines.append(f"\n✓ Use the fixed TQL above to avoid chart errors")

    return "\n".join(result_lines)


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 3] File Management Tools                            │
# │  API: /web/api/files  |  Auth: JWT                          │
# └─────────────────────────────────────────────────────────────┘

@mcp.tool()
async def create_folder(
    folder_name: str,
    parent: str = "",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Create a folder in Machbase Neo file system.

    For table analysis workflows, use the naming convention: {table_name}
    Example: "GOLD", "TEST", "SENSOR"

    Args:
        folder_name: Name of the folder to create (e.g., "GOLD")
        parent: Parent path (e.g., "" for root, "project" for /project/)
    """
    parent_path = parent.strip("/") if parent else ""
    full_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
    parent_api_path = _build_folder_api_path(parent_path)

    result = await _create_single_folder(folder_name, parent_api_path, host, port)

    if not result["success"]:
        return json.dumps(
            {"status": "error", "message": f"Failed to create folder '{full_path}': {result['reason']}"},
            indent=2, ensure_ascii=False,
        )

    exists = await _verify_folder_exists(full_path, host, port)

    if exists:
        if result["already_exists"]:
            return json.dumps(
                {"status": "exists", "message": f"Folder '{full_path}' already exists (verified)"},
                indent=2, ensure_ascii=False,
            )
        else:
            return json.dumps(
                {"status": "success", "message": f"Folder '{full_path}' created (verified)"},
                indent=2, ensure_ascii=False,
            )
    else:
        return json.dumps(
            {
                "status": "error",
                "message": f"Folder creation reported success but folder '{full_path}' does not exist. "
                           f"Check server file system permissions or disk path.",
                "api_response": result["reason"],
            },
            indent=2, ensure_ascii=False,
        )


@mcp.tool()
async def list_files(
    path: str = "/",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """List files and folders in Machbase Neo file system.

    Args:
        path: Directory path (e.g., "/" for root, "/test_analysis" for subfolder)
    """
    clean_path = path.strip("/")
    api_path = f"/files/{clean_path}" if clean_path else "/files/"
    try:
        result = await _request("GET", api_path, host, port)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing files: {e}"


@mcp.tool()
async def delete_file(
    filename: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Delete a file or empty folder from Machbase Neo file system.

    Supports all file types: .tql, .sql, .wrk, .dsh, etc.
    For dashboards, you can use either this tool or delete_dashboard().

    Args:
        filename: File path to delete (e.g., "GOLD/chart_v2.tql", "GOLD/analysis.dsh")
    """
    if not filename or not filename.strip():
        return json.dumps(
            {"status": "error", "message": "Filename is required."},
            indent=2, ensure_ascii=False,
        )

    clean = filename.strip("/")

    try:
        await _request("DELETE", f"/files/{clean}", host, port)
        return json.dumps(
            {"status": "success", "message": f"'{clean}' deleted."},
            indent=2, ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Failed to delete '{clean}': {e}"},
            indent=2, ensure_ascii=False,
        )


@mcp.tool()
async def save_tql_file(
    filename: str,
    tql_content: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Save a TQL or SQL script file to Machbase Neo.

    TQL files (.tql) are validated by execution before saving.
    If execution fails or returns empty/error, the file is NOT saved.
    SQL files (.sql) are validated by execution before saving.
    Supports folder paths - parent folders are created automatically.

    **CRITICAL - FILE PATH RULES (MUST FOLLOW):**
    - When analyzing a table, ALL related files MUST go in the SAME folder.
    - Folder naming: {TABLE_NAME} (e.g., "GOLD")
    - ALL TQL files for that table go inside: {TABLE_NAME}/filename.tql
    - NEVER save files to root. ALWAYS use the analysis folder path.
    - Example for GOLD table analysis:
        GOOD: "GOLD/normal_chart.tql"
        GOOD: "GOLD/abnormal_chart.tql"
        BAD:  "normal_chart.tql"  (root - WRONG!)
        BAD:  "GOLD/normal.tql" + "abnormal.tql" (mixed - WRONG!)

    **CRITICAL - TQL CODE CONSISTENCY RULES:**
    - When generating multiple TQL files for the same analysis, use the SAME code pattern.
    - If the first file uses SQL() + MAPVALUE() + CHART(), ALL files must use that pattern.
    - Do NOT mix different approaches (e.g., one with FAKE(), another with SQL()).
    - Keep chart options (colors, styles, axis config) consistent across related files.

    Args:
        filename: File path - MUST include folder (e.g., "GOLD/chart.tql")
        tql_content: Script content (TQL or SQL)
    """
    if not filename.endswith((".tql", ".sql", ".wrk")):
        filename += ".tql"

    # ── Path enforcement: folder path required ──
    if "/" not in filename:
        return json.dumps(
            {
                "status": "error",
                "message": (
                    f"File '{filename}' has no folder path. "
                    "ALL files MUST be saved inside a folder (e.g., 'TABLE/filename.tql'). "
                    "Please retry with a folder path like '{TABLE}/" + filename + "'."
                ),
            },
            indent=2, ensure_ascii=False,
        )

    # ── Validation: execute before saving ──
    if filename.endswith(".tql"):
        base = _get_base_url(host, port)
        validate_url = f"{base}/tql"
        validate_headers = await _get_auth_headers(host, port)
        validate_headers["Content-Type"] = "text/plain"

        try:
            async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
                resp = await client.post(
                    validate_url,
                    content=tql_content,
                    headers=validate_headers,
                )
                # HTTP error
                if resp.status_code >= 400:
                    error_detail = resp.text[:500]
                    return json.dumps(
                        {
                            "status": "validation_failed",
                            "message": f"TQL validation failed (HTTP {resp.status_code}). File NOT saved.",
                            "error": error_detail,
                        },
                        indent=2, ensure_ascii=False,
                    )
                # HTTP 200 but empty response = no data
                resp_text = resp.text.strip()
                if not resp_text:
                    return json.dumps(
                        {
                            "status": "validation_failed",
                            "message": "TQL returned empty response (no data). File NOT saved.",
                            "error": "Query executed but returned no results. Check table/tag names and time range.",
                        },
                        indent=2, ensure_ascii=False,
                    )
                # ── JSON success:false 선체크 (키워드 무관하게) ──
                try:
                    err_body = resp.json()
                    if err_body.get("success") is False:
                        reason = err_body.get("reason", resp_text[:500])
                        return json.dumps(
                            {
                                "status": "validation_failed",
                                "message": f"TQL execution error: {reason}. File NOT saved.",
                                "error": reason,
                            },
                            indent=2, ensure_ascii=False,
                        )
                except (json.JSONDecodeError, ValueError):
                    pass

                # ── 키워드 fallback (mach-err 추가) ──
                resp_lower = resp_text.lower()
                if any(kw in resp_lower for kw in ["error", "fail", "invalid", "not found", "no table", "mach-err"]):
                    return json.dumps(
                        {
                            "status": "validation_failed",
                            "message": "TQL response contains error indicators. File NOT saved.",
                            "error": resp_text[:500],
                        },
                        indent=2, ensure_ascii=False,
                    )

                # ── CHART TQL: SQL 직접 실행으로 이중 검증 ──
                if re.search(r'CHART\s*\(', tql_content, re.IGNORECASE):
                    sql_match = re.search(r'SQL\s*\(\s*`([^`]+)`', tql_content, re.IGNORECASE | re.DOTALL)
                    if not sql_match:
                        sql_match = re.search(r'SQL\s*\(\s*["\']([^"\']+)["\']', tql_content, re.IGNORECASE | re.DOTALL)
                    if sql_match:
                        test_sql = sql_match.group(1).strip()
                        if 'LIMIT' not in test_sql.upper():
                            test_sql += " LIMIT 1"
                        try:
                            db_base = get_machbase_url(host, port)
                            params = urlencode({"q": test_sql, "format": "json"})
                            async with httpx.AsyncClient(timeout=30) as sql_client:
                                sql_resp = await sql_client.get(f"{db_base}/db/query?{params}")
                                if sql_resp.status_code != 200:
                                    return json.dumps(
                                        {
                                            "status": "validation_failed",
                                            "message": f"SQL validation failed: {sql_resp.text[:300]}. File NOT saved.",
                                        },
                                        indent=2, ensure_ascii=False,
                                    )
                                sql_body = sql_resp.json()
                                if sql_body.get("success") is False:
                                    return json.dumps(
                                        {
                                            "status": "validation_failed",
                                            "message": f"SQL error: {sql_body.get('reason', 'unknown')}. File NOT saved.",
                                        },
                                        indent=2, ensure_ascii=False,
                                    )
                        except Exception as e:
                            logger.warning(f"SQL pre-validation skipped: {e}")
        except Exception as e:
            return json.dumps(
                {
                    "status": "validation_failed",
                    "message": f"TQL validation error. File NOT saved.",
                    "error": str(e)[:500],
                },
                indent=2, ensure_ascii=False,
            )

        # ── Static CHART option validation ──
        if re.search(r'CHART\s*\(', tql_content, re.IGNORECASE):
            chart_section = tql_content[tql_content.lower().find('chart('):]
            if 'series' not in chart_section:
                return json.dumps(
                    {
                        "status": "validation_failed",
                        "message": "CHART missing 'series' configuration. File NOT saved.",
                    },
                    indent=2, ensure_ascii=False,
                )
            if 'data' not in chart_section:
                return json.dumps(
                    {
                        "status": "validation_failed",
                        "message": "CHART series missing 'data' field. File NOT saved.",
                    },
                    indent=2, ensure_ascii=False,
                )

        # ── CHART validation: use validate_chart_tql for CHART() scripts ──
        if re.search(r'CHART\s*\(', tql_content, re.IGNORECASE):
            try:
                chart_report = await validate_chart_tql(tql_content, auto_fix=True, host=host, port=port)
                if "STATUS: NO_DATA" in chart_report:
                    return json.dumps(
                        {
                            "status": "validation_failed",
                            "message": "CHART validation failed: query returns no data. File NOT saved.",
                            "detail": chart_report,
                        },
                        indent=2, ensure_ascii=False,
                    )
                if "STATUS: ERROR" in chart_report:
                    return json.dumps(
                        {
                            "status": "validation_failed",
                            "message": "CHART validation failed. File NOT saved.",
                            "detail": chart_report,
                        },
                        indent=2, ensure_ascii=False,
                    )
                # Fixable issues: extract fixed TQL and use it for saving
                if "STATUS: INVALID_COLUMN" in chart_report or "STATUS: NEGATIVE_INDEX" in chart_report:
                    fixed_match = re.search(r'=== FIXED TQL ===\s*```tql\s*\n(.*?)```', chart_report, re.DOTALL)
                    if fixed_match:
                        tql_content = fixed_match.group(1).strip()
                    else:
                        return json.dumps(
                            {
                                "status": "validation_failed",
                                "message": "CHART validation failed: invalid column references and auto-fix unavailable. File NOT saved.",
                                "detail": chart_report,
                            },
                            indent=2, ensure_ascii=False,
                        )

                # ── JS asset validation: blank chart / data errors ──
                try:
                    chart_resp = resp.json()
                    js_assets = chart_resp.get("jsCodeAssets", [])
                    if js_assets and chart_resp.get("chartID"):
                        js_url = f"{base.replace('/web/api', '')}{js_assets[0]}"
                        async with httpx.AsyncClient(timeout=15) as js_client:
                            js_resp = await js_client.get(js_url, headers=validate_headers)
                            if js_resp.status_code == 200:
                                js_content = js_resp.text

                                # JS 파일 크기 체크 (빈 차트)
                                if len(js_content) < 500:
                                    return json.dumps(
                                        {
                                            "status": "validation_failed",
                                            "message": "CHART JS too small - likely empty chart. File NOT saved.",
                                        },
                                        indent=2, ensure_ascii=False,
                                    )

                                # 숫자 데이터 존재 확인
                                numbers = re.findall(r'[-+]?\d+\.?\d*(?:e[-+]?\d+)?', js_content)
                                if len(numbers) < 10:
                                    return json.dumps(
                                        {
                                            "status": "validation_failed",
                                            "message": "CHART has insufficient data points. File NOT saved.",
                                        },
                                        indent=2, ensure_ascii=False,
                                    )

                                # undefined/NaN 감지
                                if 'undefined' in js_content or 'NaN' in js_content.replace('name', '').replace('Name', ''):
                                    return json.dumps(
                                        {
                                            "status": "validation_failed",
                                            "message": "CHART contains undefined/NaN data. File NOT saved.",
                                        },
                                        indent=2, ensure_ascii=False,
                                    )

                                # ns→KST 시간 변환 누락 감지
                                if '"time"' in js_content or "'time'" in js_content:
                                    large_nums = [float(n) for n in numbers if float(n) > 1e15]
                                    if large_nums:
                                        return json.dumps(
                                            {
                                                "status": "validation_failed",
                                                "message": "CHART time axis has nanosecond values (>1e15). "
                                                           "Convert ns to ms (t/1000000) for KST display. File NOT saved.",
                                            },
                                            indent=2, ensure_ascii=False,
                                        )
                except Exception as e:
                    logger.warning(f"JS asset validation skipped: {e}")

            except Exception as e:
                logger.warning(f"CHART validation skipped: {e}")

    elif filename.endswith(".sql"):
        sql_statements = [s.strip() for s in tql_content.split(";") if s.strip()]
        if sql_statements:
            base = _get_base_url(host, port)
            validate_headers = await _get_auth_headers(host, port)
            errors = []
            for i, sql in enumerate(sql_statements):
                lines = [l for l in sql.split("\n") if l.strip() and not l.strip().startswith("--")]
                if not lines:
                    continue
                try:
                    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                        resp = await client.get(
                            f"{base}/query",
                            params={"q": sql},
                            headers=validate_headers,
                        )
                        body = resp.json() if resp.content else {}
                        if not body.get("success", False):
                            reason = body.get("reason", resp.text[:200])
                            errors.append(f"Statement {i+1}: {reason}")
                except Exception as e:
                    errors.append(f"Statement {i+1}: {str(e)[:200]}")

            if errors:
                return json.dumps(
                    {
                        "status": "validation_failed",
                        "message": f"SQL validation failed ({len(errors)} error(s)). File NOT saved.",
                        "errors": errors,
                    },
                    indent=2, ensure_ascii=False,
                )

    # ── Auto-create parent folders if path contains / ──
    if "/" in filename:
        parts = filename.split("/")
        current_path = ""
        for folder in parts[:-1]:
            expected_path = f"{current_path}/{folder}" if current_path else folder

            # Skip creation if folder already exists
            if await _verify_folder_exists(expected_path, host, port):
                current_path = expected_path
                continue

            parent_api_path = _build_folder_api_path(current_path)
            result = await _create_single_folder(folder, parent_api_path, host, port)

            if not result["success"]:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Failed to create parent folder '{expected_path}': {result['reason']}. File NOT saved.",
                    },
                    indent=2, ensure_ascii=False,
                )

            current_path = expected_path

    # ── Check for duplicate filename ──
    filename = await _get_unique_filename(filename, host, port)

    # ── Save file ──
    base = _get_base_url(host, port)
    url = f"{base}/files/{filename}"

    headers = await _get_auth_headers(host, port)
    headers["Content-Type"] = "text/plain"

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.post(
                url,
                content=tql_content,
                headers=headers,
            )
            resp.raise_for_status()
        return json.dumps(
            {"status": "success", "message": f"File '{filename}' saved (validated)", "path": f"/{filename}"},
            indent=2,
            ensure_ascii=False,
        )
    except Exception as e:
        return f"Error saving file: {e}"


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 4] Dashboard Tools                                  │
# │  API: /web/api/files/*.dsh  |  Auth: JWT                    │
# └─────────────────────────────────────────────────────────────┘

@mcp.tool()
async def list_dashboards(
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """List all dashboards in Machbase Neo Web UI.

    Returns a list of existing dashboard (.dsh) files.
    """
    try:
        result = await _request("GET", "/files/?filter=*.dsh", host, port)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing dashboards: {e}"


@mcp.tool()
async def get_dashboard(
    filename: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Get a dashboard's full configuration.

    Args:
        filename: Dashboard filename (e.g., "my_dashboard.dsh")
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"
    try:
        result = await _request("GET", f"/files/{filename}", host, port)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error getting dashboard: {e}"


@mcp.tool()
async def create_dashboard(
    filename: str,
    title: str = "New dashboard",
    time_start: str = "now-1h",
    time_end: str = "now",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Create a new empty dashboard in Machbase Neo Web UI.

    **CRITICAL - DASHBOARD PATH RULES (MUST FOLLOW):**
    - Dashboard files MUST be saved inside the analysis folder, same as TQL files.
    - Folder naming: {TABLE_NAME} (e.g., "BEARING")
    - Example: "BEARING/bearing.dsh"
    - NEVER save dashboards to root. ALWAYS use the analysis folder path.

    Args:
        filename: Dashboard path - MUST include folder (e.g., "BEARING/analysis.dsh")
        title: Dashboard title displayed in the UI
        time_start: Time range start. Relative: "now-1h", "now-7d". Fixed: epoch ms as string (e.g., "1708300800000")
        time_end: Time range end. Relative: "now". Fixed: epoch ms as string (e.g., "1708387200000")
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    # ── Path enforcement: folder path required ──
    if "/" not in filename:
        return json.dumps(
            {
                "status": "error",
                "message": (
                    f"Dashboard '{filename}' has no folder path. "
                    "ALL dashboards MUST be saved inside a folder (e.g., 'TABLE/dashboard.dsh'). "
                    "Please retry with a folder path like '{TABLE}/" + filename + "'."
                ),
            },
            indent=2, ensure_ascii=False,
        )

    # ── Auto-create parent folders if needed ──
    parts = filename.split("/")
    current_path = ""
    for folder in parts[:-1]:
        expected_path = f"{current_path}/{folder}" if current_path else folder

        if await _verify_folder_exists(expected_path, host, port):
            current_path = expected_path
            continue

        parent_api_path = _build_folder_api_path(current_path)
        result = await _create_single_folder(folder, parent_api_path, host, port)

        if not result["success"]:
            return json.dumps(
                {
                    "status": "error",
                    "message": f"Failed to create folder '{expected_path}': {result['reason']}. Dashboard NOT created.",
                },
                indent=2, ensure_ascii=False,
            )

        current_path = expected_path

    # ── Check for duplicate filename ──
    filename = await _get_unique_filename(filename, host, port)

    # Extract path and name for share link support
    if "/" in filename:
        parts = filename.rsplit("/", 1)
        dsh_path = "/" + parts[0] + "/"
        dsh_name = parts[1]
    else:
        dsh_path = "/"
        dsh_name = filename

    dashboard = _make_empty_dashboard(title, time_start, time_end, dsh_path=dsh_path, dsh_name=dsh_name)

    try:
        result = await _request("POST", f"/files/{filename}", host, port, json_data=dashboard)
        return json.dumps(
            {"status": "success", "message": f"Dashboard '{title}' created as {filename}", "url": _get_dashboard_url(filename, host, port), "data": result},
            indent=2, ensure_ascii=False,
        )
    except Exception as e:
        return f"Error creating dashboard: {e}"


async def _fill_table_info(panel: dict, table: str, host, port):
    """Fill tableInfo in panel's blockList by querying column metadata."""
    if not table or not panel.get("blockList"):
        return
    try:
        col_resp = await _request(
            "GET", "/query", host, port,
            params={"q": f"SELECT * FROM {table} LIMIT 0"},
        )
        if col_resp.get("data", {}).get("columns"):
            cols = col_resp["data"]["columns"]
            types = col_resp["data"].get("types", [])
            type_map = {"string": 5, "varchar": 5, "datetime": 6, "double": 20, "float": 16, "int32": 8, "int64": 12}
            size_map = {"string": 32, "varchar": 32, "datetime": 8, "double": 8, "float": 4, "int32": 4, "int64": 8}
            table_info = []
            for i, c in enumerate(cols):
                t = types[i] if i < len(types) else "string"
                table_info.append([c, type_map.get(t, 5), size_map.get(t, 32), i])
            table_info.append(["_RID", 12, 8, 65534])
            for bl in panel["blockList"]:
                bl["tableInfo"] = table_info
    except Exception:
        pass


@mcp.tool()
async def create_dashboard_with_charts(
    filename: str,
    title: str = "Dashboard",
    time_start: str = "now-1h",
    time_end: str = "now",
    charts: str = "[]",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Create a dashboard with multiple chart panels in a single call.

    Much more efficient than calling create_dashboard + add_chart_to_dashboard × N.
    Charts are auto-laid-out left-to-right, wrapping to next row on the 36-col grid.

    Args:
        filename: Dashboard path (e.g., "BEARING/analysis.dsh") - MUST include folder
        title: Dashboard title
        time_start: Time range start ("now-1h", "now-7d", or epoch ms string)
        time_end: Time range end ("now", or epoch ms string)
        charts: JSON array string of chart definitions. Each chart object:
            - title (str): Chart title
            - type (str): "Line", "Bar", "Scatter", "Pie", "Gauge" (default: "Line")
            - table (str): Tag table name
            - tag (str): Tag name(s), comma-separated for multi-tag
            - column (str): Column name (default: "VALUE")
            - color (str): Hex color (default: auto)
            - tql_path (str): TQL file path (for TQL charts)
            - w (int): Width override (0 = auto)
            - h (int): Height override (0 = auto)
            - smooth (bool): Smooth curves (Line only)
            - area_style (bool): Fill area (Line only)
            - is_stack (bool): Stack mode (Line/Bar)

        Example charts:
        [
          {"title": "Temperature", "type": "Line", "table": "SENSOR", "tag": "temp-01"},
          {"title": "Distribution", "type": "Pie", "table": "SENSOR", "tag": "s1,s2,s3"},
          {"title": "Current", "type": "Gauge", "table": "SENSOR", "tag": "amp-01"}
        ]
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    # ── Path enforcement ──
    if "/" not in filename:
        return json.dumps(
            {"status": "error", "message": f"Dashboard '{filename}' needs a folder path (e.g., 'TABLE/{filename}')."},
            indent=2, ensure_ascii=False,
        )

    # ── Parse charts JSON ──
    try:
        chart_list = json.loads(charts)
        if not isinstance(chart_list, list):
            return json.dumps({"status": "error", "message": "charts must be a JSON array"}, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({"status": "error", "message": f"Invalid charts JSON: {e}"}, indent=2)

    # ── Auto-create parent folders ──
    parts = filename.split("/")
    current_path = ""
    for folder in parts[:-1]:
        expected_path = f"{current_path}/{folder}" if current_path else folder
        if await _verify_folder_exists(expected_path, host, port):
            current_path = expected_path
            continue
        parent_api_path = _build_folder_api_path(current_path)
        result = await _create_single_folder(folder, parent_api_path, host, port)
        if not result["success"]:
            return json.dumps(
                {"status": "error", "message": f"Failed to create folder '{expected_path}': {result['reason']}"},
                indent=2, ensure_ascii=False,
            )
        current_path = expected_path

    # ── Check for duplicate filename ──
    filename = await _get_unique_filename(filename, host, port)

    # ── Build dashboard with path/name for share links ──
    if "/" in filename:
        fn_parts = filename.rsplit("/", 1)
        dsh_path = "/" + fn_parts[0] + "/"
        dsh_name = fn_parts[1]
    else:
        dsh_path = "/"
        dsh_name = filename

    dashboard = _make_empty_dashboard(title, time_start, time_end, dsh_path=dsh_path, dsh_name=dsh_name)

    # ── Create panels with auto-layout ──
    panels = []
    for chart_def in chart_list:
        ct = chart_def.get("type", "Line")
        tql = chart_def.get("tql_path", "")
        cw = chart_def.get("w", 0)
        ch = chart_def.get("h", 0)

        effective_type = "Tql chart" if tql else ct
        needed_w = cw if cw > 0 else (CHART_W_LARGE if effective_type in _LARGE_CHART_TYPES else CHART_W_SMALL)

        ax, ay = _calculate_next_position(panels, needed_w)

        panel = _make_chart_panel(
            title=chart_def.get("title", "Chart"),
            chart_type=ct,
            table=chart_def.get("table", ""),
            tag=chart_def.get("tag", ""),
            column=chart_def.get("column", "VALUE"),
            color=chart_def.get("color", "#367FEB"),
            tql_path=tql,
            x=ax, y=ay, w=cw, h=ch,
            smooth=chart_def.get("smooth", False),
            area_style=chart_def.get("area_style", False),
            is_stack=chart_def.get("is_stack", False),
        )

        # Fill tableInfo
        tbl = chart_def.get("table", "")
        await _fill_table_info(panel, tbl, host, port)

        panels.append(panel)

    dashboard["dashboard"]["panels"] = panels

    # ── Save ──
    try:
        await _request("POST", f"/files/{filename}", host, port, json_data=dashboard)
        return json.dumps(
            {
                "status": "success",
                "message": f"Dashboard '{title}' created with {len(panels)} chart(s) as {filename}",
                "url": _get_dashboard_url(filename, host, port),
                "filename": filename,
                "panel_count": len(panels),
            },
            indent=2, ensure_ascii=False,
        )
    except Exception as e:
        return f"Error creating dashboard: {e}"


@mcp.tool()
async def add_chart_to_dashboard(
    filename: str,
    chart_title: str = "New chart",
    chart_type: str = "Line",
    table: str = "",
    tag: str = "",
    column: str = "VALUE",
    user_name: str = "sys",
    color: str = "#367FEB",
    tql_path: str = "",
    x: int = -1,
    y: int = -1,
    w: int = 0,
    h: int = 0,
    smooth: bool = False,
    area_style: bool = False,
    is_stack: bool = False,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Add a chart panel to an existing dashboard.

    **MODE SELECTION GUIDE (MUST FOLLOW):**
    - Table-based (PREFERRED - use by default): ALL chart types work without TQL.
      Line, Bar, Scatter, Pie, Gauge - ALL can be created with just table, tag, column.

    **IMPORTANT - tag supports COMMA-SEPARATED multiple tags:**
      Pie: tag="sensor-01,sensor-02,sensor-03" (ALWAYS use multiple for Pie)
      Gauge: tag="temp-01" (single value)
      Line: tag="vibration-01"

    - TQL-based (ONLY when Table-based is impossible): SQL JOIN, MAPVALUE, GROUP BY etc.

    Grid: 36 columns. Auto-width: Line/Bar/Scatter/Tql=17, Pie/Gauge/etc=7.

    Args:
        filename: Dashboard filename (e.g., "BEARING/analysis.dsh")
        chart_title: Title displayed on the chart
        chart_type: "Line", "Bar", "Scatter", "Pie", "Gauge", "Tql chart"
        table: Tag table name (e.g., "GOLD", "SENSOR_DATA")
        tag: Tag name(s). Single: "tag-001". Multiple: "tag-001,tag-002,tag-003"
        column: Column name for Y axis (e.g., "VALUE")
        user_name: Database user name (default: "SYS")
        color: Chart line/bar color (hex, e.g., "#367FEB")
        tql_path: Path to saved TQL file (e.g., "BEARING/c1_vibration.tql")
        x: Panel X position (-1 = auto-layout, 0+ = manual position)
        y: Panel Y position (-1 = auto-layout, 0+ = manual position)
        w: Panel width (0 = auto based on chart type)
        h: Panel height (0 = default 7)
        smooth: Smooth line curves (Line only)
        area_style: Fill area under line (Line only)
        is_stack: Stack multiple series (Line/Bar)
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    try:
        dashboard_data = await _request("GET", f"/files/{filename}", host, port)
    except Exception as e:
        return f"Error: Dashboard '{filename}' not found. Create it first with create_dashboard. ({e})"

    # ── Auto-layout: x<0 or y<0 means auto-position ──
    if x < 0 or y < 0:
        # Determine needed width for layout calculation
        effective_type = "Tql chart" if tql_path else chart_type
        needed_w = w if w > 0 else (CHART_W_LARGE if effective_type in _LARGE_CHART_TYPES else CHART_W_SMALL)

        existing_panels = dashboard_data.get("dashboard", {}).get("panels", [])
        x, y = _calculate_next_position(existing_panels, needed_w)

    panel = _make_chart_panel(
        title=chart_title, chart_type=chart_type, table=table,
        user_name=user_name, tag=tag, color=color, column=column,
        tql_path=tql_path, x=x, y=y, w=w, h=h,
        smooth=smooth, area_style=area_style, is_stack=is_stack,
    )

    await _fill_table_info(panel, table, host, port)

    if "dashboard" not in dashboard_data:
        dashboard_data["dashboard"] = {
            "panels": [], "title": "Dashboard",
            "timeRange": {"start": "now-1h", "end": "now", "refresh": "Off"},
            "variables": []
        }

    dashboard_data["dashboard"]["panels"].append(panel)

    result = await _request("POST", f"/files/{filename}", host, port, json_data=dashboard_data)

    panel_count = len(dashboard_data["dashboard"]["panels"])
    return json.dumps(
        {
            "status": "success",
            "message": f"Chart '{chart_title}' ({chart_type}) added to {filename}. Total panels: {panel_count}",
            "url": _get_dashboard_url(filename, host, port),
            "panel_id": panel["id"],
            "position": {"x": panel["x"], "y": panel["y"], "w": panel["w"], "h": panel["h"]},
        },
        indent=2, ensure_ascii=False,
    )


@mcp.tool()
async def remove_chart_from_dashboard(
    filename: str,
    panel_id: Optional[str] = None,
    panel_title: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Remove a chart panel from a dashboard.

    Identify the panel by either panel_id or panel_title.

    Args:
        filename: Dashboard filename
        panel_id: Panel UUID to remove
        panel_title: Panel title to remove (removes first match)
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    if not panel_id and not panel_title:
        return "Error: Provide either panel_id or panel_title"

    try:
        dashboard_data = await _request("GET", f"/files/{filename}", host, port)
    except Exception as e:
        return f"Error: Dashboard not found ({e})"

    panels = dashboard_data.get("dashboard", {}).get("panels", [])
    original_count = len(panels)

    if panel_id:
        panels = [p for p in panels if p.get("id") != panel_id]
    elif panel_title:
        found = False
        new_panels = []
        for p in panels:
            if p.get("title") == panel_title and not found:
                found = True
                continue
            new_panels.append(p)
        panels = new_panels

    dashboard_data["dashboard"]["panels"] = panels
    removed = original_count - len(panels)

    if removed == 0:
        return "No matching panel found to remove."

    await _request("POST", f"/files/{filename}", host, port, json_data=dashboard_data)

    return json.dumps(
        {"status": "success", "message": f"Removed {removed} panel(s). Remaining: {len(panels)}"},
        indent=2, ensure_ascii=False,
    )


@mcp.tool()
async def update_chart_in_dashboard(
    filename: str,
    panel_id: str = "",
    panel_title: str = "",
    new_title: str = "",
    new_chart_type: str = "",
    new_table: str = "",
    new_tag: str = "",
    new_column: str = "",
    new_color: str = "",
    x: int = -1,
    y: int = -1,
    w: int = -1,
    h: int = -1,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Update an existing chart panel in a dashboard.

    Find panel by panel_id or panel_title, then update only the provided fields.
    Fields left at default values are not changed.

    Args:
        filename: Dashboard filename (e.g., "BEARING/analysis.dsh")
        panel_id: Panel UUID to update (preferred)
        panel_title: Panel title to update (first match)
        new_title: New panel title
        new_chart_type: New chart type ("Line", "Bar", "Scatter", "Pie", "Gauge")
        new_table: New table name
        new_tag: New tag name(s) (comma-separated for multi-tag)
        new_column: New column name
        new_color: New color (hex)
        x: New X position (-1 = keep current)
        y: New Y position (-1 = keep current)
        w: New width (-1 = keep current)
        h: New height (-1 = keep current)
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    if not panel_id and not panel_title:
        return "Error: Provide either panel_id or panel_title to identify the panel."

    try:
        dashboard_data = await _request("GET", f"/files/{filename}", host, port)
    except Exception as e:
        return f"Error: Dashboard not found ({e})"

    panels = dashboard_data.get("dashboard", {}).get("panels", [])

    # Find target panel
    target = None
    for p in panels:
        if panel_id and p.get("id") == panel_id:
            target = p
            break
        if panel_title and p.get("title") == panel_title and target is None:
            target = p

    if not target:
        return json.dumps(
            {"status": "error", "message": f"No panel found matching id='{panel_id}' or title='{panel_title}'"},
            indent=2, ensure_ascii=False,
        )

    # Update only provided fields
    if new_title:
        target["title"] = new_title
        if target.get("commonOptions"):
            target["commonOptions"]["title"] = new_title

    if new_chart_type:
        target["type"] = new_chart_type
        chart_options = dict(_CHART_TYPE_DEFAULTS.get(new_chart_type, _CHART_TYPE_DEFAULTS["Line"]))
        target["chartInfo"] = chart_options
        target["chartOptions"] = dict(chart_options)

    if x >= 0:
        target["x"] = x
    if y >= 0:
        target["y"] = y
    if w > 0:
        target["w"] = w
    if h > 0:
        target["h"] = h

    # Rebuild blockList if table/tag/column changed
    rebuild_blocks = new_table or new_tag or new_column or new_color
    if rebuild_blocks:
        tbl = new_table or target.get("blockList", [{}])[0].get("table", "") if target.get("blockList") else new_table
        tg = new_tag or target.get("blockList", [{}])[0].get("tag", "") if target.get("blockList") else new_tag
        col = new_column or target.get("blockList", [{}])[0].get("value", "VALUE") if target.get("blockList") else new_column
        clr = new_color or target.get("blockList", [{}])[0].get("color", "#367FEB") if target.get("blockList") else new_color
        usr = target.get("blockList", [{}])[0].get("userName", "sys") if target.get("blockList") else "sys"

        if tbl and tg:
            chart_type_effective = new_chart_type or target.get("type", "Line")
            _SERIES_COLORS = [
                "#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de",
                "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc", "#FADE2A",
            ]
            if chart_type_effective == "Pie":
                agg = "count"
            elif chart_type_effective in ("Gauge", "Liquid fill"):
                agg = "last"
            else:
                agg = "value"

            tags = [t.strip() for t in tg.split(",") if t.strip()]
            blocks = []
            for i, t in enumerate(tags):
                c = clr if len(tags) == 1 else _SERIES_COLORS[i % len(_SERIES_COLORS)]
                blocks.append(_make_block(tbl, t, col, c, usr, aggregator=agg))

            # Fill tableInfo
            try:
                col_resp = await _request(
                    "GET", "/query", host, port,
                    params={"q": f"SELECT * FROM {tbl} LIMIT 0"},
                )
                if col_resp.get("data", {}).get("columns"):
                    cols = col_resp["data"]["columns"]
                    types = col_resp["data"].get("types", [])
                    type_map = {"string": 5, "varchar": 5, "datetime": 6, "double": 20, "float": 16, "int32": 8, "int64": 12}
                    size_map = {"string": 32, "varchar": 32, "datetime": 8, "double": 8, "float": 4, "int32": 4, "int64": 8}
                    table_info = []
                    for i, c_name in enumerate(cols):
                        t = types[i] if i < len(types) else "string"
                        table_info.append([c_name, type_map.get(t, 5), size_map.get(t, 32), i])
                    table_info.append(["_RID", 12, 8, 65534])
                    for bl in blocks:
                        bl["tableInfo"] = table_info
            except Exception:
                pass

            target["blockList"] = blocks

    # Save updated dashboard
    try:
        await _request("POST", f"/files/{filename}", host, port, json_data=dashboard_data)
        return json.dumps(
            {"status": "success", "message": f"Panel '{target['title']}' updated in {filename}", "panel_id": target["id"]},
            indent=2, ensure_ascii=False,
        )
    except Exception as e:
        return f"Error saving dashboard: {e}"


@mcp.tool()
async def delete_dashboard(
    filename: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Delete a dashboard file from Machbase Neo.

    Args:
        filename: Dashboard filename to delete
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    try:
        result = await _request("DELETE", f"/files/{filename}", host, port)
        return json.dumps(
            {"status": "success", "message": f"Dashboard '{filename}' deleted"},
            indent=2, ensure_ascii=False,
        )
    except Exception as e:
        return f"Error deleting dashboard: {e}"


@mcp.tool()
async def update_dashboard_time_range(
    filename: str,
    time_start: str = "now-1h",
    time_end: str = "now",
    refresh: str = "Off",
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Update the time range of a dashboard.

    Args:
        filename: Dashboard filename
        time_start: Start time. Relative: "now-1h", "now-7d". Fixed: epoch ms as string (e.g., "1708300800000")
        time_end: End time. Relative: "now". Fixed: epoch ms as string (e.g., "1708387200000")
        refresh: Auto-refresh interval ("Off", "3 seconds", "5 seconds", "10 seconds", "30 seconds", "1 minutes", "5 minutes")
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    try:
        dashboard_data = await _request("GET", f"/files/{filename}", host, port)
    except Exception as e:
        return f"Error: Dashboard not found ({e})"

    dashboard_data["dashboard"]["timeRange"] = {
        "start": _parse_time_value(time_start),
        "end": _parse_time_value(time_end),
        "refresh": refresh,
    }

    await _request("POST", f"/files/{filename}", host, port, json_data=dashboard_data)

    return json.dumps(
        {"status": "success", "message": f"Time range updated to {time_start} ~ {time_end} (refresh: {refresh})"},
        indent=2, ensure_ascii=False,
    )


@mcp.tool()
async def preview_dashboard(
    filename: str,
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> str:
    """Get a dashboard preview: summary info and direct Neo Web UI link.

    Returns the dashboard title, panel list, time range, and a clickable
    URL to open the dashboard in Machbase Neo Web UI.

    Args:
        filename: Dashboard filename (e.g., "BEARING/analysis.dsh")
    """
    if not filename.endswith(".dsh"):
        filename += ".dsh"

    try:
        dashboard_data = await _request("GET", f"/files/{filename}", host, port)
    except Exception as e:
        return json.dumps(
            {"status": "error", "message": f"Dashboard '{filename}' not found. ({e})"},
            indent=2, ensure_ascii=False,
        )

    dsh = dashboard_data.get("dashboard", {})
    title = dsh.get("title", dashboard_data.get("name", filename))
    time_range = dsh.get("timeRange", {})
    panels = dsh.get("panels", [])

    panel_summaries = []
    for p in panels:
        panel_summaries.append({
            "title": p.get("title", ""),
            "type": p.get("type", ""),
            "position": f"{p.get('x', 0)},{p.get('y', 0)}",
            "size": f"{p.get('w', 0)}x{p.get('h', 0)}",
        })

    url = _get_dashboard_url(filename, host, port)

    return json.dumps(
        {
            "status": "success",
            "url": url,
            "title": title,
            "panel_count": len(panels),
            "time_range": f"{time_range.get('start', 'now-1h')} ~ {time_range.get('end', 'now')}",
            "refresh": time_range.get("refresh", "Off"),
            "panels": panel_summaries,
        },
        indent=2, ensure_ascii=False,
    )


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 5] Document Tools                                   │
# │  Source: Local file system (neo/ folder)                     │
# └─────────────────────────────────────────────────────────────┘

@mcp.tool()
async def list_available_documents() -> str:
    """List all available documentation files."""
    global document_extractor

    try:
        if not document_extractor.file_index:
            return "No documentation files found."

        files_by_dir = defaultdict(list)

        for filename, full_path in document_extractor.file_index.items():
            if filename.endswith('.md'):
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
        result += "• `get_full_document_content('installation/installation.md')` - Installation guide\n"
        result += "• `get_full_document_content('operations/service-linux.md')` - Service management\n"
        result += "• `extract_code_blocks('tql/tql_guide.md', 'tql')` - TQL code examples\n"
        result += "• `get_document_sections('sql/sql_guide.md', 'SELECT')` - SQL sections\n\n"
        result += "**IMPORTANT - dbms/ folder policy**:\n"
        result += "The dbms/ folder contains low-level DBMS internals.\n"
        result += "Only search dbms/ folder when:\n"
        result += "  1. User explicitly asks about DBMS internals\n"
        result += "  2. Information is NOT found in other folders (installation/, operations/, sql/, tql/, api/)\n"
        result += "Always search non-dbms folders FIRST.\n"

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

    **CRITICAL - EXAMPLE CODE EXECUTION POLICY:**
    When providing TQL/SQL examples from documentation to users:
    - MUST execute ALL TQL examples with execute_tql_script() before providing to user
    - MUST execute ALL SQL examples with execute_sql_query() before providing to user
    - Verify every single example code block is executable and returns valid results
    - NEVER provide example code without execution validation
    - If any example fails execution, fix it or inform user that example needs updating
    - Document examples may be outdated - always validate before providing

    Args:
        file_identifier: relative path (e.g., "sql/rollup.md")
    """
    global document_extractor

    try:
        file_identifier = os.path.normpath(file_identifier)

        doc = document_extractor.get_full_document(file_identifier)

        if not doc:
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
            for section in doc.sections[:5]:
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

    **CRITICAL - EXAMPLE CODE EXECUTION POLICY:**
    When providing TQL/SQL examples from documentation to users:
    - MUST execute ALL TQL examples with execute_tql_script() before providing to user
    - MUST execute ALL SQL examples with execute_sql_query() before providing to user
    - Verify every single example code block is executable and returns valid results
    - NEVER provide example code without execution validation
    - If any example fails execution, fix it or inform user that example needs updating
    - Document examples may be outdated - always validate before providing

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

    **CRITICAL - EXAMPLE CODE EXECUTION POLICY:**
    When providing TQL/SQL examples from documentation to users:
    - MUST execute ALL TQL examples with execute_tql_script() before providing to user
    - MUST execute ALL SQL examples with execute_sql_query() before providing to user
    - Verify every single example code block is executable and returns valid results
    - NEVER provide example code without execution validation
    - If any example fails execution, fix it or inform user that example needs updating
    - Document examples may be outdated - always validate before providing

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


# ┌─────────────────────────────────────────────────────────────┐
# │  [Tools 6] Utility Tools                                    │
# └─────────────────────────────────────────────────────────────┘

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
    ✓ TQL execution and validation
    ✓ File management (TQL/SQL file saving)
    ✓ Dashboard creation and chart management
    ✓ User Manual
    ✓ Error handling and debugging tools

    ## Tool Categories (25 tools)
    - **Database Tools** (3): list_tables, list_table_tags, execute_sql_query
    - **TQL Tools** (2): execute_tql_script, validate_chart_tql
    - **File Management Tools** (4): create_folder, list_files, delete_file, save_tql_file
    - **Dashboard Tools** (10): list_dashboards, get_dashboard, create_dashboard, create_dashboard_with_charts, add_chart_to_dashboard, remove_chart_from_dashboard, update_chart_in_dashboard, delete_dashboard, update_dashboard_time_range, preview_dashboard
    - **Document Tools** (4): get_full_document_content, extract_code_blocks, get_document_sections, list_available_documents
    - **Utility Tools** (2): get_version, debug_mcp_status

    For detailed usage information, use `debug_mcp_status()` tool.
    """


@mcp.tool()
async def debug_mcp_status() -> str:
    """Check current status and performance of MCP server."""
    global document_extractor

    # Version information
    version_info = f"=== Machbase Neo MCP Server Status ===\n"
    version_info += f"Version: {VERSION}\n"
    version_info += f"Build Date: {BUILD_DATE}\n"
    version_info += f"Description: {DESCRIPTION}\n\n"

    # DB API connection status (/db/)
    db_status = ""
    try:
        machbase_url = get_machbase_url()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{machbase_url}/db/query?q=SELECT 1 FROM M$SYS_TABLES LIMIT 1&format=csv",
                timeout=5.0
            )
            if response.status_code == 200:
                db_status = f"[OK] DB API connection successful ({machbase_url}/db/)"
            else:
                db_status = f"[ERROR] DB API connection failed: HTTP {response.status_code}"
    except Exception as e:
        db_status = f"[ERROR] DB API connection error: {str(e)}"

    # Web API connection status (/web/api/)
    web_status = ""
    try:
        result = await _request("GET", "/check")
        web_status = f"[OK] Web API connection successful ({_get_base_url()})"
    except Exception as e:
        web_status = f"[ERROR] Web API connection error: {str(e)}"

    # Document extractor status
    doc_status = f"\n=== Document Content Access Status ===\n"
    doc_status += f"Documentation folder: {document_extractor.docs_folder}\n"
    doc_status += f"Folder exists: {os.path.exists(document_extractor.docs_folder)}\n"
    doc_status += f"Indexed files: {len(document_extractor.file_index)}\n"
    doc_status += f"Cached documents: {len(document_extractor.document_cache)}\n"

    doc_status += f"\n=== Available Tools (25) ===\n"
    doc_status += f"Database Tools (3):\n"
    doc_status += f"  • list_tables() - Get all database tables\n"
    doc_status += f"  • list_table_tags() - Get tags from specific table\n"
    doc_status += f"  • execute_sql_query() - Execute SQL queries\n\n"

    doc_status += f"TQL Tools (2):\n"
    doc_status += f"  • execute_tql_script() - Execute TQL via HTTP API\n"
    doc_status += f"  • validate_chart_tql() - Validate TQL chart scripts\n\n"

    doc_status += f"File Management Tools (4):\n"
    doc_status += f"  • create_folder() - Create folders in Neo file system\n"
    doc_status += f"  • list_files() - List files and folders\n"
    doc_status += f"  • delete_file() - Delete a file or empty folder\n"
    doc_status += f"  • save_tql_file() - Save TQL/SQL files with validation\n\n"

    doc_status += f"Dashboard Tools (10):\n"
    doc_status += f"  • list_dashboards() - List all dashboards\n"
    doc_status += f"  • get_dashboard() - Get dashboard configuration\n"
    doc_status += f"  • create_dashboard() - Create new dashboard\n"
    doc_status += f"  • create_dashboard_with_charts() - Create dashboard with charts\n"
    doc_status += f"  • add_chart_to_dashboard() - Add chart to dashboard\n"
    doc_status += f"  • remove_chart_from_dashboard() - Remove chart from dashboard\n"
    doc_status += f"  • update_chart_in_dashboard() - Update chart in dashboard\n"
    doc_status += f"  • delete_dashboard() - Delete a dashboard\n"
    doc_status += f"  • update_dashboard_time_range() - Update dashboard time range\n"
    doc_status += f"  • preview_dashboard() - Get dashboard preview and Neo UI link\n\n"

    doc_status += f"Document Tools (4):\n"
    doc_status += f"  • get_full_document_content() - Get complete document\n"
    doc_status += f"  • extract_code_blocks() - Extract code examples\n"
    doc_status += f"  • get_document_sections() - Get document sections\n"
    doc_status += f"  • list_available_documents() - List all files\n\n"

    doc_status += f"Utility Tools (2):\n"
    doc_status += f"  • get_version() - Show version information\n"
    doc_status += f"  • debug_mcp_status() - Check server status\n"

    return f"{version_info}{db_status}\n{web_status}\n{doc_status}"


# ═══════════════════════════════════════════════════════════════
# [Section 7] Main
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info(f"Starting Machbase Neo MCP server v{VERSION}")
    logger.info("Available tools (25):")
    logger.info("  Database (3): list_tables, list_table_tags, execute_sql_query")
    logger.info("  TQL (2): execute_tql_script, validate_chart_tql")
    logger.info("  File Mgmt (4): create_folder, list_files, delete_file, save_tql_file")
    logger.info("  Dashboard (10): list_dashboards, get_dashboard, create_dashboard, create_dashboard_with_charts, add_chart_to_dashboard, remove_chart_from_dashboard, update_chart_in_dashboard, delete_dashboard, update_dashboard_time_range, preview_dashboard")
    logger.info("  Documents (4): get_full_document_content, extract_code_blocks, get_document_sections, list_available_documents")
    logger.info("  Utility (2): get_version, debug_mcp_status")

    try:
        document_extractor._build_file_index()
        logger.info(f"Document index ready: {len(document_extractor.file_index)} files indexed")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")

    mcp.run()