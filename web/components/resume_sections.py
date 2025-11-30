import reflex as rx
from ..resume_data import education_data, work_experience_data, portfolio_data, skills_data, social_media_data


def section_heading(text: str) -> rx.Component:
    return rx.el.h2(
        text,
        class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
    )


def education_section() -> rx.Component:
    return rx.el.section(
        section_heading("Education"),
        rx.el.div(
            rx.el.div(
                rx.el.span(education_data[0], class_name="font-bold text-gray-900 text-lg"),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(education_data[1], class_name="italic text-gray-700"),
                class_name="flex-1",
            ),
            rx.el.span(education_data[2], class_name="text-gray-600 font-medium"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-6",
        ),
        id="education",
        class_name="mb-12 scroll-mt-24",
    )


def experience_item(item: list) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(item[0], class_name="font-bold text-gray-900 text-lg"),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(item[1], class_name="italic text-gray-700"),
            ),
            rx.el.span(item[2], class_name="text-gray-600 font-medium whitespace-nowrap"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-baseline mb-3",
        ),
        rx.cond(
            item[3] is not None,
            rx.el.ul(
                rx.foreach(
                    item[3],
                    lambda r: rx.el.li(r, class_name="mb-1 leading-relaxed"),
                ),
                class_name="list-disc list-outside ml-5 text-gray-700 mb-4 space-y-1",
            ),
            rx.fragment(),
        ),
        rx.cond(
            item[4] is not None,
            rx.el.p(
                rx.el.span("Tech Stack: ", class_name="font-semibold text-gray-800"),
                item[4],
                class_name="text-sm text-gray-600 bg-gray-100/50 p-3 rounded-lg",
            ),
            rx.fragment(),
        ),
        class_name="mb-10 last:mb-0",
    )


def work_experience_section() -> rx.Component:
    return rx.el.section(
        section_heading("Work Experience"),
        rx.foreach(
            work_experience_data,
            lambda item: experience_item(item)
        ),
        id="work-experience",
        class_name="mb-12 scroll-mt-24",
    )


def portfolio_section() -> rx.Component:
    """Portfolio section with notebook links."""
    return rx.el.section(
        section_heading("Portfolio"),
        rx.el.h3(
            "Notebooks",
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.h4(
            "EDAs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.foreach(
                portfolio_data["edas"],
                lambda item: rx.el.li(
                    rx.el.a(
                        item[0],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-2",
                )
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        rx.el.h4(
            "Graphs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.foreach(
                portfolio_data["graphs"],
                lambda item: rx.el.li(
                    rx.el.a(
                        item[0],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-2",
                )
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        id="portfolio",
        class_name="mb-12 scroll-mt-24",
    )


def skills_list_section() -> rx.Component:
    """Skills list section (text-based)."""
    return rx.el.section(
        section_heading("Skills List"),
        rx.el.div(
            rx.foreach(
                skills_data,
                lambda item: rx.el.div(
                    rx.el.span(f"{item[0]}: ", class_name="font-bold text-gray-800"),
                    rx.el.code(f"`{item[1]}`", class_name="text-sm text-gray-700"),
                    class_name="mb-3",
                )
            ),
            class_name="space-y-2",
        ),
        id="skills-list",
        class_name="mb-12 scroll-mt-24",
    )


def social_media_section() -> rx.Component:
    """Social media links section."""
    return rx.el.section(
        section_heading("Social Media"),
        rx.el.div(
            rx.foreach(
                social_media_data,
                lambda item: rx.el.div(
                    rx.el.span(f"{item[0]}: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                    rx.el.a(
                        item[1],
                        href=item[1],
                        target="_blank",
                        class_name="text-blue-600 hover:text-blue-800 hover:underline",
                    ),
                    class_name="mb-3 flex items-start",
                )
            ),
            class_name="space-y-1",
        ),
        id="social-media",
        class_name="mb-12 scroll-mt-24",
    )


def certifications_section() -> rx.Component:
    """Certifications timeline section using iframe embed."""
    return rx.el.section(
        section_heading("Certifications"),
        rx.el.iframe(
            src="/timeline.html",
            class_name="w-full border-0 rounded-lg shadow-md h-[400px] md:h-[700px] lg:h-[800px]",
            style={"background": "white"},
        ),
        id="certifications",
        class_name="mb-12 scroll-mt-24",
    )