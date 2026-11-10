from __future__ import annotations

import re
from urllib.parse import urlsplit


URL_PATTERN = re.compile(r"https?://[^\s<>\x00-\x1f\"'`]+", re.IGNORECASE)
MAX_TEXT_LENGTH = 20_000


def extract_links(text: str = "") -> dict:
    if not isinstance(text, str) or not text.strip():
        return {"error": "invalid_text", "message": "Provide a non-empty string."}
    if len(text) > MAX_TEXT_LENGTH:
        return {"error": "text_too_long", "message": f"Use at most {MAX_TEXT_LENGTH} characters."}

    urls = {}
    for match in URL_PATTERN.finditer(text):
        url = match.group().rstrip(".,;:!?")
        for opening, closing in (("(", ")"), ("[", "]"), ("{", "}")):
            while url.endswith(closing) and url.count(closing) > url.count(opening):
                url = url[:-1]
        try:
            parsed = urlsplit(url)
            if parsed.hostname and not parsed.username and parsed.password is None:
                urls[url] = {"title": parsed.hostname, "url": url, "source": parsed.hostname}
        except ValueError:
            continue

    if not urls:
        return {"error": "no_links", "message": "No HTTP or HTTPS links were found."}
    return {"tool": "extract_links", "items": list(urls.values()), "count": len(urls)}
