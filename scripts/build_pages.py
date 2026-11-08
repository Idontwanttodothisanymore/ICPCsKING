#!/usr/bin/env python3
"""把笔记目录构建成 Docsify 静态站点（_site），供 GitHub Pages 部署。"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
WEB = ROOT / "web"

SKIP_DIRS = {".git", ".github", "_site", "web", "scripts", "node_modules"}
HOME_SOURCE = "00 首页.md"


def collect_notes():
    """按路径排序收集所有笔记（跳过 README 与构建产物）。"""
    notes = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        if p.name == "README.md":
            continue
        notes.append(rel)
    return notes


def display_folder(name):
    """去掉排序用的 `01 ` 前缀，只用于侧栏显示。"""
    return re.sub(r"^\d+\s+", "", name) or name


def build_tree(notes):
    tree = {}
    for rel in notes:
        node = tree
        for part in rel.parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault("__files__", []).append(rel)
    return tree


def render_sidebar(node, depth, lines):
    pad = "  " * depth
    for folder in sorted(k for k in node if k != "__files__"):
        lines.append("%s- %s" % (pad, display_folder(folder)))
        render_sidebar(node[folder], depth + 1, lines)
    for rel in sorted(node.get("__files__", []), key=lambda r: r.name):
        lines.append("%s- [%s](%s)" % (pad, rel.stem, slug_of(rel)))


def slug_of(rel):
    return "docs/%s" % rel_id[rel]


rel_id = {}


def render():
    files = collect_notes()
    for i, rel in enumerate(files, 1):
        rel_id[rel] = "n%03d.md" % i

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("docs/*.md"):
        old.unlink()

    for rel in files:
        target = OUT / "docs" / rel_id[rel]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, target)

    # 侧栏
    lines = ["- [首页](home.md)", ""]
    render_sidebar(build_tree([r for r in files if str(r) != HOME_SOURCE]), 0, lines)
    (OUT / "_sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 首页
    shutil.copyfile(ROOT / HOME_SOURCE, OUT / "home.md")

    # 双链映射：既能用文件名，也能用完整相对路径
    mapping = {"home": "home.md", "首页": "home.md"}
    for rel in files:
        dest = slug_of(rel)
        mapping[rel.stem] = dest
        mapping[str(rel.with_suffix(""))] = dest
        mapping[str(rel)] = dest
    body = "window.NOTES_MAP = %s;\n" % json.dumps(
        mapping, ensure_ascii=False, indent=2, sort_keys=True
    )
    (OUT / "notes-map.js").write_text(body, encoding="utf-8")

    shutil.copyfile(WEB / "index.html", OUT / "index.html")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    print("构建完成：%d 篇笔记 -> %s" % (len(files), OUT))


if __name__ == "__main__":
    render()
