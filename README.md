# reflex_resume

Reflex Resume is a lightweight web app built with the Reflex Python framework to showcase a developer resume/CV with interactive sections and Plotly-based skill visualizations.

This README documents the tech stack, requirements, setup instructions, run commands, available scripts, environment variables, project structure, testing status, and licensing. Stale or unknown items are explicitly marked as TODOs.

## Overview

- Purpose: Personal resume site with sections for education, work experience, portfolio, certifications, social links, and interactive skill charts.
- Frontend/Backend: Built with [Reflex](https://reflex.dev) (Python full‑stack framework). Plotly is used for radar charts of skills.
- Deployment: Dockerfile provided; a `build.sh` script can export a static frontend that talks to a configured API URL.

## Stack

- Language: Python (requires Python ≥ 3.13)
- Framework: Reflex `0.8.21`
- Charts: Plotly `6.5.0`
- Package/dependency manager(s):
  - uv (preferred; `uv.lock` present and used in Dockerfile)
  - pip (fallback; `requirements.txt` generated from `pyproject.toml`)
- Node ecosystem: minimal, Tailwind Typography plugin via `package.json`
  - Tailwind configured in `tailwind.config.js`, and Reflex `TailwindV4Plugin()` is enabled in `rxconfig.py`.

## Requirements

- Python 3.13+
- One of:
  - uv (recommended): https://github.com/astral-sh/uv
  - or pip + virtualenv/venv
- Optional (only if you plan to modify Tailwind-related assets outside Reflex’s pipeline): Node.js 20+ and npm

## Setup

Using uv (recommended):

```bash
# From repository root
uv sync --frozen

# Initialize Reflex (generates required .web assets on first run)
uv run reflex init
```

Using pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Initialize Reflex once
reflex init
```

## Running the app (development)

With uv:

```bash
uv run reflex run
```

With pip/venv:

```bash
source .venv/bin/activate
reflex run
```

Notes:
- Reflex typically serves a frontend and backend; port conventions can vary by version. In Docker we expose `8000` for the backend. TODO: Confirm dev frontend/backend ports for this project and update here.

## Production / Build

There are two common approaches: Docker or exporting the frontend.

### Docker

The provided Dockerfile is multi‑stage and uses uv:

```bash
docker build -t reflex-resume .
docker run --rm -p 8000:8000 reflex-resume
```

This starts the Reflex backend (command: `uv run reflex run --backend-only`). For a complete setup serving the compiled frontend, you may need a separate static file server or Reflex frontend process. TODO: Document full prod topology (frontend + backend) if using Docker in production.

### Export frontend only

The `build.sh` script demonstrates exporting a static frontend that communicates with an API URL:

```bash
# Optionally adjust API_URL inside build.sh or provide it in the environment
./build.sh
```

What it does:
- Installs dependencies
- Runs `reflex init`
- Removes any previous `public/`
- Runs `reflex export --frontend-only` with `API_URL` set
- Unzips `frontend.zip` to `public/`

You can then deploy the `public/` directory to any static host. Make sure the `API_URL` points to a running backend that serves the Reflex API for this app.

## Scripts

- `build.sh` — builds/export the frontend only and places it under `public/`. It sets `API_URL` inside the script; adjust as needed.
- Dockerfile — builds a runtime image that launches the backend (`--backend-only`).
- `inspect_app.py` — local diagnostic helper to introspect Reflex `App`.
- `inspect_router.py` — local diagnostic helper to introspect Reflex state/router.

## Environment variables

- `API_URL` — used during `reflex export --frontend-only` to point the static frontend at the backend API. Example:

```bash
API_URL=https://your-backend.example.com uv run reflex export --frontend-only
```

TODO: List any additional env vars if introduced (e.g., secrets, analytics keys). None are required by the current codebase beyond `API_URL` for static exports.

## Tests

No test suite is present at this time. TODO: Add unit tests for state logic and component rendering, and document how to run them here.

## Project structure

High‑level layout (selected paths):

```
.
├─ web/
│  ├─ web.py                 # Reflex app entry (creates rx.App, adds page route "/")
│  ├─ states/
│  │  ├─ base.py             # Base state (project-specific)
│  │  └─ resume_state.py     # Resume state and Plotly charts
│  └─ components/
│     ├─ resume_sections.py  # Page sections (education, experience, etc.)
│     └─ ...                 # Other components (navbar, sidebar, skills_chart, ...)
├─ rxconfig.py               # Reflex configuration (app_name="web", plugins incl. Tailwind and Sitemap)
├─ pyproject.toml            # Project metadata and dependencies
├─ requirements.txt          # Locked dependencies (generated by uv)
├─ uv.lock                   # uv lockfile
├─ tailwind.config.js        # Tailwind configuration (content points at ./web/**/*)
├─ Dockerfile                # Multi-stage Docker build (uv + backend-only run)
├─ build.sh                  # Export frontend-only build to ./public
├─ public/                   # Static export output (generated by build.sh)
├─ assets/, public/, node_modules/ (if present)
├─ package.json, package-lock.json (Tailwind plugin only)
└─ LICENSE
```

Reflex configuration (`rxconfig.py`):
- `app_name="web"`
- `favicon="👨‍🔬"`
- `state_manager_mode="memory"` (note in comment mentions Vercel)
- Plugins: `SitemapPlugin`, `TailwindV4Plugin`

App entry (`web/web.py`):
- Defines `index()` page component and registers it at route `/` via `app.add_page(index, route="/")`.

## License

This project includes a LICENSE file. See `LICENSE` for the full text.

## TODOs / Notes

- Confirm dev server ports and whether a separate frontend process is needed during development for this Reflex version; update the Run section accordingly.
- Document production architecture when using the Docker image (how frontend assets are served alongside the backend, if desired).
- Add tests and a CI workflow; update the Tests section with commands.