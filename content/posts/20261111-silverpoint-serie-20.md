Title: Silverpoint, artículo 20: datos en vivo y rendimiento
Date: 2026-11-11 20:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_20
Authors: Ernesto Crespo
Summary: Un gráfico de silverpoint con datos en vivo en React, Vue, Angular y Reflex, qué se redibuja en cada actualización y cuánto cuesta: tiempos medidos, el peso de los trazos, el volumen de datos y el tamaño del paquete.

Hasta ahora, los gráficos de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) recibían sus datos una vez. Un panel de operaciones de verdad se actualiza solo: llega una lectura nueva y el gráfico se mueve. Este artículo del nivel 3 hace eso con el gráfico de visitas por hora y después mide lo que cuesta.

## Lo que vas a construir

El gráfico de visitas por hora de los artículos 03 a 06, convertido en una ventana de las últimas 24 horas que avanza sola: cada dos segundos llega la hora siguiente y sale la más antigua.

![El gráfico de visitas en vivo: a la izquierda tras una lectura, a la derecha doce lecturas después, con la ventana desplazada y el realce en el último valor](./images/silverpoint-serie-20.png)

La segunda mitad del artículo mide el gráfico: cuánto tarda una actualización, cuánto pesan sus trazos, cuántos datos admite y cuánto añade al paquete.

## Lo que necesitas

El proyecto de tu framework de los artículos 03 a 06, con las visitas por hora de su paso de datos propios: `src/traffic.ts` en React y Vue, `src/app/traffic.ts` en Angular y `ops_panel/traffic.py` en Reflex.

## 1. Una ventana que avanza

Las lecturas nuevas las simula una función. En un panel real vendrían de una API, con `fetch` cada cierto tiempo o con un `EventSource`; el resto del código no cambia.

Crea `src/live.ts` en React y Vue, o `src/app/live.ts` en Angular:

```ts
import { traffic, type HourlyTraffic } from './traffic';

// The next reading: the hour after the last one, taken from the day's
// profile with a small variation that changes from tick to tick.
export function nextReading(last: HourlyTraffic, tick: number): HourlyTraffic {
  const hour = (Number(last.hour) + 1) % 24;
  return {
    hour: String(hour).padStart(2, '0'),
    hits: traffic[hour].hits + ((tick * 7) % 9) - 4,
  };
}

// A rolling window: drop the oldest hour and append the new one.
export function advance(rows: readonly HourlyTraffic[], tick: number): HourlyTraffic[] {
  return [...rows.slice(1), nextReading(rows[rows.length - 1], tick)];
}
```

`advance` no modifica las filas que recibe: devuelve un array nuevo. Es lo que permite que React, Vue y Angular noten el cambio, como se verá en cada framework.

## 2. En React

Sustituye `src/App.tsx`:

```tsx
import { useEffect, useState } from 'react';
import { LineChart } from '@silverpoint/react/line-chart';
import { advance } from './live';
import { traffic } from './traffic';

export default function App() {
  const [rows, setRows] = useState(traffic);

  useEffect(() => {
    let tick = 0;
    const timer = setInterval(() => {
      tick += 1;
      setRows((current) => advance(current, tick));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  const last = rows[rows.length - 1];

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        id="live-hits"
        data={rows}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Live"
        value={last.hits}
        unit="k hits in the last hour"
        footerLeft="Last 24 hours"
        footerRight={`Updated at ${last.hour}:00`}
        height={200}
      />
    </main>
  );
}
```

* **El intervalo se limpia.** La función que devuelve `useEffect` detiene el intervalo cuando el componente se desmonta. En desarrollo, `StrictMode` monta el componente dos veces, y sin esa limpieza habría dos intervalos.
* **`setRows` recibe una función.** El intervalo se crea una sola vez, así que no puede leer `rows` directamente: vería siempre las filas del primer render. Con `setRows((current) => …)`, React le pasa las filas actuales.
* **El gráfico tiene un `id` fijo.** La sección «Qué se redibuja» explica por qué importa.

## 3. En Vue

Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { computed, onMounted, onUnmounted, shallowRef } from 'vue';
import { SpLineChart } from '@silverpoint/vue/line-chart';
import { advance } from './live';
import { traffic } from './traffic';

const rows = shallowRef(traffic);
const last = computed(() => rows.value[rows.value.length - 1]);

let timer: ReturnType<typeof setInterval> | undefined;

onMounted(() => {
  let tick = 0;
  timer = setInterval(() => {
    tick += 1;
    rows.value = advance(rows.value, tick);
  }, 2000);
});

onUnmounted(() => clearInterval(timer));
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart
      id="live-hits"
      :data="rows"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      badge="Live"
      :value="last.hits"
      unit="k hits in the last hour"
      footer-left="Last 24 hours"
      :footer-right="`Updated at ${last.hour}:00`"
      :height="200"
    />
  </main>
</template>
```

`shallowRef` en lugar de `ref`: el array se sustituye entero en cada lectura y nunca se modifica por dentro, así que Vue solo necesita vigilar la referencia. Con `ref`, Vue convertiría además cada fila en un objeto reactivo, un trabajo que aquí no sirve de nada.

## 4. En Angular

Sustituye `src/app/app.ts`:

```ts
import { Component, computed, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { interval } from 'rxjs';
import { advance } from './live';
import { traffic } from './traffic';

@Component({
  selector: 'app-root',
  imports: [SpLineChart],
  template: `
    <main style="max-width: 640px">
      <sp-line-chart
        id="live-hits"
        [data]="rows()"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Live"
        [value]="last().hits"
        unit="k hits in the last hour"
        footerLeft="Last 24 hours"
        [footerRight]="'Updated at ' + last().hour + ':00'"
        [height]="200"
      />
    </main>
  `,
})
export class App {
  protected readonly rows = signal(traffic);
  protected readonly last = computed(() => {
    const rows = this.rows();
    return rows[rows.length - 1];
  });

  constructor() {
    interval(2000)
      .pipe(takeUntilDestroyed())
      .subscribe((tick) => this.rows.update((current) => advance(current, tick + 1)));
  }
}
```

`interval` de RxJS emite 0, 1, 2… cada dos segundos, y `takeUntilDestroyed` cancela la suscripción cuando el componente se destruye. `rows.update` sustituye el signal por el array nuevo, `last` se recalcula y los inputs del gráfico cambian. Como en el [artículo 05](/blog/silverpoint_serie_5), no hace falta zone.js: los componentes de silverpoint redibujan siguiendo a los signals.

## 5. En Reflex

En Reflex, las lecturas llegan al estado en el backend y Reflex envía el cambio al navegador. Crea `ops_panel/live.py`, la misma ventana en Python:

```python
from .traffic import TRAFFIC


def next_reading(last: dict, tick: int) -> dict:
    """The hour after the last one, from the day's profile with a small variation."""
    hour = (int(last["hour"]) + 1) % 24
    return {"hour": f"{hour:02d}", "hits": TRAFFIC[hour]["hits"] + (tick * 7) % 9 - 4}


def advance(rows: list[dict], tick: int) -> list[dict]:
    """A rolling window: drop the oldest hour and append the new one."""
    return [*rows[1:], next_reading(rows[-1], tick)]
```

Y sustituye `ops_panel/ops_panel.py`:

```python
import asyncio

import reflex as rx
from reflex_silverpoint_react import line_chart

from .live import advance
from .traffic import TRAFFIC


class LiveState(rx.State):
    rows: list[dict[str, str | int]] = TRAFFIC

    @rx.var
    def last(self) -> dict[str, str | int]:
        return self.rows[-1]

    @rx.event(background=True)
    async def stream(self):
        tick = 0
        while True:
            await asyncio.sleep(2)
            tick += 1
            async with self:
                self.rows = advance(self.rows, tick)


def index() -> rx.Component:
    return rx.box(
        line_chart(
            id="live-hits",
            data=LiveState.rows,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            badge="Live",
            value=LiveState.last["hits"],
            unit="k hits in the last hour",
            footer_left="Last 24 hours",
            footer_right=f"Updated at {LiveState.last['hour']}:00",
            height=200,
        ),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index, on_load=LiveState.stream)
```

`stream` es una tarea en segundo plano: `@rx.event(background=True)` la deja correr sin bloquear los demás eventos, y solo puede modificar el estado dentro de `async with self`, que toma el estado en exclusiva el tiempo justo de escribir las filas nuevas.

¿Qué pasa con el bucle `while True` cuando el usuario se va? La tarea arranca con `on_load`, y en Reflex 0.10.1 eso la ata a la carga de la página. Lo comprobé con el servidor en marcha: al cerrar la pestaña, Reflex cancela la tarea, y al recargar, la carga nueva cancela la anterior, de modo que nunca corren dos. Una tarea que lanzas de otra forma, con un botón por ejemplo, no se cancela sola; la [documentación de Reflex](https://reflex.dev/docs/events/background-events/) explica cómo detenerla.

## Qué se redibuja

Con cada lectura nueva, el gráfico vuelve a calcular todo lo que dibuja: escalas, ejes, la curva y su entintado. No hay una animación de transición entre la ventana vieja y la nueva: el gráfico pasa de una a otra en un solo paso.

Lo que no cambia es el elemento. En los cuatro frameworks medí que el `<svg>` del gráfico es el mismo nodo antes y después de cada actualización; solo cambian sus trazos. Por eso la animación de entrada, que descubre el gráfico de izquierda a derecha en 280 ms, se ve una sola vez, al montarlo, y no en cada lectura. Con `prefers-reduced-motion: reduce` no se ve nunca, como explicó el [artículo 10](/blog/silverpoint_serie_10).

El realce sigue al dato: siempre marca el último punto, el valor vivo.

### El `id` y el trazo a mano

El temblor de la línea no es aleatorio en cada render: sale de una semilla, y la semilla sale del `id`. Lo medí comparando los trazos:

| Render | Trazos |
|---|---|
| El mismo `id` y los mismos datos | Idénticos |
| Otro `id` y los mismos datos | Distintos |

Por eso un gráfico en vivo debe tener un `id` fijo. Si lo generas en cada render, por ejemplo con la hora actual, la línea temblaría distinta en cada lectura aunque los datos fueran iguales. El [artículo 19](/blog/silverpoint_serie_19) vuelve sobre esto, porque el render en servidor depende de lo mismo.

Un dato curioso de las pruebas: con el mismo ancho, React, Vue y Angular dibujaron exactamente los mismos trazos en cada lectura. El motor es el mismo, y la semilla también.

## Lo que cuesta

Para medir, monté una página de pruebas con la versión de producción de React y medí con `performance.now()` cada actualización completa: el render de React, la geometría y el entintado de silverpoint y la escritura en el DOM. Cada cifra es la mediana de 15 a 30 actualizaciones, en tres ejecuciones. Son números de mi máquina, un portátil con un AMD Ryzen AI 9 HX PRO 370 y Chrome 157 sin interfaz; en la tuya serán otros, pero las proporciones se mantienen.

| Gráfico | Actualización | Trazos (`d`) |
|---|---|---|
| Línea, 24 puntos | 1,4 a 1,9 ms | 1,9 KB |
| Línea, 500 puntos | 6,5 a 6,7 ms | 20,9 KB |
| Línea, 1440 puntos | 15 a 20 ms | 58,3 KB |
| Barras, 24 barras, `hatchFill="tile"` | 1,8 a 2,3 ms | 8,1 KB |
| Barras, 24 barras, `hatchFill="per-shape"` | 5,6 a 5,9 ms | 25,0 KB |
| Área, 24 puntos, `hatchFill="tile"` | 1,5 a 2,3 ms | 5,6 KB |
| Área, 24 puntos, `hatchFill="per-shape"` | 2,5 a 2,8 ms | 10,3 KB |

Tres lecturas de la tabla:

* **Un gráfico normal cabe de sobra en un fotograma.** A 60 imágenes por segundo, cada fotograma dura unos 16 ms. El gráfico del panel se actualiza en menos de 2 ms.
* **El rellenado por figura es caro.** Con `hatchFill="per-shape"`, cada barra lleva su propio tramado: el peso de los trazos se multiplica por tres y el tiempo por más de dos. El valor por defecto, `tile`, comparte una trama por nivel de tono.
* **El volumen se nota.** Con 1440 puntos, una actualización ya no cabe en un fotograma y los trazos pasan de 40 KB.

### Los dos avisos

Silverpoint vigila esos dos límites y, en desarrollo, avisa en la consola:

| Aviso | Cuándo | Lo que vi con 1440 puntos |
|---|---|---|
| `SP008` | Una serie pasa de 500 puntos | «1440 points; the ceiling is 500 per series. Aggregate the data before charting it.» |
| `SP011` | Los trazos de un gráfico pasan de 40 KB | «58331 bytes of path data. Use `hatchFill: 'tile'` or a larger hatch gap.» |

`SP011` sugiere `hatchFill`, porque el tramado es la causa más común. En un gráfico de línea no hay tramado: la causa es el número de puntos, y la solución es la de `SP008`. Los 40 KB importan también fuera del navegador: un gráfico renderizado en el servidor viaja con todos sus trazos dentro del HTML.

## Agrega antes de dibujar

Si tu API da una lectura por minuto, son 1440 filas al día. Una línea de 640 píxeles no puede mostrar 1440 valores distintos: cada punto tendría menos de medio píxel. Agrégalos antes de pasárselos al gráfico. En TypeScript:

```ts
import type { HourlyTraffic } from './traffic';

export type MinuteReading = { minute: string; requests: number };

// 1,440 readings a minute become 24 rows an hour, in thousands of requests.
export function perHour(readings: readonly MinuteReading[]): HourlyTraffic[] {
  const totals = new Map<string, number>();
  for (const { minute, requests } of readings) {
    const hour = minute.slice(0, 2);
    totals.set(hour, (totals.get(hour) ?? 0) + requests);
  }
  return [...totals].map(([hour, requests]) => ({ hour, hits: Math.round(requests / 1000) }));
}
```

Y en Python, para Reflex:

```python
from collections import defaultdict


def per_hour(readings: list[dict]) -> list[dict]:
    """1,440 readings a minute become 24 rows an hour, in thousands of requests."""
    totals: dict[str, int] = defaultdict(int)
    for reading in readings:
        totals[reading["minute"][:2]] += reading["requests"]
    return [
        {"hour": hour, "hits": round(total / 1000)} for hour, total in totals.items()
    ]
```

Las dos funciones convierten las 1440 lecturas por minuto en las 24 filas por hora del panel. En Reflex, agregar en el backend tiene una ventaja más: al navegador solo viajan 24 filas en cada actualización, no 1440.

## El tamaño del paquete

Cada gráfico se importa desde su propia ruta, como `@silverpoint/react/line-chart`. El paquete también tiene una entrada general, `@silverpoint/react`, con todos los gráficos. Medí la versión de producción de la aplicación de React de este artículo con Vite:

| La aplicación | JavaScript | Con gzip |
|---|---|---|
| Sin gráfico, solo React y el intervalo | 220,3 kB | 68,9 kB |
| Con `LineChart` desde `@silverpoint/react/line-chart` | 316,6 kB | 101,5 kB |
| Con `LineChart` desde `@silverpoint/react` | 316,6 kB | 101,5 kB |
| Con `LineChart` y `BarChart`, cada uno desde su ruta | 320,6 kB | 102,7 kB |

El primer gráfico añade unos 33 kB comprimidos: el motor, el estilo base, el entintado y el gráfico. El segundo añade poco más de 1 kB, porque comparte todo lo demás.

En producción, la entrada general y la ruta propia dan exactamente el mismo paquete: Vite descarta los gráficos que no usas. La diferencia está en desarrollo. Con la entrada general, el servidor de desarrollo carga el código de todos los gráficos: en mi prueba, unos 1,5 MB más en cada carga de la página. Importar cada gráfico desde su ruta mantiene el desarrollo ligero y no depende de que tu empaquetador descarte bien lo que sobra.

## Medirlo en tu aplicación

Para medir una actualización en tu propio código, marca el principio y el final con la API de rendimiento del navegador. En React, `flushSync` hace que la actualización ocurra entera dentro de la medida:

```tsx
  useEffect(() => {
    let tick = 0;
    const timer = setInterval(() => {
      tick += 1;
      performance.mark('update-start');
      flushSync(() => setRows((current) => advance(current, tick)));
      performance.measure('chart update', 'update-start');
    }, 2000);
    return () => clearInterval(timer);
  }, []);
```

Importa `flushSync` de `react-dom`. Cada medida aparece en la sección de tiempos del panel de rendimiento de las herramientas del navegador, y también en la consola:

```js
performance.getEntriesByName('chart update').map((entry) => entry.duration);
```

En mi máquina, esta aplicación dio entre 1,6 y 3,2 ms por actualización. Quita `flushSync` cuando termines: obliga a React a actualizar de forma síncrona, y solo sirve para que la medida sea completa. En Vue, Angular y Reflex, el panel de rendimiento del navegador da la misma información sin tocar el código.

## Problemas comunes

* **El gráfico no se mueve.** El array se modificó por dentro, con `push` o `shift`, en lugar de sustituirse. React, `shallowRef` y los signals comparan la referencia: si es la misma, no hay cambio. Devuelve siempre un array nuevo, como `advance`.
* **La línea tiembla distinta en cada lectura.** El `id` del gráfico cambia en cada render. Dale un `id` fijo.
* **En desarrollo, el gráfico avanza dos horas en cada lectura.** Hay dos intervalos: falta la limpieza del intervalo en `useEffect` o en `onUnmounted`.
* **La consola muestra `SP008` o `SP011`.** Hay demasiados puntos o demasiado tramado. Agrega los datos o vuelve a `hatchFill="tile"`.

## Lo que viene

El panel ya se actualiza solo y sabes cuánto cuesta cada gráfico. El [artículo 21](/blog/silverpoint_serie_21) cambia de tipo de dato: líneas de tiempo con TimelineJS, dibujadas en el estilo de silverpoint, como la de las certificaciones de este mismo sitio.
