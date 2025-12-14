import reflex as rx
from web.components.sidebar import sidebar
from web.components.navbar import navbar
from web.components.resume_sections import (
    education_section, 
    work_experience_section,
    portfolio_section,
    skills_list_section,
    social_media_section,
    certifications_section,
)
from web.components.skills_chart import skills_chart_section
from web.states.resume_state import ResumeState
from web.blog.blog import blog_list_page, blog_post_routes
from web.blog.archives import archives_page
from web.blog.categories import categories_page
from web.blog.tags import tags_page


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                # Regular sections with max width
                rx.el.div(
                    education_section(),
                    work_experience_section(),
                    portfolio_section(),
                    skills_list_section(),
                    skills_chart_section(),
                    social_media_section(),
                    class_name="container mx-auto",
                ),
                # Certifications section - full width on desktop
                rx.el.div(
                    certifications_section(),
                    class_name="container mx-auto px-4 md:px-8 lg:px-16",
                ),
                class_name="p-4 md:p-8 lg:p-16 w-full",
            ),
            class_name="flex-1 flex flex-col min-w-0 bg-[#f5f5dc] min-h-screen md:ml-96",
        ),
        class_name="flex min-h-screen font-['Inter'] bg-[#f5f5dc]",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.style("""
            html {
                scroll-behavior: smooth;
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

# Main pages
app.add_page(index, route="/")
app.add_page(blog_list_page, route="/blog", title="Blog | Seraph's Resume")
app.add_page(archives_page, route="/blog/archives", title="Blog Archives")
app.add_page(categories_page, route="/blog/categories", title="Blog Categories")
app.add_page(tags_page, route="/blog/tags", title="Blog Tags")

# Register all blog post pages (statically generated - same pattern as Reflex official blog)
for route, page_fn, title in blog_post_routes:
    app.add_page(page_fn, route=route, title=f"Blog | {title}")