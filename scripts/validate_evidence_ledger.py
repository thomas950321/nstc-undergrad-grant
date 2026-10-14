#!/usr/bin/env python3
"""Validate the portable NSTC evidence-ledger contract.

This checks structure and provenance fields only. It does not prove that a
source exists or that a claim is scientifically correct; those still require
human/source verification.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

STATUSES = {"verified", "needs-check", "rejected"}
USED_IN = {"motivation", "gap", "method", "budget", "figure", "review"}
REQUIRED = ("id", "claim", "source", "locator", "evidence", "status", "used_in")
PLACEHOLDERS = ("在此填入", "TODO", "待填")

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an NSTC evidence ledger")
    parser.add_argument("ledger", type=Path)
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="僅供範本 CI 使用；實際台帳不要開啟",
    )
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] 無法讀取 JSON：{exc}")
        return 1
    errors: list[str] = []
    if data.get("schema_version") != "nstc-evidence-ledger/1.0":
        errors.append("schema_version 必須是 nstc-evidence-ledger/1.0")
    if not isinstance(data.get("entries"), list) or not data["entries"]:
        errors.append("entries 必須是非空陣列")
        entries = []
    else:
        entries = data["entries"]
    ids: set[str] = set()
    for i, entry in enumerate(entries, 1):
        prefix = f"entries[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} 必須是物件")
            continue
        missing = [key for key in REQUIRED if not entry.get(key)]
        if missing:
            errors.append(f"{prefix} 缺少欄位：{', '.join(missing)}")
        entry_id = entry.get("id")
        if entry_id in ids:
            errors.append(f"{prefix} 重複 id：{entry_id}")
        if isinstance(entry_id, str):
            ids.add(entry_id)
        status = entry.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}.status 必須是：{' | '.join(sorted(STATUSES))}")
        used_in = entry.get("used_in")
        if not isinstance(used_in, list) or not used_in or any(x not in USED_IN for x in used_in):
            errors.append(f"{prefix}.used_in 必須包含有效用途：{' | '.join(sorted(USED_IN))}")
        for key in ("claim", "source", "locator", "evidence"):
            value = entry.get(key)
            if (not args.allow_placeholders and isinstance(value, str)
                    and any(token in value for token in PLACEHOLDERS)):
                errors.append(f"{prefix}.{key} 仍含範本佔位文字")
        if status == "verified" and not entry.get("checked_at"):
            errors.append(f"{prefix} 為 verified 時必須提供 checked_at")
        if status == "verified" and isinstance(entry.get("locator"), str) and entry["locator"].strip().lower() in {"n/a", "無", "搜尋結果"}:
            errors.append(f"{prefix}.locator 不可用模糊描述代替可追溯位置")
    if errors:
        print("[FAIL] evidence ledger validation")
        for error in errors:
            print(f"- {error}")
        return 1
    counts = {status: sum(e.get("status") == status for e in entries) for status in sorted(STATUSES)}
    print("[OK] evidence ledger structure passed")
    print(f"[OK] entries={len(entries)} | " + " | ".join(f"{k}={v}" for k, v in counts.items()))
    print("[NOTE] 結構通過不等於來源已被外部查證；請保留每筆核對紀錄。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
