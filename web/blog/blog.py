"""Blog pages - using static route generation like Reflex official blog."""
import reflex as rx

from web.components.sidebar import sidebar
from web.components.navbar import navbar, blog_navbar
from web.blog.paths import blog_data, sorted_posts
from web.states.blog_state import BlogState


# Common CSS classes
MAIN_LAYOUT_CLASS = "flex min-h-screen font-['Inter'] bg-[#f5f5dc]"
CONTENT_AREA_CLASS = "flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96"
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"
META_SEPARATOR = "text-gray-400 mx-2"


def post_card(post) -> rx.Component:
    """Card for displaying a post in the blog list."""
    return rx.el.article(
        rx.link(
            rx.el.div(
                rx.el.h3(
                    post['title'],
                    class_name="text-xl font-bold text-gray-900 mb-2 group-hover:text-[#4a9bba] transition-colors",
                ),
                rx.el.div(
                    rx.el.span(post['formatted_date'], class_name="text-sm text-gray-500"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    rx.el.span(post['category'], class_name="text-sm text-[#4a9bba] font-medium"),
                    rx.el.span(" • ", class_name=META_SEPARATOR),
                    rx.el.span(post['author'], class_name="text-sm text-gray-600"),
                    class_name="flex items-center flex-wrap mb-3",
                ),
                rx.el.p(
                    post['summary'],
                    class_name="text-gray-700 text-sm line-clamp-3 mb-4",
                ),
                rx.el.span("Leer más →", class_name="text-[#4a9bba] font-medium text-sm group-hover:underline"),
                class_name="p-6",
            ),
            href="/blog/" + post['slug'].to(str),
            class_name="block",
        ),
        class_name="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-200 overflow-hidden group",
    )


def pagination() -> rx.Component:
    """Pagination controls."""
    return rx.el.div(
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
        rx.el.span(
            "Página ", BlogState.current_page, " de ", BlogState.total_pages,
            class_name="text-gray-700 font-medium mx-4",
        ),
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


def blog_list_page() -> rx.Component:
    """Blog listing page with paginated posts."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            blog_navbar(),
            rx.el.main(
                rx.el.div(
                    # Header
                    rx.el.header(
                        rx.el.h1("Blog", class_name="text-3xl font-bold text-gray-900 mb-2"),
                        rx.el.p(
                            "Artículos sobre Python, desarrollo de software, ciencia de datos y más.",
                            class_name="text-gray-600",
                        ),
                        rx.el.div(
                            rx.el.span(BlogState.total_posts, class_name="font-bold text-[#4a9bba]"),
                            " artículos publicados",
                            class_name="text-sm text-gray-500 mt-2",
                        ),
                        class_name="mb-8",
                    ),
                    # Posts grid
                    rx.el.div(
                        rx.foreach(BlogState.current_page_posts, post_card),
                        class_name="grid gap-6 grid-cols-1 lg:grid-cols-2",
                    ),
                    # Pagination
                    rx.cond(BlogState.total_pages > 1, pagination(), rx.fragment()),
                    class_name="container mx-auto max-w-5xl",
                ),
                class_name=MAIN_PADDING_CLASS,
            ),
            class_name=CONTENT_AREA_CLASS,
            id="content-area",
        ),
        class_name=MAIN_LAYOUT_CLASS,
    )


def create_post_page(post_data: dict) -> rx.Component:
    """Create a component for a specific blog post."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            blog_navbar(),
            rx.el.main(
                rx.el.div(
                    # Back button
                    rx.link(
                        rx.el.span(
                            "← Volver al Blog",
                            class_name="inline-flex items-center px-4 py-2 bg-[#4a9bba] text-white rounded-lg hover:bg-[#3a8baa] transition-colors font-medium mb-6",
                        ),
                        href="/blog",
                    ),
                    # Header
                    rx.el.header(
                        rx.el.h1(
                            post_data['title'],
                            class_name="text-3xl md:text-4xl font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.el.span(post_data['formatted_date'], class_name="text-gray-500"),
                            rx.el.span(" • ", class_name=META_SEPARATOR),
                            rx.el.span(post_data['category'], class_name="text-[#4a9bba] font-medium"),
                            rx.el.span(" • ", class_name=META_SEPARATOR),
                            rx.el.span("Por ", class_name="text-gray-600"),
                            rx.el.span(post_data['author'], class_name="text-gray-800 font-medium"),
                            class_name="flex items-center flex-wrap text-sm mb-6",
                        ),
                        class_name="mb-8 pb-6 border-b border-gray-200",
                    ),
                    # Content
                    rx.el.article(
                        rx.markdown(
                            post_data['content'].replace("./images/", "/blog/images/"),
                            class_name="prose prose-lg max-w-none"
                        ),
                        class_name="post-content",
                    ),
                    class_name="container mx-auto max-w-4xl",
                ),
                class_name=MAIN_PADDING_CLASS,
            ),
            class_name=CONTENT_AREA_CLASS,
        ),
        class_name=MAIN_LAYOUT_CLASS,
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
        route = f"/blog/{slug}"
        
        # Create a closure to capture the post data for this specific route
        # This is the key pattern used by Reflex official blog
        def make_page(data=post_data):
            return lambda: create_post_page(data)
        
        routes.append((route, make_page(), post_data['title']))
    
    return routes


# Generate all blog post routes
blog_post_routes = get_blog_routes()
