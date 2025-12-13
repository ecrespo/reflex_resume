import reflex as rx
from web.states.resume_state import ResumeState


def individual_radar_chart() -> rx.Component:
    """Radar chart for the currently selected skill category."""
    return rx.recharts.radar_chart(
        rx.recharts.polar_grid(),
        rx.recharts.polar_angle_axis(data_key="subject"),
        rx.recharts.polar_radius_axis(angle=90, domain=[0, 5]),
        rx.recharts.radar(
            data_key="value",
            stroke="#636efa",
            fill="#636efa",
            fill_opacity=0.6,
        ),
        data=ResumeState.individual_chart_data,
        width="100%",
        height=350,
    )


def comparative_radar_chart() -> rx.Component:
    """Radar chart comparing all skill categories."""
    return rx.recharts.radar_chart(
        rx.recharts.polar_grid(),
        rx.recharts.polar_angle_axis(data_key="subject"),
        rx.recharts.polar_radius_axis(angle=90, domain=[0, 5]),
        # Add a radar for each category with different colors
        rx.recharts.radar(data_key="Programming", name="Programming", stroke="#636efa", fill="#636efa", fill_opacity=0.3),
        rx.recharts.radar(data_key="Data processing/wrangling", name="Data processing", stroke="#EF553B", fill="#EF553B", fill_opacity=0.3),
        rx.recharts.radar(data_key="Data visualization", name="Data visualization", stroke="#00cc96", fill="#00cc96", fill_opacity=0.3),
        rx.recharts.radar(data_key="Dashboard", name="Dashboard", stroke="#ab63fa", fill="#ab63fa", fill_opacity=0.3),
        rx.recharts.radar(data_key="Machine Learning/Deep Learning", name="ML/DL", stroke="#FFA15A", fill="#FFA15A", fill_opacity=0.3),
        rx.recharts.radar(data_key="IA", name="IA", stroke="#19d3f3", fill="#19d3f3", fill_opacity=0.3),
        rx.recharts.radar(data_key="Web development", name="Web development", stroke="#FF6692", fill="#FF6692", fill_opacity=0.3),
        rx.recharts.radar(data_key="Operating System", name="Operating System", stroke="#B6E880", fill="#B6E880", fill_opacity=0.3),
        rx.recharts.radar(data_key="Low code tools", name="Low code tools", stroke="#FF97FF", fill="#FF97FF", fill_opacity=0.3),
        rx.recharts.radar(data_key="Containers", name="Containers", stroke="#FECB52", fill="#FECB52", fill_opacity=0.3),
        rx.recharts.radar(data_key="Serverless Development", name="Serverless", stroke="#8dd3c7", fill="#8dd3c7", fill_opacity=0.3),
        rx.recharts.radar(data_key="Database Engine", name="Database Engine", stroke="#bebada", fill="#bebada", fill_opacity=0.3),
        rx.recharts.legend(),
        data=ResumeState.comparative_chart_data,
        outer_radius="55%",  # Smaller radar to give more space for labels
        width="100%",
        height=800,
    )


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
        # Individual skill chart title
        rx.el.h3(
            ResumeState.selected_skill,
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        # Individual skill chart with responsive container
        rx.el.div(
            individual_radar_chart(),
            class_name="mb-12 w-full overflow-x-auto",
        ),
        id="skills",
        class_name="mb-12 scroll-mt-24",
    )
