"""
Generic WOD Scraper
Best-effort scraper for unknown CrossFit sites
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


WORKOUT_KEYWORDS = [
    'amrap', 'emom', 'for time', 'rounds', 'reps',
    'run', 'row', 'bike', 'kg', 'lbs'
]


def clean_line(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def looks_like_workout(lines):
    text = ' '.join(lines).lower()
    return any(k in text for k in WORKOUT_KEYWORDS)


def fetch_wod(date: datetime, url: str):
    """
    Generic fetcher:
    - Ignores date logic (site dependent)
    - Extracts best workout-looking content
    """

    try:
        print(f"  🔍 Generic scrape: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove obvious noise
        for tag in soup.find_all([
            'script', 'style', 'nav', 'footer', 'header', 'form'
        ]):
            tag.decompose()

        sections = []
        current_section = None

        # Prefer headers as section starters
        elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'])

        for el in elements:
            text = clean_line(el.get_text())
            if not text or len(text) < 3:
                continue

            # Header → new section
            if el.name in ['h1', 'h2', 'h3', 'h4']:
                if current_section and looks_like_workout(current_section['lines']):
                    sections.append(current_section)

                current_section = {
                    'title': text,
                    'lines': []
                }
            else:
                if current_section is None:
                    current_section = {
                        'title': 'Workout',
                        'lines': []
                    }

                current_section['lines'].append(text)

        if current_section and looks_like_workout(current_section['lines']):
            sections.append(current_section)

        # Fallback: raw workout
        if not sections:
            body_text = soup.get_text(separator='\n')
            lines = [
                clean_line(l) for l in body_text.split('\n')
                if len(l.strip()) > 4
            ]

            if looks_like_workout(lines):
                sections = [{
                    'title': 'Workout',
                    'lines': lines[:40]
                }]

        if not sections:
            return None

        return {
            'date': date.strftime('%Y-%m-%d'),
            'sections': sections,
            'url': url,
            'confidence': 'medium'
        }

    except Exception as e:
        print(f"  ❌ Generic scraper error: {e}")
        return None
