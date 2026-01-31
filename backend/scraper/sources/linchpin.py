"""
CrossFit Linchpin Scraper
Fetches today's WOD from crossfitlinchpin.com
Note: Linchpin only publishes today's WOD (no archive)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def fetch_wod(date):
    """
    Fetch today's WOD from CrossFit Linchpin
    
    Args:
        date: datetime object (only today is supported)
        
    Returns:
        dict with WOD data or None if not today or not found
    """
    # Linchpin only has today's workout
    today = datetime.now().date()
    if date.date() != today:
        return None
    
    date_str = date.strftime('%Y-%m-%d')
    url = 'https://crossfitlinchpin.com/pages/workout-of-the-day'
    
    try:
        print(f"  Fetching Linchpin for {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        wod_content = None
        
        # Look for the blog post or workout section
        blog_post = soup.find('div', class_='blog-post')
        if blog_post:
            wod_content = blog_post.get_text(separator='\n', strip=True)
        
        # Alternative: look for article
        if not wod_content:
            article = soup.find('article')
            if article:
                wod_content = article.get_text(separator='\n', strip=True)
        
        # Alternative: look for main content
        if not wod_content:
            main = soup.find('main') or soup.find('div', {'id': 'content'})
            if main:
                wod_content = main.get_text(separator='\n', strip=True)
        
        if wod_content:
            # Clean up the content
            lines = [line.strip() for line in wod_content.split('\n') if line.strip()]
            # Filter out navigation/footer elements
            filtered_lines = [
                line for line in lines 
                if not any(skip in line.lower() for skip in [
                    'cookie', 'privacy', 'subscribe', 'instagram',
                    'podcast', 'shop', 'cart', 'testimonials'
                ])
            ]
            wod_content = '\n'.join(filtered_lines[:100])  # Limit to first 100 lines
            
            if len(wod_content) > 50:  # Must have substantial content
                return {
                    'date': date_str,
                    'source': 'CrossFit Linchpin',
                    'full_text': wod_content,
                    'url': url,
                    'has_archive': False,
                    'note': 'Today only - no archive available',
                    'fetched_at': datetime.now().isoformat()
                }
        
        print(f"  ⚠️  No WOD content found for {date_str}")
        return None
        
    except requests.RequestException as e:
        print(f"  ❌ Error fetching Linchpin for {date_str}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Unexpected error for {date_str}: {e}")
        return None


def test():
    """Test the scraper with today's date"""
    print("Testing Linchpin scraper...")
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ Success! Fetched {len(result['full_text'])} characters")
        print(f"Preview: {result['full_text'][:200]}...")
    else:
        print("❌ Failed to fetch WOD")
    return result


if __name__ == '__main__':
    test()
