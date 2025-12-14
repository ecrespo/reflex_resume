"""Blog UI components."""
import reflex as rx
from typing import Dict, Any

from web.states.blog_state import BlogState


def post_card(post: Dict[str, Any]) -> rx.Component:
    """
    Card component for displaying a post in the list view.
    
    Args:
        post: Dictionary with post data (title, date, category, summary, author, slug)
    """
    return rx.el.article(
        rx.link(
            rx.el.div(
                # Title
                rx.el.h3(
                    post['title'],
                    class_name="text-xl font-bold text-gray-900 mb-2 group-hover:text-[#4a9bba] transition-colors",
                ),
                # Meta info
                rx.el.div(
                    rx.el.span(
                        post['formatted_date'],
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.span(
                        " • ",
                        class_name="text-gray-400 mx-2",
                    ),
                    rx.el.span(
                        post['category'],
                        class_name="text-sm text-[#4a9bba] font-medium",
                    ),
                    rx.el.span(
                        " • ",
                        class_name="text-gray-400 mx-2",
                    ),
                    rx.el.span(
                        post['author'],
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="flex items-center flex-wrap mb-3",
                ),
                # Summary
                rx.el.p(
                    post['summary'],
                    class_name="text-gray-700 text-sm line-clamp-3 mb-4",
                ),
                # Tags
                rx.cond(
                    len(post['tags']) > 0,
                    rx.el.div(
                        rx.foreach(
                            post['tags'][:3],
                            lambda tag: rx.el.span(
                                tag,
                                class_name="inline-block bg-[#73cbb6] text-gray-800 text-xs px-2 py-1 rounded mr-2 mb-1",
                            ),
                        ),
                        class_name="flex flex-wrap",
                    ),
                    rx.fragment(),
                ),
                # Read more indicator
                rx.el.div(
                    rx.el.span(
                        "Leer más →",
                        class_name="text-[#4a9bba] font-medium text-sm group-hover:underline",
                    ),
                    class_name="mt-4",
                ),
                class_name="p-6",
            ),
            href=f"/blog/{post['slug']}",
            class_name="block",
        ),
        class_name="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-200 overflow-hidden group",
    )


def post_card_from_dict(post: rx.Var[Dict[str, Any]]) -> rx.Component:
    """
    Card component that works with rx.Var for use with rx.foreach.
    """
    return rx.el.article(
        rx.link(
            rx.el.div(
                # Title
                rx.el.h3(
                    post['title'],
                    class_name="text-xl font-bold text-gray-900 mb-2 group-hover:text-[#4a9bba] transition-colors",
                ),
                # Meta info
                rx.el.div(
                    rx.el.span(
                        post['formatted_date'],
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.span(
                        " • ",
                        class_name="text-gray-400 mx-2",
                    ),
                    rx.el.span(
                        post['category'],
                        class_name="text-sm text-[#4a9bba] font-medium",
                    ),
                    rx.el.span(
                        " • ",
                        class_name="text-gray-400 mx-2",
                    ),
                    rx.el.span(
                        post['author'],
                        class_name="text-sm text-gray-600",
                    ),
                    class_name="flex items-center flex-wrap mb-3",
                ),
                # Summary
                rx.el.p(
                    post['summary'],
                    class_name="text-gray-700 text-sm line-clamp-3 mb-4",
                ),
                # Read more indicator
                rx.el.div(
                    rx.el.span(
                        "Leer más →",
                        class_name="text-[#4a9bba] font-medium text-sm group-hover:underline",
                    ),
                    class_name="mt-4",
                ),
                class_name="p-6",
            ),
            href=("/blog/" + post['slug'].to(str)),
            class_name="block",
        ),
        class_name="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-200 overflow-hidden group",
    )


def pagination_controls() -> rx.Component:
    """Pagination controls for blog list."""
    return rx.el.div(
        # Previous button
        rx.button(
            "← Anterior",
            on_click=BlogState.previous_page,
            disabled=~BlogState.has_previous_page,
            class_name=rx.cond(
                BlogState.has_previous_page,
                "px-4 py-2 bg-[#4a9bba] text-white rounded-lg hover:bg-[#3a8baa] transition-colors font-medium cursor-pointer",
                "px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed font-medium",
            ),
        ),
        # Page indicator
        rx.el.span(
            "Página ", BlogState.current_page, " de ", BlogState.total_pages,
            class_name="text-gray-700 font-medium mx-4",
        ),
        # Next button
        rx.button(
            "Siguiente →",
            on_click=BlogState.next_page,
            disabled=~BlogState.has_next_page,
            class_name=rx.cond(
                BlogState.has_next_page,
                "px-4 py-2 bg-[#4a9bba] text-white rounded-lg hover:bg-[#3a8baa] transition-colors font-medium cursor-pointer",
                "px-4 py-2 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed font-medium",
            ),
        ),
        class_name="flex items-center justify-center gap-2 mt-8 mb-4",
    )


def blog_header() -> rx.Component:
    """Header for the blog page."""
    return rx.el.header(
        rx.el.h1(
            "Blog",
            class_name="text-3xl font-bold text-gray-900 mb-2",
        ),
        rx.el.p(
            "Artículos sobre Python, desarrollo de software, ciencia de datos y más.",
            class_name="text-gray-600",
        ),
        rx.el.div(
            rx.el.span(
                BlogState.total_posts,
                class_name="font-bold text-[#4a9bba]",
            ),
            rx.text(" artículos publicados"),
            class_name="text-sm text-gray-500 mt-2",
        ),
        class_name="mb-8",
    )


def back_to_blog_button() -> rx.Component:
    """Button to go back to blog list."""
    return rx.link(
        rx.el.div(
            rx.el.span("← Volver al Blog"),
            class_name="inline-flex items-center px-4 py-2 bg-[#4a9bba] text-white rounded-lg hover:bg-[#3a8baa] transition-colors font-medium mb-6",
        ),
        href="/blog",
    )


def post_detail_header(post: rx.Var[Dict[str, Any]]) -> rx.Component:
    """Header for post detail page."""
    return rx.el.header(
        rx.el.h1(
            post['title'],
            class_name="text-3xl md:text-4xl font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.span(
                post['formatted_date'],
                class_name="text-gray-500",
            ),
            rx.el.span(
                " • ",
                class_name="text-gray-400 mx-2",
            ),
            rx.el.span(
                post['category'],
                class_name="text-[#4a9bba] font-medium",
            ),
            rx.el.span(
                " • ",
                class_name="text-gray-400 mx-2",
            ),
            rx.el.span(
                "Por ",
                class_name="text-gray-600",
            ),
            rx.el.span(
                post['author'],
                class_name="text-gray-800 font-medium",
            ),
            class_name="flex items-center flex-wrap text-sm mb-6",
        ),
        class_name="mb-8 pb-6 border-b border-gray-200",
    )


def post_content(content: rx.Var[str]) -> rx.Component:
    """Render post content as markdown."""
    return rx.el.article(
        rx.markdown(
            content,
            class_name="prose prose-lg max-w-none",
        ),
        class_name="post-content",
    )


def post_not_found() -> rx.Component:
    """Component shown when post is not found."""
    return rx.el.div(
        rx.el.h2(
            "Post no encontrado",
            class_name="text-2xl font-bold text-gray-900 mb-4",
        ),
        rx.el.p(
            "El artículo que buscas no existe o ha sido movido.",
            class_name="text-gray-600 mb-6",
        ),
        rx.link(
            rx.el.span(
                "← Volver al Blog",
                class_name="text-[#4a9bba] hover:underline font-medium",
            ),
            href="/blog",
        ),
        class_name="text-center py-16",
    )
