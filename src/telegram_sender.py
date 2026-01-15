"""
Telegram message sender
"""
import requests
from typing import List, Optional
import time
import re


class TelegramSender:
    """Send formatted messages to Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def _clean_html(self, text: str) -> str:
        """Remove unsupported HTML tags, keep only Telegram-supported ones"""
        if not text:
            return ""
        
        # Remove all HTML tags except the ones Telegram supports
        # Telegram supports: <b>, <i>, <u>, <s>, <code>, <pre>, <a>
        
        # First, remove all tags
        clean = re.sub(r'<[^>]+>', '', text)
        
        # Also clean up special characters that might break HTML
        clean = clean.replace('&', '&amp;')
        clean = clean.replace('<', '&lt;')
        clean = clean.replace('>', '&gt;')
        
        return clean.strip()
    
    def send_message(self, text: str, disable_preview: bool = False) -> bool:
        """Send a message to the configured chat"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": disable_preview
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return True
            else:
                # If HTML parsing fails, try without parse_mode
                if "can't parse entities" in response.text:
                    return self._send_plain_text(text)
                print(f"Telegram error: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending to Telegram: {e}")
            return False
    
    def _send_plain_text(self, text: str) -> bool:
        """Send message as plain text (fallback)"""
        try:
            # Remove all HTML tags
            clean_text = re.sub(r'<[^>]+>', '', text)
            
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": clean_text,
                    "disable_web_page_preview": False
                },
                timeout=30
            )
            
            return response.status_code == 200
        except:
            return False
    
    def format_news_message(self, processed_item: dict) -> str:
        """Format a processed news item for Telegram - DETAILED VERSION"""
        original = processed_item["original"]
        processed = processed_item["processed"]
        
        # Build message
        message_parts = []
        
        # === HEADER WITH EMOJI ===
        emoji = self._get_source_emoji(original["source"])
        title = self._clean_html(processed.get("hebrew_title") or original["title"])
        message_parts.append(f"{emoji} <b>{title}</b>")
        message_parts.append("")
        
        # === DETAILED SUMMARY (150+ words) ===
        if processed.get("summary"):
            message_parts.append("📋 <b>סיכום מפורט:</b>")
            message_parts.append(self._clean_html(processed["summary"]))
            message_parts.append("")
        
        # === BOTTOM LINE ===
        if processed.get("bottom_line"):
            message_parts.append(f"💡 <b>שורה תחתונה:</b>")
            message_parts.append(self._clean_html(processed["bottom_line"]))
            message_parts.append("")
        
        # === VIDEO SCRIPT ===
        if processed.get("video_script") and processed["video_script"] != "לא ניתן ליצור תסריט כרגע.":
            message_parts.append("🎬 <b>תסריט לסרטון (דקה):</b>")
            message_parts.append(self._clean_html(processed["video_script"]))
            message_parts.append("")
        
        # === SOURCE AND LINK ===
        message_parts.append("─" * 25)
        message_parts.append(f"📰 מקור: {original['source']}")
        message_parts.append(f"🔗 <a href=\"{original['url']}\">לקריאה המלאה</a>")
        
        return "\n".join(message_parts)
    
    def _get_source_emoji(self, source: str) -> str:
        """Get emoji based on source"""
        source_lower = source.lower()
        
        if "reddit" in source_lower:
            return "🔥"
        elif "hacker news" in source_lower:
            return "📰"
        elif "product hunt" in source_lower:
            return "🚀"
        elif "techcrunch" in source_lower:
            return "📱"
        elif "openai" in source_lower:
            return "🤖"
        elif "anthropic" in source_lower:
            return "🧠"
        elif "there's an ai" in source_lower:
            return "🛠️"
        else:
            return "✨"
    
    def send_news_batch(self, processed_items: List[dict], delay: float = 3.0) -> int:
        """Send multiple news items with delay between them"""
        sent_count = 0
        
        for item in processed_items:
            message = self.format_news_message(item)
            
            # Telegram has 4096 char limit - split if needed
            if len(message) > 4000:
                if self._send_long_message(item):
                    sent_count += 1
                    print(f"Sent (split): {item['original']['title'][:50]}...")
                else:
                    print(f"Failed to send: {item['original']['title'][:50]}...")
            else:
                if self.send_message(message):
                    sent_count += 1
                    print(f"Sent: {item['original']['title'][:50]}...")
                else:
                    print(f"Failed to send: {item['original']['title'][:50]}...")
            
            time.sleep(delay)
        
        return sent_count
    
    def _send_long_message(self, processed_item: dict) -> bool:
        """Send a long message in multiple parts"""
        original = processed_item["original"]
        processed = processed_item["processed"]
        
        emoji = self._get_source_emoji(original["source"])
        title = self._clean_html(processed.get("hebrew_title") or original["title"])
        
        # Part 1: Title + Summary + Bottom line
        part1 = []
        part1.append(f"{emoji} <b>{title}</b>")
        part1.append("")
        part1.append("📋 <b>סיכום מפורט:</b>")
        part1.append(self._clean_html(processed.get("summary", "")))
        part1.append("")
        part1.append(f"💡 <b>שורה תחתונה:</b>")
        part1.append(self._clean_html(processed.get("bottom_line", "")))
        
        success1 = self.send_message("\n".join(part1))
        time.sleep(1)
        
        # Part 2: Video Script + Link
        part2 = []
        part2.append(f"🎬 <b>תסריט לסרטון (דקה) - {title}:</b>")
        part2.append("")
        part2.append(self._clean_html(processed.get("video_script", "")))
        part2.append("")
        part2.append("─" * 25)
        part2.append(f"📰 מקור: {original['source']}")
        part2.append(f"🔗 <a href=\"{original['url']}\">לקריאה המלאה</a>")
        
        success2 = self.send_message("\n".join(part2))
        
        return success1 and success2
    
    def send_summary(self, total_collected: int, total_sent: int) -> bool:
        """Send a summary message"""
        message = f"""📊 <b>סיכום עדכון חדשות AI</b>

נאספו: {total_collected} חדשות
נשלחו: {total_sent} חדשות חדשות

⏰ העדכון הבא בעוד 4 שעות"""
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """Test the bot connection"""
        try:
            response = requests.get(
                f"{self.api_url}/getMe",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    bot_name = data["result"]["username"]
                    print(f"✅ Connected to bot: @{bot_name}")
                    return True
            
            print(f"❌ Connection failed: {response.text}")
            return False
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
