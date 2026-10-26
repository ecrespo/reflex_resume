"""The `/dev-dashboard-stats` page: the GitHub EDA, filtered and linked, on one screen.

An exploratory analysis of every hand-written commit in the `ecrespo` account and
the `prismal-ai` organisation, drawn so the reader can ask their own questions of
it. A period control and a profile select
swap the whole slice behind every chart (`DevDashboardState`), the tabs group
the charts into silverpoint `dashboard` grids sized so each view fits a desktop
screen without scrolling, and three interactions drill in:

- the weekday chart and the weekday x hour heatmap share the `day` link, so
  pointing at a day marks it in both;
- clicking a repository bar opens that repository's figures and monthly series;
- clicking a technology in the treemap draws its group as the root.

Row-oriented bar charts read the short `label` of each row (see
`dev_dashboard_data.short_label`); the full name is in the tooltip.
"""

import reflex as rx
from reflex_silverpoint_react import (
    bar_chart,
    bubble_chart,
    bullet_chart,
    dashboard,
    dashboard_cell,
    dashboard_cell_layout,
    dashboard_layout,
    donut_chart,
    heatmap_chart,
    line_chart,
    sp_button,
    sp_card,
    sp_descriptions,
    sp_empty,
    sp_segmented,
    sp_select,
    sp_slider,
    sp_statistic,
    sp_tab_panel,
    sp_tabs,
    squarified_treemap,
    tooltip_template,
    ui_item,
)

from ..dev_dashboard_data import (
    DATA_AS_OF,
    PERIODS,
    PERIODS_ES,
    PROFILE_ITEMS_ES,
    PROFILE_OPTIONS,
)
from ..i18n import format_iso_day, t
from ..states.dev_dashboard_state import DevDashboardState as S
from .dev_dashboard_sections import SECTIONS

_HOUR_LABELS = [f"{hour:02d}" for hour in range(24)]
_NOTE = "text-xs text-gray-600"

# Every view is a 2-row grid of this height, which with the header, the KPI strip
# and the tabs fits a 1080p desktop screen (about 930 px below the navbar).
_ROW_HEIGHT = 280
_GAP = 12
_VIEW_HEIGHT = 2 * _ROW_HEIGHT + _GAP
_COLUMNS = {"sm": 1, "md": 2, "lg": 4}

_TABS = [
    ("activity", {"en": "Activity", "es": "Actividad"}),
    ("rhythm", {"en": "Rhythm", "es": "Ritmo"}),
    ("repositories", {"en": "Repositories", "es": "Repositorios"}),
    ("technology", {"en": "Technology & stack", "es": "Tecnología y stack"}),
    ("profiles", {"en": "Profiles & impact", "es": "Perfiles e impacto"}),
]


def _rows(lang: str, english, spanish):
    """The state var a chart reads: the English rows, or the same rows in Spanish."""
    return spanish if lang == "es" else english


def _grid(*cells: rx.Component, grid_id: str, label: str, layout: list, **props) -> rx.Component:
    """A silverpoint dashboard without a visible heading: the tab already names it."""
    return dashboard(
        *cells,
        id=grid_id,
        label=label,
        layout=dashboard_layout(layout, columns=_COLUMNS, row_height=_ROW_HEIGHT, gap=_GAP),
        **props,
    )


# --------------------------------------------------------------------------- #
# Header: title, filters, KPIs
# --------------------------------------------------------------------------- #


def _header(lang: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                t(lang, "Dev Dashboard Stats", "Estadísticas de desarrollo"),
                class_name="text-2xl font-bold text-gray-800 leading-tight",
            ),
            rx.el.p(
                t(
                    lang,
                    f"3,119 hand-written commits · ecrespo + prismal-ai · as of "
                    f"{format_iso_day(DATA_AS_OF, lang)}",
                    f"3.119 commits escritos a mano · ecrespo + prismal-ai · al "
                    f"{format_iso_day(DATA_AS_OF, lang)}",
                ),
                class_name=_NOTE + " whitespace-nowrap",
            ),
            class_name="min-w-0 mr-auto",
        ),
        # The controls stay together and never wrap internally; the whole group
        # drops under the title only on narrow screens.
        rx.el.div(
            rx.el.div(
                sp_segmented(
                    label=t(lang, "Period", "Periodo"),
                    name="period",
                    items=[ui_item(p["key"], p["label"]) for p in _rows(lang, PERIODS, PERIODS_ES)],
                    value=S.period,
                    on_change=S.set_period,
                    size="sm",
                ),
                class_name="min-w-0 max-w-full overflow-x-auto [&_*]:whitespace-nowrap",
            ),
            rx.el.div(
                sp_select(
                    _rows(lang, PROFILE_OPTIONS, PROFILE_ITEMS_ES),
                    value=S.profile,
                    on_change=S.set_profile,
                    label=t(lang, "Profile", "Perfil"),
                    width="100%",
                    id="dashboard-profile",
                ),
                class_name="w-full sm:w-52",
            ),
            sp_button(
                t(lang, "Reset", "Restablecer"),
                size="sm",
                on_click=S.reset_filters,
                label=t(lang, "Reset filters", "Restablecer los filtros"),
            ),
            class_name="flex flex-wrap lg:flex-nowrap items-end gap-3 min-w-0",
        ),
        class_name="flex flex-wrap items-end gap-x-4 gap-y-2 mb-3",
    )


def _kpi(title: str, value, suffix: str | None = None) -> rx.Component:
    return rx.el.div(
        sp_statistic(title, value, suffix=suffix, size="sm"),
        class_name="px-3 py-1.5 border-r border-[#5C7B71]/30 last:border-r-0 min-w-0 overflow-hidden",
    )


def _kpis(lang: str) -> rx.Component:
    kpis = _rows(lang, S.kpis, S.kpis_es)
    return sp_card(
        rx.el.div(
            _kpi("Commits", kpis["commits"]),
            _kpi(t(lang, "Active days", "Días activos"), kpis["active_days"]),
            _kpi(t(lang, "Repositories", "Repositorios"), kpis["repos"]),
            _kpi(t(lang, "Streak", "Racha"), kpis["streak"], t(lang, " days", " días")),
            _kpi(t(lang, "Per active day", "Por día activo"), kpis["per_active_day"]),
            _kpi(t(lang, "Weekend", "Fin de semana"), kpis["weekend"], "%"),
            _kpi(t(lang, "Peak hour", "Hora pico"), kpis["peak_hour"]),
            _kpi(t(lang, "Conventional", "Convencionales"), kpis["conventional"], "%"),
            class_name="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8",
        ),
        size="sm",
        class_name="mb-3",
    )


# --------------------------------------------------------------------------- #
# Views
# --------------------------------------------------------------------------- #


def _activity(lang: str) -> rx.Component:
    return _grid(
        dashboard_cell(
            line_chart(
                data=S.monthly,
                x_key="month",
                value_key="commits",
                title=t(lang, "Commits per month", "Commits por mes"),
                unit="commits",
                tooltip=tooltip_template("{datum.month} · {value} commits"),
                id="dash-monthly",
            ),
            cell="monthly",
        ),
        dashboard_cell(
            bar_chart(
                data=S.day_sizes,
                x_key="size",
                value_key="days",
                title=t(lang, "Active days by commits", "Días activos según sus commits"),
                unit=t(lang, "days", "días"),
                id="dash-day-sizes",
            ),
            cell="sizes",
        ),
        dashboard_cell(
            bar_chart(
                data=S.yearly,
                x_key="year",
                value_key="commits",
                title=t(lang, "Commits per year", "Commits por año"),
                unit="commits",
                id="dash-yearly",
            ),
            cell="yearly",
        ),
        dashboard_cell(
            bar_chart(
                data=_rows(lang, S.weekly, S.weekly_es),
                x_key="week",
                value_key="commits",
                title=t(
                    lang,
                    "Commits per week (last 52 weeks of the period)",
                    "Commits por semana (últimas 52 semanas del periodo)",
                ),
                unit="commits",
                tooltip=tooltip_template(
                    t(
                        lang,
                        "Week of {datum.start} · {value} commits",
                        "Semana del {datum.start} · {value} commits",
                    )
                ),
                id="dash-weekly",
            ),
            cell="weekly",
        ),
        grid_id="dash-activity",
        label=t(lang, "Activity", "Actividad"),
        layout=[
            dashboard_cell_layout("monthly", col_span={"md": 2, "lg": 3}),
            dashboard_cell_layout("sizes", col_span={"md": 2, "lg": 1}),
            dashboard_cell_layout("yearly", col_span={"md": 1, "lg": 2}),
            dashboard_cell_layout("weekly", col_span={"md": 1, "lg": 2}),
        ],
    )


def _rhythm(lang: str) -> rx.Component:
    return _grid(
        dashboard_cell(
            bar_chart(
                data=_rows(lang, S.weekday, S.weekday_es),
                x_key="day",
                value_key="commits",
                title=t(lang, "By day of the week", "Por día de la semana"),
                unit="commits",
                id="dash-weekday",
            ),
            cell="weekday",
        ),
        dashboard_cell(
            bar_chart(
                data=S.hours,
                x_key="hour",
                value_key="commits",
                title=t(lang, "By hour of day (local time)", "Por hora del día (hora local)"),
                unit="commits",
                tooltip=tooltip_template("{datum.hour}:00 · {value} commits"),
                id="dash-hours",
            ),
            cell="hours",
        ),
        dashboard_cell(
            heatmap_chart(
                data=_rows(lang, S.heatmap, S.heatmap_es),
                label_key="day",
                values_key="hours",
                scale_max=S.heatmap_max,
                column_labels=_HOUR_LABELS,
                title=t(
                    lang,
                    "Weekday × hour — point at a day to mark it in both charts",
                    "Día × hora — señala un día para marcarlo en ambos gráficos",
                ),
                description=t(
                    lang,
                    "Rows are days, Monday to Sunday; columns are hours, 00 to 23.",
                    "Las filas son los días, de lunes a domingo; las columnas, las horas, de 00 a 23.",
                ),
                unit="commits",
                id="dash-heatmap",
            ),
            cell="heatmap",
        ),
        grid_id="dash-rhythm",
        label=t(lang, "Rhythm", "Ritmo"),
        layout=[
            dashboard_cell_layout("weekday", col_span={"md": 1, "lg": 1}),
            dashboard_cell_layout("hours", col_span={"md": 1, "lg": 3}),
            dashboard_cell_layout("heatmap", col_span={"md": 2, "lg": 4}),
        ],
        link="day",
        on_link_change=S.on_day_link,
    )


def _repo_detail(lang: str) -> rx.Component:
    return rx.cond(
        S.selected_repo != "",
        sp_card(
            sp_descriptions(_rows(lang, S.repo_facts, S.repo_facts_es), columns=3),
            rx.el.div(
                line_chart(
                    data=S.repo_monthly,
                    x_key="month",
                    value_key="commits",
                    title=t(
                        lang,
                        "Commits per month, whole history",
                        "Commits por mes, toda la historia",
                    ),
                    unit="commits",
                    height=150,
                    id="dash-repo-monthly",
                ),
                class_name="mt-3 w-full",
            ),
            title=S.selected_repo,
            extra=sp_button(
                t(lang, "Close", "Cerrar"),
                size="sm",
                on_click=S.clear_repo,
                label=t(lang, "Close repository detail", "Cerrar el detalle del repositorio"),
            ),
            size="sm",
            class_name="h-full",
        ),
        rx.el.div(
            sp_empty(
                description=t(
                    lang,
                    "Click a repository bar to open its figures and monthly series.",
                    "Haz clic en la barra de un repositorio para ver sus cifras y su serie mensual.",
                )
            ),
            class_name="h-full flex items-center justify-center",
        ),
    )


def _repositories(lang: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                sp_slider(
                    label=t(lang, "Repositories shown", "Repositorios mostrados"),
                    min=5,
                    max=25,
                    step=1,
                    marks=[5, 10, 15, 20, 25],
                    value=S.top_n,
                    on_change=S.set_top_n,
                    size="sm",
                ),
                class_name="w-full max-w-sm mb-2",
            ),
            bar_chart(
                data=S.repos_top,
                x_key="label",
                value_key="commits",
                orientation="rows",
                title=t(
                    lang,
                    "Commits per repository — click a bar for its detail",
                    "Commits por repositorio — haz clic en una barra para ver su detalle",
                ),
                unit="commits",
                tooltip=tooltip_template("{datum.repo} · {value} commits"),
                height=_VIEW_HEIGHT - 180,
                on_select=S.select_repo,
                id="dash-repos",
            ),
            class_name="min-w-0",
        ),
        # The detail scrolls inside its own column, so the page never grows.
        rx.el.div(
            _repo_detail(lang),
            class_name="min-w-0 overflow-y-auto",
            style={"max_height": f"{_VIEW_HEIGHT + 60}px"},
        ),
        class_name="grid grid-cols-1 lg:grid-cols-2 gap-3",
        style={"min_height": f"{_VIEW_HEIGHT}px"},
    )


def _technology(lang: str) -> rx.Component:
    return rx.el.div(
        _grid(
            dashboard_cell(
                squarified_treemap(
                    data=_rows(lang, S.tech_tree, S.tech_tree_es),
                    id_key="id",
                    parent_key="parent",
                    label_key="name",
                    value_key="commits",
                    root_id=S.tech_root,
                    on_root_change=S.set_tech_root,
                    title=t(
                        lang,
                        "Technologies by group — click one to open its group",
                        "Tecnologías por grupo — haz clic en una para abrir su grupo",
                    ),
                    unit="commits",
                    id="dash-tech-tree",
                ),
                cell="tree",
            ),
            dashboard_cell(
                donut_chart(
                    data=_rows(lang, S.stack_categories, S.stack_categories_es),
                    name_key="name",
                    value_key="value",
                    center_label=t(lang, "categories", "categorías"),
                    center_value=S.stack_categories.length(),
                    legend=True,
                    title=t(lang, "Commits by stack category", "Commits por categoría del stack"),
                    id="dash-stack-categories",
                ),
                cell="categories",
            ),
            dashboard_cell(
                bar_chart(
                    data=_rows(lang, S.tech_top, S.tech_top_es),
                    x_key="label",
                    value_key="commits",
                    orientation="rows",
                    title=t(
                        lang,
                        "Commits touching each technology (top 12)",
                        "Commits que tocan cada tecnología (top 12)",
                    ),
                    unit="commits",
                    tooltip=tooltip_template("{datum.tech} · {value} commits"),
                    id="dash-tech",
                ),
                cell="tech",
            ),
            dashboard_cell(
                bar_chart(
                    data=_rows(lang, S.stack_top, S.stack_top_es),
                    x_key="label",
                    value_key="commits",
                    orientation="rows",
                    title=t(
                        lang,
                        "Stack components by commits (top 12)",
                        "Componentes del stack por commits (top 12)",
                    ),
                    unit="commits",
                    tooltip=tooltip_template(
                        "{datum.component} · {datum.category} · {value} commits"
                    ),
                    id="dash-stack",
                ),
                cell="stack",
            ),
            grid_id="dash-technology",
            label=t(lang, "Technology and stack", "Tecnología y stack"),
            layout=[
                dashboard_cell_layout("tree", col_span={"md": 2, "lg": 2}),
                dashboard_cell_layout("categories", col_span={"md": 2, "lg": 2}),
                dashboard_cell_layout("tech", col_span={"md": 1, "lg": 2}),
                dashboard_cell_layout("stack", col_span={"md": 1, "lg": 2}),
            ],
        ),
        rx.cond(
            S.tech_root,
            rx.el.div(
                sp_button(
                    t(lang, "Back to all groups", "Volver a todos los grupos"),
                    size="sm",
                    on_click=S.set_tech_root(None),
                    label=t(lang, "Back to all groups", "Volver a todos los grupos"),
                ),
                class_name="absolute top-3 right-3 z-10",
            ),
            rx.fragment(),
        ),
        class_name="relative",
    )


def _bubbles(x_key: str, title: str, chart_id: str, lang: str) -> rx.Component:
    return bubble_chart(
        data=_rows(lang, S.profile_points, S.profile_points_es),
        x_key=x_key,
        y_key="momentum",
        size_key="commits",
        size_range=[120, 900],
        title=title,
        tooltip=tooltip_template(
            t(
                lang,
                "{datum.profile} · depth {datum.depth}% · momentum {datum.momentum}% · "
                "visibility {datum.visibility} · {datum.map_quadrant} / {datum.visibility_quadrant}",
                "{datum.profile} · profundidad {datum.depth}% · impulso {datum.momentum}% · "
                "visibilidad {datum.visibility} · {datum.map_quadrant} / {datum.visibility_quadrant}",
            )
        ),
        id=chart_id,
    )


def _profiles(lang: str) -> rx.Component:
    return _grid(
        dashboard_cell(
            bar_chart(
                data=_rows(lang, S.profile_mix, S.profile_mix_es),
                x_key="label",
                value_key="commits",
                orientation="rows",
                title=t(
                    lang, "Commits per profile in the period", "Commits por perfil en el periodo"
                ),
                unit="commits",
                tooltip=tooltip_template("{datum.profile} · {value} commits"),
                id="dash-profile-mix",
            ),
            cell="mix",
        ),
        dashboard_cell(
            bullet_chart(
                data=_rows(lang, S.impact_top, S.impact_top_es),
                title_key="project",
                actual_key="impact",
                target_key="median",
                title=t(
                    lang,
                    "Impact score, 0–100 (marker: the median project)",
                    "Puntaje de impacto, 0–100 (marca: el proyecto mediano)",
                ),
                tooltip=tooltip_template(
                    "{datum.project} · {value} · {datum.trajectory} · {datum.profiles_text}"
                ),
                id="dash-impact",
            ),
            cell="impact",
        ),
        dashboard_cell(
            _bubbles(
                "depth",
                t(lang, "Depth × momentum (all time)", "Profundidad × impulso (todo el historial)"),
                "dash-quad-depth",
                lang,
            ),
            cell="depth",
        ),
        dashboard_cell(
            _bubbles(
                "visibility",
                t(
                    lang,
                    "Visibility × momentum (all time)",
                    "Visibilidad × impulso (todo el historial)",
                ),
                "dash-quad-visibility",
                lang,
            ),
            cell="visibility",
        ),
        grid_id="dash-profiles",
        label=t(lang, "Profiles and impact", "Perfiles e impacto"),
        layout=[
            dashboard_cell_layout("mix", col_span={"md": 1, "lg": 2}),
            dashboard_cell_layout(
                "impact", col_span={"md": 1, "lg": 2}, row_span={"md": 1, "lg": 2}
            ),
            dashboard_cell_layout("depth", col_span={"md": 1, "lg": 1}),
            dashboard_cell_layout("visibility", col_span={"md": 1, "lg": 1}),
        ],
    )


# --------------------------------------------------------------------------- #
# Page body
# --------------------------------------------------------------------------- #

_VIEWS = {
    "activity": _activity,
    "rhythm": _rhythm,
    "repositories": _repositories,
    "technology": _technology,
    "profiles": _profiles,
}


def _panel(key: str, lang: str) -> rx.Component:
    # Only the open tab mounts its charts, so a hidden grid never measures a
    # zero width and a slice change only redraws what is on screen.
    return sp_tab_panel(
        rx.cond(
            S.tab == key,
            rx.el.div(
                _VIEWS[key](lang),
                # What did not fit the screen: more charts and tables under the grid.
                SECTIONS[key](lang) if key in SECTIONS else rx.fragment(),
                class_name="pt-2",
            ),
            rx.fragment(),
        ),
        value=key,
    )


def dev_dashboard(lang: str = "en") -> rx.Component:
    """The whole `/dev-dashboard-stats` body, in `lang`."""
    return rx.el.section(
        _header(lang),
        _kpis(lang),
        sp_tabs(
            *[_panel(key, lang) for key, _ in _TABS],
            items=[ui_item(key, label[lang]) for key, label in _TABS],
            label=t(lang, "Dashboard views", "Vistas del dashboard"),
            value=S.tab,
            on_change=S.set_tab,
            size="sm",
        ),
        id="dev-dashboard-stats",
    )
