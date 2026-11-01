"""Step 2 of the GitHub EDA: read the mirrored history and write the dashboard data.

    uv run python utils/github_eda/build.py --workdir ~/.cache/github-eda

Reads the bare mirrors written by `collect.py`, keeps the account owner's
hand-written commits and writes `web/data/dev_dashboard.json`, the file behind
`/dev-dashboard-stats` (see `specs/dev-dashboard-stats-page.md` for every
definition). Also asks PyPI whether each Python package of the account is
published (public JSON API, one request per package).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess  # nosec B404
import tomllib
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median

OUT = Path(__file__).resolve().parents[2] / "web" / "data" / "dev_dashboard.json"

# --------------------------------------------------------------------------- #
# Who and what counts
# --------------------------------------------------------------------------- #

# Every e-mail the account owner has committed with since 2006 (work, university,
# government and personal machines).
OWNER_EMAILS = {
    "ecrespo@gmail.com",
    "ecrespo@protonmail.com",
    "ernesto@zvezda",
    "ecrespo@localhost",
    "ernesto@asistensi.com",
    "ecrespo@cenditel.gob.ve",
    "ecrespo@gcenditel.gob.ve",
    "integracion.dst@gmail.com",
    "crespoe@guardiandelalba.pdvsa.com",
    "crespoe@guadiandelalba.pdvsa.com",
    "crespoej@pdvsa.com",
    "ernesto@crespo.org.ve",
    "ernesto@heimdal",
    "ernesto@grievous",
}

# Automated publishing, not hand-written work.
AUTOMATED = re.compile(
    r"^(generate pelican site|update static build|generada salida html|"
    r"((agregado|creado|generado|added|create|update|delete|add)\s+)?cname\s*$)",
    re.I,
)
CONVENTIONAL = re.compile(
    r"^(feat|fix|docs|chore|refactor|test|tests|ci|build|perf|style|revert)(\([^)]*\))?!?:", re.I
)

# Paths that are vendored, compiled or generated: they say nothing about the work.
IGNORED_PATH = re.compile(
    r"(^|/)(node_modules|vendor|dist|build|\.web|site-packages|__pycache__|"
    r"\.ipynb_checkpoints|\.venv|venv|env)/|\.min\.(js|css)$|(^|/)(package-lock\.json|"
    r"uv\.lock|poetry\.lock|yarn\.lock|pnpm-lock\.yaml|go\.sum|Pipfile\.lock)$"
)

# --------------------------------------------------------------------------- #
# Technologies (file types) and their groups
# --------------------------------------------------------------------------- #

EXTENSIONS = {
    ".py": "Python", ".pyi": "Python", ".js": "JavaScript", ".mjs": "JavaScript",
    ".cjs": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".vue": "Vue", ".go": "Go", ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell",
    ".sql": "SQL", ".json": "JSON", ".toml": "TOML", ".yml": "YAML", ".yaml": "YAML",
    ".ini": "INI/conf", ".cfg": "INI/conf", ".conf": "INI/conf", ".md": "Markdown",
    ".rst": "reStructuredText", ".html": "HTML", ".htm": "HTML", ".svg": "SVG",
    ".css": "CSS", ".scss": "CSS", ".glade": "GTK / Glade", ".ui": "GTK / Glade",
    ".csv": "Data (CSV)", ".ipynb": "Jupyter", ".tmpl": "Go templates",
    ".gotmpl": "Go templates", ".po": "gettext i18n", ".pot": "gettext i18n",
}  # fmt: skip
TECH_GROUPS = {
    "Code": ("Python", "JavaScript", "TypeScript", "Vue", "Go", "Shell", "SQL"),
    "Config & build": ("JSON", "TOML", "YAML", "Dockerfile", "Makefile", "INI/conf"),
    "Docs": ("Markdown", "reStructuredText", "gettext i18n"),
    "Markup & UI": ("HTML", "SVG", "CSS", "GTK / Glade", "Go templates"),
    "Data": ("Data (CSV)", "Jupyter"),
}
TECH_GROUP = {tech: group for group, techs in TECH_GROUPS.items() for tech in techs}


def tech_of(path: str) -> str | None:
    name = path.rsplit("/", 1)[-1]
    if name.startswith("Dockerfile") or name.endswith(".dockerfile"):
        return "Dockerfile"
    if name in ("Makefile", "makefile", "GNUmakefile") or name.endswith(".mk"):
        return "Makefile"
    dot = name.rfind(".")
    return EXTENSIONS.get(name[dot:].lower()) if dot > 0 else None


# --------------------------------------------------------------------------- #
# Stack: what each repository declares in its manifests at HEAD
# --------------------------------------------------------------------------- #

CATEGORY = {
    "GitHub Actions": "DevOps", "Docker": "DevOps", "Vercel": "DevOps", "Railway": "DevOps",
    "Travis CI": "DevOps",
    "pytest": "Python tooling", "uv": "Python tooling", "Ruff": "Python tooling",
    "Pydantic": "Python tooling", "Poetry": "Python tooling",
    "MCP": "AI / LLM", "OpenAI SDK": "AI / LLM", "Anthropic SDK": "AI / LLM",
    "LangChain / LangGraph": "AI / LLM", "Ollama": "AI / LLM",
    "Hugging Face / PyTorch": "AI / LLM",
    "SQLite": "Data store", "SQLAlchemy / SQLModel": "Data store", "PostgreSQL": "Data store",
    "MongoDB": "Data store", "Redis": "Data store", "DuckDB": "Data store",
    "Node.js / npm": "Runtime", "Go modules": "Runtime",
    "pandas": "Data / ML", "Polars": "Data / ML", "NumPy": "Data / ML",
    "Matplotlib / Plotly": "Data / ML", "scikit-learn": "Data / ML", "Jupyter": "Data / ML",
    "Pelican": "Web framework", "Reflex": "Web framework", "FastAPI": "Web framework",
    "Flask": "Web framework", "Django": "Web framework", "Streamlit": "Web framework",
    "Gin / Go HTTP": "Web framework",
    "React": "Frontend", "Vite": "Frontend", "Tailwind CSS": "Frontend", "Vue": "Frontend",
    "D3": "Frontend", "Next.js": "Frontend", "Three.js": "Frontend",
    "GTK (PyGObject)": "Desktop", "Textual": "Desktop",
}  # fmt: skip

# (component, regex over a manifest's text). Python and JavaScript dependency names.
PY_RULES = [
    ("Reflex", r"\breflex\b"), ("FastAPI", r"\bfastapi\b"), ("Flask", r"\bflask\b"),
    ("Django", r"\bdjango\b"), ("Pydantic", r"\bpydantic\b"),
    ("SQLAlchemy / SQLModel", r"\b(sqlalchemy|sqlmodel)\b"),
    ("PostgreSQL", r"\b(psycopg2?|psycopg-binary|asyncpg|postgres(ql)?)\b"),
    ("Redis", r"\bredis\b"), ("MongoDB", r"\b(pymongo|motor|mongoengine|beanie)\b"),
    ("SQLite", r"\b(sqlite3?|aiosqlite)\b"), ("DuckDB", r"\bduckdb\b"),
    ("pandas", r"\bpandas\b"), ("Polars", r"\bpolars\b"), ("NumPy", r"\bnumpy\b"),
    ("Matplotlib / Plotly", r"\b(matplotlib|plotly|seaborn)\b"),
    ("scikit-learn", r"\b(scikit-learn|sklearn)\b"),
    ("Jupyter", r"\b(jupyter|jupyterlab|ipykernel|notebook)\b"),
    ("Streamlit", r"\bstreamlit\b"),
    ("LangChain / LangGraph", r"\b(langchain|langgraph)"),
    ("MCP", r"(\bmcp\b|fastmcp|modelcontextprotocol)"),
    ("OpenAI SDK", r"\bopenai\b"), ("Anthropic SDK", r"\banthropic\b"),
    ("Ollama", r"\bollama\b"),
    ("Hugging Face / PyTorch", r"\b(transformers|torch|huggingface[-_]hub|sentence-transformers)\b"),
    ("pytest", r"\bpytest\b"), ("Ruff", r"\bruff\b"), ("Pelican", r"\bpelican\b"),
    ("GTK (PyGObject)", r"\b(pygobject|gi\.repository)\b"), ("Textual", r"\btextual\b"),
]  # fmt: skip
JS_RULES = [
    ("React", r'"react"'), ("Vite", r'"vite"'), ("Tailwind CSS", r'"tailwindcss"|"@tailwindcss/'),
    ("Vue", r'"vue"'), ("Next.js", r'"next"'), ("D3", r'"d3(-[a-z]+)?"'),
    ("Three.js", r'"three"'), ("MCP", r'"@modelcontextprotocol/'),
    ("OpenAI SDK", r'"openai"'), ("Anthropic SDK", r'"@anthropic-ai/'),
    ("LangChain / LangGraph", r'"@langchain/'),
]  # fmt: skip
GO_RULES = [
    ("Gin / Go HTTP", r"(gin-gonic/gin|labstack/echo|gofiber/fiber|go-chi/chi|gorilla/mux)"),
    ("SQLite", r"(mattn/go-sqlite3|modernc\.org/sqlite|glebarez/sqlite)"),
    ("PostgreSQL", r"(jackc/pgx|lib/pq)"), ("MCP", r"(mark3labs/mcp-go|modelcontextprotocol)"),
    ("OpenAI SDK", r"openai"), ("Anthropic SDK", r"anthropic"),
]  # fmt: skip

PY_MANIFESTS = {"pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "environment.yml",
                "pelicanconf.py", "rxconfig.py"}  # fmt: skip
MANIFEST_SKIP = re.compile(r"(^|/)(node_modules|vendor|testdata|fixtures?|examples?|e2e|\.web)/")


def is_manifest(path: str) -> bool:
    if MANIFEST_SKIP.search(path) or path.count("/") > 2:
        return False
    name = path.rsplit("/", 1)[-1]
    return (
        name in PY_MANIFESTS
        or (name.startswith(("requirements", "requerimientos")) and name.endswith(".txt"))
        or name in ("package.json", "go.mod")
    )


def detect_stack(paths: list[str], read) -> set[str]:
    """Components declared at HEAD; `read(path)` returns a file's text."""
    stack: set[str] = set()
    names = {p.rsplit("/", 1)[-1] for p in paths}
    if any(
        n.startswith("Dockerfile") or n.startswith(("docker-compose", "compose.")) for n in names
    ):
        stack.add("Docker")
    if any(p.startswith(".github/workflows/") for p in paths):
        stack.add("GitHub Actions")
    if any(DEPLOY_WORKFLOW.search(p) for p in paths):
        stack.add(RELEASE)
    if ".travis.yml" in names:
        stack.add("Travis CI")
    if "vercel.json" in names:
        stack.add("Vercel")
    if names & {"railway.json", "railway.toml"}:
        stack.add("Railway")
    if "uv.lock" in names:
        stack.add("uv")
    if "poetry.lock" in names:
        stack.add("Poetry")
    if any(p.endswith(".ipynb") for p in paths):
        stack.add("Jupyter")
    if any(p.endswith(".glade") for p in paths):
        stack.add("GTK (PyGObject)")
    if "manage.py" in names:
        stack.add("Django")
    for path in filter(is_manifest, paths):
        name = path.rsplit("/", 1)[-1]
        text = read(path)
        if not text:
            continue
        if name == "package.json":
            stack.add("Node.js / npm")
            rules = JS_RULES
        elif name == "go.mod":
            stack.add("Go modules")
            rules = GO_RULES
        else:
            rules = PY_RULES
            low = text.lower()
            if "[tool.uv" in low:
                stack.add("uv")
            if "[tool.poetry" in low:
                stack.add("Poetry")
            if name == "pelicanconf.py":
                stack.add("Pelican")
            if name == "rxconfig.py":
                stack.add("Reflex")
        for component, pattern in rules:
            if re.search(pattern, text, re.I):
                stack.add(component)
    return stack


# --------------------------------------------------------------------------- #
# Profiles
# --------------------------------------------------------------------------- #

FDE = "Forward Deployed Engineer"
PROFILES = [
    "AI Engineer",
    "Full-stack Engineer",
    "Backend Engineer",
    "DevOps / Platform",
    "Data Engineer / Scientist",
    "Systems & Linux",
    FDE,
]
AI_STACK = {"LangChain / LangGraph", "MCP", "OpenAI SDK", "Anthropic SDK", "Ollama",
            "Hugging Face / PyTorch"}  # fmt: skip
FRONT_STACK = {"Reflex", "React", "Vue", "Next.js", "Vite", "Tailwind CSS"}
BACK_STACK = {"FastAPI", "Django", "Flask", "Pydantic", "SQLAlchemy / SQLModel", "PostgreSQL",
              "Redis", "MongoDB", "Gin / Go HTTP"}  # fmt: skip
DATA_STACK = {"pandas", "Polars", "NumPy", "Matplotlib / Plotly", "Jupyter", "Streamlit",
              "scikit-learn", "DuckDB"}  # fmt: skip
SYSTEMS_STACK = {"Go modules", "GTK (PyGObject)"}
# Linux daemons and desktop integration (SMS gateways, GNOME, Canaima / Debian).
SYSTEMS_NAME = re.compile(r"(android|sms|gnome|linux|canaima|debian|daemon|sysctl|kernel)", re.I)
AI_NAME = re.compile(
    r"(agent|llm|gpt|rag\b|chatbot|langchain|langgraph|mcp|openai|ollama|claude)", re.I
)

# A workflow that deploys or releases (not plain CI). A marker, not a stack component.
RELEASE = "release workflow"
DEPLOY_WORKFLOW = re.compile(
    r"^\.github/workflows/[^/]*(deploy|release|publish|pages|docker|cd)[^/]*\.ya?ml$", re.I
)

# Forward Deployed Engineer: the work of shipping a complete, integrated solution
# where it is used. A repository is an end-to-end delivery when it declares at
# least three of the four layers below; a commit also counts when it changes how
# a user-facing product is deployed (container, hosting, release workflow).
FDE_LAYERS = {
    "interface": FRONT_STACK | {"Streamlit", "Textual", "GTK (PyGObject)"},
    "service": BACK_STACK - {"Pydantic"} | {"MCP"},
    "integration": AI_STACK | {"PostgreSQL", "MongoDB", "Redis", "SQLite", "DuckDB"},
    "delivery": {"Docker", "Vercel", "Railway", RELEASE},
}
DEVOPS_FILE = re.compile(
    r"(^|/)(Dockerfile[^/]*|[^/]*\.dockerfile|(docker-)?compose[^/]*\.ya?ml|Makefile|"
    r"\.github/workflows/[^/]+|\.travis\.yml|vercel\.json|railway\.(json|toml)|fly\.toml|"
    r"Procfile|netlify\.toml|render\.yaml|k8s/[^/]+|helm/[^/]+|\.gitlab-ci\.yml)$"
)
DEPLOY_FILE = re.compile(
    r"(^|/)(Dockerfile[^/]*|(docker-)?compose[^/]*\.ya?ml|vercel\.json|railway\.(json|toml)|"
    r"fly\.toml|Procfile|render\.yaml|netlify\.toml|\.github/workflows/[^/]*(deploy|release|"
    r"publish|docker|pages|build)[^/]*)$",
    re.I,
)
TEST_FILE = re.compile(
    r"(^|/)(tests?|__tests__|spec)/|(^|/)test_[^/]+$|_test\.[a-z]+$|\.(test|spec)\.[a-z]+$"
)


def fde_layers(stack: set[str]) -> int:
    return sum(bool(stack & components) for components in FDE_LAYERS.values())


def profiles_of(commit: Commit, repo: Repo) -> set[str]:
    stack, files, techs = repo.stack, commit.files, commit.techs
    out = set()
    if (
        stack & AI_STACK
        or repo.owner == "prismal-ai"
        or AI_NAME.search(repo.name)
        or any(re.search(r"lang(chain|graph)", f, re.I) for f in files)
    ):
        out.add("AI Engineer")
    if (
        stack & FRONT_STACK
        or any(f.endswith((".tsx", ".jsx", ".vue")) for f in files)
        or (techs & {"CSS", "HTML"})
    ):
        out.add("Full-stack Engineer")
    if stack & BACK_STACK:
        out.add("Backend Engineer")
    if any(DEVOPS_FILE.search(f) for f in files):
        out.add("DevOps / Platform")
    if stack & DATA_STACK or techs & {"Jupyter", "Data (CSV)"}:
        out.add("Data Engineer / Scientist")
    if (
        stack & SYSTEMS_STACK
        or techs & {"Go", "Shell", "GTK / Glade"}
        or repo.name == "vigia-eew"
        or SYSTEMS_NAME.search(repo.name)
    ):
        out.add("Systems & Linux")
    if fde_layers(stack) >= 3 or (
        any(DEPLOY_FILE.search(f) for f in files)
        and stack & (FDE_LAYERS["interface"] | FDE_LAYERS["service"])
    ):
        out.add(FDE)
    return out


# --------------------------------------------------------------------------- #
# Reading the mirrors
# --------------------------------------------------------------------------- #


@dataclass
class Repo:
    owner: str
    name: str
    path: Path
    fork: bool
    stars: int
    forks: int
    language: str
    description: str
    created: str
    stack: set[str] = field(default_factory=set)
    tags: int = 0
    merges: int = 0
    package: str | None = None
    pypi: bool = False

    @property
    def key(self) -> str:
        return f"{self.owner}/{self.name}" if self.owner != "ecrespo" else self.name


@dataclass
class Commit:
    sha: str
    repo: Repo
    when: datetime  # author's local time
    subject: str
    files: list[str]
    techs: set[str] = field(default_factory=set)
    profiles: set[str] = field(default_factory=set)

    @property
    def day(self) -> date:
        return self.when.date()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(  # nosec B603 B607
        ["git", "-C", str(repo), *args], capture_output=True, text=True, errors="replace"
    )
    return result.stdout


def author_args() -> list[str]:
    return [f"--author=<{re.escape(email)}>" for email in sorted(OWNER_EMAILS)]


def read_log(repo: Repo) -> list[tuple[str, str, str, list[str]]]:
    out = git(repo.path, "log", "--all", "--no-merges", "--no-renames", *author_args(),
              "--format=%x1e%H%x1f%aE%x1f%aI%x1f%s", "--name-only")  # fmt: skip
    rows = []
    for block in out.split("\x1e")[1:]:
        head, _, rest = block.partition("\n")
        sha, email, when, subject = head.split("\x1f", 3)
        if email.lower() not in OWNER_EMAILS:
            continue
        rows.append((sha, when, subject, [f for f in rest.splitlines() if f.strip()]))
    return rows


def inspect_repo(repo: Repo) -> None:
    """Stack, tags, merges by the owner, Python package name.

    The stack is read from the most recently updated branch: some repositories keep
    the default branch as a skeleton while the work lives on `develop`.
    """
    ref = git(repo.path, "for-each-ref", "--sort=-committerdate", "--count=1",
              "--format=%(refname)", "refs/heads").strip() or "HEAD"  # fmt: skip
    paths = git(repo.path, "ls-tree", "-r", "--name-only", ref).splitlines()
    cache: dict[str, str] = {}

    def read(p: str) -> str:
        if p not in cache:
            cache[p] = git(repo.path, "cat-file", "-p", f"{ref}:{p}")
        return cache[p]

    repo.stack = detect_stack(paths, read)
    if repo.key == "ecrespo.github.io":
        repo.stack.add("Pelican")  # stores only Pelican's output
    repo.tags = 0 if repo.fork else len(git(repo.path, "tag").split())
    repo.merges = len(
        git(repo.path, "log", "--all", "--merges", *author_args(), "--format=%H").split()
    )
    if "pyproject.toml" in paths:
        try:
            meta = tomllib.loads(read("pyproject.toml"))
            repo.package = (meta.get("project") or {}).get("name") or (
                meta.get("tool", {}).get("poetry", {}).get("name")
            )
        except tomllib.TOMLDecodeError:
            repo.package = None


def on_pypi(package: str) -> bool:
    url = f"https://pypi.org/pypi/{package}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as response:  # nosec B310
            info = json.load(response)["info"]
    except Exception:  # noqa: BLE001 — 404 or network: not published
        return False
    # The same name can belong to someone else: require the owner as author or a link back.
    blob = json.dumps(info).lower()
    return "ecrespo" in blob or "ernesto crespo" in blob or "prismal" in blob


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAY_BUCKETS = [("1", 1, 1), ("2-3", 2, 3), ("4-5", 4, 5), ("6-10", 6, 10), ("11-20", 11, 20),
               ("21+", 21, 10**9)]  # fmt: skip


def months_between(first: date, last: date) -> list[str]:
    out, y, m = [], first.year, first.month
    while (y, m) <= (last.year, last.month):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def monthly_rows(commits: list[Commit]) -> list[dict]:
    if not commits:
        return []
    counts = Counter(c.when.strftime("%Y-%m") for c in commits)
    days = [c.day for c in commits]
    return [{"month": m, "commits": counts.get(m, 0)} for m in months_between(min(days), max(days))]


def longest_streak(days: set[date]) -> int:
    best = 0
    for d in days:
        if d - timedelta(days=1) not in days:
            n = 1
            while d + timedelta(days=n) in days:
                n += 1
            best = max(best, n)
    return best


def levels(counts: dict[date, int]) -> dict[date, int]:
    active = sorted(v for v in counts.values() if v)
    if not active:
        return {}
    q = [active[int(len(active) * f)] if int(len(active) * f) < len(active) else active[-1]
         for f in (0.25, 0.5, 0.75)]  # fmt: skip
    return {d: 1 + sum(v > cut for cut in q) for d, v in counts.items() if v}


def stack_rows(commits: list[Commit]) -> tuple[list[dict], list[dict]]:
    comp, cats = Counter(), Counter()
    for c in commits:
        for component in c.repo.stack:
            if component in CATEGORY:
                comp[component] += 1
        for category in {CATEGORY[s] for s in c.repo.stack if s in CATEGORY}:
            cats[category] += 1
    stack = [{"component": k, "commits": v, "category": CATEGORY[k]} for k, v in comp.most_common()]
    return stack, [{"name": k, "value": v} for k, v in cats.most_common()]


def tech_tree(tech: Counter) -> list[dict]:
    nodes = [{"id": "root", "parent": None, "name": "Commits"}]
    for group, techs in TECH_GROUPS.items():
        present = [t for t in techs if tech.get(t)]
        if not present:
            continue
        nodes.append({"id": group, "parent": "root", "name": group})
        nodes += [{"id": t, "parent": group, "name": t, "commits": tech[t]} for t in present]
    return nodes


def make_slice(commits: list[Commit], end: date) -> dict:
    n = len(commits)
    days = Counter(c.day for c in commits)
    weekday = Counter(c.when.weekday() for c in commits)
    hours = Counter(c.when.hour for c in commits)
    heat = Counter((c.when.weekday(), c.when.hour) for c in commits)
    tech = Counter(t for c in commits for t in c.techs)
    repos = Counter(c.repo.key for c in commits)
    by_key = {c.repo.key: c.repo for c in commits}

    week0 = end - timedelta(days=end.weekday()) - timedelta(weeks=51)
    weeks = Counter((c.day - week0).days // 7 for c in commits if c.day >= week0)
    daily_start = end - timedelta(days=364)
    daily = {daily_start + timedelta(days=i): 0 for i in range(365)}
    for c in commits:
        if c.day in daily:
            daily[c.day] += 1
    lv = levels(daily)

    years = sorted({c.when.year for c in commits})
    top6 = [t for t, _ in tech.most_common(6)]
    tech_year = Counter((c.when.year, t) for c in commits for t in c.techs if t in top6)
    stack, categories = stack_rows(commits)
    mix = Counter(p for c in commits for p in c.profiles)
    peak = max(range(24), key=lambda h: hours.get(h, 0)) if n else 0

    return {
        "kpis": {
            "commits": n,
            "active_days": len(days),
            "repos": len(repos),
            "weekend": round(100 * (weekday[5] + weekday[6]) / n, 1) if n else 0.0,
            "peak_hour": f"{peak:02d}:00",
            "streak": longest_streak(set(days)),
            "conventional": round(
                100 * sum(bool(CONVENTIONAL.match(c.subject)) for c in commits) / n, 1
            )
            if n
            else 0.0,
            "per_active_day": round(n / len(days), 1) if days else 0.0,
        },
        "monthly": monthly_rows(commits),
        "yearly": [
            {"year": str(y), "commits": sum(1 for c in commits if c.when.year == y)} for y in years
        ],
        "weekly": [
            {
                "week": (week0 + timedelta(weeks=i)).strftime("%b %-d"),
                "start": (week0 + timedelta(weeks=i)).isoformat(),
                "commits": weeks.get(i, 0),
            }
            for i in range(52)
        ],
        "weekday": [{"day": DAYS[i], "commits": weekday.get(i, 0)} for i in range(7)],
        "hours": [{"hour": f"{h:02d}", "commits": hours.get(h, 0)} for h in range(24)],
        "heatmap": [
            {"day": DAYS[d], "hours": [heat.get((d, h), 0) for h in range(24)]} for d in range(7)
        ],
        "heatmap_max": max(heat.values(), default=0),
        "day_sizes": [
            {"size": label, "days": sum(1 for v in days.values() if lo <= v <= hi)}
            for label, lo, hi in DAY_BUCKETS
        ],
        "repos": [
            {"repo": by_key[k].name, "key": k, "commits": v} for k, v in repos.most_common(25)
        ],
        "tech": [{"tech": t, "commits": v} for t, v in tech.most_common(16)],
        "tech_tree": tech_tree(tech),
        "stack": stack,
        "stack_categories": categories,
        "profile_mix": [{"profile": p, "commits": mix[p]} for p in PROFILES if mix.get(p)],
        "daily": [
            {"date": d.isoformat(), "commits": v, "level": lv.get(d, 0)} for d, v in daily.items()
        ],
        "tech_by_year": [
            {"year": str(y), **{t: tech_year.get((y, t), 0) for t in top6}} for y in years
        ],
        "tech_year_keys": top6,
    }


def trajectory(last: date, last90: int, prev90: int, as_of: date) -> str:
    if last90 == 0:
        return "Dormant" if (as_of - last).days > 365 else "Maintained"
    return "Accelerating" if last90 > prev90 else "Active"


def windows(commits: list[Commit], as_of: date) -> tuple[int, int]:
    last90 = sum(1 for c in commits if (as_of - c.day).days < 90)
    prev90 = sum(1 for c in commits if 90 <= (as_of - c.day).days < 180)
    return last90, prev90


def main_profiles(commits: list[Commit], share: float) -> list[str]:
    counts = Counter(p for c in commits for p in c.profiles)
    return [p for p in PROFILES if counts.get(p, 0) >= share * len(commits)]


def log_score(value: float, top: float) -> float:
    return math.log1p(value) / math.log1p(top) if top > 0 else 0.0


# Reflex apps and frameworks that stand on their own, not component wrappers.
REFLEX_PRODUCTS = {"reflex-agentkit", "reflex-agentlens", "reflex-mcphost"}

# LLM learning labs: LangChain / LangGraph tutorials, RAG and agent experiments.
LAB_NAME = re.compile(r"(lang(chain|graph)|llm_tutorials|agents_ai|rag-with|demo_mcp_agent)", re.I)


def project_of(repo: Repo) -> str:
    if repo.owner == "prismal-ai":
        return "Prismal ecosystem"
    if repo.name in REFLEX_PRODUCTS:
        return repo.name
    if repo.name.startswith("reflex-") or (
        repo.pypi and (repo.package or "").startswith("reflex-")
    ):
        return "Reflex component suite"
    if LAB_NAME.search(repo.name):
        return "LangChain / LangGraph labs"
    return repo.name


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def load_repos(workdir: Path) -> list[Repo]:
    repos = []
    for meta in json.loads((workdir / "repos.json").read_text()):
        path = workdir / "repos" / meta["owner"] / f"{meta['name']}.git"
        if not (path / "HEAD").exists():
            continue
        repos.append(
            Repo(
                owner=meta["owner"],
                name=meta["name"],
                path=path,
                fork=meta["isFork"],
                stars=meta["stargazerCount"],
                forks=meta["forkCount"],
                language=(meta.get("primaryLanguage") or {}).get("name") or "—",
                description=meta.get("description") or "",
                created=meta["createdAt"],
            )
        )
    return repos


def collect_commits(repos: list[Repo], jobs: int) -> tuple[list[Commit], int, int]:
    # A commit present in several mirrors (forks) belongs to the original first.
    order = sorted(repos, key=lambda r: (r.fork, r.created))
    with ThreadPoolExecutor(jobs) as pool:
        logs = dict(zip([r.key for r in order], pool.map(read_log, order), strict=True))
    seen: set[str] = set()
    commits, owner_total, automated = [], 0, 0
    for repo in order:
        for sha, when, subject, files in logs[repo.key]:
            if sha in seen:
                continue
            seen.add(sha)
            owner_total += 1
            if AUTOMATED.match(subject):
                automated += 1
                continue
            stamp = datetime.fromisoformat(when).replace(tzinfo=None)
            files = [f for f in files if not IGNORED_PATH.search(f)]
            commit = Commit(sha, repo, stamp, subject, files)
            commit.techs = {t for f in files if (t := tech_of(f))}
            commits.append(commit)
    return commits, owner_total, automated


def build(workdir: Path, as_of: date, jobs: int) -> dict:
    repos = load_repos(workdir)
    with ThreadPoolExecutor(jobs) as pool:
        list(pool.map(inspect_repo, repos))
    commits, owner_total, automated = collect_commits(repos, jobs)
    commits = [c for c in commits if c.day <= as_of]
    for c in commits:
        c.profiles = profiles_of(c, c.repo)

    active_repos = {c.repo.key: c.repo for c in commits}
    packages = {r.key: r.package for r in active_repos.values() if r.package and not r.fork}
    with ThreadPoolExecutor(jobs) as pool:
        published = dict(zip(packages, pool.map(on_pypi, packages.values()), strict=True))
    for key, ok in published.items():
        active_repos[key].pypi = ok

    print(f"{len(repos)} repositories, {owner_total} owner commits, {automated} automated, "
          f"{len(commits)} hand-written in {len(active_repos)} repositories")  # fmt: skip

    year_ago = as_of - timedelta(days=365)
    periods = [
        ("all", "All time", date.min, as_of),
        ("last12", "Last 12 months", year_ago + timedelta(days=1), as_of),
        ("2025-2026", "2025–2026", date(2025, 1, 1), as_of),
        ("2020-2024", "2020–2024", date(2020, 1, 1), date(2024, 12, 31)),
        ("2006-2019", "2006–2019", date(2006, 1, 1), date(2019, 12, 31)),
    ]
    slices = {}
    for key, _, start, end in periods:
        in_period = [c for c in commits if start <= c.day <= end]
        slices[f"{key}|all"] = make_slice(in_period, end)
        for profile in PROFILES:
            slices[f"{key}|{profile}"] = make_slice(
                [c for c in in_period if profile in c.profiles], end
            )

    by_repo: dict[str, list[Commit]] = defaultdict(list)
    for c in commits:
        by_repo[c.repo.key].append(c)

    repo_details = {}
    for _key, rc in sorted(by_repo.items()):
        repo = rc[0].repo
        days = sorted({c.day for c in rc})
        last90, prev90 = windows(rc, as_of)
        tech = Counter(t for c in rc for t in c.techs)
        repo_details[repo.name] = {
            "repo": repo.name,
            "commits": len(rc),
            "active_days": len(days),
            "first": days[0].isoformat(),
            "last": days[-1].isoformat(),
            "span_days": (days[-1] - days[0]).days,
            "language": repo.language,
            "tags": repo.tags,
            "pypi": repo.pypi,
            "stars": repo.stars,
            "merges": repo.merges,
            "trajectory": trajectory(days[-1], last90, prev90, as_of),
            "techs": ", ".join(t for t, _ in tech.most_common(5)),
            "stack": ", ".join(sorted(s for s in repo.stack if s in CATEGORY)),
            "profiles": ", ".join(main_profiles(rc, 0.5)),
            "monthly": monthly_rows(rc),
        }

    # Projects: a family of repositories counts once.
    projects: dict[str, list[Commit]] = defaultdict(list)
    for c in commits:
        projects[project_of(c.repo)].append(c)
    raw = []
    for name, pc in projects.items():
        prepos = {c.repo.key: c.repo for c in pc}.values()
        days = sorted({c.day for c in pc})
        last90, prev90 = windows(pc, as_of)
        row = {
            "project": name,
            "trajectory": trajectory(days[-1], last90, prev90, as_of),
            "repos": len(prepos),
            "commits": len(pc),
            "last90": last90,
            "pypi": sum(r.pypi for r in prepos),
            "tags": sum(r.tags for r in prepos),
            "tests": sum(1 for c in pc if any(TEST_FILE.search(f) for f in c.files)),
            "stars": sum(r.stars for r in prepos),
            "profiles": main_profiles(pc, 0.3),
            "active_days": len(days),
            "merges": sum(r.merges for r in prepos),
            "forks": sum(r.forks for r in prepos),
            "first": days[0].isoformat(),
            "last": days[-1].isoformat(),
        }
        row["_delivery"] = 5 * row["pypi"] + row["tags"] + row["merges"] + row["tests"]
        row["_social"] = row["stars"] + row["forks"]
        raw.append(row)
    top = {
        k: max(r[k] for r in raw)
        for k in ("commits", "active_days", "_delivery", "_social", "last90")
    }
    weights = {"commits": 0.3, "active_days": 0.2, "_delivery": 0.2, "_social": 0.1, "last90": 0.2}
    for r in raw:
        r["impact"] = round(100 * sum(w * log_score(r[k], top[k]) for k, w in weights.items()))
    raw.sort(key=lambda r: (-r["impact"], -r["commits"]))
    impact = [
        {"project": r["project"], "impact": r["impact"],
         **{k: v for k, v in r.items() if k not in ("project", "impact") and not k.startswith("_")}}
        for r in raw[:20]
    ]  # fmt: skip

    # Profile quadrants (all time).
    total = len(commits)
    points, vis_raw = [], {}
    for profile in PROFILES:
        pc = [c for c in commits if profile in c.profiles]
        recent = sum(1 for c in pc if c.day > year_ago)
        primary = [
            by_repo[k][0].repo
            for k, rc in by_repo.items()
            if sum(profile in c.profiles for c in rc) >= 0.5 * len(rc)
        ]
        vis_raw[profile] = (
            len(primary)
            + 3 * sum(r.pypi for r in primary)
            + 2 * sum(r.tags > 0 for r in primary)
            + sum(r.stars + r.forks for r in primary)
        )
        top_repos = Counter(c.repo.key for c in pc).most_common(4)
        points.append({
            "profile": profile,
            "commits": len(pc),
            "depth": round(100 * len(pc) / total, 1),
            "momentum": round(100 * recent / len(pc), 1) if pc else 0.0,
            "_top": ", ".join(k for k, _ in top_repos),
        })  # fmt: skip
    vis_top = max(vis_raw.values()) or 1
    for p in points:
        p["visibility"] = round(100 * vis_raw[p["profile"]] / vis_top)
        deep, fast, seen = p["depth"] >= 25, p["momentum"] >= 65, p["visibility"] >= 50
        p["map_quadrant"] = (
            ("Core & accelerating" if fast else "Established core")
            if deep
            else ("Emerging" if fast else "Supporting")
        )
        p["visibility_quadrant"] = (
            ("Showcase & growing" if fast else "Showcase")
            if seen
            else ("Hidden strength" if fast else "Latent")
        )
    profile_points = [
        {k: p[k] for k in ("profile", "commits", "depth", "momentum", "visibility",
                           "map_quadrant", "visibility_quadrant")}
        for p in points
    ]  # fmt: skip
    profiles_table = [
        {**pp, "top_repos": p["_top"], "opportunity": OPPORTUNITY.get(pp["profile"], "")}
        for pp, p in zip(profile_points, points, strict=True)
    ]

    return {
        "as_of": as_of.isoformat(),
        "periods": [{"key": k, "label": label} for k, label, _, _ in periods],
        "profiles": ["All profiles", *PROFILES],
        "slices": slices,
        "repo_details": repo_details,
        "profile_points": profile_points,
        "impact": impact,
        "profiles_table": profiles_table,
        "_summary": {
            "repositories": len(repos),
            "owner_commits": owner_total,
            "automated": automated,
            "hand_written": total,
            "active_repositories": len(active_repos),
            "medians": {"impact": median(r["impact"] for r in impact)},
        },
    }


# The opportunity each profile's evidence points to (editorial; Spanish in
# `web/dev_dashboard_data.OPPORTUNITY_ES`).
OPPORTUNITY: dict[str, str] = {
    "AI Engineer": (
        "Strongest momentum and little exposure for its size: tag Umbral releases, publish "
        "reflex-agentlens, and turn the LangChain/LangGraph labs into public write-ups."
    ),
    "Full-stack Engineer": (
        "The public face (36 Reflex components on PyPI), now growing again with agentkit and "
        "agentlens. Next step is adoption: demos, docs and stars on the component suite."
    ),
    "Backend Engineer": (
        "Growing inside Prismal, agentkit and agentlens but barely published: ship "
        "prismal-server and prismal-sdk as packages with API docs."
    ),
    "DevOps / Platform": (
        "uv, Ruff, pytest and GitHub Actions now ship with every new repository. Worth showing "
        "as release and supply-chain discipline."
    ),
    "Data Engineer / Scientist": (
        "Revived by Prismal's data layer (Polars, DuckDB, SQLAlchemy). A public case study would "
        "make it visible again."
    ),
    "Systems & Linux": (
        "Umbral (Go) and vigia-eew (cross-platform desktop alerts) restarted this line of work. "
        "Tagged Umbral releases would surface it."
    ),
    FDE: (
        "Half of all commits ship complete solutions (interface, API or MCP, LLM and data "
        "integrations, deployment): Prismal, Umbral, agentkit, agentlens, mcphost. A live "
        "reference deployment with a client-style case study would make it visible."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workdir", type=Path, default=Path.home() / ".cache" / "github-eda")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    data = build(args.workdir, args.as_of, args.jobs)
    summary = data.pop("_summary")
    args.out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
