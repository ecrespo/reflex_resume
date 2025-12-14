import reflex as rx
from collections import defaultdict
from datetime import datetime
from web.components.sidebar import sidebar
from web.components.navbar import blog_navbar
from web.blog.paths import sorted_posts

# Constants
MAIN_LAYOUT_CLASS = "flex min-h-screen font-['Inter'] bg-[#f5f5dc]"
CONTENT_AREA_CLASS = "flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96"
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


def archive_entry(post: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            post['formatted_date'],
            class_name="text-gray-700 font-medium mb-1"
        ),
        rx.link(
            post['title'],
            href="/blog/" + post['slug'].to(str),
            class_name="text-[#d05040] hover:underline text-lg block mb-4 ml-4"
        ),
        class_name="mb-2"
    )

def archives_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            blog_navbar(),
            rx.el.main(
                rx.el.div(
                    rx.el.header(
                        rx.el.h1("Archives", class_name="text-4xl font-light text-gray-800 mb-8"),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ArchivesState.all_posts_flat,
                            archive_entry
                        ),
                        class_name="max-w-4xl"
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
