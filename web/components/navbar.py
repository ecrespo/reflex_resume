import reflex as rx
from ..states.resume_state import ResumeState


def navbar_link(text: str, url: str = "#") -> rx.Component:
    return rx.el.a(
        text,
        href=url,
        class_name="text-white hover:text-white/80 text-sm font-medium hover:underline transition-all whitespace-nowrap",
    )


def navbar() -> rx.Component:
    """The top navigation bar."""
    return rx.el.nav(
        rx.el.div(
            # Hamburger menu button for mobile
            rx.el.button(
                rx.el.div(
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white"),
                    class_name="flex flex-col",
                ),
                on_click=ResumeState.toggle_mobile_menu,
                class_name="md:hidden p-2 hover:bg-white/10 rounded",
            ),
            # Navigation links
            navbar_link("Education", url="#education"),
            navbar_link("Work Experience", url="#work-experience"),
            navbar_link("Portfolio", url="#portfolio"),
            navbar_link("Skills", url="#skills"),
            navbar_link("Social Media", url="#social-media"),
            navbar_link("Certifications", url="#certifications"),
            class_name="flex flex-row gap-6 items-center overflow-x-auto w-full px-4 md:px-8 h-full no-scrollbar",
        ),
        class_name="w-full h-14 bg-[#4a9bba] flex items-center shadow-sm flex-shrink-0 z-20 sticky top-0",
    )