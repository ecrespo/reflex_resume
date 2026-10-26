"""Blog pages - using static route generation like Reflex official blog."""

import reflex as rx
from reflex_silverpoint_react import sp_button, sp_card, sp_pagination, sp_tag

from web.blog.paths import blog_data
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import LANGS, localize, t
from web.states.blog_state import BlogState

MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"
META_SEPARATOR = "text-gray-400 mx-2"


def date_field(lang: str) -> str:
    """The post field holding its date in `lang`."""
    return "formatted_date_es" if lang == "es" else "formatted_date"


def post_card(post, lang: str = "en") -> rx.Component:
    """Card for displaying a post in the blog list."""
    return rx.el.article(
        rx.link(
            sp_card(
                rx.el.div(
                    rx.el.span(post[date_field(lang)], class_name="text-sm text-gray-500"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    sp_tag(post["category"], tone=2, size="sm"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    rx.el.span(post["author"], class_name="text-sm text-gray-600"),
                    class_name="flex items-center flex-wrap mb-3",
                ),
                rx.el.p(
                    post["summary"],
                    class_name="text-gray-700 text-sm line-clamp-3 mb-4",
                ),
                rx.el.span(
                    t(lang, "Read more →", "Leer más →"),
                    class_name="text-[#2F6F86] font-medium text-sm group-hover:underline",
                ),
                title=post["title"],
                class_name="h-full",
            ),
            href=localize("/blog/", lang) + post["slug"].to(str),
            class_name="block h-full",
        ),
        class_name="group hover:shadow-md transition-shadow rounded-lg",
    )


def pagination(lang: str = "en") -> rx.Component:
    """Pagination controls."""
    return rx.el.div(
        sp_pagination(
            total=BlogState.total_posts,
            page_size=BlogState.posts_per_page,
            current=BlogState.current_page,
            on_change=BlogState.go_to_page,
            label=t(lang, "Blog pages", "Páginas del blog"),
            previous_label=t(lang, "Previous", "Anterior"),
            next_label=t(lang, "Next", "Siguiente"),
            page_label=t(lang, "Page", "Página"),
        ),
        class_name="flex items-center justify-center mt-8 mb-4",
    )


def blog_list_page(lang: str = "en") -> rx.Component:
    """Blog listing page with paginated posts."""
    return site_shell(
        rx.el.main(
            rx.el.div(
                # Header
                rx.el.header(
                    rx.el.h1("Blog", class_name="text-3xl font-bold text-gray-900 mb-2"),
                    rx.el.p(
                        t(
                            lang,
                            "Articles on Python, software development, data science and more. "
                            "The posts are written in Spanish.",
                            "Artículos sobre Python, desarrollo de software, ciencia de datos y más.",
                        ),
                        class_name="text-gray-600",
                    ),
                    rx.el.div(
                        rx.el.span(BlogState.total_posts, class_name="font-bold text-[#2F6F86]"),
                        t(lang, " published articles", " artículos publicados"),
                        class_name="text-sm text-gray-500 mt-2",
                    ),
                    class_name="mb-8",
                ),
                # Posts grid
                rx.el.div(
                    rx.foreach(BlogState.current_page_posts, lambda post: post_card(post, lang)),
                    class_name="grid gap-6 grid-cols-1 lg:grid-cols-2",
                ),
                # Pagination
                rx.cond(BlogState.total_pages > 1, pagination(lang), rx.fragment()),
                class_name="container mx-auto max-w-5xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang),
        lang=lang,
        route="/blog",
        id="content-area",
    )


def create_post_page(post_data: dict, lang: str = "en") -> rx.Component:
    """Create a component for a specific blog post.

    The posts are written in Spanish; `lang` is the language of the page around them.
    """
    return site_shell(
        rx.el.main(
            rx.el.div(
                # Back button
                rx.el.div(
                    sp_button(
                        t(lang, "← Back to the blog", "← Volver al blog"),
                        href=localize("/blog", lang),
                    ),
                    class_name="mb-6",
                ),
                # Header
                rx.el.header(
                    rx.el.h1(
                        post_data["title"],
                        class_name="text-3xl md:text-4xl font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.span(post_data[date_field(lang)], class_name="text-gray-500"),
                        rx.el.span(" • ", class_name=META_SEPARATOR),
                        sp_tag(post_data["category"], tone=2, size="sm"),
                        rx.el.span(" • ", class_name=META_SEPARATOR),
                        rx.el.span(t(lang, "By ", "Por "), class_name="text-gray-600"),
                        rx.el.span(post_data["author"], class_name="text-gray-800 font-medium"),
                        class_name="flex items-center flex-wrap text-sm mb-6",
                    ),
                    class_name="mb-8 pb-6 border-b border-gray-200",
                ),
                # Content
                rx.el.article(
                    rx.markdown(
                        post_data["content"].replace("./images/", "/blog/images/"),
                        class_name="prose prose-lg max-w-none",
                    ),
                    # The post itself is in Spanish on both versions of the page.
                    lang="es",
                    class_name="post-content",
                ),
                class_name="container mx-auto max-w-4xl",
            ),
            class_name=MAIN_PADDING_CLASS,
        ),
        top=blog_navbar(lang),
        lang=lang,
        route=f"/blog/{post_data['slug']}",
    )


def get_blog_routes():
    """Generate static routes for all blog posts.

    This follows the same pattern as Reflex official blog:
    - Iterate over all posts
    - Create a static route for each one
    - Use a closure to capture the post data
    """
    routes = []

    for slug, post in blog_data.items():
        post_data = post.to_dict()
        for lang in LANGS:
            route = localize(f"/blog/{slug}", lang)

            # Create a closure to capture the post data for this specific route
            # This is the key pattern used by Reflex official blog
            def make_page(data=post_data, lang=lang):
                return lambda: create_post_page(data, lang)

            routes.append((route, make_page(), post_data["title"], lang))

    return routes


# Generate all blog post routes
blog_post_routes = get_blog_routes()
