#!/usr/bin/env python3
"""
Sources Management API
Handles adding/removing/toggling sources
"""

import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


DATA_DIR = Path(__file__).parent.parent.parent / 'data'
SOURCES_FILE = DATA_DIR / 'sources.json'


def load_sources():
    """Load sources from file"""
    if SOURCES_FILE.exists():
        with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_sources(sources):
    """Save sources to file"""
    with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)


def validate_source_url(url):
    """
    Validate that a source URL can provide WODs for at least 14 days back
    Returns: (is_valid, error_message)
    """
    try:
        # Test fetching today
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if page has workout content
        text = soup.get_text()
        
        # Look for workout indicators
        indicators = ['workout', 'wod', 'metcon', 'amrap', 'emom', 'for time', 'rounds']
        has_workout = any(indicator in text.lower() for indicator in indicators)
        
        if not has_workout:
            return False, "URL does not appear to contain workout content"
        
        # Try to check if archive exists (basic check)
        # If URL has date format, try 14 days ago
        test_date = datetime.now() - timedelta(days=14)
        
        # Different date formats to try
        date_formats = [
            test_date.strftime('%Y-%m-%d'),  # 2026-01-17
            test_date.strftime('%y%m%d'),     # 260117
            test_date.strftime('%Y/%m/%d'),   # 2026/01/17
        ]
        
        has_archive = False
        for date_format in date_formats:
            test_url = f"{url.rstrip('/')}/{date_format}/"
            try:
                test_response = requests.get(test_url, timeout=5)
                if test_response.status_code == 200:
                    has_archive = True
                    break
            except:
                continue
        
        if not has_archive:
            return True, "Warning: Could not verify 14-day archive. Source added but may only have today's WOD."
        
        return True, None
        
    except requests.RequestException as e:
        return False, f"Cannot access URL: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def add_source(name, url):
    """
    Add a new source
    Returns: (success, message)
    """
    sources = load_sources()
    
    # Generate ID from name
    source_id = name.lower().replace(' ', '_').replace('-', '_')
    source_id = ''.join(c for c in source_id if c.isalnum() or c == '_')
    
    # Check if already exists
    if any(s['id'] == source_id for s in sources):
        return False, f"Source with ID '{source_id}' already exists"
    
    # Validate URL
    is_valid, error = validate_source_url(url)
    if not is_valid:
        return False, error
    
    # Add source
    new_source = {
        'id': source_id,
        'name': name,
        'url': url,
        'enabled': True,
        'added_at': datetime.now().isoformat()
    }
    
    sources.append(new_source)
    save_sources(sources)
    
    return True, error if error else "Source added successfully"


def remove_source(source_id):
    """
    Remove a source
    Returns: (success, message)
    """
    sources = load_sources()
    
    # Find and remove
    original_count = len(sources)
    sources = [s for s in sources if s['id'] != source_id]
    
    if len(sources) == original_count:
        return False, f"Source '{source_id}' not found"
    
    save_sources(sources)
    return True, "Source removed successfully"


def toggle_source(source_id, enabled):
    """
    Enable/disable a source
    Returns: (success, message)
    """
    sources = load_sources()
    
    found = False
    for source in sources:
        if source['id'] == source_id:
            source['enabled'] = enabled
            found = True
            break
    
    if not found:
        return False, f"Source '{source_id}' not found"
    
    save_sources(sources)
    status = "enabled" if enabled else "disabled"
    return True, f"Source {status} successfully"


def get_sources():
    """Get all sources"""
    return load_sources()


if __name__ == '__main__':
    # Test
    print("Testing source management...")
    
    # Test validation
    print("\n1. Testing URL validation:")
    valid, msg = validate_source_url("https://www.crossfit.com/")
    print(f"   CrossFit.com: {valid} - {msg}")
    
    # Test add
    print("\n2. Testing add source:")
    success, msg = add_source("Test Source", "https://example.com/wod")
    print(f"   Add: {success} - {msg}")
    
    # Test toggle
    print("\n3. Testing toggle:")
    success, msg = toggle_source("test_source", False)
    print(f"   Toggle: {success} - {msg}")
    
    # Test remove
    print("\n4. Testing remove:")
    success, msg = remove_source("test_source")
    print(f"   Remove: {success} - {msg}")
    
    print("\n✅ Done!")
