from typing import Any

import reflex as rx

from ..dev_dashboard_data import (
    ALL_PROFILES,
    DEFAULT_PERIOD,
    DEFAULT_PROFILE,
    DEFAULT_TOP_N,
    IMPACT,
    PERIODS,
    PROFILE_POINTS,
    REPO_DETAILS,
    es_list,
    es_rows,
    es_term,
    get_slice,
)

_DEFAULT = get_slice(DEFAULT_PERIOD, DEFAULT_PROFILE)

# Rows drawn by the compact charts, so the whole dashboard fits one screen.
CHART_ROWS = 12
IMPACT_ROWS = 8


def _es_number(value: int) -> str:
    """3,119 → 3.119."""
    return f"{value:,}".replace(",", ".")


class DevDashboardState(rx.State):
    """Filters, drill-downs and the slice of chart rows shown on `/dev-dashboard-stats`.

    Every field has a static default (the all-time, all-profiles slice), so the
    exported page draws real data before the backend answers; the filters and
    the drill-downs need the backend, and only swap whole slices.
    """

    # Controls.
    period: str = DEFAULT_PERIOD
    profile: str = ALL_PROFILES
    top_n: int = DEFAULT_TOP_N
    tab: str = "activity"

    # The slice on screen.
    kpis: dict[str, Any] = _DEFAULT["kpis"]
    monthly: list[dict] = _DEFAULT["monthly"]
    yearly: list[dict] = _DEFAULT["yearly"]
    weekly: list[dict] = _DEFAULT["weekly"]
    weekday: list[dict] = _DEFAULT["weekday"]
    hours: list[dict] = _DEFAULT["hours"]
    heatmap: list[dict] = _DEFAULT["heatmap"]
    heatmap_max: int = _DEFAULT["heatmap_max"]
    day_sizes: list[dict] = _DEFAULT["day_sizes"]
    repos_all: list[dict] = _DEFAULT["repos"]
    tech: list[dict] = _DEFAULT["tech"]
    tech_tree: list[dict] = _DEFAULT["tech_tree"]
    stack: list[dict] = _DEFAULT["stack"]
    stack_categories: list[dict] = _DEFAULT["stack_categories"]
    profile_mix: list[dict] = _DEFAULT["profile_mix"]

    # Constant across filters.
    profile_points: list[dict] = PROFILE_POINTS

    # Drill-downs and linked highlights.
    tech_root: str | None = None
    selected_repo: str = ""
    repo_detail: dict[str, Any] = {}
    repo_monthly: list[dict] = []
    linked_day: str = ""

    # ------------------------------------------------------------------ #
    # Derived rows
    # ------------------------------------------------------------------ #

    @rx.var
    def repos_top(self) -> list[dict]:
        return self.repos_all[: self.top_n]

    @rx.var
    def tech_top(self) -> list[dict]:
        return self.tech[:CHART_ROWS]

    @rx.var
    def stack_top(self) -> list[dict]:
        return self.stack[:CHART_ROWS]

    @rx.var
    def impact_top(self) -> list[dict]:
        return self.impact_rows[:IMPACT_ROWS]

    @rx.var
    def impact_rows(self) -> list[dict]:
        if self.profile == ALL_PROFILES:
            return IMPACT
        return [project for project in IMPACT if self.profile in project["profiles"]]

    @rx.var
    def repo_facts(self) -> list[dict]:
        d = self.repo_detail
        if not d:
            return []
        return [
            {"label": "Commits", "value": f"{d['commits']:,}"},
            {"label": "Active days", "value": str(d["active_days"])},
            {"label": "First → last", "value": f"{d['first']} → {d['last']}"},
            {"label": "Span", "value": f"{d['span_days']:,} days"},
            {"label": "Trajectory", "value": d["trajectory"]},
            {"label": "Language", "value": d["language"]},
            {"label": "Tags / merges", "value": f"{d['tags']} / {d['merges']}"},
            {"label": "On PyPI", "value": "Yes" if d["pypi"] else "No"},
            {"label": "Technologies", "value": d["techs"]},
            {"label": "Stack", "value": d["stack"]},
            {"label": "Profiles", "value": d["profiles"]},
        ]

    # ------------------------------------------------------------------ #
    # The same rows in Spanish, for `/es/dev-dashboard-stats`
    # ------------------------------------------------------------------ #

    @rx.var
    def kpis_es(self) -> dict[str, Any]:
        return {**self.kpis, "commits": str(self.kpis["commits"]).replace(",", ".")}

    @rx.var
    def weekly_es(self) -> list[dict]:
        return es_rows(self.weekly, "week")

    @rx.var
    def weekday_es(self) -> list[dict]:
        return es_rows(self.weekday, "day")

    @rx.var
    def heatmap_es(self) -> list[dict]:
        return es_rows(self.heatmap, "day")

    @rx.var
    def tech_tree_es(self) -> list[dict]:
        return es_rows(self.tech_tree, "name")

    @rx.var
    def tech_top_es(self) -> list[dict]:
        return es_rows(self.tech_top, "tech", "label")

    @rx.var
    def stack_top_es(self) -> list[dict]:
        return es_rows(self.stack_top, "category")

    @rx.var
    def stack_categories_es(self) -> list[dict]:
        return es_rows(self.stack_categories, "name")

    @rx.var
    def profile_mix_es(self) -> list[dict]:
        return es_rows(self.profile_mix, "profile", "label")

    @rx.var
    def impact_top_es(self) -> list[dict]:
        return es_rows(self.impact_top, "project", "trajectory", "profiles_text", "label")

    @rx.var
    def profile_points_es(self) -> list[dict]:
        return es_rows(self.profile_points, "profile", "map_quadrant", "visibility_quadrant")

    @rx.var
    def repo_facts_es(self) -> list[dict]:
        d = self.repo_detail
        if not d:
            return []
        return [
            {"label": "Commits", "value": _es_number(d["commits"])},
            {"label": "Días activos", "value": str(d["active_days"])},
            {"label": "Primero → último", "value": f"{d['first']} → {d['last']}"},
            {"label": "Duración", "value": f"{_es_number(d['span_days'])} días"},
            {"label": "Trayectoria", "value": es_term(d["trajectory"])},
            {"label": "Lenguaje", "value": d["language"]},
            {"label": "Etiquetas / merges", "value": f"{d['tags']} / {d['merges']}"},
            {"label": "En PyPI", "value": "Sí" if d["pypi"] else "No"},
            {"label": "Tecnologías", "value": d["techs"]},
            {"label": "Stack", "value": d["stack"]},
            {"label": "Perfiles", "value": es_list(d["profiles"])},
        ]

    @rx.var
    def filter_summary(self) -> str:
        period = {p["key"]: p["label"] for p in PERIODS}.get(self.period, self.period)
        return f"{period} · {self.profile}"

    # ------------------------------------------------------------------ #
    # Events
    # ------------------------------------------------------------------ #

    def _load_slice(self):
        profile = DEFAULT_PROFILE if self.profile == ALL_PROFILES else self.profile
        data = get_slice(self.period, profile)
        self.kpis = data["kpis"]
        self.monthly = data["monthly"]
        self.yearly = data["yearly"]
        self.weekly = data["weekly"]
        self.weekday = data["weekday"]
        self.hours = data["hours"]
        self.heatmap = data["heatmap"]
        self.heatmap_max = data["heatmap_max"]
        self.day_sizes = data["day_sizes"]
        self.repos_all = data["repos"]
        self.tech = data["tech"]
        self.tech_tree = data["tech_tree"]
        self.stack = data["stack"]
        self.stack_categories = data["stack_categories"]
        self.profile_mix = data["profile_mix"]
        # A drilled-into technology group may not exist in the new slice.
        self.tech_root = None

    @rx.event
    def set_period(self, value: str):
        self.period = value
        self._load_slice()

    @rx.event
    def set_profile(self, value: str):
        self.profile = value
        self._load_slice()

    @rx.event
    def set_top_n(self, value: float):
        self.top_n = int(value)

    @rx.event
    def set_tab(self, value: str):
        self.tab = value

    @rx.event
    def reset_filters(self):
        self.period = DEFAULT_PERIOD
        self.profile = ALL_PROFILES
        self.top_n = DEFAULT_TOP_N
        self._load_slice()

    @rx.event
    def set_tech_root(self, node_id: str | None):
        """Drill the technology treemap: a click on a technology opens its group.

        The treemap sends the id of the node clicked. A technology is a leaf, and
        drawing a leaf as the root would fill the frame with one cell, so a leaf
        opens its parent group instead; a group needs two or more technologies to
        be worth opening. The top of the tree is `None`.
        """
        if node_id in (None, "root"):
            self.tech_root = None
            return
        rows = {row["id"]: row for row in self.tech_tree}
        children = [row for row in self.tech_tree if row.get("parent") == node_id]
        if not children:
            node_id = (rows.get(node_id) or {}).get("parent")
            if node_id in (None, "root"):
                return
            children = [row for row in self.tech_tree if row.get("parent") == node_id]
        if len(children) >= 2:
            self.tech_root = node_id

    @rx.event
    def select_repo(self, item: dict):
        """A bar of the repository chart was clicked: open its detail."""
        datum = (item or {}).get("datum") or {}
        name = datum.get("repo", "")
        detail = REPO_DETAILS.get(name)
        if not detail:
            return
        self.selected_repo = name
        self.repo_detail = {k: v for k, v in detail.items() if k != "monthly"}
        self.repo_monthly = detail["monthly"]

    @rx.event
    def clear_repo(self):
        self.selected_repo = ""
        self.repo_detail = {}
        self.repo_monthly = []

    @rx.event
    def on_day_link(self, link: dict | None):
        self.linked_day = link["value"] if link else ""
