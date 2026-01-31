# 🦆 DUCK-WOD

**אימוני קרוספיט יומיים + חיפוש חכם**

## ✨ תכונות

- 🗓️ עיון באימונים (14 ימים)
- 🔍 חיפוש לפי זמן וציוד
- 🔄 עדכון אוטומטי יומי
- ➕ הוספת מקורות בקלות

## 🚀 התקנה

1. Upload ל-GitHub
2. Settings → Pages → main/frontend
3. Actions → Run workflow
4. קבל לינק!

## ➕ הוספת מקור

צור `backend/scraper/sources/new.py`:
```python
def fetch_wod(date):
    # Your scraping logic
    return {'date': ..., 'source': ..., 'full_text': ...}
```

הוסף ל-`run_scraper.py` ו-`sources.json` - זהו!

## 💡 שימוש

פתח את הלינק שלך - הכל אוטומטי! 🦆

---
100% חינם • MIT License • 🇮🇱
