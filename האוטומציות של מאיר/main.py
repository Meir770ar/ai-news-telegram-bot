#!/usr/bin/env python3
"""
האוטומציות של מאיר - מעקב טרנדים + רעיונות להרוויח כסף
מערכת שלמה: סורקת טרנדים, מנתחת הזדמנויות, ושולחת לטלגרם
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from trend_tracker import TrendTracker, TrendHistory
from money_ideas import MoneyIdeasGenerator, QuickMoneyIdeas
from telegram_notifier import TrendNotifier


def run_full_pipeline():
    """מריץ את כל הצינור - טרנדים + רעיונות + שליחה לטלגרם"""
    print("=" * 50)
    print("🚀 האוטומציות של מאיר - מתחיל!")
    print("=" * 50)

    # בדיקת הגדרות
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("❌ חסר TELEGRAM_BOT_TOKEN או TELEGRAM_CHAT_ID")
        sys.exit(1)

    if not config.GEMINI_API_KEY:
        print("⚠️ חסר GEMINI_API_KEY - רעיונות AI לא יעבדו, ישתמש בתבניות")

    # אתחול
    tracker = TrendTracker(config)
    history = TrendHistory(config.SENT_TRENDS_FILE)
    notifier = TrendNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)

    # שלב 1: איסוף טרנדים
    print("\n📡 שלב 1: איסוף טרנדים...")
    all_trends = tracker.collect_all_trends()

    if not all_trends:
        print("ℹ️ לא נמצאו טרנדים. יוצא.")
        return

    # שלב 2: סינון טרנדים שכבר נשלחו
    print("\n🔍 שלב 2: סינון כפילויות...")
    new_trends = history.filter_new(all_trends)
    print(f"📊 טרנדים חדשים: {len(new_trends)} (סוננו {len(all_trends) - len(new_trends)})")

    if not new_trends:
        print("ℹ️ אין טרנדים חדשים. יוצא.")
        return

    # הגבלה
    top_trends = new_trends[:config.MAX_TRENDS_PER_RUN]

    # שלב 3: שליחת דו"ח טרנדים
    print("\n📤 שלב 3: שליחת טרנדים לטלגרם...")
    notifier.send_trends_report(top_trends)

    # שלב 4: יצירת רעיונות כסף
    print("\n💰 שלב 4: יצירת רעיונות להרוויח כסף...")
    ideas = []

    if config.GEMINI_API_KEY:
        try:
            generator = MoneyIdeasGenerator(config.GEMINI_API_KEY)
            ideas = generator.generate_ideas(top_trends, num_ideas=5)
            print(f"  ✅ נוצרו {len(ideas)} רעיונות עם AI")
        except Exception as e:
            print(f"  ⚠️ שגיאה ביצירת רעיונות: {e}")

    if not ideas:
        # fallback לתבניות
        print("  📋 משתמש ברעיונות מתבניות...")
        template_text = QuickMoneyIdeas.get_template_ideas()
        notifier.send_message(template_text)
    else:
        # שליחת רעיונות AI
        print("\n📤 שולח רעיונות לטלגרם...")
        sent = notifier.send_money_ideas(ideas)
        print(f"  ✅ נשלחו {sent} רעיונות")

    # שלב 5: ניתוח מעמיק של הטרנד החם ביותר
    if config.GEMINI_API_KEY and top_trends:
        print("\n🔍 שלב 5: ניתוח מעמיק של הטרנד החם ביותר...")
        try:
            generator = MoneyIdeasGenerator(config.GEMINI_API_KEY)
            analysis = generator.analyze_single_trend(top_trends[0])
            if analysis:
                notifier.send_trend_analysis(analysis)
                print("  ✅ ניתוח מעמיק נשלח!")
        except Exception as e:
            print(f"  ⚠️ שגיאה בניתוח מעמיק: {e}")

    # שלב 6: סימון כנשלח וניקוי
    for trend in top_trends:
        history.mark_sent(trend)
    history.cleanup()

    print("\n" + "=" * 50)
    print("✅ האוטומציות של מאיר - הושלם בהצלחה!")
    print(f"📊 טרנדים שנשלחו: {len(top_trends)}")
    print(f"💰 רעיונות שנוצרו: {len(ideas)}")
    print("=" * 50)


def run_trends_only():
    """מריץ רק את מעקב הטרנדים"""
    print("🔍 מצב: מעקב טרנדים בלבד")
    tracker = TrendTracker(config)
    trends = tracker.collect_all_trends()

    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        notifier = TrendNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        notifier.send_trends_report(trends)
    else:
        for t in trends[:10]:
            print(f"  {'📈' if t.rising else '📊'} [{t.score}/10] {t.title} ({t.source})")


def run_ideas_only():
    """מריץ רק את יצירת הרעיונות"""
    print("💰 מצב: רעיונות כסף בלבד")

    if not config.GEMINI_API_KEY:
        print(QuickMoneyIdeas.get_template_ideas())
        return

    tracker = TrendTracker(config)
    trends = tracker.collect_all_trends()
    generator = MoneyIdeasGenerator(config.GEMINI_API_KEY)
    ideas = generator.generate_ideas(trends, num_ideas=5)

    if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
        notifier = TrendNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        notifier.send_money_ideas(ideas)
    else:
        for idea in ideas:
            print(idea.get("content", ""))
            print("---")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"

    if mode == "trends":
        run_trends_only()
    elif mode == "ideas":
        run_ideas_only()
    else:
        run_full_pipeline()
