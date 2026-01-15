"""
אוסף חדשות AI מ-Hacker News
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict

class HackerNewsCollector:
    """אוסף סטוריז על AI מ-Hacker News"""

    def __init__(self):
        """מאתחל את Hacker News collector"""
        self.api_base = "https://hacker-news.firebaseio.com/v0"
        # מילות מפתח לזיהוי סטוריז של AI
        self.ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'gpt', 'chatbot', 'llm', 'neural', 'deep learning',
            'openai', 'claude', 'anthropic', 'chatgpt', 'gemini',
            'nlp', 'computer vision', 'transformer', 'generative'
        ]

    def _is_ai_related(self, title: str) -> bool:
        """בודק אם כותרת קשורה ל-AI"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.ai_keywords)

    def collect(self, hours_back: int = 4) -> List[Dict]:
        """
        אוסף סטוריז חדשים על AI

        Args:
            hours_back: כמה שעות אחורה לאסוף

        Returns:
            רשימה של סטוריז
        """
        news_items = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        try:
            print("📡 אוסף מ-Hacker News...")

            # אוסף את הסטוריז החמים ביותר
            response = requests.get(f"{self.api_base}/topstories.json", timeout=10)
            story_ids = response.json()[:100]  # ה-100 הראשונים

            for story_id in story_ids:
                try:
                    # מקבל פרטים על הסטורי
                    story_response = requests.get(
                        f"{self.api_base}/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_response.json()

                    if not story or story.get('type') != 'story':
                        continue

                    # בודק זמן
                    post_time = datetime.utcfromtimestamp(story.get('time', 0))
                    if post_time < cutoff_time:
                        continue

                    title = story.get('title', '')

                    # בודק אם קשור ל-AI
                    if not self._is_ai_related(title):
                        continue

                    # בודק שיש מספיק upvotes
                    if story.get('score', 0) < 20:
                        continue

                    news_items.append({
                        'title': title,
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'score': story.get('score', 0),
                        'source': 'Hacker News',
                        'created_at': post_time,
                        'text': story.get('text', '')[:500] if story.get('text') else '',
                        'id': f'hn_{story_id}'
                    })

                except Exception as e:
                    print(f"⚠️ שגיאה בעיבוד סטורי {story_id}: {e}")
                    continue

        except Exception as e:
            print(f"❌ שגיאה באיסוף מ-Hacker News: {e}")

        print(f"✅ נאספו {len(news_items)} סטוריז מ-Hacker News")
        return news_items
