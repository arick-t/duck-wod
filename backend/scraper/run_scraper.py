#!/usr/bin/env python3
"""
DUCK-WOD Scraper v2.1
- Clear logging
- No silent failures
- Explicit scraper mapping
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- Path setup ---
CURRENT_DIR = Path(__file__).parent
SCRAPER_DIR = CURRENT_DIR
BACKEND_DIR = CURRENT_DIR.parent
BASE_DIR = BACKEND_DIR.parent

sys.path.insert(0, str(BACKEND_DIR))

from scraper.sources import myleo, crossfit, linchpin

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


# --- Load sources ---
def load_sources():
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # fallback default
    return [
        {
            "id": "myleo",
            "name": "myleo CrossFit",
            "url": "https://myleo.de/en/wods/",
            "enabled": True,
        },
        {
            "id": "crossfit",
            "name": "CrossFit.com",
            "url": "https://www.crossfit.com/workout/",
            "enabled": True,
        },
        {
