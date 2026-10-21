"""claude_desktop_config.json에 machbase MCP 서버 등록 — 다른 서버·설정은 유지

usage: python update_claude_config.py <config.json> <python 경로> <Machbase.py 경로>
"""
import json
import shutil
import sys
from pathlib import Path

TOKEN_PLACEHOLDER = "YOUR_NEO_API_TOKEN"


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    config_path = Path(sys.argv[1])
    python_path, script_path = sys.argv[2], sys.argv[3]

    config = {}
    if config_path.exists():
        text = config_path.read_text(encoding="utf-8-sig")
        if text.strip():
            try:
                config = json.loads(text)
            except ValueError as e:
                print(f"Error: {config_path} is not valid JSON ({e}). Fix or remove it and run again.")
                return 1
        shutil.copyfile(config_path, config_path.with_name(config_path.name + ".bak"))

    servers = config.setdefault("mcpServers", {})
    previous = servers.get("machbase") if isinstance(servers.get("machbase"), dict) else {}
    env = dict(previous.get("env") or {})
    # 계정 로그인 방식 설정 제거 · 기존 접속 정보와 토큰은 유지
    env.pop("MACHBASE_USER", None)
    env.pop("MACHBASE_PASSWORD", None)
    env.setdefault("MACHBASE_HOST", "localhost")
    env.setdefault("MACHBASE_PORT", "5654")
    env.setdefault("MACHBASE_TOKEN", TOKEN_PLACEHOLDER)
    servers["machbase"] = {"command": python_path, "args": [script_path], "env": env}

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Updated: {config_path}")
    if env["MACHBASE_TOKEN"] == TOKEN_PLACEHOLDER:
        print(f'Next: replace "{TOKEN_PLACEHOLDER}" with your Machbase Neo API token in the file above, then restart Claude Desktop.')
    else:
        print("Existing MACHBASE_TOKEN kept.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
