"""The home page (`/`): a profile summary and the main projects."""

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
from .resume_sections import section_heading

_LINK = "text-[#2F6F86] hover:text-[#1F3D36] hover:underline"


def profile_section() -> rx.Component:
    """Who I am, in two paragraphs and five figures."""
    return rx.el.section(
        rx.el.h1("Ernesto Crespo", class_name="text-4xl font-bold text-gray-800"),
        rx.el.p(PROFILE_ROLE, class_name="text-xl italic text-gray-600 mt-1 mb-6"),
        *[
            rx.el.p(paragraph, class_name="text-gray-700 leading-relaxed mb-4 max-w-3xl")
            for paragraph in PROFILE_SUMMARY
        ],
        rx.el.div(
            *[
                sp_card(sp_statistic(stat["label"], stat["value"]), size="sm")
                for stat in PROFILE_STATS
            ],
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3 mt-6",
        ),
        rx.el.div(
            sp_button("Resume", href="/resume", label="Open the resume"),
            sp_button(
                "Dev Dashboard Stats",
                href="/dev-dashboard-stats",
                label="Open the GitHub dashboard",
            ),
            sp_button("Portfolio", href="/portfolio", label="Open the portfolio"),
            class_name="flex flex-wrap gap-3 mt-6",
        ),
        id="profile",
        class_name="mb-14",
    )


def _project_card(project: dict) -> rx.Component:
    return sp_card(
        rx.el.p(project["tagline"], class_name="text-gray-700"),
        rx.el.ul(
            *[
                rx.el.li(fact, class_name="text-gray-600 text-sm py-1 border-b border-gray-100")
                for fact in project["facts"]
            ],
            class_name="mt-3",
        ),
        title=project["name"],
        extra=rx.el.div(
            *[
                sp_button(text, href=url, size="sm", label=f"{project['name']} on {text}")
                for text, url in project["links"]
            ],
            class_name="flex gap-2",
        ),
        footer=rx.el.div(
            *[sp_tag(tag, tone=1, size="sm") for tag in project["tags"]],
            class_name="flex flex-wrap gap-2",
            aria_label="Tech stack",
        ),
        class_name="h-full",
    )


def projects_section() -> rx.Component:
    """The main projects, then their monthly activity side by side."""
    return rx.el.section(
        section_heading("Main projects"),
        rx.el.div(
            *[_project_card(project) for project in PROJECTS],
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        rx.el.div(
            sparkline_rows(
                data=PROJECT_ACTIVITY,
                name_key="name",
                series_key="points",
                readout_key="readout",
                title=f"Hand-written commits per month, {ACTIVITY_SPAN}",
                description="One row per main project: its monthly commits and the total.",
                id="projects-activity",
            ),
            class_name="mt-8 w-full",
        ),
        rx.el.p(
            f"Figures as of {DATA_AS_OF}, from the git history of github.com/ecrespo and "
            "github.com/prismal-ai. ",
            rx.el.a(
                "Explore them on Dev Dashboard Stats", href="/dev-dashboard-stats", class_name=_LINK
            ),
            ".",
            class_name="text-sm text-gray-600 mt-4",
        ),
        id="projects",
        class_name="mb-12",
    )
