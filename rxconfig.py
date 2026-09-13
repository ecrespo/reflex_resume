import reflex as rx

config = rx.Config(
    app_name="web",
    api_url="https://api.seraph.to",
    favicon="👨‍🔬",
    state_manager_mode="memory",  # Use in-memory state manager for Vercel deployment
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(theme=rx.theme(appearance="light")),
    ],
    cookie_secure=True,
    cors_allow_origins=["http://localhost:3000", "https://seraph.to", "https://www.seraph.to"],
)
