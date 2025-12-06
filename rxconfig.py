import reflex as rx

config = rx.Config(
    app_name="web",
    favicon="👨‍🔬",
    state_manager_mode="memory",  # Use in-memory state manager for Vercel deployment
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)