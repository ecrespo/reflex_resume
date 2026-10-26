"""Silverpoint theme shared by every page.

The palette starts from the `verdigris` preset, whose teal ink matches the
sidebar, and keeps the site's identity: a paper substrate a shade lighter than
the beige page background, and the navbar blue as the second ink (darkened from
#4a9bba, which fails the 4.5:1 contrast check on the substrate).
`check_palette(SITE_PALETTE)` returns `[]`.
"""

import reflex as rx
from reflex_silverpoint_react import Palette, silverpoint_provider

SITE_PALETTE = Palette(
    substrate="#FBF8EF",
    ink="#2C6355",
    ink_secondary="#2F6F86",
    heighten="#FFFFFF",
    rule="#5C7B71",
    grid="#5C7B71",
    text="#1F3D36",
    text_muted="#3E6A5E",
)


def themed(*children: rx.Component) -> rx.Component:
    """Ground, substrate, palette and locale for every silverpoint element below."""
    return silverpoint_provider(
        *children,
        ground="silverpoint",
        substrate="cream",
        palette=SITE_PALETTE,
        locale="en-US",
    )
