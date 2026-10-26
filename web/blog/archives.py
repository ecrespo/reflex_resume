from collections import defaultdict

import reflex as rx
from reflex_silverpoint_react import sp_card

from web.blog.paths import sorted_posts
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import localize, t

# Constants
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"
META_SEPARATOR = "text-gray-400 mx-2"


class ArchivesState(rx.State):
    """State for archives page."""

    @rx.var
    def posts_by_date(self) -> list[tuple[str, list[dict]]]:
        """Group posts by Year-Month."""
        groups = defaultdict(list)

        for post in sorted_posts:
            # Group keys like "September 2023"
            key = post.date.strftime("%B %Y")
            # Sort keys by date descending essentially relies on sorted_posts being sorted
            groups[key].append(post.to_dict())

        # Since sorted_posts is already sorted by date descending,
        # the groups will be populated in that order if we iterate linearly.
        # However, defaultdict doesn't maintain order.
        # Let's use a list of tuples to keep order.

        ordered_groups = []
        current_key = None
        current_list = []

        for post in sorted_posts:
            date_key = post.date.strftime("%B %Y")
            if date_key != current_key:
                if current_key is not None:
                    ordered_groups.append((current_key, current_list))
                current_key = date_key
                current_list = []

            current_list.append(post.to_dict())

        if current_key is not None:
            ordered_groups.append((current_key, current_list))

        return ordered_groups

    @rx.var
    def all_posts_flat(self) -> list[dict]:
        """Return all posts for flat listing if needed (User screenshot shows simple list by date)."""
        return [p.to_dict() for p in sorted_posts]


def archive_entry(post: dict, lang: str = "en") -> rx.Component:
    date_field = "formatted_date_es" if lang == "es" else "formatted_date"
    return rx.el.div(
        rx.el.div(post[date_field], class_name="text-gray-700 font-medium mb-1"),
        rx.link(
            post["title"],
            href=localize("/blog/", lang) + post["slug"].to(str),
            class_name="text-[#2F6F86] hover:underline text-lg block mb-4 ml-4",
        ),
        class_name="mb-2",
    )


def archives_page(lang: str = "en") -> rx.Component:
    return site_shell(
        rx.el.main(
            rx.el.div(
                rx.el.header(
                    rx.el.h1(
                        t(lang, "Archives", "Archivo"),
                        class_name="text-4xl font-light text-gray-800 mb-8",
                    ),
                    class_name="mb-8",
                ),
                sp_card(
                    rx.foreach(
                        ArchivesState.all_posts_flat, lambda post: archive_entry(post, lang)
                    ),
                    class_name="max-w-4xl",
                ),
                class_name="container mx-auto max-w-5xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang),
        lang=lang,
        route="/blog/archives",
        id="content-area",
    )
