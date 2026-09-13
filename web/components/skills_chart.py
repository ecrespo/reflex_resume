import reflex as rx
import reflex_rosencharts as rxc

from web.states.resume_state import ResumeState

# The rosencharts radar draws its axis labels outside the circle, so the card
# needs room around it.
_CHART_CARD = "mb-12 w-full bg-white rounded-lg shadow-md px-6 py-10 md:px-16 md:py-14"


def skills_chart_section() -> rx.Component:
    """Interactive skills radar charts (reflex-rosencharts)."""
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
        # One axis per skill of the selected category.
        rx.el.div(
            rx.el.h3(
                ResumeState.selected_skill,
                class_name="text-xl font-semibold text-gray-700 text-center",
            ),
            rxc.radar_chart_rounded(data=ResumeState.current_skill_radar),
            class_name=_CHART_CARD,
        ),
        # Comparative chart title
        rx.el.h3(
            "Comparative View",
            class_name="text-2xl font-bold text-gray-700 mb-4 mt-8",
        ),
        # One axis per category, valued by the average level of its skills.
        rx.el.div(
            rx.el.h3(
                "Average level per category",
                class_name="text-xl font-semibold text-gray-700 text-center",
            ),
            rxc.radar_chart_rounded(data=ResumeState.category_average_radar),
            class_name=_CHART_CARD,
        ),
        id="skills",
        class_name="mb-12 scroll-mt-24",
    )
