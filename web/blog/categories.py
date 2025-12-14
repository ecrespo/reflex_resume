import reflex as rx
from collections import defaultdict
from web.components.sidebar import sidebar
from web.components.navbar import blog_navbar
from web.blog.paths import sorted_posts

# Constants
MAIN_LAYOUT_CLASS = "flex min-h-screen font-['Inter'] bg-[#f5f5dc]"
CONTENT_AREA_CLASS = "flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96"
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


def category_entry(item: tuple[str, int]) -> rx.Component:
    category = item[0]
    count = item[1]
    return rx.el.li(
        rx.link(
            rx.el.span(category, class_name="text-[#d05040] hover:underline"),
            f" ({count})",
            href=f"#",
            class_name="text-gray-700 block py-1"
        )
    )

def categories_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            blog_navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.header(
                        rx.el.h1("Categories", class_name="text-4xl font-light text-gray-800 mb-8"),
                        class_name="mb-8",
                    ),
                    rx.el.ul(
                        rx.foreach(
                            CategoriesState.categories_with_counts,
                            category_entry
                        ),
                        class_name="list-none space-y-2"
                    ),
                    class_name="container mx-auto max-w-5xl",
                ),
                class_name=MAIN_PADDING_CLASS,
            ),
            class_name=CONTENT_AREA_CLASS,
            id="content-area",
        ),
        class_name=MAIN_LAYOUT_CLASS,
    )
