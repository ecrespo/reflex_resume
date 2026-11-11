Title: Silverpoint, artículo 19: render en servidor y determinismo
Date: 2026-11-11 20:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_19
Authors: Ernesto Crespo
Summary: Por qué un gráfico de silverpoint dibujado a mano sale igual en el servidor y en el navegador: la semilla que sale del id, los gráficos de servidor de React en Next.js, el render con Vue y Angular, lo que exporta Reflex, y los errores que rompen el determinismo.

Un gráfico de silverpoint parece dibujado a mano: las líneas tiemblan un poco y el marco no es un rectángulo perfecto. Si ese temblor fuera aleatorio, el servidor dibujaría un gráfico y el navegador otro, y la página mostraría un salto al cargar o un error de hidratación.

Este artículo de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) explica por qué no pasa, y cómo renderizar el panel de operaciones en el servidor con Next.js, Vue y Angular. También qué hace Reflex.

## El temblor sale de una semilla

El trazo a mano no usa `Math.random()`. Sale de una semilla, y la semilla sale del `id` del gráfico. El [artículo 07](/blog/silverpoint_serie_7) lo presentó entre las props comunes:

| Prop | Qué hace | Por defecto |
|---|---|---|
| `id` | Un identificador estable | Uno generado de forma determinista |
| `seed` | La semilla del trazo a mano | Derivada de `id` |

La especificación de la librería lo fija con cuatro reglas:

* La semilla se deriva del `id` de forma estable.
* El código que dibuja no puede llamar a `Math.random()` ni a `Date.now()`. Una comprobación en la integración continua lo impide.
* Las mismas entradas dan el mismo SVG, byte a byte.
* Las coordenadas se redondean a dos decimales, para que dos motores de JavaScript no difieran en el último dígito.

La consecuencia es la que importa aquí: **el mismo `id`, con los mismos datos y el mismo tamaño, da los mismos trazos en el servidor y en el navegador**, y en cada ejecución. El servidor manda un SVG, el navegador dibuja otro idéntico encima y no hay nada que corregir.

## Los gráficos de servidor de React

En React, cada gráfico tiene dos entradas:

| Entrada | Qué es |
|---|---|
| `@silverpoint/react/line-chart` | El componente de cliente: mide su contenedor, responde al puntero y al teclado |
| `@silverpoint/react/server/line-chart` | Un componente de servidor: SVG puro, sin JavaScript en el navegador |

El de servidor no mide nada, porque en el servidor no hay contenedor. Por eso necesita tres props que el de cliente no exige: `id`, `width` y `height`. Si falta alguna, el gráfico avisa con `SP002` o `SP003`. Tampoco acepta eventos: no hay JavaScript que los escuche.

## Un gráfico de servidor en Next.js

Una aplicación nueva de Next.js con el App Router:

```bash
npx create-next-app@latest ops-panel
cd ops-panel
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
```

Las filas por hora del [artículo 03](/blog/silverpoint_serie_3) van en `app/traffic.ts`. Las hojas de estilos se cargan una vez, en `app/layout.tsx`:

```tsx
import type { Metadata } from 'next';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './globals.css';

export const metadata: Metadata = {
  title: 'Operations panel',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

`app/globals.css` deja el fondo y el margen:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

Y la página, `app/page.tsx`, que es un componente de servidor:

```tsx
import { LineChart } from '@silverpoint/react/server/line-chart';
import { traffic } from './traffic';

export default function Page() {
  return (
    <main>
      <LineChart
        id="hits"
        width={640}
        height={200}
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
      />
    </main>
  );
}
```

Con `npm run build`, Next.js trata la página como estática y guarda su HTML. Ese HTML ya contiene el gráfico entero: el SVG con sus trazos, la tabla de datos oculta y `data-status="ready"`. La página no carga en el navegador ni una línea de JavaScript de silverpoint.

Comparé el SVG de esa página con el que exporta `toSVGString()` en el navegador, con la aplicación de Vite del [artículo 18](/blog/silverpoint_serie_18) y el mismo `id`, ancho y alto. Son idénticos, byte a byte: Node y Chrome dibujan los mismos trazos.

![El panel de operaciones renderizado en el servidor por Next.js con el Dashboard de servidor: el tráfico por hora en dos columnas y los errores por hora en una](./images/silverpoint-serie-19.png)

## Un panel en el servidor

El `Dashboard` del [artículo 13](/blog/silverpoint_serie_13) también tiene su entrada de servidor, `@silverpoint/react/server/dashboard`. Las filas ganan el campo `errors`, en `app/ops.ts`:

```ts
export type HourlyOps = {
  hour: string;
  hits: number;
  errors: number;
};

export const ops: HourlyOps[] = [
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
```

`app/panel/page.tsx`:

```tsx
import { BarChart } from '@silverpoint/react/server/bar-chart';
import { Dashboard, DashboardCell, type DashboardLayout } from '@silverpoint/react/server/dashboard';
import { LineChart } from '@silverpoint/react/server/line-chart';
import { ops } from '../ops';

const layout: DashboardLayout = {
  columns: { sm: 1, md: 2, lg: 3 },
  cells: [{ id: 'hits', colSpan: { md: 2, lg: 2 } }, { id: 'errors' }],
};

export default function PanelPage() {
  return (
    <Dashboard id="ops" title="Operations" layout={layout} ssrWidth={1200}>
      <DashboardCell cell="hits">
        <LineChart data={ops} xKey="hour" valueKey="hits" title="Hits per hour" />
      </DashboardCell>
      <DashboardCell cell="errors">
        <BarChart data={ops} xKey="hour" valueKey="errors" title="Errors per hour" />
      </DashboardCell>
    </Dashboard>
  );
}
```

Aquí los gráficos no llevan `id`, `width` ni `height`. Los da el panel: cada gráfico recibe el `id` de su celda, `ops--hits` y `ops--errors`, y el tamaño de la celda. Es la imagen de arriba.

El servidor no conoce el ancho de la ventana, así que el panel supone uno: `ssrWidth`, 1200 px por defecto. Con 1200 px el panel está en el tamaño `lg`, de tres columnas, y el servidor dibuja el tráfico a 794,67 px y los errores a 389,33 px.

Un panel de servidor no tiene `link`: los gráficos enlazados necesitan JavaScript en el navegador. Si quieres enlazarlos, usa el `Dashboard` de cliente.

## Gráficos de cliente en Next.js

Un gráfico interactivo es un componente de cliente. Va en su propio archivo con `'use client'`, `app/live/hits-chart.tsx`:

```tsx
'use client';

import { useState } from 'react';
import type { ActiveItem } from '@silverpoint/core';
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from '../traffic';

export function HitsChart() {
  const [active, setActive] = useState<ActiveItem | null>(null);

  return (
    <>
      <LineChart
        id="hits"
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        height={200}
        onActiveChange={setActive}
      />
      <p>{active ? `${String(active.datum.hour)}:00, ${active.value}k hits` : 'Point at an hour'}</p>
    </>
  );
}
```

Y la página que lo usa, `app/live/page.tsx`, sigue siendo de servidor:

```tsx
import { HitsChart } from './hits-chart';

export default function LivePage() {
  return (
    <main style={{ maxWidth: 640 }}>
      <HitsChart />
    </main>
  );
}
```

Next.js también renderiza este gráfico en el servidor, pero sin `width` no sabe su tamaño. El HTML lleva un hueco con `data-status="deferred"` y un SVG vacío. En el navegador, el gráfico mide su contenedor y dibuja: 640 × 260 px, sin errores en la consola, y al pasar el puntero el texto cambia a «11:00, 62k hits».

Si quieres el dibujo en el HTML también en un gráfico de cliente, dale `id` y `width`. Con los dos fijos, los trazos del servidor y los del navegador coinciden.

## Lo que rompe el determinismo

Probé tres variantes del gráfico de cliente con `next dev`:

| `id` | Resultado |
|---|---|
| `id="hits"` | Los mismos trazos en el servidor y en el navegador, sin avisos |
| ``id={`hits-${Math.random().toString(36).slice(2)}`}`` | Next.js avisa de un valor inestable de `Math.random()` y React, de atributos que no coinciden al hidratar; 6 de los 9 trazos cambian |
| Sin `id` | El gráfico usa `useId` de React y genera el mismo `id` en los dos lados |

Un `id` con `Math.random()` o `Date.now()` da una semilla distinta en cada render: el servidor y el navegador dibujan dos gráficos distintos. El aviso de React lo dice claro: esas diferencias no se corrigen, y la página queda con atributos de un render y de otro mezclados.

Sin `id` funciona, pero el `id` generado depende de la posición del gráfico en el árbol de componentes. Si mueves el gráfico, cambia su dibujo. Un `id` explícito y estable es lo más seguro.

## En Vue

Vue renderiza en el servidor con `createSSRApp` y `renderToString`. Sobre la aplicación de Vite del [artículo 04](/blog/silverpoint_serie_4), `src/App.vue`:

```vue
<script setup lang="ts">
import { SpLineChart } from '@silverpoint/vue/line-chart';
import { traffic } from './traffic';
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart
      id="hits"
      :width="640"
      :data="traffic"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      badge="Today"
      :height="200"
    />
  </main>
</template>
```

La entrada del servidor, `src/entry-server.ts`, instala el proveedor con el idioma de los números, como en el [artículo 09](/blog/silverpoint_serie_9):

```ts
import { createSSRApp } from 'vue';
import { renderToString } from 'vue/server-renderer';
import { provideSilverpoint } from '@silverpoint/vue';
import App from './App.vue';

export function render(): Promise<string> {
  return renderToString(createSSRApp(App).use(provideSilverpoint({ locale: 'en' })));
}
```

Para probarla, Vite la compila para Node y un script la ejecuta. `render.mjs`:

```js
import { render } from './dist-server/entry-server.js';

console.log(await render());
```

```bash
npx vite build --ssr src/entry-server.ts --outDir dist-server
node render.mjs
```

Sale el HTML del gráfico con `data-status="ready"` y un SVG de 640 × 260 px. Sus trazos son los mismos que los del gráfico de React del servidor y que los del navegador. Dos ejecuciones dan exactamente el mismo HTML.

Como en React, sin `width` el gráfico sale en el estado `deferred`, sin trazos, y se dibuja al montarse en el navegador. Nuxt usa este mismo mecanismo, pero la documentación de silverpoint no lo da como integración comprobada.

## En Angular

En Angular no hay nada específico de silverpoint. Sobre la aplicación del [artículo 05](/blog/silverpoint_serie_5):

```bash
npx ng add @angular/ssr
```

El comando crea `src/server.ts` y `src/main.server.ts`, pone `"outputMode": "server"` en `angular.json` y añade `provideClientHydration()` a la configuración. Por defecto, todas las rutas se prerenderizan al compilar. `src/app/app.ts`:

```ts
import { Component } from '@angular/core';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { traffic } from './traffic';

@Component({
  selector: 'app-root',
  imports: [SpLineChart],
  template: `
    <main style="max-width: 640px">
      <sp-line-chart
        id="hits"
        [width]="640"
        [data]="traffic"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        [height]="200"
      />
    </main>
  `,
})
export class App {
  protected readonly traffic = traffic;
}
```

`ng build` prerenderiza la ruta y deja el HTML en `dist/ops-panel/browser/index.html`. El gráfico va dentro, listo, con los mismos trazos que en React y Vue. Sin `[width]`, sale `deferred`, como en los otros dos.

En Angular, un `id` escrito como atributo también queda en el elemento `sp-line-chart`. Los elementos internos del gráfico llevan el `id` con un sufijo, como `hits-title` o `hits-desc`, así que no se repiten.

Para servirlo:

```bash
NG_ALLOWED_HOSTS=localhost node dist/ops-panel/server/server.mjs
```

Sin `NG_ALLOWED_HOSTS`, el servidor de Angular responde con un error 400 a `localhost`: solo atiende a los nombres de servidor que conoce, como protección. En producción, pon tu dominio. En el navegador, la página hidrata con el gráfico listo y sin errores en la consola.

## En Reflex

Reflex compila las páginas a una aplicación de React, y `reflex export --frontend-only` genera una versión estática: este blog se publica así. La documentación de silverpoint dice que en Reflex los gráficos se dibujan en el cliente. La exportación, sin embargo, prerenderiza cada página a HTML, y el gráfico se comporta como un gráfico de cliente de React en Next.js.

Con el gráfico del [artículo 06](/blog/silverpoint_serie_6), sin `width`, el HTML exportado lleva el gráfico en `deferred` y un SVG vacío. Con `id` y `width`, `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import line_chart

from .traffic import TRAFFIC


def index() -> rx.Component:
    return rx.box(
        line_chart(
            id="hits",
            width=640,
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            badge="Today",
            height=200,
        ),
        max_width="704px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

`max_width` pasa a 704 px para que quepan los 640 px del gráfico y los 32 px de `padding` a cada lado. El `index.html` exportado ya contiene el gráfico listo, con los mismos trazos que en React, Vue y Angular. Servido como archivos estáticos, sin backend, el gráfico se ve igual. La consola solo se queja de que no puede abrir el WebSocket del backend, lo esperado sin él.

En Reflex el determinismo también se nota fuera del primer render: un gráfico que se vuelve a montar con los mismos datos se dibuja igual, porque su `id` no cambia.

## Problemas comunes

* **`SP002` o `SP003` en un gráfico de servidor.** Le falta `id`, `width` o `height`. Dentro de un `Dashboard` de servidor, los pone el panel.
* **Un aviso de hidratación en Next.js.** Algo del `id` cambia entre el servidor y el navegador: `Math.random()`, `Date.now()` o un dato que solo existe en uno de los dos.
* **El HTML tiene `data-status="deferred"` y ningún trazo.** El gráfico no tenía `width` en el servidor. Es correcto: se dibuja en el navegador. Si lo quieres en el HTML, fija `width`.
* **Un 400 al servir Angular en local.** Falta `NG_ALLOWED_HOSTS`.
* **El panel de servidor se dibuja a otro ancho.** Usa `ssrWidth`, no el ancho real de la ventana.

## Lo que viene

El [artículo 20](/blog/silverpoint_serie_20) alimenta el panel con datos en vivo y se ocupa del rendimiento.

La [guía de render en servidor](https://silverpointweb.vercel.app/docs/ssr) de la documentación resume el caso de cada framework.
