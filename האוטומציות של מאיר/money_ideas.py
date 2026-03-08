"""
מנוע רעיונות להרוויח כסף עם Claude Code / AI
מנתח טרנדים ומייצר רעיונות מעשיים ויצירתיים
"""
from typing import List, Dict, Optional
from trend_tracker import Trend

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class MoneyIdeasGenerator:
    """מייצר רעיונות להרוויח כסף על בסיס טרנדים"""

    def __init__(self, gemini_api_key: str):
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai is required. Install with: pip install google-genai")
        self.client = genai.Client(api_key=gemini_api_key)

    def generate_ideas(self, trends: List[Trend], num_ideas: int = 5) -> List[Dict]:
        """מייצר רעיונות כסף על בסיס טרנדים נוכחיים"""
        if not trends:
            return []

        trends_summary = self._format_trends_for_prompt(trends)
        prompt = self._build_prompt(trends_summary, num_ideas)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return self._parse_ideas(response.text)
        except Exception as e:
            print(f"⚠️ שגיאה ביצירת רעיונות: {e}")
            return []

    def analyze_single_trend(self, trend: Trend) -> Optional[Dict]:
        """מנתח טרנד בודד ומייצר רעיון מפורט"""
        prompt = f"""אתה יועץ עסקי ומומחה טכנולוגי ישראלי. נתח את הטרנד הבא וצור רעיון מפורט להרוויח ממנו כסף באמצעות Claude Code או כלי AI.

טרנד: {trend.title}
מקור: {trend.source}
תיאור: {trend.description}
ציון פופולריות: {trend.score}/10

צור ניתוח בפורמט הבא (בעברית):

💰 שם הרעיון: [שם קצר וקליט]

📋 תיאור: [2-3 משפטים על מה הרעיון]

🛠️ איך לבנות עם Claude Code:
- [צעד 1]
- [צעד 2]
- [צעד 3]

💵 מודל הכנסה: [איך מרוויחים - פרילאנס/SaaS/תוכן/אחר]

⏱️ זמן להקמה: [שעות/ימים]

🎯 פוטנציאל הכנסה חודשית: [טווח ריאלי ב-₪]

⚡ יתרון תחרותי: [למה זה שווה לעשות עכשיו]

🔥 רמת קושי: [קל/בינוני/מאתגר]
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return {
                "trend": trend.to_dict(),
                "analysis": response.text,
            }
        except Exception as e:
            print(f"⚠️ שגיאה בניתוח טרנד: {e}")
            return None

    def _format_trends_for_prompt(self, trends: List[Trend]) -> str:
        """מעצב רשימת טרנדים לפרומפט"""
        lines = []
        for i, trend in enumerate(trends[:15], 1):
            rising = " 📈 עולה!" if trend.rising else ""
            lines.append(
                f"{i}. [{trend.source}] {trend.title} (ציון: {trend.score}/10){rising}"
                f"\n   {trend.description[:100]}"
            )
        return "\n".join(lines)

    def _build_prompt(self, trends_summary: str, num_ideas: int) -> str:
        """בונה את הפרומפט הראשי"""
        return f"""אתה יועץ עסקי מבריק, מומחה בטכנולוגיה ו-AI, ומתמחה בלמצוא הזדמנויות עסקיות.
אתה חושב כמו יזם ישראלי שרוצה להרוויח כסף מהר ובצורה חכמה.

הנה הטרנדים החמים כרגע:

{trends_summary}

בהתבסס על הטרנדים האלה, צור {num_ideas} רעיונות מקוריים ויצירתיים להרוויח כסף באמצעות Claude Code וכלי AI.

דגשים חשובים:
- רעיונות שאפשר להתחיל מיד (לא צריך הון התחלתי גדול)
- שימוש ב-Claude Code לפיתוח מהיר
- מתאים לשוק הישראלי והגלובלי
- רעיונות מעשיים, לא תיאורטיים
- חשוב על ניצול של "חלון הזדמנויות" - מה חם עכשיו

לכל רעיון, כתוב בפורמט הזה (בעברית):

---
💰 רעיון [מספר]: [שם קצר]

📋 מה זה: [משפט אחד]

🛠️ איך בונים עם Claude Code:
• [צעד 1]
• [צעד 2]
• [צעד 3]

💵 איך מרוויחים: [מודל הכנסה]

⏱️ זמן: [כמה זמן לוקח לבנות]

🎯 פוטנציאל: [₪ לחודש]

🔥 למה עכשיו: [למה הטיימינג מושלם]
---

חשוב: תהיה יצירתי ומקורי! לא רעיונות גנריים. תחשוב על זוויות שרוב האנשים מפספסים.
"""

    def _parse_ideas(self, text: str) -> List[Dict]:
        """מפרסר את התשובה לרשימת רעיונות"""
        ideas = []

        # חלוקה לפי "---" או "רעיון"
        sections = text.split("---")
        if len(sections) < 2:
            sections = text.split("💰 רעיון")
            sections = [f"💰 רעיון{s}" for s in sections[1:]] if len(sections) > 1 else [text]

        for section in sections:
            section = section.strip()
            if not section or len(section) < 50:
                continue

            ideas.append({
                "content": section,
                "raw_text": section,
            })

        return ideas


class QuickMoneyIdeas:
    """רעיונות מהירים בלי API - מבוססי תבניות"""

    TEMPLATES = [
        {
            "category": "בוטים",
            "ideas": [
                "בוט טלגרם לניהול הזמנות למסעדות",
                "בוט WhatsApp לתמיכת לקוחות אוטומטית",
                "בוט דיסקורד לניהול קהילות",
                "בוט לתזמון פגישות אוטומטי",
            ]
        },
        {
            "category": "אוטומציות לעסקים",
            "ideas": [
                "מערכת אוטומטית לשליחת הצעות מחיר",
                "אוטומציה של חשבוניות וקבלות",
                "סקרייפר מותאם אישית לניטור מתחרים",
                "מערכת דיוור חכמה עם פרסונליזציה",
            ]
        },
        {
            "category": "כלי AI",
            "ideas": [
                "כלי לכתיבת תיאורי מוצרים לחנויות אונליין",
                "מערכת לייצור תמונות מוצר אוטומטית",
                "כלי לכתיבת פוסטים לרשתות חברתיות",
                "מנתח ביקורות לקוחות אוטומטי",
            ]
        },
        {
            "category": "Micro SaaS",
            "ideas": [
                "כלי לניהול לינקים חכם עם אנליטיקס",
                "דאשבורד לניטור ביצועי SEO",
                "כלי להשוואת מחירים בין ספקים",
                "מערכת ניהול פרויקטים מינימלית",
            ]
        },
    ]

    @classmethod
    def get_template_ideas(cls) -> str:
        """מחזיר רעיונות מתוך תבניות מוכנות"""
        lines = ["💡 רעיונות מהירים להרוויח כסף עם Claude Code:\n"]
        for template in cls.TEMPLATES:
            lines.append(f"📂 {template['category']}:")
            for idea in template["ideas"]:
                lines.append(f"  • {idea}")
            lines.append("")
        return "\n".join(lines)
