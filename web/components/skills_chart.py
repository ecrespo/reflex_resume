import reflex as rx
from reflex_silverpoint_react import radar_chart, sp_select

from web.states.resume_state import ResumeState

# Skill levels run from 1 to 5; a fixed domain keeps every category on the same
# radial scale instead of stretching each one to its own maximum.
_LEVEL_DOMAIN = [0, 5]


def skills_chart_section() -> rx.Component:
    """Interactive skills radar charts (silverpoint)."""
    return rx.el.section(
        rx.el.h2(
            "Skills",
            class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
        ),
        rx.el.div(
            sp_select(
                ResumeState.skill_categories,
                value=ResumeState.selected_skill,
                on_change=ResumeState.set_selected_skill,
                label="Select Skill Category",
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
                title=ResumeState.selected_skill,
                description="Self-assessed level of each skill, from 1 to 5.",
                height=360,
                id="skills-radar",
            ),
            class_name="mb-12 w-full",
        ),
        rx.el.h3(
            "Comparative View",
            class_name="text-2xl font-bold text-gray-700 mb-4 mt-8",
        ),
        # One spoke per category, valued by the average level of its skills.
        rx.el.div(
            radar_chart(
                data=ResumeState.category_average_radar,
                subject_key="topic",
                value_key="value",
                domain=_LEVEL_DOMAIN,
                title="Average level per category",
                description="Mean self-assessed level of the skills in each category.",
                height=360,
                id="skills-category-radar",
            ),
            class_name="mb-12 w-full",
        ),
        id="skills",
        class_name="mb-12 scroll-mt-24",
    )
