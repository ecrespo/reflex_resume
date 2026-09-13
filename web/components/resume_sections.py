import reflex as rx
from reflex_knightlab_timeline import timeline

from ..resume_data import (
    education_data,
    portfolio_data,
    skills_data,
    social_media_data,
    work_experience_data,
)
from ..states.certifications_state import CertificationsState
from ..timeline_data import certifications_data, certifications_options


def section_heading(text: str) -> rx.Component:
    return rx.el.h2(
        text,
        class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
    )


def education_section() -> rx.Component:
    return rx.el.section(
        section_heading("Education"),
        rx.el.div(
            rx.el.div(
                rx.el.span(education_data[0], class_name="font-bold text-gray-900 text-lg"),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(education_data[1], class_name="italic text-gray-700"),
                class_name="flex-1",
            ),
            rx.el.span(education_data[2], class_name="text-gray-600 font-medium"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-6",
        ),
        id="education",
        class_name="mb-12 scroll-mt-24",
    )


def experience_item(item: list) -> rx.Component:
    # Built from static Python data (not state Vars), so plain Python conditionals apply.
    title, company, period, responsibilities, tech_stack = item
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(title, class_name="font-bold text-gray-900 text-lg"),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(company, class_name="italic text-gray-700"),
            ),
            rx.el.span(period, class_name="text-gray-600 font-medium whitespace-nowrap"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-baseline mb-3",
        ),
        rx.el.ul(
            *[rx.el.li(r, class_name="mb-1 leading-relaxed") for r in responsibilities],
            class_name="list-disc list-outside ml-5 text-gray-700 mb-4 space-y-1",
        )
        if responsibilities
        else rx.fragment(),
        rx.el.p(
            rx.el.span("Tech Stack: ", class_name="font-semibold text-gray-800"),
            tech_stack,
            class_name="text-sm text-gray-600 bg-gray-100/50 p-3 rounded-lg",
        )
        if tech_stack
        else rx.fragment(),
        class_name="mb-10 last:mb-0",
    )


def work_experience_section() -> rx.Component:
    return rx.el.section(
        section_heading("Work Experience"),
        *[experience_item(item) for item in work_experience_data],
        id="work-experience",
        class_name="mb-12 scroll-mt-24",
    )


def portfolio_section() -> rx.Component:
    """Portfolio section with notebook links."""
    return rx.el.section(
        section_heading("Portfolio"),
        rx.el.h3(
            "Notebooks",
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.h4(
            "EDAs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.foreach(
                portfolio_data["edas"],
                lambda item: rx.el.li(
                    rx.el.a(
                        item[0],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-2",
                ),
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        rx.el.h4(
            "Graphs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.foreach(
                portfolio_data["graphs"],
                lambda item: rx.el.li(
                    rx.el.a(
                        item[0],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-2",
                ),
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        id="portfolio",
        class_name="mb-12 scroll-mt-24",
    )


def skills_list_section() -> rx.Component:
    """Skills list section (text-based)."""

    return rx.el.section(
        section_heading("Skills List"),
        rx.el.div(
            rx.foreach(
                skills_data,
                lambda item: rx.el.div(
                    rx.el.span(f"{item[0]}: ", class_name="font-bold text-gray-800"),
                    rx.el.code(f"{item[1]}", class_name="text-sm text-gray-700"),
                    class_name="mb-3",
                ),
            ),
            class_name="space-y-2",
        ),
        id="skills-list",
        class_name="mb-12 scroll-mt-24",
    )


def social_media_section() -> rx.Component:
    """Social media links section."""
    return rx.el.section(
        section_heading("Social Media"),
        rx.el.div(
            rx.foreach(
                social_media_data,
                lambda item: rx.el.div(
                    rx.el.span(
                        f"{item[0]}: ", class_name="font-semibold text-gray-800 inline-block w-32"
                    ),
                    rx.el.a(
                        item[1],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-3 flex items-start",
                ),
            ),
            class_name="space-y-1",
        ),
        id="social-media",
        class_name="mb-12 scroll-mt-24",
    )


def certifications_section() -> rx.Component:
    """Certifications timeline, rendered by the native Knight Lab component.

    Data comes from `assets/timeline.json` via `web/timeline_data.py`; the
    selected slide is pushed back into `CertificationsState` by `on_change`.
    """
    return rx.el.section(
        section_heading("Certifications"),
        rx.el.p(
            rx.cond(
                CertificationsState.current_certification != "",
                CertificationsState.current_certification,
                "Browse the timeline to explore every certification.",
            ),
            class_name="text-sm text-gray-600 mb-3 min-h-[1.25rem]",
        ),
        rx.el.div(
            timeline(
                data=certifications_data,
                options=certifications_options,
                on_change=CertificationsState.on_slide_change,
                width="100%",
                height="100%",
            ),
            class_name=(
                "w-full overflow-hidden border-0 rounded-lg shadow-md bg-white "
                "h-[400px] md:h-[700px] lg:h-[800px]"
            ),
        ),
        id="certifications",
        class_name="mb-12 scroll-mt-24",
    )
