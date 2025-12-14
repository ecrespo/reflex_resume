import reflex as rx
from ..states.resume_state import ResumeState


def navbar_link(text: str, url: str = "#") -> rx.Component:
    return rx.el.a(
        text,
        href=url,
        class_name="text-white hover:text-white/80 text-sm font-medium hover:underline transition-all whitespace-nowrap",
    )


def blog_navbar_link(text: str, url: str) -> rx.Component:
    """Specific link style for blog navbar (red/orange text on hover as per screenshot implies theme).
    Actually user asked to KEEP main page style. 
    But looking at the screenshots, the blog navbar has a specific look in the second screenshot?
    Wait, the user said: "Tienes que mantener el estilo de la página principal como ya se tiene en los post del blog."
    (You have to maintain the style of the main page as it is already in the blog posts).
    
    The screenshots show:
    Image 1: HOME ARCHIVES CATEGORIES TAGS ATOM (Reddish text)
    Image 2: Categories list (Orange/Reddish links)
    
    However, the current blog uses the blue theme (#4a9bba) from the main resume.
    If I look at `web/blog/blog.py`:
    `navbar()` is used.
    And `navbar()` uses `bg-[#4a9bba]`.
    
    The user request says: "Cuando se muestra los post del blog el navbar debe cambiar a lo siguiente... Tienes que mantener el estilo de la página principal como ya se tiene en los post del blog."
    This is slightly contradictory if the screenshots show a different style (white bg, red text).
    BUT, "mantener el estilo de la página principal" implies keeping the BLUE navbar.
    
    Let's re-read carefully: "Tienes que mantener el estilo de la página principal como ya se tiene en los post del blog."
    This implies the CURRENT blog posts have the main page style (Blue navbar). 
    So I should probably keep the Blue Navbar but CHANGE the links.
    
    The screenshots provided might be from the OLD blog (Pelican) which had white background and red text.
    The user wants the NEW blog (Reflex) to have the links from the OLD blog, but the STYLE of the NEW blog (Main page).
    
    So:
    - Background: #4a9bba (Blue)
    - Text: White
    - Links: Home, Blog, Archives, Categories, Tags, Atom
    """
    return navbar_link(text, url)


def blog_navbar() -> rx.Component:
    """The navigation bar for the blog section."""
    return rx.el.nav(
        rx.el.div(
            # Hamburger menu button for mobile (reusing state)
            rx.el.button(
                rx.el.div(
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white"),
                    class_name="flex flex-col",
                ),
                on_click=ResumeState.toggle_mobile_menu,
                class_name="md:hidden p-2 hover:bg-white/10 rounded",
            ),
            # Navigation links
            blog_navbar_link("HOME", url="/"),
            blog_navbar_link("BLOG", url="/blog"),
            blog_navbar_link("ARCHIVES", url="/blog/archives"),
            blog_navbar_link("CATEGORIES", url="/blog/categories"),
            blog_navbar_link("TAGS", url="/blog/tags"),
            blog_navbar_link("ATOM", url="/feed.xml"),
            class_name="flex flex-row gap-6 items-center overflow-x-auto w-full px-4 md:px-8 h-full no-scrollbar",
        ),
        class_name="w-full h-14 bg-[#4a9bba] flex items-center shadow-sm flex-shrink-0 z-20 sticky top-0",
    )


def navbar() -> rx.Component:
    """The top navigation bar."""
    return rx.el.nav(
        rx.el.div(
            # Hamburger menu button for mobile
            rx.el.button(
                rx.el.div(
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white mb-1.5"),
                    rx.el.span(class_name="block w-6 h-0.5 bg-white"),
                    class_name="flex flex-col",
                ),
                on_click=ResumeState.toggle_mobile_menu,
                class_name="md:hidden p-2 hover:bg-white/10 rounded",
            ),
            # Navigation links
            navbar_link("Education", url="/#education"),
            navbar_link("Work Experience", url="/#work-experience"),
            navbar_link("Portfolio", url="/#portfolio"),
            navbar_link("Skills", url="/#skills"),
            navbar_link("Social Media", url="/#social-media"),
            navbar_link("Certifications", url="/#certifications"),
            class_name="flex flex-row gap-6 items-center overflow-x-auto w-full px-4 md:px-8 h-full no-scrollbar",
        ),
        class_name="w-full h-14 bg-[#4a9bba] flex items-center shadow-sm flex-shrink-0 z-20 sticky top-0",
    )