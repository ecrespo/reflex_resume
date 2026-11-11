Title: Silverpoint, artículo 18: exportar un gráfico a SVG
Date: 2026-11-11 19:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_18
Authors: Ernesto Crespo
Summary: Cómo sacar un gráfico de silverpoint de la página como un archivo SVG: el manejador con toSVGString(), un botón de descarga, qué contiene el SVG, por qué hay que añadirle la hoja de estilos del estilo base para que se vea fuera de la aplicación, y el mismo botón en React, Vue, Angular y Reflex.

Un gráfico del panel de operaciones vive dentro de la página. A veces hay que sacarlo: pegarlo en un informe, en una presentación o en un correo. Este artículo de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) añade al gráfico de tráfico un botón que lo descarga como un archivo SVG.

Cada gráfico es ya un SVG, así que exportarlo no exige dibujarlo otra vez. Lo que hay que saber es qué lleva ese SVG y qué no lleva, porque fuera de la aplicación no tiene la hoja de estilos de la página.

## El manejador del gráfico

Cada gráfico expone un manejador con dos métodos:

| Método | Qué devuelve |
|---|---|
| `toSVGString()` | El SVG del gráfico tal como está dibujado, como texto |
| `getGeometry()` | La geometría del dibujo: `viewBox`, trazos, textos y áreas activas |

La forma de los objetos que devuelve `getGeometry()` es interna: la especificación de la librería avisa de que puede cambiar en una versión menor. Para exportar basta `toSVGString()`.

Cómo se llega al manejador depende del framework:

| Framework | Cómo se obtiene |
|---|---|
| React | `ref` con el tipo `ChartHandle` |
| Vue | Una referencia de plantilla, `InstanceType<typeof SpLineChart>` |
| Angular | `viewChild.required<SpLineChart>('chart')`; el componente tiene los dos métodos |
| Reflex | `get_svg` y `download_svg`, que lo llaman en el navegador |

## Un botón de descarga en React

El punto de partida es la aplicación de React del [artículo 03](/blog/silverpoint_serie_3), con las filas por hora en `src/traffic.ts`. Una función descarga un texto como archivo: crea un `Blob`, le da una URL temporal y hace clic en un enlace con `download`. `src/download.ts`:

```ts
export function downloadSvg(svg: string, filename: string) {
  const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
```

Y la página, `src/App.tsx`:

```tsx
import { useRef } from 'react';
import { LineChart, type ChartHandle } from '@silverpoint/react/line-chart';
import { downloadSvg } from './download';
import { traffic } from './traffic';

export default function App() {
  const chart = useRef<ChartHandle>(null);

  const exportChart = () => {
    const svg = chart.current?.toSVGString();
    if (svg) downloadSvg(svg, 'hits-per-hour.svg');
  };

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        ref={chart}
        id="hits"
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        height={200}
      />
      <button type="button" onClick={exportChart}>
        Download SVG
      </button>
    </main>
  );
}
```

`ref={chart}` deja el manejador en `chart.current`. Al pulsar «Download SVG», el navegador guarda `hits-per-hour.svg`.

## El problema: el archivo sale negro

Abre ese archivo en el navegador, sin la aplicación, y verás un bloque negro con letras de sistema. A la izquierda de la imagen está ese archivo; a la derecha, el mismo después del arreglo de la sección siguiente:

![El SVG exportado abierto solo: a la izquierda tal como sale de toSVGString(), relleno de negro; a la derecha con la hoja de estilos del estilo base dentro, igual que en la página](./images/silverpoint-serie-18.png)

La razón está en lo que contiene. El SVG no lleva colores: cada trazo tiene un atributo `part` y los colores salen de la hoja de estilos del estilo base, `@silverpoint/grounds/styles.css`, a través de variables CSS. En la página esa hoja está cargada. Fuera de ella, el SVG cae en los valores por defecto del navegador: relleno negro y la fuente del sistema.

La documentación de la exportación y la de `download_svg` en Reflex dicen que el SVG lleva sus propios colores. Con silverpoint 0.9.2 no es así: lo comprobé en los cuatro frameworks, y el archivo sale igual de negro en todos.

## El arreglo: la hoja de estilos dentro del SVG

La hoja de estilos del estilo base está preparada para esto: sus reglas también se aplican a un `<svg>` suelto, sin la página alrededor. Basta con meterla dentro del propio SVG, justo después de la etiqueta de apertura. `src/standalone.ts`:

```ts
import groundCss from '@silverpoint/grounds/styles.css?raw';

export function standaloneSvg(svg: string): string {
  const open = svg.indexOf('>') + 1;
  return `${svg.slice(0, open)}<style><![CDATA[${groundCss}]]></style>${svg.slice(open)}`;
}
```

Dos detalles:

* **`?raw`** es la forma de Vite de importar un archivo como texto. La hoja ocupa unos 11,7 kB y queda dentro del bundle de la aplicación.
* **`<![CDATA[…]]>`** es obligatorio. La hoja tiene un comentario que contiene `<svg>`, y sin `CDATA` el archivo deja de ser XML válido: el navegador muestra un error en lugar del gráfico.

La función de descarga pasa por `standaloneSvg` antes de crear el `Blob`. `src/download.ts` queda así:

```ts
import { standaloneSvg } from './standalone';

export function downloadSvg(svg: string, filename: string) {
  const file = new Blob([standaloneSvg(svg)], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(file);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
```

`App.tsx` no cambia. Ahora el archivo descargado, abierto solo, se ve como la mitad derecha de la imagen. Es lo mismo que hace la herramienta `render_chart` del servidor MCP de silverpoint, que veremos en el artículo 28: pone la hoja del estilo base en la raíz del `<svg>`.

## Qué contiene el SVG

Estas son las partes del archivo, abierto en un editor:

| Parte | Qué es |
|---|---|
| `<svg viewBox width height>` | El tamaño medido en la página: 640 × 260 px aquí, 200 de área de dibujo más la tarjeta |
| `class` y `data-substrate` | El estilo base y el sustrato, `sp-ground-silverpoint` y `cream` |
| `role="img"` y `aria-labelledby` | El nombre accesible, que apunta a `<title>` y `<desc>` |
| `<title>` y `<desc>` | El título y la descripción que el gráfico genera con sus datos |
| `<defs>` | Los patrones del tramado |
| `<path part data-role>` | Los trazos: el marco, la cuadrícula, la línea y sus puntos |
| `<text part>` | Los textos: título, etiqueta y marcas de los ejes |
| `<style>` | La hoja del estilo base, después del arreglo |

Es la tarjeta completa, con el título, la etiqueta «Today» y el marco.

Y esto es lo que no lleva:

* **La tabla de datos.** La tabla oculta para lectores de pantalla está fuera del SVG. El archivo conserva el nombre y la descripción.
* **La fuente.** Las letras piden EB Garamond. Si el equipo que abre el archivo no la tiene, usa la siguiente de la lista: Iowan Old Style o Georgia.
* **La animación de entrada.** Va en la hoja de estilos, así que el archivo la repite al abrirse. Si haces una captura nada más abrirlo, puede salir a medio dibujar.

Una paleta propia sí viaja. Si el gráfico tiene `palette`, o la recibe del proveedor, el SVG la escribe como variables en el atributo `style` de la raíz, y la hoja del estilo base las usa.

El tamaño del archivo es el del gráfico en la página. Si quieres otro tamaño en el archivo, fija `width` y `height` en el gráfico. Con el arreglo, el archivo de este ejemplo pasa de 4,5 kB a 15,3 kB.

## En Vue

El mismo botón, con una referencia de plantilla. `src/standalone.ts` y `src/download.ts` son los de React. `src/App.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpLineChart } from '@silverpoint/vue/line-chart';
import { downloadSvg } from './download';
import { traffic } from './traffic';

const chart = ref<InstanceType<typeof SpLineChart>>();

function exportChart() {
  const svg = chart.value?.toSVGString();
  if (svg) downloadSvg(svg, 'hits-per-hour.svg');
}
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart
      ref="chart"
      id="hits"
      :data="traffic"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      badge="Today"
      :height="200"
    />
    <button type="button" @click="exportChart">Download SVG</button>
  </main>
</template>
```

`ref="chart"` enlaza la referencia `chart` con el componente, y `InstanceType<typeof SpLineChart>` le da el tipo con `toSVGString()`.

## En Angular

Angular no entiende `?raw`. Su forma de importar un archivo como texto es el atributo de importación `loader: 'text'`. `src/app/standalone.ts`:

```ts
import groundCss from '@silverpoint/grounds/styles.css' with { loader: 'text' };

export function standaloneSvg(svg: string): string {
  const open = svg.indexOf('>') + 1;
  return `${svg.slice(0, open)}<style><![CDATA[${groundCss}]]></style>${svg.slice(open)}`;
}
```

TypeScript no sabe qué tipo tiene un `.css` importado así, y `ng build` falla con `TS2307`. Lo resuelve una declaración, `src/text-imports.d.ts`:

```ts
declare module '*.css' {
  const text: string;
  export default text;
}
```

Con eso `ng build` funciona, pero `ng serve` no: su servidor de desarrollo preempaqueta `@silverpoint/grounds`, y la página queda en blanco con «does not provide an export named 'default'» en la consola. Lo evita desactivar el preempaquetado en `angular.json`, en `projects` → `architect` → `serve`:

```json
"options": {
  "prebundle": false
}
```

Es un fallo abierto como [silverpoint#19](https://github.com/ecrespo/silverpoint/issues/19). Se corregirá en una próxima versión del paquete.

`src/app/download.ts` es el de React. Y el componente, `src/app/app.ts`:

```ts
import { Component, viewChild } from '@angular/core';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { downloadSvg } from './download';
import { traffic } from './traffic';

@Component({
  selector: 'app-root',
  imports: [SpLineChart],
  template: `
    <main style="max-width: 640px">
      <sp-line-chart
        #chart
        id="hits"
        [data]="traffic"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        [height]="200"
      />
      <button type="button" (click)="exportChart()">Download SVG</button>
    </main>
  `,
})
export class App {
  protected readonly traffic = traffic;
  private readonly chart = viewChild.required<SpLineChart>('chart');

  protected exportChart() {
    downloadSvg(this.chart().toSVGString(), 'hits-per-hour.svg');
  }
}
```

`#chart` marca el gráfico, y `viewChild.required` lo devuelve como `SpLineChart`, el componente con `toSVGString()` y `getGeometry()`.

## En Reflex

Reflex trae dos ayudas para esto en `reflex_silverpoint_react`:

| Función | Qué hace |
|---|---|
| `download_svg(id, filename)` | Llama a `toSVGString()` en el navegador y descarga el archivo |
| `get_svg(id, handler)` | Llama a `toSVGString()` y envía el texto a un evento del backend |

Las dos buscan el gráfico por su `id`, así que el gráfico necesita uno. `download_svg` es lo más corto:

```python
import reflex as rx
from reflex_silverpoint_react import download_svg, line_chart

from .traffic import TRAFFIC


def index() -> rx.Component:
    return rx.box(
        line_chart(
            id="hits",
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            badge="Today",
            height=200,
        ),
        rx.el.button(
            "Download SVG",
            type="button",
            on_click=download_svg("hits", "hits-per-hour.svg"),
        ),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

Descarga el mismo SVG que los otros tres, sin la hoja de estilos: también sale negro fuera de la aplicación. Para añadirla, `get_svg` manda el SVG al backend, que la inserta y devuelve el archivo con `rx.download`. La hoja va copiada en el proyecto, en `data/silverpoint-grounds.css`, desde `.web/node_modules/@silverpoint/grounds/dist/styles.css`. Cópiala otra vez cuando actualices el paquete. `ops_panel/ops_panel.py`:

```python
from pathlib import Path

import reflex as rx
from reflex_silverpoint_react import get_svg, line_chart

from .traffic import TRAFFIC

GROUND_CSS = Path("data/silverpoint-grounds.css")


class ExportState(rx.State):
    @rx.event
    def save_svg(self, svg: str | None):
        if not svg:
            return
        css = GROUND_CSS.read_text()
        start = svg.index(">") + 1
        standalone = f"{svg[:start]}<style><![CDATA[{css}]]></style>{svg[start:]}"
        return rx.download(data=standalone, filename="hits-per-hour.svg")


def index() -> rx.Component:
    return rx.box(
        line_chart(
            id="hits",
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            badge="Today",
            height=200,
        ),
        rx.el.button(
            "Download SVG",
            type="button",
            on_click=get_svg("hits", ExportState.save_svg),
        ),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

El SVG viaja al backend y vuelve, unos 4,5 kB de ida y 15 kB de vuelta. Para un botón de descarga no importa.

Una diferencia de tamaño: en Reflex el gráfico mide 576 px de ancho, porque `max_width="640px"` incluye los 32 px de `padding` a cada lado. El archivo sale de 576 × 260.

Los cuatro archivos se comprobaron con Chrome sin interfaz: React, Vue y Angular descargan exactamente los mismos bytes, y el de Reflex es el mismo gráfico a 576 px. Abiertos solos, sin la hoja se ven negros y con ella se ven como en la página.

## Sin navegador

`toSVGString()` necesita el gráfico montado en una página. Para generar SVG en un servidor o en un script hay dos caminos: los gráficos de servidor de React, que son el tema del artículo siguiente, y la herramienta `render_chart` del servidor MCP. Por dentro, los adaptadores usan funciones del paquete `@silverpoint/grounds` que también funcionan sin DOM, pero la especificación no las incluye en la API pública: pueden cambiar sin aviso.

## Problemas comunes

* **El archivo se ve negro.** Le falta la hoja de estilos del estilo base. Añádela con `standaloneSvg`.
* **El navegador muestra un error de XML al abrirlo.** La hoja está dentro de `<style>` sin `CDATA`.
* **`toSVGString` es `undefined`.** El manejador aún no existe: el gráfico no se ha montado, o en Reflex el `id` de `get_svg` no coincide con el del gráfico.
* **`TS2307` en Angular.** Falta la declaración de `src/text-imports.d.ts`.
* **Con `ng serve`, la página queda en blanco.** Falta `"prebundle": false` en `angular.json` ([silverpoint#19](https://github.com/ecrespo/silverpoint/issues/19)).
* **El texto cambia de forma en otro equipo.** El SVG no lleva la fuente. Si la forma de las letras importa, convierte el archivo a PNG o PDF en un equipo que tenga EB Garamond.

## Lo que viene

El [artículo 19](/blog/silverpoint_serie_19) lleva el dibujo al servidor: los gráficos de servidor de React, el render en Vue y Angular, y por qué el mismo `id` da el mismo dibujo en el servidor y en el navegador.

La [guía de exportación](https://silverpointweb.vercel.app/docs/export) de la documentación describe el manejador de cada framework.
