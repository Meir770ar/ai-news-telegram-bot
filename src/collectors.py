"""
News collectors from various sources - FOCUSED ON PRACTICAL AI TOOLS
"""
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import re

class NewsItem:
    """Represents a news item"""
    def __init__(self, title: str, url: str, source: str, description: str = "", score: int = 0, is_tool: bool = False):
        self.title = title
        self.url = url
        self.source = source
        self.description = description
        self.score = score
        self.is_tool = is_tool  # Flag for practical tools
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID from URL"""
        return str(hash(self.url))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "description": self.description,
            "score": self.score,
            "is_tool": self.is_tool
        }


def is_practical_content(title: str, description: str = "") -> bool:
    """Check if content is about practical AI tools/features"""
    text = (title + " " + description).lower()
    
    # Practical keywords - things users can actually USE
    practical_keywords = [
        "tool", "app", "release", "launch", "feature", "update",
        "free", "api", "plugin", "extension", "how to", "tutorial",
        "tips", "trick", "workflow", "productivity", "generator",
        "image", "video", "audio", "writing", "code", "assistant",
        "bot", "create", "make", "build", "use", "try", "new",
        "midjourney", "dall-e", "stable diffusion", "chatgpt",
        "claude", "gemini", "copilot", "notion", "canva",
        "prompt", "template", "automation", "zapier", "cursor"
    ]
    
    # Skip boring corporate/investment news
    skip_keywords = [
        "lawsuit", "sued", "court", "regulation", "billion dollar",
        "acquisition", "merger", "ipo", "stock", "investor",
        "ceo says", "interview with", "opinion:", "analysis:"
    ]
    
    has_practical = any(kw in text for kw in practical_keywords)
    has_skip = any(kw in text for kw in skip_keywords)
    
    return has_practical and not has_skip


class RedditCollector:
    """Collect posts from Reddit subreddits"""
    
    def __init__(self, subreddits: List[str]):
        self.subreddits = subreddits
        self.base_url = "https://www.reddit.com/r/{}/hot.json"
        self.headers = {"User-Agent": "AI-News-Bot/1.0"}
    
    def collect(self, limit: int = 10) -> List[NewsItem]:
        """Collect hot posts from all subreddits"""
        items = []
        
        for subreddit in self.subreddits:
            try:
                url = self.base_url.format(subreddit)
                response = requests.get(
                    url, 
                    headers=self.headers,
                    params={"limit": 25},  # Get more to filter
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    count = 0
                    for post in posts:
                        if count >= limit:
                            break
                            
                        post_data = post.get("data", {})
                        
                        # Skip stickied posts
                        if post_data.get("stickied"):
                            continue
                        
                        # Only posts from last 48 hours
                        created = post_data.get("created_utc", 0)
                        if datetime.utcnow().timestamp() - created > 172800:
                            continue
                        
                        title = post_data.get("title", "")
                        description = post_data.get("selftext", "")[:500]
                        
                        # Check if practical content
                        is_tool = is_practical_content(title, description)
                        
                        item = NewsItem(
                            title=title,
                            url=f"https://reddit.com{post_data.get('permalink', '')}",
                            source=f"Reddit r/{subreddit}",
                            description=description,
                            score=post_data.get("score", 0),
                            is_tool=is_tool
                        )
                        items.append(item)
                        count += 1
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error collecting from r/{subreddit}: {e}")
        
        # Sort by score, prioritize practical tools
        items.sort(key=lambda x: (x.is_tool, x.score), reverse=True)
        return items


class RSSCollector:
    """Collect news from RSS feeds"""
    
    def __init__(self, feeds: Dict[str, str]):
        self.feeds = feeds
    
    def collect(self, limit: int = 5) -> List[NewsItem]:
        """Collect latest items from RSS feeds"""
        items = []
        
        for source_name, feed_url in self.feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                
                count = 0
                for entry in feed.entries[:20]:  # Check more entries
                    if count >= limit:
                        break
                        
                    # Check if from last 48 hours
                    published = entry.get("published_parsed") or entry.get("updated_parsed")
                    if published:
                        pub_time = datetime(*published[:6])
                        if datetime.utcnow() - pub_time > timedelta(hours=48):
                            continue
                    
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    
                    # Must be AI related
                    ai_keywords = ["ai", "artificial intelligence", "machine learning", 
                                   "gpt", "llm", "neural", "deep learning", "openai",
                                   "anthropic", "claude", "gemini", "chatgpt", "midjourney",
                                   "stable diffusion", "dall-e", "copilot"]
                    
                    text_lower = (title + " " + summary).lower()
                    if not any(kw in text_lower for kw in ai_keywords):
                        continue
                    
                    # Check if practical
                    is_tool = is_practical_content(title, summary)
                    
                    item = NewsItem(
                        title=title,
                        url=entry.get("link", ""),
                        source=source_name,
                        description=self._clean_html(summary)[:500],
                        is_tool=is_tool
                    )
                    items.append(item)
                    count += 1
                    
            except Exception as e:
                print(f"Error collecting from {source_name}: {e}")
        
        # Prioritize practical tools
        items.sort(key=lambda x: x.is_tool, reverse=True)
        return items
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text"""
        clean = re.sub(r'<[^>]+>', '', text)
        return clean.strip()


class HackerNewsCollector:
    """Collect AI-related stories from Hacker News"""
    
    def __init__(self):
        self.api_base = "https://hacker-news.firebaseio.com/v0"
    
    def collect(self, limit: int = 10) -> List[NewsItem]:
        """Collect top AI stories from HN"""
        items = []
        
        try:
            # Get top stories
            response = requests.get(
                f"{self.api_base}/topstories.json",
                timeout=10
            )
            story_ids = response.json()[:150]  # Check more
            
            ai_keywords = ["ai", "artificial intelligence", "machine learning",
                          "gpt", "llm", "neural", "openai", "anthropic", 
                          "claude", "gemini", "chatgpt", "deep learning",
                          "transformer", "diffusion", "midjourney", "copilot"]
            
            for story_id in story_ids:
                if len(items) >= limit:
                    break
                    
                try:
                    story_response = requests.get(
                        f"{self.api_base}/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_response.json()
                    
                    if not story:
                        continue
                    
                    title = story.get("title", "")
                    title_lower = title.lower()
                    
                    # Check if AI related
                    if any(kw in title_lower for kw in ai_keywords):
                        # Check if from last 48 hours
                        created = story.get("time", 0)
                        if datetime.utcnow().timestamp() - created > 172800:
                            continue
                        
                        url = story.get("url", f"https://news.ycombinator.com/item?id={story_id}")
                        
                        is_tool = is_practical_content(title, "")
                        
                        item = NewsItem(
                            title=title,
                            url=url,
                            source="Hacker News",
                            score=story.get("score", 0),
                            is_tool=is_tool
                        )
                        items.append(item)
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Error collecting from Hacker News: {e}")
        
        items.sort(key=lambda x: (x.is_tool, x.score), reverse=True)
        return items


class ProductHuntCollector:
    """Collect AI products from Product Hunt - BEST SOURCE FOR TOOLS"""
    
    def __init__(self):
        self.api_url = "https://api.producthunt.com/v2/api/graphql"
    
    def collect(self, limit: int = 8) -> List[NewsItem]:
        """Collect today's AI products"""
        items = []
        
        try:
            feed_url = "https://www.producthunt.com/feed"
            response = requests.get(feed_url, timeout=10, headers={
                "User-Agent": "AI-News-Bot/1.0"
            })
            
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                
                ai_keywords = ["ai", "artificial intelligence", "gpt", "llm",
                              "machine learning", "chatbot", "automation",
                              "copilot", "assistant", "generate", "creator",
                              "writer", "image", "video", "voice", "audio"]
                
                for entry in feed.entries[:50]:  # Check more
                    title = entry.get("title", "").lower()
                    summary = entry.get("summary", "").lower()
                    
                    if any(kw in title or kw in summary for kw in ai_keywords):
                        item = NewsItem(
                            title=entry.get("title", ""),
                            url=entry.get("link", ""),
                            source="Product Hunt",
                            description=entry.get("summary", "")[:400],
                            is_tool=True  # Product Hunt = always tools
                        )
                        items.append(item)
                        
                        if len(items) >= limit:
                            break
                            
        except Exception as e:
            print(f"Error collecting from Product Hunt: {e}")
        
        return items


class ThereIsAnAICollector:
    """Collect from There's An AI For That - curated AI tools"""
    
    def __init__(self):
        self.url = "https://theresanaiforthat.com/feed/"
    
    def collect(self, limit: int = 5) -> List[NewsItem]:
        """Collect latest AI tools"""
        items = []
        
        try:
            feed = feedparser.parse(self.url)
            
            for entry in feed.entries[:limit]:
                item = NewsItem(
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    source="There's An AI For That",
                    description=entry.get("summary", "")[:400],
                    is_tool=True
                )
                items.append(item)
                
        except Exception as e:
            print(f"Error collecting from There's An AI For That: {e}")
        
        return items


def collect_all_news(config) -> List[NewsItem]:
    """Collect news from all sources - prioritize practical tools"""
    all_items = []
    
    # Product Hunt - BEST for tools
    print("Collecting from Product Hunt...")
    ph = ProductHuntCollector()
    all_items.extend(ph.collect(limit=config.MAX_ARTICLES_PER_SOURCE))
    
    # There's An AI For That
    print("Collecting from There's An AI For That...")
    taift = ThereIsAnAICollector()
    all_items.extend(taift.collect(limit=5))
    
    # Reddit - practical subreddits
    print("Collecting from Reddit...")
    reddit = RedditCollector(config.REDDIT_SUBREDDITS)
    all_items.extend(reddit.collect(limit=config.MAX_ARTICLES_PER_SOURCE))
    
    # RSS Feeds
    print("Collecting from RSS feeds...")
    rss = RSSCollector(config.RSS_FEEDS)
    all_items.extend(rss.collect(limit=config.MAX_ARTICLES_PER_SOURCE))
    
    # Hacker News
    print("Collecting from Hacker News...")
    hn = HackerNewsCollector()
    all_items.extend(hn.collect(limit=config.MAX_ARTICLES_PER_SOURCE))
    
    # Sort: practical tools first, then by score
    all_items.sort(key=lambda x: (x.is_tool, x.score), reverse=True)
    
    print(f"Total collected: {len(all_items)} items ({sum(1 for x in all_items if x.is_tool)} practical tools)")
    return all_items
