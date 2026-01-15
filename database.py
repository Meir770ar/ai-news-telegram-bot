"""
מערכת מעקב אחרי פריטים שכבר נשלחו (למניעת כפילויות)
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Set, Dict

class NewsDatabase:
    """מנהל מסד נתונים פשוט של פריטים שכבר נשלחו"""

    def __init__(self, db_file: str = 'sent_items.json'):
        """
        מאתחל את מסד הנתונים

        Args:
            db_file: שם קובץ מסד הנתונים
        """
        self.db_file = db_file
        self.data = self._load()

    def _load(self) -> Dict:
        """
        טוען את מסד הנתונים מהקובץ

        Returns:
            דיקשנרי עם הנתונים
        """
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ שגיאה בטעינת מסד הנתונים: {e}")
                return {'sent_items': [], 'last_updated': None}
        else:
            return {'sent_items': [], 'last_updated': None}

    def _save(self):
        """שומר את מסד הנתונים לקובץ"""
        try:
            self.data['last_updated'] = datetime.utcnow().isoformat()
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ שגיאה בשמירת מסד הנתונים: {e}")

    def is_sent(self, item_id: str) -> bool:
        """
        בודק אם פריט כבר נשלח

        Args:
            item_id: מזהה הפריט

        Returns:
            True אם כבר נשלח
        """
        sent_items = self.data.get('sent_items', [])
        return any(item['id'] == item_id for item in sent_items)

    def mark_as_sent(self, news_item: Dict):
        """
        מסמן פריט כנשלח

        Args:
            news_item: פריט החדשות
        """
        if 'sent_items' not in self.data:
            self.data['sent_items'] = []

        # מוסיף את הפריט
        self.data['sent_items'].append({
            'id': news_item.get('id'),
            'title': news_item.get('title'),
            'source': news_item.get('source'),
            'sent_at': datetime.utcnow().isoformat()
        })

        # שומר
        self._save()

    def filter_new_items(self, news_items: List[Dict]) -> List[Dict]:
        """
        מסנן רק פריטים חדשים (שעוד לא נשלחו)

        Args:
            news_items: רשימת פריטי חדשות

        Returns:
            רשימה של פריטים חדשים בלבד
        """
        new_items = []
        for item in news_items:
            item_id = item.get('id')
            if item_id and not self.is_sent(item_id):
                new_items.append(item)

        print(f"🔍 סוננו {len(new_items)} פריטים חדשים מתוך {len(news_items)}")
        return new_items

    def cleanup_old_items(self, days: int = 7):
        """
        מנקה פריטים ישנים ממסד הנתונים

        Args:
            days: כמה ימים אחורה לשמור
        """
        if 'sent_items' not in self.data:
            return

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_count = len(self.data['sent_items'])

        # שומר רק פריטים שנשלחו לאחרונה
        self.data['sent_items'] = [
            item for item in self.data['sent_items']
            if datetime.fromisoformat(item['sent_at']) > cutoff_date
        ]

        new_count = len(self.data['sent_items'])
        removed_count = old_count - new_count

        if removed_count > 0:
            print(f"🧹 נוקו {removed_count} פריטים ישנים")
            self._save()

    def get_stats(self) -> Dict:
        """
        מחזיר סטטיסטיקות על מסד הנתונים

        Returns:
            דיקשנרי עם סטטיסטיקות
        """
        sent_items = self.data.get('sent_items', [])
        total_count = len(sent_items)

        # ספירה לפי מקור
        sources = {}
        for item in sent_items:
            source = item.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        return {
            'total_sent': total_count,
            'by_source': sources,
            'last_updated': self.data.get('last_updated')
        }

    def print_stats(self):
        """מדפיס סטטיסטיקות"""
        stats = self.get_stats()
        print("\n📊 סטטיסטיקות מסד נתונים:")
        print(f"   סה\"כ פריטים שנשלחו: {stats['total_sent']}")
        print("   לפי מקור:")
        for source, count in stats['by_source'].items():
            print(f"   - {source}: {count}")
        if stats['last_updated']:
            print(f"   עדכון אחרון: {stats['last_updated']}")
