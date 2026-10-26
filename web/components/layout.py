"""The shell every resume page shares: sidebar, navbar and a main column.

Each navbar entry is its own page (see `web/web.py`), so every page passes its
route as `active` and the navbar marks it as the current one.
"""

import reflex as rx

from .footer import site_footer
from .navbar import navbar
from .sidebar import sidebar

# The main column of the regular pages; the dashboard passes a tighter one.
_MAIN = "p-4 md:p-8 lg:p-16 w-full"
_CONTENT = "container mx-auto"


def page_shell(
    *children: rx.Component,
    active: str,
    main_class: str = _MAIN,
    content_class: str = _CONTENT,
) -> rx.Component:
    """Sidebar + navbar (with `active` marked) + the page's content + the footer."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(active=active),
            rx.el.main(
                rx.el.div(*children, class_name=content_class),
                class_name=main_class,
            ),
            site_footer(),
            class_name="flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-60",
        ),
        class_name="flex min-h-screen bg-[#f5f5dc]",
    )
