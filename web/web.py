import reflex as rx
from web.components.sidebar import sidebar
from web.components.navbar import navbar
from web.components.resume_sections import (
    education_section, 
    work_experience_section,
    portfolio_section,
    skills_list_section,
    social_media_section,
    certifications_section,
)
from web.components.skills_chart import skills_chart_section
from web.states.resume_state import ResumeState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                rx.el.div(
                    education_section(),
                    work_experience_section(),
                    portfolio_section(),
                    skills_list_section(),
                    skills_chart_section(),
                    social_media_section(),
                    certifications_section(),
                    class_name="container mx-auto",
                ),
                class_name="p-4 md:p-8 lg:p-16 w-full max-w-5xl",
            ),
            class_name="flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96",
        ),
        class_name="flex min-h-screen font-['Inter'] bg-[#f5f5dc]",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.style("""
            html {
                scroll-behavior: smooth;
            }
            """),
    ],
)
app.add_page(index, route="/")