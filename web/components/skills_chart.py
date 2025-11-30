import reflex as rx
from web.states.resume_state import ResumeState


def skills_chart_section() -> rx.Component:
    """Interactive skills radar chart section."""
    return rx.el.section(
        rx.el.h2(
            "Skills",
            class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
        ),
        # Skill selector dropdown
        rx.el.div(
            rx.el.label(
                "Select Skill Category:",
                class_name="block text-lg font-semibold text-gray-700 mb-3",
            ),
            rx.select(
                ResumeState.skill_categories,
                value=ResumeState.selected_skill,
                on_change=ResumeState.set_selected_skill,
                class_name="w-full md:w-96 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
            ),
            class_name="mb-8",
        ),
        # Individual skill chart
        rx.plotly(
            data=ResumeState.individual_chart,
            class_name="mb-12",
        ),
        # Comparative chart title
        rx.el.h3(
            "Comparative View",
            class_name="text-2xl font-bold text-gray-700 mb-4 mt-8",
        ),
        # Comparative chart - all skills
        rx.plotly(
            data=ResumeState.comparative_chart,
            class_name="mb-12",
        ),
        id="skills",
        class_name="mb-12 scroll-mt-24",
    )
