import reflex as rx
from ..states.resume_state import ResumeState


def skill_item(text: str) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            "•",
            class_name="text-blue-700 text-xl leading-none mr-3 align-middle inline-block",
        ),
        rx.el.span(text, class_name="text-gray-700 font-medium text-[15px]"),
        class_name="flex items-start mb-3 last:mb-0",
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
                class_name="text-[26px] font-bold text-gray-900 mb-1 tracking-tight",
            ),
            rx.el.p(
                "Resume",
                class_name="italic text-gray-700 text-sm font-medium tracking-wide",
            ),
            class_name="mb-8 text-center",
        ),
        rx.image(
            src="/ec.jpg",
            alt="Ernesto Crespo",
            class_name="w-32 h-32 rounded-xl object-cover mb-10 shadow-sm bg-gray-100 border-2 border-white/30",
        ),
        rx.el.div(
            rx.el.h2(
                "Summary",
                class_name="text-lg font-bold text-gray-800 mb-4 self-start w-full pl-1",
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
                class_name="bg-[#73cbb6] p-6 rounded-lg w-full shadow-sm",
            ),
            class_name="w-full flex flex-col mb-6",
        ),
        # LinkedIn Badge
        rx.el.div(
            rx.el.script(
                src="https://platform.linkedin.com/badges/js/profile.js",
                type_="text/javascript",
                async_=True,
                defer=True,
            ),
            rx.el.div(
                class_name="badge-base LI-profile-badge",
                data_locale="en_US",
                data_size="medium",
                data_theme="light",
                data_type="VERTICAL",
                data_vanity="ernestocrespo",
                data_version="v1",
            ),
            class_name="w-full flex justify-center mb-6",
        ),
        # Contact section
        rx.el.div(
            rx.el.p(
                "Wish to connect?",
                class_name="text-sm text-gray-700 font-medium mb-2",
            ),
            rx.link(
                "📧 ecrespo@gmail.com",
                href="mailto:ecrespo@gmail.com",
                is_external=True,
                class_name="text-sm text-blue-600 hover:text-blue-800 hover:underline mb-4 inline-block",
            ),
            # PDF Download button
            rx.link(
                "Download Resume",
                href="/Resume_Ernesto_Crespo_software.pdf",
                download="ErnestoCrespo.pdf",
                is_external=True,
                class_name="inline-block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors shadow-sm",
            ),
            class_name="w-full px-6",
        ),
        class_name="flex flex-col items-center pt-12 px-6 w-full pb-8",
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