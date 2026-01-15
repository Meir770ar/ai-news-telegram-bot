"""
מתרגם חדשות AI לעברית ומוסיף רעיונות לסרטונים
"""
import os
import google.generativeai as genai
from typing import Dict, List

class NewsTranslator:
    """מתרגם חדשות לעברית ומוסיף רעיונות לסרטונים"""

    def __init__(self):
        """מאתחל את Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("חסר GEMINI_API_KEY במשתני הסביבה")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def translate_and_enhance(self, news_item: Dict) -> Dict:
        """
        מתרגם פריט חדשות לעברית ומוסיף רעיונות לסרטונים

        Args:
            news_item: דיקשנרי עם מידע על החדשה

        Returns:
            דיקשנרי מעודכן עם תרגום ורעיונות
        """
        title = news_item.get('title', '')
        text = news_item.get('text', '')
        url = news_item.get('url', '')
        source = news_item.get('source', '')

        # בונה את הפרומפט ל-Gemini
        prompt = f"""אתה עוזר שמתרגם חדשות AI לעברית ומוסיף רעיונות לסרטונים.

קיבלת את החדשה הבאה:

כותרת: {title}
מקור: {source}
תוכן: {text[:1000]}

המשימות שלך:

1. תרגם את החדשה לעברית בשפה פשוטה ועממית (2-3 משפטים)
   - השתמש בשפה ישירה וקלה להבנה
   - הימנע ממונחים טכניים מסובכים
   - הסבר מה זה אומר בפועל למשתמש הממוצע

2. הוסף 2-3 רעיונות לסרטוני הדרכה או מדריכים שאפשר ליצור על הנושא הזה
   - כל רעיון צריך להיות קצר (משפט אחד)
   - התמקד ברעיונות מעשיים ושימושיים
   - חשוב על מה שמעניין את הקהל

פורמט התשובה (חשוב מאוד לעקוב אחרי הפורמט הזה בדיוק):

תרגום:
[התרגום שלך כאן]

רעיונות:
• [רעיון 1]
• [רעיון 2]
• [רעיון 3]"""

        try:
            # שולח בקשה ל-Gemini API
            response = self.model.generate_content(prompt)

            # מנתח את התשובה
            response_text = response.text

            # מפריד את התרגום והרעיונות
            hebrew_summary = ""
            video_ideas = []

            if "תרגום:" in response_text and "רעיונות:" in response_text:
                parts = response_text.split("רעיונות:")
                hebrew_summary = parts[0].replace("תרגום:", "").strip()

                ideas_text = parts[1].strip()
                # מחלץ את הרעיונות
                for line in ideas_text.split("\n"):
                    line = line.strip()
                    if line.startswith("•") or line.startswith("-"):
                        idea = line.lstrip("•-").strip()
                        if idea:
                            video_ideas.append(idea)

            # מעדכן את פריט החדשות
            news_item['hebrew_summary'] = hebrew_summary or "לא ניתן לתרגם את החדשה"
            news_item['video_ideas'] = video_ideas[:3]  # מקסימום 3 רעיונות

            print(f"✅ תורגם: {title[:50]}...")

        except Exception as e:
            print(f"❌ שגיאה בתרגום: {e}")
            # ערכים ברירת מחדל במקרה של שגיאה
            news_item['hebrew_summary'] = f"חדשה על: {title}"
            news_item['video_ideas'] = []

        return news_item

    def translate_batch(self, news_items: List[Dict]) -> List[Dict]:
        """
        מתרגם מספר פריטי חדשות

        Args:
            news_items: רשימת פריטי חדשות

        Returns:
            רשימה מעודכנת עם תרגומים
        """
        print(f"\n🔄 מתרגם {len(news_items)} פריטים לעברית...")

        translated_items = []
        for i, item in enumerate(news_items, 1):
            print(f"מתרגם {i}/{len(news_items)}...", end=" ")
            translated = self.translate_and_enhance(item)
            translated_items.append(translated)

        print(f"\n✅ סיים תרגום של {len(translated_items)} פריטים")
        return translated_items
