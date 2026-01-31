#!/usr/bin/env python3
"""
DUCK-WOD Scraper Runner v2.2
- Safe merge (never deletes existing data)
- Supports generic scraper for new sources
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- Path setup ---
CURRENT_DIR = Path(__file__).parent
BACKEND_DIR = CURRENT_DIR.parent
BASE_DIR = BACKEND_DIR.parent

sys.path.insert(0, str(BACKEND_DIR))

from scraper.sources import myleo, crossfit, linchpin
from scraper.sources import generic  # ✅ generic scraper

# --- Paths ---
DATA_DIR = BASE_DIR / "data"
WODS_FILE = DATA_DIR / "wods.json"
SOURCES_FILE = DATA_DIR / "sources.json"

DATA_DIR.mkdir(exist_ok=True)

# --- Scraper registry ---
SCRAPER_MODULES = {
    "myleo": myleo,
    "crossfit": crossfit,
    "linchpin": linchpin,
}

# --- Helpers ---
def load_json(path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Main ---
def main():
    print("🦆 DUCK-WOD Fetch Started")

    sources = load_json(SOURCES_FILE, [])
    existing_data = load_json(WODS_FILE, {
        "last_updated": None,
        "sources": []
    })

    existing_sources_map = {
        s["id"]: s for s in existing_data.get("sources", [])
    }

    updated_sources = []

    today = datetime.now()

    for source in sources:
        if not source.get("enabled", True):
            continue

        source_id = source["id"]
        source_name = source["name"]
        source_url = source["url"]

        print(f"\n🔍 Processing source: {source_name}")

        scraper = SCRAPER_MODULES.get(source_id)
        wods = []

        for days_back in range(0, 14):
            date = today - timedelta(days=days_back)

            try:
                if scraper:
                    result = scraper.fetch_wod(date)
                else:
                    result = generic.fetch_wod(date, source_url)

                if result:
                    wods.append(result)

            except Exception as e:
                print(f"  ❌ Error: {e}")

        if not wods:
            print("  ⚠️ No WODs fetched — keeping existing data if any")
            if source_id in existing_sources_map:
                updated_sources.append(existing_sources_map[source_id])
            continue

        updated_sources.append({
            "id": source_id,
            "name": source_name,
            "url": source_url,
            "wods": sorted(wods, key=lambda x: x["date"], reverse=True)
        })

        print(f"  ✅ {len(wods)} WODs saved")

    if not updated_sources:
        print("\n❌ No sources updated — aborting save")
        return

    output = {
        "last_updated": datetime.now().isoformat(),
        "sources": updated_sources
    }

    save_json(WODS_FILE, output)
    print("\n🎉 Fetch completed successfully")


if __name__ == "__main__":
    main()
