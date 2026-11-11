Title: Silverpoint, artículo 14: distribuciones, comparaciones e incertidumbre
Date: 2026-11-11 17:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_14
Authors: Ernesto Crespo
Summary: Los tiempos de respuesta del panel de operaciones con los gráficos estadísticos de silverpoint: histograma, diagrama de caja, violín y distribución acumulada, un antes y después con un gráfico de pesas, e intervalos con barras de error y una banda, en React y Reflex.

Un tiempo de respuesta medio de 393 milisegundos no dice si todas las peticiones tardan eso o si la mayoría tarda 300 y unas pocas pasan del segundo. Para verlo hay que dibujar la distribución, no la media.

Este artículo del nivel 2 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) añade al panel de operaciones los tiempos de respuesta de tres servicios. Los dibuja con los gráficos de distribución, compara un antes y un después, y muestra la incertidumbre de una estimación. Son gráficos de la familia `distributions-comparisons` y de la familia `areas`, las del [artículo 08](/blog/silverpoint_serie_8).

## Los datos

Cuarenta tiempos de respuesta en milisegundos por servicio: `API`, `Search` y `Checkout`. Los gráficos de distribución reciben una fila por observación, así que los tiempos se escriben por servicio y se aplanan. En `src/latency.ts`:

```ts
export type Timing = { service: string; ms: number };

const samples: Record<string, number[]> = {
  API: [69, 115, 158, 104, 138, 91, 125, 210, 114, 153, 102, 136, 89, 123, 187, 112, 150, 100, 133, 85,
    121, 176, 110, 146, 98, 131, 82, 119, 168, 108, 143, 96, 129, 77, 117, 163, 106, 141, 94, 127],
  Search: [107, 200, 291, 177, 248, 151, 220, 411, 197, 282, 174, 243, 146, 216, 358, 193, 274, 169, 238, 140,
    212, 333, 189, 267, 165, 233, 133, 208, 315, 185, 260, 161, 229, 123, 204, 302, 181, 254, 156, 224],
  Checkout: [174, 324, 472, 287, 402, 245, 356, 666, 318, 457, 281, 394, 236, 350, 580, 312, 444, 274, 386, 226,
    343, 539, 306, 432, 268, 378, 215, 337, 511, 300, 421, 261, 370, 199, 331, 489, 294, 411, 980, 1150],
};

export const timings: Timing[] = Object.entries(samples).flatMap(([service, values]) =>
  values.map((ms) => ({ service, ms })),
);
```

El resultado son 120 filas como `{ service: 'Checkout', ms: 980 }`. Las dos últimas de `Checkout` son peticiones que pasaron del segundo.

![Los siete gráficos de este artículo: histograma, caja, violín, distribución acumulada, pesas, barras de error y banda](./images/silverpoint-serie-14.png)

## Cuatro formas de ver una distribución

En `src/Distributions.tsx`:

```tsx
import { BoxPlotChart } from '@silverpoint/react/box-plot-chart';
import { EcdfChart } from '@silverpoint/react/ecdf-chart';
import { HistogramChart } from '@silverpoint/react/histogram-chart';
import { ViolinChart } from '@silverpoint/react/violin-chart';
import { timings } from './latency';

const twoServices = timings.filter((row) => row.service !== 'Search');

export function Distributions() {
  return (
    <>
      <HistogramChart data={timings} valueKey="ms" bins={12} title="Response time, all requests" />
      <BoxPlotChart data={timings} valueKey="ms" groupKey="service" title="Response time by service" />
      <ViolinChart data={timings} valueKey="ms" groupKey="service" title="Response time by service" />
      <EcdfChart
        data={twoServices}
        valueKey="ms"
        groupKey="service"
        markers={[0.5, 0.95]}
        title="Share of requests under each time"
      />
    </>
  );
}
```

**El histograma** cuenta cuántas observaciones caen en cada intervalo. `bins` acepta un número de intervalos iguales o una lista de límites crecientes. Sin `bins`, el número sale de la regla de Freedman–Diaconis, o de la de Sturges cuando el rango intercuartílico es 0; con estos datos serían 22 intervalos de 50 ms. Con `bins={12}` son doce de 100 ms, de 0 a 1200. `cumulative` convierte los conteos en un total acumulado.

**El diagrama de caja** resume cada grupo en cinco números: la caja va del primer al tercer cuartil, la línea interior es la mediana y los bigotes llegan hasta la última observación a menos de 1,5 rangos intercuartílicos de la caja. Lo que queda fuera se dibuja como puntos sueltos. En `Checkout` son tres: 666, 980 y 1150. `whisker` cambia el 1,5 y `outliers={false}` oculta los puntos.

**El violín** dibuja la densidad de cada grupo, en espejo, con los cuartiles marcados dentro. Enseña lo que la caja esconde: si un grupo tiene dos modas, la caja no lo dice y el violín sí. `bandwidth` fija el ancho del núcleo; por defecto es la media de las reglas de Silverman de los grupos.

**La distribución acumulada** (ECDF) dibuja, para cada tiempo, la proporción de peticiones que tardan eso o menos. `markers` traza reglas en los cuantiles que le pidas: aquí, la mediana y el percentil 95. Dibuja dos grupos como máximo, por eso el ejemplo filtra `Search`.

## El gráfico dibuja valores derivados

Estos cuatro gráficos no dibujan tus filas, sino lo que calculan con ellas: intervalos y conteos, cuartiles, densidades. silverpoint aplica esa misma regla a todo lo demás:

* **La tabla de datos** muestra los valores derivados. La del diagrama de caja tiene las columnas `n`, `min`, `q1`, `median`, `q3`, `max` y `outliers`, una fila por servicio. `min` y `max` son los extremos de los bigotes: en `API`, `max` vale 187 y el 210 aparece en `outliers`.
* **La descripción** nombra el método y sus parámetros. La del histograma dice «Histogram of 120 ms observations in 12 bins as 12 equal bins, from 0 to 1,200; the fullest bin, 100–200, holds 49».
* **La navegación por teclado** recorre los intervalos, o los grupos y sus valores atípicos, y anuncia sus valores derivados, no las observaciones.
* **Los eventos** entregan un resumen. En el diagrama de caja, el `datum` del elemento activo es `{ group, min, q1, median, q3, max, outliers }` y su `value` es la mediana; en el histograma, el `datum` es `{ x0, x1, count }`.

Dos diagnósticos son propios de estos gráficos, y como todos los `SP0xx`, solo aparecen en desarrollo:

* **`SP021`**: un parámetro estadístico no es válido y se usa el valor por defecto. Con `bins={0}`, el histograma vuelve a Freedman–Diaconis.
* **`SP022`**: un grupo tiene pocas observaciones para su estadístico, y se dibujan como puntos. El diagrama de caja necesita cinco por grupo; el violín, dos.

## Comparar un antes y un después

El servicio estrenó una versión, y la pregunta es cuánto bajó el percentil 95 de cada servicio. Son categorías con dos valores, la forma `categories` con la intención `change`, y el primero de la tabla del artículo 08 es el gráfico de pesas.

## La incertidumbre de una estimación

La media de cada servicio es una estimación, y tiene un margen. El gráfico de barras de error dibuja cada estimación con su intervalo del 95 %. La línea punteada de `reference` es el presupuesto de latencia, 300 ms: la media de `Checkout` está por encima, y su intervalo no llega a cruzarla.

La banda dibuja la incertidumbre a lo largo de un eje: el mínimo y el máximo de visitas de cada franja de dos horas en los últimos 30 días.

Los tres gráficos reciben valores ya calculados. En `src/summaries.ts`:

```ts
export type P95Change = { service: string; before: number; after: number };
export type MeanLatency = { service: string; mean: number; low: number; high: number };
export type HitRange = { hour: string; low: number; high: number };

export const p95: P95Change[] = [
  { service: 'API', before: 230, after: 177 },
  { service: 'Search', before: 410, after: 334 },
  { service: 'Checkout', before: 760, after: 682 },
];

export const means: MeanLatency[] = [
  { service: 'API', mean: 124, low: 114, high: 133 },
  { service: 'Search', mean: 219, low: 199, high: 240 },
  { service: 'Checkout', mean: 393, low: 334, high: 452 },
];

export const hitRange: HitRange[] = [
  { hour: '00', low: 15, high: 22 }, { hour: '02', low: 9, high: 14 },
  { hour: '04', low: 9, high: 14 }, { hour: '06', low: 19, high: 29 },
  { hour: '08', low: 35, high: 50 }, { hour: '10', low: 49, high: 67 },
  { hour: '12', low: 55, high: 74 }, { hour: '14', low: 50, high: 68 },
  { hour: '16', low: 48, high: 66 }, { hour: '18', low: 39, high: 55 },
  { hour: '20', low: 24, high: 36 }, { hour: '22', low: 18, high: 27 },
];
```

Los percentiles 95 de después y las medias con su intervalo salen de los tiempos de `src/latency.ts`. El intervalo es la media más y menos 1,96 errores típicos.

En `src/Comparisons.tsx`:

```tsx
import { DumbbellChart } from '@silverpoint/react/dumbbell-chart';
import { ErrorBarChart } from '@silverpoint/react/error-bar-chart';
import { RangeBandChart } from '@silverpoint/react/range-band-chart';
import { hitRange, means, p95 } from './summaries';

export function Comparisons() {
  return (
    <>
      <DumbbellChart
        data={p95}
        labelKey="service"
        startKey="before"
        endKey="after"
        names={['Before', 'After']}
        endMarker="arrow"
        title="p95 before and after the release"
      />
      <ErrorBarChart
        data={means}
        labelKey="service"
        estimateKey="mean"
        lowKey="low"
        highKey="high"
        reference={300}
        title="Mean response time, 95% interval"
      />
      <RangeBandChart
        data={hitRange}
        xKey="hour"
        lowKey="low"
        highKey="high"
        title="Hits per hour, last 30 days"
      />
    </>
  );
}
```

| Gráfico | Accesores | Otras props |
|---|---|---|
| `DumbbellChart` | `labelKey`, `startKey`, `endKey` | `names`, los títulos de los dos valores; `endMarker="arrow"`, una flecha que indica el sentido del cambio |
| `ErrorBarChart` | `labelKey`, `estimateKey`, `lowKey`, `highKey` | `reference`, una regla punteada |
| `RangeBandChart` | `xKey`, `lowKey`, `highKey` | — |

El gráfico de pesas y el de barras de error se orientan en filas por defecto, como se leen un antes y un después o un diagrama de bosque. Las descripciones resumen la comparación: la del gráfico de pesas dice «0 rise, 3 fall; the largest change is Checkout, −78», y la de las barras de error, «read against 300; 0 of them include it».

Los dos componentes van juntos en `src/App.tsx`:

```tsx
import { Comparisons } from './Comparisons';
import { Distributions } from './Distributions';

export default function App() {
  return (
    <main className="panel">
      <Distributions />
      <Comparisons />
    </main>
  );
}
```

La clase `panel` es la rejilla del artículo 08.

## El código en Reflex

Los datos, en `ops_panel/latency.py`:

```python
SAMPLES = {
    "API": [69, 115, 158, 104, 138, 91, 125, 210, 114, 153, 102, 136, 89, 123, 187, 112, 150, 100, 133, 85,
            121, 176, 110, 146, 98, 131, 82, 119, 168, 108, 143, 96, 129, 77, 117, 163, 106, 141, 94, 127],
    "Search": [107, 200, 291, 177, 248, 151, 220, 411, 197, 282, 174, 243, 146, 216, 358, 193, 274, 169, 238, 140,
               212, 333, 189, 267, 165, 233, 133, 208, 315, 185, 260, 161, 229, 123, 204, 302, 181, 254, 156, 224],
    "Checkout": [174, 324, 472, 287, 402, 245, 356, 666, 318, 457, 281, 394, 236, 350, 580, 312, 444, 274, 386, 226,
                 343, 539, 306, 432, 268, 378, 215, 337, 511, 300, 421, 261, 370, 199, 331, 489, 294, 411, 980, 1150],
}

TIMINGS = [{"service": service, "ms": ms} for service, values in SAMPLES.items() for ms in values]

P95 = [
    {"service": "API", "before": 230, "after": 177},
    {"service": "Search", "before": 410, "after": 334},
    {"service": "Checkout", "before": 760, "after": 682},
]

MEANS = [
    {"service": "API", "mean": 124, "low": 114, "high": 133},
    {"service": "Search", "mean": 219, "low": 199, "high": 240},
    {"service": "Checkout", "mean": 393, "low": 334, "high": 452},
]

HIT_RANGE = [
    {"hour": "00", "low": 15, "high": 22}, {"hour": "02", "low": 9, "high": 14},
    {"hour": "04", "low": 9, "high": 14}, {"hour": "06", "low": 19, "high": 29},
    {"hour": "08", "low": 35, "high": 50}, {"hour": "10", "low": 49, "high": 67},
    {"hour": "12", "low": 55, "high": 74}, {"hour": "14", "low": 50, "high": 68},
    {"hour": "16", "low": 48, "high": 66}, {"hour": "18", "low": 39, "high": 55},
    {"hour": "20", "low": 24, "high": 36}, {"hour": "22", "low": 18, "high": 27},
]
```

La página, en `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import (
    box_plot_chart,
    dumbbell_chart,
    ecdf_chart,
    error_bar_chart,
    histogram_chart,
    range_band_chart,
    violin_chart,
)

from .latency import HIT_RANGE, MEANS, P95, TIMINGS

TWO_SERVICES = [row for row in TIMINGS if row["service"] != "Search"]


def index() -> rx.Component:
    return rx.grid(
        histogram_chart(data=TIMINGS, value_key="ms", bins=12, title="Response time, all requests"),
        box_plot_chart(data=TIMINGS, value_key="ms", group_key="service", title="Response time by service"),
        violin_chart(data=TIMINGS, value_key="ms", group_key="service", title="Response time by service"),
        ecdf_chart(
            data=TWO_SERVICES,
            value_key="ms",
            group_key="service",
            markers=[0.5, 0.95],
            title="Share of requests under each time",
        ),
        dumbbell_chart(
            data=P95,
            label_key="service",
            start_key="before",
            end_key="after",
            names=["Before", "After"],
            end_marker="arrow",
            title="p95 before and after the release",
        ),
        error_bar_chart(
            data=MEANS,
            label_key="service",
            estimate_key="mean",
            low_key="low",
            high_key="high",
            reference=300,
            title="Mean response time, 95% interval",
        ),
        range_band_chart(
            data=HIT_RANGE,
            x_key="hour",
            low_key="low",
            high_key="high",
            title="Hits per hour, last 30 days",
        ),
        columns="4",
        gap="16px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

Las descripciones y las tablas de datos son las mismas que en React: los cálculos los hace el motor, no el adaptador.

## En Vue y en Angular

| Gráfico | Vue | Angular |
|---|---|---|
| Histograma | `SpHistogramChart` | `<sp-histogram-chart>` |
| Diagrama de caja | `SpBoxPlotChart` | `<sp-box-plot-chart>` |
| Violín | `SpViolinChart` | `<sp-violin-chart>` |
| Distribución acumulada | `SpEcdfChart` | `<sp-ecdf-chart>` |
| Pesas | `SpDumbbellChart` | `<sp-dumbbell-chart>` |
| Barras de error | `SpErrorBarChart` | `<sp-error-bar-chart>` |
| Banda | `SpRangeBandChart` | `<sp-range-band-chart>` |

Cada uno se importa de su ruta, como `@silverpoint/vue/box-plot-chart` o `@silverpoint/angular/box-plot-chart`, y las props son las mismas con la sintaxis de cada framework.

## Lo que viene

Ya tienes en el panel la forma de los tiempos de respuesta, no solo su media. El artículo 15 cierra el nivel 2 con los datos que no caben en una tabla plana: jerarquías, flujos y redes, y la navegación por niveles de los gráficos jerárquicos.

La [galería](https://silverpointweb.vercel.app/gallery) muestra los 14 gráficos de la familia de distribuciones y comparaciones.
