#!/usr/bin/env python3
"""
DUCK-WOD Scraper Runner
Main script to fetch WODs from all active sources
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scraper.sources import myleo, crossfit, linchpin


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
WODS_FILE = DATA_DIR / 'wods.json'
SOURCES_FILE = DATA_DIR / 'sources.json'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


def load_sources():
    """Load sources configuration"""
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Default sources
    return {
        "sources": [
            {
                "id": "myleo",
                "name": "myleo CrossFit",
                "base_url": "https://myleo.de/en/wods/",
                "has_archive": True,
                "active": True
            },
            {
                "id": "crossfit",
                "name": "CrossFit.com",
                "base_url": "https://www.crossfit.com/",
                "has_archive": True,
                "active": True
            },
            {
                "id": "linchpin",
                "name": "CrossFit Linchpin",
                "base_url": "https://crossfitlinchpin.com/pages/workout-of-the-day",
                "has_archive": False,
                "active": True
            }
        ]
    }


def load_existing_wods():
    """Load existing WODs from file"""
    if WODS_FILE.exists():
        try:
            with open(WODS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('wods', {})
        except Exception as e:
            print(f"⚠️  Error loading existing WODs: {e}")
            return {}
    return {}


def save_wods(wods_data):
    """Save WODs to file"""
    output = {
        'last_updated': datetime.now().isoformat(),
        'wods': wods_data
    }
    
    with open(WODS_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved to {WODS_FILE}")


def clean_old_wods(wods_data, days_to_keep=14):
    """Remove WODs older than specified days"""
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    
    cleaned = {}
    removed_count = 0
    
    for date_str, wods in wods_data.items():
        if date_str >= cutoff_str:
            cleaned[date_str] = wods
        else:
            removed_count += len(wods)
    
    if removed_count > 0:
        print(f"🧹 Cleaned {removed_count} old WODs (older than {days_to_keep} days)")
    
    return cleaned


def fetch_wods_for_date(date, sources_config):
    """Fetch WODs from all active sources for a specific date"""
    date_str = date.strftime('%Y-%m-%d')
    wods = []
    
    source_modules = {
        'myleo': myleo,
        'crossfit': crossfit,
        'linchpin': linchpin
    }
    
    for source in sources_config['sources']:
        if not source['active']:
            continue
        
        source_id = source['id']
        if source_id not in source_modules:
            print(f"  ⚠️  Unknown source: {source_id}")
            continue
        
        module = source_modules[source_id]
        wod = module.fetch_wod(date)
        
        if wod:
            # Generate unique ID
            wod['id'] = f"{source_id}_{date_str}"
            wods.append(wod)
    
    return wods


def run_scraper(days_back=14):
    """
    Main scraper function
    
    Args:
        days_back: Number of days to fetch (default 14)
    """
    print("🦆 DUCK-WOD Scraper Starting...")
    print(f"📅 Fetching WODs for the past {days_back} days")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load configuration
    sources_config = load_sources()
    print(f"📋 Loaded {len(sources_config['sources'])} sources")
    active_sources = [s for s in sources_config['sources'] if s['active']]
    print(f"✅ {len(active_sources)} sources are active")
    print()
    
    # Load existing WODs
    existing_wods = load_existing_wods()
    print(f"📂 Loaded {sum(len(v) for v in existing_wods.values())} existing WODs")
    print()
    
    # Fetch new WODs
    new_count = 0
    updated_count = 0
    
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        print(f"📅 Processing {date_str}...")
        
        # Fetch WODs for this date
        new_wods = fetch_wods_for_date(date, sources_config)
        
        if new_wods:
            # Merge with existing WODs for this date
            if date_str not in existing_wods:
                existing_wods[date_str] = []
            
            # Track existing IDs
            existing_ids = {wod['id'] for wod in existing_wods[date_str]}
            
            # Add new WODs (don't overwrite existing)
            for wod in new_wods:
                if wod['id'] not in existing_ids:
                    existing_wods[date_str].append(wod)
                    new_count += 1
                    print(f"  ✨ New WOD: {wod['source']}")
                else:
                    print(f"  ⏭️  Already exists: {wod['source']}")
        
        print()
    
    # Clean old WODs
    existing_wods = clean_old_wods(existing_wods, days_to_keep=14)
    
    # Save results
    save_wods(existing_wods)
    
    # Summary
    print()
    print("=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"✨ New WODs added: {new_count}")
    print(f"📝 Total WODs in database: {sum(len(v) for v in existing_wods.values())}")
    print(f"📅 Date range: {min(existing_wods.keys())} to {max(existing_wods.keys())}")
    print(f"🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


if __name__ == '__main__':
    run_scraper()
