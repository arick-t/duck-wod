# 🦆 DUCK-WOD V2.0

**CrossFit Workout Aggregator with Smart Search**

---

## ✨ What's New in V2.0

### 🎯 **Priority 1: Clean Scraper**
- ✅ Extracts **ONLY workout content** (no menus, footers, strategy)
- ✅ **Structured sections** (Warm-up, Strength, Metcon, etc.)
- ✅ **Bullet-point format** preserved
- ✅ New JSON structure with sections

### ⚙️ **Priority 2: Source Management**
- ✅ **Add custom sources** via UI
- ✅ **Enable/Disable** sources with toggle
- ✅ **Delete** sources
- ✅ **URL validation** (checks for 14-day archive)

### 🔍 **Priority 3: Advanced Find Workout**
- ✅ Search by **time** and **equipment**
- ✅ **Equipment matching** (60% of score)
- ✅ **Time estimation** (40% of score)
- ✅ **Match score percentage**
- ✅ Shows **original workout** (no modifications)

---

## 📦 Installation

1. Upload to GitHub
2. Enable GitHub Pages (Settings → Pages → main/frontend)
3. Run Actions workflow once
4. Done! 🎉

---

## 🎯 How to Use

### Browse Workouts
- See recent WODs from all enabled sources
- Organized in **sections with bullets**
- Clean, readable format

### Find Workout
1. Enter available time (minutes)
2. Select equipment you have
3. Click "Find Best Match"
4. Get best workout with match score!

### Manage Sources
- **Toggle** sources on/off
- **Add** custom sources
- **Delete** unused sources

---

## ➕ Adding a Custom Source

### Via UI (Easy!)
1. Go to "Manage Sources" tab
2. Enter source name and URL
3. Click "Add Source"
4. ✅ Source added!

⚠️ **Note:** To actually fetch workouts, you need to create a scraper module.

### Creating a Scraper

Create `backend/scraper/sources/your_source.py`:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_wod(date):
    date_str = date.strftime('%Y-%m-%d')
    url = f'https://yoursource.com/wod/{date_str}/'
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract workout sections
        sections = []
        # ... your parsing logic ...
        
        return {
            'date': date_str,
            'sections': sections,
            'url': url
        }
    except:
        return None
```

Add to `run_scraper.py`:
```python
from scraper.sources import myleo, crossfit, linchpin, your_source

modules = {
    'myleo': myleo,
    'crossfit': crossfit,
    'linchpin': linchpin,
    'your_source': your_source,  # Add here
}
```

---

## 📊 JSON Structure

### wods.json
```json
{
  "last_updated": "2026-01-31T12:00:00",
  "sources": [
    {
      "id": "myleo",
      "name": "myleo CrossFit",
      "url": "https://myleo.de/en/wods/",
      "wods": [
        {
          "date": "2026-01-31",
          "sections": [
            {
              "title": "Warm-up",
              "lines": ["10 min easy jog", "Mobility drills"]
            },
            {
              "title": "Strength",
              "lines": ["5x5 Back Squat @ 75%"]
            }
          ],
          "url": "https://..."
        }
      ]
    }
  ]
}
```

### sources.json
```json
[
  {
    "id": "myleo",
    "name": "myleo CrossFit",
    "url": "https://myleo.de/en/wods/",
    "enabled": true,
    "added_at": "2026-01-31T12:00:00"
  }
]
```

---

## 🔧 Technical Details

### Scraper Features
- Removes unwanted content (navigation, footers, comments)
- Parses sections automatically
- Preserves workout structure
- Filters out strategy/scaling text

### Find Workout Algorithm
1. **Equipment Match (60%)**
   - Checks for keywords in workout text
   - More matches = higher score

2. **Time Estimate (40%)**
   - Extracts explicit time from workout
   - Uses heuristics for AMRAP/EMOM/For Time
   - Penalizes time mismatches

3. **Result**
   - Best match from last 14 days
   - Shows original workout (unchanged)
   - Match score 0-100%

---

## 🐛 Troubleshooting

**No workouts showing?**
- Check that sources are enabled in "Manage Sources"
- Run GitHub Actions workflow
- Check `data/wods.json` exists

**Find Workout returns nothing?**
- Try selecting more equipment
- Adjust time range
- Check that you have WODs in last 14 days

**Source management not saving?**
- Changes save to localStorage (browser only)
- To persist, manually update `data/sources.json` in repo

---

## 💰 Cost

**100% FREE!**
- GitHub Pages ✅
- GitHub Actions ✅

---

## 🦆 Happy Training!

Built with ❤️ for the CrossFit community
