"""
Configuration settings for AI News Bot
"""
import os

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gmail Configuration (for newsletters)
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# Reddit Subreddits - focused on PRACTICAL AI tools
REDDIT_SUBREDDITS = [
    "ChatGPT",
    "ChatGPTPro",
    "midjourney",
    "StableDiffusion",
    "LocalLLaMA",
    "ClaudeAI",
    "singularity",
    "ArtificialInteligence",
]

# RSS Feeds
RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "Ars Technica AI": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "VentureBeat AI": "https://feeds.feedburner.com/venturebeat/SZYF",
}

# File to track sent articles
SENT_ARTICLES_FILE = "sent_articles.json"

# Maximum articles per source
MAX_ARTICLES_PER_SOURCE = 8

# Newsletter settings
NEWSLETTER_DAYS_BACK = 2
