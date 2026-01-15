# ⚡ התחלה מהירה - 5 דקות להפעלת הבוט

## 🎯 מה צריך כדי להתחיל?

שני דברים בלבד:
1. **ANTHROPIC_API_KEY** (מפתח Claude)
2. **TELEGRAM_CHAT_ID** (ה-ID שלך בטלגרם)

יש לך כבר את הטוקן של הבוט: `8127197113:AAE-jwO1z77G1z8FN5Oxj0ujWTuZXmzUlKU`

---

## 📋 צ'קליסט מהיר

- [ ] קבלת Chat ID מטלגרם
- [ ] קבלת Claude API Key
- [ ] הוספת שני הסודות ל-GitHub
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

## 2️⃣ קבלת Claude API Key (3 דקות)

### צעדים:

1. **גש ל:** https://console.anthropic.com/
2. **הירשם** (עם Google או Email)
3. **הוסף כרטיס אשראי** (דרוש, אבל יש קרדיט חינמי!)
4. **לחץ על API Keys → Create Key**
5. **העתק את המפתח** (מתחיל ב-`sk-ant-api03-...`)

⚠️ **חשוב:** המפתח מוצג רק פעם אחת - העתק אותו מיד!

💰 **עלות:** ~$1-2 לחודש (יש $5-10 קרדיט חינמי בהתחלה!)

✅ **סיימת!** יש לך את ה-API Key

📖 [מדריך מפורט →](./GET_ANTHROPIC_KEY.md)

---

## 3️⃣ הוספת הסודות ל-GitHub (1 דקה)

1. **לך ל:** https://github.com/Meir770ar/ai-news-telegram-bot/settings/secrets/actions

2. **הוסף סוד ראשון:**
   - לחץ **New repository secret**
   - שם: `ANTHROPIC_API_KEY`
   - ערך: המפתח שקיבלת מ-Anthropic (כל המחרוזת)
   - לחץ **Add secret**

3. **הוסף סוד שני:**
   - לחץ **New repository secret** שוב
   - שם: `TELEGRAM_CHAT_ID`
   - ערך: המספר שקיבלת מטלגרם
   - לחץ **Add secret**

4. **(אופציונלי) הוסף את טוקן הבוט:**
   - שם: `TELEGRAM_BOT_TOKEN`
   - ערך: `8127197113:AAE-jwO1z77G1z8FN5Oxj0ujWTuZXmzUlKU`

✅ **סיימת!** כל הסודות במקום

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
