import reflex as rx

config = rx.Config(
    app_name="web",
    favicon="👨‍🔬",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)