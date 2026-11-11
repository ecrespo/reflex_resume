Title: Silverpoint, artículo 26: proyecto final en Reflex, una aplicación completa en Python con datos reales
Date: 2026-11-11 22:45
Category: Tutorial Silverpoint
Tags: silverpoint, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_26
Authors: Ernesto Crespo
Summary: La aplicación Operations del proyecto final, escrita entera en Python con Reflex y silverpoint: tres páginas, un tema para toda la sesión, visitas en vivo y tiempos de respuesta reales que el backend mide cada 15 segundos.

Los artículos 23, 24 y 25 construyen la misma aplicación, Operations, en React, Vue y Angular. Este la construye en Reflex, sin escribir JavaScript: las páginas, el estado y los eventos son Python, y Reflex compila el frontend en React.

Reflex tiene algo que los otros tres no tienen de serie: un backend propio. Por eso esta versión añade datos reales. Mientras la aplicación corre, el backend mide el tiempo de respuesta de tres direcciones públicas y el panel lo dibuja.

## Lo que vas a construir

| Ruta | Página | Qué tiene |
|---|---|---|
| `/` | Overview | El panel del [artículo 13](/blog/silverpoint_serie_13) con las visitas en vivo, la lectura de la hora activa, la descarga del SVG y los tiempos de respuesta medidos |
| `/incidents` | Incidents | La tabla de incidencias con orden, páginas, la ventana para reconocer una incidencia y el aviso del [artículo 17](/blog/silverpoint_serie_17) |
| `/settings` | Settings | El formulario de la regla de alerta del [artículo 16](/blog/silverpoint_serie_16) y el tema: paleta y estilo base |

Una barra de navegación arriba enlaza las tres. El tema que eliges en Settings colorea toda la aplicación y se conserva mientras dura la sesión.

![La página Overview de Operations en Reflex: el panel con las visitas en vivo, la lectura de las 14:00 y los tiempos de respuesta medidos](./images/silverpoint-serie-26.png)

## Qué es real y qué es de ejemplo

| Dato | Origen |
|---|---|
| Tiempos de respuesta de `www.seraph.to`, `api.seraph.to/ping` y `silverpointweb.vercel.app` | **Reales.** El backend hace una petición a cada dirección cada 15 segundos y mide cuánto tarda |
| Visitas y errores por hora | De ejemplo: las filas de la serie, que avanzan cada 2 segundos como en el [artículo 20](/blog/silverpoint_serie_20) |
| Visitas y errores de hoy, errores por día, ventas por canal | De ejemplo: las filas de la serie |
| Las 12 incidencias | De ejemplo: las del artículo 17 |

Los tiempos se miden desde la máquina donde corre el backend. En mis pruebas salieron entre 100 y 350 ms.

## Lo que necesitas

Python 3.13 y `uv`. Las versiones con las que lo probé:

| Paquete | Versión |
|---|---|
| `reflex` | 0.10.1 |
| `reflex-silverpoint-react` | 0.9.1 |
| `httpx` | 0.28.1 |

Crea el proyecto como en el [artículo 06](/blog/silverpoint_serie_6):

```bash
uv init operations
cd operations
uv add reflex reflex-silverpoint-react httpx
uv run reflex init
```

`reflex init` crea `rxconfig.py` y el módulo `operations/` con una página de bienvenida, que este artículo sustituye. Borra también el `main.py` que crea `uv init`. Las dependencias quedan así en `pyproject.toml`:

```toml
dependencies = [
    "httpx>=0.28.1",
    "reflex>=0.10.1",
    "reflex-silverpoint-react>=0.9.1",
]
```

## La estructura

```text
operations/
├── assets/
│   └── operations.css
├── data/
│   └── silverpoint-grounds.css
├── operations/
│   ├── __init__.py
│   ├── data.py
│   ├── incidents.py
│   ├── layout.py
│   ├── live.py
│   ├── operations.py
│   ├── overview.py
│   ├── probes.py
│   ├── settings.py
│   └── theme.py
├── pyproject.toml
└── rxconfig.py
```

| Archivo | Qué hace |
|---|---|
| `data.py` | Las filas de ejemplo de la serie y las 12 incidencias, copiadas de los artículos 13 y 17 |
| `probes.py` | Los datos reales: mide las tres direcciones y guarda las lecturas |
| `live.py` | La ventana de 24 horas que avanza, del artículo 20 |
| `theme.py` | El tema de la sesión |
| `layout.py` | La navegación y el proveedor que envuelve cada página |
| `overview.py`, `incidents.py`, `settings.py` | Las tres páginas |
| `operations.py` | La aplicación: hoja de estilos, tarea de fondo y rutas |

`rxconfig.py` solo conserva el plugin del mapa del sitio. Quité los de Tailwind y Radix Themes, que la aplicación no usa:

```python
import reflex as rx

config = rx.Config(
    app_name="operations",
    plugins=[rx.plugins.SitemapPlugin()],
)
```

## 1. Los datos reales

`operations/probes.py` hace una petición GET a cada dirección, mide el tiempo hasta recibir la respuesta completa y guarda las últimas 40 lecturas de cada una:

```python
"""The real data: the response time of three public endpoints."""

import asyncio
import time
from collections import deque

import httpx

TARGETS = {
    "www.seraph.to": "https://www.seraph.to",
    "api.seraph.to/ping": "https://api.seraph.to/ping",
    "silverpointweb.vercel.app": "https://silverpointweb.vercel.app",
}
INTERVAL = 15  # seconds between rounds: one request per endpoint and round
KEEP = 40  # readings kept per endpoint: the last ten minutes

READINGS: dict[str, deque[dict]] = {name: deque(maxlen=KEEP) for name in TARGETS}


async def measure(client: httpx.AsyncClient, url: str) -> dict:
    """One GET, timed from the request to the last byte of the body."""
    start = time.perf_counter()
    try:
        response = await client.get(url)
    except httpx.HTTPError as error:
        return {"ms": None, "status": type(error).__name__}
    ms = round((time.perf_counter() - start) * 1000)
    return {"ms": ms, "status": response.status_code}


async def probe_forever():
    """Measure every endpoint, wait, repeat; Reflex cancels it on shutdown."""
    headers = {"User-Agent": "operations-demo/0.1"}
    async with httpx.AsyncClient(timeout=10, headers=headers) as client:
        while True:
            for name, url in TARGETS.items():
                READINGS[name].append(await measure(client, url))
            await asyncio.sleep(INTERVAL)


def latency_rows() -> list[dict]:
    """One row per endpoint for sparkline_rows: the points and the last reading."""
    rows = []
    for name, readings in READINGS.items():
        if not readings:
            continue
        last = readings[-1]
        ok = last["status"] == 200
        rows.append(
            {
                "name": name,
                "points": [r["ms"] for r in readings if r["ms"] is not None],
                "readout": f"{last['ms']} ms" if ok else str(last["status"]),
            }
        )
    return rows
```

`probe_forever` no es un evento de ningún estado. Es una tarea de vida de la aplicación: `operations.py` la registra con `app.register_lifespan_task`, Reflex la arranca con el backend y la cancela al pararlo. Corre una sola vez por proceso, abran la página uno o cien usuarios. Así el ritmo es siempre el mismo: tres peticiones cada 15 segundos.

Tres detalles de la medida:

* **La conexión se reutiliza.** `httpx.AsyncClient` mantiene abiertas las conexiones entre rondas. La primera lectura incluye el saludo TLS y las demás no. Con `curl`, que abre una conexión nueva, `www.seraph.to` tarda unos 470 ms; con la conexión abierta, unos 150 ms.
* **Un fallo también es una lectura.** Si la petición falla, se guarda el nombre del error, como `ConnectTimeout`, y la fila lo muestra en lugar de los milisegundos.
* **Las lecturas viven en memoria.** Un `deque` con `maxlen=40` guarda los últimos diez minutos y descarta lo anterior. Al reiniciar el backend se pierden. Para conservarlas, Reflex ofrece `rx.Model` con SQLite, que necesita el extra `reflex[db]`; aquí no lo usé.

Sin Redis, Reflex arranca el backend con un solo proceso, y por eso hay un solo bucle. Con Redis y varios procesos, cada proceso tendría su `READINGS` y su bucle, y las peticiones se multiplicarían. En ese caso, saca la medida a un proceso aparte que escriba en una base de datos.

## 2. El tema de la sesión

El [artículo 12](/blog/silverpoint_serie_12) cambiaba el tema de una página. Aquí lo cambia toda la aplicación. `operations/theme.py` guarda dos decisiones, la paleta y si el estilo base es la cianotipia, y deriva de ellas lo que necesitan los componentes:

```python
import reflex as rx
from reflex_silverpoint_react import PALETTES

PALETTE_ITEMS = [
    {"key": key, "label": key.replace("_", " ").capitalize()} for key in PALETTES
]
CYANOTYPE_PAGE = {"background": "#1B3F6B", "color": "#F4F6F8"}


class ThemeState(rx.State):
    palette_name: str = "silverpoint"
    cyanotype: bool = False

    @rx.event
    def set_palette_name(self, value: str):
        self.palette_name = value

    @rx.event
    def set_cyanotype(self, value: bool):
        self.cyanotype = value

    @rx.var
    def ground(self) -> str:
        return "cyanotype" if self.cyanotype else "silverpoint"

    @rx.var
    def palette(self) -> dict[str, str]:
        return {} if self.cyanotype else PALETTES[self.palette_name].to_dict()

    @rx.var
    def page(self) -> dict[str, str]:
        if self.cyanotype:
            return CYANOTYPE_PAGE
        colors = PALETTES[self.palette_name].to_dict()
        return {"background": colors["substrate"], "color": colors["text"]}
```

| Variable | Para qué |
|---|---|
| `ground` | El estilo base del proveedor y del panel |
| `palette` | Los colores de la paleta; vacío en cianotipia, que trae los suyos |
| `page` | El fondo y el color del texto de la página |

`page` existe porque el proveedor no pinta la página: solo da estilo a los componentes de silverpoint, como avisaba el artículo 12. Con la cianotipia, el fondo de la página es el azul de Prusia del estilo base, `#1B3F6B`.

`operations/layout.py` envuelve cada página con la navegación y el proveedor del [artículo 09](/blog/silverpoint_serie_9), con el tema de la sesión:

```python
import reflex as rx
from reflex_silverpoint_react import silverpoint_provider

from .theme import ThemeState

LINKS = [("/", "Overview"), ("/incidents", "Incidents"), ("/settings", "Settings")]


def nav(route: str) -> rx.Component:
    return rx.el.nav(
        rx.el.strong("Operations"),
        *[
            rx.el.a(text, href=href, aria_current="page" if href == route else None)
            for href, text in LINKS
        ],
        class_name="top-nav",
    )


def shell(route: str, *children: rx.Component) -> rx.Component:
    """Every page: the provider with the session's theme, the nav and the content."""
    return silverpoint_provider(
        rx.el.div(
            nav(route),
            rx.el.main(*children),
            class_name="shell",
            style=ThemeState.page,
        ),
        ground=ThemeState.ground,
        palette=ThemeState.palette,
    )
```

El artículo 09 envolvía la aplicación entera con `app.extra_app_wraps`. Aquí no sirve: ese envoltorio se construye una vez, sin acceso al estado de la sesión. `shell` lo resuelve en cada página.

El estado de Reflex vive en el backend, una copia por pestaña. Los enlaces de la barra cambian de página sin recargarla, así que el tema y el formulario de Settings siguen ahí al volver. Al cerrar la pestaña se pierden: es el alcance de una sesión.

## 3. La página Overview

`operations/live.py` es la ventana del artículo 20, con una diferencia: cada lectura nueva trae también los errores de esa hora, para que el gráfico de barras avance a la vez que la línea:

```python
from .data import HOURLY


def next_reading(last: dict, tick: int) -> dict:
    """The hour after the last one, from the day's profile with a small variation."""
    hour = (int(last["hour"]) + 1) % 24
    return {
        "hour": f"{hour:02d}",
        "hits": HOURLY[hour]["hits"] + (tick * 7) % 9 - 4,
        "errors": HOURLY[hour]["errors"],
    }


def advance(rows: list[dict], tick: int) -> list[dict]:
    """A rolling window: drop the oldest hour and append the new one."""
    return [*rows[1:], next_reading(rows[-1], tick)]
```

`operations/overview.py` empieza con sus importaciones:

```python
import asyncio
from pathlib import Path

import reflex as rx
from reflex_silverpoint_react import (
    bar_chart,
    dashboard,
    dashboard_cell,
    dashboard_cell_layout,
    dashboard_layout,
    donut_chart,
    get_svg,
    heatmap_chart,
    kpi_card,
    line_chart,
    sparkline_rows,
    tooltip_template,
)

from .data import BLOCKS, ERRORS_BY_DAY, HOURLY, SALES
from .layout import shell
from .live import advance
from .probes import latency_rows
from .theme import ThemeState

GROUND_CSS = Path("data/silverpoint-grounds.css")
```

El estado de lo que se mueve. `rows` son las visitas de ejemplo y `latency`, las filas de los tiempos reales:

```python
class LiveState(rx.State):
    rows: list[dict[str, str | int]] = HOURLY
    latency: list[dict] = []

    @rx.var
    def last(self) -> dict[str, str | int]:
        return self.rows[-1]

    @rx.event(background=True)
    async def stream(self):
        async with self:
            self.latency = latency_rows()
        tick = 0
        while True:
            await asyncio.sleep(2)
            tick += 1
            async with self:
                self.rows = advance(self.rows, tick)
                if (latency := latency_rows()) != self.latency:
                    self.latency = latency
```

`stream` es la tarea de fondo del artículo 20. Cada 2 segundos avanza la ventana y copia las lecturas de `probes.py`; solo las asigna si cambiaron, para no enviar al navegador lo mismo cada vez. La tarea no hace peticiones: lee la memoria del proceso, que llena la tarea de vida.

La arranca `on_load` de la página Overview. Lo comprobé en el navegador: al ir a Incidents con la barra, Reflex cancela la tarea y no llega ningún mensaje por el websocket durante 6 segundos; al volver, arranca una nueva y la ventana avanza una hora cada 2 segundos, no dos.

La lectura de la hora activa es la del [artículo 11](/blog/silverpoint_serie_11) y la descarga, la del [artículo 18](/blog/silverpoint_serie_18), con la hoja del estilo base dentro de `CDATA` porque el SVG exportado no la incluye ([silverpoint#14](https://github.com/ecrespo/silverpoint/issues/14), se corregirá en una próxima versión del paquete):

```python
class ReadoutState(rx.State):
    active: str = ""

    @rx.event
    def show(self, item: dict | None):
        if item is None:
            self.active = ""
        else:
            self.active = f"{item['datum']['hour']}:00, {item['value']} thousand hits"


class ExportState(rx.State):
    @rx.event
    def save_svg(self, svg: str | None):
        if not svg:
            return
        css = GROUND_CSS.read_text()
        start = svg.index(">") + 1
        standalone = f"{svg[:start]}<style><![CDATA[{css}]]></style>{svg[start:]}"
        return rx.download(data=standalone, filename="hits-per-hour.svg")
```

`data/silverpoint-grounds.css` es una copia de `.web/node_modules/@silverpoint/grounds/dist/styles.css`, que aparece tras el primer `reflex run`. Va en `data/` y no en `.web/` porque la lee el backend, y un backend desplegado solo no tiene `.web/`.

El panel es el del artículo 13 con tres cambios: la línea y las barras leen `LiveState.rows`, la línea lleva la descripción emergente y `on_active_change`, y el panel recibe el tema:

```python
def panel() -> rx.Component:
    return dashboard(
        dashboard_cell(
            kpi_card(
                title="Hits today",
                data=HOURLY,
                value_key="hits",
                value=886,
                unit="thousand hits",
                delta=4.2,
            ),
            cell="hits-today",
        ),
        dashboard_cell(
            kpi_card(
                title="Errors today",
                data=HOURLY,
                value_key="errors",
                value=103,
                unit="errors",
                delta=-12,
            ),
            cell="errors-today",
        ),
        dashboard_cell(
            line_chart(
                id="hits",
                title="Hits per hour",
                badge="Live",
                data=LiveState.rows,
                x_key="hour",
                value_key="hits",
                footer_left="Thousands",
                footer_right=f"Updated at {LiveState.last['hour']}:00",
                tooltip=tooltip_template("{datum.hour}:00 · {value}k hits"),
                on_active_change=ReadoutState.show,
            ),
            cell="traffic",
        ),
        dashboard_cell(
            bar_chart(
                title="Errors per hour",
                data=LiveState.rows,
                x_key="hour",
                value_key="errors",
            ),
            cell="errors-hour",
        ),
        dashboard_cell(
            heatmap_chart(
                title="Errors by day",
                data=ERRORS_BY_DAY,
                label_key="day",
                values_key="values",
                column_labels=BLOCKS,
                scale_max=40,
            ),
            cell="errors-day",
        ),
        dashboard_cell(
            donut_chart(
                title="Sales by channel",
                data=SALES,
                name_key="channel",
                value_key="sales",
                center_label="thousand EUR",
            ),
            cell="channels",
        ),
        id="ops",
        title="Operations",
        description="Traffic, errors and sales of the web service today.",
        layout=LAYOUT,
        link="hour",
        ground=ThemeState.ground,
        palette=ThemeState.palette,
    )
```

El tercer cambio tiene una razón. El panel no lee el proveedor: su papel, el título y el fondo usan solo sus propias props, porque también se dibuja en componentes de servidor, que no tienen proveedor. Sus gráficos sí siguen al proveedor. Sin `ground` y `palette` en `dashboard`, al elegir la cianotipia los seis gráficos se vuelven azules sobre un marco color crema. Con ellas, el marco cambia con todo lo demás. Es un [error conocido](https://github.com/ecrespo/silverpoint/issues/17) que se corregirá en una próxima versión del paquete.

`link="hour"` une los gráficos por la hora: al señalar las 14:00 en la línea, las barras y las dos tarjetas marcan su punto de las 14:00. La línea avanza mientras tanto; las barras también, porque leen las mismas filas.

El resto de la página. Los tiempos reales se dibujan con `sparkline_rows`, una fila por dirección con su curva y la última lectura:

```python
def response_times() -> rx.Component:
    return rx.cond(
        LiveState.latency,
        sparkline_rows(
            title="Response time",
            badge="Measured",
            data=LiveState.latency,
            footer_left="Milliseconds, one request every 15 s",
        ),
        rx.el.p("Waiting for the first measurements…"),
    )


def overview() -> rx.Component:
    return shell(
        "/",
        panel(),
        rx.el.div(
            rx.el.p(
                rx.cond(
                    ReadoutState.active,
                    ReadoutState.active,
                    "Point at an hour, or focus the chart and use the arrow keys.",
                ),
                role="status",
            ),
            rx.el.button(
                "Download SVG",
                type="button",
                on_click=get_svg("hits", ExportState.save_svg),
            ),
            class_name="toolbar",
        ),
        response_times(),
    )
```

`rx.cond` está ahí porque `sparkline_rows` con una lista vacía dibuja su estado vacío, «No data». Hasta que llega la primera ronda de medidas, la página dice que espera.

## 4. La página Incidents

`operations/incidents.py` es el código del artículo 17 sin cambios: las columnas, `IncidentsState`, la tabla, la paginación, la ventana y el aviso. Solo cambia el final, que mete la sección en `shell`:

```python
def incidents() -> rx.Component:
    return shell("/incidents", incidents_table())
```

Siguen valiendo los dos avisos de aquel artículo. El disparador de la ventana es un `rx.el.button`, porque con la ventana controlada desde el estado el texto en `trigger` rompe la página ([reflex-silverpoint-react#44](https://github.com/ecrespo/reflex-silverpoint-react/issues/44)). Y las celdas de la tabla necesitan la regla de `operations.css` que las alinea al inicio ([silverpoint#12](https://github.com/ecrespo/silverpoint/issues/12)). Los dos errores se corregirán en una próxima versión del paquete.

## 5. La página Settings

`operations/settings.py` empieza con el formulario del artículo 16, `RuleState` y `alert_rule_form`, sin cambios. Después añade la tarjeta del tema y la página:

```python
def theme_settings() -> rx.Component:
    return sp_card(
        sp_select(
            PALETTE_ITEMS,
            label="Palette",
            value=ThemeState.palette_name,
            on_change=ThemeState.set_palette_name,
            disabled=ThemeState.cyanotype,
        ),
        sp_switch(
            label="Cyanotype ground",
            checked=ThemeState.cyanotype,
            on_change=ThemeState.set_cyanotype,
        ),
        line_chart(
            title="Preview",
            data=HOURLY,
            x_key="hour",
            value_key="hits",
            height=120,
        ),
        title="Theme",
    )


def settings() -> rx.Component:
    return shell(
        "/settings",
        rx.el.div(alert_rule_form(), theme_settings(), class_name="columns"),
    )
```

La paleta se elige con `sp_select` entre las seis de `PALETTES`, y el estilo base con `sp_switch`. Con la cianotipia activa, el selector se desactiva: ese estilo base trae sus propios colores. La vista previa es un gráfico de línea pequeño que cambia con el tema.

## 6. La aplicación

`operations/operations.py` lo une todo:

```python
import reflex as rx

from .incidents import incidents
from .overview import LiveState, overview
from .probes import probe_forever
from .settings import settings

app = rx.App(stylesheets=["/operations.css"])
app.register_lifespan_task(probe_forever)
app.add_page(overview, route="/", title="Operations", on_load=LiveState.stream)
app.add_page(incidents, route="/incidents", title="Incidents · Operations")
app.add_page(settings, route="/settings", title="Settings · Operations")
```

Las reglas de estilo van en `assets/operations.css`. Las de la barra y las columnas son de maquetación; estas dos vienen de artículos anteriores:

```css
/* silverpoint#12: SpTable cells without an align follow the start edge */
.sp-table {
  justify-self: stretch;
}

.sp-ui-table td:not([data-align]) {
  text-align: start;
}

/* Plain buttons: the SVG download and the modal's trigger (reflex-silverpoint-react#44) */
.toolbar button,
button[aria-haspopup="dialog"] {
  padding: 6px 14px;
  border: 1px solid currentColor;
  border-radius: 2px;
  background: transparent;
  color: inherit;
  font: inherit;
  cursor: pointer;
}
```

Las puse en un archivo por una razón práctica. En el artículo 17 iban en `rx.App(style=...)`. Sin el plugin `RadixThemesPlugin`, en Reflex 0.10.1 esas reglas no llegan a la página: la tabla salía alineada a la derecha. Con `stylesheets` la hoja llega siempre.

## Ejecutar, compilar y desplegar

En desarrollo:

```bash
uv run reflex run
```

El frontend queda en `http://localhost:3000` y el backend, con la tarea de medida, en el puerto 8000. Para probar el modo de producción en tu equipo:

```bash
uv run reflex run --env prod
```

En producción, frontend y backend comparten un puerto. Si les das dos distintos, Reflex se niega a arrancar con «In prod mode, frontend and backend must run on the same port».

Para desplegar hay dos caminos:

| Camino | Cómo |
|---|---|
| Separado | `uv run reflex export --frontend-only` genera el frontend estático, que sirve cualquier alojamiento de archivos. El backend corre en un servidor con `uv run reflex run --env prod --backend-only`, y `api_url` en `rxconfig.py` le dice al frontend dónde está |
| Reflex Cloud | `uv run reflex deploy` sube la aplicación al alojamiento de Reflex |

Este blog usa el primer camino: el frontend estático está en Vercel y el backend, en un contenedor. No desplegué Operations; probé el modo de producción y la exportación en local. Con el camino separado, los tiempos de respuesta se miden desde el servidor del backend, no desde el navegador de quien mira.

## Las comprobaciones

Todo el código de este artículo es el del proyecto probado. Con Chrome sin interfaz, desde Playwright, en desarrollo y otra vez con `--env prod`:

| Qué | Resultado |
|---|---|
| Los siete gráficos de Overview | `data-status="ready"` |
| En vivo | El pie de la línea pasa de «Updated at 23:00» a «Updated at 01:00» en 4 segundos |
| Hora activa | Al pasar el puntero, la lectura dice «14:00, 59 thousand hits» y la descripción emergente, «14:00 · 59k hits» |
| Enlace por hora | Las barras dibujan su marca de enlace (`part="linked"`) |
| Tiempos reales | Tres filas con su lectura, como «154 ms» |
| Descarga | `hits-per-hour.svg`, unos 15,8 KB, con `<![CDATA[` y las reglas del estilo base |
| Navegación | Ningún mensaje del websocket en 6 segundos en Incidents; al volver, una hora cada 2 segundos |
| Incidents | Orden por minutos en los dos sentidos, página 2, reconocer INC-1042 cierra la ventana y abre el aviso, la fila pasa a `acknowledged`, celdas alineadas al inicio |
| Formulario | «hits ≥ 15, by chat, paused. Notes: Page the API team» |
| Tema | Con Sanguine el fondo pasa a `#F2E8DC`; con la cianotipia, a `#1B3F6B`, y el panel de Overview y los componentes de Incidents la siguen |
| Sesión | Al volver a Settings, el formulario y el interruptor conservan su valor |
| Consola | Sin errores |

Además, `ruff format` y `ruff check` sobre el proyecto. Con las reglas por defecto de ruff 0.17, `ruff check` solo marca RUF012 en `latency: list[dict] = []`. En un estado de Reflex es la forma normal de declarar una variable: Reflex copia el valor inicial para cada sesión.

## Las cifras

Medidas en mi equipo, para compararlas en el artículo 27:

| Medida | Valor |
|---|---|
| Código escrito | 9 módulos de Python, una hoja CSS y `rxconfig.py`: 670 líneas no vacías; unas 270 son el código de los artículos 13, 16 y 17 sin cambios |
| Dependencias añadidas | `reflex`, `reflex-silverpoint-react`, `httpx` |
| `reflex export --frontend-only` | 3,7 s |
| JavaScript exportado | 16 archivos, 664 KB; 214 KB con gzip |
| CSS exportado | 4 archivos, 154 KB; 17 KB con gzip |
| Arranque de `reflex run` | 2,7 s hasta que responden frontend y backend; 3,3 s sin `.web/` |
| Primer gráfico listo | 294 ms en producción, 1.049 ms en desarrollo (mediana de 3) |

## Problemas comunes

* **El panel se queda color crema con la cianotipia.** Falta pasar `ground` y `palette` a `dashboard`: el panel no lee el proveedor.
* **La página no cambia de color.** El proveedor solo da estilo a los componentes de silverpoint. El fondo lo pone `ThemeState.page` en `shell`.
* **Las reglas de `rx.App(style=...)` no se aplican.** Sin `RadixThemesPlugin` no llegan al navegador. Usa una hoja en `assets/` y `stylesheets`.
* **Los tiempos de respuesta dicen «No data» al arrancar.** `sparkline_rows` recibió una lista vacía antes de la primera ronda. Pon el gráfico detrás de `rx.cond`.
* **La descarga falla con `FileNotFoundError`.** Falta `data/silverpoint-grounds.css`, o el backend arranca desde otra carpeta: la ruta es relativa a la raíz del proyecto.
* **Las peticiones se multiplican.** Hay varios procesos de backend, cada uno con su tarea de vida. Mide desde un solo proceso.

## Lo que viene

La aplicación Operations ya existe en cuatro frameworks. El [artículo 27](/blog/silverpoint_serie_27) las pone una al lado de la otra: cuánto código pide cada una, cuánto pesa y qué resultó más fácil o más difícil en cada framework.
