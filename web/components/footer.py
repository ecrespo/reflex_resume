"""The site footer: copyright, the stack the site is built with, social links and contact.

Shared by every page: `components/layout.py` for the main pages and the blog
pages directly. Brand icons are the official marks from Simple Icons
(https://simpleicons.org, CC0 1.0, v8.15.0), drawn inline so they need no
icon font and no network request; the blog and e-mail icons are Lucide icons,
which Reflex ships (`rx.icon`).
"""

from datetime import date

import reflex as rx

from ..resume_data import social_media_data

OWNER = "Ernesto Crespo"
EMAIL = "ecrespo@gmail.com"
SOURCE_URL = "https://github.com/ecrespo/reflex_resume"
LICENSE_URL = f"{SOURCE_URL}/blob/main/LICENSE"

# Simple Icons path data, 24 x 24 viewBox.
_BRAND_PATHS = {
    "GitHub": (
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
    ),
    "GitLab": (
        "m23.6004 9.5927-.0337-.0862L20.3.9814a.851.851 0 0 0-.3362-.405.8748.8748 0 0 0-.9997.0539.8748.8748 0 0 0-.29.4399l-2.2055 6.748H7.5375l-2.2057-6.748a.8573.8573 0 0 0-.29-.4412.8748.8748 0 0 0-.9997-.0537.8585.8585 0 0 0-.3362.4049L.4332 9.5015l-.0325.0862a6.0657 6.0657 0 0 0 2.0119 7.0105l.0113.0087.03.0213 4.976 3.7264 2.462 1.8633 1.4995 1.1321a1.0085 1.0085 0 0 0 1.2197 0l1.4995-1.1321 2.4619-1.8633 5.006-3.7489.0125-.01a6.0682 6.0682 0 0 0 2.0094-7.003z"
    ),
    "LinkedIn": (
        "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
    ),
    "Twitter": (
        "M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"
    ),
    "Medium": (
        "M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"
    ),
}

# Social networks without a brand mark use a Lucide icon instead.
_LUCIDE_FALLBACK = {"Blog": "rss"}

# What the site is made with, in the order a reader would look for it.
BUILT_WITH = [
    ("Python", "https://www.python.org"),
    ("Reflex", "https://reflex.dev"),
    ("reflex-silverpoint-react", "https://pypi.org/project/reflex-silverpoint-react/"),
    ("Tailwind CSS", "https://tailwindcss.com"),
    ("uv", "https://docs.astral.sh/uv/"),
]
HOSTED_ON = [
    ("Vercel", "https://vercel.com"),
    ("Railway", "https://railway.com"),
]

_LINK = "text-[#2F6F86] hover:text-[#1F3D36] hover:underline underline-offset-4"
_ICON_LINK = "text-[#2F6F86] hover:text-[#1F3D36] transition-colors"
_GUTTER = "px-4 md:px-8 lg:px-16"


def _brand_icon(name: str) -> rx.Component:
    if name in _BRAND_PATHS:
        return rx.el.svg(
            rx.el.svg.path(d=_BRAND_PATHS[name]),
            view_box="0 0 24 24",
            fill="currentColor",
            width="18",
            height="18",
            aria_hidden="true",
        )
    return rx.icon(_LUCIDE_FALLBACK.get(name, "link"), size=18, aria_hidden="true")


def _social_link(name: str, url: str) -> rx.Component:
    """An icon-only link; the network's name is its tooltip and accessible name."""
    return rx.el.a(
        _brand_icon(name),
        href=url,
        target="_blank",
        rel="noopener noreferrer",
        title=name,
        aria_label=f"{name} (opens in a new tab)",
        class_name=_ICON_LINK,
    )


def _inline_links(items: list[tuple[str, str]]) -> list[rx.Component]:
    out: list[rx.Component] = []
    for index, (text, url) in enumerate(items):
        if index:
            out.append(rx.el.span(" · ", aria_hidden="true"))
        out.append(
            rx.el.a(text, href=url, target="_blank", rel="noopener noreferrer", class_name=_LINK)
        )
    return out


def site_footer() -> rx.Component:
    """The footer at the bottom of every page: two compact rows."""
    year = date.today().year
    return rx.el.footer(
        rx.el.div(
            # Who, and how to get in touch.
            rx.el.div(
                rx.el.span(OWNER, class_name="font-semibold text-[#1F3D36]"),
                rx.el.a(
                    rx.icon("mail", size=16, aria_hidden="true"),
                    rx.el.span(EMAIL),
                    href=f"mailto:{EMAIL}",
                    aria_label=f"Send an e-mail to {EMAIL}",
                    class_name=f"flex items-center gap-1.5 {_LINK}",
                ),
                class_name="flex flex-wrap items-center gap-x-4 gap-y-1",
            ),
            # The stack.
            rx.el.p(
                rx.el.span("Built with "),
                *_inline_links(BUILT_WITH),
                rx.el.span(" · hosted on "),
                *_inline_links(HOSTED_ON),
                class_name="text-sm text-gray-700",
            ),
            # Social networks.
            rx.el.nav(
                *[_social_link(name, url) for name, url in social_media_data],
                aria_label="Social networks",
                class_name="flex items-center gap-4",
            ),
            class_name=(
                f"flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 {_GUTTER} py-3"
            ),
        ),
        rx.el.div(
            rx.el.span(f"© {year} {OWNER}. All rights reserved."),
            rx.el.span(
                "Source code under the ",
                rx.el.a(
                    "Apache 2.0 License",
                    href=LICENSE_URL,
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name=_LINK,
                ),
                " · ",
                rx.el.a(
                    "View the source",
                    href=SOURCE_URL,
                    target="_blank",
                    rel="noopener noreferrer",
                    class_name=_LINK,
                ),
            ),
            class_name=(
                f"flex flex-col sm:flex-row sm:justify-between gap-1 text-xs text-gray-600 "
                f"{_GUTTER} py-2 border-t border-[#5C7B71]/40"
            ),
        ),
        # mt-auto keeps the footer at the bottom of short pages.
        class_name="mt-auto w-full bg-[#DFF1EC] border-t border-[#5C7B71]/60",
    )
