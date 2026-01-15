# 🤖 AI News Telegram Bot

בוט שאוסף חדשות AI ממקורות שונים, מתרגם לעברית ושולח לטלגרם כל 4 שעות.

## ✨ מה הבוט עושה?

1. **אוסף חדשות** מ:
   - Reddit (r/artificial, r/OpenAI, r/MachineLearning, r/ChatGPT)
   - Hacker News
   - TechCrunch AI
   - OpenAI Blog
   - Anthropic News
   - Product Hunt (מוצרי AI)

2. **מעבד את החדשות** עם Gemini AI:
   - מתרגם לעברית פשוטה
   - כותב תקציר
   - מציע רעיונות לסרטוני הדרכה

3. **שולח לטלגרם** בפורמט מסודר עם אימוג'ים

---

## 🚀 התקנה מהירה ב-GitHub

### שלב 1: צור ריפו חדש ב-GitHub
1. לך ל-GitHub ולחץ **New Repository**
2. תן שם: `ai-news-telegram-bot`
3. לחץ **Create Repository**

### שלב 2: העלה את הקוד
```bash
# בתיקיית הפרויקט
git remote add origin https://github.com/YOUR_USERNAME/ai-news-telegram-bot.git
git branch -M main
git push -u origin main
```

### שלב 3: הגדר Secrets ב-GitHub
לך להגדרות הריפו → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

הוסף את הסודות הבאים:

| שם | ערך |
|---|---|
| `TELEGRAM_BOT_TOKEN` | הטוקן של הבוט שלך |
| `TELEGRAM_CHAT_ID` | ה-Chat ID שלך |
| `GEMINI_API_KEY` | מפתח Gemini API |

### שלב 4: הפעל!
1. לך ל-**Actions** בריפו
2. לחץ על **AI News Bot**
3. לחץ **Run workflow** → **Run workflow**

הבוט ירוץ אוטומטית כל 4 שעות!

---

## 🔑 איפה משיגים את המפתחות?

### Telegram Bot Token
1. פתח את @BotFather בטלגרם
2. שלח `/newbot`
3. עקוב אחרי ההוראות
4. תקבל טוקן כזה: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Telegram Chat ID
1. פתח את @userinfobot בטלגרם
2. לחץ Start
3. תקבל את ה-ID שלך

### Gemini API Key
1. לך ל: https://aistudio.google.com/app/apikey
2. לחץ **Create API Key**
3. העתק את המפתח

---

## 🖥️ הרצה מקומית

```bash
# התקן את התלויות
pip install -r requirements.txt

# הגדר משתני סביבה
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export GEMINI_API_KEY="your_api_key"

# הרץ
python main.py
```

---

## 📁 מבנה הפרויקט

```
ai-news-telegram-bot/
├── main.py                 # סקריפט ראשי
├── config.py               # הגדרות
├── requirements.txt        # תלויות
├── src/
│   ├── collectors.py       # איסוף חדשות
│   ├── translator.py       # תרגום עם Gemini
│   ├── telegram_sender.py  # שליחה לטלגרם
│   └── tracker.py          # מעקב כפילויות
└── .github/
    └── workflows/
        └── run-bot.yml     # GitHub Actions
```

---

## 📝 פורמט ההודעה

כל הודעה נראית כך:

```
🔥 כותרת החדשה בעברית

תקציר קצר של 2-3 משפטים בעברית פשוטה.

💡 רעיונות לסרטונים:
  1. רעיון ראשון
  2. רעיון שני
  3. רעיון שלישי

📰 מקור: Reddit r/OpenAI
🔗 לקריאה המלאה
```

---

## ⚙️ התאמה אישית

### להוסיף/להסיר מקורות
ערוך את `config.py`:

```python
# Subreddits לעקוב
REDDIT_SUBREDDITS = [
    "artificial",
    "OpenAI",
    # הוסף עוד...
]

# RSS Feeds
RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/...",
    # הוסף עוד...
}
```

### לשנות תדירות
ערוך את `.github/workflows/run-bot.yml`:

```yaml
schedule:
  - cron: '0 */4 * * *'  # כל 4 שעות
  # או:
  - cron: '0 */2 * * *'  # כל 2 שעות
  - cron: '0 8,20 * * *' # פעמיים ביום
```

---

## 🐛 פתרון בעיות

### "API key was reported as leaked"
צור מפתח חדש ב-Google AI Studio

### "Chat not found"
וודא שהתחלת שיחה עם הבוט (שלח `/start`)

### "Rate limit exceeded"
הבוט יחכה אוטומטית, או הפחת את מספר החדשות

---

## 📜 רישיון

MIT - עשה מה שבא לך! 🎉
