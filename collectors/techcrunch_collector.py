"""
אוסף חדשות AI מ-TechCrunch
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict

class TechCrunchCollector:
    """אוסף חדשות AI מ-TechCrunch"""

    def __init__(self):
        """מאתחל את TechCrunch collector"""
        # RSS feed של TechCrunch לנושא AI
        self.rss_url = "https://techcrunch.com/tag/artificial-intelligence/feed/"

    def collect(self, hours_back: int = 4) -> List[Dict]:
        """
        אוסף חדשות AI חדשות מ-TechCrunch

        Args:
            hours_back: כמה שעות אחורה לאסוף

        Returns:
            רשימה של חדשות
        """
        news_items = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        try:
            print("📡 אוסף מ-TechCrunch AI...")

            # אוסף את ה-RSS feed
            feed = feedparser.parse(self.rss_url)

            for entry in feed.entries:
                try:
                    # מנתח זמן פרסום
                    if hasattr(entry, 'published_parsed'):
                        post_time = datetime(*entry.published_parsed[:6])
                    else:
                        continue

                    # בודק אם חדש מספיק
                    if post_time < cutoff_time:
                        continue

                    title = entry.get('title', '')
                    description = entry.get('summary', '')

                    news_items.append({
                        'title': title,
                        'url': entry.get('link', ''),
                        'source': 'TechCrunch',
                        'created_at': post_time,
                        'text': description[:500],
                        'id': f'tc_{entry.get("id", entry.get("link", ""))}'
                    })

                except Exception as e:
                    print(f"⚠️ שגיאה בעיבוד פריט מ-TechCrunch: {e}")
                    continue

        except Exception as e:
            print(f"❌ שגיאה באיסוף מ-TechCrunch: {e}")

        print(f"✅ נאספו {len(news_items)} חדשות מ-TechCrunch")
        return news_items
