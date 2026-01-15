#!/usr/bin/env python3
"""
סקריפט בדיקה - בודק שהאיסוף עובד (בלי תרגום ושליחה)
"""
import sys
from collectors import (
    RedditCollector,
    ProductHuntCollector,
    HackerNewsCollector,
    TechCrunchCollector,
    BlogsCollector
)

def test_collectors():
    """בודק שכל האספנים עובדים"""

    print("\n" + "="*60)
    print("🧪 בדיקת מודולי איסוף חדשות")
    print("="*60 + "\n")

    all_news = []

    # בדיקה 1: Reddit
    print("1️⃣ בודק Reddit Collector...")
    try:
        reddit = RedditCollector()
        reddit_news = reddit.collect(hours_back=24)  # 24 שעות לבדיקה
        all_news.extend(reddit_news)
        print(f"   ✅ עבד! נמצאו {len(reddit_news)} פוסטים\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # בדיקה 2: Product Hunt
    print("2️⃣ בודק Product Hunt Collector...")
    try:
        ph = ProductHuntCollector()
        ph_news = ph.collect(hours_back=24)
        all_news.extend(ph_news)
        print(f"   ✅ עבד! נמצאו {len(ph_news)} מוצרים\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # בדיקה 3: Hacker News
    print("3️⃣ בודק Hacker News Collector...")
    try:
        hn = HackerNewsCollector()
        hn_news = hn.collect(hours_back=24)
        all_news.extend(hn_news)
        print(f"   ✅ עבד! נמצאו {len(hn_news)} סטוריז\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # בדיקה 4: TechCrunch
    print("4️⃣ בודק TechCrunch Collector...")
    try:
        tc = TechCrunchCollector()
        tc_news = tc.collect(hours_back=24)
        all_news.extend(tc_news)
        print(f"   ✅ עבד! נמצאו {len(tc_news)} חדשות\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # בדיקה 5: Blogs
    print("5️⃣ בודק Blogs Collector (OpenAI + Anthropic)...")
    try:
        blogs = BlogsCollector()
        blog_news = blogs.collect(hours_back=24)
        all_news.extend(blog_news)
        print(f"   ✅ עבד! נמצאו {len(blog_news)} פוסטים\n")
    except Exception as e:
        print(f"   ⚠️ שגיאה: {e}\n")

    # סיכום
    print("="*60)
    print(f"📊 סה\"כ נאספו: {len(all_news)} פריטים")
    print("="*60 + "\n")

    if all_news:
        print("📰 דוגמה לפריטים שנאספו (5 הראשונים):\n")
        for i, item in enumerate(all_news[:5], 1):
            print(f"{i}. [{item.get('source')}] {item.get('title')[:70]}...")
            print(f"   🔗 {item.get('url')}\n")

    return all_news

if __name__ == "__main__":
    try:
        news = test_collectors()

        if news:
            print("\n✅ הבדיקה הצליחה! האיסוף עובד כמו שצריך.")
            print("\n💡 השלב הבא: הוסף ANTHROPIC_API_KEY ו-TELEGRAM_CHAT_ID ל-.env")
            print("   ואז תוכל להריץ: python main.py")
        else:
            print("\n⚠️ לא נמצאו חדשות. זה יכול להיות תקין אם לא היו חדשות חמות.")

    except KeyboardInterrupt:
        print("\n\n⏹️ הבדיקה הופסקה על ידי המשתמש")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
        sys.exit(1)
