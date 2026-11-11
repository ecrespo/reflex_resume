Title: Silverpoint, artículo 22: presentaciones en Markdown con gráficos vivos
Date: 2026-11-11 21:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Marp, Visualización
lang: es
translation: true
Slug: silverpoint_serie_22
Authors: Ernesto Crespo
Summary: SpDeck y @silverpoint/marp en React, Vue, Angular y Reflex: una presentación escrita en Markdown con la sintaxis de Marp, con gráficos de silverpoint vivos en bloques de código, directivas, teclado, fragmentos, eventos de página, los límites SP026 a SP029 y la línea de comandos de Marp.

El panel de operaciones de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) ya tiene gráficos, un panel, componentes y una línea de tiempo. Falta contarlo en la reunión de los lunes. Este último artículo del nivel 3 hace la revisión semanal de operaciones como una presentación escrita en Markdown, con los gráficos del panel dentro.

La sintaxis es la de [Marp](https://marp.app/): diapositivas separadas por `---`, directivas en comentarios HTML. silverpoint añade un tipo de bloque de código, `silverpoint`, que se convierte en un gráfico vivo: con su descripción emergente, su tabla accesible y el entintado del estilo base.

## Lo que vas a construir

Una presentación de cuatro diapositivas: la portada, el tráfico por hora como gráfico de línea, una lista de lo que pasó en la semana y las ventas por canal como gráfico de anillo, esta última en cianotipia. Debajo, un texto dice en qué diapositiva estás.

![La diapositiva Traffic de la revisión semanal: el gráfico de visitas por hora dentro de la diapositiva, el pie «Weekly operations review», el número 2/4 y los controles de la presentación](./images/silverpoint-serie-22.png)

Las flechas del teclado pasan las diapositivas, y la dirección de la página guarda la diapositiva actual, como `#2`.

## Lo que necesitas

El proyecto de tu framework de los artículos 03 a 06. Los datos de los gráficos van dentro del Markdown, así que no hace falta el archivo de visitas.

## 1. Instalar @silverpoint/marp

El motor de las presentaciones está en su propio paquete, `@silverpoint/marp`, que trae Marpit, el núcleo de Marp. Es una dependencia opcional de los adaptadores. En React, Vue y Angular:

```sh
npm install @silverpoint/marp@^0.9.2
```

En Reflex no hace falta: `sp_deck` lo instala y añade sus hojas de estilo.

## 2. Las hojas de estilo

Cuatro, en este orden: las fuentes, el estilo base, los componentes de interfaz y la de las presentaciones, `@silverpoint/marp/deck.css`.

En React, en `src/main.tsx`:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import '@silverpoint/marp/deck.css';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

En Vue, en `src/main.ts`:

```ts
import { createApp } from 'vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import '@silverpoint/marp/deck.css';
import './style.css';
import App from './App.vue';

createApp(App).mount('#app');
```

En Angular, en `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';
@import '@silverpoint/marp/deck.css';

body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

## 3. La presentación en Markdown

Crea `src/review.md` en React y Vue, `src/app/review.md` en Angular u `ops_panel/review.md` en Reflex. Es el mismo archivo en los cuatro:

````markdown
---
paginate: true
footer: Weekly operations review
---

<!-- _class: lead -->

# Weekly operations review

The web service, week 45.

---

## Traffic

```silverpoint
{
  "chart": "line-chart",
  "data": [
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
    {"hour": "23", "hits": 20}
  ],
  "props": {"xKey": "hour", "valueKey": "hits", "title": "Hits per hour", "unit": "thousands"},
  "height": 360
}
```

---

## What happened

* Release 2.2 put a CDN in front of the API
* Errors peaked at 12:00, with 11 in the hour
* Search stayed under its latency budget

<!-- Pause on the CDN: it explains the lower p95. -->

---

<!-- _ground: cyanotype -->

## Sales by channel

```silverpoint
{
  "chart": "donut-chart",
  "data": [
    {"channel": "Web", "sales": 46},
    {"channel": "App", "sales": 31},
    {"channel": "Partners", "sales": 15},
    {"channel": "Phone", "sales": 8}
  ],
  "props": {"nameKey": "channel", "valueKey": "sales", "title": "Sales by channel", "centerLabel": "thousand EUR"},
  "height": 360
}
```
````

Lo que hay en él:

| Elemento | Qué hace |
|---|---|
| El bloque inicial entre `---` | Las directivas globales: `paginate` numera las diapositivas y `footer` pone el pie en todas |
| `---` | Separa dos diapositivas |
| `<!-- _class: lead -->` | Una directiva de una sola diapositiva: el guion bajo la limita a esa. `lead` centra la portada |
| Un bloque de código `silverpoint` | Un gráfico vivo: un objeto JSON con el gráfico, sus filas y sus props |
| `<!-- Pause on the CDN… -->` | Un comentario que no es una directiva es una nota del presentador |
| `<!-- _ground: cyanotype -->` | Cambia el estilo base solo en esa diapositiva |

### Las directivas

silverpoint añade tres directivas a las de Marpit: `ground`, `substrate` y `mode`, con sus formas de una sola diapositiva, `_ground`, `_substrate` y `_mode`. Las de Marpit también funcionan: `theme`, `class`, `paginate`, `header`, `footer`, `backgroundColor`, `backgroundImage`, `color`, `size`, `headingDivider` y `lang`.

Las clases de diapositiva son cuatro: `lead`, `invert`, `plate` y `hatched`.

El HTML del Markdown nunca se dibuja: los comentarios se leen como directivas o notas, y el resto del HTML se ignora.

### Los bloques de gráfico

| Clave | Qué es |
|---|---|
| `chart` | El gráfico, por su nombre en el catálogo: `line-chart`, `donut-chart`… |
| `data` | Las filas |
| `props` | Las props del gráfico, con sus nombres de React: `xKey`, `valueKey`, `nameKey`… |
| `width`, `height` | El tamaño; el alto es 360 por defecto |
| `id` | El identificador del gráfico; por defecto, el de la presentación, la diapositiva y el orden del gráfico |
| `ground`, `substrate`, `mode`, `palette` | El estilo de ese gráfico; si no los pones, hereda los de su diapositiva |

### Los fragmentos

Cada elemento de una lista es un fragmento. Al llegar a la diapositiva What happened, la lista está oculta, y cada pulsación de la flecha muestra un elemento. Con los tres a la vista, la siguiente pulsación pasa a la diapositiva siguiente.

## 4. En React

Vite carga el Markdown como texto con el sufijo `?raw`:

```tsx
import { useState } from 'react';
import { SpDeck } from '@silverpoint/react/deck';
import markdown from './review.md?raw';

export default function App() {
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  return (
    <main style={{ maxWidth: 960 }}>
      <SpDeck
        markdown={markdown}
        page={page}
        onPageChange={(change) => {
          setPage(change.page);
          setTotal(change.total);
        }}
        onReady={(ready) => setTotal(ready.total)}
        hash={true}
      />
      <p>
        Slide {page} of {total}
      </p>
    </main>
  );
}
```

`page` y `onPageChange` hacen de la página un estado controlado: el componente avisa del cambio y tú decides la página. `onPageChange` recibe `{ page, total }`, y `onReady` recibe `{ total }` cuando la presentación está lista. Con `hash`, la dirección de la página lleva el número de la diapositiva.

## 5. En Vue

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpDeck } from '@silverpoint/vue/deck';
import markdown from './review.md?raw';

const page = ref(1);
const total = ref(0);

function onReady(ready: { total: number }) {
  total.value = ready.total;
}
</script>

<template>
  <main style="max-width: 960px">
    <SpDeck :markdown="markdown" v-model:page="page" :hash="true" @ready="onReady" />
    <p>Slide {{ page }} of {{ total }}</p>
  </main>
</template>
```

`v-model:page` hace lo mismo que `page` y `onPageChange` en React. Los demás eventos son emisiones: `@page-change`, `@fragment-change` y `@ready`.

## 6. En Angular

Angular no carga Markdown por defecto. En `angular.json`, dentro de las `options` de `build`, dile que cargue los `.md` como texto:

```json
"loader": {
  ".md": "text"
},
"allowedCommonJsDependencies": [
  "@marp-team/marpit"
]
```

`allowedCommonJsDependencies` calla el aviso de que Marpit no es un módulo ESM. Para que TypeScript acepte la importación, crea `src/markdown.d.ts`:

```ts
declare module '*.md' {
  const markdown: string;
  export default markdown;
}
```

Y el componente, en `src/app/app.ts`:

```ts
import { Component, signal } from '@angular/core';
import { SpDeckComponent } from '@silverpoint/angular/deck';
import markdown from './review.md';

@Component({
  selector: 'app-root',
  imports: [SpDeckComponent],
  template: `
    <main style="max-width: 960px">
      @defer {
        <sp-deck
          [markdown]="markdown"
          [page]="page()"
          (pageChange)="page.set($event.page)"
          (ready)="total.set($event.total)"
          [hash]="true"
        />
      } @placeholder {
        <p>Loading the deck…</p>
      }
      <p>Slide {{ page() }} of {{ total() }}</p>
    </main>
  `,
})
export class App {
  protected readonly markdown = markdown;
  protected readonly page = signal(1);
  protected readonly total = signal(0);
}
```

`(pageChange)` recibe `{ page, total }`, como en React y Vue. El bloque `@defer` no es obligatorio, pero hace falta con el presupuesto por defecto de Angular: sin él, el motor de las presentaciones va en el paquete inicial, que pasa de 1 MB y la compilación de producción falla. Con `@defer`, el paquete inicial se queda en 420 kB y la presentación se carga aparte.

## 7. En Reflex

```python
from pathlib import Path

import reflex as rx
from reflex_silverpoint_react import sp_deck

MARKDOWN = Path(__file__).with_name("review.md").read_text()


class DeckState(rx.State):
    page: int = 1
    total: int = 0

    @rx.event
    def set_page(self, page: int, total: int):
        self.page = page
        self.total = total

    @rx.event
    def set_total(self, total: int):
        self.total = total


def index() -> rx.Component:
    return rx.box(
        sp_deck(
            MARKDOWN,
            page=DeckState.page,
            on_page_change=DeckState.set_page,
            on_ready=DeckState.set_total,
            hash=True,
        ),
        rx.text("Slide ", DeckState.page, " of ", DeckState.total),
        max_width="960px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

El Markdown se lee una vez, al importar el módulo. `on_page_change` llama al backend con la página y el total, y `on_ready` con el total. Con `hash=True`, la página vive también en la dirección, como en los otros tres.

## El teclado

Con el foco en la presentación:

| Teclas | Qué hacen |
|---|---|
| Flecha derecha, flecha abajo, Av Pág, Espacio, Intro | El paso siguiente: un fragmento o la diapositiva siguiente |
| Flecha izquierda, flecha arriba, Re Pág, Mayús + Espacio | El paso anterior |
| Inicio, Fin | La primera y la última diapositiva |
| o | La vista general de todas las diapositivas |
| f | Pantalla completa |
| n | Las notas del presentador |

Las teclas que se escriben en un campo de formulario no mueven la presentación. En pantallas táctiles, deslizar el dedo en horizontal también pasa las diapositivas.

## Los eventos

| Evento | Qué lleva | React | Vue | Angular | Reflex |
|---|---|---|---|---|---|
| Cambio de página | `page`, `total` | `onPageChange` | `v-model:page`, `@page-change` | `(pageChange)` | `on_page_change` |
| Cambio de fragmento | `page`, `step`, `steps` | `onFragmentChange` | `@fragment-change` | `(fragmentChange)` | `on_fragment_change` |
| Lista | `total` | `onReady` | `@ready` | `(ready)` | `on_ready` |

## Los límites y los avisos

| Código | Cuándo |
|---|---|
| `SP026` | Un bloque de gráfico no es válido: su JSON, su gráfico, una prop, un tamaño o un error del gráfico. La diapositiva muestra el error en su lugar |
| `SP027` | Una directiva tiene un valor desconocido. Se mantiene el heredado |
| `SP028` | La página está fuera de la presentación. Se ajusta a la más cercana |
| `SP029` | El Markdown supera un límite: 512 KB, 300 diapositivas o 60 bloques de gráfico. Se dibuja hasta el límite |

Con el servidor MCP de silverpoint conectado, la herramienta `validate_deck` revisa el Markdown antes de abrirlo. Con un estilo base que no existe, `_ground: sepia`, y una prop que el gráfico de línea no declara, `colour`, devolvió dos avisos:

* `SP027`: «Slide 2: ground "sepia" is not a registered ground; the inherited value holds.»
* `SP026`: «Chart fence on slide 2: line-chart does not declare "colour".»

Con la presentación de este artículo, no devuelve ninguno. `render_deck` devuelve la presentación como un documento HTML independiente.

## Marp CLI

La misma presentación se puede convertir sin aplicación, con la línea de comandos de Marp y el motor de silverpoint. Los fondos y los gráficos salen como SVG estático:

```sh
npx @marp-team/marp-cli --engine @silverpoint/marp/cli review.md
```

`@silverpoint/marp` trae también el tema como hoja de estilo, `@silverpoint/marp/theme.css`, para Marp CLI con `--theme` o para la extensión de Marp para VS Code. Con el tema solo, sin el motor, la presentación pierde los fondos generados y los bloques `silverpoint` se ven como código.

## El tamaño

El motor de las presentaciones incluye Marpit y su intérprete de Markdown. En React, la compilación da un paquete de 856 kB, 272 kB comprimido, y Vite avisa de que pasa de 500 kB. En Vue, 651 kB, 210 kB comprimido. Los gráficos de los bloques se cargan aparte, cada uno en su fragmento, solo si la presentación los usa. Si la presentación no está en la primera página de tu aplicación, cárgala con una importación dinámica, como hace `@defer` en Angular.

## Problemas comunes

* **La compilación no encuentra `@silverpoint/marp`.** No está instalado: es una dependencia opcional.
* **Un bloque de gráfico se ve como código.** El bloque no se llama `silverpoint`, o estás usando el tema de Marp sin el motor de silverpoint.
* **En lugar del gráfico aparece un error y la consola muestra `SP026`.** El JSON del bloque no es válido o tiene una prop que el gráfico no declara. `validate_deck` dice cuál.
* **Una directiva no hace nada y la consola muestra `SP027`.** Su valor no existe: usa `silverpoint` o `cyanotype`, uno de sus sustratos, e `ink` o `precision`.
* **Las flechas no pasan las diapositivas.** El foco no está en la presentación: haz clic en ella primero.
* **La compilación de Angular falla por el presupuesto.** Usa `@defer` o sube el presupuesto en `angular.json`.

## Lo que viene

Con este artículo termina el nivel 3. El panel ya es una aplicación: componentes de interfaz, exportación, render en servidor, datos en vivo, una línea de tiempo y una presentación.

El nivel 4 junta todo en un proyecto final. Empieza por el [artículo 23](/blog/silverpoint_serie_23): el panel de operaciones completo en React con Next.js.
