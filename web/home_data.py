"""Content of the home page (`/`): the profile summary and the main projects.

Text that differs by language is a `{"en": …, "es": …}` value (see `web/i18n.py`).

Every figure comes from the GitHub EDA behind `/dev-dashboard-stats` (bare
clones of `ecrespo` and `prismal-ai`, hand-written commits only, as of
`DATA_AS_OF`); every career fact comes from `web/resume_data.py`.
"""

from .dev_dashboard_data import DATA_AS_OF

GITHUB_URL = "https://github.com/ecrespo"

# --------------------------------------------------------------------------- #
# Profile
# --------------------------------------------------------------------------- #

PROFILE_ROLE = {
    "en": "Software engineer · Python, data and AI agents",
    "es": "Ingeniero de software · Python, datos y agentes de IA",
}

PROFILE_SUMMARY = [
    {
        "en": (
            "Electrical engineer (Carabobo University, 2001) and backend developer, currently "
            "Software Engineer III at Asistensi Global Insurance. Two decades of Python across "
            "oil and gas, cloud and data engineering, business intelligence and insurtech."
        ),
        "es": (
            "Ingeniero electricista (Universidad de Carabobo, 2001) y desarrollador backend, "
            "actualmente Software Engineer III en Asistensi Global Insurance. Dos décadas de "
            "Python en petróleo y gas, ingeniería cloud y de datos, inteligencia de negocios e "
            "insurtech."
        ),
    },
    {
        "en": (
            "Today most of my work is agentic AI: a multi-agent framework on LangGraph, an "
            "agentic terminal in Go, MCP servers, and Reflex components that bring React "
            "libraries to Python."
        ),
        "es": (
            "Hoy la mayor parte de mi trabajo es IA agéntica: un framework multiagente sobre "
            "LangGraph, una terminal agéntica en Go, servidores MCP y componentes de Reflex que "
            "llevan librerías de React a Python."
        ),
    },
]

PROFILE_STATS = [
    {
        "label": {"en": "Years of commits", "es": "Años de commits"},
        "value": {"en": "20.8", "es": "20,8"},
    },
    {
        "label": {"en": "Hand-written commits", "es": "Commits escritos a mano"},
        "value": {"en": "3,119", "es": "3.119"},
    },
    {"label": {"en": "Packages on PyPI", "es": "Paquetes en PyPI"}, "value": "35"},
    {"label": {"en": "Certifications", "es": "Certificaciones"}, "value": "178"},
    {"label": {"en": "Notebooks", "es": "Notebooks"}, "value": "104"},
]

# --------------------------------------------------------------------------- #
# Main projects
# --------------------------------------------------------------------------- #

PROJECTS = [
    {
        "name": "Umbral",
        "tagline": {
            "en": "A local-first agentic terminal in Go.",
            "es": "Una terminal agéntica local-first en Go.",
        },
        "tags": ["Go", "MCP", "Anthropic SDK", "OpenAI SDK", "SQLite"],
        "facts": [
            {
                "en": "223 commits in 43 days (September–October 2026)",
                "es": "223 commits en 43 días (septiembre–octubre de 2026)",
            },
            {
                "en": "117 merge commits: every change lands through a branch",
                "es": "117 commits de merge: cada cambio entra por una rama",
            },
            {
                "en": "Speaks MCP and both the Anthropic and OpenAI SDKs",
                "es": "Habla MCP y los SDK de Anthropic y de OpenAI",
            },
        ],
        "links": [("GitHub", f"{GITHUB_URL}/umbral")],
    },
    {
        "name": "Prismal AI",
        "tagline": {
            "en": "Prism-inspired multi-agent orchestration framework built on LangGraph. Security-first.",
            "es": "Framework de orquestación multiagente inspirado en un prisma, construido sobre LangGraph. La seguridad primero.",
        },
        "tags": ["Python", "LangGraph", "LangChain", "MCP", "FastAPI", "Polars", "DuckDB"],
        "facts": [
            {
                "en": "Eight repositories: core, server, SDK, TUI, webchat, dashboard, chatbot, notebooks",
                "es": "Ocho repositorios: núcleo, servidor, SDK, TUI, webchat, dashboard, chatbot, notebooks",
            },
            {
                "en": "544 commits since February 2026, 326 of them touching tests",
                "es": "544 commits desde febrero de 2026, 326 de ellos con cambios en pruebas",
            },
            {
                "en": "23 tagged releases and 74 example notebooks",
                "es": "23 versiones etiquetadas y 74 notebooks de ejemplo",
            },
        ],
        "links": [("GitHub", "https://github.com/prismal-ai")],
    },
    {
        "name": "Vigia EEW",
        "tagline": {
            "en": "Real-time earthquake early-warning desktop agent for Linux, Windows and macOS.",
            "es": "Agente de escritorio de alerta sísmica temprana en tiempo real para Linux, Windows y macOS.",
        },
        "tags": ["Python", "WebSocket", "REST", "Pydantic", "PyInstaller"],
        "facts": [
            {
                "en": "WebSocket push from EMSC with a REST fallback to USGS; alerts that cannot be dismissed",
                "es": "Avisos por WebSocket del EMSC con respaldo REST del USGS; alertas que no se pueden descartar",
            },
            {
                "en": "117 commits, 13 tagged releases, 77 commits touching tests",
                "es": "117 commits, 13 versiones etiquetadas, 77 commits con cambios en pruebas",
            },
            {"en": "Version 1.0.0 published on PyPI", "es": "Versión 1.0.0 publicada en PyPI"},
        ],
        "links": [
            ("GitHub", f"{GITHUB_URL}/vigia-eew"),
            ("PyPI", "https://pypi.org/project/vigia-eew/"),
        ],
    },
    {
        "name": "Silverpoint",
        "tagline": {
            "en": "Charts for React and Angular drawn in the manner of a Renaissance silverpoint drawing.",
            "es": "Gráficos para React y Angular trazados a la manera de un dibujo renacentista a punta de plata.",
        },
        "tags": ["TypeScript", "React", "Angular", "D3", "MCP", "Reflex"],
        "facts": [
            {
                "en": "187 commits in 40 days (September–October 2026)",
                "es": "187 commits en 40 días (septiembre–octubre de 2026)",
            },
            {
                "en": "An MCP server documents every chart and component for AI assistants",
                "es": "Un servidor MCP documenta cada gráfico y componente para asistentes de IA",
            },
            {
                "en": "reflex-silverpoint-react on PyPI: the Reflex wrapper this site is built with",
                "es": "reflex-silverpoint-react en PyPI: el wrapper de Reflex con el que está hecho este sitio",
            },
        ],
        "links": [
            ({"en": "Site", "es": "Sitio"}, "https://silverpointweb.vercel.app/"),
            ("GitHub", "https://github.com/ecrespo/silverpoint"),
        ],
    },
    {
        "name": "LangChain",
        "tagline": {
            "en": "LLM applications with LangChain: local models, agents and APIs.",
            "es": "Aplicaciones de LLM con LangChain: modelos locales, agentes y APIs.",
        },
        "tags": ["LangChain", "Ollama", "CrewAI", "FastAPI"],
        "facts": [
            {
                "en": "langchain_tutorials: hands-on LangChain exercises",
                "es": "langchain_tutorials: ejercicios prácticos de LangChain",
            },
            {
                "en": "fastapi_ollama_langchain: an LLM service on FastAPI and Ollama",
                "es": "fastapi_ollama_langchain: un servicio de LLM con FastAPI y Ollama",
            },
            {
                "en": "crewai_ollama_langchain: CrewAI agents on local models",
                "es": "crewai_ollama_langchain: agentes de CrewAI con modelos locales",
            },
        ],
        "links": [("GitHub", f"{GITHUB_URL}?tab=repositories&q=langchain")],
    },
    {
        "name": "LangGraph",
        "tagline": {
            "en": "Stateful agents and graphs with LangGraph, from notebooks to apps.",
            "es": "Agentes y grafos con estado en LangGraph, de los notebooks a las aplicaciones.",
        },
        "tags": ["LangGraph", "MCP", "Reflex", "Jupyter"],
        "facts": [
            {"en": "Langgraph_tutorials: 30 notebooks", "es": "Langgraph_tutorials: 30 notebooks"},
            {
                "en": "recruitment_agency: a LangGraph app that screens candidates by profile, with a Reflex UI",
                "es": "recruitment_agency: una app de LangGraph que evalúa candidatos por perfil, con interfaz en Reflex",
            },
            {
                "en": "onlyVans: a data-analysis agent with a Reflex chatbot; demo_mcp_agent: a LangGraph agent over MCP",
                "es": "onlyVans: un agente de análisis de datos con un chatbot en Reflex; demo_mcp_agent: un agente de LangGraph sobre MCP",
            },
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

ACTIVITY_SPAN = {"en": "January 2024 – October 2026", "es": "enero de 2024 – octubre de 2026"}

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
