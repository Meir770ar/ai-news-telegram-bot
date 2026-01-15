#!/usr/bin/env python3
"""
AI News Telegram Bot - Main Script
Collects AI news from web + Gmail newsletters, translates to Hebrew, sends to Telegram
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from src.collectors import collect_all_news, NewsItem
from src.gmail_collector import collect_from_gmail
from src.translator import GeminiTranslator
from src.telegram_sender import TelegramSender
from src.tracker import ArticleTracker


def main():
    """Main function - collect, process, and send news"""
    print("=" * 50)
    print("🤖 AI News Bot Starting...")
    print("=" * 50)
    
    # Validate configuration
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set")
        sys.exit(1)
    
    if not config.TELEGRAM_CHAT_ID:
        print("❌ Error: TELEGRAM_CHAT_ID not set")
        sys.exit(1)
    
    if not config.GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY not set")
        sys.exit(1)
    
    # Initialize components
    tracker = ArticleTracker(config.SENT_ARTICLES_FILE)
    translator = GeminiTranslator(config.GEMINI_API_KEY)
    telegram = TelegramSender(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
    
    # Test Telegram connection
    print("\n📡 Testing Telegram connection...")
    if not telegram.test_connection():
        print("❌ Failed to connect to Telegram")
        sys.exit(1)
    
    # Step 1: Collect from web sources
    print("\n📰 Collecting news from web sources...")
    all_news = collect_all_news(config)
    
    # Step 2: Collect from Gmail newsletters
    if config.GMAIL_ADDRESS and config.GMAIL_APP_PASSWORD:
        print("\n📬 Collecting from Gmail newsletters...")
        newsletter_items = collect_from_gmail(
            config.GMAIL_ADDRESS,
            config.GMAIL_APP_PASSWORD,
            days_back=config.NEWSLETTER_DAYS_BACK
        )
        
        # Convert newsletter items to NewsItem format
        for item in newsletter_items:
            news_item = NewsItem(
                title=item.title,
                url=item.url,
                source=item.source,
                description=item.description,
                score=item.score
            )
            news_item.is_tool = True
            all_news.insert(0, news_item)  # Add at beginning (priority)
        
        print(f"📬 Added {len(newsletter_items)} newsletter items")
    else:
        print("\n📬 Gmail not configured, skipping newsletters")
    
    print(f"\n📊 Total collected: {len(all_news)} items")
    
    if not all_news:
        print("ℹ️ No news found. Exiting.")
        return
    
    # Step 3: Filter out already sent items
    print("\n🔍 Filtering duplicates...")
    new_news = tracker.filter_new(all_news)
    print(f"📊 New items: {len(new_news)} (filtered {len(all_news) - len(new_news)} duplicates)")
    
    if not new_news:
        print("ℹ️ No new news to send. Exiting.")
        return
    
    # Limit to top 10 items (newsletters get priority)
    new_news = new_news[:10]
    print(f"📊 Processing top {len(new_news)} items")
    
    # Step 4: Process with Gemini (translate + generate content)
    print("\n🔄 Processing with Gemini AI...")
    processed_news = translator.process_batch(new_news, delay=4.0)
    print(f"📊 Successfully processed: {len(processed_news)} items")
    
    if not processed_news:
        print("❌ Failed to process any news items")
        return
    
    # Step 5: Send to Telegram
    print("\n📤 Sending to Telegram...")
    sent_count = telegram.send_news_batch(processed_news, delay=3.0)
    print(f"📊 Sent: {sent_count} messages")
    
    # Step 6: Mark as sent
    sent_ids = [item["original"]["id"] for item in processed_news]
    tracker.mark_batch_sent(sent_ids)
    
    # Step 7: Send summary
    print("\n📊 Sending summary...")
    telegram.send_summary(len(all_news), sent_count)
    
    # Cleanup old entries
    tracker.cleanup_old()
    
    print("\n" + "=" * 50)
    print("✅ AI News Bot Completed Successfully!")
    print(f"📊 Collected: {len(all_news)} | Sent: {sent_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()
