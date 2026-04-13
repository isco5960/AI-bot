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


def write_site_files(base_dir: Path, site_name: str, files: dict) -> Path:
    folder_name = sanitize_name(site_name)
    site_dir = base_dir / folder_name
    site_dir.mkdir(parents=True, exist_ok=True)

    (site_dir / "index.html").write_text(files["index_html"], encoding="utf-8")
    (site_dir / "style.css").write_text(files["style_css"], encoding="utf-8")
    (site_dir / "script.js").write_text(files["script_js"], encoding="utf-8")

    zip_path = base_dir / f"{folder_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in ("index.html", "style.css", "script.js"):
            zf.write(site_dir / fname, arcname=fname)
    return zip_path


def ensure_temp_root() -> Path:
    root = Path(os.getcwd()) / "temp" / "sites"
    root.mkdir(parents=True, exist_ok=True)
    return root
