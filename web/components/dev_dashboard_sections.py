"""Sections under each tab of `/dev-dashboard-stats`.

Every tab opens with a grid sized to fit one screen; the analysis has more than
fits there. These sections sit under the grid and scroll with the page:

- Activity: commits per day over the last 365 days of the period.
- Repositories: every repository in one sortable table.
- Technology & stack: commits touching each technology, year by year.
- Profiles & impact: the profile quadrants with names and dividers, profiles and
  opportunities, and the full impact ranking.
"""

import reflex as rx
from reflex_silverpoint_react import activity_grid, sp_card, sp_table, stacked_bar_chart

from ..dev_dashboard_data import (
    IMPACT_MEDIAN,
    OPPORTUNITY_ES,
    PROFILE_POINTS,
    PROFILES_TABLE,
    es_term,
)
from ..i18n import t
from ..states.dev_dashboard_state import DevDashboardState as S
from .quadrant_chart import Axis, quadrant_chart

_NOTE = "text-xs text-gray-600"
_TH = "text-left font-semibold text-[#1F3D36] px-3 py-2 border-b border-[#5C7B71]/40 align-bottom"
_TD = "px-3 py-2 border-b border-[#5C7B71]/15 align-top"
_NUM = "text-right tabular-nums"


def _rows(lang: str, english, spanish):
    return spanish if lang == "es" else english


def _section(title: str, note: str, *children: rx.Component, section_id: str) -> rx.Component:
    """A titled block under a tab's grid."""
    return rx.el.section(
        rx.el.h2(title, class_name="text-lg font-semibold text-gray-800"),
        rx.el.p(note, class_name=_NOTE + " mb-3 max-w-4xl"),
        *children,
        id=section_id,
        class_name="mt-6 scroll-mt-24",
    )


def _number(lang: str, value: float) -> str:
    text = f"{value:,}" if isinstance(value, int) else f"{value:,.1f}"
    return text.translate(str.maketrans(",.", ".,")) if lang == "es" else text


# --------------------------------------------------------------------------- #
# Activity
# --------------------------------------------------------------------------- #


def activity_sections(lang: str) -> rx.Component:
    return _section(
        t(lang, "Commits per day", "Commits por día"),
        t(
            lang,
            "The last 365 days of the period, one cell per day; darker cells hold more commits "
            "(four levels, by quartile of the active days).",
            "Los últimos 365 días del periodo, una celda por día; las más oscuras tienen más "
            "commits (cuatro niveles, por cuartil de los días activos).",
        ),
        sp_card(
            activity_grid(
                data=S.daily,
                date_key="date",
                count_key="commits",
                level_key="level",
                weeks=53,
                title=t(
                    lang, "Commits per day, last 365 days", "Commits por día, últimos 365 días"
                ),
                unit="commits",
                chrome="bare",
                id="dash-daily",
            ),
            size="sm",
        ),
        section_id="dash-section-daily",
    )


# --------------------------------------------------------------------------- #
# Repositories
# --------------------------------------------------------------------------- #


def _repo_columns(lang: str) -> list[dict]:
    return [
        {"key": "repo", "title": t(lang, "Repository", "Repositorio"), "sortable": True},
        {"key": "commits", "title": "Commits", "align": "end", "sortable": True},
        {
            "key": "active_days",
            "title": t(lang, "Active days", "Días activos"),
            "align": "end",
            "sortable": True,
        },
        {
            "key": "span_days",
            "title": t(lang, "Span (days)", "Duración (días)"),
            "align": "end",
            "sortable": True,
        },
        {"key": "first", "title": t(lang, "First", "Primero"), "sortable": True},
        {"key": "last", "title": t(lang, "Last", "Último"), "sortable": True},
        {"key": "language", "title": t(lang, "Language", "Lenguaje"), "sortable": True},
        {"key": "trajectory", "title": t(lang, "Trajectory", "Trayectoria"), "sortable": True},
    ]


def repositories_sections(lang: str) -> rx.Component:
    return _section(
        t(lang, "Every repository", "Todos los repositorios"),
        t(
            lang,
            "All time, whatever the filters. Sort by any column; span is the days from the first "
            "to the last commit.",
            "Todo el historial, sin importar los filtros. Ordena por cualquier columna; la duración "
            "son los días entre el primer y el último commit.",
        ),
        rx.el.div(
            sp_table(
                _repo_columns(lang),
                _rows(lang, S.repo_table, S.repo_table_es),
                caption=t(lang, "Every repository", "Todos los repositorios"),
                sort_key=S.repo_sort_key,
                sort_order=S.repo_sort_order,
                on_sort=S.sort_repos,
                striped=True,
                hoverable=True,
                row_key="repo",
                id="dash-repo-table",
            ),
            class_name="max-h-[520px] overflow-y-auto",
        ),
        section_id="dash-section-repos",
    )


# --------------------------------------------------------------------------- #
# Technology & stack
# --------------------------------------------------------------------------- #


def technology_sections(lang: str) -> rx.Component:
    return _section(
        t(lang, "Technology by year", "Tecnología por año"),
        t(
            lang,
            "Commits touching each of the period's six main technologies, per year. A commit "
            "counts once for every technology it touched.",
            "Commits que tocan cada una de las seis tecnologías principales del periodo, por año. "
            "Un commit cuenta una vez por cada tecnología que tocó.",
        ),
        sp_card(
            stacked_bar_chart(
                data=S.tech_by_year,
                x_key="year",
                keys=S.tech_year_keys,
                names=_rows(lang, S.tech_year_keys, S.tech_year_names_es),
                title=t(lang, "Commits per technology and year", "Commits por tecnología y año"),
                unit="commits",
                height=300,
                chrome="bare",
                id="dash-tech-by-year",
            ),
            size="sm",
        ),
        section_id="dash-section-tech-year",
    )


# --------------------------------------------------------------------------- #
# Profiles & impact
# --------------------------------------------------------------------------- #


def _quadrants(lang: str) -> rx.Component:
    points = [
        {**point, "name": point["profile"] if lang == "en" else es_term(point["profile"])}
        for point in PROFILE_POINTS
    ]
    momentum = Axis(
        "momentum", 40, 100, [40, 50, 60, 70, 80, 90, 100], 65, t(lang, "Momentum", "Impulso"), True
    )
    q = (lambda name: name) if lang == "en" else es_term
    return rx.el.div(
        sp_card(
            quadrant_chart(
                points,
                label_key="name",
                size_key="commits",
                x=Axis(
                    "depth",
                    0,
                    50,
                    [0, 10, 20, 30, 40, 50],
                    25,
                    t(lang, "Depth: % of all commits", "Profundidad: % de todos los commits"),
                ),
                y=momentum,
                quadrants=(
                    q("Emerging"),
                    q("Core & accelerating"),
                    q("Supporting"),
                    q("Established core"),
                ),
                title=t(
                    lang, "Profile map: depth × momentum", "Mapa de perfiles: profundidad × impulso"
                ),
                description=t(
                    lang,
                    "Depth is the share of all hand-written commits that belong to the profile; "
                    "momentum is the share of the profile's commits made in the last 12 months. "
                    "Bubble size is commits. A commit can belong to several profiles.",
                    "La profundidad es la parte de todos los commits escritos a mano que pertenece "
                    "al perfil; el impulso, la parte de los commits del perfil hecha en los últimos "
                    "12 meses. El tamaño de la burbuja son los commits. Un commit puede pertenecer "
                    "a varios perfiles.",
                ),
                chart_id="dash-quadrant-depth",
            ),
            size="sm",
        ),
        sp_card(
            quadrant_chart(
                points,
                label_key="name",
                size_key="commits",
                x=Axis(
                    "visibility",
                    0,
                    105,
                    [0, 20, 40, 60, 80, 100],
                    50,
                    t(lang, "Visibility index", "Índice de visibilidad"),
                ),
                y=momentum,
                quadrants=(
                    q("Hidden strength"),
                    q("Showcase & growing"),
                    q("Latent"),
                    q("Showcase"),
                ),
                title=t(lang, "Visibility × momentum", "Visibilidad × impulso"),
                description=t(
                    lang,
                    "Visibility is public evidence in the profile's primary repositories (repos + "
                    "3 × PyPI packages + 2 × tagged repos + stars + forks), scaled to the most "
                    "visible profile. Top-left is where work is growing faster than anyone can see it.",
                    "La visibilidad es la evidencia pública en los repositorios principales del "
                    "perfil (repos + 3 × paquetes en PyPI + 2 × repos con versiones + estrellas + "
                    "forks), escalada al perfil más visible. Arriba a la izquierda está el trabajo "
                    "que crece más rápido de lo que se ve.",
                ),
                chart_id="dash-quadrant-visibility",
            ),
            size="sm",
        ),
        class_name="grid grid-cols-1 xl:grid-cols-2 gap-3",
    )


def _profiles_table(lang: str) -> rx.Component:
    headers = [
        (t(lang, "Profile", "Perfil"), ""),
        ("Commits", _NUM),
        (t(lang, "Depth %", "Profundidad %"), _NUM),
        (t(lang, "Momentum %", "Impulso %"), _NUM),
        (t(lang, "Visibility", "Visibilidad"), _NUM),
        (t(lang, "Map", "Mapa"), ""),
        (t(lang, "Visibility quadrant", "Cuadrante de visibilidad"), ""),
        (t(lang, "Main repositories", "Repositorios principales"), ""),
        (t(lang, "Opportunity", "Oportunidad"), ""),
    ]
    q = (lambda name: name) if lang == "en" else es_term

    def row(profile: dict) -> rx.Component:
        cells = [
            (q(profile["profile"]), "font-medium text-gray-800 whitespace-nowrap"),
            (_number(lang, profile["commits"]), _NUM),
            (_number(lang, profile["depth"]), _NUM),
            (_number(lang, profile["momentum"]), _NUM),
            (str(profile["visibility"]), _NUM),
            (q(profile["map_quadrant"]), ""),
            (q(profile["visibility_quadrant"]), ""),
            (profile["top_repos"], "text-xs"),
            (
                OPPORTUNITY_ES.get(profile["profile"], profile["opportunity"])
                if lang == "es"
                else profile["opportunity"],
                "min-w-[18rem]",
            ),
        ]
        return rx.el.tr(*[rx.el.td(text, class_name=f"{_TD} {extra}") for text, extra in cells])

    return rx.el.div(
        rx.el.table(
            rx.el.caption(
                t(lang, "Profiles and opportunities", "Perfiles y oportunidades"),
                class_name="sr-only",
            ),
            rx.el.thead(
                rx.el.tr(
                    *[
                        rx.el.th(text, scope="col", class_name=f"{_TH} {extra}")
                        for text, extra in headers
                    ]
                )
            ),
            rx.el.tbody(*[row(profile) for profile in PROFILES_TABLE]),
            class_name="w-full text-sm text-gray-700 border-collapse",
        ),
        class_name="overflow-x-auto",
    )


_TRAJECTORY_TONE = {
    "Accelerating": "border-[#2C6355] text-[#2C6355]",
    "En aceleración": "border-[#2C6355] text-[#2C6355]",
    "Active": "border-[#1F3D36] text-[#1F3D36]",
    "Activo": "border-[#1F3D36] text-[#1F3D36]",
    "Maintained": "border-[#9A7414] text-[#8A6612]",
    "Mantenido": "border-[#9A7414] text-[#8A6612]",
}
_TRAJECTORY_DEFAULT = "border-gray-400 text-gray-500"
_PILL = "inline-block px-2 py-0.5 rounded-full border text-xs whitespace-nowrap"


def _impact_row(row: dict) -> rx.Component:
    trajectory = row["trajectory"].to(str)
    tone = rx.match(
        trajectory,
        *[(value, f"{_PILL} {classes}") for value, classes in _TRAJECTORY_TONE.items()],
        f"{_PILL} {_TRAJECTORY_DEFAULT}",
    )
    return rx.el.tr(
        rx.el.td(row["project"], class_name=f"{_TD} font-medium text-gray-800"),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-2 rounded-full bg-[#2F6F86]",
                        style={"width": row["impact"].to(str) + "%"},
                    ),
                    class_name="w-28 h-2 rounded-full bg-[#2F6F86]/15 overflow-hidden",
                ),
                rx.el.span(row["impact"], class_name="font-semibold tabular-nums"),
                class_name="flex items-center gap-2",
            ),
            class_name=_TD,
        ),
        rx.el.td(
            rx.el.span(
                row["trajectory"],
                class_name=tone,
            ),
            class_name=_TD,
        ),
        *[
            rx.el.td(row[key], class_name=f"{_TD} {_NUM}")
            for key in (
                "commits",
                "repos",
                "active_days",
                "last90",
                "pypi",
                "tags",
                "merges",
                "tests",
                "stars",
            )
        ],
        rx.el.td(row["profiles_text"], class_name=f"{_TD} text-xs"),
    )


def _impact_table(lang: str) -> rx.Component:
    headers = [
        (t(lang, "Project", "Proyecto"), ""),
        (t(lang, "Impact", "Impacto"), ""),
        (t(lang, "Trajectory", "Trayectoria"), ""),
        ("Commits", _NUM),
        ("Repos", _NUM),
        (t(lang, "Active days", "Días activos"), _NUM),
        (t(lang, "Last 90 d", "Últimos 90 d"), _NUM),
        ("PyPI", _NUM),
        (t(lang, "Tags", "Versiones"), _NUM),
        ("Merges", _NUM),
        (t(lang, "Test commits", "Commits de pruebas"), _NUM),
        (t(lang, "Stars", "Estrellas"), _NUM),
        (t(lang, "Profiles", "Perfiles"), ""),
    ]
    return rx.el.div(
        rx.el.table(
            rx.el.caption(
                t(lang, "Projects ranked by impact", "Proyectos por impacto"), class_name="sr-only"
            ),
            rx.el.thead(
                rx.el.tr(
                    *[
                        rx.el.th(text, scope="col", class_name=f"{_TH} {extra}")
                        for text, extra in headers
                    ]
                )
            ),
            rx.el.tbody(rx.foreach(_rows(lang, S.impact_rows, S.impact_rows_es), _impact_row)),
            class_name="w-full text-sm text-gray-700 border-collapse",
        ),
        class_name="overflow-x-auto max-h-[560px] overflow-y-auto",
    )


def profiles_sections(lang: str) -> rx.Component:
    return rx.fragment(
        _section(
            t(lang, "Engineering profile quadrants", "Cuadrantes de perfil de ingeniería"),
            t(
                lang,
                "All time, the same in every filter. The dashed lines are the cuts: depth 25 %, "
                "visibility 50, momentum 65 %.",
                "Todo el historial, igual con cualquier filtro. Las líneas punteadas son los cortes: "
                "profundidad 25 %, visibilidad 50, impulso 65 %.",
            ),
            _quadrants(lang),
            section_id="dash-section-quadrants",
        ),
        _section(
            t(lang, "Profiles and opportunities", "Perfiles y oportunidades"),
            t(
                lang,
                "Opportunities are read from the commit history, not from job-market data.",
                "Las oportunidades salen del historial de commits, no de datos del mercado laboral.",
            ),
            sp_card(_profiles_table(lang), size="sm"),
            section_id="dash-section-opportunities",
        ),
        _section(
            t(lang, "Projects ranked by impact", "Proyectos por impacto"),
            t(
                lang,
                f"Impact (0–100) = 30 % commit volume + 20 % active days + 20 % delivery (PyPI, "
                f"tags, merge flow, tests) + 10 % stars and forks + 20 % commits in the last 90 "
                f"days, each log-scaled to the leader. The median project scores {IMPACT_MEDIAN}. "
                "The profile filter narrows the list.",
                f"Impacto (0–100) = 30 % volumen de commits + 20 % días activos + 20 % entrega "
                f"(PyPI, versiones, flujo de merges, pruebas) + 10 % estrellas y forks + 20 % commits "
                f"de los últimos 90 días, cada uno en escala logarítmica respecto del líder. El "
                f"proyecto mediano tiene {IMPACT_MEDIAN}. El filtro de perfil acota la lista.",
            ),
            sp_card(_impact_table(lang), size="sm"),
            section_id="dash-section-impact",
        ),
    )


SECTIONS = {
    "activity": activity_sections,
    "repositories": repositories_sections,
    "technology": technology_sections,
    "profiles": profiles_sections,
}
