from __future__ import annotations

import json
import os
import re
import socket
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "EXPORTS" / "brain-overview"

SURFACES = [
    ("David", r"X:\\David", ROOT / "David"),
    ("GUI", r"X:\\GUI", ROOT / "GUI"),
    ("Conversions", r"X:\\Conversions", ROOT / "Conversions"),
    ("EXPORTS", r"X:\\EXPORTS", ROOT / "EXPORTS"),
    ("Backside", r"X:\\Backside", ROOT / "Backside"),
    ("Repo", r"D:\\GitHub\\theophysics-brain-map", ROOT),
]

CATEGORY_PATTERNS = {
    "workflows": re.compile(r"workflow|pipeline|intake", re.I),
    "stations": re.compile(r"station", re.I),
    "models": re.compile(r"model|ollama|mistral|whisper", re.I),
    "exports": re.compile(r"export|output", re.I),
    "prompt_banks": re.compile(r"prompt|brief", re.I),
    "services": re.compile(r"service|daemon|scheduler|task", re.I),
}

REF_PATTERNS = [re.compile(r"X:\\[^\s\)\]\"]+"), re.compile(r"D:\\[^\s\)\]\"]+")]

@dataclass
class Item:
    name: str
    relative_path: str
    kind: str
    category: str
    owner_hint: str
    last_modified_utc: str | None
    source_of_truth_path: str


def iso_utc(ts: float | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def owner_hint(path: Path) -> str:
    parts = {p.lower() for p in path.parts}
    if "david" in parts:
        return "David"
    if "backside" in parts:
        return "Backside"
    if "00_workflows" in parts:
        return "Workflow team"
    return "Unknown"


def detect_category(name: str) -> str:
    for cat, pat in CATEGORY_PATTERNS.items():
        if pat.search(name):
            return cat
    return "other"


def scan_surface(label: str, source_path: str, resolved: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "label": label,
        "source_of_truth_path": source_path,
        "resolved_path": str(resolved),
        "status": "unavailable",
        "last_modified_utc": None,
        "items": [],
    }
    if not resolved.exists():
        return result

    stat = resolved.stat()
    result["status"] = "ok"
    result["last_modified_utc"] = iso_utc(stat.st_mtime)

    items: list[dict[str, Any]] = []
    for child in sorted(resolved.iterdir(), key=lambda p: p.name.lower()):
        try:
            cstat = child.stat()
            kind = "dir" if child.is_dir() else "file"
            item = Item(
                name=child.name,
                relative_path=str(child.relative_to(ROOT)) if ROOT in child.parents or child == ROOT else child.name,
                kind=kind,
                category=detect_category(child.name),
                owner_hint=owner_hint(child),
                last_modified_utc=iso_utc(cstat.st_mtime),
                source_of_truth_path=f"{source_path}\\{child.name}" if source_path.endswith('\\') is False else f"{source_path}{child.name}",
            )
            items.append(asdict(item))
        except OSError:
            continue

    result["items"] = items
    return result


def find_warnings_and_connections(repo_root: Path) -> tuple[list[str], list[dict[str, str]]]:
    warnings: list[str] = []
    connections: list[dict[str, str]] = []

    for path in repo_root.rglob("README.md"):
        pass

    for path in repo_root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        refs: set[str] = set()
        for pat in REF_PATTERNS:
            refs.update(pat.findall(text))
        for ref in sorted(refs):
            connections.append({"from": str(path.relative_to(repo_root)), "to": ref})

    for path in repo_root.rglob("*"):
        if not path.is_dir() or ".git" in path.parts:
            continue
        readme = path / "README.md"
        config_json = path / "config.json"
        config_yaml = path / "config.yaml"
        if len(path.parts) - len(repo_root.parts) <= 2:
            if not readme.exists():
                warnings.append(f"Missing README: {path.relative_to(repo_root)}")
            if not (config_json.exists() or config_yaml.exists()):
                warnings.append(f"Missing config: {path.relative_to(repo_root)}")

    return warnings[:300], connections[:1000]


def postgres_snapshot() -> dict[str, Any]:
    host, port = "192.168.1.177", 2665
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        s.connect((host, port))
        return {"status": "reachable", "host": host, "port": port, "schema": "unavailable_without_credentials"}
    except OSError as exc:
        return {"status": "unavailable", "host": host, "port": port, "reason": str(exc)}
    finally:
        s.close()


def render_markdown(data: dict[str, Any]) -> str:
    lines = ["# Brain Overview Snapshot", "", f"Generated: {data['generated_at_utc']}", ""]
    lines.append("## Surfaces")
    for s in data["surfaces"]:
        lines.append(f"- **{s['label']}**: `{s['source_of_truth_path']}` → `{s['status']}`")
    lines.append("")
    lines.append("## Warnings")
    for w in data["warnings"][:50]:
        lines.append(f"- {w}")
    if not data["warnings"]:
        lines.append("- None")
    lines.append("")
    lines.append("## Postgres")
    lines.append(f"- Status: {data['postgres']['status']}")
    return "\n".join(lines) + "\n"


def render_html(data: dict[str, Any]) -> str:
    body = ["<h1>Brain Overview Snapshot</h1>", f"<p>Generated: {data['generated_at_utc']}</p>"]
    body.append("<h2>Surfaces</h2><ul>")
    for s in data["surfaces"]:
        body.append(f"<li><b>{s['label']}</b> ({s['status']})<br><code>{s['source_of_truth_path']}</code></li>")
    body.append("</ul><h2>Warnings</h2><ul>")
    for w in data["warnings"][:100]:
        body.append(f"<li>{w}</li>")
    body.append("</ul>")
    return "<!doctype html><html><body>" + "\n".join(body) + "</body></html>"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    surfaces = [scan_surface(label, src, resolved) for label, src, resolved in SURFACES]
    warnings, connections = find_warnings_and_connections(ROOT)

    snapshot = {
        "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "host": socket.gethostname(),
        "surfaces": surfaces,
        "warnings": warnings,
        "connections": connections,
        "postgres": postgres_snapshot(),
    }

    (OUTPUT_DIR / "brain-overview.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    (OUTPUT_DIR / "README.md").write_text(render_markdown(snapshot), encoding="utf-8")
    (OUTPUT_DIR / "index.html").write_text(render_html(snapshot), encoding="utf-8")

    print(f"Wrote: {OUTPUT_DIR / 'brain-overview.json'}")
    print(f"Wrote: {OUTPUT_DIR / 'README.md'}")
    print(f"Wrote: {OUTPUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
