#!/usr/bin/env python3
"""Extract Hebrew text from each PDF page and write to translations/he/N.html."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PDF = ROOT / "original" / "Rabbi Saadya Liberow - 4 Adar I, 5768.pdf"
OUT_DIR = ROOT / "translations" / "he"
TOTAL = 117

# Unicode bidi control characters inserted by pdftotext
BIDI_CONTROLS = re.compile(r"[‎‏‪-‮⁦-⁩]")


def extract_page_text(n: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-f", str(n), "-l", str(n), str(PDF), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def text_to_html(raw: str) -> str:
    text = BIDI_CONTROLS.sub("", raw)
    blocks = [b.strip() for b in re.split(r"\n{2,}", text) if b.strip()]
    paragraphs = "\n".join(f"<p>{b}</p>" for b in blocks)
    return f'<div dir="rtl">\n{paragraphs}\n</div>\n'


def main():
    parser = argparse.ArgumentParser(description="Extract Hebrew text from PDF pages.")
    parser.add_argument("--start", type=int, default=1, metavar="N")
    parser.add_argument("--end", type=int, default=TOTAL, metavar="N")
    parser.add_argument("--force", action="store_true", help="Re-process existing files")
    args = parser.parse_args()

    if not PDF.exists():
        sys.exit(f"PDF not found: {PDF}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for n in range(args.start, args.end + 1):
        out = OUT_DIR / f"{n}.html"
        if out.exists() and not args.force:
            print(f"page {n:3d}: skip (exists)")
            continue
        try:
            raw = extract_page_text(n)
            html = text_to_html(raw)
            out.write_text(html, encoding="utf-8")
            print(f"page {n:3d}: ok")
        except subprocess.CalledProcessError as e:
            print(f"page {n:3d}: error — {e.stderr.strip()}", file=sys.stderr)


if __name__ == "__main__":
    main()
