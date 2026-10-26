"""Content of the home page (`/`): the profile summary and the main projects.

Every figure comes from the GitHub EDA behind `/dev-dashboard-stats` (bare
clones of `ecrespo` and `prismal-ai`, hand-written commits only, as of
`DATA_AS_OF`); every career fact comes from `web/resume_data.py`.
"""

from .dev_dashboard_data import DATA_AS_OF

GITHUB_URL = "https://github.com/ecrespo"

# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #

PROFILE_ROLE = "Software engineer · Python, data and AI agents"

PROFILE_SUMMARY = [
    (
        "Electrical engineer (Carabobo University, 2001) and backend developer, currently "
        "Software Engineer III at Asistensi Global Insurance. Two decades of Python across "
        "oil and gas, cloud and data engineering, business intelligence and insurtech."
    ),
    (
        "Today most of my work is agentic AI: a multi-agent framework on LangGraph, an "
        "agentic terminal in Go, MCP servers, and Reflex components that bring React "
        "libraries to Python."
    ),
]

PROFILE_STATS = [
    {"label": "Years of commits", "value": "20.8"},
    {"label": "Hand-written commits", "value": "3,119"},
    {"label": "Packages on PyPI", "value": "35"},
    {"label": "Certifications", "value": "178"},
    {"label": "Notebooks", "value": "104"},
]

# --------------------------------------------------------------------------- #
# Main projects
# --------------------------------------------------------------------------- #

PROJECTS = [
    {
        "name": "Umbral",
        "tagline": "A local-first agentic terminal in Go.",
        "tags": ["Go", "MCP", "Anthropic SDK", "OpenAI SDK", "SQLite"],
        "facts": [
            "223 commits in 43 days (September–October 2026)",
            "117 merge commits: every change lands through a branch",
            "Speaks MCP and both the Anthropic and OpenAI SDKs",
        ],
        "links": [("GitHub", f"{GITHUB_URL}/umbral")],
    },
    {
        "name": "Prismal AI",
        "tagline": "Prism-inspired multi-agent orchestration framework built on LangGraph. Security-first.",
        "tags": ["Python", "LangGraph", "LangChain", "MCP", "FastAPI", "Polars", "DuckDB"],
        "facts": [
            "Eight repositories: core, server, SDK, TUI, webchat, dashboard, chatbot, notebooks",
            "544 commits since February 2026, 326 of them touching tests",
            "23 tagged releases and 74 example notebooks",
        ],
        "links": [("GitHub", "https://github.com/prismal-ai")],
    },
    {
        "name": "Vigia EEW",
        "tagline": "Real-time earthquake early-warning desktop agent for Linux, Windows and macOS.",
        "tags": ["Python", "WebSocket", "REST", "Pydantic", "PyInstaller"],
        "facts": [
            "WebSocket push from EMSC with a REST fallback to USGS; alerts that cannot be dismissed",
            "117 commits, 13 tagged releases, 77 commits touching tests",
            "Version 1.0.0 published on PyPI",
        ],
        "links": [
            ("GitHub", f"{GITHUB_URL}/vigia-eew"),
            ("PyPI", "https://pypi.org/project/vigia-eew/"),
        ],
    },
    {
        "name": "LangChain",
        "tagline": "LLM applications with LangChain: local models, agents and APIs.",
        "tags": ["LangChain", "Ollama", "CrewAI", "FastAPI"],
        "facts": [
            "langchain_tutorials: hands-on LangChain exercises",
            "fastapi_ollama_langchain: an LLM service on FastAPI and Ollama",
            "crewai_ollama_langchain: CrewAI agents on local models",
        ],
        "links": [("GitHub", f"{GITHUB_URL}?tab=repositories&q=langchain")],
    },
    {
        "name": "LangGraph",
        "tagline": "Stateful agents and graphs with LangGraph, from notebooks to apps.",
        "tags": ["LangGraph", "MCP", "Reflex", "Jupyter"],
        "facts": [
            "Langgraph_tutorials: 30 notebooks",
            "recruitment_agency: a LangGraph app that screens candidates by profile, with a Reflex UI",
            "onlyVans: a data-analysis agent with a Reflex chatbot; demo_mcp_agent: a LangGraph agent over MCP",
        ],
        "links": [("GitHub", f"{GITHUB_URL}/Langgraph_tutorials")],
    },
]

# --------------------------------------------------------------------------- #
# Activity of the main projects — sparkline_rows: [{"name", "readout", "points"}]
# Hand-written commits per month, January 2024 to October 2026.
# --------------------------------------------------------------------------- #

_MONTHLY = {
    "Umbral": [0] * 32 + [99, 124],
    "Prismal AI": [0] * 25 + [92, 119, 52, 59, 102, 44, 0, 0, 76],
    "Vigia EEW": [0] * 29 + [7, 40, 0, 64, 6],
    "LangChain": [0, 0, 8] + [0] * 15 + [1] + [0] * 7 + [6, 2] + [0] * 6,
    "LangGraph": [0] * 24 + [9, 2, 0, 2, 7, 0, 0, 0, 0, 0],
}

PROJECT_ACTIVITY = [
    {"name": name, "readout": f"{sum(points):,} commits", "points": points}
    for name, points in _MONTHLY.items()
]

ACTIVITY_SPAN = "January 2024 – October 2026"

__all__ = [
    "ACTIVITY_SPAN",
    "DATA_AS_OF",
    "GITHUB_URL",
    "PROFILE_ROLE",
    "PROFILE_STATS",
    "PROFILE_SUMMARY",
    "PROJECT_ACTIVITY",
    "PROJECTS",
]
