import reflex as rx


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
            navbar_link("Education", url="#education"),
            navbar_link("Work Experience", url="#work-experience"),
            navbar_link("Portfolio", url="#portfolio"),
            navbar_link("Skills", url="#skills"),
            navbar_link("Social Media", url="#social-media"),
            navbar_link("Certifications", url="#certifications"),
            class_name="flex flex-row gap-6 items-center overflow-x-auto w-full px-8 h-full no-scrollbar",
        ),
        class_name="w-full h-14 bg-[#4a9bba] flex items-center shadow-sm flex-shrink-0 z-20 sticky top-0",
    )