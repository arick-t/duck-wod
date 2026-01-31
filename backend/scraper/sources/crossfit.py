"""
CrossFit.com Scraper
Fetches WODs from crossfit.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def fetch_wod(date):
    """
    Fetch a single WOD from CrossFit.com for a specific date
    
    Args:
        date: datetime object
        
    Returns:
        dict with WOD data or None if not found
    """
    date_str = date.strftime('%Y-%m-%d')
    # CrossFit.com uses format like /260130 for Jan 30, 2026
    date_code = date.strftime('%y%m%d')
    url = f'https://www.crossfit.com/{date_code}'
    
    try:
        print(f"  Fetching CrossFit.com for {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        wod_content = None
        
        # Try to find the main workout content
        # CrossFit.com has different structures, try multiple approaches
        
        # Approach 1: Look for article or main content
        article = soup.find('article')
        if article:
            wod_content = article.get_text(separator='\n', strip=True)
        
        # Approach 2: Look for specific content divs
        if not wod_content:
            content_div = soup.find('div', class_='content-block')
            if content_div:
                wod_content = content_div.get_text(separator='\n', strip=True)
        
        # Approach 3: Look for main tag
        if not wod_content:
            main = soup.find('main')
            if main:
                wod_content = main.get_text(separator='\n', strip=True)
        
        if wod_content:
            # Clean up the content
            lines = [line.strip() for line in wod_content.split('\n') if line.strip()]
            # Filter out navigation/footer elements
            filtered_lines = [
                line for line in lines 
                if not any(skip in line.lower() for skip in [
                    'cookie', 'privacy', 'sign up', 'subscribe',
                    'find a gym', 'crossfit games', 'shop', 'cart'
                ])
            ]
            wod_content = '\n'.join(filtered_lines[:100])  # Limit to first 100 lines
            
            if len(wod_content) > 50:  # Must have substantial content
                return {
                    'date': date_str,
                    'source': 'CrossFit.com',
                    'full_text': wod_content,
                    'url': url,
                    'fetched_at': datetime.now().isoformat()
                }
        
        print(f"  ⚠️  No WOD content found for {date_str}")
        return None
        
    except requests.RequestException as e:
        print(f"  ❌ Error fetching CrossFit.com for {date_str}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error for {date_str}: {e}")
        return None


def test():
    """Test the scraper with today's date"""
    print("Testing CrossFit.com scraper...")
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ Success! Fetched {len(result['full_text'])} characters")
        print(f"Preview: {result['full_text'][:200]}...")
    else:
        print("❌ Failed to fetch WOD")
    return result


if __name__ == '__main__':
    test()
