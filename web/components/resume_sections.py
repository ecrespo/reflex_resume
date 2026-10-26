import reflex as rx
from reflex_silverpoint_react import (
    sp_button,
    sp_card,
    sp_descriptions,
    sp_empty,
    sp_tag,
    sp_timeline,
)

from ..i18n import t
from ..resume_data import (
    education_data,
    period_text,
    portfolio_data,
    skills_data,
    social_media_data,
    translate,
    work_experience_data,
)
from ..states.certifications_state import CertificationsState
from ..timeline_data import certifications_data, certifications_options


def section_heading(text: str) -> rx.Component:
    return rx.el.h2(
        text,
        class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
    )


def education_section(lang: str = "en") -> rx.Component:
    degree, university, year = education_data
    return rx.el.section(
        section_heading(t(lang, "Education", "Educación")),
        sp_card(
            rx.el.p(translate(university, lang), class_name="italic text-gray-700"),
            title=translate(degree, lang),
            extra=year,
        ),
        id="education",
        class_name="mb-12 scroll-mt-24",
    )


def _tech_tags(tech_stack: str, lang: str = "en") -> rx.Component:
    """One tag per technology of a comma-separated stack."""
    stack = translate(tech_stack, lang)
    names = [name.strip() for name in stack.rstrip(".").split(",") if name.strip()]
    return rx.el.div(
        *[sp_tag(name, tone=1, size="sm") for name in names],
        class_name="flex flex-wrap gap-2",
        aria_label=t(lang, "Tech stack", "Stack tecnológico"),
    )


def experience_item(item: list, lang: str = "en") -> rx.Component:
    # Built from static Python data (not state Vars), so plain Python conditionals apply.
    title, company, period, responsibilities, tech_stack = item
    return sp_card(
        rx.el.ul(
            *[
                rx.el.li(translate(r, lang), class_name="mb-1 leading-relaxed")
                for r in responsibilities
            ],
            class_name="list-disc list-outside ml-5 text-gray-700 space-y-1",
        )
        if responsibilities
        else rx.fragment(),
        title=f"{translate(title, lang)}, {translate(company, lang)}",
        extra=period_text(period, lang),
        footer=_tech_tags(tech_stack, lang) if tech_stack else None,
        class_name="mb-6 last:mb-0",
    )


def work_experience_section(lang: str = "en") -> rx.Component:
    return rx.el.section(
        section_heading(t(lang, "Work Experience", "Experiencia laboral")),
        *[experience_item(item, lang) for item in work_experience_data],
        id="work-experience",
        class_name="mb-12 scroll-mt-24",
    )


def _link_list(items: list, lang: str = "en") -> rx.Component:
    return rx.el.ul(
        *[
            rx.el.li(
                rx.el.a(
                    translate(name, lang),
                    href=url,
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name="text-[#2F6F86] hover:text-[#1F3D36] hover:underline",
                ),
                class_name="mb-2",
            )
            for name, url in items
        ],
        class_name="list-disc list-outside ml-5 text-gray-700",
    )


def portfolio_section(lang: str = "en") -> rx.Component:
    """Portfolio section with notebook links."""
    return rx.el.section(
        section_heading(t(lang, "Portfolio", "Portafolio")),
        rx.el.h3(
            "Notebooks",
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.div(
            sp_card(_link_list(portfolio_data["edas"], lang), title="EDAs", heading_level=4),
            sp_card(
                _link_list(portfolio_data["graphs"], lang),
                title=t(lang, "Graphs", "Gráficos"),
                heading_level=4,
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        id="portfolio",
        class_name="mb-12 scroll-mt-24",
    )


def skills_list_section(lang: str = "en") -> rx.Component:
    """Skills list section (text-based)."""
    return rx.el.section(
        section_heading(t(lang, "Skills List", "Lista de habilidades")),
        sp_descriptions(
            [{"label": translate(row[0], lang), "value": row[1]} for row in skills_data],
            columns=1,
            bordered=True,
        ),
        id="skills-list",
        class_name="mb-12 scroll-mt-24",
    )


def social_media_section(lang: str = "en") -> rx.Component:
    """Social media links section."""
    return rx.el.section(
        section_heading(t(lang, "Social Media", "Redes sociales")),
        rx.el.div(
            *[sp_button(name, href=url, label=f"{name}: {url}") for name, url in social_media_data],
            class_name="flex flex-wrap gap-3",
        ),
        id="social-media",
        class_name="mb-12 scroll-mt-24",
    )


def certifications_section(lang: str = "en") -> rx.Component:
    """Certifications timeline: Knight Lab TimelineJS drawn in silverpoint.

    Data comes from `assets/timeline.json` via `web/timeline_data.py`; the
    selected slide is pushed back into `CertificationsState` by `on_change`.
    """
    return rx.el.section(
        section_heading(t(lang, "Certifications", "Certificaciones")),
        rx.el.p(
            rx.cond(
                CertificationsState.current_certification != "",
                CertificationsState.current_certification,
                t(
                    lang,
                    "Browse the timeline to explore every certification.",
                    "Recorre la línea de tiempo para explorar cada certificación.",
                ),
            ),
            class_name="text-sm text-gray-600 mb-3 min-h-[1.25rem]",
            aria_live="polite",
        ),
        rx.el.div(
            sp_timeline(
                certifications_data,
                certifications_options,
                height="100%",
                label=t(lang, "Certifications", "Certificaciones"),
                fallback=sp_empty(
                    description=t(
                        lang,
                        "The certifications timeline could not load.",
                        "No se pudo cargar la línea de tiempo de certificaciones.",
                    )
                ),
                on_change=CertificationsState.on_slide_change,
                id="certifications-timeline",
            ),
            class_name="w-full h-[400px] md:h-[700px] lg:h-[800px] xl:h-[680px]",
        ),
        id="certifications",
        class_name="mb-12 scroll-mt-24",
    )
