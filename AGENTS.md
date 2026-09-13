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

# AGENTS.md - Developer Portfolio Project

## Project Overview

This is a developer portfolio web application built with **Reflex**, a modern Python framework for building full-stack web applications. The project showcases a personal portfolio with sections for introduction, featured projects, and contact information.

## Technology Stack

- **Framework**: Reflex v0.8.21+
- **Language**: Python 3.13+
- **Package Manager**: `uv` (fast Python package installer and resolver)
- **Build Tool**: Reflex CLI
- **Styling**: Tailwind CSS v4 (via Reflex plugin)

## Project Structure

```
reflex-hello/
├── web/                    # Main application package
│   ├── __init__.py
│   └── web.py             # Main application code (pages, components, state)
├── assets/                # Static assets (images, fonts, etc.)
├── .web/                  # Generated frontend code (auto-generated)
├── .states/               # State persistence (auto-generated)
├── pyproject.toml         # Project dependencies and metadata
├── uv.lock               # Locked dependencies
├── rxconfig.py           # Reflex configuration
├── .python-version       # Python version specification (3.13)
└── README.md
```

## Environment Setup

### Prerequisites

- Python 3.13 or higher
- `uv` package manager installed

### Installation

1. **Clone the repository** (if not already):
   ```bash
   cd /home/ernesto/proyectos/reflex-hello
   ```

2. **Install dependencies with uv**:
   ```bash
   uv sync
   ```
   This will create a virtual environment and install all dependencies from `uv.lock`.

3. **Activate the virtual environment** (optional, uv handles this automatically):
   ```bash
   source .venv/bin/activate
   ```

## Common Commands

### Development

```bash
# Run the development server
uv run reflex run

# Run with auto-reload (hot reload)
uv run reflex run --reload
```

The app will be available at `http://localhost:3000`.

### Dependency Management

```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Update dependencies
uv sync

# Remove a dependency
uv remove <package-name>
```

### Build & Deploy

```bash
# Export the app for production
uv run reflex export

# Run production build
uv run reflex run --env prod
```

## Development Workflow

### Making Changes

1. **Edit components** in `web/web.py`
2. **Save the file** - Reflex will auto-reload in development mode
3. **View changes** at `http://localhost:3000`

### Adding New Pages

```python
# In web/web.py
def new_page() -> rx.Component:
    return rx.container(
        rx.heading("New Page"),
        # Your components here
    )


# Register the page
app.add_page(new_page, route="/new-page")
```

### State Management

The `State` class in `web/web.py` manages application state:

```python
class State(rx.State):
    """The app state."""

    # Add your state variables here
    # Example:
    # counter: int = 0
    #
    # def increment(self):
    #     self.counter += 1
```

## Best Practices

### 1. **Use uv for all package operations**
   - Always use `uv run` to execute commands to ensure correct environment
   - Use `uv add` instead of `pip install` to maintain `uv.lock`

### 2. **Keep components modular**
   - Break down UI into small, reusable functions
   - Each component function should return `rx.Component`
   - Follow the pattern: `def component_name() -> rx.Component:`

### 3. **State management**
   - Keep state variables at the class level
   - Use methods for state mutations
   - Avoid complex logic in component functions

### 4. **Styling with Reflex**
   - Use Reflex's built-in styling props (spacing, padding, color_scheme, etc.)
   - Leverage the Tailwind v4 plugin for custom styles when needed
   - Use `rx.card`, `rx.vstack`, `rx.hstack` for layouts

### 5. **File organization**
   - Keep all application code in the `web/` package
   - Use `assets/` for static files
   - Don't modify `.web/` or `.states/` manually (auto-generated)

### 6. **Version control**
   - Commit `uv.lock` to ensure reproducible builds
   - Don't commit `.venv/`, `.web/`, `.states/`, or `__pycache__/`

## Configuration

### Reflex Configuration (`rxconfig.py`)

```python
import reflex as rx

config = rx.Config(
    app_name="web",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
```

### Python Version (`.python-version`)

The project uses Python 3.13 as specified in `.python-version`. `uv` will automatically use this version.

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run `uv sync` to ensure all dependencies are installed

2. **Port already in use**
   - Kill the existing process: `lsof -ti:3000 | xargs kill -9`
   - Or use a different port: `uv run reflex run --port 8000`

3. **Changes not reflecting**
   - Ensure you're running with `--reload` flag
   - Clear browser cache (Ctrl+Shift+R)
   - Check terminal for error messages

4. **Virtual environment issues**
   - Delete `.venv/` and run `uv sync` again

## Resources

- [Reflex Documentation](https://reflex.dev/docs)
- [Reflex Component Library](https://reflex.dev/docs/library)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)

## Agent-Specific Notes

When working with this codebase as an AI agent:

1. **Always use `uv run` prefix** for Python commands to ensure correct environment
2. **Main application logic** is in `web/web.py` - this is where you'll make most changes
3. **Testing changes**: Run `uv run reflex run` and check `http://localhost:3000`
4. **Dependencies**: Use `uv add <package>` to add new dependencies
5. **Reflex uses reactive state** - changes to `State` variables automatically update the UI
6. **Component pattern**: Functions that return `rx.Component` are UI components
