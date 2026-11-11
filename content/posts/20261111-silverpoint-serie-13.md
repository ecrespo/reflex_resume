Title: Silverpoint, artículo 13: paneles, una rejilla responsiva definida como datos
Date: 2026-11-11 17:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_13
Authors: Ernesto Crespo
Summary: El panel de operaciones como un Dashboard de silverpoint: una rejilla responsiva cuya distribución es un objeto de datos, celdas que dan su tamaño a cada gráfico, gráficos enlazados por la hora y el mismo panel en React, Vue, Angular y Reflex.

Hasta ahora cada artículo de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) dibujaba gráficos sueltos. Este los reúne en el panel de operaciones: dos indicadores, el tráfico por hora, los errores por hora, los errores por día y las ventas por canal, en una rejilla que se adapta al ancho disponible.

La pieza es `Dashboard`. No tiene coordenadas ni arrastre: la distribución es un objeto de datos que dice cuántas columnas hay en cada tamaño y cuántas columnas y filas ocupa cada celda. Los gráficos son sus hijos, y cada uno recibe de su celda el ancho y el alto.

## Lo que vas a construir

![El panel de operaciones en una pantalla de escritorio, con la hora 11 enlazada en todos los gráficos](./images/silverpoint-serie-13.png)

En una pantalla de escritorio el panel tiene cuatro columnas. En una tableta pasa a dos y en un móvil a una, sin cambiar el orden de lectura. Al pasar el puntero por la hora 11 del tráfico, la misma hora se marca en los errores por hora y en los dos indicadores.

## Los datos

Las filas por hora de los artículos anteriores ganan un campo, `errors`. Con ellas, las dos tablas nuevas del panel: los errores por día y franja de cuatro horas, y las ventas por canal en miles de euros. En React y Vue, este archivo es `src/ops.ts`; en Angular, `src/app/ops.ts`:

```ts
export type HourRow = { hour: string; hits: number; errors: number };
export type DayRow = { day: string; values: number[] };
export type ChannelRow = { channel: string; sales: number };

export const hourly: HourRow[] = [
  { hour: '00', hits: 18, errors: 2 },
  { hour: '01', hits: 14, errors: 1 },
  { hour: '02', hits: 11, errors: 1 },
  { hour: '03', hits: 9, errors: 0 },
  { hour: '04', hits: 11, errors: 1 },
  { hour: '05', hits: 16, errors: 1 },
  { hour: '06', hits: 24, errors: 2 },
  { hour: '07', hits: 33, errors: 4 },
  { hour: '08', hits: 42, errors: 6 },
  { hour: '09', hits: 51, errors: 7 },
  { hour: '10', hits: 58, errors: 9 },
  { hour: '11', hits: 62, errors: 8 },
  { hour: '12', hits: 64, errors: 11 },
  { hour: '13', hits: 61, errors: 9 },
  { hour: '14', hits: 59, errors: 7 },
  { hour: '15', hits: 58, errors: 6 },
  { hour: '16', hits: 57, errors: 6 },
  { hour: '17', hits: 52, errors: 5 },
  { hour: '18', hits: 47, errors: 4 },
  { hour: '19', hits: 41, errors: 4 },
  { hour: '20', hits: 30, errors: 3 },
  { hour: '21', hits: 26, errors: 2 },
  { hour: '22', hits: 22, errors: 2 },
  { hour: '23', hits: 20, errors: 2 },
];

export const errorsByDay: DayRow[] = [
  { day: 'Mon', values: [3, 5, 31, 38, 22, 8] },
  { day: 'Tue', values: [2, 6, 28, 35, 20, 7] },
  { day: 'Wed', values: [4, 7, 34, 40, 25, 9] },
  { day: 'Thu', values: [3, 5, 29, 36, 21, 8] },
  { day: 'Fri', values: [2, 6, 26, 30, 18, 10] },
  { day: 'Sat', values: [1, 2, 9, 12, 10, 6] },
  { day: 'Sun', values: [1, 1, 7, 10, 8, 5] },
];

export const blocks = ['00-04', '04-08', '08-12', '12-16', '16-20', '20-24'];

export const sales: ChannelRow[] = [
  { channel: 'Web', sales: 46 },
  { channel: 'App', sales: 31 },
  { channel: 'Partners', sales: 15 },
  { channel: 'Phone', sales: 8 },
];
```

## El panel en React

Sustituye `src/App.tsx`:

```tsx
import { useState } from 'react';
import { BarChart } from '@silverpoint/react/bar-chart';
import { Dashboard, DashboardCell, type DashboardLayout } from '@silverpoint/react/dashboard';
import { DonutChart } from '@silverpoint/react/donut-chart';
import { HeatmapChart } from '@silverpoint/react/heatmap-chart';
import { KpiCard } from '@silverpoint/react/kpi-card';
import { LineChart } from '@silverpoint/react/line-chart';
import { blocks, errorsByDay, hourly, sales } from './ops';

const layout: DashboardLayout = {
  columns: { sm: 1, md: 2, lg: 4 },
  rowHeight: 240,
  gap: 16,
  cells: [
    { id: 'hits-today' },
    { id: 'errors-today' },
    { id: 'traffic', colSpan: { md: 2, lg: 2 } },
    { id: 'errors-hour', colSpan: { md: 2, lg: 2 } },
    { id: 'errors-day' },
    { id: 'channels' },
  ],
};

export default function App() {
  const [linked, setLinked] = useState('—');

  return (
    <main>
      <Dashboard
        id="ops"
        title="Operations"
        description="Traffic, errors and sales of the web service today."
        layout={layout}
        link={{ key: 'hour' }}
        onLinkChange={(link) => setLinked(link?.value == null ? '—' : `${link.key} ${String(link.value)}`)}
      >
        <DashboardCell cell="hits-today">
          <KpiCard title="Hits today" data={hourly} valueKey="hits" value={886} unit="thousand hits" delta={4.2} />
        </DashboardCell>
        <DashboardCell cell="errors-today">
          <KpiCard title="Errors today" data={hourly} valueKey="errors" value={103} unit="errors" delta={-12} />
        </DashboardCell>
        <DashboardCell cell="traffic">
          <LineChart title="Hits per hour" data={hourly} xKey="hour" valueKey="hits" footerLeft="Thousands" />
        </DashboardCell>
        <DashboardCell cell="errors-hour">
          <BarChart title="Errors per hour" data={hourly} xKey="hour" valueKey="errors" />
        </DashboardCell>
        <DashboardCell cell="errors-day">
          <HeatmapChart
            title="Errors by day"
            data={errorsByDay}
            labelKey="day"
            valuesKey="values"
            columnLabels={blocks}
            scaleMax={40}
          />
        </DashboardCell>
        <DashboardCell cell="channels">
          <DonutChart title="Sales by channel" data={sales} nameKey="channel" valueKey="sales" centerLabel="thousand EUR" />
        </DashboardCell>
      </Dashboard>
      <p>Linked: {linked}</p>
    </main>
  );
}
```

Con `npm run dev` verás el panel de la imagen. El resto del artículo explica sus piezas.

## El panel y su nombre

`Dashboard` necesita dos cosas: un `id` y un nombre, `title` o `label`. En React y Vue, el tipo no deja omitirlos.

| Prop | Qué hace | Por defecto |
|---|---|---|
| `id` | El identificador estable del panel | Obligatorio |
| `title` | El título visible, que también nombra la región | `title` o `label`, obligatorio |
| `label` | El nombre accesible, cuando no quieres título visible | |
| `description` | Una descripción larga de la región | |
| `headingLevel` | El nivel del encabezado del título | 2 |
| `layout` | La distribución, como datos | Una celda por hijo |
| `link` | El campo que enlaza los gráficos | Sin enlace |
| `ssrWidth` | El ancho supuesto al renderizar en el servidor | 1200 |

El panel se dibuja como un `<section>` con un `<h2>` que lo nombra. Cada gráfico sin `id` propio recibe uno derivado del panel y de su celda: el de los errores por hora es `ops--errors-hour`. Como el trazo a mano sale de esa semilla, un `id` estable para el panel deja estable el dibujo de todos sus gráficos.

## La distribución es un dato

`layout` es un objeto sin funciones ni componentes, que se puede guardar en un JSON o enviar desde un servidor:

| Campo | Qué hace | Por defecto |
|---|---|---|
| `columns` | Las columnas de cada tamaño | `{ sm: 1, md: 2, lg: 4 }` |
| `rowHeight` | El alto de una fila en píxeles, con el marco de la tarjeta incluido | 240 |
| `gap` | La separación entre celdas en píxeles | 16 |
| `cells` | Las celdas, en orden de lectura | Una celda por hijo, de una columna |

Y cada celda:

| Campo | Qué hace | Por defecto |
|---|---|---|
| `id` | El nombre que usa `DashboardCell` | Obligatorio |
| `colSpan` | Las columnas que ocupa | 1 |
| `rowSpan` | Las filas que ocupa | 1 |

Los tamaños no dependen de la ventana del navegador, sino del ancho del propio panel. Un panel dentro de una barra lateral es estrecho aunque la pantalla sea grande.

| Tamaño | Ancho del panel | Columnas en este panel |
|---|---|---|
| `sm` | Menos de 640 px | 1 |
| `md` | De 640 a 1023 px | 2 |
| `lg` | 1024 px o más | 4 |

`colSpan` y `rowSpan` aceptan un número, que vale para los tres tamaños, o un objeto por tamaño. El tráfico y los errores por hora ocupan `{ md: 2, lg: 2 }`: dos columnas en tableta y en escritorio, y una en móvil, donde no hay más. Si escribes `colSpan: 2` a secas, en `sm` la celda pide dos columnas donde solo hay una: el panel la recorta a una y, en desarrollo, avisa con `SP014`.

Estas son las celdas medidas en el navegador con el panel de este artículo:

| Ancho del panel | Columnas | Cómo quedan las celdas |
|---|---|---|
| 1336 px | 4 | Dos filas: los indicadores y el tráfico; los errores por hora, los errores por día y las ventas |
| 836 px | 2 | Cuatro filas: los indicadores; el tráfico; los errores por hora; los errores por día y las ventas |
| 436 px | 1 | Seis filas, una celda en cada una, en el mismo orden |

Las celdas nunca se reordenan: el orden de `cells` es el orden de lectura en todos los tamaños. Una celda ancha que no cabe en lo que queda de fila pasa a la siguiente y deja un hueco al final. Para evitarlo, haz que las celdas de cada fila sumen las columnas del tamaño, como aquí: 1 + 1 + 2 y 2 + 1 + 1.

## Cada gráfico en su celda

`DashboardCell` pone un gráfico en la celda cuyo `id` coincide con su `cell`. En React, el gráfico tiene que ser el hijo directo de `DashboardCell`, porque el panel le pasa el tamaño como props.

El gráfico toma el ancho y el alto de la celda, salvo que fije los suyos con `width` y `height`. Con el panel a 1336 px, cada celda de una columna mide 314 × 240 px, y la de dos columnas, 644 × 240 px.

Si el panel y sus hijos no coinciden, el panel sigue funcionando, pero avisa en desarrollo con `SP015`: un hijo que nombra una celda que la distribución no declara se coloca al final con una columna, y una celda de la distribución sin hijo se descarta.

El panel también reparte el estilo, como anunció el artículo 12. `ground`, `substrate`, `mode`, `locale` y `palette` puestos en `Dashboard` pasan a todos sus gráficos. Cada campo se resuelve en el orden del [artículo 09](/blog/silverpoint_serie_9), y gana el primero que lo declara: la prop del propio gráfico, el panel que lo contiene, el proveedor más cercano y el valor por defecto de la librería. Con `substrate="green"` en el panel y `substrate="ochre"` en los errores por hora, cinco gráficos se dibujan en verde y uno en ocre.

## Gráficos enlazados

Con `link={{ key: 'hour' }}`, explorar un gráfico marca en los demás los elementos con el mismo valor de `hour`. Es lo que muestra la imagen: el puntero está en la hora 11 del tráfico, y la hora 11 se marca en las barras de errores y en las curvas de los dos indicadores, cuyas filas también tienen `hour`.

`onLinkChange` recibe `{ key, value }` cuando cambia el valor enlazado, y `null` cuando se borra. Los errores por día y las ventas por canal no tienen el campo `hour`: no muestran marca y, en desarrollo, avisan una vez con `SP016`. Es lo esperado en un panel que mezcla datos por hora con otros que no lo son. Cuando el foco está en uno de esos gráficos, `onLinkChange` recibe `hour` con el valor `undefined`, y por eso el ejemplo comprueba `link?.value == null`.

Las marcas enlazadas son solo visuales. El lector de pantalla anuncia el elemento del gráfico que tiene el foco, no los de los demás.

## El teclado

El panel no añade paradas de tabulación propias. `Tab` recorre los gráficos en el orden de `cells`, el mismo en los tres tamaños, y al entrar en cada gráfico se activa su primer elemento. Dentro, las flechas recorren los elementos, como en cualquier gráfico. En este panel, el recorrido es: los dos indicadores, el tráfico, los errores por hora, los errores por día y las ventas.

## El panel en Vue

El mismo panel, con `SpDashboard`, `SpDashboardCell` y el evento `@link-change`. Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpBarChart } from '@silverpoint/vue/bar-chart';
import { SpDashboard, SpDashboardCell, type DashboardLayout } from '@silverpoint/vue/dashboard';
import { SpDonutChart } from '@silverpoint/vue/donut-chart';
import { SpHeatmapChart } from '@silverpoint/vue/heatmap-chart';
import { SpKpiCard } from '@silverpoint/vue/kpi-card';
import { SpLineChart } from '@silverpoint/vue/line-chart';
import { blocks, errorsByDay, hourly, sales } from './ops';

const layout: DashboardLayout = {
  columns: { sm: 1, md: 2, lg: 4 },
  rowHeight: 240,
  gap: 16,
  cells: [
    { id: 'hits-today' },
    { id: 'errors-today' },
    { id: 'traffic', colSpan: { md: 2, lg: 2 } },
    { id: 'errors-hour', colSpan: { md: 2, lg: 2 } },
    { id: 'errors-day' },
    { id: 'channels' },
  ],
};

const linked = ref('—');

function onLinkChange(link: { key: string; value: unknown } | null) {
  linked.value = link?.value == null ? '—' : `${link.key} ${String(link.value)}`;
}
</script>

<template>
  <main>
    <SpDashboard
      id="ops"
      title="Operations"
      description="Traffic, errors and sales of the web service today."
      :layout="layout"
      :link="{ key: 'hour' }"
      @link-change="onLinkChange"
    >
      <SpDashboardCell cell="hits-today">
        <SpKpiCard title="Hits today" :data="hourly" value-key="hits" :value="886" unit="thousand hits" :delta="4.2" />
      </SpDashboardCell>
      <SpDashboardCell cell="errors-today">
        <SpKpiCard title="Errors today" :data="hourly" value-key="errors" :value="103" unit="errors" :delta="-12" />
      </SpDashboardCell>
      <SpDashboardCell cell="traffic">
        <SpLineChart title="Hits per hour" :data="hourly" x-key="hour" value-key="hits" footer-left="Thousands" />
      </SpDashboardCell>
      <SpDashboardCell cell="errors-hour">
        <SpBarChart title="Errors per hour" :data="hourly" x-key="hour" value-key="errors" />
      </SpDashboardCell>
      <SpDashboardCell cell="errors-day">
        <SpHeatmapChart
          title="Errors by day"
          :data="errorsByDay"
          label-key="day"
          values-key="values"
          :column-labels="blocks"
          :scale-max="40"
        />
      </SpDashboardCell>
      <SpDashboardCell cell="channels">
        <SpDonutChart title="Sales by channel" :data="sales" name-key="channel" value-key="sales" center-label="thousand EUR" />
      </SpDashboardCell>
    </SpDashboard>
    <p>Linked: {{ linked }}</p>
  </main>
</template>
```

## El panel en Angular

En Angular el evento es la salida `(linkChange)`. Sustituye `src/app/app.ts`:

```ts
import { Component, signal } from '@angular/core';
import { SpBarChart } from '@silverpoint/angular/bar-chart';
import { SpDashboard, SpDashboardCell, type DashboardLayout } from '@silverpoint/angular/dashboard';
import { SpDonutChart } from '@silverpoint/angular/donut-chart';
import { SpHeatmapChart } from '@silverpoint/angular/heatmap-chart';
import { SpKpiCard } from '@silverpoint/angular/kpi-card';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { blocks, errorsByDay, hourly, sales } from './ops';

@Component({
  selector: 'app-root',
  imports: [SpDashboard, SpDashboardCell, SpKpiCard, SpLineChart, SpBarChart, SpHeatmapChart, SpDonutChart],
  template: `
    <main>
      <sp-dashboard
        id="ops"
        title="Operations"
        description="Traffic, errors and sales of the web service today."
        [layout]="layout"
        [link]="{ key: 'hour' }"
        (linkChange)="onLinkChange($event)"
      >
        <sp-dashboard-cell cell="hits-today">
          <sp-kpi-card title="Hits today" [data]="hourly" valueKey="hits" [value]="886" unit="thousand hits" [delta]="4.2" />
        </sp-dashboard-cell>
        <sp-dashboard-cell cell="errors-today">
          <sp-kpi-card title="Errors today" [data]="hourly" valueKey="errors" [value]="103" unit="errors" [delta]="-12" />
        </sp-dashboard-cell>
        <sp-dashboard-cell cell="traffic">
          <sp-line-chart title="Hits per hour" [data]="hourly" xKey="hour" valueKey="hits" footerLeft="Thousands" />
        </sp-dashboard-cell>
        <sp-dashboard-cell cell="errors-hour">
          <sp-bar-chart title="Errors per hour" [data]="hourly" xKey="hour" valueKey="errors" />
        </sp-dashboard-cell>
        <sp-dashboard-cell cell="errors-day">
          <sp-heatmap-chart
            title="Errors by day"
            [data]="errorsByDay"
            labelKey="day"
            valuesKey="values"
            [columnLabels]="blocks"
            [scaleMax]="40"
          />
        </sp-dashboard-cell>
        <sp-dashboard-cell cell="channels">
          <sp-donut-chart title="Sales by channel" [data]="sales" nameKey="channel" valueKey="sales" centerLabel="thousand EUR" />
        </sp-dashboard-cell>
      </sp-dashboard>
      <p>Linked: {{ linked() }}</p>
    </main>
  `,
})
export class App {
  protected readonly hourly = hourly;
  protected readonly errorsByDay = errorsByDay;
  protected readonly blocks = blocks;
  protected readonly sales = sales;
  protected readonly linked = signal('—');

  protected readonly layout: DashboardLayout = {
    columns: { sm: 1, md: 2, lg: 4 },
    rowHeight: 240,
    gap: 16,
    cells: [
      { id: 'hits-today' },
      { id: 'errors-today' },
      { id: 'traffic', colSpan: { md: 2, lg: 2 } },
      { id: 'errors-hour', colSpan: { md: 2, lg: 2 } },
      { id: 'errors-day' },
      { id: 'channels' },
    ],
  };

  protected onLinkChange(link: { key: string; value: unknown } | null) {
    this.linked.set(link?.value == null ? '—' : `${link.key} ${String(link.value)}`);
  }
}
```

## El panel en Reflex

En Reflex los datos pasan a Python. `ops_panel/ops.py`:

```python
HOURLY = [
    {"hour": "00", "hits": 18, "errors": 2},
    {"hour": "01", "hits": 14, "errors": 1},
    {"hour": "02", "hits": 11, "errors": 1},
    {"hour": "03", "hits": 9, "errors": 0},
    {"hour": "04", "hits": 11, "errors": 1},
    {"hour": "05", "hits": 16, "errors": 1},
    {"hour": "06", "hits": 24, "errors": 2},
    {"hour": "07", "hits": 33, "errors": 4},
    {"hour": "08", "hits": 42, "errors": 6},
    {"hour": "09", "hits": 51, "errors": 7},
    {"hour": "10", "hits": 58, "errors": 9},
    {"hour": "11", "hits": 62, "errors": 8},
    {"hour": "12", "hits": 64, "errors": 11},
    {"hour": "13", "hits": 61, "errors": 9},
    {"hour": "14", "hits": 59, "errors": 7},
    {"hour": "15", "hits": 58, "errors": 6},
    {"hour": "16", "hits": 57, "errors": 6},
    {"hour": "17", "hits": 52, "errors": 5},
    {"hour": "18", "hits": 47, "errors": 4},
    {"hour": "19", "hits": 41, "errors": 4},
    {"hour": "20", "hits": 30, "errors": 3},
    {"hour": "21", "hits": 26, "errors": 2},
    {"hour": "22", "hits": 22, "errors": 2},
    {"hour": "23", "hits": 20, "errors": 2},
]

ERRORS_BY_DAY = [
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

Y la página, `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import (
    bar_chart,
    dashboard,
    dashboard_cell,
    dashboard_cell_layout,
    dashboard_layout,
    donut_chart,
    heatmap_chart,
    kpi_card,
    line_chart,
)

from .ops import BLOCKS, ERRORS_BY_DAY, HOURLY, SALES

LAYOUT = dashboard_layout(
    [
        "hits-today",
        "errors-today",
        dashboard_cell_layout("traffic", col_span={"md": 2, "lg": 2}),
        dashboard_cell_layout("errors-hour", col_span={"md": 2, "lg": 2}),
        "errors-day",
        "channels",
    ],
    columns={"sm": 1, "md": 2, "lg": 4},
    row_height=240,
    gap=16,
)


class PanelState(rx.State):
    linked: str = "—"

    @rx.event
    def on_link(self, link: dict | None):
        value = link.get("value") if link else None
        self.linked = "—" if value is None else f"{link['key']} {value}"


def index() -> rx.Component:
    return rx.el.main(
        dashboard(
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
                    title="Hits per hour",
                    data=HOURLY,
                    x_key="hour",
                    value_key="hits",
                    footer_left="Thousands",
                ),
                cell="traffic",
            ),
            dashboard_cell(
                bar_chart(
                    title="Errors per hour",
                    data=HOURLY,
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
            on_link_change=PanelState.on_link,
        ),
        rx.el.p("Linked: ", PanelState.linked),
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

Tres diferencias con los adaptadores de JavaScript:

* **`dashboard_layout` escribe la distribución** con nombres de Python y la entrega con los nombres que lee el componente (`colSpan`, `rowHeight`). Una cadena en la lista es una celda de una columna.
* **`link="hour"`** es la forma corta de `link={"key": "hour"}`.
* **`on_link_change` es un evento del backend.** Recibe un `dict` o `None`, y el texto «Linked» lo actualiza el estado.

Los cuatro paneles se comprobaron en el navegador con el panel a 1336, 836 y 436 px de ancho: las mismas columnas, las mismas celdas y el mismo recorrido con el teclado.

## Problemas comunes

* **`SP014` en la consola.** Una celda ocupa más columnas de las que tiene un tamaño, casi siempre por un `colSpan` numérico que también se aplica en `sm`. Escríbelo por tamaño: `{ md: 2, lg: 2 }`.
* **`SP015` en la consola.** Un `cell` no coincide con ningún `id` de `cells`, o una celda de la distribución no tiene gráfico. Revisa los nombres en los dos sitios.
* **`SP016` en la consola.** Un gráfico del panel no tiene el campo de `link`. Si es un gráfico que no debe enlazarse, como aquí, puedes ignorarlo.
* **Un gráfico no ocupa su celda en React.** Hay otro elemento entre `DashboardCell` y el gráfico. El gráfico tiene que ser su hijo directo.
* **Un hueco al final de una fila.** Una celda ancha no cabía en lo que quedaba de la fila. Ajusta los `colSpan` para que cada fila sume sus columnas.

## Lo que viene

El panel ya tiene su forma. El artículo 14 vuelve al catálogo con los gráficos de distribuciones, comparaciones e incertidumbre, y el 15 cierra el nivel 2 con jerarquías, flujos y redes.

La [guía del panel](https://silverpointweb.vercel.app/docs/dashboard) de la documentación tiene la referencia completa de sus props.
