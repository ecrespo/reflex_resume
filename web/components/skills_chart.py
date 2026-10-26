import reflex as rx
from reflex_silverpoint_react import radar_chart, sp_select

from web.i18n import t
from web.resume_data import translate
from web.states.resume_state import SKILL_LEVELS, ResumeState

# Skill levels run from 1 to 5; a fixed domain keeps every category on the same
# radial scale instead of stretching each one to its own maximum.
_LEVEL_DOMAIN = [0, 5]


def skills_chart_section(lang: str = "en") -> rx.Component:
    """Interactive skills radar charts (silverpoint)."""
    spanish = lang == "es"
    return rx.el.section(
        rx.el.h2(
            t(lang, "Skills", "Habilidades"),
            class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
        ),
        rx.el.div(
            sp_select(
                # The keys stay English; Spanish pages show Spanish labels.
                [{"key": category, "label": translate(category, "es")} for category in SKILL_LEVELS]
                if spanish
                else ResumeState.skill_categories,
                value=ResumeState.selected_skill,
                on_change=ResumeState.set_selected_skill,
                label=t(lang, "Select Skill Category", "Elige una categoría"),
                width="100%",
                id="skill-category",
            ),
            class_name="mb-8 w-full md:w-96",
        ),
        # One spoke per skill of the selected category.
        rx.el.div(
            radar_chart(
                data=ResumeState.current_skill_radar,
                subject_key="topic",
                value_key="value",
                domain=_LEVEL_DOMAIN,
                title=ResumeState.selected_skill_es if spanish else ResumeState.selected_skill,
                description=t(
                    lang,
                    "Self-assessed level of each skill, from 1 to 5.",
                    "Nivel autoevaluado de cada habilidad, de 1 a 5.",
                ),
                height=360,
                id="skills-radar",
            ),
            class_name="mb-12 w-full",
        ),
        rx.el.h3(
            t(lang, "Comparative View", "Vista comparativa"),
            class_name="text-2xl font-bold text-gray-700 mb-4 mt-8",
        ),
        # One spoke per category, valued by the average level of its skills.
        rx.el.div(
            radar_chart(
                data=(
                    ResumeState.category_average_radar_es
                    if spanish
                    else ResumeState.category_average_radar
                ),
                subject_key="topic",
                value_key="value",
                domain=_LEVEL_DOMAIN,
                title=t(lang, "Average level per category", "Nivel promedio por categoría"),
                description=t(
                    lang,
                    "Mean self-assessed level of the skills in each category.",
                    "Nivel autoevaluado promedio de las habilidades de cada categoría.",
                ),
                height=360,
                id="skills-category-radar",
            ),
            class_name="mb-12 w-full",
        ),
        id="skills",
        class_name="mb-12 scroll-mt-24",
    )
