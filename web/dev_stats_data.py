"""Static data for the `/dev-stats` page.

Results of an exploratory data analysis of the GitHub account `ecrespo`: 269
repositories cloned as `git clone --bare --filter=blob:none` and their history
flattened to a CSV, then aggregated with pandas.

The figures live here as module constants on purpose. The site is exported as a
static frontend and the unauthenticated GitHub API allows 60 requests per hour,
so a render-time call would both break the build and tie the page to a quota.
`DATA_AS_OF` is surfaced in the page footer so readers know the cut-off.

Field names follow the schemas of the `reflex-rosencharts` components that
consume them (`key`/`value`, `date`/`value`, `topic`/`value`, `name`/`value`,
`revenue`/`value`/`company`); they are passed through to the underlying TSX
unchanged and must not be renamed.
"""

DATA_AS_OF = "2026-09-13"

GITHUB_USER = "ecrespo"
GITHUB_URL = f"https://github.com/{GITHUB_USER}"

# --------------------------------------------------------------------------- #
# 1. Hero
# --------------------------------------------------------------------------- #

HERO_STATS = [
    {"value": "269", "label": "Repositories analysed", "detail": "128 original, 141 forks"},
    {"value": "28,103", "label": "Commits processed", "detail": "across every branch and tag"},
    {"value": "20.7", "label": "Years of history", "detail": "first commit: 6 Jan 2006"},
    {"value": "43", "label": "D3 charts ported to Python", "detail": "the reflex-rosencharts set"},
]

HERO_METHOD_LEAD = "Every repository was cloned with"
HERO_METHOD_COMMAND = "git clone --bare --filter=blob:none"
HERO_METHOD_TAIL = (
    " — a partial clone that pulls the commit graph and directory trees but no file "
    "contents. 269 repositories, 71 MB, 17 seconds, zero failures."
)

# Commit counts below are the subset authored by the account owner, in original
# repositories, with merge commits excluded: 3,253 of the 28,103 processed. The
# page labels them that way so the two totals are never confused.
AUTHORED_COMMITS_TOTAL = 3253
AUTHORED_SCOPE = "Authored commits, original repositories, merge commits excluded"

# --------------------------------------------------------------------------- #
# 2. Yearly activity — bar_chart_vertical: [{"key", "value"}], input order kept
# --------------------------------------------------------------------------- #

ANNUAL_COMMITS = [
    {"key": "2006", "value": 22},
    {"key": "2009", "value": 97},
    {"key": "2010", "value": 39},
    {"key": "2011", "value": 16},
    {"key": "2012", "value": 60},
    {"key": "2013", "value": 2},
    {"key": "2014", "value": 1},
    {"key": "2015", "value": 151},
    {"key": "2016", "value": 133},
    {"key": "2017", "value": 2},
    {"key": "2018", "value": 120},
    {"key": "2019", "value": 966},
    {"key": "2020", "value": 349},
    {"key": "2021", "value": 35},
    {"key": "2022", "value": 99},
    {"key": "2023", "value": 59},
    {"key": "2024", "value": 122},
    {"key": "2025", "value": 202},
    {"key": "2026", "value": 778},
]

# --------------------------------------------------------------------------- #
# 3. The acceleration — line_chart_pulse: [{"date": "YYYY-MM-DD", "value"}]
# --------------------------------------------------------------------------- #

_MONTHLY_SERIES = {
    2024: [0, 0, 8, 0, 22, 8, 23, 12, 17, 19, 5, 8],
    2025: [3, 10, 1, 0, 0, 9, 7, 21, 10, 41, 66, 34],
    2026: [9, 94, 130, 59, 66, 193, 85, 61, 81],
}

# No time zone on purpose: a bare "YYYY-MM-DD" is parsed by `new Date()` as UTC
# midnight, which west of Greenwich is the previous day, so axis labels read
# "12/31" for January. A date-time without an offset is parsed as local time.
MONTHLY_COMMITS = [
    {"date": f"{year}-{month:02d}-01T00:00:00", "value": value}
    for year, values in _MONTHLY_SERIES.items()
    for month, value in enumerate(values, start=1)
]

# Averages over the two regimes either side of the October 2025 inflection.
MONTHLY_BEFORE = 10  # Jan 2024 → Sep 2025
MONTHLY_AFTER = 76  # Oct 2025 → Sep 2026
MONTHLY_SPEEDUP = "7.6x"

# --------------------------------------------------------------------------- #
# 4. Process maturity — bar_chart_benchmark: [{"key", "value"}]
#
# The component highlights the row at index 0 as the benchmark, so the years run
# newest first and the highlighted row is the headline figure.
# --------------------------------------------------------------------------- #

CONVENTION_ADOPTION = [
    {"key": "2026", "value": 84.2},
    {"key": "2025", "value": 22.8},
    {"key": "2024", "value": 17.2},
    {"key": "2023", "value": 15.3},
    {"key": "2022", "value": 11.1},
    {"key": "2021", "value": 5.7},
    {"key": "2020", "value": 4.3},
]

SUBJECT_LENGTH_BEFORE = 18  # median characters, 2024
SUBJECT_LENGTH_AFTER = 66  # median characters, 2025-2026

# --------------------------------------------------------------------------- #
# 5. Built vs studied — radar_chart_rounded: [{"topic", "value"}]
# --------------------------------------------------------------------------- #

TOPICS_BUILT = [
    {"topic": "AI / Agents", "value": 19.5},
    {"topic": "Reflex", "value": 21.1},
    {"topic": "Web / API", "value": 15.6},
    {"topic": "Data / ML", "value": 12.5},
    {"topic": "Linux / CLI", "value": 10.2},
    {"topic": "DevOps", "value": 4.7},
]

TOPICS_STUDIED = [
    {"topic": "AI / Agents", "value": 38.3},
    {"topic": "Reflex", "value": 0.0},
    {"topic": "Web / API", "value": 12.1},
    {"topic": "Data / ML", "value": 15.6},
    {"topic": "Linux / CLI", "value": 0.7},
    {"topic": "DevOps", "value": 9.2},
]

# --------------------------------------------------------------------------- #
# 6. Code composition — treemap_chart: nested hierarchy for d3.hierarchy.
#    Top-level children are the colour groups; their children are the leaves.
# --------------------------------------------------------------------------- #

CODE_COMPOSITION = {
    "name": "root",
    "children": [
        {
            "name": "Code",
            "children": [
                {"name": "Python", "value": 3259},
                {"name": "JavaScript", "value": 1926},
                {"name": "TypeScript", "value": 96},
                {"name": "Shell", "value": 63},
                {"name": "Go", "value": 25},
            ],
        },
        {
            "name": "Markup",
            "children": [
                {"name": "HTML", "value": 1861},
                {"name": "CSS", "value": 252},
            ],
        },
        {
            "name": "Docs",
            "children": [
                {"name": "Markdown", "value": 1118},
                {"name": "Text", "value": 91},
            ],
        },
        {
            "name": "Data & Config",
            "children": [
                {"name": "Data / CSV", "value": 552},
                {"name": "YAML / TOML", "value": 170},
                {"name": "Jupyter", "value": 130},
                {"name": "JSON", "value": 91},
            ],
        },
    ],
}

FILES_TOTAL = 9692
FILES_CLASSIFIED = sum(
    leaf["value"] for group in CODE_COMPOSITION["children"] for leaf in group["children"]
)
MARKDOWN_SHARE = "11.5%"

# --------------------------------------------------------------------------- #
# 7. Portfolio split — donut_chart_center_text: [{"name", "value"}]
# --------------------------------------------------------------------------- #

# `donut_chart_center_text` prints each slice as `value%`, so the slices must
# carry percentages, not counts.
# Slice labels are drawn outside the ring and clip against the card, so the
# names stay short; the absolute counts live in the section headline.
PORTFOLIO_SPLIT = [
    {"name": "Original", "value": 47.6},
    {"name": "Forks", "value": 52.4},
]

PORTFOLIO_TOTAL = "269"

LICENSES = [
    {"name": "MIT", "value": 86},
    {"name": "GPLv3", "value": 40},
    {"name": "Other", "value": 21},
    {"name": "Apache-2.0", "value": 16},
    {"name": "GPLv2", "value": 7},
]

# --------------------------------------------------------------------------- #
# 8. Weekly rhythm — bar_chart_breakdown: [{"key", "value", "color"}].
#    One segmented bar, input order preserved: weekend segments carry the accent.
# --------------------------------------------------------------------------- #

_WEEKDAY_COLOR = "from-slate-300 to-slate-400 dark:from-slate-500 dark:to-slate-700"
_WEEKEND_COLOR = "from-teal-300 to-teal-400 dark:from-teal-500 dark:to-teal-700"

WEEKDAY_RHYTHM = [
    {"key": "Mon", "value": 200, "color": _WEEKDAY_COLOR},
    {"key": "Tue", "value": 390, "color": _WEEKDAY_COLOR},
    {"key": "Wed", "value": 293, "color": _WEEKDAY_COLOR},
    {"key": "Thu", "value": 229, "color": _WEEKDAY_COLOR},
    {"key": "Fri", "value": 260, "color": _WEEKDAY_COLOR},
    {"key": "Sat", "value": 852, "color": _WEEKEND_COLOR},
    {"key": "Sun", "value": 1029, "color": _WEEKEND_COLOR},
]

WEEKEND_SHARE = "57.8%"
NIGHT_SHARE = "0.4%"  # commits between midnight and 6 a.m.

# --------------------------------------------------------------------------- #
# 9. Repo -> release funnel — funnel_chart: [{"key", "value", "color"}].
#    Stages are re-sorted descending by the component; ours already are.
#    Keys stay short: the narrow stages at the bottom clip long labels.
# --------------------------------------------------------------------------- #

DELIVERY_FUNNEL = [
    {
        "key": "Repositories",
        "value": 269,
        "color": "from-teal-200 to-teal-300 dark:from-teal-500 dark:to-teal-700",
    },
    {
        "key": "Original",
        "value": 128,
        "color": "from-teal-300 to-teal-400 dark:from-teal-500 dark:to-teal-700",
    },
    {
        "key": "Branch / PR",
        "value": 46,
        "color": "from-cyan-300 to-cyan-400 dark:from-cyan-500 dark:to-cyan-700",
    },
    {
        "key": "Tags",
        "value": 17,
        "color": "from-sky-300 to-sky-400 dark:from-sky-500 dark:to-sky-700",
    },
    {
        "key": "PyPI",
        "value": 12,
        "color": "from-slate-400 to-slate-500 dark:from-slate-500 dark:to-slate-700",
    },
]

# --------------------------------------------------------------------------- #
# 10. Repository lifecycle — scatter_chart: [{"revenue", "value", "company"}].
#     The field names come from the original rosencharts example and are wired
#     into the TSX: `revenue` is the x axis (days from first to last commit),
#     `value` the y axis (commits), `company` the tooltip label (repository).
#
#     The component builds its x domain from `data[0]` and `data[-1]` rather than
#     from the min/max, so the rows MUST stay sorted ascending by `revenue`;
#     any other order yields negative hover-band widths and a broken axis.
# --------------------------------------------------------------------------- #

REPO_LIFECYCLE = [
    {"company": "omagnome", "revenue": 1, "value": 53},
    {"company": "reflex-mapcn", "revenue": 1, "value": 38},
    {"company": "mcp-joke-server", "revenue": 1, "value": 34},
    {"company": "fastapi_todos", "revenue": 16, "value": 43},
    {"company": "vigia-eew", "revenue": 19, "value": 46},
    {"company": "quiz", "revenue": 28, "value": 47},
    {"company": "prismal", "revenue": 143, "value": 440},
    {"company": "python-android_sms", "revenue": 229, "value": 138},
    {"company": "ecrespo-localpaquetes", "revenue": 273, "value": 46},
    {"company": "reflex_resume", "revenue": 287, "value": 50},
    {"company": "python-autoaccesibilidad", "revenue": 403, "value": 49},
    {"company": "tutorial_fastAPI", "revenue": 1409, "value": 45},
    {"company": "pysms-send", "revenue": 2345, "value": 29},
    {"company": "ecrespo.github.io", "revenue": 2609, "value": 1451},
]

# --------------------------------------------------------------------------- #
# 11. Live contributions calendar — reflex-react-github-calendar.
#     The component fetches the account's contribution data in the visitor's
#     browser from github-contributions-api.jogruber.de, so this section is the
#     only one on the page that is live rather than frozen at DATA_AS_OF.
# --------------------------------------------------------------------------- #

CALENDAR_THEME = {
    "light": ["#e8eddf", "#99d5c9", "#5cb8a7", "#2f9184", "#1d6f66"],
    "dark": ["#e8eddf", "#99d5c9", "#5cb8a7", "#2f9184", "#1d6f66"],
}

CALENDAR_LABELS = {"totalCount": "{{count}} contributions in the last year"}

CALENDAR_ERROR = "GitHub's contributions API is unreachable right now."

# --------------------------------------------------------------------------- #
# Closing cards
# --------------------------------------------------------------------------- #

FLAGSHIP_PROJECTS = [
    {
        "name": "prismal",
        "url": "https://github.com/prismal-ai",
        "tagline": "Multi-agent orchestration on top of LangGraph. MIT.",
        "facts": [
            "440 commits in 143 days (3.1 a day, sustained)",
            "18 versioned releases",
            "67 merge commits — real branch and PR flow",
            "35 test commits: the only repository with real test volume in its history",
        ],
    },
    {
        "name": "reflex-rosencharts",
        "url": f"{GITHUB_URL}/reflex-rosencharts",
        "tagline": "43 D3 + Tailwind charts ported to Reflex, in pure Python. MIT.",
        "facts": [
            "One of 24 Reflex components, 12 of them published to PyPI",
            "Eleven components released between 14 and 24 June 2026",
            "The charts on this very page are built with it",
        ],
    },
]
