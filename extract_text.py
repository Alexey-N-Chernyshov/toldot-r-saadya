#!/usr/bin/env python3
"""Re-extract per-page Hebrew text from the PDF into translations/he.json.

Usage:
    python3 extract_text.py

Requires poppler (pdftotext) to be installed:
    brew install poppler
"""
import subprocess
import json
import os

PDF = os.path.join(os.path.dirname(__file__),
                   "original", "Rabbi Saadya Liberow - 4 Adar I, 5768.pdf")
OUT_HE = os.path.join(os.path.dirname(__file__), "translations", "he.json")
OUT_RU = os.path.join(os.path.dirname(__file__), "translations", "ru.json")

TOTAL = 117

def main():
    os.makedirs(os.path.dirname(OUT_HE), exist_ok=True)

    # Preserve existing Russian translations if present
    ru_existing = {}
    if os.path.exists(OUT_RU):
        with open(OUT_RU, encoding="utf-8") as f:
            ru_existing = json.load(f)

    he_data = {}
    ru_data = {}

    for page in range(1, TOTAL + 1):
        result = subprocess.run(
            ["pdftotext", "-layout", "-f", str(page), "-l", str(page), PDF, "-"],
            capture_output=True, text=True
        )
        he_data[str(page)] = result.stdout.strip()
        ru_data[str(page)] = ru_existing.get(str(page), "")
        print(f"  Page {page:3d}: {len(he_data[str(page)])} chars")

    with open(OUT_HE, "w", encoding="utf-8") as f:
        json.dump(he_data, f, ensure_ascii=False, indent=2)

    with open(OUT_RU, "w", encoding="utf-8") as f:
        json.dump(ru_data, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {OUT_HE}")
    print(f"Wrote {OUT_RU}  (existing translations preserved)")

if __name__ == "__main__":
    main()
