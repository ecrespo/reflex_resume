"""Blog pages - using static route generation like Reflex official blog."""

import reflex as rx
from reflex_silverpoint_react import sp_button, sp_card, sp_pagination, sp_tag

from web.blog.paths import blog_data
from web.components.layout import site_shell
from web.components.navbar import blog_navbar
from web.i18n import LANGS, localize, t
from web.states.blog_state import BlogState

MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"
META_SEPARATOR = "text-[#5C7B71] mx-2"


def post_card(post, lang: str = "en") -> rx.Component:
    """Card for displaying a post in the blog list."""
    return rx.el.article(
        rx.link(
            sp_card(
                rx.el.div(
                    rx.el.span(post["formatted_date"], class_name="text-sm text-[#3E6A5E]"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    sp_tag(post["category"], tone=2, size="sm"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    rx.el.span(post["author"], class_name="text-sm text-[#3E6A5E]"),
                    class_name="flex items-center flex-wrap mb-3",
                ),
                rx.el.p(
                    post["summary"],
                    class_name="text-[#1F3D36] text-sm line-clamp-3 mb-4",
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
                    rx.el.h1("Blog", class_name="text-3xl font-bold text-[#1F3D36] mb-2"),
                    rx.el.p(
                        t(
                            lang,
                            "Articles on Python, software development, data science and more.",
                            "Artículos sobre Python, desarrollo de software, ciencia de datos y más.",
                        ),
                        class_name="text-[#3E6A5E]",
                    ),
                    rx.el.div(
                        rx.el.span(BlogState.total_posts, class_name="font-bold text-[#2F6F86]"),
                        t(lang, " published articles", " artículos publicados"),
                        class_name="text-sm text-[#3E6A5E] mt-2",
                    ),
                    class_name="mb-8",
                ),
                # Posts grid
                rx.el.div(
                    rx.foreach(
                        BlogState.current_page_posts_es
                        if lang == "es"
                        else BlogState.current_page_posts,
                        lambda post: post_card(post, lang),
                    ),
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


def post_body(post_data: dict) -> str:
    """The post's markdown, with image paths served from assets and without a leading
    `# Title` that repeats the page heading."""
    body = post_data["content"].replace("./images/", "/blog/images/").lstrip()
    first, _, rest = body.partition("\n")
    if first.startswith("# ") and first[2:].strip().lower() == post_data["title"].strip().lower():
        body = rest.lstrip()
    return body


def create_post_page(post_data: dict, lang: str = "en") -> rx.Component:
    """The page of one post; `post_data` is the post in `lang` (`BlogPost.to_dict`)."""
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
                        class_name="text-3xl md:text-4xl font-bold text-[#1F3D36] leading-tight mb-4",
                    ),
                    rx.el.div(
                        rx.el.span(post_data["formatted_date"], class_name="text-[#3E6A5E]"),
                        rx.el.span(" • ", class_name=META_SEPARATOR),
                        sp_tag(post_data["category"], tone=2, size="sm"),
                        rx.el.span(" • ", class_name=META_SEPARATOR),
                        rx.el.span(
                            t(lang, "By", "Por"),
                            rx.el.span(
                                post_data["author"], class_name="text-[#1F3D36] font-medium"
                            ),
                            class_name="text-[#3E6A5E] inline-flex gap-1",
                        ),
                        class_name="flex items-center flex-wrap text-sm mb-6",
                    ),
                    class_name="mb-8 pb-6 border-b border-[#5C7B71]/40",
                ),
                # Content
                rx.el.article(
                    rx.markdown(
                        post_body(post_data),
                        class_name="prose prose-lg max-w-none",
                    ),
                    # Spanish when the post has no English translation yet.
                    lang=post_data["lang"],
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
        for lang in LANGS:
            route = localize(f"/blog/{slug}", lang)
            post_data = post.to_dict(lang)

            # Create a closure to capture the post data for this specific route
            # This is the key pattern used by Reflex official blog
            def make_page(data=post_data, lang=lang):
                return lambda: create_post_page(data, lang)

            routes.append((route, make_page(), post_data["title"], lang))

    return routes


# Generate all blog post routes
blog_post_routes = get_blog_routes()
