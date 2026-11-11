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
from web.i18n import LANGS, localize, page_title, t

# --------------------------------------------------------------------------- #
# Pages: one per navbar entry, each on its own route, in English and in Spanish
# (see `web/i18n.py`).
# --------------------------------------------------------------------------- #


def home_page(lang: str = "en") -> rx.Component:
    """`/` — a profile summary and the main projects."""
    return page_shell(profile_section(lang), projects_section(lang), active="/", lang=lang)


_RESUME_SECTIONS = [
    ({"en": "Education", "es": "Educación"}, "#education"),
    ({"en": "Work Experience", "es": "Experiencia laboral"}, "#work-experience"),
    ({"en": "Skills", "es": "Habilidades"}, "#skills-list"),
    ({"en": "Social Media", "es": "Redes sociales"}, "#social-media"),
    ({"en": "Certifications", "es": "Certificaciones"}, "#certifications"),
]


def _resume_contents(lang: str) -> rx.Component:
    """In-page links to the sections of the resume."""
    return rx.el.nav(
        *[
            rx.el.a(
                text[lang],
                href=anchor,
                class_name="text-[#2F6F86] hover:text-[#1F3D36] hover:underline whitespace-nowrap",
            )
            for text, anchor in _RESUME_SECTIONS
        ],
        aria_label=t(lang, "Resume sections", "Secciones del currículum"),
        class_name="flex flex-wrap gap-x-5 gap-y-1 text-sm mb-10",
    )


def resume_page(lang: str = "en") -> rx.Component:
    """`/resume` — education, work experience, skills, social media and certifications."""
    return page_shell(
        rx.el.div(
            rx.el.h1(
                t(lang, "Resume", "Currículum"), class_name="text-4xl font-bold text-gray-800 mb-3"
            ),
            _resume_contents(lang),
            education_section(lang),
            work_experience_section(lang),
            skills_list_section(lang),
            skills_chart_section(lang),
            social_media_section(lang),
            class_name="container mx-auto",
        ),
        # The certifications timeline is wider than the other sections on desktop.
        rx.el.div(
            certifications_section(lang),
            class_name="container mx-auto px-4 md:px-8 lg:px-16",
        ),
        active="/resume",
        lang=lang,
        content_class="w-full",
    )


def not_found_page() -> rx.Component:
    """The 404 page, inside the site's layout so it keeps the navbar and the footer.

    Reflex serves one 404 page for every unknown path, in either language, so it
    says it in both and offers the way home in each.
    """
    return page_shell(
        rx.el.section(
            rx.el.p("404", class_name="text-6xl font-bold text-[#2F6F86] mb-2"),
            rx.el.h1("Page not found", class_name="text-3xl font-bold text-gray-800 mb-1"),
            rx.el.p(
                "Página no encontrada",
                lang="es",
                class_name="text-2xl italic text-gray-600 mb-4",
            ),
            rx.el.p(
                "The page you are looking for does not exist or has moved.",
                class_name="text-gray-700",
            ),
            rx.el.p(
                "La página que buscas no existe o cambió de dirección.",
                lang="es",
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
                class_name="flex flex-wrap gap-3 mb-3",
            ),
            rx.el.div(
                sp_button("Inicio", href="/es", label="Ir a la página de inicio"),
                sp_button("Currículum", href="/es/resume", label="Ir al currículum"),
                sp_button("Portafolio", href="/es/portfolio", label="Ir al portafolio"),
                sp_button(
                    "Estadísticas de desarrollo",
                    href="/es/dev-dashboard-stats",
                    label="Ir al dashboard de GitHub",
                ),
                lang="es",
                class_name="flex flex-wrap gap-3",
            ),
            class_name="py-16",
        ),
        active="",
        route="/",
    )


def portfolio_page(lang: str = "en") -> rx.Component:
    """`/portfolio` — notebooks, then the repositories."""
    return page_shell(
        portfolio_section(lang), repositories_section(lang), active="/portfolio", lang=lang
    )


def dev_dashboard_page(lang: str = "en") -> rx.Component:
    """`/dev-dashboard-stats` — the GitHub EDA as an interactive, filterable dashboard."""
    return page_shell(
        dev_dashboard(lang),
        active="/dev-dashboard-stats",
        lang=lang,
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
            /* Blog posts (`.post-content`): the site's inks on the cream page,
               EB Garamond for prose, a monospace only for code. rx.markdown renders
               Radix Themes elements (rt-Text, rt-Link, rt-Code) and the code
               highlighter writes its colours inline, hence the specificity and the
               few !important. Inks: theme.SITE_PALETTE. */
            .post-content {
                --post-ink: #1F3D36;
                --post-muted: #3E6A5E;
                --post-accent: #2F6F86;
                --post-green: #2C6355;
                --post-rule: #5C7B71;
                --post-mint: #DFF1EC;
                --post-paper: #FBF8EF;
                color: var(--post-ink);
                font-size: 1.125rem;
                line-height: 1.75;
                overflow-wrap: anywhere;
            }
            .post-content .prose {
                max-width: none;
            }
            .post-content :is(h1, h2, h3, h4, h5, h6) {
                font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif;
                color: var(--post-ink);
                line-height: 1.25;
                letter-spacing: normal;
            }
            .post-content h1 { font-size: 1.875rem; font-weight: 700; margin: 2.25rem 0 1rem; }
            .post-content h2 {
                font-size: 1.5rem; font-weight: 600; margin: 2rem 0 0.75rem;
                padding-bottom: 0.35rem; border-bottom: 1px solid rgba(92, 123, 113, 0.35);
            }
            .post-content h3 { font-size: 1.25rem; font-weight: 600; margin: 1.5rem 0 0.5rem; }
            .post-content :is(h4, h5, h6) {
                font-size: 1.1rem; font-weight: 600; font-style: italic; margin: 1.25rem 0 0.5rem;
            }
            .post-content :is(p, li, td, th, .rt-Text) {
                font-family: 'EB Garamond', 'Iowan Old Style', Georgia, serif;
                font-size: 1.125rem;
                line-height: 1.75;
                color: var(--post-ink);
            }
            .post-content p { margin: 0 0 1.1rem; }
            .post-content :is(strong, b) { font-weight: 600; color: var(--post-ink); }
            .post-content :is(a, .rt-Link) {
                color: var(--post-accent);
                text-decoration: underline;
                text-decoration-thickness: 1px;
                text-underline-offset: 3px;
                text-decoration-color: rgba(47, 111, 134, 0.45);
                transition: color 0.15s, text-decoration-color 0.15s;
            }
            .post-content :is(a, .rt-Link):hover {
                color: var(--post-green);
                text-decoration-color: currentColor;
            }
            .post-content :is(ul, ol) { margin: 0 0 1.25rem; padding-left: 1.5rem; }
            .post-content ul { list-style: disc; }
            .post-content ol { list-style: decimal; }
            .post-content li { margin: 0.3rem 0; padding-left: 0.25rem; }
            .post-content li::marker { color: var(--post-green); }
            .post-content li > :is(p, .rt-Text) { margin: 0; }
            /* Inline code: a mint chip in the ink, without the backticks. */
            .post-content :not(pre) > code,
            .post-content .rt-Code {
                font-family: 'Fira Code', 'JetBrains Mono', Menlo, Consolas, monospace;
                font-size: 0.8em;
                font-weight: 400;
                color: var(--post-ink);
                background: var(--post-mint);
                border: 1px solid rgba(92, 123, 113, 0.3);
                border-radius: 3px;
                padding: 0.05em 0.35em;
            }
            .post-content code::before,
            .post-content code::after {
                content: none !important;
            }
            /* Code blocks: paper with a hairline frame, like the site's cards. */
            .post-content pre {
                background: var(--post-paper) !important;
                border: 1px solid var(--post-rule);
                border-left: 3px solid var(--post-green);
                border-radius: 4px !important;
                padding: 1rem 1.25rem !important;
                margin: 1.25rem 0 1.5rem !important;
                font-size: 0.875rem;
                line-height: 1.6 !important;
                overflow-x: auto;
            }
            .post-content pre code {
                background: transparent !important;
                border: 0;
                padding: 0;
                font-size: inherit;
                white-space: pre !important;
            }
            .post-content blockquote {
                margin: 1.25rem 0;
                padding: 0.5rem 1.25rem;
                border-left: 3px solid var(--post-green);
                background: rgba(223, 241, 236, 0.45);
                color: var(--post-muted);
                font-style: italic;
            }
            .post-content blockquote :is(p, .rt-Text) { color: var(--post-muted); margin: 0.25rem 0; }
            .post-content img {
                display: block;
                max-width: 100%;
                height: auto;
                margin: 1.5rem auto;
                border: 1px solid rgba(92, 123, 113, 0.35);
                border-radius: 4px;
                background: #FFFFFF;
            }
            .post-content iframe {
                display: block;
                max-width: 100%;
                margin: 1.5rem auto;
                border: 1px solid rgba(92, 123, 113, 0.35);
                border-radius: 4px;
            }
            .post-content table {
                display: block;
                max-width: 100%;
                overflow-x: auto;
                border-collapse: collapse;
                margin: 1.25rem 0 1.5rem;
            }
            .post-content :is(th, td) {
                border: 1px solid rgba(92, 123, 113, 0.45);
                padding: 0.4rem 0.75rem;
                text-align: left;
                vertical-align: top;
                font-size: 1rem;
            }
            .post-content th { background: var(--post-mint); font-weight: 600; }
            .post-content tr:nth-child(even) td { background: rgba(251, 248, 239, 0.7); }
            .post-content hr {
                border: 0;
                border-top: 1px solid rgba(92, 123, 113, 0.45);
                margin: 2rem 0;
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

# Every page in both languages: English at its route, Spanish under `/es`.
# (route, page function, English title, Spanish title); an empty title is the site's.
_PAGES = [
    ("/", home_page, "", ""),
    ("/resume", resume_page, "Resume", "Currículum"),
    ("/portfolio", portfolio_page, "Portfolio", "Portafolio"),
    (
        "/dev-dashboard-stats",
        dev_dashboard_page,
        "Dev Dashboard Stats",
        "Estadísticas de desarrollo",
    ),
    ("/blog", blog_list_page, "Blog", "Blog"),
    ("/blog/archives", archives_page, "Blog Archives", "Archivo del blog"),
    ("/blog/categories", categories_page, "Blog Categories", "Categorías del blog"),
    ("/blog/tags", tags_page, "Blog Tags", "Etiquetas del blog"),
]


def _in_language(page, lang: str):
    """`page` bound to `lang`, named after both (Reflex names compiled pages after them)."""

    def localized_page() -> rx.Component:
        return page(lang)

    localized_page.__name__ = f"{page.__name__}_{lang}"
    return localized_page


for _route, _page, _title_en, _title_es in _PAGES:
    for _lang in LANGS:
        app.add_page(
            _in_language(_page, _lang),
            route=localize(_route, _lang),
            title=page_title(_lang, _title_en, _title_es),
        )

# Reflex serves the "404" route for every unknown path.
app.add_page(not_found_page, route="404", title="Page not found | Página no encontrada")

# Register all blog post pages (statically generated - same pattern as Reflex official blog)
for route, page_fn, title, _post_lang, preview in blog_post_routes:
    app.add_page(page_fn, route=route, title=f"Blog | {title}", **preview)
