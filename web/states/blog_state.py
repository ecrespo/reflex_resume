"""Blog state management for pagination and filtering."""

import reflex as rx

from web.blog.paths import sorted_posts


class BlogState(rx.State):
    """State management for the blog listing page."""

    # Pagination state
    current_page: int = 1
    posts_per_page: int = 10

    @rx.var
    def total_posts(self) -> int:
        """Get total number of posts."""
        return len(sorted_posts)

    @rx.var
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        return max(1, (len(sorted_posts) + self.posts_per_page - 1) // self.posts_per_page)

    def _page(self, lang: str) -> list[dict]:
        """The current page's cards in `lang` (no bodies: the list never shows them)."""
        start = (self.current_page - 1) * self.posts_per_page
        return [post.card(lang) for post in sorted_posts[start : start + self.posts_per_page]]

    @rx.var
    def current_page_posts(self) -> list[dict]:
        """The current page's posts in English."""
        return self._page("en")

    @rx.var
    def current_page_posts_es(self) -> list[dict]:
        """The current page's posts in Spanish."""
        return self._page("es")

    @rx.var
    def has_previous_page(self) -> bool:
        """Check if there is a previous page."""
        return self.current_page > 1

    @rx.var
    def has_next_page(self) -> bool:
        """Check if there is a next page."""
        return self.current_page < self.total_pages

    def next_page(self):
        """Navigate to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        """Navigate to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1

    def go_to_page(self, page: int):
        """Navigate to a specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page

    def reset_to_first_page(self):
        """Reset pagination to the first page."""
        self.current_page = 1
