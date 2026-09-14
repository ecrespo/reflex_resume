"""Sections of the `/dev-stats` page.

Each section pairs one `reflex-rosencharts` chart with the prose and the headline
figure that carry the same point, so the section still reads with the chart
ignored. `chart_figure` is the single builder behind all of them; it also emits a
screen-reader-only table with the chart's numbers, because a bare D3 drawing
exposes nothing to assistive technology.
"""

import reflex as rx
import reflex_rosencharts as rxc
from reflex_react_github_calendar import github_calendar

from ..dev_stats_data import (
    ANNUAL_COMMITS,
    AUTHORED_COMMITS_TOTAL,
    AUTHORED_SCOPE,
    CALENDAR_ERROR,
    CALENDAR_LABELS,
    CALENDAR_THEME,
    CODE_COMPOSITION,
    CONVENTION_ADOPTION,
    DATA_AS_OF,
    DELIVERY_FUNNEL,
    FILES_CLASSIFIED,
    FILES_TOTAL,
    FLAGSHIP_PROJECTS,
    GITHUB_URL,
    GITHUB_USER,
    HERO_METHOD_COMMAND,
    HERO_METHOD_LEAD,
    HERO_METHOD_TAIL,
    HERO_STATS,
    LICENSES,
    MARKDOWN_SHARE,
    MONTHLY_AFTER,
    MONTHLY_BEFORE,
    MONTHLY_COMMITS,
    MONTHLY_SPEEDUP,
    NIGHT_SHARE,
    PORTFOLIO_SPLIT,
    PORTFOLIO_TOTAL,
    REPO_LIFECYCLE,
    REPO_LIFECYCLE_EXCLUDED,
    SUBJECT_LENGTH_AFTER,
    SUBJECT_LENGTH_BEFORE,
    TOPICS_BUILT,
    TOPICS_STUDIED,
    WEEKDAY_RHYTHM,
    WEEKEND_SHARE,
)
from ..states.dev_stats_state import DevStatsState
from .resume_sections import section_heading

_CARD = "w-full bg-white rounded-lg shadow-md px-4 py-8 sm:px-6 md:px-10 md:py-12"
_LEAD = "text-gray-700 leading-relaxed mb-6 max-w-3xl"
_HEADLINE = "text-3xl md:text-4xl font-bold text-gray-900"
_HEADLINE_LABEL = "text-sm uppercase tracking-wide text-gray-500 mt-1"
_FOOTNOTE = "text-sm text-gray-600 mt-4 max-w-3xl"


def _sr_table(caption: str, headers: list[str], rows: list[list]) -> rx.Component:
    """Screen-reader-only table carrying the same numbers as the chart.

    `sr-only` goes on a wrapping div, not on the table: a table's used width can
    never fall below its min-content width, so `width: 1px` alone would leave it
    sticking out of the layout and pushing the page sideways.
    """
    return rx.el.div(
        rx.el.table(
            rx.el.caption(caption),
            rx.el.thead(rx.el.tr(*[rx.el.th(header, scope="col") for header in headers])),
            rx.el.tbody(
                *[rx.el.tr(*[rx.el.td(str(cell)) for cell in row]) for row in rows],
            ),
        ),
        class_name="sr-only",
    )


def chart_figure(
    *,
    section_id: str,
    title: str,
    lead: str,
    chart: rx.Component,
    headline: str,
    headline_label: str,
    table_caption: str,
    table_headers: list[str],
    table_rows: list[list],
    footnote: str | None = None,
    min_height: str = "min-h-[18rem]",
    scrollable: bool = False,
) -> rx.Component:
    """One page section: heading, lead, chart card, headline figure, footnote.

    The chart sits in a box with an explicit minimum height because every
    rosencharts component is a `NoSSRComponent` that mounts client-side; without
    it the page jumps when the charts hydrate.
    """
    return rx.el.section(
        section_heading(title),
        rx.el.p(lead, class_name=_LEAD),
        rx.el.figure(
            rx.el.div(
                chart,
                class_name=f"w-full {min_height}" + (" overflow-x-auto" if scrollable else ""),
                custom_attrs={"aria-hidden": "true"},
            ),
            _sr_table(table_caption, table_headers, table_rows),
            rx.el.figcaption(
                rx.el.p(headline, class_name=_HEADLINE),
                rx.el.p(headline_label, class_name=_HEADLINE_LABEL),
                class_name="mt-8 border-t border-gray-200 pt-6",
            ),
            class_name=_CARD,
        ),
        rx.el.p(footnote, class_name=_FOOTNOTE) if footnote else rx.fragment(),
        id=section_id,
        class_name="mb-16 scroll-mt-24",
    )


# --------------------------------------------------------------------------- #
# 1. Hero
# --------------------------------------------------------------------------- #


def _stat_card(stat: dict) -> rx.Component:
    return rx.el.div(
        rx.el.p(stat["value"], class_name="text-4xl font-bold text-gray-900"),
        rx.el.p(stat["label"], class_name="text-base font-semibold text-gray-700 mt-2"),
        rx.el.p(stat["detail"], class_name="text-sm text-gray-500 mt-1"),
        class_name="bg-white rounded-lg shadow-md p-6",
    )


def hero_section() -> rx.Component:
    """Key figures and a note on how the data was collected."""
    return rx.el.section(
        section_heading("Dev Stats"),
        rx.el.p(
            "Anyone can say they have been programming for twenty years. This is the "
            "measurement: an exploratory analysis of every commit in my GitHub account, "
            "read straight from git history rather than estimated.",
            class_name=_LEAD,
        ),
        rx.el.div(
            *[_stat_card(stat) for stat in HERO_STATS],
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        rx.el.p(
            rx.el.span(f"{HERO_METHOD_LEAD} "),
            rx.el.code(
                HERO_METHOD_COMMAND,
                class_name="bg-gray-100 text-gray-800 rounded px-1.5 py-0.5 text-sm",
            ),
            rx.el.span(HERO_METHOD_TAIL),
            class_name=_FOOTNOTE,
        ),
        id="overview",
        class_name="mb-16 scroll-mt-24",
    )


# --------------------------------------------------------------------------- #
# 2-10. Chart sections
# --------------------------------------------------------------------------- #


def yearly_activity_section() -> rx.Component:
    """Commits per year, 2006 to 2026."""
    return chart_figure(
        section_id="yearly-activity",
        title="Twenty years, no gaps",
        lead=(
            "The first commit is dated 6 January 2006 and there has not been an empty year "
            "since 2012. Counts below are "
            f"{AUTHORED_SCOPE.lower()} — {AUTHORED_COMMITS_TOTAL:,} of the 28,103 commits "
            "processed."
        ),
        chart=rxc.bar_chart_vertical(data=DevStatsState.annual_commits),
        headline="778 commits in 2026",
        headline_label="spread across 39 new repositories",
        table_caption="Authored commits per year",
        table_headers=["Year", "Commits"],
        table_rows=[[row["key"], row["value"]] for row in ANNUAL_COMMITS],
        footnote=(
            "The 2019 spike (966 commits) is almost entirely the blog's automated static "
            "generation, not hand-written work."
        ),
    )


def acceleration_section() -> rx.Component:
    """Monthly commits across the October 2025 inflection."""
    return chart_figure(
        section_id="acceleration",
        title="The inflection was October 2025",
        lead=(
            "Monthly commits from January 2024 onward. The step up in October 2025 has held "
            "for twelve months, which makes it a new regime rather than a spike."
        ),
        chart=rxc.line_chart_pulse(data=DevStatsState.monthly_commits),
        headline=f"{MONTHLY_BEFORE} → {MONTHLY_AFTER} commits/month",
        headline_label=f"a {MONTHLY_SPEEDUP} acceleration, sustained for a year",
        table_caption="Authored commits per month, January 2024 to September 2026",
        table_headers=["Month", "Commits"],
        table_rows=[[row["date"][:7], row["value"]] for row in MONTHLY_COMMITS],
    )


def process_maturity_section() -> rx.Component:
    """Conventional Commits adoption and commit-subject length."""
    return chart_figure(
        section_id="process-maturity",
        title="Process improved in steps, not ramps",
        lead=(
            "Share of commits following the Conventional Commits specification "
            "(feat / fix / docs / test / ci). Two discrete jumps: in 2025 messages stopped "
            "being labels and became descriptions; in 2026 the convention became the default."
        ),
        chart=rxc.bar_chart_benchmark(data=DevStatsState.convention_adoption),
        headline="84.2% in 2026",
        headline_label=(
            f"median commit subject: {SUBJECT_LENGTH_BEFORE} characters in 2024, "
            f"{SUBJECT_LENGTH_AFTER} in 2025-2026"
        ),
        table_caption="Share of commits following Conventional Commits, by year",
        table_headers=["Year", "Conventional commits (%)"],
        table_rows=[[row["key"], row["value"]] for row in CONVENTION_ADOPTION],
        footnote="Years run newest first; the top row is the chart's highlighted benchmark.",
        min_height="min-h-[33rem]",
    )


def built_vs_studied_section() -> rx.Component:
    """Topic mix of original repositories against forks."""
    return rx.el.section(
        section_heading("What I build vs. what I study"),
        rx.el.p(
            "The same six topics, measured twice: as a share of my original repositories, and "
            "as a share of the repositories I fork to read. Forks run one to two years ahead "
            "of production — today's forks predict the code of 2028.",
            class_name=_LEAD,
        ),
        rx.el.div(
            rx.el.figure(
                rx.el.h3(
                    "Built — original repos",
                    class_name="text-xl font-semibold text-gray-700 text-center",
                ),
                rx.el.div(
                    rxc.radar_chart_rounded(data=DevStatsState.topics_built),
                    class_name="w-full min-h-[20rem]",
                    custom_attrs={"aria-hidden": "true"},
                ),
                _sr_table(
                    "Share of original repositories by topic",
                    ["Topic", "Share (%)"],
                    [[row["topic"], row["value"]] for row in TOPICS_BUILT],
                ),
                class_name=_CARD,
            ),
            rx.el.figure(
                rx.el.h3(
                    "Studied — forks",
                    class_name="text-xl font-semibold text-gray-700 text-center",
                ),
                rx.el.div(
                    rxc.radar_chart_rounded(data=DevStatsState.topics_studied),
                    class_name="w-full min-h-[20rem]",
                    custom_attrs={"aria-hidden": "true"},
                ),
                _sr_table(
                    "Share of forked repositories by topic",
                    ["Topic", "Share (%)"],
                    [[row["topic"], row["value"]] for row in TOPICS_STUDIED],
                ),
                class_name=_CARD,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
        ),
        rx.el.div(
            rx.el.p("19.5% → 38.3%", class_name=_HEADLINE),
            rx.el.p(
                "AI and agents: share of what I build, share of what I read",
                class_name=_HEADLINE_LABEL,
            ),
            class_name="mt-6",
        ),
        id="built-vs-studied",
        class_name="mb-16 scroll-mt-24",
    )


def code_composition_section() -> rx.Component:
    """File-type composition of the original repositories."""
    return chart_figure(
        section_id="code-composition",
        title="Python, with Markdown as a second language",
        lead=(
            f"File-type composition across the {FILES_TOTAL:,} files in the original "
            f"repositories ({FILES_CLASSIFIED:,} of them classified below). Much of the "
            "JavaScript and HTML is compiled output rather than written code, so the real "
            "profile is close to monolingual Python."
        ),
        chart=rxc.treemap_chart(data=DevStatsState.code_composition),
        headline=f"{MARKDOWN_SHARE} Markdown",
        headline_label="one file in nine is documentation",
        table_caption="Files by group and type",
        table_headers=["Group", "Type", "Files"],
        table_rows=[
            [group["name"], leaf["name"], leaf["value"]]
            for group in CODE_COMPOSITION["children"]
            for leaf in group["children"]
        ],
        footnote=(
            "Working with Spec-Driven Design leaves a measurable trace in the file tree: the "
            "specs are committed alongside the code."
        ),
        min_height="min-h-[16rem]",
        scrollable=True,
    )


def portfolio_split_section() -> rx.Component:
    """Original repositories against forks, plus the licence mix."""
    return rx.el.section(
        section_heading("A portfolio and a reading library"),
        rx.el.p(
            "Just over half of the account is forks. Those are not abandoned copies: they are "
            "the reading list, which is why they are counted separately from the work.",
            class_name=_LEAD,
        ),
        rx.el.div(
            rx.el.figure(
                rx.el.div(
                    rxc.donut_chart_center_text(
                        data=DevStatsState.portfolio_split,
                        center_text=PORTFOLIO_TOTAL,
                    ),
                    class_name="w-full min-h-[20rem]",
                    custom_attrs={"aria-hidden": "true"},
                ),
                _sr_table(
                    "Repositories by kind",
                    ["Kind", "Share (%)"],
                    [[row["name"], row["value"]] for row in PORTFOLIO_SPLIT],
                ),
                class_name=_CARD,
            ),
            rx.el.div(
                rx.el.h3("Licences", class_name="text-xl font-semibold text-gray-700 mb-4"),
                rx.el.ul(
                    *[
                        rx.el.li(
                            rx.el.span(row["name"], class_name="font-medium text-gray-800"),
                            rx.el.span(str(row["value"]), class_name="text-gray-600 tabular-nums"),
                            class_name="flex justify-between border-b border-gray-100 py-2",
                        )
                        for row in LICENSES
                    ],
                ),
                rx.el.p(
                    "The MIT-over-GPL crossover dates the cultural shift of the Python "
                    "ecosystem almost as precisely as carbon dating.",
                    class_name=_FOOTNOTE,
                ),
                class_name=_CARD,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
        ),
        rx.el.div(
            rx.el.p("128 original · 141 forks", class_name=_HEADLINE),
            rx.el.p("269 repositories analysed in total", class_name=_HEADLINE_LABEL),
            class_name="mt-6",
        ),
        id="portfolio-split",
        class_name="mb-16 scroll-mt-24",
    )


def weekly_rhythm_section() -> rx.Component:
    """Commit distribution across the days of the week."""
    return chart_figure(
        section_id="weekly-rhythm",
        title="The code gets written on Sundays",
        lead=(
            "One bar, split by day of the week from Monday to Sunday. Saturday and Sunday "
            "together take more of it than Monday, Tuesday and Wednesday combined."
        ),
        chart=rxc.bar_chart_breakdown(data=DevStatsState.weekday_rhythm),
        headline=f"{WEEKEND_SHARE} on weekends",
        headline_label=f"and only {NIGHT_SHARE} between midnight and 6 a.m.",
        table_caption="Authored commits by day of the week",
        table_headers=["Day", "Commits"],
        table_rows=[[row["key"], row["value"]] for row in WEEKDAY_RHYTHM],
        footnote=(
            "A sustainable rhythm rather than an all-nighter habit: the work is episodic and "
            "concentrated — 397 active days, a median of 3 commits on an active day, and a "
            "maximum of 126 in one."
        ),
        min_height="min-h-[5rem]",
    )


def delivery_funnel_section() -> rx.Component:
    """Maturity funnel from repository to published package."""
    return chart_figure(
        section_id="delivery-funnel",
        title="From repository to release",
        lead=(
            "Not every repository is meant to ship, and the funnel says how many actually do: "
            "how many are original work, how many show real branch and PR flow, how many carry "
            "tagged releases, and how many end up installable."
        ),
        # Bar widths are proportional to the value, so on a phone the 17 and 12
        # stages shrink to a few pixels and their labels collide. A minimum
        # width keeps every stage legible; the card scrolls horizontally instead.
        chart=rx.el.div(
            rxc.funnel_chart(data=DevStatsState.delivery_funnel),
            class_name="min-w-[48rem]",
        ),
        headline="269 → 12",
        headline_label="repositories that reach a published PyPI package",
        table_caption="Repositories at each delivery stage",
        table_headers=["Stage", "Repositories"],
        table_rows=[[row["key"], row["value"]] for row in DELIVERY_FUNNEL],
        min_height="min-h-[18rem]",
        scrollable=True,
    )


def repo_lifecycle_section() -> rx.Component:
    """Lifespan against commit count for the most active repositories."""
    return chart_figure(
        section_id="repo-lifecycle",
        title="Sprints and marathons",
        lead=(
            "Each point is a repository: horizontally, the days between its first and last "
            "commit; vertically, how many commits it holds. The upper left is compressed "
            "sprints; the right is the long-running projects. Hover a point for its name."
        ),
        chart=rxc.scatter_chart(data=DevStatsState.repo_lifecycle),
        headline="53 commits in one day",
        headline_label="omagnome: 173 files, a single sitting",
        table_caption="Lifespan and commit count of the most active repositories",
        table_headers=["Repository", "Lifespan (days)", "Commits"],
        table_rows=[[row["company"], row["revenue"], row["value"]] for row in REPO_LIFECYCLE],
        footnote=(
            f"Not plotted: {REPO_LIFECYCLE_EXCLUDED['company']}, with "
            f"{REPO_LIFECYCLE_EXCLUDED['value']:,} commits over "
            f"{REPO_LIFECYCLE_EXCLUDED['revenue']:,} days, most of them the blog's automated "
            "static generation rather than hand-written work. On the same axes it would "
            "squash every other repository into one corner."
        ),
        # Not scrollable: 0.2.2 sizes the x ticks to the available width, and an
        # overflow-x container would clip the last tick label at the right edge.
        min_height="min-h-[20rem]",
    )


def contributions_section() -> rx.Component:
    """Live GitHub contributions calendar."""
    return rx.el.section(
        section_heading("The last twelve months, day by day"),
        rx.el.p(
            "Every other figure on this page is frozen at the analysis date. This one is "
            "live: the calendar is fetched from GitHub in your browser when the page loads, "
            "so it always shows the trailing year as it stands today.",
            class_name=_LEAD,
        ),
        rx.el.div(
            rx.el.div(
                github_calendar(
                    username=GITHUB_USER,
                    color_scheme="light",
                    block_size=12,
                    block_margin=4,
                    font_size=13,
                    theme=CALENDAR_THEME,
                    labels=CALENDAR_LABELS,
                    error_message=CALENDAR_ERROR,
                ),
                class_name="w-full min-h-[9rem] overflow-x-auto",
            ),
            class_name=_CARD,
        ),
        id="contributions",
        class_name="mb-16 scroll-mt-24",
    )


# --------------------------------------------------------------------------- #
# Closing cards and footer
# --------------------------------------------------------------------------- #


def _flagship_card(project: dict) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            project["name"],
            href=project["url"],
            target="_blank",
            rel="noopener noreferrer",
            class_name="text-2xl font-bold text-blue-600 hover:text-blue-800 hover:underline",
        ),
        rx.el.p(project["tagline"], class_name="text-gray-700 mt-2"),
        rx.el.ul(
            *[
                rx.el.li(fact, class_name="text-gray-600 text-sm py-1 border-b border-gray-100")
                for fact in project["facts"]
            ],
            class_name="mt-4",
        ),
        class_name=_CARD,
    )


def flagship_section() -> rx.Component:
    """The two projects the numbers single out."""
    return rx.el.section(
        section_heading("Two projects the numbers single out"),
        rx.el.div(
            *[_flagship_card(project) for project in FLAGSHIP_PROJECTS],
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
        ),
        id="flagship-projects",
        class_name="mb-16 scroll-mt-24",
    )


def dev_stats_footer() -> rx.Component:
    """Data cut-off and a link to the source account."""
    return rx.el.p(
        rx.el.span(f"Figures as of {DATA_AS_OF}. Source: "),
        rx.el.a(
            GITHUB_URL,
            href=GITHUB_URL,
            target="_blank",
            rel="noopener noreferrer",
            class_name="text-blue-600 hover:text-blue-800 hover:underline",
        ),
        rx.el.span(". Charts built with reflex-rosencharts."),
        class_name="text-sm text-gray-600 border-t border-gray-200 pt-6",
    )
