import reflex as rx
import reflex_google_analytics_reactjs as rga
from reflex_silverpoint_react import sp_button

from web.blog.archives import archives_page
from web.blog.blog import blog_list_page, blog_post_routes
from web.blog.categories import categories_page
from web.blog.tags import tags_page
from web.components.dev_dashboard import dev_dashboard
from web.components.home_sections import profile_section, projects_section
from web.components.layout import page_shell
from web.components.portfolio_sections import repositories_section
from web.components.resume_sections import (
    certifications_section,
    education_section,
    portfolio_section,
    skills_list_section,
    social_media_section,
    work_experience_section,
)
from web.components.skills_chart import skills_chart_section
from web.components.theme import themed

# --------------------------------------------------------------------------- #
# Pages: one per navbar entry, each on its own route.
# --------------------------------------------------------------------------- #


def home_page() -> rx.Component:
    """`/` — a profile summary and the main projects."""
    return page_shell(profile_section(), projects_section(), active="/")


_RESUME_SECTIONS = [
    ("Education", "#education"),
    ("Work Experience", "#work-experience"),
    ("Skills", "#skills-list"),
    ("Social Media", "#social-media"),
    ("Certifications", "#certifications"),
]


def _resume_contents() -> rx.Component:
    """In-page links to the sections of the resume."""
    return rx.el.nav(
        *[
            rx.el.a(
                text,
                href=anchor,
                class_name="text-[#2F6F86] hover:text-[#1F3D36] hover:underline whitespace-nowrap",
            )
            for text, anchor in _RESUME_SECTIONS
        ],
        aria_label="Resume sections",
        class_name="flex flex-wrap gap-x-5 gap-y-1 text-sm mb-10",
    )


def resume_page() -> rx.Component:
    """`/resume` — education, work experience, skills, social media and certifications."""
    return page_shell(
        rx.el.div(
            rx.el.h1("Resume", class_name="text-4xl font-bold text-gray-800 mb-3"),
            _resume_contents(),
            education_section(),
            work_experience_section(),
            skills_list_section(),
            skills_chart_section(),
            social_media_section(),
            class_name="container mx-auto",
        ),
        # The certifications timeline is wider than the other sections on desktop.
        rx.el.div(
            certifications_section(),
            class_name="container mx-auto px-4 md:px-8 lg:px-16",
        ),
        active="/resume",
        content_class="w-full",
    )


def not_found_page() -> rx.Component:
    """The 404 page, inside the site's layout so it keeps the navbar and the footer."""
    return page_shell(
        rx.el.section(
            rx.el.p("404", class_name="text-6xl font-bold text-[#2F6F86] mb-2"),
            rx.el.h1("Page not found", class_name="text-3xl font-bold text-gray-800 mb-4"),
            rx.el.p(
                "The page you are looking for does not exist or has moved.",
                class_name="text-gray-700 mb-8",
            ),
            rx.el.div(
                sp_button("Home", href="/", label="Go to the home page"),
                sp_button("Resume", href="/resume", label="Go to the resume"),
                sp_button("Portfolio", href="/portfolio", label="Go to the portfolio"),
                sp_button(
                    "Dev Dashboard Stats",
                    href="/dev-dashboard-stats",
                    label="Go to the GitHub dashboard",
                ),
                class_name="flex flex-wrap gap-3",
            ),
            class_name="py-16",
        ),
        active="",
    )


def portfolio_page() -> rx.Component:
    """`/portfolio` — notebooks, then the repositories."""
    return page_shell(portfolio_section(), repositories_section(), active="/portfolio")


def dev_dashboard_page() -> rx.Component:
    """`/dev-dashboard-stats` — the GitHub EDA as an interactive, filterable dashboard."""
    return page_shell(
        dev_dashboard(),
        active="/dev-dashboard-stats",
        # Tighter than the other pages: the dashboard is sized to fit one screen.
        main_class="px-3 pt-3 pb-1 md:px-6 md:pt-4 md:pb-1 w-full",
        content_class="w-full max-w-[1800px] mx-auto",
    )


app = rx.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        # EB Garamond, silverpoint's typeface, for the whole page. @silverpoint/fonts
        # ships only 400, 500 and italic; Google Fonts adds the 600/700 weights the
        # headings use, so the browser does not synthesise a faux bold.
        rx.el.link(
            href=(
                "https://fonts.googleapis.com/css2?family=EB+Garamond:"
                "ital,wght@0,400..700;1,400..700&display=swap"
            ),
            rel="stylesheet",
        ),
        rx.el.style("""
            html {
                scroll-behavior: smooth;
            }
            body, .radix-themes {
                font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif;
                --default-font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif;
                --heading-font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif;
            }
            /* TimelineJS sets its own sans fonts; icons keep the tl-icons font. */
            .tl-timeline :is(h1, h2, h3, h4, h5, h6, p, a, span, div, blockquote):not([class*="tl-icon"]),
            .sp-timeline .tl-timeline h3.tl-headline-date {
                font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif !important;
            }
            /* silverpoint's skin sets its display font on the slide arrows too,
               which turns the tl-icons glyphs into empty boxes. */
            .sp-timeline .tl-timeline div.tl-slidenav-icon {
                font-family: 'tl-icons' !important;
            }
            /* silverpoint 0.8.0: the charts' screen-reader table and SpTable's
               wrapper share the class `sp-table`, whose `th, td { text-align: right }`
               then right-aligns every SpTable cell and defeats `align: "start"`. */
            .sp-ui-table :is(th, td):not([data-align='end'], [data-align='center']) {
                text-align: start;
            }
            /* Tags keep their hand-drawn frame but drop the hatched tone. */
            .sp-tag > [part="sp-tone"] {
                display: none;
            }
            .prose {
                max-width: none;
            }
            .prose h1 {
                font-size: 2rem;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: #1a202c;
            }
            .prose h2 {
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
                color: #2d3748;
            }
            .prose h3 {
                font-size: 1.25rem;
                font-weight: 600;
                margin-top: 1.25rem;
                margin-bottom: 0.5rem;
                color: #4a5568;
            }
            .prose p {
                margin-bottom: 1rem;
                line-height: 1.75;
                color: #4a5568;
            }
            .prose code {
                background-color: #f7fafc;
                padding: 0.125rem 0.25rem;
                border-radius: 0.25rem;
                font-size: 0.875rem;
            }
            .prose pre {
                background-color: #2d3748;
                color: #e2e8f0;
                padding: 1rem;
                border-radius: 0.5rem;
                overflow-x: auto;
                margin: 1rem 0;
            }
            .prose pre code {
                background-color: transparent;
                padding: 0;
                color: inherit;
            }
            .prose ul, .prose ol {
                margin: 1rem 0;
                padding-left: 1.5rem;
            }
            .prose li {
                margin-bottom: 0.5rem;
            }
            .prose a {
                color: #4a9bba;
                text-decoration: underline;
            }
            .prose a:hover {
                color: #3a8baa;
            }
            .prose img {
                max-width: 100%;
                height: auto;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
            .prose blockquote {
                border-left: 4px solid #4a9bba;
                padding-left: 1rem;
                margin: 1rem 0;
                color: #718096;
                font-style: italic;
            }
            .line-clamp-3 {
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }
            """),
    ],
)

# One silverpoint provider around every page: ground, substrate and the site
# palette reach each chart and component without repeating them.
app.extra_app_wraps[(10, "SilverpointProvider")] = lambda _stateful: themed()

# Google Analytics 4, mounted once above the pages. Settings live in
# `google_analytics.toml`; the measurement id comes from the
# GOOGLE_ANALYTICS_MEASUREMENT_ID environment variable at export time, and
# without it the component stays disabled.
rga.install(app)

# Main pages
_TITLE = "Seraph's Resume"

app.add_page(home_page, route="/", title=_TITLE)
app.add_page(resume_page, route="/resume", title=f"Resume | {_TITLE}")
app.add_page(portfolio_page, route="/portfolio", title=f"Portfolio | {_TITLE}")
# Reflex serves the "404" route for every unknown path.
app.add_page(not_found_page, route="404", title=f"Page not found | {_TITLE}")
app.add_page(
    dev_dashboard_page,
    route="/dev-dashboard-stats",
    title=f"Dev Dashboard Stats | {_TITLE}",
)
app.add_page(blog_list_page, route="/blog", title="Blog | Seraph's Resume")
app.add_page(archives_page, route="/blog/archives", title="Blog Archives")
app.add_page(categories_page, route="/blog/categories", title="Blog Categories")
app.add_page(tags_page, route="/blog/tags", title="Blog Tags")

# Register all blog post pages (statically generated - same pattern as Reflex official blog)
for route, page_fn, title in blog_post_routes:
    app.add_page(page_fn, route=route, title=f"Blog | {title}")
