Title: Silverpoint, artículo 09: estilos base, sustratos y el proveedor
Date: 2026-11-11 15:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_9
Authors: Ernesto Crespo
Summary: Cómo dar un estilo común a toda una aplicación con silverpoint: los dos estilos base y sus sustratos, el proveedor en React, Vue, Angular y Reflex, las secciones con otro estilo y el orden de prioridad entre el gráfico, el panel y el proveedor.

En el [artículo 07](/blog/silverpoint_serie_7) vimos que cada gráfico acepta `ground`, `substrate` y `mode`. Repetirlos en cada gráfico funciona con uno o dos, pero en un panel de diez es fácil que uno se quede con otro sustrato. Para eso existe el proveedor: se declara una vez, arriba del todo, y todos los gráficos y componentes que hay debajo lo leen.

Este artículo es del nivel 2 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint). Muestra el proveedor en los cuatro frameworks, cómo una sección de la página puede tener su propio estilo y quién gana cuando el gráfico y el proveedor dicen cosas distintas.

## Lo que vas a construir

Dos copias del mismo panel, con las visitas por hora y las ventas por canal. La de la izquierda usa el estilo de toda la aplicación: el estilo base `silverpoint` sobre el sustrato ocre. La de la derecha está en una sección con su propio proveedor, en cianotipia.

![El mismo panel dos veces: a la izquierda en silverpoint sobre ocre, a la derecha en cianotipia](./images/silverpoint-serie-9.png)

Fíjate en la cifra de arriba: «63.844», con punto de miles. El idioma de los números se declara solo una vez, en el proveedor de la aplicación, y la sección en cianotipia lo hereda.

## Los dos estilos base

Un estilo base es la técnica de dibujo: el papel, las tintas y cómo se construye el tono. silverpoint trae dos.

| Estilo base | Sustratos | El tono se construye con |
|---|---|---|
| `silverpoint` (por defecto) | `cream` (por defecto), `green`, `blue`, `ochre` | La densidad del tramado; la línea va entintada a mano |
| `cyanotype` | `prussian` | El grosor de una línea blanca exacta; no hay tramado |

En `silverpoint`, una categoría más oscura no lleva otro color: lleva un tramado más denso. Por eso un gráfico se lee igual en escala de grises o impreso. `cyanotype` imita una copia al cianotipo: líneas blancas sobre azul de Prusia.

`cyanotype` tiene un único sustrato. Lo pinta siempre, diga lo que diga `substrate`, así que con ese estilo base no hace falta indicarlo.

El proveedor acepta cinco campos, los mismos que el gráfico lee de él:

| Campo | Qué fija |
|---|---|
| `ground` | El estilo base |
| `substrate` | El sustrato dentro del estilo base |
| `mode` | `ink`, con entintado a mano, o `precision`, con trazos exactos |
| `locale` | El idioma y la región de los números |
| `palette` | Los colores; las paletas tienen su propio artículo, el 12 |

## El panel

Los datos de las visitas son los del [artículo 03](/blog/silverpoint_serie_3): `traffic.ts`, con una fila `{ hour, hits }` por hora. Las ventas por canal van en `src/sales.ts`:

```ts
export type ChannelSales = {
  channel: string;
  sales: number;
};

export const sales: ChannelSales[] = [
  { channel: 'Web', sales: 46 },
  { channel: 'App', sales: 31 },
  { channel: 'Partners', sales: 15 },
  { channel: 'Phone', sales: 8 },
];
```

El panel, en `src/Panel.tsx`, no dice nada del estilo. Solo dibuja los dos gráficos:

```tsx
import { BarChart } from '@silverpoint/react/bar-chart';
import { LineChart } from '@silverpoint/react/line-chart';
import { sales } from './sales';
import { traffic } from './traffic';

export function Panel() {
  return (
    <section style={{ display: 'grid', gap: 16 }}>
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        value={63844}
        unit="requests at the peak"
      />
      <BarChart data={sales} xKey="channel" valueKey="sales" title="Sales by channel" />
    </section>
  );
}
```

En Vue y en Angular el panel es un componente con los mismos dos gráficos (`Panel.vue` y `panel.ts`), escritos con la sintaxis de los artículos 04 y 05.

## Un proveedor para toda la aplicación

### React

`SilverpointProvider` envuelve la aplicación en `src/main.tsx`:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { SilverpointProvider } from '@silverpoint/react';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <SilverpointProvider ground="silverpoint" substrate="ochre" locale="es-ES">
      <App />
    </SilverpointProvider>
  </StrictMode>,
);
```

### Vue

En Vue, el proveedor de la aplicación es un plugin. Se instala en `src/main.ts`:

```ts
import { createApp } from 'vue';
import { provideSilverpoint } from '@silverpoint/vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './style.css';
import App from './App.vue';

createApp(App)
  .use(provideSilverpoint({ ground: 'silverpoint', substrate: 'ochre', locale: 'es-ES' }))
  .mount('#app');
```

### Angular

En Angular es un proveedor más de la aplicación, en `src/app/app.config.ts`:

```ts
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideSilverpoint } from '@silverpoint/angular';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideSilverpoint({ ground: 'silverpoint', substrate: 'ochre', locale: 'es-ES' }),
  ],
};
```

### Reflex

En Reflex, `silverpoint_provider` es un componente que envuelve la página. Este es `ops_panel/ops_panel.py` completo, con el panel, el proveedor de la página y, dentro, la sección en cianotipia de la que hablamos enseguida:

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart, line_chart, silverpoint_provider

from .sales import SALES
from .traffic import TRAFFIC


def panel() -> rx.Component:
    return rx.el.section(
        line_chart(
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            value=63844,
            unit="requests at the peak",
        ),
        bar_chart(data=SALES, x_key="channel", value_key="sales", title="Sales by channel"),
        style={"display": "grid", "gap": "16px"},
    )


def index() -> rx.Component:
    return silverpoint_provider(
        rx.el.main(
            panel(),
            silverpoint_provider(panel(), ground="cyanotype"),
            style={
                "display": "grid",
                "grid_template_columns": "1fr 1fr",
                "gap": "24px",
                "max_width": "1040px",
                "padding": "32px",
            },
        ),
        ground="silverpoint",
        substrate="ochre",
        locale="es-ES",
    )


app = rx.App()
app.add_page(index)
```

`TRAFFIC` y `SALES` son las mismas filas, como listas de diccionarios, en `traffic.py` y `sales.py`.

Envolver cada página funciona, pero con varias páginas se repite. Reflex permite envolver la aplicación entera con `app.extra_app_wraps`, un diccionario de envoltorios que Reflex coloca alrededor de todas las páginas. Así lo hace este mismo blog: un único proveedor de silverpoint da el estilo a todos los gráficos del sitio. Con él, la página ya no necesita su propio proveedor:

```python
def index() -> rx.Component:
    return rx.el.main(
        panel(),
        silverpoint_provider(panel(), ground="cyanotype"),
        style={
            "display": "grid",
            "grid_template_columns": "1fr 1fr",
            "gap": "24px",
            "max_width": "1040px",
            "padding": "32px",
        },
    )


app = rx.App()
app.extra_app_wraps[(10, "SilverpointProvider")] = lambda _stateful: silverpoint_provider(
    ground="silverpoint",
    substrate="ochre",
    locale="es-ES",
)
app.add_page(index)
```

La clave es una tupla con el orden del envoltorio y un nombre. El valor es una función que recibe si la aplicación usa estado y devuelve el componente.

## Una sección con otro estilo base

Un proveedor dentro de otro da estilo a una sección de la página. Los campos que declara ganan; los que no declara los hereda del de fuera. Es lo que hace la mitad derecha del panel: solo cambia `ground`, y hereda `locale`.

En React, `src/App.tsx`:

```tsx
import { SilverpointProvider } from '@silverpoint/react';
import { Panel } from './Panel';

export default function App() {
  return (
    <main style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, maxWidth: 1040 }}>
      <Panel />
      <SilverpointProvider ground="cyanotype">
        <Panel />
      </SilverpointProvider>
    </main>
  );
}
```

En Vue, el plugin es para la aplicación y el componente `SilverpointProvider`, para una sección. No añade ningún elemento a la página, así que no cambia la maqueta. `src/App.vue`:

```vue
<script setup lang="ts">
import { SilverpointProvider } from '@silverpoint/vue';
import Panel from './Panel.vue';
</script>

<template>
  <main style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 1040px">
    <Panel />
    <SilverpointProvider ground="cyanotype">
      <Panel />
    </SilverpointProvider>
  </main>
</template>
```

En Angular, una sección es un componente con su propio `provideSilverpoint` en `providers`. `src/app/cyanotype-panel.ts`:

```ts
import { Component } from '@angular/core';
import { provideSilverpoint } from '@silverpoint/angular';
import { Panel } from './panel';

@Component({
  selector: 'app-cyanotype-panel',
  imports: [Panel],
  providers: [provideSilverpoint({ ground: 'cyanotype' })],
  template: `<app-panel />`,
})
export class CyanotypePanel {}
```

Y `src/app/app.ts` pone las dos secciones lado a lado:

```ts
import { Component } from '@angular/core';
import { CyanotypePanel } from './cyanotype-panel';
import { Panel } from './panel';

@Component({
  selector: 'app-root',
  imports: [Panel, CyanotypePanel],
  template: `
    <main style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 1040px">
      <app-panel />
      <app-cyanotype-panel />
    </main>
  `,
})
export class App {}
```

En Reflex ya lo viste en la función `index`: `silverpoint_provider(panel(), ground="cyanotype")` dentro del proveedor de la página.

Los cuatro dibujan la imagen del principio. En la sección en cianotipia, el sustrato `ochre` que viene del proveedor de fuera no tiene efecto: `cyanotype` pinta siempre su azul de Prusia.

## Quién gana

Cada campo se resuelve en este orden, y gana el primero que lo declara:

1. La prop del propio gráfico.
2. El panel (`Dashboard`) que lo contiene, que veremos en el artículo 13.
3. El proveedor más cercano y, si no lo declara, los de fuera.
4. El valor por defecto de la librería.

Un ejemplo en React:

```tsx
import { SilverpointProvider } from '@silverpoint/react';
import { LineChart } from '@silverpoint/react/line-chart';

export default function App() {
  return (
    <main style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, maxWidth: 1040 }}>
      <SilverpointProvider substrate="green" mode="precision">
        <LineChart title="Inherited" />
        <LineChart title="Own props" substrate="blue" mode="ink" />
      </SilverpointProvider>
    </main>
  );
}
```

El primer gráfico hereda el sustrato verde y el modo `precision`. El segundo declara los suyos y se dibuja sobre azul y con entintado a mano.

Hay una excepción que ninguna prop puede saltarse. Si el sistema pide más contraste (`prefers-contrast: more`) o colores forzados (`forced-colors: active`), todos los gráficos pasan a `precision`. Lo vemos en el artículo 10.

## Problemas comunes

* **Cambié `substrate` y la cianotipia sigue igual.** Es lo esperado: `cyanotype` solo tiene el sustrato `prussian` y lo pinta siempre.
* **Un gráfico no recibe el estilo del proveedor.** Está fuera de él. En React, comprueba que `SilverpointProvider` envuelve el componente que dibuja el gráfico; en Vue, que el plugin está instalado antes de `mount`.
* **Quiero cambiar el estilo mientras la aplicación corre.** En React, Vue y Reflex basta con cambiar las props del proveedor. En Angular, `provideSilverpoint` recibe un objeto fijo al crear el inyector, así que el cambio se hace en las entradas de los gráficos. El artículo 12 lo resuelve en los cuatro.

## Lo que viene

Con el proveedor, el estilo de la aplicación vive en un solo sitio. El artículo 10 entra en el modo `precision` y en la accesibilidad: qué cambia cuando se apaga el entintado, cómo se navega un gráfico con el teclado y qué lee un lector de pantalla.

La [documentación de los estilos base](https://silverpointweb.vercel.app/docs/grounds) tiene los dos estilos base y sus sustratos.
