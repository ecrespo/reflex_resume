Title: Silverpoint, artículo 21: líneas de tiempo con TimelineJS
Date: 2026-11-11 21:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, TimelineJS, Visualización
lang: es
translation: true
Slug: silverpoint_serie_21
Authors: Ernesto Crespo
Summary: SpTimeline, la piel de silverpoint sobre TimelineJS, en React, Vue, Angular y Reflex: la dependencia opcional, el orden de las hojas de estilo, el JSON de TimelineJS, los eventos, el contenido de reserva con SP025 y la línea de tiempo de certificaciones de este blog como ejemplo real.

Los gráficos de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) dibujan números. Un panel de operaciones también tiene una historia: cuándo salió cada versión y cuándo falló algo. Para eso silverpoint trae `SpTimeline`, una piel sobre [TimelineJS](https://timeline.knightlab.com/), la biblioteca de líneas de tiempo de Knight Lab.

TimelineJS pone las diapositivas, la navegación y la escala de fechas. silverpoint pone los marcos, los tonos y la tipografía del estilo base. El resultado se ve como el resto del panel.

## Lo que vas a construir

La historia del servicio web en 2026: tres versiones, dos incidentes y una época, la migración del clúster. Debajo, un texto dice qué diapositiva está activa.

![La línea de tiempo del servicio en la diapositiva del incidente del checkout, con las filas Releases e Incidents y el texto «Showing: Checkout errors» debajo](./images/silverpoint-serie-21.png)

Las versiones y los incidentes van en filas separadas: TimelineJS agrupa los eventos por su campo `group`.

## Lo que necesitas

El proyecto de tu framework de los artículos 03 a 06. La línea de tiempo no usa los datos de visitas: tiene su propio JSON.

## 1. Instalar TimelineJS

TimelineJS es una dependencia opcional de los adaptadores: no se instala con `@silverpoint/react`, `@silverpoint/vue` o `@silverpoint/angular`. Instálala tú antes de importar la ruta `timeline`, o la compilación no la encuentra:

```sh
npm install @knight-lab/timelinejs@^3.9.13
```

En Reflex no hace falta: `sp_timeline` declara la dependencia y Reflex la instala al compilar.

## 2. Las hojas de estilo, en orden

La línea de tiempo necesita cinco hojas de estilo, en este orden: las fuentes, el estilo base, los componentes de interfaz, la de TimelineJS y la piel de silverpoint. La piel va después de la de TimelineJS porque la sobrescribe.

En React, en `src/main.tsx`:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import '@knight-lab/timelinejs/dist/css/timeline.css';
import '@silverpoint/grounds/timeline.css';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

En Vue, en `src/main.ts`, con las mismas importaciones:

```ts
import { createApp } from 'vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import '@knight-lab/timelinejs/dist/css/timeline.css';
import '@silverpoint/grounds/timeline.css';
import './style.css';
import App from './App.vue';

createApp(App).mount('#app');
```

En Angular, en `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';
@import '@knight-lab/timelinejs/dist/css/timeline.css';
@import '@silverpoint/grounds/timeline.css';

body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}

/* The skin sets its display font on the slide arrows too: give them back TimelineJS's icon font. */
.sp-timeline .tl-timeline div.tl-slidenav-icon {
  font-family: 'tl-icons' !important;
}
```

No te saltes `@silverpoint/grounds/ui.css`. Sin ella, la línea de tiempo pierde la tarjeta que la enmarca: la piel la dibuja con las clases de los componentes de interfaz.

La regla del final, que en React y Vue va en `src/index.css` y `src/style.css`, corrige un fallo de la piel en la versión 0.9.2. La piel pone su tipografía también en las flechas de las diapositivas, que son glifos de la fuente de iconos de TimelineJS, `tl-icons`. Sin la regla, las flechas salen como cajas vacías. En React queda así:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}

/* The skin sets its display font on the slide arrows too: give them back TimelineJS's icon font. */
.sp-timeline .tl-timeline div.tl-slidenav-icon {
  font-family: 'tl-icons' !important;
}
```

## 3. Los datos: el JSON de TimelineJS

`data` es el JSON de TimelineJS sin cambios: una diapositiva `title`, los `events` y, si quieres, `eras` y `scale`. La [documentación de TimelineJS](https://timeline.knightlab.com/docs/json-format.html) describe cada campo.

Crea `src/history.ts` en React y Vue, o `src/app/history.ts` en Angular:

```ts
export const history = {
  title: {
    unique_id: 'overview',
    text: {
      headline: 'Service history',
      text: 'Releases and incidents of the web service in 2026.',
    },
  },
  events: [
    {
      unique_id: 'release-2-0',
      group: 'Releases',
      start_date: { year: 2026, month: 1, day: 12 },
      text: { headline: 'Release 2.0', text: 'The new checkout goes live.' },
    },
    {
      unique_id: 'incident-checkout',
      group: 'Incidents',
      start_date: { year: 2026, month: 3, day: 3 },
      text: {
        headline: 'Checkout errors',
        text: '47 minutes of 5xx errors after a database failover.',
      },
    },
    {
      unique_id: 'release-2-1',
      group: 'Releases',
      start_date: { year: 2026, month: 5, day: 20 },
      text: { headline: 'Release 2.1', text: 'Search rewritten on a new index.' },
    },
    {
      unique_id: 'incident-search',
      group: 'Incidents',
      start_date: { year: 2026, month: 8, day: 7 },
      text: {
        headline: 'Slow search',
        text: 'The p95 of search reached 2 seconds for three hours.',
      },
    },
    {
      unique_id: 'release-2-2',
      group: 'Releases',
      start_date: { year: 2026, month: 10, day: 2 },
      text: { headline: 'Release 2.2', text: 'A CDN in front of the API.' },
    },
  ],
  eras: [
    {
      start_date: { year: 2026, month: 6, day: 1 },
      end_date: { year: 2026, month: 7, day: 15 },
      text: { headline: 'Cluster migration' },
    },
  ],
};
```

Tres cosas de este JSON:

| Campo | Para qué |
|---|---|
| `unique_id` | El identificador de cada diapositiva. El evento de cambio lo devuelve, así que dale uno estable a cada una |
| `group` | La fila del evento en la barra de navegación |
| `eras` | Una franja de fechas sin diapositiva propia, como la migración del clúster |

El componente construye TimelineJS sobre una copia de `data`: tu objeto no se modifica.

## 4. En React

```tsx
import { useState } from 'react';
import { SpTimeline } from '@silverpoint/react/timeline';
import { history } from './history';

const options = { timenav_position: 'bottom', initial_zoom: 2 };

const headlines = new Map(
  [history.title, ...history.events].map((slide) => [slide.unique_id, slide.text.headline]),
);

export default function App() {
  const [current, setCurrent] = useState('Service history');

  return (
    <main style={{ maxWidth: 960 }}>
      <SpTimeline
        data={history}
        options={options}
        height="560px"
        label="Service history"
        onChange={(id) => setCurrent(headlines.get(id ?? '') ?? 'Service history')}
        fallback={<p>The timeline could not load.</p>}
      />
      <p>Showing: {current}</p>
    </main>
  );
}
```

`options` pasa a TimelineJS sus opciones tal cual, salvo `font` y `theme`, que pone el estilo base. Aquí la barra de navegación va abajo y el zoom inicial es 2.

`height` es una longitud CSS, `'600px'` por defecto. Un valor que no sea una longitud se descarta con el aviso `SP017`. `label` es el nombre accesible de la región; sin él, se usa el titular de la diapositiva `title`.

`onChange` recibe el `unique_id` de la diapositiva activa. Con el mapa `headlines`, el texto de debajo muestra su titular.

### Datos y opciones estables

`options` está fuera del componente a propósito. El componente reconstruye TimelineJS cuando cambian `data`, `options` o `inkedFrames`, y compara las referencias. Si escribes `options={{ timenav_position: 'bottom' }}` dentro del JSX, cada render crea un objeto nuevo: al pulsar la flecha, `onChange` actualiza el estado, React vuelve a renderizar, la línea de tiempo se reconstruye y regresa a la primera diapositiva.

Lo vi al probar este artículo: la flecha parecía no hacer nada. Declara `data` y `options` fuera del componente, o guárdalos en un `useMemo`.

## 5. En Vue

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpTimeline } from '@silverpoint/vue/timeline';
import { history } from './history';

const options = { timenav_position: 'bottom', initial_zoom: 2 };

const headlines = new Map(
  [history.title, ...history.events].map((slide) => [slide.unique_id, slide.text.headline]),
);

const current = ref('Service history');

function onChange(id: string | undefined) {
  current.value = headlines.get(id ?? '') ?? 'Service history';
}
</script>

<template>
  <main style="max-width: 960px">
    <SpTimeline
      :data="history"
      :options="options"
      height="560px"
      label="Service history"
      @change="onChange"
    >
      <template #fallback>
        <p>The timeline could not load.</p>
      </template>
    </SpTimeline>
    <p>Showing: {{ current }}</p>
  </main>
</template>
```

Los eventos son emisiones: `@change`, `@loaded`, `@nav-next`… El contenido de reserva va en el slot `fallback`.

## 6. En Angular

```ts
import { Component, signal } from '@angular/core';
import { SpTimeline, SpTimelineFallback } from '@silverpoint/angular/timeline';
import { history } from './history';

const options = { timenav_position: 'bottom', initial_zoom: 2 };

const headlines = new Map(
  [history.title, ...history.events].map((slide) => [slide.unique_id, slide.text.headline]),
);

@Component({
  selector: 'app-root',
  imports: [SpTimeline, SpTimelineFallback],
  template: `
    <main style="max-width: 960px">
      <sp-timeline
        [data]="history"
        [options]="options"
        height="560px"
        label="Service history"
        (change)="onChange($event)"
      >
        <ng-template spFallback>
          <p>The timeline could not load.</p>
        </ng-template>
      </sp-timeline>
      <p>Showing: {{ current() }}</p>
    </main>
  `,
})
export class App {
  protected readonly history = history;
  protected readonly options = options;
  protected readonly current = signal('Service history');

  protected onChange(id: string | undefined) {
    this.current.set(headlines.get(id ?? '') ?? 'Service history');
  }
}
```

Los eventos son salidas: `(change)`, `(loaded)`, `(navNext)`… El contenido de reserva es un `<ng-template spFallback>`, y la directiva `SpTimelineFallback` va en `imports` junto al componente.

## 7. En Reflex

En `ops_panel/history.py`, el mismo JSON como diccionario, `HISTORY`, y el mapa de titulares:

```python
HEADLINES = {
    slide["unique_id"]: slide["text"]["headline"]
    for slide in [HISTORY["title"], *HISTORY["events"]]
}
```

Y la página, en `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import sp_timeline

from .history import HEADLINES, HISTORY

OPTIONS = {"timenav_position": "bottom", "initial_zoom": 2}


class TimelineState(rx.State):
    current: str = "Service history"

    @rx.event
    def on_slide(self, unique_id: str):
        self.current = HEADLINES.get(unique_id, "Service history")


def index() -> rx.Component:
    return rx.box(
        sp_timeline(
            HISTORY,
            OPTIONS,
            height="560px",
            label="Service history",
            on_change=TimelineState.on_slide,
            fallback=rx.text("The timeline could not load."),
        ),
        rx.text("Showing: ", TimelineState.current),
        max_width="960px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

En Reflex, `data` y `options` son los dos primeros argumentos. `on_change` llama al backend con el `unique_id`, y el estado guarda el titular. `fallback` acepta cualquier componente.

## Los eventos

| Evento | Cuándo | React | Vue | Angular | Reflex |
|---|---|---|---|---|---|
| Cambio | Se activa otra diapositiva; lleva su `unique_id` | `onChange` | `@change` | `(change)` | `on_change` |
| Carga | TimelineJS terminó de construirse | `onLoaded` | `@loaded` | `(loaded)` | `on_loaded` |
| Siguiente | Se pulsa la flecha derecha | `onNavNext` | `@nav-next` | `(navNext)` | `on_nav_next` |
| Anterior | Se pulsa la flecha izquierda | `onNavPrevious` | `@nav-previous` | `(navPrevious)` | `on_nav_previous` |
| Zoom | Se acerca o se aleja la escala | `onZoomIn`, `onZoomOut` | `@zoom-in`, `@zoom-out` | `(zoomIn)`, `(zoomOut)` | `on_zoom_in`, `on_zoom_out` |
| Inicio | Se vuelve a la primera diapositiva | `onBackToStart` | `@back-to-start` | `(backToStart)` | `on_back_to_start` |

## El contenido de reserva y SP025

TimelineJS se carga solo en el navegador y con una importación dinámica. Si esa carga falla, el componente muestra el contenido de reserva y avisa en la consola con `SP025`: TimelineJS no se pudo cargar.

Lo probé en Angular bloqueando el fragmento de TimelineJS: apareció «The timeline could not load.» y el aviso `SP025`. Dale siempre un contenido de reserva. Si no, la región se queda vacía.

## La nota de Vite

En desarrollo, Vite descubre la importación dinámica de TimelineJS cuando la página monta la línea de tiempo, no al arrancar. Entonces vuelve a optimizar las dependencias a mitad de sesión, cambia el `?v=` de cada una y la importación en curso falla con «error loading dynamically imported module». La línea de tiempo se queda en blanco.

La solución es pedirle a Vite que la empaquete al arrancar. En React y Vue, en `vite.config.ts`:

```ts
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: { include: ['@knight-lab/timelinejs'] },
})
```

Solo afecta al servidor de desarrollo: la compilación de producción no usa el optimizador. En Reflex, el `.web/vite.config.js` se genera en cada compilación; este blog lo resuelve con un plugin en `rxconfig.py`, `VitePrebundlePlugin`, que añade la misma línea.

## Un ejemplo real: las certificaciones de este blog

La [página del currículum](/resume) de este sitio tiene una línea de tiempo con mis certificaciones, hecha con `sp_timeline`. Así la usa `web/components/resume_sections.py`:

```python
sp_timeline(
    certifications_data,
    certifications_options,
    height="100%",
    label=t(lang, "Certifications", "Certificaciones"),
    fallback=sp_empty(
        description=t(
            lang,
            "The certifications timeline could not load.",
            "No se pudo cargar la línea de tiempo de certificaciones.",
        )
    ),
    on_change=CertificationsState.on_slide_change,
    id="certifications-timeline",
)
```

Lo que hay detrás:

* `certifications_data` sale de `assets/timeline.json`, que se carga al importar el módulo. Cada diapositiva recibe un `unique_id` determinista, y así `on_change` sabe qué certificado está activo.
* Las imágenes de los certificados se sirven desde una copia local, no desde Google Drive, que responde con 429 a las imágenes enlazadas desde otro sitio.
* `web/web.py` tiene la misma regla de `tl-icons` de este artículo y otra que pone EB Garamond, la fuente del sitio, en los textos de TimelineJS.
* `rxconfig.py` tiene el `VitePrebundlePlugin` de la nota anterior.

## El tamaño

TimelineJS no es ligero. En la compilación de React de este artículo, el fragmento de TimelineJS pesa 229 kB, 68 kB comprimido, y se carga aparte, solo cuando se monta la línea de tiempo. Su CSS y la fuente de iconos van en el CSS principal.

En Angular, la compilación de producción avisa de dos cosas. El paquete inicial supera por poco el presupuesto de 500 kB del proyecto, y el módulo `wicg-inert`, que usa TimelineJS, no es ESM. Las dos son avisos, no errores.

## Problemas comunes

* **La compilación no encuentra `@knight-lab/timelinejs`.** No está instalado: es una dependencia opcional.
* **La línea de tiempo vuelve a la primera diapositiva.** `data` u `options` se crean en cada render. Sácalos del componente.
* **Las flechas salen como cajas vacías.** Falta la regla de `tl-icons`.
* **La línea de tiempo no tiene marco.** Falta `@silverpoint/grounds/ui.css`.
* **En desarrollo, la línea de tiempo se queda en blanco con «error loading dynamically imported module».** Añade TimelineJS a `optimizeDeps.include`.
* **Se ve el contenido de reserva y la consola muestra `SP025`.** TimelineJS no se pudo cargar: revisa la instalación y la red.

## Lo que viene

La línea de tiempo cuenta lo que pasó. El [artículo 22](/blog/silverpoint_serie_22) lo presenta: diapositivas escritas en Markdown con la sintaxis de Marp, con gráficos de silverpoint vivos dentro, para la revisión semanal de operaciones.
