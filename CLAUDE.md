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
uv run reflex export --frontend-only   # static frontend -> frontend.zip

bash build_local.sh              # local static build into public/ (uv sync --frozen + reflex export)
uv run python web/blog/rss.py    # regenerate assets/feed.xml (Atom) from content/posts — run from repo root
uv run python utils/validate_links.py  # curl-checks links in posts and REWRITES broken internal blog links in place

# Same checks as .github/workflows/ci.yml (runs on push/PR to develop and main)
uv run ruff check . && uv run ruff format --check .
uv run bandit -c pyproject.toml -r .
uv run reflex compile
```

CI also runs pip-audit on the exported lock, gitleaks (config in `.gitleaks.toml`; `public/`, `node_modules/` and two old example tokens in blog posts are allowlisted), hadolint (`.hadolint.yaml`) and a Docker build without push. Dev tools (ruff, bandit, pip-audit) live in the `dev` dependency group; the Docker image sets `UV_NO_DEV=1` so they are never installed there.

Note: `uv.lock` is the only lockfile — both build scripts, CI and the Dockerfile install with `uv sync --frozen`, which never updates it. Run `uv lock` (or use `uv add`/`uv remove`) after changing `pyproject.toml`.

## Deployment model

- **Frontend**: static export served by Vercel from `public/` (`vercel.json`, SPA rewrite to `index.html`). `.github/workflows/static_build.yml` runs `remote_build.sh` (exports with `API_URL=https://api.seraph.to`) on PRs to `main` as a check, and on push to `main` auto-commits `public/` as "Update static build [skip ci]". Don't hand-edit `public/`.
- **Backend**: Railway builds the Dockerfile on push to `main`; the image runs `reflex run --backend-only` on port 8000 at `api.seraph.to`. `rxconfig.py` sets `api_url`, CORS origins, and `state_manager_mode="memory"`.
- Work happens on `develop`; `main` is the deploy branch, protected by the "Protect main" ruleset (changes only via PR with the CI and Static Build checks passing; no force-push or deletion). The Static Build pushes `public/` with the `STATIC_BUILD_DEPLOY_KEY` deploy key, which is the ruleset's bypass actor.

## Architecture

- `web/web.py` — creates `rx.App`, global `<head>` (Inter font, `.prose` CSS for rendered posts), and registers all routes: `/`, `/blog`, `/blog/archives`, `/blog/categories`, `/blog/tags`, plus one static route per post.
- **Resume page**: content is hardcoded Python data in `web/resume_data.py`, rendered by `web/components/resume_sections.py`; `web/states/resume_state.py` builds Plotly radar charts used by `components/skills_chart.py`. Layout is sidebar (`components/sidebar.py`, fixed, `md:ml-96` offset) + navbar + main, styled with Tailwind classes via `class_name` (TailwindV4Plugin).
- **Certifications timeline**: not Reflex components — `resume_sections.certifications_section` iframes `assets/timeline.html` (Knight Lab TimelineJS), which fetches `assets/timeline.json`. Add certificates by editing `assets/timeline.json` (`web/timeline.json` is a separate, stale copy). See `timeline.md` (Spanish) for the entry format.
- **Blog** (`web/blog/`):
  - `paths.py` loads every `content/posts/*.md` **at import time** into `blog_data` (slug → `BlogPost`) and `sorted_posts`. Posts use Pelican-style header metadata (`Title:`, `Date:`, `Category:`, `Tags:`, `Slug:`, `Summary:`…) terminated by a blank line; files without `Title` are skipped. Slug comes from `Slug:` or the filename minus its date prefix, then `sanitize_slug` strips to `[a-z0-9_-]`.
  - `blog.py` builds `blog_post_routes` — one statically generated page per post via closures (the Reflex official blog pattern). Adding/renaming a post requires restarting the app / re-exporting.
  - `archives.py`, `categories.py`, `tags.py` are index pages; `states/blog_state.py` handles list pagination.
  - Post markdown image refs `./images/x.png` are rewritten to `/blog/images/x.png`, served from `assets/blog/images/`. `content/images/` mirrors those images.
  - `rss.py` is a standalone script, not wired into the app; the navbar links to `/feed.xml`.
  - `blog.md` (Spanish) is the full guide for adding a post.
- `.web/`, `.states/`, `public/` are generated.
