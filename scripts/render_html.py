#!/usr/bin/env python3
"""Render a local HTML page to PNG with the installed Chromium binary."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="用 Chromium 將 HTML 渲染成 PNG")
    parser.add_argument("html")
    parser.add_argument("png")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=800)
    args = parser.parse_args()

    chromium = shutil.which("chromium") or shutil.which("chromium-browser")
    if not chromium:
        print("[FAIL] 找不到 Chromium；請安裝 Chromium 後再渲染", file=sys.stderr)
        return 1
    html = Path(args.html).resolve()
    output = Path(args.png).resolve()
    if not html.is_file():
        print(f"[FAIL] 找不到 HTML：{html}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    url = html.as_uri()
    command = [
        chromium, "--headless", "--no-sandbox", "--disable-gpu",
        f"--window-size={args.width},{args.height}",
        "--hide-scrollbars", "--virtual-time-budget=1000",
        f"--screenshot={output}", url,
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as exc:
        print(f"[FAIL] Chromium 渲染失敗：{exc.stderr[-1000:]}", file=sys.stderr)
        return 1
    if not output.is_file() or output.stat().st_size == 0:
        print("[FAIL] Chromium 沒有產生有效 PNG", file=sys.stderr)
        return 1
    print(f"[OK] 已渲染 PNG：{output} ({output.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
