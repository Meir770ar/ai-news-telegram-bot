"""
מודול לאיסוף חדשות AI ממקורות שונים
"""
# Lazy imports to handle missing dependencies gracefully
import sys

__all__ = []

# Always available
try:
    from .reddit_collector import RedditCollector
    __all__.append('RedditCollector')
except ImportError as e:
    print(f"Warning: RedditCollector not available: {e}")

try:
    from .hackernews_collector import HackerNewsCollector
    __all__.append('HackerNewsCollector')
except ImportError as e:
    print(f"Warning: HackerNewsCollector not available: {e}")

# Requires feedparser
try:
    from .producthunt_collector import ProductHuntCollector
    __all__.append('ProductHuntCollector')
except ImportError as e:
    print(f"Warning: ProductHuntCollector not available (needs feedparser): {e}")

try:
    from .techcrunch_collector import TechCrunchCollector
    __all__.append('TechCrunchCollector')
except ImportError as e:
    print(f"Warning: TechCrunchCollector not available (needs feedparser): {e}")

try:
    from .blogs_collector import BlogsCollector
    __all__.append('BlogsCollector')
except ImportError as e:
    print(f"Warning: BlogsCollector not available (needs feedparser): {e}")
