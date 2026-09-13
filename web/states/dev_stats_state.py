import reflex as rx

from ..dev_stats_data import (
    ANNUAL_COMMITS,
    CODE_COMPOSITION,
    CONVENTION_ADOPTION,
    DELIVERY_FUNNEL,
    MONTHLY_COMMITS,
    PORTFOLIO_SPLIT,
    REPO_LIFECYCLE,
    TOPICS_BUILT,
    TOPICS_STUDIED,
    WEEKDAY_RHYTHM,
)


class DevStatsState(rx.State):
    """Chart series for the `/dev-stats` page.

    Plain vars with static defaults rather than computed vars: the figures never
    change at runtime, and Reflex embeds a state's initial values in the compiled
    page, so every chart still renders if the backend is unreachable (the site
    ships as a static frontend with a separately deployed backend).
    """

    annual_commits: list[dict] = ANNUAL_COMMITS
    monthly_commits: list[dict] = MONTHLY_COMMITS
    convention_adoption: list[dict] = CONVENTION_ADOPTION
    topics_built: list[dict] = TOPICS_BUILT
    topics_studied: list[dict] = TOPICS_STUDIED
    code_composition: dict = CODE_COMPOSITION
    portfolio_split: list[dict] = PORTFOLIO_SPLIT
    weekday_rhythm: list[dict] = WEEKDAY_RHYTHM
    delivery_funnel: list[dict] = DELIVERY_FUNNEL
    repo_lifecycle: list[dict] = REPO_LIFECYCLE
