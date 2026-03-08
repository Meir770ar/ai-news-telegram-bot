#!/usr/bin/env python3
"""
דמו - מציג את שתי המערכות בקונסולה (בלי טלגרם)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from trend_tracker import TrendTracker, Trend
from money_ideas import QuickMoneyIdeas

# Override config to disable telegram requirement
config.TELEGRAM_BOT_TOKEN = ""
config.TELEGRAM_CHAT_ID = ""


def demo_trends():
    """דמו מעקב טרנדים"""
    print("=" * 55)
    print("🔥  מערכת 1: מעקב טרנדים חמים")
    print("=" * 55)
    print()

    tracker = TrendTracker(config)
    trends = tracker.collect_all_trends()

    if not trends:
        print("⚠️ לא הצליח לאסוף טרנדים (ייתכן בעיית רשת)")
        return []

    print()
    print("═══════════════════════════════════════════════════")
    print(f"  🔥 טופ {min(10, len(trends))} טרנדים חמים עכשיו!")
    print("═══════════════════════════════════════════════════")
    print()

    for i, trend in enumerate(trends[:10], 1):
        rising = " 📈 עולה!" if trend.rising else ""
        stars = "⭐" * min(5, max(1, trend.score // 2))

        print(f"  {i}. {trend.title}{rising}")
        if trend.description:
            print(f"     📋 {trend.description[:80]}")
        print(f"     📊 ציון: {stars} ({trend.score}/10)")
        print(f"     📌 מקור: {trend.source}")
        if trend.url:
            print(f"     🔗 {trend.url[:70]}")
        print()

    print("═══════════════════════════════════════════════════")
    print(f"  📊 סה\"כ נאספו: {len(trends)} טרנדים מכל המקורות")
    print("═══════════════════════════════════════════════════")

    return trends


def demo_money_ideas(trends):
    """דמו רעיונות כסף"""
    print()
    print()
    print("=" * 55)
    print("💰  מערכת 2: רעיונות להרוויח כסף עם Claude Code")
    print("=" * 55)
    print()

    # אם יש Gemini API - ניצור רעיונות מבוססי AI
    if config.GEMINI_API_KEY and trends:
        print("🧠 מייצר רעיונות עם AI על בסיס הטרנדים...")
        print()
        try:
            from money_ideas import MoneyIdeasGenerator
            generator = MoneyIdeasGenerator(config.GEMINI_API_KEY)
            ideas = generator.generate_ideas(trends, num_ideas=5)

            if ideas:
                for i, idea in enumerate(ideas, 1):
                    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print(idea.get("content", ""))
                    print()

                # ניתוח מעמיק של הטרנד הכי חם
                print()
                print("═══════════════════════════════════════════════════")
                print(f"  🔍 ניתוח מעמיק: {trends[0].title}")
                print("═══════════════════════════════════════════════════")
                print()

                analysis = generator.analyze_single_trend(trends[0])
                if analysis:
                    print(analysis.get("analysis", ""))

                return
        except Exception as e:
            print(f"⚠️ שגיאה ב-AI: {e}")
            print("📋 עובר לרעיונות מתבניות...\n")

    # Fallback - תבניות מוכנות
    print(QuickMoneyIdeas.get_template_ideas())


if __name__ == "__main__":
    trends = demo_trends()
    demo_money_ideas(trends)

    print()
    print("═══════════════════════════════════════════════════")
    print("  ✅ הדמו הסתיים!")
    print("  💡 הפעל עם GEMINI_API_KEY לרעיונות AI מותאמים")
    print("  📱 הפעל עם TELEGRAM_BOT_TOKEN לשליחה לטלגרם")
    print("═══════════════════════════════════════════════════")
