import reflex as rx
from collections import defaultdict
from web.components.sidebar import sidebar
from web.components.navbar import blog_navbar
from web.blog.paths import sorted_posts

# Constants
MAIN_LAYOUT_CLASS = "flex min-h-screen font-['Inter'] bg-[#f5f5dc]"
CONTENT_AREA_CLASS = "flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96"
MAIN_PADDING_CLASS = "p-4 md:p-8 lg:p-16 w-full"


class TagsState(rx.State):
    """State for tags page."""
    
    @rx.var
    def tags_with_counts(self) -> list[tuple[str, int]]:
        """Get list of tags with their post counts."""
        counts = defaultdict(int)
        for post in sorted_posts:
            # post.tags is already a list of strings
            for tag in post.tags:
                tag = tag.strip()
                if tag:
                    counts[tag] += 1
                
        # Sort alphabetically (case insensitive)
        return sorted(counts.items(), key=lambda x: x[0].lower())


def tag_entry(item: tuple[str, int]) -> rx.Component:
    tag = item[0]
    count = item[1]
    return rx.el.li(
        rx.link(
            rx.el.span(tag, class_name="text-[#d05040] hover:underline"),
            f" ({count})",
            href=f"#",
            class_name="text-gray-700 block py-1"
        )
    )

def tags_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            blog_navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.header(
                        rx.el.h1("Tags", class_name="text-4xl font-light text-gray-800 mb-8"),
                        class_name="mb-8",
                    ),
                    rx.el.ul(
                        rx.foreach(
                            TagsState.tags_with_counts,
                            tag_entry
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
