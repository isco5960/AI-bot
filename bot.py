import traceback
import telebot
from telebot import types

from config import TELEGRAM_BOT_TOKEN
from prompts import build_site_prompt
from ai_engine import generate_site_code
from site_builder import PAGE_MAP, ensure_temp_root, write_site_files

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")
user_state = {}

SITE_TYPES = ["💼 Biznes", "🍔 Restoran", "💇 Sartaroshxona", "🛒 Do'kon", "🧑‍💻 Portfolio"]
DESIGNS = ["⚡ Zamonaviy", "🎯 Minimal", "💎 Luxus", "🌑 Dark"]
COLORS = ["🔵 Ko'k", "⚫ Qora", "🟢 Yashil", "🔴 Qizil", "🟣 Binafsha"]


def kb(rows: list[list[str]]) -> types.ReplyKeyboardMarkup:
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for r in rows:
        m.row(*r)
    return m


def fallback_site_files(st: dict) -> dict:
    site_name = st.get("site_name", "Yangi Sayt")
    color = st.get("color", "🔵 Ko'k")
    color_map = {
        "🔵 Ko'k": "#2563eb",
        "⚫ Qora": "#111827",
        "🟢 Yashil": "#16a34a",
        "🔴 Qizil": "#dc2626",
        "🟣 Binafsha": "#7c3aed",
    }
    main = color_map.get(color, "#2563eb")

    pages = PAGE_MAP.get(st.get("pages_count", 1), ["Home"])
    links = "".join(f'<a href="#{p.lower()}">{p}</a>' for p in pages)
    sections = "".join(
        f'<section id="{p.lower()}" class="card"><h2>{p}</h2><p>{site_name} uchun {p} bo\'limi tayyor.</p></section>'
        for p in pages
    )

    html = f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{site_name}</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header class="hero">
    <h1>{site_name}</h1>
    <p>{st.get("site_type","Sayt")} · {st.get("design","Zamonaviy")} dizayn</p>
    <nav>{links}</nav>
  </header>
  <main>{sections}</main>
  <script src="script.js"></script>
</body>
</html>"""
    css = f"""*{{box-sizing:border-box}}body{{font-family:Arial;margin:0;background:#f8fafc;color:#111827}}.hero{{padding:40px;background:{main};color:#fff}}nav a{{color:#fff;margin-right:12px;text-decoration:none}}main{{padding:20px;display:grid;gap:12px}}.card{{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:16px}}"""
    js = "document.querySelectorAll('nav a').forEach(a=>a.addEventListener('click',()=>console.log('navigate:',a.getAttribute('href'))));"
    return {"index_html": html, "style_css": css, "script_js": js}


@bot.message_handler(commands=["start"])
def on_start(message: types.Message):
    user_state[message.chat.id] = {"step": "start"}
    bot.send_message(
        message.chat.id,
        "👋 Salom! Web sayt yaratamizmi?",
        reply_markup=kb([["🚀 Sayt yaratish", "📖 Qanday ishlaydi?"]]),
    )


@bot.message_handler(func=lambda m: True, content_types=["text"])
def on_text(message: types.Message):
    chat_id = message.chat.id
    text = (message.text or "").strip()
    st = user_state.get(chat_id, {"step": "start"})
    step = st.get("step")

    try:
        if text == "📖 Qanday ishlaydi?":
            bot.send_message(
                chat_id,
                "1) Ma'lumotlarni kiritasiz\n2) AI sayt yaratadi\n3) ZIP qilib yuboraman.",
                reply_markup=kb([["🚀 Sayt yaratish"]]),
            )
            return

        if text == "🔁 Qayta sozlash":
            user_state[chat_id] = {"step": "ask_name"}
            bot.send_message(chat_id, "🏷 Sayt nomini kiriting:")
            return

        if text == "🚀 Sayt yaratish":
            user_state[chat_id] = {"step": "ask_name"}
            bot.send_message(chat_id, "🏷 Sayt nomini kiriting:")
            return

        if step == "ask_name":
            st["site_name"] = text
            st["step"] = "ask_pages"
            user_state[chat_id] = st
            bot.send_message(chat_id, "📄 Nechta sahifa bo'lsin?", reply_markup=kb([["1", "2", "3", "4", "5"]]))
            return

        if step == "ask_pages" and text in {"1", "2", "3", "4", "5"}:
            st["pages_count"] = int(text)
            st["step"] = "ask_type"
            user_state[chat_id] = st
            bot.send_message(chat_id, "🧩 Sayt turi qanday bo'lsin?", reply_markup=kb([SITE_TYPES[:3], SITE_TYPES[3:]]))
            return

        if step == "ask_type" and text in SITE_TYPES:
            st["site_type"] = text
            st["step"] = "ask_design"
            user_state[chat_id] = st
            bot.send_message(chat_id, "🎨 Dizayn uslubi:", reply_markup=kb([DESIGNS[:2], DESIGNS[2:]]))
            return

        if step == "ask_design" and text in DESIGNS:
            st["design"] = text
            st["step"] = "ask_color"
            user_state[chat_id] = st
            bot.send_message(chat_id, "🌈 Asosiy rang:", reply_markup=kb([COLORS[:2], COLORS[2:4], [COLORS[4]]]))
            return

        if step == "ask_color" and text in COLORS:
            st["color"] = text
            st["step"] = "confirm"
            user_state[chat_id] = st
            summary = (
                f"📋 Hammasi tayyormi?\n\n"
                f"🏷 Nomi: {st['site_name']}\n"
                f"📄 Sahifa: {st['pages_count']}\n"
                f"🧩 Turi: {st['site_type']}\n"
                f"🎨 Dizayn: {st['design']}\n"
                f"🌈 Rang: {st['color']}"
            )
            bot.send_message(chat_id, summary, reply_markup=kb([["✅ Yaratish", "🔁 Qayta sozlash"]]))
            return

        if step == "confirm" and text == "✅ Yaratish":
            bot.send_message(chat_id, "⏳ Saytingiz yaratilmoqda...")
            pages = PAGE_MAP[st["pages_count"]]
            prompt = build_site_prompt(
                site_name=st["site_name"],
                pages=pages,
                design=st["design"],
                color=st["color"],
                site_type=st["site_type"],
            )
            try:
                files = generate_site_code(prompt)
            except Exception:
                files = fallback_site_files(st)
            root = ensure_temp_root()
            zip_path = write_site_files(root, st["site_name"], files)
            with open(zip_path, "rb") as f:
                bot.send_document(chat_id, f, caption="📦 Tayyor! Saytingiz ZIP holatda.")

            user_state[chat_id] = {"step": "start"}
            bot.send_message(chat_id, "Yana sayt yaratamizmi?", reply_markup=kb([["🚀 Sayt yaratish", "📖 Qanday ishlaydi?"]]))
            return

        bot.send_message(chat_id, "Avval /start bosing yoki 🚀 Sayt yaratish ni tanlang.")
    except Exception as exc:
        print("Xatolik:", exc)
        traceback.print_exc()
        bot.send_message(chat_id, f"❌ Xatolik yuz berdi: {exc}")


if __name__ == "__main__":
    print("AI Builder Bot ishga tushdi...")
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN topilmadi. Env variable kiriting.")
        raise SystemExit(1)
    bot.infinity_polling(skip_pending=True)


def run_bot() -> None:
    print("AI Builder Bot polling boshlandi...")
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN topilmadi. Bot ishga tushmadi.")
        return
    bot.infinity_polling(skip_pending=True)
