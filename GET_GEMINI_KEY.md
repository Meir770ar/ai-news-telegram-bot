# 🔑 איך לקבל Gemini API Key מ-Google (חינמי!)

## 🎉 למה Gemini?

- 💰 **לגמרי חינמי!** (15 בקשות לדקה)
- ⚡ מהיר ואיכותי
- 🇮🇱 תומך מצוין בעברית
- 🚀 קל להתקנה

---

## 📋 צעדים מהירים (2 דקות!)

### 1️⃣ גש ל-Google AI Studio

**🔗 לחץ כאן:** https://aistudio.google.com/app/apikey

### 2️⃣ התחבר עם חשבון Google

- השתמש בכל חשבון Google (Gmail, Workspace, וכו')
- לא צריך לשלם כלום!

### 3️⃣ צור API Key

1. לחץ על **"Create API Key"** או **"Get API key"**
2. בחר **"Create API key in new project"** (אם זה הראשון שלך)
3. **העתק את המפתח!** (מתחיל ב-`AIza...`)

```
דוגמה למפתח Gemini:
AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
```

⚠️ **חשוב:** שמור את המפתח במקום בטוח!

---

## ✅ זהו! זה כל מה שצריך!

**לא צריך:**
- ❌ כרטיס אשראי
- ❌ אימות טלפון
- ❌ תשלום

**רק:**
- ✅ חשבון Google
- ✅ 2 דקות

---

## 🔐 הוספה ל-GitHub Secrets

עכשיו תוסיף את המפתח ל-GitHub:

1. **לך ל:** https://github.com/Meir770ar/ai-news-telegram-bot/settings/secrets/actions

2. **לחץ:** "New repository secret"

3. **מלא:**
   - **Name:** `GEMINI_API_KEY`
   - **Value:** המפתח שקיבלת (כל המחרוזת עם `AIza...`)

4. **לחץ:** "Add secret"

---

## 💰 כמה זה עולה?

### תמחור של Gemini (Free Tier):

| פרמטר | חינמי | בתשלום |
|-------|-------|--------|
| בקשות לדקה | 15 | 1000+ |
| בקשות ליום | 1500 | ללא הגבלה |
| עלות | **$0** | מ-$0.35 לכל מיליון טוקנים |

### עבור הבוט שלנו:

- **6 הרצות ביום** (כל 4 שעות)
- **כל הרצה:** ~10 בקשות (תרגום 10 חדשות)
- **סה"כ ביום:** ~60 בקשות
- **עלות:** **$0 - חינמי לגמרי!** 🎉

---

## 📊 מגבלות (Free Tier)

| מגבלה | ערך |
|-------|-----|
| בקשות לדקה | 15 RPM |
| בקשות ליום | 1,500 RPD |
| טוקנים לדקה | 32,000 TPM |
| טוקנים ליום | 50,000 TPD |

**הבוט שלנו משתמש בהרבה פחות מזה!** ✅

---

## 🎯 השוואה: Gemini vs Claude

| מאפיין | Gemini Free | Claude |
|---------|-------------|---------|
| עלות חודשית | **$0** | $1-2 |
| איכות תרגום | מצוין | מצוין |
| מהירות | מהיר | מהיר |
| תמיכה בעברית | מצוין | טוב |
| צריך כרטיס | לא | כן |

---

## ✅ בדיקה שהמפתח עובד

אם רוצה לבדוק שהמפתח עובד:

```bash
curl \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"שלום! איך קוראים לך?"}]}]}' \
  -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

אם קיבלת תשובה - המפתח עובד! 🎉

---

## 🐛 פתרון בעיות

### "Invalid API Key"
- ודא שהעתקת את המפתח המלא
- ודא שהוא מתחיל ב-`AIza`

### "Quota exceeded"
- המתן דקה (מגבלה של 15 בקשות לדקה)
- הבוט שלנו לא אמור להגיע למגבלה הזו

### "API not enabled"
- לך ל-Google Cloud Console
- הפעל את "Generative Language API"

---

## 📚 מידע נוסף

- **תיעוד:** https://ai.google.dev/docs
- **AI Studio:** https://aistudio.google.com/
- **תמחור:** https://ai.google.dev/pricing

---

## 🎉 סיימת!

עכשיו יש לך:
- ✅ Gemini API Key (חינמי!)
- ✅ הוא מוסף ב-GitHub Secrets
- ✅ הבוט מוכן לרוץ!

**זה הכל! הרבה יותר פשוט מ-Claude, נכון?** 😊
