import reflex as rx

from ..timeline_data import certification_headlines


class CertificationsState(rx.State):
    """Tracks which slide of the certifications timeline is on screen."""

    # Slide id reported by TimelineJS through the component's `on_change` event.
    current_slide_id: str = ""

    @rx.var
    def current_certification(self) -> str:
        """Headline of the current slide, falling back to its raw id."""
        if not self.current_slide_id:
            return ""
        return certification_headlines.get(self.current_slide_id, self.current_slide_id)

    @rx.event
    def on_slide_change(self, unique_id: str):
        """Store the slide TimelineJS just navigated to."""
        self.current_slide_id = unique_id
