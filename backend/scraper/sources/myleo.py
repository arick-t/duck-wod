"""
myleo CrossFit Scraper
Fetches WODs from myleo.de/en/wods/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def fetch_wod(date):
    """
    Fetch a single WOD from myleo for a specific date
    
    Args:
        date: datetime object
        
    Returns:
        dict with WOD data or None if not found
    """
    date_str = date.strftime('%Y-%m-%d')
    url = f'https://myleo.de/en/wods/{date_str}/'
    
    try:
        print(f"  Fetching myleo for {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main WOD section
        wod_content = None
        
        # Try to find the article content
        article = soup.find('article', class_='post')
        if article:
            # Get all text content, preserving structure
            content_div = article.find('div', class_='entry-content')
            if content_div:
                # Extract text with proper formatting
                wod_content = content_div.get_text(separator='\n', strip=True)
        
        # Alternative: look for specific WOD sections
        if not wod_content:
            wod_section = soup.find('div', class_='wod-single')
            if wod_section:
                wod_content = wod_section.get_text(separator='\n', strip=True)
        
        # Last resort: find any content that looks like a WOD
        if not wod_content:
            # Look for content between headers
            content_area = soup.find('main') or soup.find('article')
            if content_area:
                wod_content = content_area.get_text(separator='\n', strip=True)
        
        if wod_content:
            # Clean up the content
            lines = [line.strip() for line in wod_content.split('\n') if line.strip()]
            # Filter out navigation/footer elements
            filtered_lines = [
                line for line in lines 
                if not any(skip in line.lower() for skip in [
                    'cookie', 'privacy', 'login', 'weekly overview',
                    'post your score', 'navigation', 'menu'
                ])
            ]
            wod_content = '\n'.join(filtered_lines[:100])  # Limit to first 100 lines
            
            if len(wod_content) > 50:  # Must have substantial content
                return {
                    'date': date_str,
                    'source': 'myleo CrossFit',
                    'full_text': wod_content,
                    'url': url,
                    'fetched_at': datetime.now().isoformat()
                }
        
        print(f"  ⚠️  No WOD content found for {date_str}")
        return None
        
    except requests.RequestException as e:
        print(f"  ❌ Error fetching myleo for {date_str}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error for {date_str}: {e}")
        return None


def test():
    """Test the scraper with today's date"""
    print("Testing myleo scraper...")
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ Success! Fetched {len(result['full_text'])} characters")
        print(f"Preview: {result['full_text'][:200]}...")
    else:
        print("❌ Failed to fetch WOD")
    return result


if __name__ == '__main__':
    test()
