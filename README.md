# 🤖 AI News Telegram Bot

סוכן Python שאוסף חדשות AI אוטומטית ושולח אותן לטלגרם בעברית עם רעיונות לסרטונים.

## 🔥 מה הבוט עושה?

1. **אוסף חדשות חמות** מעולם ה-AI מ-6 מקורות מובילים:
   - 🔴 Reddit (r/artificial, r/OpenAI, r/MachineLearning, r/ChatGPT)
   - 🚀 Product Hunt (מוצרי AI חדשים)
   - 🟠 Hacker News (סטוריז על AI)
   - 📰 TechCrunch AI
   - 🤖 OpenAI Blog
   - 🧠 Anthropic News

2. **מתרגם לעברית** בשפה פשוטה ועממית עם Claude API

3. **מוסיף 2-3 רעיונות** לסרטוני הדרכה/מדריכים לכל חדשה

4. **שולח לטלגרם** בפורמט מעוצב עם אמוג'ים

5. **רץ אוטומטית** כל 4 שעות ב-GitHub Actions (חינמי!)

6. **מונע כפילויות** - לא שולח אותה חדשה פעמיים

## 📋 דרישות

- חשבון GitHub (חינמי)
- API Key של Claude (Anthropic)
- בוט טלגרם + Chat ID
- (אופציונלי) Reddit API credentials

## 🚀 התקנה - שלב אחר שלב

### שלב 1: יצירת בוט טלגרם

1. פתח שיחה עם [@BotFather](https://t.me/botfather) בטלגרם
2. שלח את הפקודה: `/newbot`
3. בחר שם לבוט (למשל: "AI News Bot")
4. בחר username (חייב להסתיים ב-bot, למשל: `my_ai_news_bot`)
5. שמור את ה-**Token** שקיבלת

### שלב 2: קבלת Chat ID

**אופציה 1 - שיחה אישית:**
1. שלח הודעה כלשהי לבוט שלך
2. גש ל: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. חפש את השדה `"chat":{"id":123456789}`
4. זה ה-Chat ID שלך

**אופציה 2 - קבוצה/ערוץ:**
1. הוסף את הבוט לקבוצה/ערוץ
2. תן לו הרשאות לשלוח הודעות
3. שלח הודעה כלשהי בקבוצה
4. גש ל: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. שמור את ה-Chat ID (יתחיל ב-מינוס אם זה קבוצה)

### שלב 3: קבלת Claude API Key

1. גש ל-[Anthropic Console](https://console.anthropic.com/)
2. צור חשבון או התחבר
3. לך ל-**API Keys**
4. צור מפתח חדש
5. שמור את ה-API Key (מתחיל ב-`sk-ant-...`)

### שלב 4: (אופציונלי) Reddit API

אם אתה רוצה גישה מלאה ל-Reddit:

1. גש ל-[Reddit Apps](https://www.reddit.com/prefs/apps)
2. לחץ על "create another app..."
3. בחר "script"
4. שמור את ה-`client_id` (מתחת ל-"personal use script")
5. שמור את ה-`client_secret`

**הערה:** הבוט יעבוד גם בלי Reddit API, אבל עם מגבלות יותר מחמירות.

### שלב 5: הגדרת GitHub Secrets

1. עלה את הפרויקט ל-GitHub (או עשה Fork)
2. לך ל: **Settings → Secrets and variables → Actions**
3. לחץ על **New repository secret**
4. הוסף את הסודות הבאים:

| שם המשתנה | ערך | חובה? |
|----------|-----|-------|
| `ANTHROPIC_API_KEY` | המפתח שקיבלת מ-Anthropic | ✅ חובה |
| `TELEGRAM_BOT_TOKEN` | הטוקן של הבוט מ-BotFather | ✅ חובה |
| `TELEGRAM_CHAT_ID` | ה-Chat ID שלך | ✅ חובה |
| `REDDIT_CLIENT_ID` | (אופציונלי) | ❌ אופציונלי |
| `REDDIT_CLIENT_SECRET` | (אופציונלי) | ❌ אופציונלי |

### שלב 6: הפעלת GitHub Actions

1. לך ל-**Actions** בריפו שלך
2. אשר שאתה רוצה להפעיל Workflows
3. הבוט יתחיל לרוץ אוטומטית כל 4 שעות!

### שלב 7: בדיקה ידנית (אופציונלי)

אם אתה רוצה לבדוק שהכל עובד מיד:

1. לך ל-**Actions**
2. בחר ב-**Collect AI News**
3. לחץ על **Run workflow**
4. הבוט יתחיל לרוץ מיד!

## 🎯 מבנה הפרויקט

```
ai-news-telegram-bot/
├── collectors/              # מודולים לאיסוף חדשות
│   ├── reddit_collector.py
│   ├── producthunt_collector.py
│   ├── hackernews_collector.py
│   ├── techcrunch_collector.py
│   └── blogs_collector.py
├── translator.py            # תרגום עם Claude API
├── telegram_sender.py       # שליחה לטלגרם
├── database.py             # מניעת כפילויות
├── main.py                 # הסקריפט הראשי
├── requirements.txt        # תלויות Python
├── .github/workflows/      # GitHub Actions
│   └── collect-news.yml
└── README.md              # המדריך הזה
```

## 🧪 הרצה מקומית (לפיתוח)

אם אתה רוצה לבדוק מקומית:

```bash
# 1. שכפל את הריפו
git clone https://github.com/YOUR_USERNAME/ai-news-telegram-bot.git
cd ai-news-telegram-bot

# 2. צור סביבה וירטואלית
python -m venv venv
source venv/bin/activate  # ב-Windows: venv\Scripts\activate

# 3. התקן תלויות
pip install -r requirements.txt

# 4. צור קובץ .env
cp .env.example .env

# 5. ערוך את .env והכנס את המפתחות שלך
nano .env

# 6. הרץ את הבוט
python main.py
```

## 📱 פורמט ההודעות

כל הודעה תכלול:

```
🔥 כותרת החדשה באנגלית

תקציר בעברית פשוטה (2-3 משפטים)

💡 רעיונות לסרטונים:
• רעיון 1
• רעיון 2
• רעיון 3

🔗 קרא עוד
```

## ⚙️ התאמה אישית

### שינוי תדירות ההרצה

ערוך את `.github/workflows/collect-news.yml`:

```yaml
schedule:
  - cron: '0 */4 * * *'  # כל 4 שעות
  # דוגמאות:
  # - cron: '0 */2 * * *'  # כל 2 שעות
  # - cron: '0 8,12,16,20 * * *'  # ב-8, 12, 16, 20
  # - cron: '0 9 * * *'  # כל יום ב-9 בבוקר
```

### שינוי מספר החדשות המקסימלי

ערוך `main.py`, שורה 97:

```python
max_items = 10  # שנה למספר שאתה רוצה
```

### הוספת מקורות נוספים

1. צור קובץ חדש ב-`collectors/`
2. הוסף אותו ל-`collectors/__init__.py`
3. הוסף קריאה אליו ב-`main.py`

## 🐛 פתרון בעיות

### הבוט לא שולח הודעות

1. בדוק שה-Token נכון: שלח GET ל-`https://api.telegram.org/bot<TOKEN>/getMe`
2. בדוק שהבוט לא חסום בשיחה
3. בדוק שה-Chat ID נכון

### שגיאות תרגום

1. בדוק שיש לך קרדיט ב-Anthropic
2. בדוק שה-API Key תקין
3. בדוק את ה-Logs ב-GitHub Actions

### GitHub Actions לא רץ

1. וודא ש-Actions מופעל בהגדרות הריפו
2. בדוק שכל ה-Secrets מוגדרים נכון
3. נסה להריץ ידנית דרך "Run workflow"

### אין חדשות חדשות

זה תקין! אם לא היו חדשות ב-4 השעות האחרונות, הבוט פשוט לא ישלח כלום.

## 💰 עלויות

- **GitHub Actions**: חינמי לגמרי (2,000 דקות/חודש)
- **Telegram Bot**: חינמי לגמרי
- **Claude API**: ~$0.01-0.05 לכל הרצה (תלוי במספר החדשות)
  - בממוצע: ~$1-2 לחודש

**סה"כ**: כ-$1-2 לחודש בלבד!

## 📊 סטטיסטיקות

הבוט שומר סטטיסטיקות ב-`sent_items.json`:
- כמה פריטים נשלחו
- מאיזה מקור
- מתי נשלחו

## 🔒 אבטחה

- כל ה-API Keys שמורים כ-GitHub Secrets (מוצפנים)
- הקוד לא שומר סיסמאות או מידע רגיש
- מסד הנתונים (JSON) נשמר ב-GitHub Artifacts בלבד

## 🤝 תרומה לפרויקט

רוצה לתרום? מעולה!

1. עשה Fork לפרויקט
2. צור branch חדש: `git checkout -b feature/amazing-feature`
3. עשה commit: `git commit -m 'Add amazing feature'`
4. דחוף: `git push origin feature/amazing-feature`
5. פתח Pull Request

## 📝 רישיון

MIT License - אתה יכול להשתמש בזה בחופשיות!

## 💬 תמיכה

יש בעיה? רוצה עזרה? פתח Issue ב-GitHub!

---

**נוצר עם ❤️ בעזרת Claude**
