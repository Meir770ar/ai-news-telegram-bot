"""
שולח חדשות לטלגרם בפורמט מעוצב
"""
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from typing import List, Dict

class TelegramSender:
    """שולח הודעות מעוצבות לטלגרם"""

    def __init__(self):
        """מאתחל את Telegram Bot"""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not self.token:
            raise ValueError("חסר TELEGRAM_BOT_TOKEN במשתני הסביבה")
        if not self.chat_id:
            raise ValueError("חסר TELEGRAM_CHAT_ID במשתני הסביבה")

        self.bot = Bot(token=self.token)

        # אמוג'ים לסוגי מקורות שונים
        self.source_emojis = {
            'Reddit': '🔴',
            'Product Hunt': '🚀',
            'Hacker News': '🟠',
            'TechCrunch': '📰',
            'OpenAI': '🤖',
            'Anthropic': '🧠'
        }

    def _format_message(self, news_item: Dict) -> str:
        """
        מעצב הודעה לטלגרם

        Args:
            news_item: פריט חדשות

        Returns:
            הודעה מעוצבת
        """
        # בוחר אמוג'י לפי המקור
        source = news_item.get('source', '')
        emoji = self.source_emojis.get(source, '🔥')

        title = news_item.get('title', '')
        hebrew_summary = news_item.get('hebrew_summary', '')
        video_ideas = news_item.get('video_ideas', [])
        url = news_item.get('url', '')

        # בונה את ההודעה
        message = f"{emoji} <b>{title}</b>\n\n"
        message += f"{hebrew_summary}\n\n"

        # מוסיף רעיונות לסרטונים
        if video_ideas:
            message += "💡 <b>רעיונות לסרטונים:</b>\n"
            for idea in video_ideas:
                message += f"• {idea}\n"
            message += "\n"

        # מוסיף קישור
        message += f"🔗 <a href='{url}'>קרא עוד</a>"

        return message

    async def send_message(self, message: str) -> bool:
        """
        שולח הודעה בודדת לטלגרם

        Args:
            message: תוכן ההודעה

        Returns:
            True אם נשלח בהצלחה
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            return True
        except Exception as e:
            print(f"❌ שגיאה בשליחת הודעה: {e}")
            return False

    async def send_news_item(self, news_item: Dict) -> bool:
        """
        שולח פריט חדשות בודד

        Args:
            news_item: פריט חדשות

        Returns:
            True אם נשלח בהצלחה
        """
        try:
            message = self._format_message(news_item)
            success = await self.send_message(message)

            if success:
                print(f"✅ נשלח: {news_item.get('title', '')[:50]}...")
            else:
                print(f"❌ נכשל: {news_item.get('title', '')[:50]}...")

            # מחכה קצת בין הודעות (למנוע rate limiting)
            await asyncio.sleep(1)

            return success

        except Exception as e:
            print(f"❌ שגיאה בשליחת פריט: {e}")
            return False

    async def send_batch(self, news_items: List[Dict]) -> int:
        """
        שולח מספר פריטי חדשות

        Args:
            news_items: רשימת פריטי חדשות

        Returns:
            מספר הפריטים שנשלחו בהצלחה
        """
        if not news_items:
            print("אין חדשות לשלוח")
            return 0

        print(f"\n📤 שולח {len(news_items)} חדשות לטלגרם...")

        # שולח הודעת פתיחה
        header_message = f"🔥 <b>עדכוני AI חמים ({len(news_items)} חדשות)</b> 🔥"
        await self.send_message(header_message)
        await asyncio.sleep(1)

        # שולח כל חדשה
        success_count = 0
        for i, item in enumerate(news_items, 1):
            print(f"שולח {i}/{len(news_items)}...", end=" ")
            if await self.send_news_item(item):
                success_count += 1

        # הודעת סיום
        footer_message = f"✅ סיימנו! נשלחו {success_count} מתוך {len(news_items)} חדשות"
        await self.send_message(footer_message)

        print(f"\n✅ נשלחו בהצלחה {success_count} פריטים")
        return success_count

    def send_batch_sync(self, news_items: List[Dict]) -> int:
        """
        גרסה סינכרונית של send_batch

        Args:
            news_items: רשימת פריטי חדשות

        Returns:
            מספר הפריטים שנשלחו בהצלחה
        """
        return asyncio.run(self.send_batch(news_items))
