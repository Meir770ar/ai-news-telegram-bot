"""
Telegram message sender with beautiful formatting
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
    
    def _clean_text(self, text: str) -> str:
        """Clean text for Telegram - remove HTML tags and special chars"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        
        # Convert ** bold markers to nothing (we'll use emoji instead)
        clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)
        
        # Remove extra whitespace but keep structure
        lines = clean.split('\n')
        cleaned_lines = []
        for line in lines:
            # Keep meaningful lines
            stripped = line.strip()
            if stripped:
                cleaned_lines.append(stripped)
            elif cleaned_lines and cleaned_lines[-1]:
                # Keep one empty line for paragraph breaks
                cleaned_lines.append('')
        
        return '\n'.join(cleaned_lines)
    
    def send_message(self, text: str, disable_preview: bool = True) -> bool:
        """Send a message to the configured chat"""
        try:
            # First try with HTML
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
            
            # If HTML fails, try plain text
            if "can't parse entities" in response.text:
                return self._send_plain_text(text)
            
            print(f"Telegram error: {response.text[:100]}")
            return False
                
        except Exception as e:
            print(f"Error sending to Telegram: {e}")
            return False
    
    def _send_plain_text(self, text: str) -> bool:
        """Send message as plain text (fallback)"""
        try:
            clean_text = re.sub(r'<[^>]+>', '', text)
            
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": clean_text,
                    "disable_web_page_preview": True
                },
                timeout=30
            )
            
            return response.status_code == 200
        except:
            return False
    
    def format_news_message(self, processed_item: dict) -> str:
        """Format a processed news item for Telegram - BEAUTIFUL DETAILED VERSION"""
        original = processed_item["original"]
        processed = processed_item["processed"]
        
        # Get source emoji
        emoji = self._get_source_emoji(original["source"])
        
        # Clean texts
        title = self._clean_text(processed.get("hebrew_title") or original["title"])
        summary = self._clean_text(processed.get("summary", ""))
        bottom_line = self._clean_text(processed.get("bottom_line", ""))
        video_script = self._clean_text(processed.get("video_script", ""))
        
        # Build message parts
        parts = []
        
        # === HEADER ===
        parts.append(f"{emoji} <b>{title}</b>")
        parts.append("")
        parts.append("═══════════════════════════")
        parts.append("")
        
        # === DETAILED SUMMARY ===
        if summary:
            parts.append("📋 <b>סיכום מפורט:</b>")
            parts.append("")
            parts.append(summary)
            parts.append("")
        
        # === BOTTOM LINE ===
        if bottom_line:
            parts.append("━━━━━━━━━━━━━━━━━━━━━━━━")
            parts.append("")
            parts.append(f"💡 <b>שורה תחתונה:</b>")
            parts.append(bottom_line)
            parts.append("")
        
        # === SOURCE AND LINK ===
        parts.append("═══════════════════════════")
        parts.append(f"📰 מקור: {original['source']}")
        url = original.get('url', '')
        if url:
            parts.append(f"🔗 <a href=\"{url}\">לקריאה המלאה</a>")
        
        message = "\n".join(parts)
        
        # Check if need to split (video script separate)
        if video_script and len(message) + len(video_script) > 3800:
            # Will send video script as separate message
            return message
        elif video_script:
            # Add video script to same message
            script_parts = [
                "",
                "━━━━━━━━━━━━━━━━━━━━━━━━",
                "",
                "🎬 <b>תסריט לסרטון (דקה):</b>",
                "",
                video_script
            ]
            message += "\n".join(script_parts)
        
        return message
    
    def format_video_script_message(self, processed_item: dict) -> Optional[str]:
        """Format video script as separate message if too long"""
        processed = processed_item["processed"]
        original = processed_item["original"]
        
        video_script = self._clean_text(processed.get("video_script", ""))
        if not video_script:
            return None
            
        title = self._clean_text(processed.get("hebrew_title") or original["title"])
        
        parts = []
        parts.append(f"🎬 <b>תסריט לסרטון: {title[:40]}...</b>")
        parts.append("")
        parts.append("═══════════════════════════")
        parts.append("")
        parts.append(video_script)
        
        return "\n".join(parts)
    
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
        elif "there's an ai" in source_lower or "theresanai" in source_lower:
            return "🛠️"
        elif "gmail" in source_lower or "newsletter" in source_lower:
            return "📧"
        elif "dharmesh" in source_lower:
            return "💼"
        elif "superhuman" in source_lower:
            return "⚡"
        elif "rundown" in source_lower:
            return "📊"
        elif "ben" in source_lower and "bites" in source_lower:
            return "🍕"
        else:
            return "✨"
    
    def send_news_batch(self, processed_items: List[dict], delay: float = 3.0) -> int:
        """Send multiple news items with delay between them"""
        sent_count = 0
        
        for item in processed_items:
            # Format main message
            message = self.format_news_message(item)
            
            # Check if video script needs separate message
            video_msg = None
            if len(message) < 3500:  # Room for video script
                video_script = self._clean_text(item["processed"].get("video_script", ""))
                if video_script:
                    message += "\n\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    message += "\n🎬 <b>תסריט לסרטון (דקה):</b>\n\n"
                    message += video_script
            else:
                video_msg = self.format_video_script_message(item)
            
            # Send main message
            if len(message) > 4000:
                # Split very long messages
                success = self._send_split_message(item)
            else:
                success = self.send_message(message)
            
            if success:
                sent_count += 1
                print(f"✅ Sent: {item['original']['title'][:50]}...")
                
                # Send separate video script if needed
                if video_msg:
                    time.sleep(1)
                    self.send_message(video_msg)
            else:
                print(f"❌ Failed: {item['original']['title'][:50]}...")
            
            time.sleep(delay)
        
        return sent_count
    
    def _send_split_message(self, processed_item: dict) -> bool:
        """Send a long message in multiple parts"""
        original = processed_item["original"]
        processed = processed_item["processed"]
        
        emoji = self._get_source_emoji(original["source"])
        title = self._clean_text(processed.get("hebrew_title") or original["title"])
        summary = self._clean_text(processed.get("summary", ""))
        bottom_line = self._clean_text(processed.get("bottom_line", ""))
        video_script = self._clean_text(processed.get("video_script", ""))
        
        # Part 1: Title + Summary + Bottom line
        part1 = []
        part1.append(f"{emoji} <b>{title}</b>")
        part1.append("")
        part1.append("═══════════════════════════")
        part1.append("")
        part1.append("📋 <b>סיכום מפורט:</b>")
        part1.append("")
        part1.append(summary)
        part1.append("")
        part1.append("━━━━━━━━━━━━━━━━━━━━━━━━")
        part1.append("")
        part1.append(f"💡 <b>שורה תחתונה:</b>")
        part1.append(bottom_line)
        part1.append("")
        part1.append("═══════════════════════════")
        part1.append(f"📰 מקור: {original['source']}")
        url = original.get('url', '')
        if url:
            part1.append(f"🔗 <a href=\"{url}\">לקריאה המלאה</a>")
        
        success1 = self.send_message("\n".join(part1))
        time.sleep(1)
        
        # Part 2: Video Script (if exists and meaningful)
        success2 = True
        if video_script and len(video_script) > 50:
            part2 = []
            part2.append(f"🎬 <b>תסריט לסרטון: {title[:40]}...</b>")
            part2.append("")
            part2.append("═══════════════════════════")
            part2.append("")
            part2.append(video_script)
            
            success2 = self.send_message("\n".join(part2))
        
        return success1
    
    def send_summary(self, total_collected: int, total_sent: int) -> bool:
        """Send a summary message"""
        message = f"""📊 <b>סיכום עדכון חדשות AI</b>

═══════════════════════════

📥 נאספו: {total_collected} חדשות
📤 נשלחו: {total_sent} חדשות חדשות

⏰ העדכון הבא בעוד 4 שעות

═══════════════════════════
🤖 AI News Bot by @meirarad_bot"""
        
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
