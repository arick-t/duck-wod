"""
CrossFit Linchpin Scraper - V2.0
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def clean_line(text):
    return re.sub(r'\s+', ' ', text).strip()


def parse_workout_sections(raw_text):
    """Parse into sections"""
    sections = [{'title': 'Workout', 'lines': []}]
    
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    for line in lines:
        if any(x in line.lower() for x in ['private track', 'subscribe', 'compare to']):
            break
        
        cleaned = clean_line(line)
        if cleaned and len(cleaned) > 1:
            sections[0]['lines'].append(cleaned)
    
    return sections if sections[0]['lines'] else []


def fetch_wod(date):
    """Fetch today's WOD only (Linchpin has no archive)"""
    if date.date() != datetime.now().date():
        return None
    
    date_str = date.strftime('%Y-%m-%d')
    url = 'https://crossfitlinchpin.com/pages/workout-of-the-day'
    
    try:
        print(f"  Fetching Linchpin {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for tag in soup.find_all(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        
        content = None
        blog_post = soup.find('div', class_='blog-post')
        if blog_post:
            content = blog_post.get_text(separator='\n', strip=True)
        
        if not content:
            article = soup.find('article')
            if article:
                content = article.get_text(separator='\n', strip=True)
        
        if not content or len(content) < 30:
            return None
        
        skip = ['private track', 'podcast', 'testimonials', 'shop']
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        filtered = [l for l in lines if not any(s in l.lower() for s in skip)]
        
        clean_content = '\n'.join(filtered[:40])
        
        sections = parse_workout_sections(clean_content)
        
        if not sections:
            return None
        
        return {
            'date': date_str,
            'sections': sections,
            'url': url,
            'note': 'Today only'
        }
        
    except Exception as e:
        print(f"  ❌ Linchpin error: {e}")
        return None


if __name__ == '__main__':
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ {len(result['sections'])} sections")
    else:
        print("❌ Failed")
