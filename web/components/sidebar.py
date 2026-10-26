import reflex as rx
import reflex_google_analytics_reactjs as rga
from reflex_silverpoint_react import sp_avatar, sp_button, sp_card, sp_drawer

from ..i18n import LANG_NAMES, LANGS, localize, t
from ..states.resume_state import ResumeState

_LINK_CARD = "block w-full mb-3 hover:shadow-md transition-shadow rounded-lg"


def skill_item(text: str) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            "•",
            class_name="text-[#2C6355] text-xl leading-none mr-2 align-middle inline-block",
        ),
        rx.el.span(text, class_name="text-gray-700 font-medium text-sm"),
        class_name="flex items-start mb-1.5 last:mb-0",
    )


def _link_card(icon: rx.Component, title: str, subtitle: str) -> rx.Component:
    return sp_card(
        rx.el.div(
            icon,
            rx.el.div(
                rx.el.p(title, class_name="font-bold text-gray-900 text-sm mb-0"),
                rx.el.p(subtitle, class_name="text-xs text-gray-600 mb-0"),
                class_name="flex-1",
            ),
            class_name="flex items-center gap-2",
        ),
        size="sm",
    )


_SUMMARY = [
    {"en": "Electrical Engineer.", "es": "Ingeniero electricista."},
    {"en": "Python Developer.", "es": "Desarrollador Python."},
    {"en": "AI Engineer.", "es": "Ingeniero de IA."},
    {"en": "Data analyst.", "es": "Analista de datos."},
    {"en": "Data Engineer.", "es": "Ingeniero de datos."},
    {"en": "AWS Cloud Engineer.", "es": "Ingeniero cloud de AWS."},
    {"en": "Data Scientist.", "es": "Científico de datos."},
]

# --------------------------------------------------------------------------- #
# Language switch: a flag per language, the current one framed.
# --------------------------------------------------------------------------- #

# The Union Flag and Spain's civil flag (without the coat of arms), 3:2.
_FLAGS = {
    "en": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="27" height="18" aria-hidden="true">
            <rect width="60" height="40" fill="#012169"/>
            <path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="8"/>
            <path d="M0,0 L30,20 M60,0 L30,20 M0,40 L30,20 M60,40 L30,20" stroke="#C8102E" stroke-width="3"/>
            <path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="12"/>
            <path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="7"/>
        </svg>
    """,
    "es": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="27" height="18" aria-hidden="true">
            <rect width="60" height="40" fill="#AA151B"/>
            <rect y="10" width="60" height="20" fill="#F1BF00"/>
        </svg>
    """,
}

_FLAG_LINK = (
    "inline-flex items-center gap-1.5 px-1.5 py-1 rounded border text-xs tracking-wide "
    "transition-colors"
)


def _flag(code: str, lang: str, route: str) -> rx.Component:
    """The flag of `code`: a link to this page in that language, or the current one."""
    body = (
        rx.html(_FLAGS[code], class_name="flex shadow-sm"),
        rx.el.span(code.upper(), class_name="font-semibold"),
    )
    name = LANG_NAMES[code]
    if code == lang:
        return rx.el.span(
            *body,
            title=name,
            aria_current="true",
            aria_label=t(lang, f"{name} (current language)", f"{name} (idioma actual)"),
            class_name=f"{_FLAG_LINK} border-[#2F6F86] bg-white/70 text-[#1F3D36]",
        )
    return rx.el.a(
        *body,
        href=localize(route, code),
        title=name,
        hreflang=code,
        aria_label=t(lang, f"Read this page in {name}", f"Leer esta página en {name}"),
        class_name=f"{_FLAG_LINK} border-transparent text-[#3E6A5E] hover:border-[#5C7B71]/60 hover:text-[#1F3D36]",
    )


def language_switch(lang: str, route: str) -> rx.Component:
    """English and Spanish flags, at the end of the sidebar and aligned right."""
    return rx.el.nav(
        *[_flag(code, lang, route) for code in LANGS],
        aria_label=t(lang, "Language", "Idioma"),
        class_name="w-full flex justify-end gap-1.5 mt-auto pt-4 px-1",
    )


def sidebar_content(lang: str = "en", route: str = "/") -> rx.Component:
    """Shared sidebar content for both desktop and mobile."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Ernesto Crespo.",
                class_name="text-[1.7rem] font-semibold text-[#1F3D36] mb-0.5 tracking-tight",
            ),
            rx.el.p(
                "Seraph13",
                class_name="italic text-[#3E6A5E] text-base tracking-wide",
            ),
            class_name="mb-4 text-center",
        ),
        rx.el.div(
            sp_avatar(src="/ec_drawing.jpg", name="Ernesto Crespo", shape="circle", pixel_size=96),
            class_name="mb-4",
        ),
        sp_card(
            rx.el.ul(
                *[skill_item(item[lang]) for item in _SUMMARY],
                class_name="list-none m-0 p-0",
            ),
            title=t(lang, "Summary", "Resumen"),
            heading_level=2,
            class_name="w-full mb-3",
        ),
        rx.el.a(
            _link_card(
                # LinkedIn logo
                rx.html("""
                    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="#0077b5" aria-hidden="true">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                """),
                "Ernesto Crespo",
                t(lang, "View LinkedIn Profile", "Ver el perfil de LinkedIn"),
            ),
            href="https://www.linkedin.com/in/ernestocrespo/",
            target="_blank",
            rel="noopener noreferrer",
            class_name=_LINK_CARD,
        ),
        # Résumé download
        rx.el.div(
            # SpButton forwards no `download` attribute, so the file name comes
            # from rx.download instead of an <a download>.
            sp_button(
                t(lang, "Download Resume", "Descargar currículum"),
                block=True,
                on_click=[
                    rga.event("resume_download", {"file_name": "ErnestoCrespo.pdf"}),
                    rx.download(
                        url="/Resume_Ernesto_Crespo_software.pdf", filename="ErnestoCrespo.pdf"
                    ),
                ],
            ),
            class_name="w-full px-4",
        ),
        language_switch(lang, route),
        class_name="flex flex-col items-center pt-6 px-4 w-full pb-4 min-h-full",
    )


def sidebar(lang: str = "en", route: str = "/") -> rx.Component:
    """The left sidebar: fixed on desktop, a drawer on mobile."""
    return rx.fragment(
        # Mobile: a drawer opened by the navbar's menu button. Escape, the
        # backdrop and its close button report back through `on_open_change`.
        rx.el.div(
            sp_drawer(
                sidebar_content(lang, route),
                side="start",
                label=t(lang, "Profile", "Perfil"),
                extent="15rem",
                open=ResumeState.mobile_menu_open,
                on_open_change=ResumeState.set_mobile_menu_open,
                id="mobile-sidebar",
            ),
            class_name="md:hidden",
        ),
        # Desktop sidebar (always visible)
        rx.el.aside(
            sidebar_content(lang, route),
            class_name="hidden md:flex w-60 min-h-screen bg-[#DFF1EC] flex-shrink-0 flex-col fixed left-0 top-0 h-full overflow-y-auto border-r border-[#5C7B71]/60",
        ),
    )
