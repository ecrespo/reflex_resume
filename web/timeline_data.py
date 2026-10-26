"""Certifications timeline data for silverpoint's `sp_timeline` (Knight Lab TimelineJS).

`assets/timeline.json` stays the single source of truth for the certifications
(see `timeline.md` for the entry format). This module loads it once, at import
time, as TimelineJS' own JSON, and gives every slide a deterministic
`unique_id` so the ids reported by `on_change` resolve back to headlines.
"""

import json
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TIMELINE_JSON = ASSETS / "timeline.json"

# Presentation options passed straight through to `new TL.Timeline(...)`;
# `font` and `theme` are ignored, the silverpoint skin sets both.
certifications_options = {
    "timenav_position": "bottom",
    "timenav_height": 200,
    "timenav_height_percentage": 25,
    "scale_factor": 2,
    "initial_zoom": 2,
    "hash_bookmark": False,
}

_ACCENTS_FROM = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;"
_ACCENTS_TO = "aaaaaeeeeeiiiiooooouuuunc------"
_ACCENTS = str.maketrans(_ACCENTS_FROM, _ACCENTS_TO)


def slugify(text: str) -> str:
    """Slug in the style of TimelineJS' `Util.slugify`."""
    slug = str(text).strip().lower().translate(_ACCENTS)
    slug = re.sub(r"[^a-z0-9 -]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return re.sub(r"^([0-9])", r"_\1", slug)


def _assign_ids(data: dict) -> dict[str, str]:
    """Give every slide without one a unique, headline-based `unique_id`.

    Returns the slide id → headline map used to label the current slide.
    """
    headlines: dict[str, str] = {}
    slides = ([data["title"]] if data.get("title") else []) + data.get("events", [])
    for index, slide in enumerate(slides):
        headline = (slide.get("text") or {}).get("headline") or ""
        slide_id = slide.get("unique_id") or slugify(headline) or f"slide-{index}"
        candidate, counter = slide_id, 2
        while candidate in headlines:
            candidate = f"{slide_id}-{counter}"
            counter += 1
        slide["unique_id"] = candidate
        headlines[candidate] = headline
    return headlines


_DRIVE_FILE = re.compile(r"^https://drive\.google\.com/file/d/([\w-]+)")


def _local_images(data: dict) -> None:
    """Show each Drive certificate from its local copy, linked to the Drive file.

    Drive's preview iframe letterboxes the page on black; the copies in
    `assets/certificates/` come from `utils/fetch_certificates.py`. A slide
    without a local copy keeps the Drive preview.
    """
    for slide in data.get("events", []):
        media = slide.get("media") or {}
        match = _DRIVE_FILE.match(media.get("url", ""))
        if match and (ASSETS / "certificates" / f"{match.group(1)}.jpg").exists():
            media.setdefault("link", media["url"])
            media.setdefault("link_target", "_blank")
            media["url"] = f"/certificates/{match.group(1)}.jpg"


# Certifications, loaded once at import time.
certifications_data: dict = json.loads(TIMELINE_JSON.read_text(encoding="utf-8"))
_local_images(certifications_data)
certification_headlines = _assign_ids(certifications_data)
