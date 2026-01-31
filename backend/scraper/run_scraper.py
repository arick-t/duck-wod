#!/usr/bin/env python3
"""DUCK-WOD Scraper V2.0"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scraper.sources import myleo, crossfit, linchpin

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
WODS_FILE = DATA_DIR / 'wods.json'
SOURCES_FILE = DATA_DIR / 'sources.json'
DATA_DIR.mkdir(exist_ok=True)


def load_sources():
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, 'r') as f:
            return json.load(f)
    return [
        {"id": "myleo", "name": "myleo CrossFit", "url": "https://myleo.de/en/wods/", "enabled": True},
        {"id": "crossfit", "name": "CrossFit.com", "url": "https://www.crossfit.com/", "enabled": True},
        {"id": "linchpin", "name": "CrossFit Linchpin", "url": "https://crossfitlinchpin.com/", "enabled": True}
    ]


def save_wods(data):
    data['last_updated'] = datetime.now().isoformat()
    with open(WODS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def run_scraper(days_back=14):
    print("🦆 DUCK-WOD Scraper V2.0\n")
    
    sources_config = load_sources()
    enabled = [s for s in sources_config if s.get('enabled', True)]
    
    modules = {'myleo': myleo, 'crossfit': crossfit, 'linchpin': linchpin}
    
    new_sources_data = []
    
    for source in enabled:
        sid = source['id']
        if sid not in modules:
            continue
        
        print(f"📦 {source['name']}...")
        module = modules[sid]
        
        wods = []
        for i in range(days_back):
            date = datetime.now() - timedelta(days=i)
            wod = module.fetch_wod(date)
            if wod:
                wods.append(wod)
        
        if wods:
            new_sources_data.append({
                'id': sid,
                'name': source['name'],
                'url': source['url'],
                'wods': wods
            })
            print(f"  ✅ {len(wods)} WODs\n")
    
    save_wods({'sources': new_sources_data})
    print(f"💾 Done! Total: {sum(len(s['wods']) for s in new_sources_data)} WODs")


if __name__ == '__main__':
    run_scraper()
