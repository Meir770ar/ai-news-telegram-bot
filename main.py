#!/usr/bin/env python3
"""
סוכן איסוף חדשות AI ושליחה לטלגרם
מריץ כל 4 שעות ע"י GitHub Actions
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# טוען משתני סביבה
load_dotenv()

# מייבא את כל המודולים
from collectors import (
    RedditCollector,
    ProductHuntCollector,
    HackerNewsCollector,
    TechCrunchCollector,
    BlogsCollector
)
from translator import NewsTranslator
from telegram_sender import TelegramSender
from database import NewsDatabase


def collect_all_news(hours_back: int = 4):
    """
    אוסף חדשות מכל המקורות

    Args:
        hours_back: כמה שעות אחורה לאסוף

    Returns:
        רשימת כל החדשות
    """
    print("\n" + "="*60)
    print("🔍 מתחיל איסוף חדשות AI...")
    print("="*60)

    all_news = []

    # Reddit
    try:
        reddit = RedditCollector()
        reddit_news = reddit.collect(hours_back)
        all_news.extend(reddit_news)
    except Exception as e:
        print(f"⚠️ שגיאה באיסוף מ-Reddit: {e}")

    # Product Hunt
    try:
        ph = ProductHuntCollector()
        ph_news = ph.collect(hours_back)
        all_news.extend(ph_news)
    except Exception as e:
        print(f"⚠️ שגיאה באיסוף מ-Product Hunt: {e}")

    # Hacker News
    try:
        hn = HackerNewsCollector()
        hn_news = hn.collect(hours_back)
        all_news.extend(hn_news)
    except Exception as e:
        print(f"⚠️ שגיאה באיסוף מ-Hacker News: {e}")

    # TechCrunch
    try:
        tc = TechCrunchCollector()
        tc_news = tc.collect(hours_back)
        all_news.extend(tc_news)
    except Exception as e:
        print(f"⚠️ שגיאה באיסוף מ-TechCrunch: {e}")

    # Blogs (OpenAI, Anthropic)
    try:
        blogs = BlogsCollector()
        blog_news = blogs.collect(hours_back)
        all_news.extend(blog_news)
    except Exception as e:
        print(f"⚠️ שגיאה באיסוף מבלוגים: {e}")

    print(f"\n✅ נאספו סה\"כ {len(all_news)} פריטים מכל המקורות")
    return all_news


def sort_by_importance(news_items):
    """
    ממיין פריטי חדשות לפי חשיבות
    (score גבוה יותר, מקורות חשובים יותר)

    Args:
        news_items: רשימת חדשות

    Returns:
        רשימה ממוינת
    """
    # משקל לפי מקור
    source_weights = {
        'OpenAI': 100,
        'Anthropic': 100,
        'TechCrunch': 80,
        'Hacker News': 70,
        'Product Hunt': 60,
        'Reddit': 50
    }

    def get_importance(item):
        source_weight = source_weights.get(item.get('source', ''), 50)
        score = item.get('score', 0)
        return source_weight + score

    return sorted(news_items, key=get_importance, reverse=True)


def main():
    """הפונקציה הראשית"""
    print("\n" + "🤖"*30)
    print("🤖  AI News Bot - Starting...  🤖")
    print("🤖"*30)
    print(f"⏰ זמן הרצה: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 1. איסוף חדשות
        all_news = collect_all_news(hours_back=4)

        if not all_news:
            print("\n⚠️ לא נמצאו חדשות חדשות. יוצא.")
            return

        # 2. סינון כפילויות
        print("\n" + "="*60)
        print("🔍 מסנן כפילויות...")
        print("="*60)
        db = NewsDatabase()
        new_items = db.filter_new_items(all_news)

        if not new_items:
            print("\n✅ אין חדשות חדשות לשלוח (הכל כבר נשלח). יוצא.")
            db.print_stats()
            return

        # 3. ממיין לפי חשיבות
        new_items = sort_by_importance(new_items)

        # מגביל ל-10 חדשות הכי חשובות
        max_items = 10
        if len(new_items) > max_items:
            print(f"📊 מגביל ל-{max_items} החדשות החשובות ביותר")
            new_items = new_items[:max_items]

        # 4. תרגום והוספת רעיונות
        print("\n" + "="*60)
        print("🌐 מתרגם לעברית ומוסיף רעיונות...")
        print("="*60)
        translator = NewsTranslator()
        translated_items = translator.translate_batch(new_items)

        # 5. שליחה לטלגרם
        print("\n" + "="*60)
        print("📤 שולח לטלגרם...")
        print("="*60)
        sender = TelegramSender()
        sent_count = sender.send_batch_sync(translated_items)

        # 6. עדכון מסד נתונים
        print("\n" + "="*60)
        print("💾 מעדכן מסד נתונים...")
        print("="*60)
        for item in translated_items:
            db.mark_as_sent(item)

        # 7. ניקוי פריטים ישנים (מעל 7 ימים)
        db.cleanup_old_items(days=7)

        # 8. סיכום
        print("\n" + "="*60)
        print("📊 סיכום הרצה")
        print("="*60)
        print(f"✅ נאספו: {len(all_news)} פריטים")
        print(f"✅ חדשים: {len(new_items)} פריטים")
        print(f"✅ נשלחו: {sent_count} פריטים")

        db.print_stats()

        print("\n" + "🎉"*30)
        print("🎉  סיימנו בהצלחה!  🎉")
        print("🎉"*30)

    except Exception as e:
        print("\n" + "❌"*30)
        print(f"❌ שגיאה כללית: {e}")
        print("❌"*30)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
