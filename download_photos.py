#!/usr/bin/env python3
"""Скачивает главное фото карточки в assets/photos/<slug>/hero.jpg (запускать локально, нужен интернет).
После этого `python3 build.py` подключит локальные файлы вместо ссылок на Яндекс."""
import json, pathlib, sys, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from build import PHOTOS, ROOT
for slug, url in PHOTOS.items():
    out = ROOT / "assets" / "photos" / slug
    out.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        (out / "hero.jpg").write_bytes(urllib.request.urlopen(req, timeout=30).read())
        status = "ok"
    except Exception as ex:
        status = f"error: {ex}"
    (out / "manifest.json").write_text(json.dumps({"file": "hero.jpg", "source": url, "status": status,
        "note": "Главное фото карточки. Фильтр «От владельца» не применялся, проверьте вручную."}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(slug, status)
