"""
myleo CrossFit Scraper - V2.0
Extracts ONLY workout content with structured sections
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def clean_line(text):
    """Clean a single line of text"""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_workout_sections(raw_text):
    """
    Parse workout into structured sections
    Returns: [{'title': str, 'lines': [str, str, ...]}, ...]
    """
    sections = []
    current_section = None
    
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    for line in lines:
        # Pattern 1: a) warm up, b) strength, etc.
        match = re.match(r'^([a-z])\)\s*(.+)', line, re.IGNORECASE)
        if match:
            # Save previous section
            if current_section and current_section['lines']:
                sections.append(current_section)
            
            # Start new section
            title = clean_line(match.group(2))
            current_section = {'title': title, 'lines': []}
            continue
        
        # Pattern 2: Short line that looks like a header (less than 30 chars, contains keywords)
        if len(line) < 30 and not re.search(r'\d+\s*(reps|rounds|min|sec|kg|lbs)', line.lower()):
            keywords = ['warm', 'strength', 'conditioning', 'metcon', 'skill', 'mobility', 'wod']
            if any(kw in line.lower() for kw in keywords):
                if current_section and current_section['lines']:
                    sections.append(current_section)
                current_section = {'title': clean_line(line), 'lines': []}
                continue
        
        # Regular line - add to current section
        if current_section is not None:
            cleaned = clean_line(line)
            if cleaned and len(cleaned) > 1:
                current_section['lines'].append(cleaned)
        else:
            # No section yet, create default "Workout" section
            if not sections:
                current_section = {'title': 'Workout', 'lines': [clean_line(line)]}
    
    # Add last section
    if current_section and current_section['lines']:
        sections.append(current_section)
    
    return sections


def fetch_wod(date):
    """Fetch WOD from myleo - returns structured data"""
    date_str = date.strftime('%Y-%m-%d')
    url = f'https://myleo.de/en/wods/{date_str}/'
    
    try:
        print(f"  Fetching myleo {date_str}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove noise
        for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'form']):
            tag.decompose()
        
        # Find workout content
        content = None
        
        # Try article > entry-content
        article = soup.find('article')
        if article:
            for unwanted in article.find_all(class_=['post-navigation', 'comments', 'share', 'tags']):
                unwanted.decompose()
            
            entry = article.find('div', class_='entry-content')
            if entry:
                content = entry.get_text(separator='\n', strip=True)
        
        if not content:
            # Fallback
            main = soup.find('main') or soup.find('div', class_='wod')
            if main:
                content = main.get_text(separator='\n', strip=True)
        
        if not content or len(content) < 30:
            return None
        
        # Filter unwanted lines
        skip = ['weekly overview', 'post your score', 'compare to', 'skill class', 
                'cookie', 'privacy', 'login', 'register', 'comments']
        
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        filtered = [l for l in lines if not any(s in l.lower() for s in skip)]
        
        clean_content = '\n'.join(filtered)
        
        # Parse sections
        sections = parse_workout_sections(clean_content)
        
        if not sections:
            return None
        
        return {
            'date': date_str,
            'sections': sections,
            'url': url
        }
        
    except Exception as e:
        print(f"  ❌ myleo error: {e}")
        return None


if __name__ == '__main__':
    result = fetch_wod(datetime.now())
    if result:
        print(f"✅ {len(result['sections'])} sections")
        for s in result['sections']:
            print(f"  [{s['title']}] {len(s['lines'])} lines")
    else:
        print("❌ Failed")
