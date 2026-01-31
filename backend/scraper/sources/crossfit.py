"""
CrossFit.com Scraper - V2.0
Extracts ONLY workout content with structured sections
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def clean_line(text):
    """Clean a single line"""
    return re.sub(r'\s+', ' ', text).strip()


def parse_workout_sections(raw_text):
    """Parse workout into sections"""
    sections = []
    current_section = {'title': 'Workout', 'lines': []}
    
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    for line in lines:
        # Check for common section patterns
        lower = line.lower()
        
        # Skip strategy/scaling blocks
        if any(x in lower for x in ['stimulus', 'strategy', 'scaling', 'intermediate option', 'beginner option', 'resources']):
            break  # Stop parsing here
        
        # Detect section headers
        if ':' in line and len(line) < 40:
            # "3 rounds for time:" or "AMRAP 10:"
            if current_section['lines']:
                sections.append(current_section)
            current_section = {'title': clean_line(line), 'lines': []}
        else:
            cleaned = clean_line(line)
            if cleaned:
                current_section['lines'].append(cleaned)
    
    if current_section['lines']:
        sections.append(current_section)
    
    return sections


def fetch_wod(date):
    """Fetch WOD from CrossFit.com"""
    date_str = date.strftime('%Y-%m-%d')
    date_code = date.strftime('%y%m%d')
    url = f'https://www.crossfit.com/{date_code}'
    
    try:
        print(f"  Fetching CrossFit.com {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove noise
        for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Find workout
        content = None
        article = soup.find('article')
        if article:
            content = article.get_text(separator='\n', strip=True)
        
        if not content:
            main = soup.find('main')
            if main:
                content = main.get_text(separator='\n', strip=True)
        
        if not content or len(content) < 30:
            return None
        
        # Filter unwanted
        skip = ['find a gym', 'crossfit games', 'subscribe', 'sign up', 'shop', 
                'stimulus and strategy', 'intermediate option', 'beginner option']
        
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        # Stop at "Stimulus" or "Scaling"
        filtered = []
        for l in lines:
            lower = l.lower()
            if any(s in lower for s in ['stimulus', 'scaling', 'intermediate', 'beginner', 'resources']):
                break
            if not any(s in lower for s in skip):
                filtered.append(l)
        
        clean_content = '\n'.join(filtered[:50])  # Limit to first 50 lines
        
        sections = parse_workout_sections(clean_content)
        
        if not sections:
            return None
        
        return {
            'date': date_str,
            'sections': sections,
            'url': url
        }
        
    except Exception as e:
        print(f"  ❌ CrossFit.com error: {e}")
        return None


if __name__ == '__main__':
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ {len(result['sections'])} sections")
    else:
        print("❌ Failed")
