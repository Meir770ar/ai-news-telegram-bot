"""
אוסף חדשות מבלוגים רשמיים של חברות AI
"""
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
from bs4 import BeautifulSoup

class BlogsCollector:
    """אוסף מבלוגים רשמיים: OpenAI, Anthropic"""

    def __init__(self):
        """מאתחל את Blogs collector"""
        self.sources = {
            'OpenAI': 'https://openai.com/blog/rss',
            'Anthropic': 'https://www.anthropic.com/news'
        }

    def _collect_from_rss(self, source_name: str, rss_url: str, hours_back: int) -> List[Dict]:
        """
        אוסף מ-RSS feed

        Args:
            source_name: שם המקור
            rss_url: כתובת ה-RSS
            hours_back: כמה שעות אחורה

        Returns:
            רשימת פריטים
        """
        items = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

        try:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries:
                try:
                    # מנתח זמן
                    if hasattr(entry, 'published_parsed'):
                        post_time = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        post_time = datetime(*entry.updated_parsed[:6])
                    else:
                        continue

                    # בודק אם חדש מספיק
                    if post_time < cutoff_time:
                        continue

                    title = entry.get('title', '')
                    description = entry.get('summary', '')

                    items.append({
                        'title': title,
                        'url': entry.get('link', ''),
                        'source': source_name,
                        'created_at': post_time,
                        'text': description[:500],
                        'id': f'{source_name.lower()}_{entry.get("id", entry.get("link", ""))}'
                    })

                except Exception as e:
                    print(f"⚠️ שגיאה בעיבוד פריט מ-{source_name}: {e}")
                    continue

        except Exception as e:
            print(f"❌ שגיאה באיסוף מ-{source_name}: {e}")

        return items

    def _collect_anthropic_news(self, hours_back: int) -> List[Dict]:
        """
        אוסף חדשות מ-Anthropic (אין RSS, נשתמש ב-web scraping פשוט)

        Args:
            hours_back: כמה שעות אחורה

        Returns:
            רשימת פריטים
        """
        items = []

        try:
            print("📡 אוסף מ-Anthropic News...")

            response = requests.get(
                'https://www.anthropic.com/news',
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # מחפש את פוסטי החדשות (הסלקטורים עשויים להשתנות)
                # זה דוגמה בסיסית - ייתכן שצריך להתאים
                articles = soup.find_all('article')[:5]  # 5 הראשונים

                for article in articles:
                    try:
                        title_elem = article.find(['h2', 'h3', 'h4'])
                        link_elem = article.find('a')

                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            url = link_elem.get('href', '')

                            if not url.startswith('http'):
                                url = f"https://www.anthropic.com{url}"

                            items.append({
                                'title': title,
                                'url': url,
                                'source': 'Anthropic',
                                'created_at': datetime.utcnow(),
                                'text': '',
                                'id': f'anthropic_{url}'
                            })

                    except Exception as e:
                        print(f"⚠️ שגיאה בעיבוד פריט מ-Anthropic: {e}")
                        continue

        except Exception as e:
            print(f"❌ שגיאה באיסוף מ-Anthropic: {e}")

        return items

    def collect(self, hours_back: int = 4) -> List[Dict]:
        """
        אוסף מכל הבלוגים

        Args:
            hours_back: כמה שעות אחורה לאסוף

        Returns:
            רשימה של כל הפריטים
        """
        all_items = []

        # אוסף מ-OpenAI RSS
        print("📡 אוסף מ-OpenAI Blog...")
        openai_items = self._collect_from_rss('OpenAI', self.sources['OpenAI'], hours_back)
        all_items.extend(openai_items)

        # אוסף מ-Anthropic
        anthropic_items = self._collect_anthropic_news(hours_back)
        all_items.extend(anthropic_items)

        print(f"✅ נאספו {len(all_items)} פוסטים מבלוגים")
        return all_items
