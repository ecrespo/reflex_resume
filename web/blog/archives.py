import reflex as rx
from reflex_silverpoint_react import sp_card

from web.blog.paths import sorted_posts
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import localize, t

# Constants
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"
META_SEPARATOR = "text-[#5C7B71] mx-2"


def archive_entry(post: dict, lang: str = "en") -> rx.Component:
    """One post of the archive, built at compile time (`BlogPost.card(lang)`)."""
    return rx.el.div(
        rx.el.div(post["formatted_date"], class_name="text-[#3E6A5E] font-medium mb-1"),
        rx.link(
            post["title"],
            href=localize(f"/blog/{post['slug']}", lang),
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
                        class_name="text-4xl font-light text-[#1F3D36] mb-8",
                    ),
                    class_name="mb-8",
                ),
                sp_card(
                    *[archive_entry(post.card(lang), lang) for post in sorted_posts],
                    class_name="max-w-4xl",
                ),
                class_name="container mx-auto max-w-5xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang, active="/blog/archives"),
        lang=lang,
        route="/blog/archives",
        id="content-area",
    )
