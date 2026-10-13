#!/usr/bin/env python3
"""Validate the repository as a portable Agent Skill.

This checks deterministic packaging concerns only; it does not judge proposal quality
or claim that a regulation is current.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not SKILL.is_file():
        print("[FAIL] SKILL.md 不存在")
        return 1

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md 必須以 YAML frontmatter 開始", errors)
    frontmatter = re.search(r"\A---\n(.*?)\n---\n", text, re.S)
    if not frontmatter:
        fail("找不到完整 YAML frontmatter", errors)
    else:
        metadata = frontmatter.group(1)
        name = re.search(r"^name:\s*([^\n]+)$", metadata, re.M)
        description = re.search(r"^description:\s*(.+)$", metadata, re.M)
        if not name:
            fail("frontmatter 缺少 name", errors)
        else:
            value = name.group(1).strip()
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
                fail(f"name 不符合 lowercase-hyphen 格式：{value}", errors)
            if len(value) > 64:
                fail("name 不得超過 64 字元", errors)
        if not description:
            fail("frontmatter 缺少 description", errors)
        elif len(description.group(1).strip()) > 1024:
            fail("description 不得超過 1024 字元", errors)

    body = text[frontmatter.end():] if frontmatter else text
    if len(body.splitlines()) >= 500:
        fail("SKILL.md body 應少於 500 行", errors)
    if "TODO" in text:
        fail("仍包含 TODO 佔位內容", errors)

    # Every relative path mentioned in backticks should resolve when it looks like a file.
    candidates = re.findall(r"`([^`\n]+)`", text)
    for candidate in candidates:
        candidate = candidate.strip()
        if candidate.startswith(("http://", "https://", "python ", "<", "proposal.md", "output.docx")):
            continue
        if ("/" in candidate or candidate.endswith((".md", ".py", ".json"))) and " " not in candidate:
            path = ROOT / candidate
            try:
                exists = path.exists()
            except OSError:
                exists = False
            if not exists:
                fail(f"SKILL.md 指向不存在的資源：{candidate}", errors)

    # Detect common claims that should be sourced or framed as current-year checks.
    if "當年度" not in text or "官方" not in text or "覆核" not in text:
        fail("缺少當年度官方公告優先的規則覆核指示", errors)
    if "不要" not in text or "未驗證" not in text:
        fail("缺少未驗證資料的停止／標記策略", errors)

    if errors:
        print("[FAIL] skill validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[OK] skill validation passed")
    print(f"[OK] SKILL.md: {len(text.splitlines())} lines")
    print("[OK] referenced resources exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
