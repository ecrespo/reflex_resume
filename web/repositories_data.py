"""Repositories shown on the Portfolio page (`/portfolio`).

Generated from the same git history as the Dev Dashboard Stats page: hand-written commits by the
account owner across ecrespo and the prismal-ai organisation, as of 2026-10-25. Every repository
with commits in 2026 is listed, plus the older LangChain / LangGraph labs and data-science work.
"""

DATA_AS_OF = "2026-10-25"
YEAR = 2026

CATEGORIES = [
    {"id": "ai", "title": "Agentic AI & LLM apps"},
    {"id": "labs", "title": "LangChain & LangGraph labs"},
    {"id": "reflex", "title": "Reflex custom components"},
    {"id": "viz", "title": "Data visualization"},
    {"id": "data", "title": "Data science & EDAs"},
    {"id": "tools", "title": "Tools & desktop"},
    {"id": "sites", "title": "Sites"},
]

REPOSITORIES = [
    {
        "name": "prismal",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Prism-inspired multi-agent orchestration framework built on LangGraph: "
        "security-first, provider-agnostic and composable.",
        "commits_2026": 504,
        "commits_total": 504,
        "first": "2026-02-25",
        "last": "2026-10-22",
        "tags": ["Python", "Anthropic", "Docker", "Hugging Face", "LangGraph"],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal")],
    },
    {
        "name": "umbral",
        "owner": "ecrespo",
        "category": "ai",
        "description": "Local-first agentic terminal written in Go, with MCP tools and Anthropic / "
        "OpenAI providers.",
        "commits_2026": 223,
        "commits_total": 223,
        "first": "2026-09-11",
        "last": "2026-10-24",
        "tags": ["Go", "Anthropic", "MCP", "OpenAI", "SQLite"],
        "links": [("GitHub", "https://github.com/ecrespo/umbral")],
    },
    {
        "name": "prismal-server",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "REST, WebSocket and SSE API server for the Prismal framework.",
        "commits_2026": 22,
        "commits_total": 22,
        "first": "2026-05-31",
        "last": "2026-10-12",
        "tags": ["Python", "Docker", "FastAPI", "Pydantic"],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-server")],
    },
    {
        "name": "chatbot",
        "owner": "ecrespo",
        "category": "ai",
        "description": "Reflex chatbot built on reflex-assistant-ui that talks to any OpenAI-compatible "
        "server (OpenAI, Ollama and others).",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-09-27",
        "last": "2026-10-24",
        "tags": ["Python", "Docker", "Ollama", "OpenAI", "React"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/chatbot"),
            ("PyPI", "https://pypi.org/project/chatbot/"),
        ],
    },
    {
        "name": "prismal-sdk",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Python client for prismal-server over REST, WebSocket and SSE.",
        "commits_2026": 7,
        "commits_total": 7,
        "first": "2026-05-31",
        "last": "2026-07-20",
        "tags": ["Python", "Pydantic"],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-sdk")],
    },
    {
        "name": "onlyVans",
        "owner": "ecrespo",
        "category": "ai",
        "description": "Data-analysis assistant: a LangGraph agent over PostgreSQL with a Reflex chat "
        "interface.",
        "commits_2026": 5,
        "commits_total": 5,
        "first": "2026-01-28",
        "last": "2026-01-30",
        "tags": ["Python", "Docker", "Jupyter", "LangGraph", "Matplotlib"],
        "links": [("GitHub", "https://github.com/ecrespo/onlyVans")],
    },
    {
        "name": "skills",
        "owner": "ecrespo",
        "category": "ai",
        "description": "Seven Agent Skills for software-engineering workflows: architecture evaluation, "
        "scaffolding, reviews and more.",
        "commits_2026": 5,
        "commits_total": 5,
        "first": "2026-08-04",
        "last": "2026-09-06",
        "tags": ["Markdown", "Agent Skills"],
        "links": [("GitHub", "https://github.com/ecrespo/skills")],
    },
    {
        "name": "recruitment_agency",
        "owner": "ecrespo",
        "category": "ai",
        "description": "LangGraph application that screens candidates against a job profile, with a "
        "Reflex web UI.",
        "commits_2026": 4,
        "commits_total": 4,
        "first": "2026-01-18",
        "last": "2026-02-01",
        "tags": ["Python", "LangGraph", "OpenAI", "Pydantic", "Reflex"],
        "links": [("GitHub", "https://github.com/ecrespo/recruitment_agency")],
    },
    {
        "name": "prisma-notebooks",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Jupyter notebooks with worked examples of the Prismal framework.",
        "commits_2026": 3,
        "commits_total": 3,
        "first": "2026-05-31",
        "last": "2026-07-13",
        "tags": ["Jupyter", "LangGraph", "Matplotlib", "pandas"],
        "links": [("GitHub", "https://github.com/prismal-ai/prisma-notebooks")],
    },
    {
        "name": "demo_mcp_agent",
        "owner": "ecrespo",
        "category": "ai",
        "description": "LangGraph agent demo that calls MCP tools, with a FastAPI backend and a Reflex "
        "UI.",
        "commits_2026": 2,
        "commits_total": 2,
        "first": "2026-01-22",
        "last": "2026-02-01",
        "tags": ["Python", "Anthropic", "Docker", "FastAPI", "LangGraph"],
        "links": [("GitHub", "https://github.com/ecrespo/demo_mcp_agent")],
    },
    {
        "name": "prismal-chatbot",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Connectors that put Prismal agents behind external chat bots.",
        "commits_2026": 2,
        "commits_total": 2,
        "first": "2026-05-31",
        "last": "2026-07-19",
        "tags": [],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-chatbot")],
    },
    {
        "name": "prismal-dashboard",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Admin web dashboard for Prismal.",
        "commits_2026": 2,
        "commits_total": 2,
        "first": "2026-05-31",
        "last": "2026-07-19",
        "tags": [],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-dashboard")],
    },
    {
        "name": "prismal-tui",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Terminal user interface for Prismal.",
        "commits_2026": 2,
        "commits_total": 2,
        "first": "2026-05-31",
        "last": "2026-07-19",
        "tags": [],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-tui")],
    },
    {
        "name": "prismal-webchat",
        "owner": "prismal-ai",
        "category": "ai",
        "description": "Web chat front end for Prismal agents.",
        "commits_2026": 2,
        "commits_total": 2,
        "first": "2026-05-31",
        "last": "2026-07-19",
        "tags": [],
        "links": [("GitHub", "https://github.com/prismal-ai/prismal-webchat")],
    },
    {
        "name": "Langgraph_tutorials",
        "owner": "ecrespo",
        "category": "labs",
        "description": "Hands-on LangGraph notebooks with Claude: typed state, checkpoints, branching, "
        "multi-agent supervisors, agentic RAG, computer-use agents and human-in-the-loop.",
        "commits_2026": 9,
        "commits_total": 9,
        "first": "2026-04-12",
        "last": "2026-05-24",
        "tags": ["Jupyter", "Anthropic", "Hugging Face", "LangGraph", "Matplotlib"],
        "links": [("GitHub", "https://github.com/ecrespo/Langgraph_tutorials")],
    },
    {
        "name": "langchain_tutorials",
        "owner": "ecrespo",
        "category": "labs",
        "description": "61 progressive LangChain exercises: prompts, tools, structured output, memory "
        "and full workflows.",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-03-25",
        "last": "2026-04-03",
        "tags": ["Python", "Anthropic", "LangChain", "OpenAI", "Pydantic"],
        "links": [("GitHub", "https://github.com/ecrespo/langchain_tutorials")],
    },
    {
        "name": "crewai_ollama_langchain",
        "owner": "ecrespo",
        "category": "labs",
        "description": "CrewAI agents running on local Ollama models through LangChain.",
        "commits_2026": 0,
        "commits_total": 4,
        "first": "2024-03-31",
        "last": "2024-03-31",
        "tags": ["Python", "LangChain", "Ollama"],
        "links": [("GitHub", "https://github.com/ecrespo/crewai_ollama_langchain")],
    },
    {
        "name": "fastapi_ollama_langchain",
        "owner": "ecrespo",
        "category": "labs",
        "description": "FastAPI service that serves an Ollama LLM through LangChain, with Redis caching.",
        "commits_2026": 0,
        "commits_total": 4,
        "first": "2024-03-16",
        "last": "2024-03-17",
        "tags": ["Python", "Docker", "FastAPI", "LangChain", "Ollama"],
        "links": [("GitHub", "https://github.com/ecrespo/fastapi_ollama_langchain")],
    },
    {
        "name": "streamlit_whisper_gpt",
        "owner": "ecrespo",
        "category": "labs",
        "description": "Streamlit app that transcribes audio with Whisper and processes the text with "
        "GPT.",
        "commits_2026": 0,
        "commits_total": 1,
        "first": "2022-12-12",
        "last": "2022-12-12",
        "tags": ["Python", "Hugging Face", "OpenAI", "Streamlit", "pandas"],
        "links": [("GitHub", "https://github.com/ecrespo/streamlit_whisper_gpt")],
    },
    {
        "name": "reflex-mapcn",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "mapcn maps for Reflex: ready-made, themeable map components.",
        "commits_2026": 42,
        "commits_total": 42,
        "first": "2026-09-10",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-mapcn"),
            ("PyPI", "https://pypi.org/project/reflex-mapcn/"),
        ],
    },
    {
        "name": "reflex-rosencharts",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Port of rosencharts (D3 + Tailwind) to Reflex: 43 charts in pure Python.",
        "commits_2026": 29,
        "commits_total": 29,
        "first": "2026-06-14",
        "last": "2026-10-25",
        "tags": ["TypeScript", "Reflex", "Tailwind"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-rosencharts"),
            ("PyPI", "https://pypi.org/project/reflex-rosencharts/"),
        ],
    },
    {
        "name": "reflex-silverpoint-react",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Silverpoint charts for Reflex: charts drawn in the manner of a Renaissance "
        "silverpoint drawing.",
        "commits_2026": 25,
        "commits_total": 25,
        "first": "2026-09-25",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-silverpoint-react"),
            ("PyPI", "https://pypi.org/project/reflex-silverpoint-react/"),
        ],
    },
    {
        "name": "reflex-perspective",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "FINOS Perspective for Reflex: streaming data grids and pivot charts for large "
        "datasets.",
        "commits_2026": 19,
        "commits_total": 19,
        "first": "2026-09-22",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-perspective"),
            ("PyPI", "https://pypi.org/project/reflex-perspective/"),
        ],
    },
    {
        "name": "reflex-react-player",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "react-player v3 for Reflex: YouTube, Vimeo, HLS, DASH, Mux, Spotify, Twitch and "
        "more.",
        "commits_2026": 18,
        "commits_total": 18,
        "first": "2026-06-21",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-react-player"),
            ("PyPI", "https://pypi.org/project/reflex-react-player/"),
        ],
    },
    {
        "name": "reflex-react-flow",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "React Flow v12 for Reflex: node-based editors and flow diagrams in pure Python.",
        "commits_2026": 15,
        "commits_total": 15,
        "first": "2026-08-08",
        "last": "2026-10-25",
        "tags": ["Python", "LangGraph", "Pydantic", "Reflex"],
        "links": [("GitHub", "https://github.com/ecrespo/reflex-react-flow")],
    },
    {
        "name": "reflex-threejs",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "three.js for Reflex through React Three Fiber and drei: 3D scenes in pure "
        "Python.",
        "commits_2026": 15,
        "commits_total": 15,
        "first": "2026-06-14",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex", "Three.js"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-threejs"),
            ("PyPI", "https://pypi.org/project/reflex-threejs/"),
        ],
    },
    {
        "name": "reflex-hairline",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Hairline for Reflex: six isometric line figures that react to the pointer.",
        "commits_2026": 12,
        "commits_total": 12,
        "first": "2026-10-07",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-hairline"),
            ("PyPI", "https://pypi.org/project/reflex-hairline/"),
        ],
    },
    {
        "name": "reflex-plasma-ui",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Plasma UI for Reflex: liquid-glass panels.",
        "commits_2026": 12,
        "commits_total": 12,
        "first": "2026-09-22",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-plasma-ui"),
            ("PyPI", "https://pypi.org/project/reflex-plasma-ui/"),
        ],
    },
    {
        "name": "reflex-charts",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Chart.js for Reflex, wrapping react-chartjs-2.",
        "commits_2026": 11,
        "commits_total": 11,
        "first": "2026-06-14",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-charts"),
            ("PyPI", "https://pypi.org/project/reflex-charts/"),
        ],
    },
    {
        "name": "reflex-icd11ect",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "WHO ICD-11 Embedded Classification Tool for Reflex: diagnosis search and coding.",
        "commits_2026": 11,
        "commits_total": 11,
        "first": "2026-09-17",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-icd11ect"),
            ("PyPI", "https://pypi.org/project/reflex-icd11ect/"),
        ],
    },
    {
        "name": "reflex-reactbits",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "React Bits for Reflex: animated, interactive UI components and backgrounds.",
        "commits_2026": 11,
        "commits_total": 11,
        "first": "2026-09-18",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex", "Three.js"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-reactbits"),
            ("PyPI", "https://pypi.org/project/reflex-reactbits/"),
        ],
    },
    {
        "name": "reflex-knightlab-timeline",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Knight Lab TimelineJS for Reflex: interactive storytelling timelines.",
        "commits_2026": 10,
        "commits_total": 10,
        "first": "2026-06-14",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex", "Tailwind"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-knightlab-timeline"),
            ("PyPI", "https://pypi.org/project/reflex-knightlab-timeline/"),
        ],
    },
    {
        "name": "reflex-mapgl-maplibre",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "MapLibre GL JS maps for Reflex through react-map-gl: markers, popups, GeoJSON "
        "layers, clustering and heatmaps.",
        "commits_2026": 10,
        "commits_total": 10,
        "first": "2026-06-21",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-mapgl-maplibre"),
            ("PyPI", "https://pypi.org/project/reflex-mapgl-maplibre/"),
        ],
    },
    {
        "name": "reflex-mermaidjs",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Mermaid for Reflex: flowcharts, sequence diagrams and more from Markdown-like "
        "text.",
        "commits_2026": 10,
        "commits_total": 10,
        "first": "2026-09-15",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex", "Tailwind"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-mermaidjs"),
            ("PyPI", "https://pypi.org/project/reflex-mermaidjs/"),
        ],
    },
    {
        "name": "reflex-nivo",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "nivo for Reflex: a rich set of D3-based data-visualization components.",
        "commits_2026": 10,
        "commits_total": 10,
        "first": "2026-09-17",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-nivo"),
            ("PyPI", "https://pypi.org/project/reflex-nivo/"),
        ],
    },
    {
        "name": "reflex-pragmatic-drag-and-drop",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Atlassian Pragmatic drag and drop for Reflex: sortable lists and Kanban boards.",
        "commits_2026": 10,
        "commits_total": 10,
        "first": "2026-06-14",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex", "Tailwind"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-pragmatic-drag-and-drop"),
            ("PyPI", "https://pypi.org/project/reflex-pragmatic-drag-and-drop/"),
        ],
    },
    {
        "name": "reflex-map3d",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "3D city maps for Reflex, built with React Three Fiber.",
        "commits_2026": 9,
        "commits_total": 9,
        "first": "2026-09-11",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex", "Tailwind", "Three.js"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-map3d"),
            ("PyPI", "https://pypi.org/project/reflex-map3d/"),
        ],
    },
    {
        "name": "reflex-react-github-calendar",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "react-github-calendar v5 for Reflex: a GitHub-style contribution calendar.",
        "commits_2026": 9,
        "commits_total": 9,
        "first": "2026-06-23",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-react-github-calendar"),
            ("PyPI", "https://pypi.org/project/reflex-react-github-calendar/"),
        ],
    },
    {
        "name": "reflex-monocharts",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Monocharts for Reflex: 30 monochromatic charts built from rounded-corner "
        "geometry.",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-09-12",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-monocharts"),
            ("PyPI", "https://pypi.org/project/reflex-monocharts/"),
        ],
    },
    {
        "name": "reflex-ohif-viewer",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "OHIF zero-footprint DICOM viewer for Reflex, including the oncology Lesion "
        "Tracker.",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-09-17",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-ohif-viewer"),
            ("PyPI", "https://pypi.org/project/reflex-ohif-viewer/"),
        ],
    },
    {
        "name": "reflex-react-globe-gl",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "react-globe-gl for Reflex: data on an interactive 3D globe.",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-09-21",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex", "Three.js"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-react-globe-gl"),
            ("PyPI", "https://pypi.org/project/reflex-react-globe-gl/"),
        ],
    },
    {
        "name": "reflex-schedule-x",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Schedule-X for Reflex: a modern event calendar, an alternative to FullCalendar.",
        "commits_2026": 8,
        "commits_total": 8,
        "first": "2026-09-17",
        "last": "2026-10-25",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-schedule-x"),
            ("PyPI", "https://pypi.org/project/reflex-schedule-x/"),
        ],
    },
    {
        "name": "reflex-ant-design",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Ant Design (antd) React components wrapped as Reflex components.",
        "commits_2026": 7,
        "commits_total": 7,
        "first": "2026-06-17",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-ant-design"),
            ("PyPI", "https://pypi.org/project/reflex-ant-design/"),
        ],
    },
    {
        "name": "reflex-blossom-carousel",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Blossom Carousel for Reflex: a native-scroll carousel with pointer drag.",
        "commits_2026": 7,
        "commits_total": 7,
        "first": "2026-06-14",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex", "Tailwind"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-blossom-carousel"),
            ("PyPI", "https://pypi.org/project/reflex-blossom-carousel/"),
        ],
    },
    {
        "name": "reflex-resium",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Resium for Reflex: Cesium 3D globes and maps.",
        "commits_2026": 7,
        "commits_total": 7,
        "first": "2026-09-15",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-resium"),
            ("PyPI", "https://pypi.org/project/reflex-resium/"),
        ],
    },
    {
        "name": "reflex-gravityui-graph",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "@gravity-ui/graph for Reflex: high-performance canvas graphs, flowcharts and "
        "node editors.",
        "commits_2026": 6,
        "commits_total": 6,
        "first": "2026-06-24",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-gravityui-graph"),
            ("PyPI", "https://pypi.org/project/reflex-gravityui-graph/"),
        ],
    },
    {
        "name": "reflex-jupyter-renderer-react",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Jupyter notebook renderer for Reflex: show .ipynb files with outputs in a page.",
        "commits_2026": 6,
        "commits_total": 6,
        "first": "2026-06-18",
        "last": "2026-10-24",
        "tags": ["Python", "Jupyter", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-jupyter-renderer-react"),
            ("PyPI", "https://pypi.org/project/reflex-jupyter-renderer-react/"),
        ],
    },
    {
        "name": "reflex-tanstack-charts",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "TanStack Charts for Reflex: a responsive, accessible visualization grammar.",
        "commits_2026": 6,
        "commits_total": 6,
        "first": "2026-08-07",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-tanstack-charts"),
            ("PyPI", "https://pypi.org/project/reflex-tanstack-charts/"),
        ],
    },
    {
        "name": "reflex-pdfslick",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "PDFSlick for Reflex: view and interact with PDF documents.",
        "commits_2026": 5,
        "commits_total": 5,
        "first": "2026-06-15",
        "last": "2026-10-24",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-pdfslick"),
            ("PyPI", "https://pypi.org/project/reflex-pdfslick/"),
        ],
    },
    {
        "name": "reflex-react-joyride",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "react-joyride for Reflex: guided tours for your apps.",
        "commits_2026": 5,
        "commits_total": 5,
        "first": "2026-09-16",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-react-joyride"),
            ("PyPI", "https://pypi.org/project/reflex-react-joyride/"),
        ],
    },
    {
        "name": "reflex-xtermjs",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "xterm.js for Reflex: a terminal for the web.",
        "commits_2026": 5,
        "commits_total": 5,
        "first": "2026-09-14",
        "last": "2026-10-25",
        "tags": ["Python", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-xtermjs"),
            ("PyPI", "https://pypi.org/project/reflex-xtermjs/"),
        ],
    },
    {
        "name": "reflex-google-analytics-reactjs",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "Google Analytics tracking for Reflex apps, built on React.",
        "commits_2026": 4,
        "commits_total": 4,
        "first": "2026-10-24",
        "last": "2026-10-24",
        "tags": ["Python", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-google-analytics-reactjs"),
            ("PyPI", "https://pypi.org/project/reflex-google-analytics-reactjs/"),
        ],
    },
    {
        "name": "reflex-assistant-ui",
        "owner": "ecrespo",
        "category": "reflex",
        "description": "assistant-ui for Reflex: a port of the React library for AI chat interfaces.",
        "commits_2026": 3,
        "commits_total": 3,
        "first": "2026-09-14",
        "last": "2026-10-24",
        "tags": ["Python", "LangChain", "Ollama", "React", "Reflex"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex-assistant-ui"),
            ("PyPI", "https://pypi.org/project/reflex-assistant-ui/"),
        ],
    },
    {
        "name": "silverpoint",
        "owner": "ecrespo",
        "category": "viz",
        "description": "Charts for React and Angular whose visual language is historical drawing "
        "technique, with an MCP server for AI assistants.",
        "commits_2026": 187,
        "commits_total": 187,
        "first": "2026-09-12",
        "last": "2026-10-21",
        "tags": ["TypeScript", "Angular", "D3", "MCP", "Next.js"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/silverpoint"),
            ("Site", "https://silverpointweb.vercel.app/"),
        ],
    },
    {
        "name": "streamlit-covid-19-vzla",
        "owner": "ecrespo",
        "category": "data",
        "description": "Streamlit dashboard that tracked COVID-19 cases in Venezuela.",
        "commits_2026": 0,
        "commits_total": 28,
        "first": "2020-07-04",
        "last": "2021-04-07",
        "tags": ["Python", "Docker", "Matplotlib", "NumPy", "Streamlit"],
        "links": [("GitHub", "https://github.com/ecrespo/streamlit-covid-19-vzla")],
    },
    {
        "name": "data_science_portfoliio",
        "owner": "ecrespo",
        "category": "data",
        "description": "17 notebooks: climate change, COVID-19, US retailers, Stanford Open Policing, "
        "Netflix, Spotify, video games, a movie recommender and more.",
        "commits_2026": 0,
        "commits_total": 21,
        "first": "2022-10-25",
        "last": "2023-03-20",
        "tags": ["Jupyter", "Matplotlib", "NumPy", "pandas"],
        "links": [("GitHub", "https://github.com/ecrespo/data_science_portfoliio")],
    },
    {
        "name": "signals_fft_streamlit",
        "owner": "ecrespo",
        "category": "data",
        "description": "Streamlit app that explores signals and their Fast Fourier Transform.",
        "commits_2026": 0,
        "commits_total": 10,
        "first": "2020-11-14",
        "last": "2021-03-07",
        "tags": ["Python", "Matplotlib", "NumPy", "Streamlit"],
        "links": [("GitHub", "https://github.com/ecrespo/signals_fft_streamlit")],
    },
    {
        "name": "tutorial_streamlit",
        "owner": "ecrespo",
        "category": "data",
        "description": "Multipage Streamlit tutorial: charts, dashboards, data exploration, forms, and "
        "an LLM page.",
        "commits_2026": 0,
        "commits_total": 9,
        "first": "2020-10-31",
        "last": "2023-08-13",
        "tags": ["Python", "Docker", "Hugging Face", "LangChain", "Matplotlib"],
        "links": [("GitHub", "https://github.com/ecrespo/tutorial_streamlit")],
    },
    {
        "name": "magnetic_fields",
        "owner": "ecrespo",
        "category": "data",
        "description": "Streamlit web app about magnetic fields, with interactive plots.",
        "commits_2026": 0,
        "commits_total": 5,
        "first": "2020-10-25",
        "last": "2020-11-01",
        "tags": ["Python", "Matplotlib", "NumPy", "Streamlit"],
        "links": [("GitHub", "https://github.com/ecrespo/magnetic_fields")],
    },
    {
        "name": "analisisobesidad-uk",
        "owner": "ecrespo",
        "category": "data",
        "description": "Analysis of the obesity data recorded in England up to 2014.",
        "commits_2026": 0,
        "commits_total": 3,
        "first": "2018-05-11",
        "last": "2018-05-11",
        "tags": ["Jupyter"],
        "links": [("GitHub", "https://github.com/ecrespo/analisisobesidad-uk")],
    },
    {
        "name": "articulos-cienciadedatos",
        "owner": "ecrespo",
        "category": "data",
        "description": "Notebooks behind blog articles on data science, such as dollar exchange-rate "
        "quotes from Quandl.",
        "commits_2026": 0,
        "commits_total": 2,
        "first": "2018-05-25",
        "last": "2018-05-25",
        "tags": ["Jupyter"],
        "links": [("GitHub", "https://github.com/ecrespo/articulos-cienciadedatos")],
    },
    {
        "name": "vigia-eew",
        "owner": "ecrespo",
        "category": "tools",
        "description": "Cross-platform, real-time earthquake early-warning desktop agent: EMSC WebSocket "
        "push with USGS REST fallback.",
        "commits_2026": 117,
        "commits_total": 117,
        "first": "2026-06-28",
        "last": "2026-10-17",
        "tags": ["Python", "WebSocket", "Pydantic"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/vigia-eew"),
            ("PyPI", "https://pypi.org/project/vigia-eew/"),
        ],
    },
    {
        "name": "omagnome",
        "owner": "ecrespo",
        "category": "tools",
        "description": "Opinionated, reversible, keyboard-first developer desktop for Ubuntu + GNOME.",
        "commits_2026": 53,
        "commits_total": 53,
        "first": "2026-08-22",
        "last": "2026-08-23",
        "tags": ["Shell", "GNOME", "Ubuntu"],
        "links": [("GitHub", "https://github.com/ecrespo/omagnome")],
    },
    {
        "name": "reflex_resume",
        "owner": "ecrespo",
        "category": "sites",
        "description": "This site: resume, portfolio, blog and GitHub dashboard, built with Reflex.",
        "commits_2026": 16,
        "commits_total": 50,
        "first": "2025-11-30",
        "last": "2026-10-18",
        "tags": ["Python", "Docker", "Reflex", "Tailwind", "Vercel"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/reflex_resume"),
            ("Site", "https://reflexresume.vercel.app"),
        ],
    },
    {
        "name": "silverpoint_web",
        "owner": "ecrespo",
        "category": "sites",
        "description": "Documentation and showcase site for Silverpoint, built with Reflex.",
        "commits_2026": 11,
        "commits_total": 11,
        "first": "2026-09-26",
        "last": "2026-10-21",
        "tags": ["Python", "Reflex", "Vercel"],
        "links": [
            ("GitHub", "https://github.com/ecrespo/silverpoint_web"),
            ("Site", "https://silverpointweb.vercel.app"),
        ],
    },
]

# --------------------------------------------------------------------------- #
# Spanish
# --------------------------------------------------------------------------- #

CATEGORY_TITLES_ES = {
    "ai": "IA agéntica y aplicaciones de LLM",
    "labs": "Laboratorios de LangChain y LangGraph",
    "reflex": "Componentes personalizados de Reflex",
    "viz": "Visualización de datos",
    "data": "Ciencia de datos y EDAs",
    "tools": "Herramientas y escritorio",
    "sites": "Sitios",
}

# Repository (`owner/name`) → its description in Spanish.
DESCRIPTIONS_ES = {
    "prismal-ai/prismal": (
        "Framework de orquestación multiagente inspirado en un prisma, construido sobre "
        "LangGraph: la seguridad primero, agnóstico del proveedor y componible."
    ),
    "ecrespo/umbral": (
        "Terminal agéntica local-first escrita en Go, con herramientas MCP y proveedores "
        "Anthropic / OpenAI."
    ),
    "prismal-ai/prismal-server": "Servidor de API REST, WebSocket y SSE para el framework Prismal.",
    "ecrespo/chatbot": (
        "Chatbot en Reflex sobre reflex-assistant-ui que habla con cualquier servidor compatible "
        "con la API de OpenAI (OpenAI, Ollama y otros)."
    ),
    "prismal-ai/prismal-sdk": "Cliente en Python para prismal-server sobre REST, WebSocket y SSE.",
    "ecrespo/onlyVans": (
        "Asistente de análisis de datos: un agente de LangGraph sobre PostgreSQL con una "
        "interfaz de chat en Reflex."
    ),
    "ecrespo/skills": (
        "Siete Agent Skills para flujos de ingeniería de software: evaluación de arquitectura, "
        "scaffolding, revisiones y más."
    ),
    "ecrespo/recruitment_agency": (
        "Aplicación de LangGraph que evalúa candidatos frente a un perfil de puesto, con "
        "interfaz web en Reflex."
    ),
    "prismal-ai/prisma-notebooks": "Notebooks de Jupyter con ejemplos resueltos del framework Prismal.",
    "ecrespo/demo_mcp_agent": (
        "Demo de un agente de LangGraph que llama herramientas MCP, con backend en FastAPI e "
        "interfaz en Reflex."
    ),
    "prismal-ai/prismal-chatbot": "Conectores que ponen los agentes de Prismal detrás de bots de chat externos.",
    "prismal-ai/prismal-dashboard": "Dashboard web de administración de Prismal.",
    "prismal-ai/prismal-tui": "Interfaz de terminal para Prismal.",
    "prismal-ai/prismal-webchat": "Chat web para los agentes de Prismal.",
    "ecrespo/Langgraph_tutorials": (
        "Notebooks prácticos de LangGraph con Claude: estado tipado, checkpoints, ramificación, "
        "supervisores multiagente, RAG agéntico, agentes de uso de computadora y "
        "human-in-the-loop."
    ),
    "ecrespo/langchain_tutorials": (
        "61 ejercicios progresivos de LangChain: prompts, herramientas, salida estructurada, "
        "memoria y flujos completos."
    ),
    "ecrespo/crewai_ollama_langchain": "Agentes de CrewAI con modelos locales de Ollama a través de LangChain.",
    "ecrespo/fastapi_ollama_langchain": (
        "Servicio en FastAPI que sirve un LLM de Ollama a través de LangChain, con caché en Redis."
    ),
    "ecrespo/streamlit_whisper_gpt": (
        "App en Streamlit que transcribe audio con Whisper y procesa el texto con GPT."
    ),
    "ecrespo/reflex-mapcn": "Mapas de mapcn para Reflex: componentes de mapa listos para usar y personalizables.",
    "ecrespo/reflex-rosencharts": "Port de rosencharts (D3 + Tailwind) a Reflex: 43 gráficos en Python puro.",
    "ecrespo/reflex-silverpoint-react": (
        "Gráficos Silverpoint para Reflex: gráficos trazados a la manera de un dibujo "
        "renacentista a punta de plata."
    ),
    "ecrespo/reflex-perspective": (
        "FINOS Perspective para Reflex: tablas de datos en streaming y gráficos dinámicos para "
        "grandes volúmenes de datos."
    ),
    "ecrespo/reflex-react-player": (
        "react-player v3 para Reflex: YouTube, Vimeo, HLS, DASH, Mux, Spotify, Twitch y más."
    ),
    "ecrespo/reflex-react-flow": (
        "React Flow v12 para Reflex: editores de nodos y diagramas de flujo en Python puro."
    ),
    "ecrespo/reflex-threejs": (
        "three.js para Reflex con React Three Fiber y drei: escenas 3D en Python puro."
    ),
    "ecrespo/reflex-hairline": "Hairline para Reflex: seis figuras isométricas de líneas que siguen al puntero.",
    "ecrespo/reflex-plasma-ui": "Plasma UI para Reflex: paneles de vidrio líquido.",
    "ecrespo/reflex-charts": "Chart.js para Reflex, sobre react-chartjs-2.",
    "ecrespo/reflex-icd11ect": (
        "Herramienta de clasificación integrada CIE-11 de la OMS para Reflex: búsqueda y "
        "codificación de diagnósticos."
    ),
    "ecrespo/reflex-reactbits": (
        "React Bits para Reflex: componentes de interfaz y fondos animados e interactivos."
    ),
    "ecrespo/reflex-knightlab-timeline": (
        "TimelineJS de Knight Lab para Reflex: líneas de tiempo interactivas para contar historias."
    ),
    "ecrespo/reflex-mapgl-maplibre": (
        "Mapas de MapLibre GL JS para Reflex con react-map-gl: marcadores, popups, capas "
        "GeoJSON, agrupamiento y mapas de calor."
    ),
    "ecrespo/reflex-mermaidjs": (
        "Mermaid para Reflex: diagramas de flujo, de secuencia y más a partir de texto similar a "
        "Markdown."
    ),
    "ecrespo/reflex-nivo": (
        "nivo para Reflex: un amplio conjunto de componentes de visualización de datos basados "
        "en D3."
    ),
    "ecrespo/reflex-pragmatic-drag-and-drop": (
        "Pragmatic drag and drop de Atlassian para Reflex: listas ordenables y tableros Kanban."
    ),
    "ecrespo/reflex-map3d": "Mapas 3D de ciudades para Reflex, hechos con React Three Fiber.",
    "ecrespo/reflex-react-github-calendar": (
        "react-github-calendar v5 para Reflex: un calendario de contribuciones al estilo de GitHub."
    ),
    "ecrespo/reflex-monocharts": (
        "Monocharts para Reflex: 30 gráficos monocromáticos hechos con geometría de esquinas "
        "redondeadas."
    ),
    "ecrespo/reflex-ohif-viewer": (
        "Visor DICOM OHIF, sin instalación, para Reflex, con el Lesion Tracker de oncología."
    ),
    "ecrespo/reflex-react-globe-gl": "react-globe-gl para Reflex: datos sobre un globo 3D interactivo.",
    "ecrespo/reflex-schedule-x": (
        "Schedule-X para Reflex: un calendario de eventos moderno, alternativa a FullCalendar."
    ),
    "ecrespo/reflex-ant-design": "Componentes React de Ant Design (antd) como componentes de Reflex.",
    "ecrespo/reflex-blossom-carousel": (
        "Blossom Carousel para Reflex: un carrusel con desplazamiento nativo y arrastre con el "
        "puntero."
    ),
    "ecrespo/reflex-resium": "Resium para Reflex: globos y mapas 3D de Cesium.",
    "ecrespo/reflex-gravityui-graph": (
        "@gravity-ui/graph para Reflex: grafos en canvas de alto rendimiento, diagramas de flujo "
        "y editores de nodos."
    ),
    "ecrespo/reflex-jupyter-renderer-react": (
        "Renderizador de notebooks de Jupyter para Reflex: muestra archivos .ipynb con sus "
        "salidas en una página."
    ),
    "ecrespo/reflex-tanstack-charts": (
        "TanStack Charts para Reflex: una gramática de visualización adaptable y accesible."
    ),
    "ecrespo/reflex-pdfslick": "PDFSlick para Reflex: visualiza documentos PDF e interactúa con ellos.",
    "ecrespo/reflex-react-joyride": "react-joyride para Reflex: recorridos guiados para tus aplicaciones.",
    "ecrespo/reflex-xtermjs": "xterm.js para Reflex: una terminal para la web.",
    "ecrespo/reflex-google-analytics-reactjs": (
        "Seguimiento con Google Analytics para aplicaciones de Reflex, sobre React."
    ),
    "ecrespo/reflex-assistant-ui": (
        "assistant-ui para Reflex: un port de la librería de React para interfaces de chat con IA."
    ),
    "ecrespo/silverpoint": (
        "Gráficos para React y Angular cuyo lenguaje visual son las técnicas históricas de "
        "dibujo, con un servidor MCP para asistentes de IA."
    ),
    "ecrespo/streamlit-covid-19-vzla": (
        "Dashboard en Streamlit que siguió los casos de COVID-19 en Venezuela."
    ),
    "ecrespo/data_science_portfoliio": (
        "17 notebooks: cambio climático, COVID-19, minoristas de EE. UU., Stanford Open "
        "Policing, Netflix, Spotify, videojuegos, un recomendador de películas y más."
    ),
    "ecrespo/signals_fft_streamlit": (
        "App en Streamlit que explora señales y su transformada rápida de Fourier."
    ),
    "ecrespo/tutorial_streamlit": (
        "Tutorial multipágina de Streamlit: gráficos, dashboards, exploración de datos, "
        "formularios y una página con un LLM."
    ),
    "ecrespo/magnetic_fields": "App web en Streamlit sobre campos magnéticos, con gráficos interactivos.",
    "ecrespo/analisisobesidad-uk": "Análisis de los datos de obesidad registrados en Inglaterra hasta 2014.",
    "ecrespo/articulos-cienciadedatos": (
        "Notebooks de artículos del blog sobre ciencia de datos, como las cotizaciones del dólar "
        "desde Quandl."
    ),
    "ecrespo/vigia-eew": (
        "Agente de escritorio multiplataforma de alerta sísmica temprana en tiempo real: avisos "
        "por WebSocket del EMSC con respaldo REST del USGS."
    ),
    "ecrespo/omagnome": (
        "Escritorio de desarrollo opinado, reversible y centrado en el teclado para Ubuntu + GNOME."
    ),
    "ecrespo/reflex_resume": (
        "Este sitio: currículum, portafolio, blog y dashboard de GitHub, hecho con Reflex."
    ),
    "ecrespo/silverpoint_web": "Sitio de documentación y muestra de Silverpoint, hecho con Reflex.",
}
