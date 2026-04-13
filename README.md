# AI Builder Bot

Telegram bot foydalanuvchi parametrlari asosida frontend sayt yaratadi va ZIP yuboradi.

## Ishlash oqimi
1. `/start`
2. Sayt nomi
3. Sahifa soni (1-5)
4. Sayt turi
5. Dizayn
6. Rang
7. Tasdiqlash
8. AI generation
9. ZIP yuborish

## Local ishga tushirish
```bash
pip install -r requirements.txt
python bot.py
```

## Render
- Blueprint path: `render.yaml`
- Env vars:
  - `TELEGRAM_BOT_TOKEN`
  - `OPENROUTER_API_KEY`
  - `AI_MODEL` (ixtiyoriy)
