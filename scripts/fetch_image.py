#!/usr/bin/env python3
"""Download one image URL to a local file for DOCX embedding."""
from __future__ import annotations

import argparse
import mimetypes
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/bmp", "image/tiff"}


def fetch(url: str, output: Path) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("只允許使用 http 或 https 圖片 URL")

    request = Request(url, headers={"User-Agent": "nstc-undergrad-grant-skill/1.0"})
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_type().lower()
        data = response.read()

    if content_type not in ALLOWED_TYPES:
        guessed, _ = mimetypes.guess_type(url)
        if guessed not in ALLOWED_TYPES:
            raise ValueError(f"URL 回傳的不是支援圖片格式：{content_type}")
    if not data:
        raise ValueError("下載到空的圖片檔")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    print(f"[OK] 已下載圖片：{output} ({len(data):,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description="下載圖片供 DOCX 嵌入")
    parser.add_argument("url")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        fetch(args.url, Path(args.output))
    except Exception as exc:
        print(f"[FAIL] 圖片下載失敗：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
