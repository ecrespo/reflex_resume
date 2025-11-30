import reflex as rx


def blog_section() -> rx.Component:
    """Blog section placeholder."""
    return rx.el.section(
        rx.el.div(
            # Section title
            rx.el.h2(
                "Blog",
                class_name="text-4xl font-bold mb-4 text-[#4a9bba]",
            ),
            # Placeholder content
            rx.el.div(
                rx.el.p(
                    "Acá irán los post",
                    class_name="text-gray-600 text-lg text-center py-12",
                ),
                class_name="bg-white rounded-lg shadow-md p-8 min-h-[200px] flex items-center justify-center",
            ),
            class_name="container mx-auto px-4 md:px-8",
        ),
        class_name="py-8",
    )
