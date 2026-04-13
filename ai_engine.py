import json
import re
import requests
from config import OPENROUTER_API_KEY, AI_MODEL, OPENROUTER_URL
from prompts import SYSTEM_PROMPT


def _extract_json(raw_text: str) -> dict:
    raw_text = raw_text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, flags=re.S | re.I)
    if fenced:
        raw_text = fenced.group(1).strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # JSON obyektning eng katta blokini olish
        match = re.search(r"\{[\s\S]*\}", raw_text, flags=re.S)
        if not match:
            raise ValueError("AI javobidan JSON topilmadi.")
        candidate = match.group(0).strip()
        # Ba'zi modellarda escape qilingan JSON bo'ladi
        if '\\"' in candidate and candidate.startswith('{"'):
            candidate = candidate.replace('\\"', '"')
        return json.loads(candidate)


def generate_site_code(user_prompt: str) -> dict:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY topilmadi.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    models = [AI_MODEL, "x-ai/grok-4-mini", "openai/gpt-4o-mini"]
    token_limits = [900, 600, 400]
    last_error = "Provider returned error"

    for model in models:
        for max_tokens in token_limits:
            payload = {
                "model": model,
                "temperature": 0.4,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            }

            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)
            data = response.json()

            if response.status_code >= 400:
                last_error = data.get("error", {}).get("message", "Noma'lum AI xatolik")
                # Keyingi model/token bilan qayta urinish
                continue

            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            try:
                parsed = _extract_json(text)
            except Exception:
                last_error = "AI javobida toza JSON qaytmadi."
                continue

            if not all(k in parsed for k in ("index_html", "style_css", "script_js")):
                last_error = "AI javobida kerakli fayl maydonlari to'liq emas."
                continue

            return parsed

    raise ValueError(last_error)
