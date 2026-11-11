<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** — up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above — do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs — components, state management, events, styling, database, routing, authentication — use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available — always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal resume site + blog for seraph.to, built with Reflex (Python full-stack framework compiling to a React frontend + FastAPI backend). App package is `web/` (`app_name="web"` in `rxconfig.py`). Python 3.13, dependency manager `uv`. There is no test suite.

## Commands

```bash
uv sync                          # install deps (uv.lock is committed)
uv run reflex init               # generate .web/ on first run
uv run reflex run                # dev server, frontend at http://localhost:3000
API_URL=http://localhost:8000 uv run reflex run   # …wired to the LOCAL backend
uv run reflex export --frontend-only   # static frontend -> frontend.zip

bash build_local.sh              # local static build into public/ (uv sync --frozen + reflex export)
uv run python web/blog/rss.py    # regenerate assets/feed.xml (English) and assets/es/feed.xml (Spanish) — run from repo root
uv run python utils/validate_links.py  # REWRITES old-blog links (Pelican www.seraph.to/<title>.html, ecrespo.github.io, Blogger blog.crespo.org.ve/YYYY/MM/…) to /blog/<slug>, fixes scheme-less links and image paths; --check reports only (exit 1), --external also curl-checks external links
uv run python utils/fetch_certificates.py  # downloads missing certificate images into assets/certificates/

# Same checks as .github/workflows/ci.yml (runs on push/PR to develop and main)
uv run ruff check . && uv run ruff format --check .
uv run bandit -c pyproject.toml -r .
uv run reflex compile
```

CI also runs pip-audit on the exported lock, gitleaks (config in `.gitleaks.toml`; `public/`, `node_modules/` and two old example tokens in blog posts are allowlisted), hadolint (`.hadolint.yaml`) and a Docker build without push. Dev tools (ruff, bandit, pip-audit) live in the `dev` dependency group; the Docker image sets `UV_NO_DEV=1` so they are never installed there.

Note: `uv.lock` is the only lockfile — both build scripts, CI and the Dockerfile install with `uv sync --frozen`, which never updates it. Run `uv lock` (or use `uv add`/`uv remove`) after changing `pyproject.toml`.

## Deployment model

- **Frontend**: static export served by Vercel from `public/` (`vercel.json`; every page is prerendered, so there is no SPA rewrite: an unknown path gets `public/404.html` with a 404 status — a rewrite to `index.html` made React hydrate the home page's HTML as the 404 route, error #418). `.github/workflows/static_build.yml` runs `remote_build.sh` (exports with `API_URL=https://api.seraph.to`) on PRs to `main` as a check, and on push to `main` auto-commits `public/` as "Update static build [skip ci]". Don't hand-edit `public/`.
- **Backend**: Railway builds the Dockerfile on push to `main`; the image runs `reflex run --backend-only` on port 8000 at `api.seraph.to`. `rxconfig.py` sets CORS origins, `state_manager_mode="memory"`, and `api_url` from `$API_URL` (default `https://api.seraph.to`). **A plain `uv run reflex run` therefore points the local frontend at the deployed backend** — state added since the last deploy will not come back in the deltas, so a new computed var looks like it never updates. Run `API_URL=http://localhost:8000 uv run reflex run` when testing state changes.
- Work happens on `develop`; `main` is the deploy branch, protected by the "Protect main" ruleset (changes only via PR with the CI and Static Build checks passing; no force-push or deletion). The Static Build pushes `public/` with the `STATIC_BUILD_DEPLOY_KEY` deploy key, which is the ruleset's bypass actor.

## Architecture

- `web/web.py` — creates `rx.App`, global `<head>` (EB Garamond, `.post-content` CSS for rendered posts in the site's inks: `theme.SITE_PALETTE` colours, mint inline code, paper code blocks; rx.markdown emits Radix `rt-*` elements and inline highlighter styles, hence the scoped selectors), defines one page per navbar entry and registers all routes, each in English and in Spanish (see **Languages** below): `/` (home: profile summary and main projects), `/resume`, `/portfolio`, `/dev-dashboard-stats`, `/blog`, `/blog/archives`, `/blog/categories`, `/blog/tags`, plus one static route per post; the custom 404 is one bilingual page. Every page outside the blog is wrapped by `components/layout.py`'s `page_shell` (sidebar + navbar + main), which passes the page's route to `navbar(active=...)` so the current entry is underlined and carries `aria-current="page"`; the entries live in `navbar.NAV_ITEMS`. Every page, blog included, ends with `components/footer.py`'s `site_footer()`: copyright, the stack, social links (`resume_data.social_media_data`; brand marks are inline Simple Icons paths, CC0, since the Lucide set Reflex ships has no brand icons) and a `mailto:` contact link.
- **Languages (English / Spanish)**: `web/i18n.py`. Every page is compiled twice: English, the default, at its route and Spanish under `/es` (`/es`, `/es/resume`, `/es/blog/<slug>`…), so the static export shows either language without the backend. Page functions take `lang` and pass it down; `localize(route, lang)` builds every internal link, so a reader stays in the language they chose. UI text sits next to the code as `t(lang, "English", "Español")`; data keeps both languages as `{"en": …, "es": …}` values read with `pick` (`home_data.py`), or as English originals plus a Spanish map (`resume_data.ES` + `translate`, `repositories_data.DESCRIPTIONS_ES` / `CATEGORY_TITLES_ES`, `dev_dashboard_data.ES_TERMS`). The sidebar ends with the language switch (`sidebar.language_switch`): the UK and Spain flags as inline SVG, the current one framed, the other a link to the same page in that language (`page_shell`/`site_shell` receive the page's English `route`). State-backed text has Spanish twins as computed vars (`DevDashboardState.*_es`, `ResumeState.selected_skill_es` / `category_average_radar_es`); filter and select keys stay English. Blog posts are written in Spanish and translated to English (`content/posts_en/`, see **Blog**): `/blog/…` shows the English text, `/es/blog/…` the Spanish original. Not translated: certificate titles in the timeline and TimelineJS' own controls. A new page needs both versions: add it to `_PAGES` in `web/web.py`.
- **UI library — silverpoint**: every chart and UI component comes from `reflex-silverpoint-react` (snake_case builders: charts without prefix, e.g. `radar_chart`; UI `sp_…`). `web/web.py` registers one `silverpoint_provider` for the whole app through `app.extra_app_wraps` (`components/theme.py`: `themed()` and `SITE_PALETTE`, a `verdigris`-based palette that passes `check_palette`). Charts take rows plus accessor props (`x_key`, `value_key`, …); without `data` they draw demo rows, so a chart fed by a var that can be empty sits behind `rx.cond`. Each chart renders its own screen-reader table (`data_table="hidden"`). `sp_button`/`sp_surface` forward only declared props: `href` works, `target`/`download` are dropped (the resume PDF uses `rx.download`). The `reflex-silverpoint` Claude Code plugin (skill + `silverpoint` MCP server) documents builders and props; the MCP's Reflex names can lag the installed package (`get_version` → `reflex.stale`), the `.pyi` stubs are the truth.
- **Home page** (`/`): `web/components/home_sections.py` renders `web/home_data.py` — the profile summary (career facts from `resume_data.py`, figures from the GitHub EDA), the main projects (Umbral, Prismal AI, Vigia EEW, LangChain, LangGraph) and their monthly activity as `sparkline_rows`.
- **Resume page** (`/resume`): education, work experience, skills, social media and certifications on one page, with an in-page index to each section's anchor. Content is hardcoded Python data in `web/resume_data.py`, rendered by `web/components/resume_sections.py` (Skills pairs `skills_list_section` with `skills_chart_section`) (`sp_card`, `sp_tag`, `sp_descriptions`, `sp_button`); `web/states/resume_state.py` turns `skills_data` into radar series (`current_skill_radar`, `category_average_radar`, `[{topic, value}]`) rendered by `components/skills_chart.py` with `radar_chart` on a fixed `[0, 5]` domain, the category picked with `sp_select`. Layout is sidebar (`components/sidebar.py`, fixed, `w-60` with a `md:ml-60` offset on the content; on mobile an `sp_drawer` controlled by `ResumeState.mobile_menu_open`) + navbar + main, laid out with Tailwind classes via `class_name` (TailwindV4Plugin).
- **Portfolio page** (`/portfolio`): the notebook links (`resume_sections.portfolio_section`), then **Repositories** (`web/components/portfolio_sections.py`): one `sp_card` per repository, in the home page's project-card style, grouped by category with an in-page index. The data is static in `web/repositories_data.py` (`DATA_AS_OF`): every repository with hand-written commits in the current year (ecrespo + prismal-ai) plus the older LangChain / LangGraph labs and data-science work — commits this year, total, last commit, tags (language + manifest stack) and GitHub / PyPI / site links. Regenerate it from the same git-history pipeline as the dashboard; add or recategorize a repository by editing its entry.
- **Certifications timeline**: `resume_sections.certifications_section` renders silverpoint's `sp_timeline` (Knight Lab TimelineJS with the silverpoint skin; the npm packages, icon fonts included, are bundled by Vite). `web/timeline_data.py` loads `assets/timeline.json` **at import time** as TimelineJS JSON and assigns every slide a deterministic `unique_id`, so `on_change` resolves the active slide to its headline; `web/states/certifications_state.py` holds it. Drive media URLs are swapped at load time for the local copy `assets/certificates/<drive id>.jpg` (linked to the Drive file): Drive's preview iframe letterboxes on black and Google answers browser hotlinks of its thumbnails with 429, so `utils/fetch_certificates.py` downloads them once. A global CSS rule in `web/web.py` restores the `tl-icons` font on the slide arrows, which silverpoint's skin overrides. Add certificates by editing `assets/timeline.json` and restarting the app, then running `utils/fetch_certificates.py` (`web/timeline.json` is a separate, stale copy). See `timeline.md` (Spanish) for the entry format.
- **Dev Dashboard Stats page** (`/dev-dashboard-stats`): an interactive EDA of the GitHub account (`ecrespo` + `prismal-ai`, 3,649 hand-written commits, seven engineering profiles including Forward Deployed Engineer) drawn with silverpoint `dashboard` grids, sized to fit one desktop screen. The figures are pre-aggregated in `web/data/dev_dashboard.json` (one slice per period × engineering profile, plus per-repository details), generated by `utils/github_eda/collect.py` (bare blob-less mirrors in `~/.cache/github-eda`, via `gh`) then `utils/github_eda/build.py` (every definition: owner e-mails, technologies, stack, profiles, impact), loaded at import time by `web/dev_dashboard_data.py` (with `DATA_AS_OF`) — never a render-time GitHub API call, since the frontend is exported statically and the unauthenticated API is capped at 60 req/hour. `web/states/dev_dashboard_state.py` holds the filters and only the slice on screen, with static defaults (the all-time slice), so the charts render even if the backend is unreachable; changing a filter, opening a repository or drilling the treemap are backend events. `web/components/dev_dashboard.py` builds the header, KPI strip and five tabs; each tab's grid fits one screen, and what did not fit scrolls below it (`web/components/dev_dashboard_sections.py`: commits per day as an `activity_grid`, a sortable table of every repository, technology by year, the profile quadrants, profiles and opportunities, and the full impact ranking). silverpoint's `bubble_chart` has no point labels or reference lines, so the labelled quadrants are inline SVG built at compile time (`components/quadrant_chart.py`). silverpoint 0.8.0 gives row-oriented bar charts a fixed 56 px label column, so rows carry a short `label` (`short_label`) with the full name in the tooltip. Spec: `specs/dev-dashboard-stats-page.md`.
- **Google Analytics**: `rga.install(app)` (`reflex-google-analytics-reactjs`) in `web/web.py`, configured by `google_analytics.toml` (`only_in_production = true`: test mode under `reflex run`). The measurement id is read from `GOOGLE_ANALYTICS_MEASUREMENT_ID` at compile/export time — the Static Build passes the repository variable of that name; without it GA stays disabled (`missing_measurement_id`). Custom events use `rga.event(...)` (e.g. `resume_download`).
- **Vercel Web Analytics**: `rva.install(app)` (`reflex-vercel-analytics`, wraps `@vercel/analytics/react`) in `web/web.py`, configured by `vercel_analytics.toml` (`mode = "auto"`: Vercel's debug script, console only, under `reflex run`; production script from `reflex export`). One page view per React Router navigation with its route; query strings are dropped (`include_search = false`). The frontend is served by Vercel, so the default `/_vercel/insights/*` script and endpoints apply; Web Analytics must be enabled in the Vercel project. Fields can be overridden with `VERCEL_ANALYTICS_<FIELD>`. Custom events (`rva.track`) need a Pro plan.
- **Vite dev dependency pre-bundling**: `VitePrebundlePlugin` in `rxconfig.py` adds `optimizeDeps.include` (`@knight-lab/timelinejs`, which `SpTimeline` imports dynamically) to the generated `.web/vite.config.js`. Without it `reflex run` re-optimizes mid-session and fails with "error loading dynamically imported module …/.vite/deps/…?v=…". Add any new dynamically-loaded npm package there (only packages that are installed: an unknown one breaks Vite); after changing it, restart `reflex run` (and `rm -rf .web/node_modules/.vite` if the error persists).
- **Blog** (`web/blog/`):
  - `paths.py` loads every `content/posts/*.md` **at import time** into `blog_data` (slug → `BlogPost`) and `sorted_posts`. Posts use Pelican-style header metadata (`Title:`, `Date:`, `Category:`, `Tags:`, `Slug:`, `Summary:`…) terminated by a blank line; files without `Title` are skipped. Slug comes from `Slug:` or the filename minus its date prefix, then `sanitize_slug` strips to `[a-z0-9_-]`.
  - **English translations**: `content/posts_en/<same file name>` holds each post in English — same `Slug`, `Date`, `Category`, `Tags`; `Title`, `Summary` and body translated, `lang: en`; code blocks, inline code, URLs and images byte-identical. `paths.py` attaches it as `BlogPost.en`; `BlogPost.card(lang)` (list/index fields, no body) and `to_dict(lang)` (plus body) return the post in a language, falling back to the Spanish original (`lang: es` on the article) when there is no translation. Categories and tags stay Spanish in the files and are translated in `web/blog/terms.py` (`CATEGORIES_EN`, `TAGS_EN`; unlisted terms such as library names are the same in both). `BlogState.current_page_posts` / `current_page_posts_es` hold the list page; archives, categories and tags are built statically per language. `utils/check_translations.py [FILE.md …]` validates translations against the originals (header, code blocks, inline code, link targets, length, leftover Spanish). A new or edited post needs its translation updated too.
  - `blog.py` builds `blog_post_routes` — one statically generated page per post via closures (the Reflex official blog pattern). Adding/renaming a post requires restarting the app / re-exporting. `post_preview` gives each post page its link preview (LinkedIn, X, Facebook): the meta description from `Summary`, `og:image` as the absolute URL of the first `./images/` image in the body (`DEFAULT_PREVIEW_IMAGE`, the author's photo, when there is none), and the `og:*` / `twitter:*` tags; a post meant to be shared needs a `Summary` and an image.
  - `archives.py`, `categories.py`, `tags.py` are index pages; `states/blog_state.py` handles list pagination.
  - Post markdown image refs `./images/x.png` are rewritten to `/blog/images/x.png`, served from `assets/blog/images/`. `content/images/` mirrors those images.
  - `rss.py` is a standalone script, not wired into the app: it writes one Atom feed per language, `assets/feed.xml` (English, the `/blog` pages) and `assets/es/feed.xml` (Spanish, `/es/blog`). Every URL is under `https://www.seraph.to` (`SITE`): the blog moved off `blog.seraph.to`, whose post paths now answer 404. Entry ids are the post's page in that language (the English ids are the ones the single feed always had). The blog navbar's "Atom" link points to the page's feed with `reload_document=True`: in this Reflex version `rx.el.a` is a React Router `Link`, and without it a click looks for a route and shows the 404 page.
  - `blog.md` (Spanish) is the full guide for adding a post.
  - Navigation: "Blog" is an entry of `navbar.NAV_ITEMS`; blog pages use `navbar.blog_navbar(lang, active=...)` — the same entries ("Blog" underlined) plus Archives / Categories / Tags / Atom (the feed in the page's language). Posts without an `Authors:` line show "Ernesto Crespo"; a leading `# Title` equal to the post title is dropped (`blog.post_body`).
- `.web/`, `.states/`, `public/` are generated.
