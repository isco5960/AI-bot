import json
import re
import requests
from config import OPENROUTER_API_KEY, AI_MODEL, OPENROUTER_URL
from prompts import SYSTEM_PROMPT


def _extract_json(raw_text: str) -> dict:
    raw_text = raw_text.strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_text, flags=re.S)
        if not match:
            raise ValueError("AI javobidan JSON topilmadi.")
        return json.loads(match.group(0))


def generate_site_code(user_prompt: str) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY topilmadi.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": AI_MODEL,
        "temperature": 0.4,
        "max_tokens": 1800,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
    data = response.json()

    if response.status_code >= 400:
        msg = data.get("error", {}).get("message", "Noma'lum AI xatolik")
        raise ValueError(msg)

    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    parsed = _extract_json(text)
    if not all(k in parsed for k in ("index_html", "style_css", "script_js")):
        raise ValueError("AI javobida kerakli fayl maydonlari to'liq emas.")
    return parsed
