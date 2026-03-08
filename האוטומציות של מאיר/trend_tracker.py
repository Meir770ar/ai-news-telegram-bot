"""
מעקב טרנדים - סריקת טרנדים ממספר מקורות
Google Trends, Reddit, Hacker News, Product Hunt
"""
import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Trend:
    """מייצג טרנד בודד"""
    title: str
    source: str
    url: str = ""
    description: str = ""
    score: int = 0  # פופולריות 1-10
    category: str = ""
    rising: bool = False  # האם הטרנד עולה
    timestamp: str = ""
    keywords: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


class TrendTracker:
    """סורק טרנדים ממקורות שונים"""

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MeirTrendBot/1.0"
        })

    def collect_all_trends(self) -> List[Trend]:
        """אוסף טרנדים מכל המקורות"""
        all_trends = []
        sources = self.config.TREND_SOURCES

        if sources.get("google_trends", {}).get("enabled"):
            print("🔍 סורק Google Trends...")
            all_trends.extend(self._fetch_google_trends())

        if sources.get("reddit", {}).get("enabled"):
            print("🔥 סורק Reddit...")
            all_trends.extend(self._fetch_reddit_trends())

        if sources.get("hacker_news", {}).get("enabled"):
            print("📰 סורק Hacker News...")
            all_trends.extend(self._fetch_hackernews_trends())

        if sources.get("product_hunt", {}).get("enabled"):
            print("🚀 סורק Product Hunt...")
            all_trends.extend(self._fetch_producthunt_trends())

        # מיון לפי ציון
        all_trends.sort(key=lambda t: t.score, reverse=True)

        print(f"📊 סה\"כ נאספו {len(all_trends)} טרנדים")
        return all_trends

    def _fetch_google_trends(self) -> List[Trend]:
        """שולף טרנדים מ-Google Trends (Daily Trends RSS)"""
        trends = []
        try:
            geo = self.config.TREND_SOURCES["google_trends"].get("geo", "IL")
            url = f"https://trends.google.com/trending/rss?geo={geo}"
            response = self.session.get(url, timeout=15)

            if response.status_code == 200:
                # פירוק XML פשוט
                items = re.findall(
                    r"<item>.*?<title>(.+?)</title>.*?<ht:approx_traffic>(.+?)</ht:approx_traffic>.*?</item>",
                    response.text,
                    re.DOTALL,
                )
                for title, traffic in items[:15]:
                    traffic_num = self._parse_traffic(traffic)
                    score = min(10, max(1, traffic_num // 10000))

                    trends.append(Trend(
                        title=title.strip(),
                        source="Google Trends",
                        url=f"https://trends.google.com/trends/explore?q={requests.utils.quote(title.strip())}&geo={geo}",
                        description=f"חיפושים: {traffic}",
                        score=score,
                        category="search_trend",
                        rising=True,
                    ))

            print(f"  ✅ Google Trends: {len(trends)} טרנדים")
        except Exception as e:
            print(f"  ⚠️ Google Trends שגיאה: {e}")

        return trends

    def _parse_traffic(self, traffic_str: str) -> int:
        """ממיר מחרוזת traffic למספר"""
        clean = traffic_str.replace(",", "").replace("+", "").strip()
        try:
            return int(clean)
        except ValueError:
            return 0

    def _fetch_reddit_trends(self) -> List[Trend]:
        """שולף פוסטים חמים מ-Reddit"""
        trends = []
        subreddits = self.config.TREND_SOURCES["reddit"].get("subreddits", [])

        for subreddit in subreddits:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
                response = self.session.get(url, timeout=15)

                if response.status_code != 200:
                    continue

                data = response.json()
                posts = data.get("data", {}).get("children", [])

                for post in posts:
                    post_data = post.get("data", {})
                    ups = post_data.get("ups", 0)

                    # סינון פוסטים עם מעט upvotes
                    if ups < 20:
                        continue

                    score = min(10, max(1, ups // 100))

                    trends.append(Trend(
                        title=post_data.get("title", ""),
                        source=f"Reddit r/{subreddit}",
                        url=f"https://reddit.com{post_data.get('permalink', '')}",
                        description=post_data.get("selftext", "")[:200],
                        score=score,
                        category="community_trend",
                        rising=post_data.get("upvote_ratio", 0) > 0.85,
                    ))

            except Exception as e:
                print(f"  ⚠️ Reddit r/{subreddit}: {e}")

        print(f"  ✅ Reddit: {len(trends)} טרנדים")
        return trends

    def _fetch_hackernews_trends(self) -> List[Trend]:
        """שולף פוסטים פופולריים מ-Hacker News"""
        trends = []
        min_score = self.config.TREND_SOURCES.get("hacker_news", {}).get("min_score", 50)

        try:
            # Top stories
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self.session.get(url, timeout=15)

            if response.status_code != 200:
                return trends

            story_ids = response.json()[:30]

            for story_id in story_ids:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_resp = self.session.get(story_url, timeout=10)

                    if story_resp.status_code != 200:
                        continue

                    story = story_resp.json()
                    if not story:
                        continue

                    hn_score = story.get("score", 0)
                    if hn_score < min_score:
                        continue

                    score = min(10, max(1, hn_score // 50))

                    trends.append(Trend(
                        title=story.get("title", ""),
                        source="Hacker News",
                        url=story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        description=f"Score: {hn_score} | Comments: {story.get('descendants', 0)}",
                        score=score,
                        category="tech_trend",
                        rising=hn_score > 200,
                    ))

                except Exception:
                    continue

            print(f"  ✅ Hacker News: {len(trends)} טרנדים")

        except Exception as e:
            print(f"  ⚠️ Hacker News שגיאה: {e}")

        return trends

    def _fetch_producthunt_trends(self) -> List[Trend]:
        """שולף מוצרים חמים מ-Product Hunt (דרך הדף הראשי)"""
        trends = []
        try:
            url = "https://www.producthunt.com/feed?category=undefined"
            response = self.session.get(url, timeout=15, headers={
                "Accept": "text/html,application/xhtml+xml"
            })

            if response.status_code == 200:
                # חילוץ מוצרים מה-HTML
                products = re.findall(
                    r'data-test="post-name[^"]*"[^>]*>([^<]+)</[^>]+>',
                    response.text
                )
                taglines = re.findall(
                    r'data-test="post-tagline[^"]*"[^>]*>([^<]+)</[^>]+>',
                    response.text
                )

                for i, product in enumerate(products[:10]):
                    tagline = taglines[i] if i < len(taglines) else ""
                    trends.append(Trend(
                        title=product.strip(),
                        source="Product Hunt",
                        url="https://www.producthunt.com",
                        description=tagline.strip(),
                        score=max(1, 8 - i),  # ציון לפי מיקום
                        category="product_launch",
                        rising=i < 3,
                    ))

            print(f"  ✅ Product Hunt: {len(trends)} טרנדים")
        except Exception as e:
            print(f"  ⚠️ Product Hunt שגיאה: {e}")

        return trends


class TrendHistory:
    """מעקב אחרי טרנדים שכבר נשלחו"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.history = self._load()

    def _load(self) -> dict:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"sent": [], "last_run": ""}

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def is_sent(self, trend: Trend) -> bool:
        """בודק אם הטרנד כבר נשלח"""
        key = f"{trend.source}:{trend.title}"
        return key in self.history["sent"]

    def mark_sent(self, trend: Trend):
        """מסמן טרנד כנשלח"""
        key = f"{trend.source}:{trend.title}"
        self.history["sent"].append(key)
        self.history["last_run"] = datetime.now().isoformat()
        self._save()

    def filter_new(self, trends: List[Trend]) -> List[Trend]:
        """מסנן רק טרנדים חדשים"""
        return [t for t in trends if not self.is_sent(t)]

    def cleanup(self, max_items: int = 500):
        """מנקה היסטוריה ישנה"""
        if len(self.history["sent"]) > max_items:
            self.history["sent"] = self.history["sent"][-max_items:]
            self._save()
