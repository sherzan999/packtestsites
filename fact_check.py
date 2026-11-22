#!/usr/bin/env python3
"""Сверяет цифры и контакты в HTML с data/raw/*.json (роль fact-checker)."""
import json, pathlib, html, sys
root = pathlib.Path(__file__).resolve().parent.parent
bad = 0
for f in sorted((root / "data/raw").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    page = html.unescape((root / d["slug"] / "index.html").read_text(encoding="utf-8"))
    need = [d["rating"], str(d["rating_count"]), str(d["reviews_count"]), d["address"], d["phone"]] + [p for *_, p in d["prices"]]
    need += [f"{p}%" for _, p, _ in d["aspects"]]
    miss = [x for x in need if x not in page]
    print(("APPROVED " if not miss else "REJECTED ") + d["slug"], miss or "")
    bad += bool(miss)
sys.exit(1 if bad else 0)
