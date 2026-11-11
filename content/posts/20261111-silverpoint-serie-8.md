Title: Silverpoint, artículo 08: cómo elegir el gráfico, las familias del catálogo
Date: 2026-11-11 14:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_8
Authors: Ernesto Crespo
Summary: Un método en dos pasos para elegir entre los 60 gráficos de silverpoint: la forma de los datos y lo que el lector tiene que ver. Las nueve familias del catálogo y tres decisiones del panel de operaciones, con código en React y Reflex.

Con este artículo empieza el nivel 2 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint): construir un panel con estilo propio e interacción. Antes de dar estilo a un panel hay que decidir qué gráficos lleva, y el catálogo tiene 60.

No hace falta conocerlos todos. silverpoint los clasifica con dos preguntas, y con ellas la lista se reduce a dos o tres candidatos. Este artículo explica esas dos preguntas, recorre las nueve familias del catálogo y las aplica a los tres primeros datos del panel de operaciones.

## El método: dos preguntas

La primera pregunta es qué forma tienen las filas. La segunda, qué tiene que ver el lector en ellas. El orden importa: la forma de los datos descarta la mayoría de los gráficos, y la intención elige entre los que quedan.

## Paso 1: la forma de los datos

Cada gráfico declara la forma de los datos que dibuja. Son doce:

| Forma | Las filas contienen | Por ejemplo |
|---|---|---|
| `series` | Una fila por punto de un eje ordenado (tiempo, secuencia) | Visitas por hora |
| `categories` | Una fila por categoría, con uno o más valores | Ingresos por región |
| `parts` | Las partes de un mismo total | Tráfico por canal |
| `matrix` | Un valor por cada par de categorías | Errores por día y hora |
| `hierarchy` | Una fila por nodo, con su `id` y su `parent` | Un presupuesto por departamento |
| `links` | Filas con origen, destino y valor | Los pasos de un registro |
| `points` | Dos o más medidas numéricas por fila | Precio frente a valoración |
| `distribution` | Muchas observaciones de una misma medida | Tiempos de respuesta |
| `intervals` | Un inicio y un fin por fila | Un calendario de tareas |
| `events` | Ocurrencias con fecha, o marcas sobre un ciclo | Commits por día |
| `single` | Una cifra, quizá con un objetivo | Los ingresos de este mes |
| `field` | Una medida o un vector sobre un plano | Un campo de viento |

La forma se lee en las filas, no en el tema. Las visitas por hora son una `series` porque cada fila es un punto de un eje ordenado. Los mismos números agrupados por día de la semana y franja horaria son una `matrix`.

## Paso 2: lo que el lector tiene que ver

La intención es lo que el gráfico tiene que hacer evidente. silverpoint usa catorce:

| Intención | El lector tiene que ver |
|---|---|
| `trend` | Hacia dónde va un valor |
| `change` | Cuánto cambió entre dos momentos |
| `compare` | Qué valor es mayor |
| `rank` | El orden de las categorías |
| `part-to-whole` | Cuánto pesa cada parte del total |
| `distribution` | Cómo se reparten las observaciones |
| `correlation` | Si dos medidas se mueven juntas |
| `flow` | Por dónde pasa un volumen |
| `hierarchy` | Qué contiene a qué |
| `uncertainty` | Cuánto margen tiene una estimación |
| `progress` | Cuánto falta para un objetivo |
| `schedule` | Cuándo ocurre cada cosa |
| `kpi` | Una cifra y su evolución, de un vistazo |
| `network` | Quién se conecta con quién |

Una misma forma admite varias intenciones. Con `categories`, `compare` lleva a un gráfico de barras, `change` a un gráfico de pesas y `progress` a un gráfico de bala.

## Las nueve familias

Los 60 gráficos se agrupan en nueve familias, por cómo dibujan:

| Familia | Gráficos | Algunos de ellos | Formas habituales |
|---|---|---|---|
| `lines` | 4 | `line-chart`, `step-chart`, `sparkline-rows`, `kpi-card` | `series`, `single` |
| `bars` | 8 | `bar-chart`, `stacked-bar-chart`, `waterfall-chart`, `funnel-chart` | `categories` |
| `areas` | 3 | `area-chart`, `range-band-chart`, `stream-chart` | `series`, `intervals` |
| `points-grids` | 5 | `scatter-chart`, `heatmap-chart`, `activity-grid` | `points`, `matrix`, `events` |
| `radial` | 11 | `donut-chart`, `radar-chart`, `gauge-arc` | `parts`, `categories`, `single` |
| `flows` | 2 | `sankey-chart`, `chord-ring` | `links` |
| `distributions-comparisons` | 14 | `histogram-chart`, `box-plot-chart`, `dumbbell-chart` | `distribution`, `categories`, `intervals` |
| `hierarchies-dimensions` | 8 | `squarified-treemap`, `sunburst-chart`, `waffle-chart` | `hierarchy`, `parts`, `matrix` |
| `fields-networks` | 5 | `network-chart`, `contour-chart`, `vector-field-chart` | `points`, `links`, `field` |

La familia es útil para buscar en la documentación y en la [galería](https://silverpointweb.vercel.app/gallery), pero no para elegir: un gráfico radial y uno de barras pueden responder a la misma pregunta. Para elegir se usan la forma y la intención.

## La tabla de recomendaciones

silverpoint guarda una tabla revisada a mano que cruza cada forma con cada intención y puntúa a los candidatos de 0 a 1. Estas son las combinaciones más frecuentes en un panel:

| Forma | Intención | El primero | Las alternativas |
|---|---|---|---|
| `series` | `trend` | `line-chart` (0,9) | `area-chart` (0,8), `step-chart` (0,6) |
| `series` | `kpi` | `sparkline-rows` (0,85) | `kpi-card` (0,75) |
| `categories` | `compare` | `bar-chart` (0,9) | `lollipop-chart` (0,75), `radar-chart` (0,5) |
| `categories` | `change` | `dumbbell-chart` (0,9) | `slope-chart` (0,85), `waterfall-chart` (0,75) |
| `parts` | `part-to-whole` | `donut-chart` (0,9) | `waffle-chart` (0,85), `treemap-chart` (0,7) |
| `matrix` | `compare` | `heatmap-chart` (0,9) | `marimekko-chart` (0,7) |
| `distribution` | `compare` | `box-plot-chart` (0,9) | `violin-chart` (0,85), `ridgeline-chart` (0,8) |
| `intervals` | `uncertainty` | `error-bar-chart` (0,9) | `range-band-chart` (0,85) |
| `links` | `flow` | `sankey-chart` (0,9) | `chord-ring` (0,75) |
| `hierarchy` | `part-to-whole` | `squarified-treemap` (0,9) | `sunburst-chart` (0,85) |

La tabla también tiene en cuenta el volumen. Con más de seis partes, el donut pierde 0,3 puntos, porque un anillo no se lee bien con tantos sectores. Con más de doce categorías, el gráfico de piruletas gana 0,2, y el radar, las barras polares y el coxcomb pierden 0,3. Con más de 500 puntos, el gráfico de densidad por celdas gana al de dispersión.

## Aplicado al panel de operaciones

El panel de la serie tiene tres datos para empezar. Cada uno pasa por las dos preguntas.

**Las visitas por hora.** Una fila por hora, en orden: la forma es `series`. El lector tiene que ver cómo evoluciona el tráfico durante el día: la intención es `trend`. El primero de la tabla es `line-chart`, el gráfico de los artículos 03 a 07.

**Los errores por día y franja horaria.** Cada fila es un día de la semana con seis valores, uno por franja de cuatro horas: la forma es `matrix`. El lector tiene que comparar franjas y días para encontrar dónde se concentran los errores: la intención es `compare`. El primero es `heatmap-chart`.

**Las ventas por canal.** Cuatro canales que suman un total: la forma es `parts`. El lector tiene que ver cuánto aporta cada canal: la intención es `part-to-whole`. El primero es `donut-chart`, y con cuatro partes no recibe la penalización de los seis sectores.

![Los tres gráficos del panel: visitas por hora, errores por día y franja, ventas por canal](./images/silverpoint-serie-8.png)

El gráfico de barras sería la alternativa para las ventas si la pregunta cambiara. Para comparar los canales entre sí, o este mes con el anterior, los datos dejan de ser partes de un total y pasan a ser `categories` con la intención `compare`, y ahí el primero es `bar-chart`. La pregunta decide el gráfico, no los números.

## El código en React

Los datos, en `src/panel.ts`:

```ts
export type HourlyTraffic = { hour: string; hits: number };
export type DailyErrors = { day: string; values: number[] };
export type ChannelSales = { channel: string; sales: number };

export const traffic: HourlyTraffic[] = [
  { hour: '00', hits: 18 }, { hour: '01', hits: 14 }, { hour: '02', hits: 11 },
  { hour: '03', hits: 9 }, { hour: '04', hits: 11 }, { hour: '05', hits: 16 },
  { hour: '06', hits: 24 }, { hour: '07', hits: 33 }, { hour: '08', hits: 42 },
  { hour: '09', hits: 51 }, { hour: '10', hits: 58 }, { hour: '11', hits: 62 },
  { hour: '12', hits: 64 }, { hour: '13', hits: 61 }, { hour: '14', hits: 59 },
  { hour: '15', hits: 58 }, { hour: '16', hits: 57 }, { hour: '17', hits: 52 },
  { hour: '18', hits: 47 }, { hour: '19', hits: 41 }, { hour: '20', hits: 30 },
  { hour: '21', hits: 26 }, { hour: '22', hits: 22 }, { hour: '23', hits: 20 },
];

export const errors: DailyErrors[] = [
  { day: 'Mon', values: [3, 5, 31, 38, 22, 8] },
  { day: 'Tue', values: [2, 6, 28, 35, 20, 7] },
  { day: 'Wed', values: [4, 7, 34, 40, 25, 9] },
  { day: 'Thu', values: [3, 5, 29, 36, 21, 8] },
  { day: 'Fri', values: [2, 6, 26, 30, 18, 10] },
  { day: 'Sat', values: [1, 2, 9, 12, 10, 6] },
  { day: 'Sun', values: [1, 1, 7, 10, 8, 5] },
];

export const blocks = ['00-04', '04-08', '08-12', '12-16', '16-20', '20-24'];

export const sales: ChannelSales[] = [
  { channel: 'Web', sales: 46 },
  { channel: 'App', sales: 31 },
  { channel: 'Partners', sales: 15 },
  { channel: 'Phone', sales: 8 },
];
```

Los tres gráficos, en `src/App.tsx`:

```tsx
import { DonutChart } from '@silverpoint/react/donut-chart';
import { HeatmapChart } from '@silverpoint/react/heatmap-chart';
import { LineChart } from '@silverpoint/react/line-chart';
import { blocks, errors, sales, traffic } from './panel';

export default function App() {
  return (
    <main className="panel">
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        footerLeft="Last 24 hours, in thousands"
      />
      <HeatmapChart
        data={errors}
        labelKey="day"
        valuesKey="values"
        columnLabels={blocks}
        scaleMax={40}
        title="Errors by day and time"
      />
      <DonutChart
        data={sales}
        nameKey="channel"
        valueKey="sales"
        centerLabel="thousand EUR"
        title="Sales by channel"
      />
    </main>
  );
}
```

Y una rejilla para colocarlos, en `src/index.css`:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}

.panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
```

Cada gráfico tiene sus propios accesores, que dependen de su forma:

| Gráfico | Accesores | Otras props |
|---|---|---|
| `LineChart` | `xKey`, `valueKey` | `secondaryKey` para una segunda serie punteada |
| `HeatmapChart` | `labelKey`, `valuesKey` | `columnLabels`, los nombres de las columnas; `scaleMax`, el valor del tono más oscuro |
| `DonutChart` | `nameKey`, `valueKey` | `centerValue` y `centerLabel`, el centro del anillo; `legend` |

Dos detalles de esta versión:

* **`scaleMax` del mapa de calor vale 100 por defecto.** Los errores no pasan de 40, así que con el valor por defecto todas las celdas quedarían en los tonos claros. Con `scaleMax={40}`, la celda de 40 recibe el tramado más denso.
* **El centro del donut muestra el total.** Sin `centerValue`, el anillo escribe la suma de las partes, 100, y la leyenda da el porcentaje de cada canal.

## El código en Reflex

Los datos, en `ops_panel/panel.py`:

```python
TRAFFIC = [
    {"hour": "00", "hits": 18}, {"hour": "01", "hits": 14}, {"hour": "02", "hits": 11},
    {"hour": "03", "hits": 9}, {"hour": "04", "hits": 11}, {"hour": "05", "hits": 16},
    {"hour": "06", "hits": 24}, {"hour": "07", "hits": 33}, {"hour": "08", "hits": 42},
    {"hour": "09", "hits": 51}, {"hour": "10", "hits": 58}, {"hour": "11", "hits": 62},
    {"hour": "12", "hits": 64}, {"hour": "13", "hits": 61}, {"hour": "14", "hits": 59},
    {"hour": "15", "hits": 58}, {"hour": "16", "hits": 57}, {"hour": "17", "hits": 52},
    {"hour": "18", "hits": 47}, {"hour": "19", "hits": 41}, {"hour": "20", "hits": 30},
    {"hour": "21", "hits": 26}, {"hour": "22", "hits": 22}, {"hour": "23", "hits": 20},
]

ERRORS = [
    {"day": "Mon", "values": [3, 5, 31, 38, 22, 8]},
    {"day": "Tue", "values": [2, 6, 28, 35, 20, 7]},
    {"day": "Wed", "values": [4, 7, 34, 40, 25, 9]},
    {"day": "Thu", "values": [3, 5, 29, 36, 21, 8]},
    {"day": "Fri", "values": [2, 6, 26, 30, 18, 10]},
    {"day": "Sat", "values": [1, 2, 9, 12, 10, 6]},
    {"day": "Sun", "values": [1, 1, 7, 10, 8, 5]},
]

BLOCKS = ["00-04", "04-08", "08-12", "12-16", "16-20", "20-24"]

SALES = [
    {"channel": "Web", "sales": 46},
    {"channel": "App", "sales": 31},
    {"channel": "Partners", "sales": 15},
    {"channel": "Phone", "sales": 8},
]
```

La página, en `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import donut_chart, heatmap_chart, line_chart

from .panel import BLOCKS, ERRORS, SALES, TRAFFIC


def index() -> rx.Component:
    return rx.grid(
        line_chart(
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            footer_left="Last 24 hours, in thousands",
        ),
        heatmap_chart(
            data=ERRORS,
            label_key="day",
            values_key="values",
            column_labels=BLOCKS,
            scale_max=40,
            title="Errors by day and time",
        ),
        donut_chart(
            data=SALES,
            name_key="channel",
            value_key="sales",
            center_label="thousand EUR",
            title="Sales by channel",
        ),
        columns="3",
        gap="16px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

`rx.grid` reparte el ancho en tres columnas, y cada gráfico toma el de la suya.

## En Vue y en Angular

Los mismos tres gráficos, con los nombres de cada adaptador:

| Gráfico | Vue | Angular |
|---|---|---|
| Línea | `SpLineChart`, de `@silverpoint/vue/line-chart` | `<sp-line-chart>`, de `@silverpoint/angular/line-chart` |
| Mapa de calor | `SpHeatmapChart`, de `@silverpoint/vue/heatmap-chart` | `<sp-heatmap-chart>`, de `@silverpoint/angular/heatmap-chart` |
| Donut | `SpDonutChart`, de `@silverpoint/vue/donut-chart` | `<sp-donut-chart>`, de `@silverpoint/angular/donut-chart` |

Las props son las mismas, con la sintaxis del artículo 07: `:column-labels="blocks"` y `:scale-max="40"` en Vue, `[columnLabels]="blocks"` y `[scaleMax]="40"` en Angular.

## La misma tabla, para un asistente de IA

La tabla de recomendaciones no es un modelo: es una lista revisada, y el servidor MCP de silverpoint la expone con la herramienta `recommend_chart`. Con la forma `parts`, la intención `part-to-whole` y cuatro filas, responde lo mismo que este artículo: `donut-chart` con 0,9, `waffle-chart` con 0,85 y `treemap-chart` con 0,7. El servidor MCP tiene su propio artículo, el 28.

## Lo que viene

Ya tienes los tres primeros gráficos del panel y un método para elegir los siguientes. El artículo 09 les da un estilo común: los estilos base, los sustratos y el proveedor que fija el estilo de toda la aplicación en un solo sitio.

Los 60 gráficos se pueden ver en vivo en la [galería](https://silverpointweb.vercel.app/gallery).
