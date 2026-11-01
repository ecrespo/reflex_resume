from collections import Counter

import reflex as rx
from reflex_silverpoint_react import sp_badge, sp_tag

from web.blog.paths import sorted_posts
from web.blog.terms import tag_in
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import t

# Constants
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"


def tags_with_counts(lang: str) -> list[tuple[str, int]]:
    """Every tag in `lang` with its number of posts, alphabetically (case-insensitive)."""
    counts = Counter(tag_in(tag.strip(), lang) for post in sorted_posts for tag in post.tags)
    return sorted(counts.items(), key=lambda item: item[0].lower())


def tag_entry(item: tuple[str, int], lang: str = "en") -> rx.Component:
    return rx.el.li(
        sp_tag(item[0], tone=2),
        sp_badge(count=item[1], max=999, label=t(lang, "posts", "artículos")),
        class_name="inline-flex items-center gap-1",
    )


def tags_page(lang: str = "en") -> rx.Component:
    return site_shell(
        rx.el.main(
            rx.el.div(
                rx.el.header(
                    rx.el.h1(
                        t(lang, "Tags", "Etiquetas"),
                        class_name="text-4xl font-light text-[#1F3D36] mb-8",
                    ),
                    class_name="mb-8",
                ),
                rx.el.ul(
                    *[tag_entry(item, lang) for item in tags_with_counts(lang)],
                    class_name="list-none flex flex-wrap gap-3",
                ),
                class_name="container mx-auto max-w-5xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang, active="/blog/tags"),
        lang=lang,
        route="/blog/tags",
        id="content-area",
    )
