"""The shell every resume page shares: sidebar, navbar and a main column.

Each navbar entry is its own page (see `web/web.py`), in English and in Spanish,
so every page passes its English route as `active` and its language as `lang`:
the navbar marks the current entry and the sidebar's flags link to the same page
in the other language.
"""

import reflex as rx

from .footer import site_footer
from .navbar import navbar
from .sidebar import sidebar

# The main column of the regular pages; the dashboard passes a tighter one.
_MAIN = "p-4 md:p-8 lg:p-16 w-full"
_CONTENT = "container mx-auto"

MAIN_LAYOUT_CLASS = "flex min-h-screen bg-[#f5f5dc]"
CONTENT_AREA_CLASS = "flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-60"


def site_shell(
    *children: rx.Component, top: rx.Component, lang: str, route: str, **content_props
) -> rx.Component:
    """Sidebar + a top bar + the page's main column + the footer, in `lang`.

    `route` is the page's English route; the language flags link to it in each
    language. The `lang` attribute tells browsers and screen readers which
    language the page is written in.
    """
    return rx.el.div(
        sidebar(lang=lang, route=route),
        rx.el.div(
            top,
            *children,
            site_footer(lang=lang),
            class_name=CONTENT_AREA_CLASS,
            **content_props,
        ),
        lang=lang,
        class_name=MAIN_LAYOUT_CLASS,
    )


def page_shell(
    *children: rx.Component,
    active: str,
    lang: str = "en",
    route: str | None = None,
    main_class: str = _MAIN,
    content_class: str = _CONTENT,
) -> rx.Component:
    """Sidebar + navbar (with `active` marked) + the page's content + the footer."""
    return site_shell(
        rx.el.main(
            rx.el.div(*children, class_name=content_class),
            class_name=main_class,
        ),
        top=navbar(active=active, lang=lang),
        lang=lang,
        route=route if route is not None else active,
    )
