"""The Portfolio page's "Repositories" section: one card per repository, grouped by category."""

import reflex as rx
from reflex_silverpoint_react import sp_button, sp_card, sp_tag

from ..i18n import format_iso_day, format_number, localize, t
from ..repositories_data import (
    CATEGORIES,
    CATEGORY_TITLES_ES,
    DATA_AS_OF,
    DESCRIPTIONS_ES,
    REPOSITORIES,
    YEAR,
)
from .resume_sections import section_heading

_LINK = "text-[#2F6F86] hover:text-[#1F3D36] hover:underline"
_FACT = "text-gray-600 text-sm py-1 border-b border-gray-100"

_LINK_TEXT = {"Site": {"en": "Site", "es": "Sitio"}}


def _commits(count: int, lang: str) -> str:
    return f"{format_number(count, lang)} commit" + ("" if count == 1 else "s")


def _title(repo: dict) -> str:
    return repo["name"] if repo["owner"] == "ecrespo" else f"{repo['owner']}/{repo['name']}"


def _description(repo: dict, lang: str) -> str:
    if lang == "es":
        return DESCRIPTIONS_ES.get(f"{repo['owner']}/{repo['name']}", repo["description"])
    return repo["description"]


def _category_title(category: dict, lang: str) -> str:
    return (
        CATEGORY_TITLES_ES.get(category["id"], category["title"])
        if lang == "es"
        else category["title"]
    )


def _facts(repo: dict, lang: str) -> list[str]:
    first, last = repo["first"][:4], repo["last"][:4]
    span = first if first == last else f"{first}–{last}"
    if repo["commits_2026"]:
        lead = t(
            lang,
            f"{_commits(repo['commits_2026'], lang)} in {YEAR}",
            f"{_commits(repo['commits_2026'], lang)} en {YEAR}",
        )
        if repo["commits_total"] > repo["commits_2026"]:
            total = format_number(repo["commits_total"], lang)
            lead += t(lang, f" · {total} since {first}", f" · {total} desde {first}")
    else:
        lead = t(
            lang,
            f"{_commits(repo['commits_total'], lang)} · active {span}",
            f"{_commits(repo['commits_total'], lang)} · activo en {span}",
        )
    return [
        lead,
        t(lang, "Last commit ", "Último commit: ") + format_iso_day(repo["last"], lang),
    ]


def _repo_card(repo: dict, lang: str) -> rx.Component:
    title = _title(repo)
    return sp_card(
        rx.el.p(_description(repo, lang), class_name="text-gray-700"),
        rx.el.ul(
            *[rx.el.li(fact, class_name=_FACT) for fact in _facts(repo, lang)],
            class_name="mt-3",
        ),
        title=title,
        heading_level=4,
        extra=rx.el.div(
            *[
                sp_button(
                    _LINK_TEXT.get(text, {}).get(lang, text),
                    href=url,
                    size="sm",
                    label=t(lang, f"{title} on {text}", f"{title} en {text}"),
                )
                for text, url in repo["links"]
            ],
            class_name="flex gap-2",
        ),
        footer=rx.el.div(
            *[sp_tag(tag, tone=1, size="sm") for tag in repo["tags"]],
            class_name="flex flex-wrap gap-2",
            aria_label=t(lang, "Tech stack", "Stack tecnológico"),
        ),
        class_name="h-full",
    )


def _group(category: dict, lang: str) -> rx.Component:
    repos = [repo for repo in REPOSITORIES if repo["category"] == category["id"]]
    return rx.el.div(
        rx.el.h3(
            _category_title(category, lang),
            rx.el.span(f" · {len(repos)}", class_name="text-gray-500 font-normal"),
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.div(
            *[_repo_card(repo, lang) for repo in repos],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        id=f"repos-{category['id']}",
        class_name="mb-10 scroll-mt-24",
    )


def _contents(lang: str) -> rx.Component:
    return rx.el.nav(
        *[
            rx.el.a(
                f"{_category_title(category, lang)} "
                f"({sum(r['category'] == category['id'] for r in REPOSITORIES)})",
                href=f"#repos-{category['id']}",
                class_name=_LINK,
            )
            for category in CATEGORIES
        ],
        aria_label=t(lang, "Repository categories", "Categorías de repositorios"),
        class_name="flex flex-wrap gap-x-5 gap-y-2 text-sm mb-8",
    )


def repositories_section(lang: str = "en") -> rx.Component:
    """Every repository with commits this year, plus the LangChain / LangGraph and EDA work."""
    active = [repo for repo in REPOSITORIES if repo["commits_2026"]]
    commits = format_number(sum(repo["commits_2026"] for repo in active), lang)
    earlier = len(REPOSITORIES) - len(active)
    as_of = format_iso_day(DATA_AS_OF, lang)
    return rx.el.section(
        section_heading(t(lang, "Repositories", "Repositorios")),
        rx.el.p(
            t(
                lang,
                f"{len(active)} repositories with commits in {YEAR} ({commits} hand-written "
                f"commits), plus {earlier} earlier LangChain, LangGraph and data-science "
                f"projects. Figures as of {as_of}; ",
                f"{len(active)} repositorios con commits en {YEAR} ({commits} commits escritos a "
                f"mano), más {earlier} proyectos anteriores de LangChain, LangGraph y ciencia de "
                f"datos. Cifras al {as_of}; ",
            ),
            rx.el.a(
                t(lang, "see the full picture", "mira el panorama completo"),
                href=localize("/dev-dashboard-stats", lang),
                class_name=_LINK,
            ),
            ".",
            class_name="text-gray-700 mb-4 max-w-3xl",
        ),
        _contents(lang),
        *[_group(category, lang) for category in CATEGORIES],
        id="repositories",
        class_name="mb-12 scroll-mt-24",
    )
