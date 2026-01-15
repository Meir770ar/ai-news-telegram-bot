"""
Translation and content processing using Gemini API
"""
from google import genai
from google.genai import types
from typing import Optional
import time


class GeminiTranslator:
    """Translate and process news using Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self.model = "gemini-2.0-flash"
        
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini client: {e}")
    
    def process_news_item(self, title: str, description: str, source: str, url: str = "", retries: int = 3) -> Optional[dict]:
        """Process a news item with DETAILED content"""
        
        if not self.client:
            return self._fallback_process(title, description, source)
        
        prompt = f"""אתה יוצר תוכן ישראלי מנוסה שמתמחה בסרטונים קצרים (טיקטוק/רילס/שורטס). 

קיבלת מידע על כלי/חדשה מעולם ה-AI:
שם: {title}
מידע: {description}
מקור: {source}

---

**חלק 1: סיכום מפורט (כתוב בפורמט עם פסקאות ובולטים)**

===סיכום===

🔷 **מה זה בכלל?**
[הסבר בפסקה של 2-3 משפטים מה הכלי עושה. כתוב בפשטות כאילו אתה מסביר לחבר.]

🔷 **למה זה מעניין?**
[פסקה שמסבירה למה זה חדשות גדולות ולמה אנשים צריכים לשים לב לזה]

🔷 **איך זה עובד בפועל?**
[פסקה עם הסבר טכני פשוט + דוגמה קונקרטית לשימוש יום-יומי]

🔷 **מה אפשר לעשות עם זה?**
• שימוש 1 - [דוגמה פרקטית]
• שימוש 2 - [דוגמה פרקטית]
• שימוש 3 - [דוגמה פרקטית]

🔷 **למי זה מתאים?**
[פסקה קצרה - יוצרי תוכן? עסקים? סטודנטים? כולם?]

🔷 **זמינות ומחיר**
[האם זמין בישראל? חינמי/בתשלום? יש גרסת נסיון?]

🔷 **יתרונות וחסרונות**
👍 יתרונות: [2-3 יתרונות]
👎 חסרונות: [1-2 חסרונות אם יש]

===שורה_תחתונה===
[משפט אחד חזק וברור - המלצה סופית]

---

**חלק 2: תסריט לסרטון קצר (60 שניות)**

עקוב אחרי הפרוטוקול הזה בדיוק:

**שלב 1 - ניתוח:** הכלי הזה פותר בעיה של [זהה את הכאב/רצון של הצופה הישראלי]

**שלב 2 - הוק (3-5 שניות):**
צור פתיח מבוסס פסיכולוגיה התנהגותית. בחר אחד:
- שנאת הפסד: "אתה מפסיד כסף/זמן כל יום בגלל ש..."
- פער סקרנות: "גיליתי משהו שרוב האנשים לא יודעים..."
- הוכחה חברתית: "הכלי הזה עשה לי X בזמן שלקח לאחרים Y..."
- קונטרה: "כולם חושבים ש... אבל האמת היא..."

===תסריט===

[0:00-0:04] **הוק - תפוס תשומת לב**
"[כתוב משפט פתיחה בעברית מדוברת, דוגרית, שתופס מיד. ללא מילים גבוהות. תכלס.]"
[הוראת צילום: קלוז-אפ על הפנים, אנרגיה גבוהה]

[0:04-0:12] **הבעיה/כאב**
"[תאר את הבעיה שהכלי פותר - בשפה של הצופה, לא שפה שיווקית]"
[הוראת צילום: B-roll של הבעיה או תנועת ידיים]

[0:12-0:30] **הפתרון + הדגמה**
"[הסבר מה הכלי עושה ואיך משתמשים - צעד אחר צעד, פשוט]"
[הוראת צילום: הקלטת מסך עם חיצים/הדגשות, החלפת זווית כל 2 שניות]

[0:30-0:45] **הוכחה/תוצאה**
"[הראה תוצאה אמיתית או דוגמה קונקרטית]"
[הוראת צילום: לפני/אחרי, או תוצאה על המסך]

[0:45-0:55] **למי מתאים + CTA**
"[אמור למי זה מושלם ומה הצעד הבא]"
[הוראת צילום: חזרה לפנים, אנרגיה]

[0:55-0:60] **סיום עם טוויסט**
"[משפט סיום שגורם לצפות שוב או לשתף]"
[הוראת צילום: זום אאוט או אפקט]

**ציון VPS משוער:**
- Clarity (בהירות): X/15
- Curiosity Gap (סקרנות): X/20  
- Proof (הוכחה): X/10
- Novelty (חדשנות): X/15
- Cultural Fit (התאמה ישראלית): X/10
**סה"כ: X/70**

---

כללי כתיבה חובה:
1. עברית מדוברת - "תכלס", "יאללה", "סבבה" - לא "לפיכך" או "יתרה מכך"
2. זמן עתיד במקום ציווי - "תלחץ פה" ולא "לחץ כאן"
3. השמט "את" כשאפשר - "תפתח האפליקציה" ולא "תפתח את האפליקציה"
4. אל תישמע כמו תרגום - תישמע כמו בן אדם שמדבר עם חבר
5. כל משפט צריך להיות קצר וברור"""

        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=3000
                    )
                )
                
                result = self._parse_response_v2(response.text)
                
                # Validate we got real content
                if result.get("summary") and len(result["summary"]) > 150:
                    return result
                else:
                    print(f"    Retry {attempt+1}: Short response")
                    time.sleep(3)
                    continue
                    
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = 10 * (attempt + 1)
                    print(f"    Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"    Error: {str(e)[:80]}")
                    break
        
        return self._fallback_process(title, description, source)
    
    def _fallback_process(self, title: str, description: str, source: str) -> dict:
        """Fallback when Gemini is not available"""
        desc_text = description[:800] if description else "אין תיאור זמין"
        return {
            "hebrew_title": title,
            "summary": f"""🔷 **מה זה?**
{desc_text}

🔷 **זמינות**
בדקו את הקישור המקורי לפרטים על זמינות בישראל ומחירים.

⚠️ העיבוד האוטומטי לא היה זמין - היכנסו לקישור למידע המלא.""",
            "bottom_line": "בדקו את הקישור המקורי לפרטים נוספים.",
            "video_script": ""
        }
    
    def _parse_response_v2(self, text: str) -> dict:
        """Parse response with === markers"""
        result = {
            "hebrew_title": "",
            "summary": "",
            "bottom_line": "",
            "video_script": ""
        }
        
        sections = {
            "כותרת": "hebrew_title",
            "סיכום": "summary", 
            "שורה_תחתונה": "bottom_line",
            "תסריט": "video_script"
        }
        
        current_section = None
        current_content = []
        
        for line in text.split('\n'):
            line_stripped = line.strip()
            
            # Check for section markers
            found_section = False
            for marker, field in sections.items():
                if f"==={marker}===" in line_stripped:
                    if current_section:
                        result[current_section] = '\n'.join(current_content).strip()
                    current_section = field
                    current_content = []
                    found_section = True
                    break
            
            if not found_section and current_section:
                if not line_stripped.startswith("==="):
                    current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            result[current_section] = '\n'.join(current_content).strip()
        
        # Fallback if markers didn't work
        if not result["summary"] or len(result["summary"]) < 100:
            result = self._parse_response_fallback(text)
        
        return result
    
    def _parse_response_fallback(self, text: str) -> dict:
        """Fallback parsing without markers"""
        result = {
            "hebrew_title": "",
            "summary": "",
            "bottom_line": "",
            "video_script": ""
        }
        
        lines = text.strip().split('\n')
        full_text = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("==="):
                full_text.append(line)
        
        if full_text and len(full_text[0]) < 100:
            result["hebrew_title"] = full_text[0]
            full_text = full_text[1:]
        
        if full_text:
            # Split content - first 60% is summary, rest is script
            split_point = int(len(full_text) * 0.6)
            result["summary"] = '\n'.join(full_text[:split_point])
            result["video_script"] = '\n'.join(full_text[split_point:])
        
        return result
    
    def process_batch(self, news_items: list, delay: float = 5.0) -> list:
        """Process multiple news items"""
        processed = []
        
        for i, item in enumerate(news_items):
            print(f"  [{i+1}/{len(news_items)}] {item.title[:45]}...")
            
            result = self.process_news_item(
                title=item.title,
                description=item.description,
                source=item.source,
                url=item.url
            )
            
            if result:
                processed.append({
                    "original": item.to_dict(),
                    "processed": result
                })
            
            time.sleep(delay)
        
        return processed
