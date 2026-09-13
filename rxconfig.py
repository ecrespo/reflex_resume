import os

import reflex as rx

# The deployed frontend talks to the Railway backend. Override API_URL to run
# fully locally (see CLAUDE.md), otherwise `reflex run` serves a local
# frontend wired to production, and state added since the last deploy is
# missing from the deltas it receives.
API_URL = os.environ.get("API_URL", "https://api.seraph.to")


class VitePrebundlePlugin(rx.plugins.Plugin):
    """Pre-bundle npm deps that Vite would otherwise discover mid-session.

    The rosencharts, timeline and GitHub calendar components are NoSSR, so
    their packages (d3 above all) are only imported dynamically once a page
    mounts them. The dev server then re-optimizes its dependencies and bumps
    every `?v=` hash, and an in-flight `import("…/.vite/deps/d3.js?v=<old>")`
    fails with "error loading dynamically imported module": the charts stay
    blank. Listing them in `optimizeDeps.include` bundles them at startup.
    Only affects `reflex run`; production builds do not use the optimizer.
    """

    include: tuple[str, ...] = ("d3", "react-github-calendar", "@knight-lab/timelinejs")

    def pre_compile(self, **context):
        context["add_modify_task"]("vite.config.js", self._add_optimize_deps)

    def _add_optimize_deps(self, content: str) -> str:
        if "optimizeDeps: { include:" in content:
            return content
        include = ", ".join(f'"{dep}"' for dep in self.include)
        return content.replace(
            "\n  server: {",
            f"\n  optimizeDeps: {{ include: [{include}] }},\n  server: {{",
            1,
        )


config = rx.Config(
    app_name="web",
    api_url=API_URL,
    favicon="👨‍🔬",
    state_manager_mode="memory",  # Use in-memory state manager for Vercel deployment
    plugins=[
        rx.plugins.SitemapPlugin(),
        # `darkMode: "class"` keeps the `dark:` variants tied to the `.dark`
        # class instead of the OS setting: the app is pinned to the light Radix
        # appearance, and third-party components that ship `dark:` classes (the
        # reflex-rosencharts radars, for one) would otherwise render dark on a
        # light page for visitors whose system theme is dark. Note the plugin
        # config — not the root tailwind.config.js — is what generates
        # .web/tailwind.config.js, so the typography plugin has to be repeated.
        # `content` keeps Reflex's defaults (app/, utils/) and adds two paths.
        # public/external/ is where custom components such as reflex-rosencharts
        # ship their .tsx sources; without it their Tailwind classes (fills,
        # strokes, max-w-[18rem]) are never generated and the radars render as
        # huge black shapes. app_components/ is where Reflex compiles the class
        # names written in Python, so utilities used only there — the gradient
        # `from-*`/`to-*` strings the dev-stats charts pass as data, for one —
        # are otherwise missing from the production CSS.
        rx.plugins.TailwindV4Plugin(
            config={
                "content": [
                    "./app/**/*.{js,ts,jsx,tsx}",
                    "./app_components/**/*.{js,ts,jsx,tsx}",
                    "./utils/**/*.{js,ts,jsx,tsx}",
                    "./public/external/**/*.{js,ts,jsx,tsx}",
                ],
                "darkMode": "class",
                "plugins": ["@tailwindcss/typography@0.5.20"],
            }
        ),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light")),
        VitePrebundlePlugin(),
    ],
    cookie_secure=True,
    cors_allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://seraph.to",
        "https://www.seraph.to",
    ],
)
