"""The home page (`/`, `/es`): a profile summary and the main projects."""

import reflex as rx
from reflex_silverpoint_react import sp_button, sp_card, sp_statistic, sp_tag, sparkline_rows

from ..home_data import (
    ACTIVITY_SPAN,
    DATA_AS_OF,
    PROFILE_ROLE,
    PROFILE_STATS,
    PROFILE_SUMMARY,
    PROJECT_ACTIVITY,
    PROJECTS,
)
from ..i18n import format_iso_day, localize, pick, t
from .resume_sections import section_heading

_LINK = "text-[#2F6F86] hover:text-[#1F3D36] hover:underline"


def profile_section(lang: str = "en") -> rx.Component:
    """Who I am, in two paragraphs and five figures."""
    return rx.el.section(
        rx.el.h1("Ernesto Crespo", class_name="text-4xl font-bold text-gray-800"),
        rx.el.p(pick(PROFILE_ROLE, lang), class_name="text-xl italic text-gray-600 mt-1 mb-6"),
        *[
            rx.el.p(
                pick(paragraph, lang), class_name="text-gray-700 leading-relaxed mb-4 max-w-3xl"
            )
            for paragraph in PROFILE_SUMMARY
        ],
        rx.el.div(
            *[
                sp_card(
                    sp_statistic(pick(stat["label"], lang), pick(stat["value"], lang)), size="sm"
                )
                for stat in PROFILE_STATS
            ],
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3 mt-6",
        ),
        rx.el.div(
            sp_button(
                t(lang, "Resume", "Currículum"),
                href=localize("/resume", lang),
                label=t(lang, "Open the resume", "Abrir el currículum"),
            ),
            sp_button(
                t(lang, "Dev Dashboard Stats", "Estadísticas de desarrollo"),
                href=localize("/dev-dashboard-stats", lang),
                label=t(lang, "Open the GitHub dashboard", "Abrir el dashboard de GitHub"),
            ),
            sp_button(
                t(lang, "Portfolio", "Portafolio"),
                href=localize("/portfolio", lang),
                label=t(lang, "Open the portfolio", "Abrir el portafolio"),
            ),
            class_name="flex flex-wrap gap-3 mt-6",
        ),
        id="profile",
        class_name="mb-14",
    )


def project_card(project: dict, lang: str = "en", **card_props) -> rx.Component:
    """A project as a card: tagline, facts, links in the header and the stack as tags.

    The Portfolio page's repository cards use it too.
    """
    name = project["name"]
    return sp_card(
        rx.el.p(pick(project["tagline"], lang), class_name="text-gray-700"),
        rx.el.ul(
            *[
                rx.el.li(
                    pick(fact, lang),
                    class_name="text-gray-600 text-sm py-1 border-b border-gray-100",
                )
                for fact in project["facts"]
            ],
            class_name="mt-3",
        ),
        title=name,
        extra=rx.el.div(
            *[
                sp_button(
                    pick(text, lang),
                    href=url,
                    size="sm",
                    label=t(lang, f"{name} on {pick(text, lang)}", f"{name} en {pick(text, lang)}"),
                )
                for text, url in project["links"]
            ],
            class_name="flex gap-2",
        ),
        footer=rx.el.div(
            *[sp_tag(tag, tone=1, size="sm") for tag in project["tags"]],
            class_name="flex flex-wrap gap-2",
            aria_label=t(lang, "Tech stack", "Stack tecnológico"),
        ),
        class_name="h-full",
        **card_props,
    )


def projects_section(lang: str = "en") -> rx.Component:
    """The main projects, then their monthly activity side by side."""
    return rx.el.section(
        section_heading(t(lang, "Main projects", "Proyectos principales")),
        rx.el.div(
            *[project_card(project, lang) for project in PROJECTS],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        rx.el.div(
            sparkline_rows(
                data=PROJECT_ACTIVITY,
                name_key="name",
                series_key="points",
                readout_key="readout",
                title=t(
                    lang,
                    f"Hand-written commits per month, {ACTIVITY_SPAN['en']}",
                    f"Commits escritos a mano por mes, {ACTIVITY_SPAN['es']}",
                ),
                description=t(
                    lang,
                    "One row per main project: its monthly commits and the total.",
                    "Una fila por proyecto principal: sus commits mensuales y el total.",
                ),
                id="projects-activity",
            ),
            class_name="mt-8 w-full",
        ),
        rx.el.p(
            t(
                lang,
                f"Figures as of {format_iso_day(DATA_AS_OF, lang)}, from the git history of "
                "github.com/ecrespo and github.com/prismal-ai. ",
                f"Cifras al {format_iso_day(DATA_AS_OF, lang)}, a partir del historial de git de "
                "github.com/ecrespo y github.com/prismal-ai. ",
            ),
            rx.el.a(
                t(
                    lang,
                    "Explore them on Dev Dashboard Stats",
                    "Explóralas en Estadísticas de desarrollo",
                ),
                href=localize("/dev-dashboard-stats", lang),
                class_name=_LINK,
            ),
            ".",
            class_name="text-sm text-gray-600 mt-4",
        ),
        id="projects",
        class_name="mb-12",
    )
