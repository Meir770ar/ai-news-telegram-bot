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
        
        prompt = f"""אתה יוצר תוכן ישראלי מנוסה שמתמחה בסרטונים קצרים. 

**המשימה:** קיבלת מידע על כלי/חדשה מעולם ה-AI. עליך ליצור תוכן מפורט ומעמיק.

**מידע שהתקבל:**
- כותרת: {title}
- תיאור: {description}
- מקור: {source}

**פלט נדרש - חייב לכלול את כל הסעיפים הבאים:**

###כותרת_עברית###
[כתוב כותרת קליטה בעברית - קצרה וממוקדת]

###סיכום_מפורט###

🔷 **מה זה בכלל?**
כתוב פסקה של 3-4 משפטים שמסבירה בדיוק מה הכלי/החדשה עושה. הסבר כאילו אתה מדבר עם חבר שלא מכיר את התחום. אל תשתמש במילים טכניות מסובכות.

🔷 **למה זה חדשות גדולות?**
כתוב פסקה של 2-3 משפטים שמסבירה למה זה משמעותי. מה השתנה? למה אנשים צריכים לשים לב?

🔷 **איך זה עובד בפועל?**
כתוב פסקה של 3-4 משפטים עם הסבר טכני פשוט. תן דוגמה קונקרטית לשימוש יום-יומי.

🔷 **מה אפשר לעשות עם זה?**
• שימוש ראשון - [תאר שימוש פרקטי ספציפי]
• שימוש שני - [תאר שימוש פרקטי ספציפי]  
• שימוש שלישי - [תאר שימוש פרקטי ספציפי]

🔷 **למי זה מתאים?**
כתוב 2-3 משפטים - יוצרי תוכן? עסקים קטנים? סטודנטים? מתכנתים? כולם?

🔷 **זמינות בישראל ומחיר**
כתוב 2-3 משפטים - האם זמין בישראל? עברית נתמכת? חינמי או בתשלום? יש גרסת נסיון?

🔷 **יתרונות וחסרונות**
👍 יתרונות: [ציין 2-3 יתרונות עיקריים]
👎 חסרונות: [ציין 1-2 חסרונות אם יש]

###שורה_תחתונה###
[כתוב משפט אחד חזק וברור - המלצה סופית. מתחיל ב: "בשורה התחתונה..."]

###תסריט_וידאו###

**הוק (0:00-0:04):** 
"[כתוב משפט פתיחה דרמטי בעברית מדוברת. משהו כמו: 'תכלס, אם אתה עדיין עושה X ידנית - אתה מפסיד המון זמן']"
[הוראת צילום: קלוז-אפ, אנרגיה גבוהה, הבעה מופתעת]

**הבעיה (0:04-0:12):**
"[תאר את הבעיה שהכלי פותר. השתמש בשפה יום-יומית, לא שיווקית. 'אתה יודע את הרגע שאתה...' או 'כולנו מכירים את זה - כש...']"
[הוראת צילום: B-roll של הבעיה, או תנועות ידיים שמדגימות תסכול]

**הפתרון (0:12-0:30):**
"[הסבר מה הכלי עושה ואיך משתמשים בו. צעד אחר צעד:
'ככה זה עובד - נכנסים ל... לוחצים על... וזהו.'
'בתוך X שניות/דקות אתה מקבל...']"
[הוראת צילום: הקלטת מסך עם חיצים והדגשות. החלף זווית כל 2 שניות]

**הוכחה (0:30-0:45):**
"[הראה תוצאה או דוגמה קונקרטית. 'תראו מה יצא לי...' או 'הנה דוגמה אמיתית...']"
[הוראת צילום: לפני/אחרי, או תוצאה על המסך בפול-סקרין]

**CTA וסיום (0:45-0:60):**
"[סכם למי מתאים ומה הצעד הבא. 'אם אתה X - זה בשבילך. הקישור בביו/בתגובה הראשונה.'
סיים עם טוויסט: 'ואל תגידו שלא סיפרתי לכם' או 'תודו לי אחר כך']"
[הוראת צילום: חזרה לפנים, חיוך, אנרגיה]

**ציון VPS:**
- Clarity (בהירות): X/15
- Curiosity Gap (פער סקרנות): X/20
- Proof (הוכחה): X/10
- Novelty (חדשנות): X/15
- Cultural Fit (התאמה ישראלית): X/10
**סה"כ: XX/70**

---

**כללי כתיבה חובה:**
1. עברית מדוברת - "תכלס", "יאללה", "סבבה", "חבל על הזמן" - לא "לפיכך" או "יתרה מכך"
2. זמן עתיד במקום ציווי - "תלחץ פה" ולא "לחץ כאן"
3. השמט "את" כשאפשר - "תפתח האפליקציה" ולא "תפתח את האפליקציה"
4. אל תישמע כמו תרגום - תישמע כמו בן אדם שמדבר עם חבר
5. לפחות 200 מילים בסיכום המפורט
6. התסריט חייב להיות מפורט עם טיימינג מדויק"""

        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.85,
                        max_output_tokens=4000
                    )
                )
                
                result = self._parse_response(response.text)
                
                # Validate we got real content
                if result.get("summary") and len(result["summary"]) > 200:
                    return result
                else:
                    print(f"    Retry {attempt+1}: Short response ({len(result.get('summary', ''))} chars)")
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

⚠️ **הערה:** העיבוד האוטומטי לא היה זמין כרגע. היכנסו לקישור למידע המלא.""",
            "bottom_line": "בשורה התחתונה: בדקו את הקישור המקורי לפרטים נוספים.",
            "video_script": ""
        }
    
    def _parse_response(self, text: str) -> dict:
        """Parse response with ### markers"""
        result = {
            "hebrew_title": "",
            "summary": "",
            "bottom_line": "",
            "video_script": ""
        }
        
        sections = {
            "כותרת_עברית": "hebrew_title",
            "סיכום_מפורט": "summary", 
            "שורה_תחתונה": "bottom_line",
            "תסריט_וידאו": "video_script"
        }
        
        current_section = None
        current_content = []
        
        for line in text.split('\n'):
            line_stripped = line.strip()
            
            # Check for section markers
            found_section = False
            for marker, field in sections.items():
                if f"###{marker}###" in line_stripped or f"### {marker} ###" in line_stripped:
                    if current_section and current_content:
                        result[current_section] = '\n'.join(current_content).strip()
                    current_section = field
                    current_content = []
                    found_section = True
                    break
            
            if not found_section and current_section:
                if not line_stripped.startswith("###"):
                    current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            result[current_section] = '\n'.join(current_content).strip()
        
        # Cleanup - remove markdown ** from parsed content for cleaner display
        for key in result:
            if result[key]:
                # Keep the structure but clean extra whitespace
                result[key] = result[key].strip()
        
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
        
        # Try to find sections by content
        summary_lines = []
        script_lines = []
        in_script = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect script section
            if "הוק" in line and "0:00" in line:
                in_script = True
            if "ציון VPS" in line:
                in_script = True
            
            if in_script:
                script_lines.append(line)
            elif line.startswith("🔷") or line.startswith("👍") or line.startswith("👎") or line.startswith("•"):
                summary_lines.append(line)
            elif "בשורה התחתונה" in line:
                result["bottom_line"] = line
            elif not result["hebrew_title"] and len(line) < 80 and not line.startswith("#"):
                result["hebrew_title"] = line
            else:
                if not in_script:
                    summary_lines.append(line)
        
        result["summary"] = '\n'.join(summary_lines)
        result["video_script"] = '\n'.join(script_lines)
        
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
