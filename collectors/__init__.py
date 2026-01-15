"""
מודול לאיסוף חדשות AI ממקורות שונים
"""
from .reddit_collector import RedditCollector
from .producthunt_collector import ProductHuntCollector
from .hackernews_collector import HackerNewsCollector
from .techcrunch_collector import TechCrunchCollector
from .blogs_collector import BlogsCollector

__all__ = [
    'RedditCollector',
    'ProductHuntCollector',
    'HackerNewsCollector',
    'TechCrunchCollector',
    'BlogsCollector'
]
