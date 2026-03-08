"""
שליחת התראות טרנדים ורעיונות לכסף לטלגרם
עיצוב יפה עם אימוג'ים ופורמט מסודר
"""
import requests
import re
import time
from typing import List, Dict, Optional
from trend_tracker import Trend


class TrendNotifier:
    """שולח טרנדים ורעיונות כסף לטלגרם"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text: str, disable_preview: bool = True) -> bool:
        """שולח הודעה לטלגרם"""
        try:
            # ניסיון עם HTML
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": disable_preview,
                },
                timeout=30,
            )

            if response.status_code == 200:
                return True

            # fallback לטקסט רגיל
            if "can't parse entities" in response.text:
                clean_text = re.sub(r"<[^>]+>", "", text)
                response = requests.post(
                    f"{self.api_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": clean_text,
                        "disable_web_page_preview": True,
                    },
                    timeout=30,
                )
                return response.status_code == 200

            print(f"Telegram error: {response.text[:100]}")
            return False

        except Exception as e:
            print(f"Error sending to Telegram: {e}")
            return False

    def send_trends_report(self, trends: List[Trend]) -> bool:
        """שולח דו\"ח טרנדים מעוצב"""
        if not trends:
            return False

        # כותרת
        message_parts = [
            "🔥 <b>טרנדים חמים עכשיו!</b>",
            "",
            "═══════════════════════════",
            "",
        ]

        for i, trend in enumerate(trends[:10], 1):
            emoji = self._get_trend_emoji(trend)
            rising = " 📈" if trend.rising else ""

            message_parts.append(
                f"{emoji} <b>{i}. {trend.title}</b>{rising}"
            )

            if trend.description:
                desc = trend.description[:100]
                message_parts.append(f"   {desc}")

            message_parts.append(f"   📊 ציון: {'⭐' * min(5, trend.score // 2)} ({trend.score}/10)")
            message_parts.append(f"   📌 מקור: {trend.source}")

            if trend.url:
                message_parts.append(f'   🔗 <a href="{trend.url}">לינק</a>')

            message_parts.append("")

        message_parts.extend([
            "═══════════════════════════",
            f"⏰ עודכן: {self._get_hebrew_time()}",
            "🤖 האוטומציות של מאיר",
        ])

        message = "\n".join(message_parts)

        # חלוקה אם ההודעה ארוכה מדי
        if len(message) > 4000:
            return self._send_trends_split(trends)

        return self.send_message(message)

    def send_money_ideas(self, ideas: List[Dict]) -> int:
        """שולח רעיונות כסף לטלגרם"""
        sent_count = 0

        # כותרת
        header = "\n".join([
            "💰 <b>רעיונות להרוויח כסף עם AI!</b>",
            "",
            "═══════════════════════════",
            "🧠 מבוסס על הטרנדים החמים של היום",
            "═══════════════════════════",
        ])
        self.send_message(header)
        time.sleep(2)

        for idea in ideas:
            content = idea.get("content", "")
            if not content:
                continue

            # ניקוי ועיצוב
            formatted = self._format_idea_message(content)

            if self.send_message(formatted):
                sent_count += 1
                print(f"  ✅ נשלח רעיון {sent_count}")

            time.sleep(3)

        # סיכום
        summary = "\n".join([
            "",
            "═══════════════════════════",
            f"💰 <b>סה\"כ {sent_count} רעיונות נשלחו!</b>",
            "",
            "⚡ טיפ: התחל מהרעיון הפשוט ביותר",
            "🔧 השתמש ב-Claude Code לבנייה מהירה",
            "",
            "🤖 האוטומציות של מאיר",
            "═══════════════════════════",
        ])
        self.send_message(summary)

        return sent_count

    def send_trend_analysis(self, analysis: Dict) -> bool:
        """שולח ניתוח מעמיק של טרנד בודד"""
        if not analysis:
            return False

        trend_data = analysis.get("trend", {})
        analysis_text = analysis.get("analysis", "")

        message_parts = [
            "🔍 <b>ניתוח טרנד מעמיק</b>",
            "",
            "═══════════════════════════",
            "",
            f"📌 טרנד: <b>{trend_data.get('title', '')}</b>",
            f"📊 מקור: {trend_data.get('source', '')}",
            f"⭐ ציון: {trend_data.get('score', 0)}/10",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            analysis_text,
            "",
            "═══════════════════════════",
            "🤖 האוטומציות של מאיר",
        ]

        message = "\n".join(message_parts)

        if len(message) > 4000:
            # שליחה בחלקים
            self.send_message("\n".join(message_parts[:10]))
            time.sleep(1)
            self.send_message(analysis_text)
            return True

        return self.send_message(message)

    def _format_idea_message(self, content: str) -> str:
        """מעצב רעיון להודעה יפה"""
        # הוספת מסגרת
        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            content,
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━",
        ]
        return "\n".join(lines)

    def _send_trends_split(self, trends: List[Trend]) -> bool:
        """שולח טרנדים בחלקים אם ההודעה ארוכה מדי"""
        mid = len(trends) // 2
        part1 = trends[:mid]
        part2 = trends[mid:]

        success1 = self.send_trends_report(part1)
        time.sleep(2)
        success2 = self.send_trends_report(part2)

        return success1 or success2

    def _get_trend_emoji(self, trend: Trend) -> str:
        """מחזיר אימוג'י לפי מקור הטרנד"""
        source = trend.source.lower()
        if "google" in source:
            return "🔍"
        elif "reddit" in source:
            return "🔥"
        elif "hacker" in source:
            return "📰"
        elif "product" in source:
            return "🚀"
        return "✨"

    def _get_hebrew_time(self) -> str:
        """מחזיר שעה בפורמט ישראלי"""
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%H:%M %d/%m/%Y")
