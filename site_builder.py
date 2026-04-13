import os
import zipfile
from pathlib import Path


PAGE_MAP = {
    1: ["Home"],
    2: ["Home", "Gallery"],
    3: ["Home", "Gallery", "About"],
    4: ["Home", "Gallery", "About", "Contact"],
    5: ["Home", "Gallery", "About", "Contact", "Order"],
}


def sanitize_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in name).strip("_") or "site"


COLOR_THEME = {
    "🔵 Ko'k": {"primary": "#2563eb", "secondary": "#1d4ed8", "bg": "#eff6ff"},
    "⚫ Qora": {"primary": "#111827", "secondary": "#1f2937", "bg": "#f3f4f6"},
    "🟢 Yashil": {"primary": "#16a34a", "secondary": "#15803d", "bg": "#ecfdf5"},
    "🔴 Qizil": {"primary": "#dc2626", "secondary": "#b91c1c", "bg": "#fef2f2"},
    "🟣 Binafsha": {"primary": "#7c3aed", "secondary": "#6d28d9", "bg": "#f5f3ff"},
}

PAGE_FILE = {
    "Home": "index.html",
    "Gallery": "gallery.html",
    "About": "about.html",
    "Contact": "contact.html",
    "Order": "order.html",
}


def _nav_links(pages: list[str]) -> str:
    links = []
    for page in pages:
        fname = PAGE_FILE.get(page, "index.html")
        links.append(f'<a href="{fname}">{page}</a>')
    return "\n".join(links)


def _page_content(page: str, site_name: str, site_type: str) -> str:
    if page == "Home":
        return f"""
        <section class="hero">
          <h1>{site_name}</h1>
          <p>{site_type} uchun zamonaviy, responsiv va chiroyli veb-sayt.</p>
          <a class="btn" href="order.html">Buyurtma berish</a>
        </section>
        <section class="cards">
          <article class="card"><h3>Tez xizmat</h3><p>Professional yondashuv va qulay aloqa.</p></article>
          <article class="card"><h3>Zamonaviy dizayn</h3><p>Har qanday qurilmada to'g'ri ishlaydi.</p></article>
          <article class="card"><h3>Ishonchli sifat</h3><p>Brendingizga mos vizual uslub.</p></article>
        </section>
        """
    if page == "Gallery":
        return """
        <section class="section-title"><h2>Galereya</h2><p>Ishlarimizdan namunalar</p></section>
        <section class="gallery-grid">
          <div class="gallery-item">Loyiha 1</div><div class="gallery-item">Loyiha 2</div><div class="gallery-item">Loyiha 3</div>
          <div class="gallery-item">Loyiha 4</div><div class="gallery-item">Loyiha 5</div><div class="gallery-item">Loyiha 6</div>
        </section>
        """
    if page == "About":
        return """
        <section class="section-title"><h2>Biz haqimizda</h2></section>
        <section class="card"><p>Biz mijozlar uchun sifatli va estetik yechimlar yaratamiz. Jamoamiz kreativ va tajribali mutaxassislardan iborat.</p></section>
        """
    if page == "Contact":
        return """
        <section class="section-title"><h2>Aloqa</h2></section>
        <section class="card">
          <p>Telefon: +998 90 123 45 67</p>
          <p>Email: info@example.uz</p>
          <p>Manzil: Toshkent shahri</p>
        </section>
        """
    if page == "Order":
        return """
        <section class="section-title"><h2>Buyurtma</h2></section>
        <section class="card">
          <form id="orderForm" class="form-grid">
            <input type="text" placeholder="Ismingiz" required />
            <input type="tel" placeholder="Telefon raqam" required />
            <textarea placeholder="Buyurtma tafsilotlari"></textarea>
            <button type="submit" class="btn">Yuborish</button>
          </form>
        </section>
        """
    return "<section class='card'><p>Kontent tayyor.</p></section>"


def _build_html(page: str, pages: list[str], site_name: str, site_type: str, design: str) -> str:
    nav = _nav_links(pages)
    content = _page_content(page, site_name, site_type)
    return f"""<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{site_name} | {page}</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body data-design="{design}">
  <header class="topbar">
    <div class="brand">{site_name}</div>
    <nav class="nav">{nav}</nav>
  </header>
  <main class="container">
    {content}
  </main>
  <footer class="footer">© 2026 {site_name}. Barcha huquqlar himoyalangan.</footer>
  <script src="script.js"></script>
</body>
</html>
"""


def _build_css(color: str) -> str:
    theme = COLOR_THEME.get(color, COLOR_THEME["🔵 Ko'k"])
    return f"""*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,Arial,sans-serif;background:{theme["bg"]};color:#111827}}
.topbar{{display:flex;justify-content:space-between;align-items:center;padding:16px 24px;background:linear-gradient(90deg,{theme["primary"]},{theme["secondary"]});color:#fff;position:sticky;top:0}}
.brand{{font-weight:700;font-size:1.1rem}}.nav{{display:flex;gap:12px;flex-wrap:wrap}}.nav a{{color:#fff;text-decoration:none;padding:8px 10px;border-radius:8px}}
.nav a:hover{{background:rgba(255,255,255,.18)}}.container{{max-width:1050px;margin:0 auto;padding:24px}}
.hero{{padding:38px;background:#fff;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08)}}.hero h1{{margin-top:0;font-size:2rem}}
.btn{{display:inline-block;padding:12px 18px;background:{theme["primary"]};color:#fff;border:none;border-radius:10px;text-decoration:none;cursor:pointer;font-weight:700}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:18px}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:14px;padding:18px;box-shadow:0 6px 18px rgba(0,0,0,.05)}}
.section-title h2{{margin-bottom:4px}}.gallery-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.gallery-item{{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;padding:30px;text-align:center}}
.form-grid{{display:grid;gap:10px}}input,textarea{{padding:12px;border:1px solid #d1d5db;border-radius:10px;width:100%}}
.footer{{text-align:center;padding:20px;color:#6b7280}}
@media(max-width:768px){{.cards,.gallery-grid{{grid-template-columns:1fr}}.topbar{{flex-direction:column;align-items:flex-start;gap:10px}}}}
"""


def _build_js() -> str:
    return """document.querySelectorAll('.nav a').forEach(link=>{if(link.getAttribute('href')===location.pathname.split('/').pop())link.style.background='rgba(255,255,255,.25)';});
const orderForm=document.getElementById('orderForm');if(orderForm){orderForm.addEventListener('submit',e=>{e.preventDefault();alert('Buyurtmangiz qabul qilindi!');orderForm.reset();});}"""


def write_site_files(
    base_dir: Path,
    site_name: str,
    pages: list[str],
    site_type: str,
    design: str,
    color: str,
) -> Path:
    folder_name = sanitize_name(site_name)
    site_dir = base_dir / folder_name
    site_dir.mkdir(parents=True, exist_ok=True)

    css = _build_css(color)
    js = _build_js()
    (site_dir / "style.css").write_text(css, encoding="utf-8")
    (site_dir / "script.js").write_text(js, encoding="utf-8")

    for page in pages:
        fname = PAGE_FILE.get(page, "index.html")
        html = _build_html(page, pages, site_name, site_type, design)
        (site_dir / fname).write_text(html, encoding="utf-8")

    zip_path = base_dir / f"{folder_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(site_dir / "style.css", arcname="style.css")
        zf.write(site_dir / "script.js", arcname="script.js")
        for page in pages:
            fname = PAGE_FILE.get(page, "index.html")
            zf.write(site_dir / fname, arcname=fname)
    return zip_path


def ensure_temp_root() -> Path:
    root = Path(os.getcwd()) / "temp" / "sites"
    root.mkdir(parents=True, exist_ok=True)
    return root
