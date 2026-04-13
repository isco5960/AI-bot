SYSTEM_PROMPT = """
Siz professional frontend developer va UI/UX dizaynersiz.

Vazifa: to'liq responsive website yaratish.

Talablar:
- HTML, CSS, JS
- 100% o'zbek tilida UI
- zamonaviy dizayn
- mobile responsive
- animatsiyalar

Javobni FAQAT JSON formatda qaytaring:
{
  "index_html": "...",
  "style_css": "...",
  "script_js": "..."
}
""".strip()


def build_site_prompt(site_name: str, pages: list[str], design: str, color: str, site_type: str) -> str:
    return f"""
Quyidagi ma'lumotlar asosida frontend website yarating:

- sayt nomi: {site_name}
- sahifalar: {", ".join(pages)}
- dizayn: {design}
- rang: {color}
- turi: {site_type}

Cheklovlar:
- index.html ichida navbarda barcha sahifalar linki bo'lsin
- style.css va script.js alohida fayl uchun kod yozing
- index.html ichida CSS/JS inline yozmang
- HTML semantik bo'lsin
- barcha matnlar o'zbek tilida bo'lsin
""".strip()
