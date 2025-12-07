import reflex as rx

config = rx.Config(
    app_name="web",
    favicon="👨‍🔬",
    state_manager_mode="memory",  # Use in-memory state manager for Vercel deployment
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    cookie_secure=True,
    cors_allow_origins=[
        "http://localhost:3000",
        "https://seraph.to",
        "https://www.seraph.to"
    ],
)