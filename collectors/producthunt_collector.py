"""
אוסף מוצרי AI חדשים מ-Product Hunt
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import feedparser

class ProductHuntCollector:
    """אוסף מוצרי AI חדשים מ-Product Hunt"""

    def __init__(self):
        """מאתחל את Product Hunt collector"""
        # נשתמש ב-RSS feed הציבורי של Product Hunt
        self.rss_url = "https://www.producthunt.com/feed"
        # מילות מפתח לזיהוי מוצרי AI
        self.ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'gpt', 'chatbot', 'llm', 'neural', 'deep learning',
            'automation', 'generative', 'openai', 'claude', 'anthropic',
            'nlp', 'computer vision', 'chatgpt', 'midjourney'
        ]

    def _is_ai_related(self, title: str, description: str) -> bool:
        """
        בודק אם מוצר קשור ל-AI

        Args:
            title: כותרת המוצר
            description: תיאור המוצר

        Returns:
            True אם קשור ל-AI
        """
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in self.ai_keywords)

    def collect(self, hours_back: int = 4) -> List[Dict]:
        """
        אוסף מוצרי AI חדשים מ-Product Hunt

        Args:
            hours_back: כמה שעות אחורה לאסוף

        Returns:
            רשימה של מוצרים חדשים
        """
        news_items = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        try:
            print("📡 אוסף מוצרים מ-Product Hunt...")

            # אוסף את ה-RSS feed
            feed = feedparser.parse(self.rss_url)

            for entry in feed.entries:
                try:
                    # מנתח את זמן הפרסום
                    if hasattr(entry, 'published_parsed'):
                        post_time = datetime(*entry.published_parsed[:6])
                    else:
                        continue

                    # בודק אם חדש מספיק
                    if post_time < cutoff_time:
                        continue

                    # בודק אם קשור ל-AI
                    title = entry.get('title', '')
                    description = entry.get('summary', '')

                    if not self._is_ai_related(title, description):
                        continue

                    news_items.append({
                        'title': title,
                        'url': entry.get('link', ''),
                        'source': 'Product Hunt',
                        'created_at': post_time,
                        'text': description[:500],
                        'id': f'ph_{entry.get("id", entry.get("link", ""))}'
                    })

                except Exception as e:
                    print(f"⚠️ שגיאה בעיבוד פריט מ-Product Hunt: {e}")
                    continue

        except Exception as e:
            print(f"❌ שגיאה באיסוף מ-Product Hunt: {e}")

        print(f"✅ נאספו {len(news_items)} מוצרים מ-Product Hunt")
        return news_items
