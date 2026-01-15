#!/usr/bin/env python3
"""
בדיקה מהירה - בודק שהאיסוף עובד (Reddit + Hacker News)
"""
import sys
import os

# הוספת משתני סביבה בסיסיים
os.environ['REDDIT_USER_AGENT'] = 'AI-News-Bot/1.0'

print("\n" + "="*70)
print("🧪 בדיקה מהירה של סוכן החדשות")
print("="*70 + "\n")

print("📦 טוען מודולים...")

from collectors.reddit_collector import RedditCollector
from collectors.hackernews_collector import HackerNewsCollector

def quick_test():
    """בדיקה מהירה"""

    all_news = []

    # בדיקה 1: Reddit (ללא API credentials)
    print("\n1️⃣ בודק Reddit Collector...")
    print("   (עובד במצב ציבורי - ללא API credentials)\n")
    try:
        reddit = RedditCollector()
        reddit_news = reddit.collect(hours_back=24)
        all_news.extend(reddit_news)
        print(f"\n   ✅ Reddit: נמצאו {len(reddit_news)} פוסטים\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # בדיקה 2: Hacker News
    print("2️⃣ בודק Hacker News Collector...\n")
    try:
        hn = HackerNewsCollector()
        hn_news = hn.collect(hours_back=24)
        all_news.extend(hn_news)
        print(f"\n   ✅ Hacker News: נמצאו {len(hn_news)} סטוריז\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # סיכום
    print("="*70)
    print(f"📊 סה\"כ נאספו: {len(all_news)} פריטים")
    print("="*70 + "\n")

    if all_news:
        print("📰 דוגמה לפריטים שנאספו:\n")
        for i, item in enumerate(all_news[:5], 1):
            source_emoji = "🔴" if item.get('source', '').startswith('Reddit') else "🟠"
            print(f"{i}. {source_emoji} [{item.get('source')}]")
            print(f"   📰 {item.get('title')[:65]}...")
            print(f"   🔗 {item.get('url')}")
            if item.get('score'):
                print(f"   ⭐ Score: {item.get('score')}")
            print()

        print("="*70)
        print("✅ הבדיקה הצליחה! האיסוף עובד כמו שצריך!")
        print("="*70)

        print("\n💡 מה קורה עכשיו?")
        print("\n1. הבוט אסף חדשות אמיתיות מ-Reddit ו-Hacker News")
        print("2. בשביל להמשיך, אתה צריך:")
        print("   • ANTHROPIC_API_KEY - לתרגום לעברית")
        print("   • TELEGRAM_CHAT_ID - לשליחה לטלגרם")
        print("\n3. הוסף את המפתחות האלה ב-GitHub Secrets")
        print("4. הבוט ירוץ אוטומטית כל 4 שעות!")
        print("\n📖 קרא את ה-README.md להוראות מפורטות")

    return all_news

if __name__ == "__main__":
    try:
        news = quick_test()

        if not news:
            print("\n⚠️ לא נמצאו חדשות חמות ב-24 השעות האחרונות.")
            print("   זה יכול להיות תקין - נסה שוב מאוחר יותר.")

    except KeyboardInterrupt:
        print("\n\n⏹️ הבדיקה הופסקה על ידי המשתמש")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
