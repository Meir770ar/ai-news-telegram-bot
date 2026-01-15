"""
Track sent articles to avoid duplicates
"""
import json
import os
from datetime import datetime, timedelta
from typing import Set, List


class ArticleTracker:
    """Track which articles have been sent"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.sent_ids: Set[str] = set()
        self.sent_data: dict = {}
        self._load()
    
    def _load(self):
        """Load sent articles from file"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.sent_data = json.load(f)
                    self.sent_ids = set(self.sent_data.get("ids", []))
            except Exception as e:
                print(f"Error loading tracker: {e}")
                self.sent_ids = set()
                self.sent_data = {}
    
    def _save(self):
        """Save sent articles to file"""
        try:
            self.sent_data["ids"] = list(self.sent_ids)
            self.sent_data["last_updated"] = datetime.utcnow().isoformat()
            
            with open(self.filepath, 'w') as f:
                json.dump(self.sent_data, f, indent=2)
        except Exception as e:
            print(f"Error saving tracker: {e}")
    
    def is_sent(self, article_id: str) -> bool:
        """Check if article was already sent"""
        return article_id in self.sent_ids
    
    def mark_sent(self, article_id: str):
        """Mark article as sent"""
        self.sent_ids.add(article_id)
        self._save()
    
    def mark_batch_sent(self, article_ids: List[str]):
        """Mark multiple articles as sent"""
        for aid in article_ids:
            self.sent_ids.add(aid)
        self._save()
    
    def filter_new(self, items: list) -> list:
        """Filter out already sent items"""
        return [item for item in items if not self.is_sent(item.id)]
    
    def cleanup_old(self, days: int = 7):
        """Remove entries older than X days (to keep file small)"""
        # For simplicity, we just keep the last 1000 entries
        if len(self.sent_ids) > 1000:
            # Keep only last 500
            self.sent_ids = set(list(self.sent_ids)[-500:])
            self._save()
