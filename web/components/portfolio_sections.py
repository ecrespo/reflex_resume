"""The Portfolio page's "Repositories" section: one card per repository, grouped by category."""

from datetime import date

import reflex as rx
from reflex_silverpoint_react import sp_button, sp_card, sp_tag

from ..repositories_data import CATEGORIES, DATA_AS_OF, REPOSITORIES, YEAR
from .resume_sections import section_heading

_LINK = "text-[#2F6F86] hover:text-[#1F3D36] hover:underline"
_FACT = "text-gray-600 text-sm py-1 border-b border-gray-100"


def _day(iso: str) -> str:
    """`2026-10-24` → `Oct 24, 2026`."""
    day = date.fromisoformat(iso)
    return f"{day:%b} {day.day}, {day.year}"


def _plural(count: int, word: str) -> str:
    return f"{count:,} {word}" if count == 1 else f"{count:,} {word}s"


def _title(repo: dict) -> str:
    return repo["name"] if repo["owner"] == "ecrespo" else f"{repo['owner']}/{repo['name']}"


def _facts(repo: dict) -> list[str]:
    first, last = repo["first"][:4], repo["last"][:4]
    span = first if first == last else f"{first}–{last}"
    if repo["commits_2026"]:
        lead = f"{_plural(repo['commits_2026'], 'commit')} in {YEAR}"
        if repo["commits_total"] > repo["commits_2026"]:
            lead += f" · {repo['commits_total']:,} since {first}"
    else:
        lead = f"{_plural(repo['commits_total'], 'commit')} · active {span}"
    return [lead, f"Last commit {_day(repo['last'])}"]


def _repo_card(repo: dict) -> rx.Component:
    title = _title(repo)
    return sp_card(
        rx.el.p(repo["description"], class_name="text-gray-700"),
        rx.el.ul(
            *[rx.el.li(fact, class_name=_FACT) for fact in _facts(repo)],
            class_name="mt-3",
        ),
        title=title,
        heading_level=4,
        extra=rx.el.div(
            *[
                sp_button(text, href=url, size="sm", label=f"{title} on {text}")
                for text, url in repo["links"]
            ],
            class_name="flex gap-2",
        ),
        footer=rx.el.div(
            *[sp_tag(tag, tone=1, size="sm") for tag in repo["tags"]],
            class_name="flex flex-wrap gap-2",
            aria_label="Tech stack",
        ),
        class_name="h-full",
    )


def _group(category: dict) -> rx.Component:
    repos = [repo for repo in REPOSITORIES if repo["category"] == category["id"]]
    return rx.el.div(
        rx.el.h3(
            category["title"],
            rx.el.span(f" · {len(repos)}", class_name="text-gray-500 font-normal"),
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.div(
            *[_repo_card(repo) for repo in repos],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        id=f"repos-{category['id']}",
        class_name="mb-10 scroll-mt-24",
    )


def _contents() -> rx.Component:
    return rx.el.nav(
        *[
            rx.el.a(
                f"{category['title']} ({sum(r['category'] == category['id'] for r in REPOSITORIES)})",
                href=f"#repos-{category['id']}",
                class_name=_LINK,
            )
            for category in CATEGORIES
        ],
        aria_label="Repository categories",
        class_name="flex flex-wrap gap-x-5 gap-y-2 text-sm mb-8",
    )


def repositories_section() -> rx.Component:
    """Every repository with commits this year, plus the LangChain / LangGraph and EDA work."""
    active = [repo for repo in REPOSITORIES if repo["commits_2026"]]
    commits = sum(repo["commits_2026"] for repo in active)
    return rx.el.section(
        section_heading("Repositories"),
        rx.el.p(
            f"{len(active)} repositories with commits in {YEAR} ({commits:,} hand-written "
            f"commits), plus {len(REPOSITORIES) - len(active)} earlier LangChain, LangGraph and "
            "data-science projects. Figures as of ",
            DATA_AS_OF,
            "; ",
            rx.el.a("see the full picture", href="/dev-dashboard-stats", class_name=_LINK),
            ".",
            class_name="text-gray-700 mb-4 max-w-3xl",
        ),
        _contents(),
        *[_group(category) for category in CATEGORIES],
        id="repositories",
        class_name="mb-12 scroll-mt-24",
    )
