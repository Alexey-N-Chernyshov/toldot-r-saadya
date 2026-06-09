# Scripts

## extract_original.py

Extracts Hebrew text from the original PDF and writes one HTML file per page to `translations/he/`.

**Requirement:** `pdftotext` from Poppler (`brew install poppler`).

```bash
# Single page (test)
python scripts/extract_original.py --start 11 --end 11

# Full run
python scripts/extract_original.py

# Re-process already existing files
python scripts/extract_original.py --force
```

The script is resumable — it skips pages whose output file already exists.
