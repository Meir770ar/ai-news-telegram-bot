"""
הגדרות עבור מערכת מעקב טרנדים + רעיונות להרוויח כסף
"""
import os

# Telegram (משתמש באותו בוט)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Gemini API (לניתוח טרנדים ויצירת רעיונות)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# מקורות טרנדים
TREND_SOURCES = {
    "google_trends": {
        "enabled": True,
        "geo": "IL",  # ישראל
        "language": "he",
    },
    "reddit": {
        "enabled": True,
        "subreddits": [
            "SideProject",
            "EntrepreneurRideAlong",
            "microsaas",
            "indiehackers",
            "passive_income",
            "OpenAI",
            "ClaudeAI",
            "LocalLLaMA",
            "MachineLearning",
        ],
    },
    "product_hunt": {
        "enabled": True,
    },
    "hacker_news": {
        "enabled": True,
        "min_score": 50,
    },
}

# קטגוריות רעיונות לכסף עם Claude Code
MONEY_CATEGORIES = [
    "micro_saas",           # מוצרי SaaS קטנים
    "automation_services",  # שירותי אוטומציה ללקוחות
    "content_generation",   # יצירת תוכן אוטומטית
    "data_analysis",        # ניתוח נתונים
    "bot_development",      # פיתוח בוטים
    "api_integration",      # אינטגרציות בין מערכות
    "scraping_services",    # שירותי סקרייפינג
    "freelance_tools",      # כלים לפרילאנסרים
]

# קובץ מעקב
TRENDS_HISTORY_FILE = "trends_history.json"
SENT_TRENDS_FILE = "sent_trends.json"

# הגדרות שליחה
MAX_TRENDS_PER_RUN = 10
MIN_TREND_SCORE = 3  # ציון מינימלי לשליחה (1-10)
