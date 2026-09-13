"""Certifications timeline data for the Knight Lab TimelineJS component.

`assets/timeline.json` stays the single source of truth for the certifications
(see `timeline.md` for the entry format). This module loads it once, at import
time, into the typed model consumed by `reflex-knightlab-timeline`, and mirrors
TimelineJS' own slide-id algorithm so the ids reported by `on_change` can be
resolved back to headlines in Python.
"""

import re
from pathlib import Path

from reflex_knightlab_timeline import TimelineOptions, load_timeline_data

TIMELINE_JSON = Path(__file__).resolve().parent.parent / "assets" / "timeline.json"

# Certifications, loaded and validated once at import time.
certifications_data = load_timeline_data(TIMELINE_JSON)

# Presentation options passed straight through to `new TL.Timeline(...)`.
certifications_options = TimelineOptions(
    timenav_position="bottom",
    timenav_height=200,
    timenav_height_percentage=25,
    scale_factor=2,
    initial_zoom=2,
    hash_bookmark=False,
    default_bg_color={"r": 255, "g": 255, "b": 255},
)

# --------------------------------------------------------------------------- #
# Slide ids
#
# TimelineJS derives a slide's `unique_id` from its headline when the JSON does
# not carry one (TimelineConfig._assignID -> Util.slugify + Util.ensureUniqueKey).
# The two helpers below are a faithful Python port, which lets us turn the
# `on_change` id back into the headline the visitor is looking at.
# --------------------------------------------------------------------------- #

_ACCENTS_FROM = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;"
_ACCENTS_TO = "aaaaaeeeeeiiiiooooouuuunc------"
_ACCENTS = str.maketrans(_ACCENTS_FROM, _ACCENTS_TO)


def slugify(text: str) -> str:
    """Port of TimelineJS' `Util.slugify`."""
    slug = str(text).strip().lower().translate(_ACCENTS)
    slug = re.sub(r"[^a-z0-9 -]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return re.sub(r"^([0-9])", r"_\1", slug)


def _ensure_unique_key(used: dict[str, str], candidate: str) -> str:
    """Port of TimelineJS' `Util.ensureUniqueKey`.

    Only the deterministic branch is reproduced: a headline-less slide gets a
    random id in the browser, which no Python port could predict, so it simply
    keeps its (empty) candidate here and falls back to the raw id at lookup time.
    """
    if not candidate or candidate not in used:
        return candidate

    # Greedy match, as in the original: the root is the whole candidate.
    root = re.match(r"^(.+)(-\d+)?$", candidate).group(1)
    # Lazy match, as in the original: "a-b-2" groups to root "a-b".
    similar = [key for key in used if re.match(r"^(.+?)(-\d+)?$", key).group(1) == root]

    candidate = f"{root}-{len(similar) + 1}"
    counter = len(similar)
    while candidate in similar:
        candidate = f"{root}-{counter}"
        counter += 1
    return candidate


def _headlines_by_slide_id(data) -> dict[str, str]:
    """Map every slide id TimelineJS will generate to its headline."""
    headlines: dict[str, str] = {}
    slides = ([data.title] if data.title is not None else []) + list(data.events)
    for slide in slides:
        headline = getattr(getattr(slide, "text", None), "headline", None) or ""
        slide_id = _ensure_unique_key(headlines, slugify(headline))
        if slide_id:
            headlines[slide_id] = headline
    return headlines


certification_headlines = _headlines_by_slide_id(certifications_data)
