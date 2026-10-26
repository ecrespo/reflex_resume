import reflex as rx
from reflex_silverpoint_react import sp_button

from ..i18n import localize, t
from ..states.resume_state import ResumeState


def menu_button(lang: str = "en") -> rx.Component:
    """Opens the profile drawer on mobile."""
    return rx.el.div(
        sp_button(
            t(lang, "Menu", "Menú"),
            size="sm",
            label=t(lang, "Open profile menu", "Abrir el menú del perfil"),
            on_click=ResumeState.toggle_mobile_menu,
        ),
        class_name="md:hidden flex-shrink-0",
    )


# Small caps in the site palette's inks (see theme.SITE_PALETTE); the typeface
# is the page's, EB Garamond.
_LINK = (
    "[font-variant:small-caps] "
    "text-[1.05rem] tracking-wide text-[#1F3D36] hover:text-[#2F6F86] "
    "underline-offset-4 decoration-1 decoration-[#2F6F86] hover:underline "
    "transition-colors whitespace-nowrap"
)


# The current page: underlined and in the accent ink, and announced as such.
_ACTIVE = " underline decoration-2 text-[#2F6F86]"


def navbar_link(text: str, url: str = "#", active: bool = False) -> rx.Component:
    if active:
        return rx.el.a(text, href=url, class_name=_LINK + _ACTIVE, aria_current="page")
    return rx.el.a(text, href=url, class_name=_LINK)


# One entry per page of the resume; every entry is its own route. Routes are the
# English ones; `localize` gives the Spanish route.
NAV_ITEMS = [
    ({"en": "Home", "es": "Inicio"}, "/"),
    ({"en": "Resume", "es": "Currículum"}, "/resume"),
    ({"en": "Portfolio", "es": "Portafolio"}, "/portfolio"),
    ({"en": "Dev Dashboard Stats", "es": "Estadísticas de desarrollo"}, "/dev-dashboard-stats"),
]


def _silverpoint_nav(*children: rx.Component) -> rx.Component:
    """The bar itself: a soft pastel mint from the sidebar's family and a hairline rule.

    #DFF1EC keeps the links legible: 10:1 for the text, 4.8:1 for the hover ink.
    """
    return rx.el.nav(
        rx.el.div(
            *children,
            class_name="flex flex-row gap-6 items-center overflow-x-auto w-full px-4 md:px-8 h-full no-scrollbar",
        ),
        class_name=(
            "w-full h-14 bg-[#DFF1EC] flex items-center flex-shrink-0 z-20 sticky top-0 "
            "border-b border-[#5C7B71]/60"
        ),
    )


def blog_navbar_link(text: str, url: str) -> rx.Component:
    """Blog navbar link: the main navbar's style, with the old Pelican blog's sections."""
    return navbar_link(text, url)


_BLOG_ITEMS = [
    ({"en": "HOME", "es": "INICIO"}, "/"),
    ({"en": "BLOG", "es": "BLOG"}, "/blog"),
    ({"en": "ARCHIVES", "es": "ARCHIVO"}, "/blog/archives"),
    ({"en": "CATEGORIES", "es": "CATEGORÍAS"}, "/blog/categories"),
    ({"en": "TAGS", "es": "ETIQUETAS"}, "/blog/tags"),
    ({"en": "ATOM", "es": "ATOM"}, "/feed.xml"),
    ({"en": "DEV DASHBOARD STATS", "es": "ESTADÍSTICAS DE DESARROLLO"}, "/dev-dashboard-stats"),
]


def blog_navbar(lang: str = "en") -> rx.Component:
    """The navigation bar for the blog section."""
    return _silverpoint_nav(
        # Menu button for mobile (reusing state)
        menu_button(lang),
        *[blog_navbar_link(text[lang], url=localize(url, lang)) for text, url in _BLOG_ITEMS],
    )


def navbar(active: str = "", lang: str = "en") -> rx.Component:
    """The top navigation bar; `active` is the English route of the page it sits on."""
    return _silverpoint_nav(
        # Menu button for mobile
        menu_button(lang),
        *[
            navbar_link(text[lang], url=localize(url, lang), active=url == active)
            for text, url in NAV_ITEMS
        ],
    )
