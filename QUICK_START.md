# ⚡ התחלה מהירה - 5 דקות להפעלת הבוט

## 🎯 מה צריך כדי להתחיל?

שני דברים בלבד:
1. **GEMINI_API_KEY** (מפתח Google Gemini - חינמי!)
2. **TELEGRAM_CHAT_ID** (ה-ID שלך בטלגרם)

יש לך כבר:
- ✅ בוט טלגרם: `8434612396:AAG9LDLUk69uD3yjxFfx51K225n9WsmnlSw`
- ✅ Chat ID שלך: `533703477`

---

## 📋 צ'קליסט מהיר

- [x] קבלת Chat ID מטלגרם ✅
- [ ] קבלת Gemini API Key (חינמי!)
- [ ] הוספת הסודות ל-GitHub
- [ ] הרצת הבוט!

---

## 1️⃣ קבלת Chat ID (1 דקה)

### הדרך הכי פשוטה:

1. **פתח טלגרם** ושלח הודעה לבוט שלך (כל הודעה)

2. **פתח את הקישור הזה בדפדפן:**
   ```
   https://api.telegram.org/bot8127197113:AAE-jwO1z77G1z8FN5Oxj0ujWTuZXmzUlKU/getUpdates
   ```

3. **חפש את המספר** ליד `"chat":{"id":`

   דוגמה:
   ```json
   "chat": {
     "id": 123456789,  <--- זה!
     "first_name": "שמך"
   }
   ```

4. **שמור את המספר הזה** (לדוגמה: `123456789`)

✅ **סיימת!** יש לך את ה-Chat ID

📖 [מדריך מפורט →](./GET_CHAT_ID.md)

---

## 2️⃣ קבלת Gemini API Key (2 דקות - חינמי!)

### צעדים פשוטים:

1. **גש ל:** https://aistudio.google.com/app/apikey
2. **התחבר** עם חשבון Google (Gmail)
3. **לחץ:** "Create API Key" או "Get API key"
4. **בחר:** "Create API key in new project"
5. **העתק את המפתח** (מתחיל ב-`AIza...`)

```
דוגמה למפתח:
AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
```

💰 **עלות:** **$0 - חינמי לגמרי!** 🎉
- 15 בקשות לדקה
- 1,500 בקשות ליום
- **לא צריך כרטיס אשראי!**

✅ **סיימת!** יש לך את ה-API Key

📖 [מדריך מפורט →](./GET_GEMINI_KEY.md)

---

## 3️⃣ הוספת הסודות ל-GitHub (1 דקה)

1. **לך ל:** https://github.com/Meir770ar/ai-news-telegram-bot/settings/secrets/actions

2. **הוסף 3 secrets:**

   **Secret #1: Gemini API Key**
   - לחץ **New repository secret**
   - Name: `GEMINI_API_KEY`
   - Value: המפתח שקיבלת מ-Google (מתחיל ב-`AIza...`)
   - לחץ **Add secret**

   **Secret #2: Telegram Bot Token**
   - לחץ **New repository secret**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `8434612396:AAG9LDLUk69uD3yjxFfx51K225n9WsmnlSw`
   - לחץ **Add secret**

   **Secret #3: Telegram Chat ID**
   - לחץ **New repository secret**
   - Name: `TELEGRAM_CHAT_ID`
   - Value: `533703477`
   - לחץ **Add secret**

✅ **סיימת!** כל 3 הסודות במקום

---

## 4️⃣ הפעלת הבוט! (30 שניות)

1. **לך ל:** https://github.com/Meir770ar/ai-news-telegram-bot/actions

2. **אשר Workflows** (אם מבקשים)

3. **לחץ על:** "Collect AI News"

4. **לחץ על:** "Run workflow" → "Run workflow"

5. **המתן** 1-2 דקות

6. **בדוק את הטלגרם!** 🎉

---

## ✅ זהו! הבוט רץ!

### מה קורה עכשיו?

- ✅ הבוט **רץ אוטומטית** כל 4 שעות
- ✅ אוסף חדשות AI מ-6 מקורות
- ✅ מתרגם לעברית
- ✅ מוסיף רעיונות לסרטונים
- ✅ שולח לך לטלגרם בפורמט מעוצב

### פורמט ההודעות:

```
🔥 כותרת החדשה

תקציר בעברית פשוטה

💡 רעיונות לסרטונים:
• רעיון 1
• רעיון 2
• רעיון 3

🔗 קרא עוד
```

---

## ⚙️ התאמות (אופציונלי)

### שינוי תדירות:
ערוך `.github/workflows/collect-news.yml`:
```yaml
cron: '0 */2 * * *'  # כל 2 שעות במקום 4
```

### שינוי מספר חדשות:
ערוך `main.py` שורה 97:
```python
max_items = 15  # במקום 10
```

---

## 📊 מעקב

### איפה לראות לוגים?
https://github.com/Meir770ar/ai-news-telegram-bot/actions

### איפה לראות שימוש ב-API?
https://console.anthropic.com/usage

### איפה לעזרה?
[README.md](./README.md) - מדריך מלא

---

## 🐛 בעיות?

### הבוט לא שולח הודעות?
- בדוק שה-Chat ID נכון
- בדוק שהבוט לא חסום בשיחה

### שגיאות תרגום?
- בדוק שיש קרדיט ב-Anthropic
- בדוק שה-API Key נכון

### GitHub Actions לא רץ?
- בדוק שכל ה-Secrets מוגדרים נכון
- בדוק את ה-Logs ב-Actions

---

## 🎉 בהצלחה!

יש שאלות? פתח Issue ב-GitHub!

**נהנה מהבוט? תן ⭐ לפרויקט!**
