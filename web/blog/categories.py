from collections import defaultdict

import reflex as rx
from reflex_silverpoint_react import sp_badge, sp_tag

from web.blog.paths import sorted_posts
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import t

# Constants
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"


class CategoriesState(rx.State):
    """State for categories page."""

    @rx.var
    def categories_with_counts(self) -> list[tuple[str, int]]:
        """Get list of categories with their post counts."""
        counts = defaultdict(int)
        for post in sorted_posts:
            cat = post.category.strip()
            if cat:
                counts[cat] += 1

        # Sort alphabetically
        return sorted(counts.items())


def category_entry(item: tuple[str, int], lang: str = "en") -> rx.Component:
    return rx.el.li(
        sp_tag(item[0], tone=2),
        sp_badge(count=item[1], max=999, label=t(lang, "posts", "artículos")),
        class_name="inline-flex items-center gap-1",
    )


def categories_page(lang: str = "en") -> rx.Component:
    return site_shell(
        rx.el.main(
            rx.el.div(
                rx.el.header(
                    rx.el.h1(
                        t(lang, "Categories", "Categorías"),
                        class_name="text-4xl font-light text-gray-800 mb-8",
                    ),
                    class_name="mb-8",
                ),
                rx.el.ul(
                    rx.foreach(
                        CategoriesState.categories_with_counts,
                        lambda item: category_entry(item, lang),
                    ),
                    class_name="list-none flex flex-wrap gap-3",
                ),
                class_name="container mx-auto max-w-5xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang),
        lang=lang,
        route="/blog/categories",
        id="content-area",
    )
