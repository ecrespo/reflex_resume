Title: Silverpoint, artículo 06: tu primer gráfico en Reflex, solo con Python
Date: 2026-11-11 13:30
Category: Tutorial Silverpoint
Tags: silverpoint, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_6
Authors: Ernesto Crespo
Summary: Paso a paso, de un proyecto nuevo de Reflex al primer gráfico de silverpoint sin escribir JavaScript: instalación con uv, datos propios, el texto de la tarjeta y la carga de datos en el estado con on_load.

Este es el artículo de Reflex del nivel 1 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint). Construye el mismo gráfico que el [artículo 03](/blog/silverpoint_serie_3) construye en React, el [04](/blog/silverpoint_serie_4) en Vue y el [05](/blog/silverpoint_serie_5) en Angular, pero aquí todo se escribe en Python. Puedes leer solo este: se instala todo desde cero.

## Lo que vas a construir

La primera pieza del panel de operaciones de la serie: un gráfico de línea con las visitas por hora a un servicio web durante las últimas 24 horas, en miles.

![El gráfico de visitas por hora, dibujado con Reflex](./images/silverpoint-serie-6.png)

Al terminar tendrás el gráfico con tus propios datos, el texto de la tarjeta y los datos cargados en el estado de Reflex desde un archivo JSON, como harías con una API o una base de datos.

## Lo que necesitas

* Python 3.11 o posterior. Este artículo usa la 3.13.
* [uv](https://docs.astral.sh/uv/), para el proyecto y sus dependencias.
* Conocer lo básico de Reflex: componentes, estado y eventos.

No hace falta escribir JavaScript. Reflex descarga Bun, el entorno de JavaScript con el que compila la página, la primera vez que lo necesita.

## 1. Crear el proyecto

```sh
mkdir ops_panel && cd ops_panel
uv init --python 3.13
uv add reflex-silverpoint-react
uv run reflex init --template blank
rm main.py
```

`uv add reflex-silverpoint-react` instala el paquete y, como dependencia, Reflex. `reflex init` crea `rxconfig.py` y el módulo de la aplicación, `ops_panel/ops_panel.py`. El `main.py` que genera `uv init` no se usa.

No hay que instalar nada del lado de JavaScript. Al compilar, Reflex instala `@silverpoint/react` y los demás paquetes npm en las versiones que fija el paquete, y cada componente importa las hojas de estilos que necesita.

## 2. El primer gráfico

Sustituye `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import line_chart


def index() -> rx.Component:
    return rx.box(
        line_chart(title="Hits per hour"),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

Arranca la aplicación:

```sh
uv run reflex run
```

Y abre `http://localhost:3000`. Verás un gráfico de línea con doce horas y dos series: la línea continua y una línea base punteada.

Son los datos de demostración del gráfico: cuando no recibe `data`, dibuja los suyos. Sirven para comprobar que la instalación funciona.

Todos los componentes salen del mismo módulo, `reflex_silverpoint_react`, con nombres en `snake_case`: los gráficos sin prefijo (`line_chart`, `bar_chart`) y los componentes de interfaz con `sp_` (`sp_button`).

## 3. Tus propios datos

Crea `ops_panel/traffic.py` con las visitas de un día, una fila por hora:

```python
TRAFFIC = [
    {"hour": "00", "hits": 18},
    {"hour": "01", "hits": 14},
    {"hour": "02", "hits": 11},
    {"hour": "03", "hits": 9},
    {"hour": "04", "hits": 11},
    {"hour": "05", "hits": 16},
    {"hour": "06", "hits": 24},
    {"hour": "07", "hits": 33},
    {"hour": "08", "hits": 42},
    {"hour": "09", "hits": 51},
    {"hour": "10", "hits": 58},
    {"hour": "11", "hits": 62},
    {"hour": "12", "hits": 64},
    {"hour": "13", "hits": 61},
    {"hour": "14", "hits": 59},
    {"hour": "15", "hits": 58},
    {"hour": "16", "hits": 57},
    {"hour": "17", "hits": 52},
    {"hour": "18", "hits": 47},
    {"hour": "19", "hits": 41},
    {"hour": "20", "hits": 30},
    {"hour": "21", "hits": 26},
    {"hour": "22", "hits": 22},
    {"hour": "23", "hits": 20},
]

PEAK = max(TRAFFIC, key=lambda row: row["hits"])
```

Pasa los datos al gráfico y completa la tarjeta. Sustituye `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import line_chart

from .traffic import PEAK, TRAFFIC


def index() -> rx.Component:
    return rx.box(
        line_chart(
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            badge="Today",
            value=PEAK["hits"],
            unit="k hits at the peak",
            footer_left="Last 24 hours",
            footer_right=f"Peak at {PEAK['hour']}:00",
            height=200,
        ),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

Las props son las mismas que en React, escritas en `snake_case`:

| Prop | Qué hace |
|---|---|
| `data` | Las filas que se dibujan |
| `x_key` | El campo de cada fila que va en el eje horizontal |
| `value_key` | El campo con el valor que dibuja la línea |
| `title` | El título de la tarjeta |
| `badge` | Una etiqueta corta, arriba a la derecha |
| `value` y `unit` | El valor destacado y su unidad, bajo el título |
| `footer_left` y `footer_right` | El pie de la tarjeta |
| `height` | El alto del área de dibujo en píxeles; por defecto, 160 |

El ancho no se indica: el gráfico toma el de su contenedor, el `rx.box` de 640 píxeles.

Aquí los datos son constantes de Python. Reflex los escribe en la página al compilar, así que esta versión no necesita el backend para mostrar el gráfico.

El punto realzado en blanco está al final de la línea, no en el pico. Es la regla del realce único del artículo 01: en un gráfico de línea, se realza el valor vivo, el último de la serie. El pico lo cuentan el valor destacado y el pie.

## 4. Cargar los datos en el estado

En un panel real los datos llegan de una API o de una base de datos, y cambian. En Reflex, eso es trabajo del estado: el backend lee los datos y la página se actualiza.

Para simularlo, crea `data/traffic.json` en la raíz del proyecto, junto a `rxconfig.py`, con una marca de tiempo y el número de peticiones por hora:

```json
[
  {"time": "2026-11-11T00:00:00Z", "requests": 17800},
  {"time": "2026-11-11T01:00:00Z", "requests": 13937},
  {"time": "2026-11-11T02:00:00Z", "requests": 11074},
  {"time": "2026-11-11T03:00:00Z", "requests": 8811},
  {"time": "2026-11-11T04:00:00Z", "requests": 10948},
  {"time": "2026-11-11T05:00:00Z", "requests": 16085},
  {"time": "2026-11-11T06:00:00Z", "requests": 23822},
  {"time": "2026-11-11T07:00:00Z", "requests": 32959},
  {"time": "2026-11-11T08:00:00Z", "requests": 42096},
  {"time": "2026-11-11T09:00:00Z", "requests": 50833},
  {"time": "2026-11-11T10:00:00Z", "requests": 57970},
  {"time": "2026-11-11T11:00:00Z", "requests": 62107},
  {"time": "2026-11-11T12:00:00Z", "requests": 63844},
  {"time": "2026-11-11T13:00:00Z", "requests": 60981},
  {"time": "2026-11-11T14:00:00Z", "requests": 59118},
  {"time": "2026-11-11T15:00:00Z", "requests": 57855},
  {"time": "2026-11-11T16:00:00Z", "requests": 56992},
  {"time": "2026-11-11T17:00:00Z", "requests": 52129},
  {"time": "2026-11-11T18:00:00Z", "requests": 46866},
  {"time": "2026-11-11T19:00:00Z", "requests": 41003},
  {"time": "2026-11-11T20:00:00Z", "requests": 30140},
  {"time": "2026-11-11T21:00:00Z", "requests": 25877},
  {"time": "2026-11-11T22:00:00Z", "requests": 22014},
  {"time": "2026-11-11T23:00:00Z", "requests": 20151}
]
```

Y sustituye `ops_panel/ops_panel.py` por la versión con estado:

```python
import json
from pathlib import Path

import reflex as rx
from reflex_silverpoint_react import line_chart

DATA_FILE = Path("data/traffic.json")


class TrafficState(rx.State):
    traffic: list[dict[str, str | int]] = []

    @rx.event
    def load(self):
        rows = json.loads(DATA_FILE.read_text())
        self.traffic = [
            {"hour": row["time"][11:13], "hits": round(row["requests"] / 1000)}
            for row in rows
        ]

    @rx.var
    def peak(self) -> dict[str, str | int]:
        return max(self.traffic, key=lambda row: row["hits"], default={"hour": "", "hits": 0})


def index() -> rx.Component:
    return rx.box(
        rx.cond(
            TrafficState.traffic,
            line_chart(
                data=TrafficState.traffic,
                x_key="hour",
                value_key="hits",
                title="Hits per hour",
                badge="Today",
                value=TrafficState.peak["hits"],
                unit="k hits at the peak",
                footer_left="Last 24 hours",
                footer_right=f"Peak at {TrafficState.peak['hour']}:00",
                height=200,
            ),
            rx.text("Loading…"),
        ),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index, on_load=TrafficState.load)
```

Ya no se usa `ops_panel/traffic.py`; puedes borrarlo. Cuatro decisiones de esta versión:

* **Los datos se adaptan en el backend.** El evento `load` convierte cada fila del JSON en una fila del gráfico: la hora sale de la marca de tiempo y las peticiones pasan a miles. Al navegador solo llegan las filas que dibuja el gráfico.
* **Los datos se cargan al abrir la página.** `on_load=TrafficState.load` ejecuta el evento cada vez que se abre la ruta. Para leer de una API o de una base de datos, solo cambia el cuerpo de `load`.
* **Mientras no hay datos, no hay gráfico.** `rx.cond` muestra «Loading…» mientras `traffic` está vacía. No le pases una lista vacía al gráfico: con datos vacíos dibuja su estado vacío, «No data», y no los datos de demostración.
* **El pico es una variable calculada.** `peak` se recalcula cada vez que cambia `traffic`. En la página se usa como cualquier variable de estado, también dentro de una f-string: `f"Peak at {TrafficState.peak['hour']}:00"` no es un texto fijo, Reflex lo convierte en una expresión que el navegador evalúa con el valor actual.

La ruta de `DATA_FILE` es relativa al directorio desde el que arrancas Reflex, la raíz del proyecto.

## 5. Ejecutar en modo producción

```sh
uv run reflex run --env prod
```

Reflex compila el frontend optimizado y sirve la página y el backend en el mismo puerto, `http://localhost:3000`. Para desplegarlo, la [guía de despliegue de Reflex](https://reflex.dev/docs/hosting/self-hosting/) explica las opciones.

## Problemas comunes

* **El gráfico no aparece.** Su contenedor no tiene ancho. Pasa con un `rx.hstack` o un `rx.flex` que se ajusta a su contenido: el gráfico espera a poder medirlo y, en desarrollo, la consola del navegador muestra el diagnóstico `SP003`. Dale un ancho al contenedor o al gráfico.
* **La tarjeta dice «No data».** El nombre de `x_key` o de `value_key` no coincide con los campos de las filas. En desarrollo, la consola del navegador muestra `SP002` con el nombre del campo.
* **«FileNotFoundError: [Errno 2] No such file or directory: 'data/traffic.json'».** Arrancaste Reflex desde otro directorio. Ejecútalo desde la raíz del proyecto, donde está `rxconfig.py`.
* **El gráfico se queda en «Loading…».** El backend no responde. Mira la terminal donde corre `reflex run`: un error en `load` aparece ahí.

Los diagnósticos `SP0xx` solo aparecen en desarrollo.

## Lo que viene

Ya tienes un gráfico de silverpoint en Reflex con tus propios datos, sin una línea de JavaScript. El siguiente es el 07: las propiedades que comparten los 60 gráficos, con sus nombres en las cuatro sintaxis.

La [guía de Reflex](https://silverpointweb.vercel.app/docs/reflex) de la documentación tiene más ejemplos.
