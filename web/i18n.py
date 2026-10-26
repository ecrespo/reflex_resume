"""English and Spanish versions of the site.

Every page exists once per language: English at its plain route (`/resume`), the
default, and Spanish under `/es` (`/es/resume`). Each page function takes a
`lang` and builds its text for that language at compile time, so the static
export needs no backend to show either language, and every internal link keeps
the reader in the language they chose. The flags at the end of the sidebar link
each page to its counterpart in the other language.

Text lives next to the code that shows it, as `t(lang, "English", "Español")`;
data modules keep both languages in `{"en": …, "es": …}` values read with `pick`.
"""

from typing import Any, Literal

Lang = Literal["en", "es"]

LANGS: tuple[Lang, ...] = ("en", "es")
DEFAULT_LANG: Lang = "en"

LANG_NAMES = {"en": "English", "es": "Español"}

_PREFIX = {"en": "", "es": "/es"}


def t(lang: str, en: str, es: str) -> str:
    """The text for `lang`: English unless the page is Spanish."""
    return es if lang == "es" else en


def pick(value: Any, lang: str) -> Any:
    """`value[lang]` for a `{"en", "es"}` value; anything else is the same in both."""
    if isinstance(value, dict) and set(value) == {"en", "es"}:
        return value[lang]
    return value


def localize(route: str, lang: str) -> str:
    """The route of an English page in `lang`: `/resume` → `/es/resume`, `/` → `/es`.

    Anchors, external links and files (`/feed.xml`) are left as they are.
    """
    if not route.startswith("/") or lang == DEFAULT_LANG:
        return route
    path, hash_sign, anchor = route.partition("#")
    if "." in path.rsplit("/", 1)[-1]:
        return route
    localized = _PREFIX[lang] + (path if path != "/" else "")
    return localized + hash_sign + anchor


def page_title(lang: str, en: str, es: str) -> str:
    """The browser-tab title of a page."""
    site = t(lang, "Seraph's Resume", "Currículum de Seraph")
    name = t(lang, en, es)
    return site if not name else f"{name} | {site}"


# --------------------------------------------------------------------------- #
# Dates
# --------------------------------------------------------------------------- #

MONTHS_SHORT = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"],
}
MONTHS_LONG = {
    "en": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "es": [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ],
}


def format_day(year: int, month: int, day: int, lang: str, long: bool = False) -> str:
    """`Oct 24, 2026` / `24 oct 2026` (or with the full month name)."""
    months = (MONTHS_LONG if long else MONTHS_SHORT)[lang]
    name = months[month - 1]
    if lang == "es":
        return f"{day} de {name} de {year}" if long else f"{day} {name} {year}"
    return f"{name} {day}, {year}"


def format_iso_day(iso: str, lang: str, long: bool = False) -> str:
    """`2026-10-24` → `Oct 24, 2026` / `24 oct 2026`."""
    year, month, day = (int(part) for part in iso[:10].split("-"))
    return format_day(year, month, day, lang, long)


def format_number(value: int, lang: str) -> str:
    """Thousands with a comma in English and a period in Spanish: 3,119 / 3.119."""
    text = f"{value:,}"
    return text.replace(",", ".") if lang == "es" else text
