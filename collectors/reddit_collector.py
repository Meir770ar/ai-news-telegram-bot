"""
אוסף חדשות AI מ-Reddit
"""
import os
import praw
from datetime import datetime, timedelta
from typing import List, Dict

class RedditCollector:
    """אוסף פוסטים חמים מסאברדיטים של AI"""

    def __init__(self):
        """
        מאתחל את Reddit collector.
        אם אין API credentials, עובד במצב ציבורי (מוגבל יותר).
        """
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'AI-News-Bot/1.0')

        # הסאברדיטים שנאסוף מהם
        self.subreddits = ['artificial', 'OpenAI', 'MachineLearning', 'ChatGPT']

        # אתחול Reddit API
        if self.client_id and self.client_secret:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
        else:
            # מצב ציבורי - ללא credentials
            self.reddit = praw.Reddit(
                client_id='',
                client_secret='',
                user_agent=self.user_agent,
                check_for_async=False
            )

    def collect(self, hours_back: int = 4) -> List[Dict]:
        """
        אוסף פוסטים חדשים מכל הסאברדיטים

        Args:
            hours_back: כמה שעות אחורה לאסוף (ברירת מחדל 4)

        Returns:
            רשימה של דיקשנריז עם מידע על כל פוסט
        """
        news_items = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        try:
            for subreddit_name in self.subreddits:
                print(f"📡 אוסף מ-r/{subreddit_name}...")

                try:
                    subreddit = self.reddit.subreddit(subreddit_name)

                    # אוסף את ה-hot posts
                    for post in subreddit.hot(limit=20):
                        # בודק אם הפוסט חדש מספיק
                        post_time = datetime.utcfromtimestamp(post.created_utc)

                        if post_time < cutoff_time:
                            continue

                        # מסנן פוסטים לא רלוונטיים
                        if post.stickied or post.score < 10:
                            continue

                        news_items.append({
                            'title': post.title,
                            'url': post.url if not post.is_self else f"https://reddit.com{post.permalink}",
                            'score': post.score,
                            'source': f'Reddit r/{subreddit_name}',
                            'created_at': post_time,
                            'text': post.selftext[:500] if post.is_self else '',
                            'id': f'reddit_{post.id}'
                        })

                except Exception as e:
                    print(f"⚠️ שגיאה באיסוף מ-r/{subreddit_name}: {e}")
                    continue

        except Exception as e:
            print(f"❌ שגיאה כללית ב-Reddit collector: {e}")

        print(f"✅ נאספו {len(news_items)} פוסטים מ-Reddit")
        return news_items
