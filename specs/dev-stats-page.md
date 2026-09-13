# Spec — `/dev-stats` page

| Field | Value |
|---|---|
| **Status** | `APPROVED — implemented 2026-09-13` |
| **Author** | Ernesto Crespo |
| **Date** | 2026-09-13 |
| **Route** | `/dev-stats` — "Dev Stats \| Seraph's Resume" |

## 1. Goal

A data-portfolio page presenting the EDA of the GitHub account (269 repositories,
20.7 years of history). Someone arriving from LinkedIn should understand, in ~30
seconds of scrolling, **what gets built, at what pace, and with what discipline**.
Every section must read correctly from its prose and its headline number alone —
the chart is reinforcement, not the only carrier of meaning.

## 2. Files

| File | Role | Status |
|---|---|---|
| `web/dev_stats_data.py` | Static EDA constants + `DATA_AS_OF = "2026-09-13"` | new |
| `web/states/dev_stats_state.py` | `DevStatsState(rx.State)` exposing the data as vars | new |
| `web/components/dev_stats_sections.py` | Page sections + shared `chart_figure()` helper | new |
| `web/web.py` | `app.add_page(dev_stats_page, route="/dev-stats", …)` | edit |
| `web/components/navbar.py` | "Dev Stats" link in both navbars | edit |

`reflex-rosencharts>=0.2.1` is already a dependency (added earlier this session);
the Skills section already renders `rxc.radar_chart_rounded`, and this page reuses
that card pattern (`_CHART_CARD` in `web/components/skills_chart.py`).

**No live GitHub API call.** The site is exported statically and the unauthenticated
API is capped at 60 req/hour; a render-time call would break the build. Data is
frozen in `dev_stats_data.py` with `DATA_AS_OF` shown in the page footer.

## 3. Sections

Component names and data schemas below are **verified against the v0.2.1 source**,
not inferred. Every chart is `rx.NoSSRComponent` and renders an empty container on
`data=[]` (no exception).

| # | Section | Component | Data schema | Headline |
|---|---|---|---|---|
| 1 | Hero — key figures | — (4 stat cards) | — | 269 repos · 28,103 commits · 20.7 years · 43 D3 charts ported |
| 2 | Yearly activity | `bar_chart_vertical` | `[{key, value}]` | 778 commits in 2026 across 39 repos |
| 3 | The acceleration | `line_chart_pulse` | `[{date: "YYYY-MM-01", value}]` | 10 → 76 commits/month (7.6×) |
| 4 | Process maturity | `bar_chart_benchmark` | `[{key, value}]` | 84.2 % Conventional Commits in 2026 |
| 5 | What I build vs. what I study | 2 × `radar_chart_rounded` | `[{topic, value}]` | AI/Agents: 19.5 % built, 38.3 % studied |
| 6 | Code composition | `treemap_chart` | nested `{name, children:[{name, children:[{name, value}]}]}` | 1 file in 9 is documentation |
| 7 | Portfolio split | `donut_chart_center_text` | `[{name, value}]` + `center_text="269"` | 128 original · 141 forks |
| 8 | Weekly rhythm | `bar_chart_breakdown` | `[{key, value, color}]` | 57.8 % of commits land on the weekend |
| 9 | Repo → release funnel | `funnel_chart` | `[{key, value, color}]` | 269 repos → 12 PyPI packages |
| 10 | Repository lifecycle | `scatter_chart` | `[{revenue, value, company}]` | 53 commits in a single day (`omagnome`) |
| 11 | Live contributions calendar | `github_calendar` (reflex-react-github-calendar) | `username` + theme/label props | the trailing year, fetched live |
| — | Flagship projects | — (2 link cards) | — | `prismal` · `reflex-rosencharts` |

### Component behaviours that shape the design

- **§4 `bar_chart_benchmark`** highlights the row at **index 0** as the benchmark.
  The years are therefore ordered **2026 first**, descending, so the highlighted row
  is the headline (84.2 %) rather than the worst year.
- **§8 `bar_chart_breakdown`** is *one* thick horizontal bar split into proportional
  segments — not seven separate bars. It keeps input order, so Mon→Sun is preserved
  and Sat+Sun visibly occupy 57.8 % of the band. Weekdays slate, weekend teal.
- **§9 `funnel_chart`** re-sorts descending internally (our data already is) and needs
  real Tailwind gradient strings; the source prompt left them as `"..."`, so the spec
  assigns a teal→slate ramp matching the site accent.
- **§10 `scatter_chart`** field names (`revenue`/`value`/`company`) are hardwired in the
  TSX. Mapping: `revenue` = days between first and last commit (X), `value` = commits (Y),
  `company` = repository name (tooltip). Axis labels in the section prose carry the real
  meaning. *(Worth an upstream issue: prop aliases `x`/`y`/`label` would make this chart
  general-purpose.)*
- **§2/§8** `bar_chart_vertical` preserves input order; `bar_chart_gradient` and
  `bar_chart_horizontal` sort descending internally, which is why neither is used for
  chronological or weekday series.

## 4. Shared building blocks

```python
def chart_figure(title, description, chart, table_rows, headline, footnote=None) -> rx.Component
```

One helper renders every section: `h2` title, 1–2 sentences of context, the chart inside
a white card with an explicit `min-h-*` (NoSSR components mount client-side; a fixed
height prevents hydration layout shift), the headline number below in large type, and an
optional footnote. `table_rows` renders a `sr-only` `<table>` with the same numbers —
a bare D3 chart is not accessible on its own, and `aria-hidden` goes on the chart wrapper.

Headings reuse `resume_sections.section_heading`; cards reuse the `_CHART_CARD` classes.

## 5. Layout

- Same shell as `/`: teal sidebar, cream `#f5f5dc` content, Inter, `md:ml-96` offset, navbar.
- One section per row; §5 is a 2-column grid collapsing to 1 column below `md`.
- Hero stat cards: 4 → 2 → 1 columns at `lg` / `md` / mobile.
- `overflow-x-auto` on §6 and §10 only (treemap and scatter need horizontal room).
- Verified at 375 / 768 / 1440 px.
- Charts ship `dark:` Tailwind classes; the `darkMode: "class"` fix already in
  `rxconfig.py` keeps them light on this light-pinned site.

## 6. Acceptance criteria

1. `reflex run` starts with no new console warnings.
2. All 10 sections render **real data**, never the components' bundled example datasets.
3. "Dev Stats" appears in both navbars and navigates correctly.
4. `reflex export --frontend-only` completes.
5. Correct at 375 / 768 / 1440 px.
6. No chart raises with `data=[]`.
7. `ruff check`, `ruff format --check`, `bandit` clean.

## 7. Resolved decisions

- **Two commit totals (option A).** The hero keeps "28,103 commits processed"; §2 and §8
  are labelled *authored commits, original repositories, merge commits excluded (3,253)*,
  so both numbers are true and the scope of each is explicit.
- **Navigation.** "Dev Stats" is the last link in both navbars, and the first cross-page
  link in the main one (the rest are in-page anchors).

## 8. Found during implementation

- **`scatter_chart` requires x-sorted input.** Its x domain is built from `data[0]` and
  `data[-1]` rather than from min/max, so unsorted rows produce negative hover-band widths
  and a broken axis. `REPO_LIFECYCLE` is therefore kept sorted ascending by `revenue`, and
  the data module says so. Worth an upstream issue alongside the prop-alias one.
- **`sr-only` cannot go on a `<table>`.** A table's used width never falls below its
  min-content width, so `width: 1px` leaves it overflowing the viewport. The class goes on
  a wrapping `div` instead.
- **Chart container heights are per-section.** Each rosencharts component renders at its own
  intrinsic height (54px for the breakdown bar, 520px for the benchmark); one shared floor
  left most cards mostly empty.
- **§10 stays `scatter_chart`.** It was briefly swapped for a treemap because
  `ecrespo.github.io` (1,451 commits over 2,609 days) stretches both axes and clusters the
  other 13 repositories; the scatter was restored on request. The outlier is now left out
  of the plotted series (`REPO_LIFECYCLE_EXCLUDED`) so the sprint/marathon pattern is
  visible, and the footnote names it with its figures rather than hiding it. Still open
  upstream: the x axis labels every fifth data point instead of regular ticks, so the 1-
  and 28-day labels overlap, and the y domain has no top padding.
- **Three charts were legible-but-wrong and are fixed.** `donut_chart_center_text` appends a
  hardcoded `%` to every slice value, so the raw counts rendered as "128%"/"141%" — the
  slices now carry percentages and the counts moved to the headline, and the names were
  shortened because the labels are drawn outside the ring and clip against the card.
  `funnel_chart` clips the labels of its narrow bottom stages, so the stage keys are short.
  `line_chart_pulse` and `scatter_chart` pin a 25px y-axis label gutter inline, which wraps
  every three-digit tick over two lines; a `!important` custom-property override scoped to
  `.dev-stats-page` widens it to 46px (inline custom properties lose to `!important` ones).
- **§11 is the only live section.** The calendar fetches from
  `github-contributions-api.jogruber.de` in the visitor's browser, so it carries an
  `error_message` and degrades to one line of text when that host is unreachable (verified).
- **Tailwind `content` was missing `app_components/`.** An earlier fix added
  `public/external/` so the classes inside the rosencharts `.tsx` sources are generated, but
  class names written in Python compile to `.web/app_components/`, which stayed outside the
  globs. The gradient `from-*`/`to-*` strings that §8 and §9 pass as data were absent from
  the production CSS until `./app_components/**/*.{js,ts,jsx,tsx}` was added in `rxconfig.py`.
- **Prerendering needs prod mode.** `reflex export --frontend-only` emits only `index.html`
  and `404.html` unless `REFLEX_SSR=1` (or a genuine prod-mode invocation); with it the
  export contains 825 HTML files including `dev-stats.html`.
