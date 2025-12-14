import reflex as rx
from ..states.resume_state import ResumeState


def skill_item(text: str) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            "•",
            class_name="text-blue-700 text-xl leading-none mr-2 align-middle inline-block",
        ),
        rx.el.span(text, class_name="text-gray-700 font-medium text-sm"),
        class_name="flex items-start mb-1.5 last:mb-0",
    )


def sidebar_content() -> rx.Component:
    """Shared sidebar content for both desktop and mobile."""
    return rx.el.div(
        # Close button for mobile
        rx.el.button(
            "✕",
            on_click=ResumeState.close_mobile_menu,
            class_name="md:hidden absolute top-4 right-4 text-gray-700 hover:text-gray-900 text-2xl font-bold",
        ),
        rx.el.div(
            rx.el.h1(
                "Ernesto Crespo.",
                class_name="text-2xl font-bold text-gray-900 mb-0.5 tracking-tight",
            ),
            rx.el.p(
                "Resume",
                class_name="italic text-gray-700 text-sm font-medium tracking-wide",
            ),
            class_name="mb-4 text-center",
        ),
        rx.image(
            src="/ec.jpg",
            alt="Ernesto Crespo",
            class_name="w-24 h-24 rounded-xl object-cover mb-4 shadow-sm bg-gray-100 border-2 border-white/30",
        ),
        rx.el.div(
            rx.el.h2(
                "Summary",
                class_name="text-base font-bold text-gray-800 mb-2 self-start w-full pl-1",
            ),
            rx.el.div(
                rx.el.ul(
                    skill_item("Electrical Engineer."),
                    skill_item("Python Developer."),
                    skill_item("Data analyst."),
                    skill_item("Data Engineer."),
                    skill_item("AWS Cloud Engineer."),
                    skill_item("Data Scientist."),
                    class_name="list-none m-0 p-0",
                ),
                class_name="bg-[#73cbb6] p-4 rounded-lg w-full shadow-sm",
            ),
            class_name="w-full flex flex-col mb-3",
        ),
        # LinkedIn Profile Link
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    # LinkedIn Logo SVG
                    rx.html("""
                        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="#0077b5">
                            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                        </svg>
                    """),
                    rx.el.div(
                        rx.el.p(
                            "Ernesto Crespo",
                            class_name="font-bold text-gray-900 text-sm mb-0",
                        ),
                        rx.el.p(
                            "View LinkedIn Profile",
                            class_name="text-xs text-gray-600 mb-0",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="https://www.linkedin.com/in/ernestocrespo/",
                target="_blank",
                rel="noopener noreferrer",
                class_name="block w-full",
            ),
            class_name="w-full bg-white rounded-lg p-3 mb-3 shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-200",
        ),
        # Blog Link
        rx.el.div(
            rx.link(
                rx.el.div(
                    # Blog Icon SVG
                    rx.html("""
                        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4a9bba" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path>
                            <path d="M8 7h6"></path>
                            <path d="M8 11h8"></path>
                        </svg>
                    """),
                    rx.el.div(
                        rx.el.p(
                            "Blog",
                            class_name="font-bold text-gray-900 text-sm mb-0",
                        ),
                        rx.el.p(
                            "Ver artículos",
                            class_name="text-xs text-gray-600 mb-0",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/blog",
                class_name="block w-full",
            ),
            class_name="w-full bg-white rounded-lg p-3 mb-3 shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-200",
        ),
        # Contact section
        rx.el.div(
            rx.el.p(
                "Wish to connect?",
                class_name="text-sm text-gray-700 font-medium mb-1",
            ),
            rx.link(
                "📧 ecrespo@gmail.com",
                href="mailto:ecrespo@gmail.com",
                is_external=True,
                class_name="text-sm text-blue-600 hover:text-blue-800 hover:underline mb-2 inline-block",
            ),
            # PDF Download button
            rx.link(
                "Download Resume",
                href="/Resume_Ernesto_Crespo_software.pdf",
                download="ErnestoCrespo.pdf",
                is_external=True,
                class_name="inline-block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors shadow-sm text-sm",
            ),
            class_name="w-full px-4",
        ),
        class_name="flex flex-col items-center pt-6 px-4 w-full pb-4",
    )


def sidebar() -> rx.Component:
    """The left sidebar component with mobile responsiveness."""
    return rx.fragment(
        # Mobile sidebar overlay
        rx.cond(
            ResumeState.mobile_menu_open,
            rx.el.div(
                on_click=ResumeState.close_mobile_menu,
                class_name="md:hidden fixed inset-0 bg-black/50 z-40",
            ),
        ),
        # Mobile sidebar drawer
        rx.el.aside(
            sidebar_content(),
            class_name=rx.cond(
                ResumeState.mobile_menu_open,
                "md:hidden w-80 min-h-screen bg-[#7dd3c0] flex-shrink-0 flex flex-col fixed left-0 top-0 h-full overflow-y-auto border-r border-teal-600/10 z-50 transition-transform duration-300 ease-in-out transform translate-x-0",
                "md:hidden w-80 min-h-screen bg-[#7dd3c0] flex-shrink-0 flex flex-col fixed left-0 top-0 h-full overflow-y-auto border-r border-teal-600/10 z-50 transition-transform duration-300 ease-in-out transform -translate-x-full",
            ),
        ),
        # Desktop sidebar (always visible)
        rx.el.aside(
            sidebar_content(),
            class_name="hidden md:flex w-96 min-h-screen bg-[#7dd3c0] flex-shrink-0 flex-col fixed left-0 top-0 h-full overflow-y-auto border-r border-teal-600/10",
        ),
    )