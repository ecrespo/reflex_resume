Title: Silverpoint, artículo 02: el mapa de paquetes
Date: 2026-11-11 11:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_2
Authors: Ernesto Crespo
Summary: Los paquetes de silverpoint uno por uno: el motor, los estilos base, las fuentes, los adaptadores de React, Vue, Angular y Reflex, y los paquetes opcionales. Qué instalar en cada caso y por qué.

El [artículo 01](/blog/silverpoint_serie_1) explicó las ideas de [silverpoint](https://github.com/ecrespo/silverpoint): el sustrato, el tramado, el realce único y la geometría exacta. Este artículo, el último del nivel de fundamentos, recorre los paquetes que forman la librería: qué hace cada uno, cuáles instalas tú y cuáles llegan solos.

Al terminar sabrás qué instalar para tu framework, qué hoja de estilos importar y de dónde sale cada componente. Los artículos 03 a 06 parten de aquí para dibujar el primer gráfico.

## El mapa

El proyecto es un monorepo con nueve paquetes de npm y un paquete de Python aparte. Todos los paquetes de npm salen juntos con el mismo número de versión, hoy la 0.9.2. Así se relacionan:

```text
                      @silverpoint/core
                              |
                    @silverpoint/grounds
                              |
        +---------------------+---------------------+
        |                     |                     |
@silverpoint/react    @silverpoint/vue    @silverpoint/angular
        |
reflex-silverpoint-react  (Python, PyPI)

@silverpoint/fonts   @silverpoint/tailwind   @silverpoint/marp   @silverpoint/mcp
```

Hay tres capas. Abajo del todo está el motor, que calcula. Encima, los estilos base, que deciden cómo se dibuja. Arriba, un adaptador por framework, que convierte el resultado en componentes. Los cuatro paquetes de la última línea son opcionales.

| Paquete | Qué hace | ¿Lo instalas tú? |
|---|---|---|
| `@silverpoint/core` | El motor: geometría, escalas, interacción, paletas y tipos | Casi nunca: llega con el adaptador |
| `@silverpoint/grounds` | Los estilos base y la hoja de estilos que colorea los trazos | Sí, porque importas su CSS |
| `@silverpoint/fonts` | La tipografía EB Garamond, alojada en tu propia aplicación | Opcional, recomendado |
| `@silverpoint/react` | Los componentes de React | Sí, si usas React |
| `@silverpoint/vue` | Los componentes de Vue | Sí, si usas Vue |
| `@silverpoint/angular` | Los componentes de Angular | Sí, si usas Angular |
| `reflex-silverpoint-react` | Los componentes para Reflex, en Python | Sí, si usas Reflex |
| `@silverpoint/tailwind` | Un preset de Tailwind con las variables de silverpoint | Opcional |
| `@silverpoint/marp` | Presentaciones en Markdown con gráficos vivos | Opcional |
| `@silverpoint/mcp` | Un servidor MCP para asistentes de IA | Opcional |

## El motor: `@silverpoint/core`

Todo lo que se calcula vive en el motor: las escalas, los ejes, los arcos, los trazados, la interacción y las paletas. No contiene ni una línea de DOM ni de ningún framework, y no depende de ellos. Sus únicas dependencias son tres módulos de d3 (`d3-scale`, `d3-shape` y `d3-chord`).

Esta separación es la que permite que los cuatro frameworks dibujen exactamente lo mismo, como vimos en el artículo 01: la geometría se calcula una sola vez, en un solo sitio.

No suele hacer falta instalarlo, porque cada adaptador depende de él. Lo instalas a mano cuando tu propio código importa algo del motor, por ejemplo sus tipos o sus paletas:

```sh
npm install @silverpoint/core
```

```ts
import type { ProviderConfig } from '@silverpoint/core';
import { checkPalette, sanguine } from '@silverpoint/core/palettes';

export const config: ProviderConfig = { ground: 'silverpoint', substrate: 'cream', mode: 'ink' };

console.log(checkPalette(sanguine));
console.log(checkPalette({ ...sanguine, ink: '#D8C8B0' }));
```

`checkPalette` mide el contraste de una paleta. Con `sanguine`, una de las seis paletas incluidas, devuelve una lista vacía: no hay nada que corregir. Con una tinta demasiado clara devuelve tres incumplimientos: la tinta (1,35:1, por debajo del 4,5:1 exigido), el anillo de foco y el contorno del realce blanco.

El motor tiene una entrada principal y cuatro secundarias. Cada aplicación solo carga lo que usa:

| Entrada | Contiene |
|---|---|
| `@silverpoint/core` | El motor y los tipos de todos los gráficos |
| `@silverpoint/core/catalog` | Los 27 gráficos del segundo catálogo (histograma, diagrama de caja, sunburst, red…) |
| `@silverpoint/core/ui` | Las vistas de los 38 componentes de interfaz |
| `@silverpoint/core/palettes` | Las seis paletas, `checkPalette` y `contrastRatio` |
| `@silverpoint/core/timeline` | Lo que comparten los adaptadores para la línea de tiempo |

## Los estilos base: `@silverpoint/grounds`

Un estilo base (*ground*) es el conjunto de decisiones de dibujo: el sustrato, las tintas, cómo se entinta el trazo y cómo se construye el tono. Este paquete trae los dos que existen hoy:

| Estilo base | El tono se construye con | Sustratos |
|---|---|---|
| `silverpoint` (por defecto) | Tramado dibujado a mano | `cream`, `green`, `blue`, `ochre` |
| `cyanotype` | El grosor de una línea blanca exacta sobre azul de Prusia | `prussian` |

Aquí vive también el entintado a mano: el paquete depende de rough.js, y el motor nunca lo toca directamente.

Lo más importante de este paquete para quien lo usa es su hoja de estilos. Sin ella, los trazos no tienen color. Se importa una sola vez, en la raíz de la aplicación. Hay tres:

| Hoja de estilos | Para qué | ¿Obligatoria? |
|---|---|---|
| `@silverpoint/grounds/styles.css` | Los gráficos | Sí |
| `@silverpoint/grounds/ui.css` | Los 38 componentes de interfaz | Solo si los usas |
| `@silverpoint/grounds/timeline.css` | La línea de tiempo `SpTimeline` | Solo si la usas |

Un detalle sobre la instalación: el adaptador ya depende de `@silverpoint/grounds`, pero conviene declararlo en tu `package.json` porque tu código importa su CSS directamente. Con pnpm es obligatorio, ya que pnpm no deja importar paquetes que no estén declarados.

## La tipografía: `@silverpoint/fonts`

Los gráficos están diseñados para EB Garamond. Este paquete la incluye en tres variantes (400, 500 y 400 cursiva) en formato `woff2`, con sus reglas `@font-face`. Tu empaquetador copia los archivos, así que no hay ninguna petición a un CDN de fuentes.

Es opcional. Sin él, los gráficos usan `'Iowan Old Style', Georgia, serif` y, en desarrollo, lo avisan con el diagnóstico `SP013`.

## Los adaptadores

Cada framework tiene su adaptador, y cada adaptador trae los mismos 60 gráficos, los 38 componentes de interfaz, el panel y la línea de tiempo, con las mismas props.

| Adaptador | Requisitos | Particularidades |
|---|---|---|
| `@silverpoint/react` | React y React DOM 18.2 o 19 | Componentes de cliente y entradas `server/` para React Server Components |
| `@silverpoint/vue` | Vue 3.5 | Componentes con `<script setup>`; render en servidor con `@vue/server-renderer` |
| `@silverpoint/angular` | Angular 21 o 22 (`@angular/core`, `@angular/common` y `@angular/forms`) | Componentes standalone con signal inputs y `OnPush`; funcionan sin zone.js |

Los tres necesitan un empaquetador: Vite, Next.js o el Angular CLI, que son los que el proyecto valida, sin configuración extra.

La instalación es la misma en los tres: el adaptador, los estilos base y la tipografía.

```sh
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
npm install @silverpoint/vue @silverpoint/grounds @silverpoint/fonts
npm install @silverpoint/angular @silverpoint/grounds @silverpoint/fonts
```

Y las hojas de estilos se importan una vez. En React y en Vue, en el archivo de entrada o en el componente raíz:

```ts
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
```

En Angular, en `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';
```

La tercera línea solo hace falta si usas los componentes de interfaz. Los ejemplos de abajo usan uno, así que la incluyen.

## Una entrada por componente

Ningún adaptador obliga a cargar los 60 gráficos para usar uno. Cada gráfico y cada componente de interfaz tiene su propia ruta de importación, y en tu aplicación solo entra lo que importas:

| Importas | Desde |
|---|---|
| Un gráfico | `@silverpoint/<framework>/bar-chart`, `@silverpoint/<framework>/line-chart`… |
| Un componente de interfaz | `@silverpoint/<framework>/ui/button`, `@silverpoint/<framework>/ui/modal`… |
| El panel | `@silverpoint/<framework>/dashboard` |
| La línea de tiempo | `@silverpoint/<framework>/timeline` |
| Una presentación | `@silverpoint/<framework>/deck` |
| Un gráfico para React Server Components | `@silverpoint/react/server/bar-chart`… |

Este es un gráfico de barras junto a un botón en los tres frameworks. Sin `data`, un gráfico dibuja sus propios datos de demostración, lo que viene bien para probar que todo está instalado. En React:

```tsx
import { BarChart } from '@silverpoint/react/bar-chart';
import { SpButton } from '@silverpoint/react/ui/button';

export function Entries() {
  return (
    <div style={{ width: 480 }}>
      <BarChart title="hits" />
      <SpButton>Save</SpButton>
    </div>
  );
}
```

En Vue:

```vue
<script setup lang="ts">
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import { SpBarChart } from '@silverpoint/vue/bar-chart';
import { SpButton } from '@silverpoint/vue/ui/button';
</script>

<template>
  <div style="width: 480px">
    <SpBarChart title="hits" />
    <SpButton>Save</SpButton>
  </div>
</template>
```

En Angular, el botón es una directiva sobre el `<button>` nativo, así que conserva todo su comportamiento de serie:

```ts
import { Component } from '@angular/core';
import { SpBarChart } from '@silverpoint/angular/bar-chart';
import { SpButton } from '@silverpoint/angular/ui/button';

@Component({
  selector: 'app-root',
  imports: [SpBarChart, SpButton],
  template: `
    <div style="width: 480px">
      <sp-bar-chart title="hits" />
      <button spButton type="button">Save</button>
    </div>
  `,
})
export class App {}
```

Los nombres siguen una regla fija. En React, el gráfico se llama como en el catálogo (`BarChart`) y los componentes de interfaz llevan el prefijo `Sp` (`SpButton`). En Vue, todos llevan el prefijo `Sp` (`SpBarChart`). En Angular, la clase lleva `Sp` y la etiqueta, `sp-` (`<sp-bar-chart>`).

## Reflex: un solo paquete de Python

Para Reflex hay un único paquete, `reflex-silverpoint-react`, que se publica en PyPI con su propio número de versión. La 0.9.1 envuelve `@silverpoint/react` 0.9.1, requiere Reflex 0.10 y Python 3.11 o posterior.

```sh
pip install reflex-silverpoint-react
```

O con uv:

```sh
uv add reflex-silverpoint-react
```

No hay nada que hacer en el lado de JavaScript. Al compilar, Reflex instala `@silverpoint/react`, `@silverpoint/core`, `@silverpoint/grounds` y `@silverpoint/fonts` en las versiones que fija el paquete, y cada componente importa las hojas de estilos que necesita. Tampoco hay rutas de importación por componente: todo sale del mismo módulo, con los nombres en `snake_case`.

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart, check_palette, sp_button

print(check_palette("sanguine"))
print(check_palette({"ink": "#D8C8B0"}))


def index() -> rx.Component:
    return rx.box(
        bar_chart(title="hits"),
        sp_button("Save"),
        width="480px",
    )


app = rx.App()
app.add_page(index)
```

Las dos llamadas a `check_palette` se ejecutan al cargar la aplicación e imprimen:

```text
[]
['ink #D8C8B0 on #EDE7DA: 1.33:1, below 4.5:1', 'focus #D8C8B0 on #EDE7DA: 1.33:1, below 3.0:1']
```

Es la misma comprobación que `checkPalette` del motor. Las cifras cambian un poco respecto al ejemplo de JavaScript porque esta paleta no indica sustrato y se mide contra el crema por defecto.

## Los paquetes opcionales

Ninguno de estos es necesario para dibujar un gráfico. Llegarán en su artículo correspondiente.

* **`@silverpoint/tailwind`**: un preset para Tailwind 4 (`theme.css`) y Tailwind 3.4 que nombra las variables de silverpoint como clases (`bg-sp-substrate`, `text-sp-ink`, `font-sp-display`). Sirve para que el resto de la página use la tinta y el sustrato de los gráficos. La librería no necesita Tailwind: todo el tema va en variables CSS.
* **`@silverpoint/marp`**: presentaciones escritas en Markdown con la sintaxis de Marp, dibujadas en el estilo de silverpoint y con gráficos vivos dentro. Se usa a través de la entrada `deck` de cada adaptador. Es una dependencia opcional: solo la instalas si haces presentaciones. Lo veremos en el artículo 22.
* **`@silverpoint/mcp`**: un servidor MCP que describe la librería a un asistente de IA (el catálogo, las props, una recomendación de gráfico para tus datos) y escribe el código en React, Vue, Angular o Reflex. Hay una versión alojada, de solo lectura y sin cuenta, que se conecta a Claude Code así:

```sh
claude mcp add --transport http silverpoint https://silverpointweb.vercel.app/mcp
```

Y también funciona en local con `npx @silverpoint/mcp`. Lo veremos en el artículo 28.

La línea de tiempo tiene una dependencia opcional más, `@knight-lab/timelinejs`, que solo instalas si usas `SpTimeline` (artículo 21).

## Qué instalar, en resumen

| Usas | Instala | Importa una vez |
|---|---|---|
| React | `@silverpoint/react @silverpoint/grounds @silverpoint/fonts` | `fonts.css`, `styles.css` y, si usas la interfaz, `ui.css` |
| Vue | `@silverpoint/vue @silverpoint/grounds @silverpoint/fonts` | Lo mismo |
| Angular | `@silverpoint/angular @silverpoint/grounds @silverpoint/fonts` | Lo mismo, con `@import` en `src/styles.css` |
| Reflex | `reflex-silverpoint-react` | Nada: lo hace el paquete |

Con esto termina el nivel de fundamentos. En el nivel 1 cada framework tiene su artículo para dibujar el primer gráfico con datos propios: el 03 con React y Vite, el 04 con Vue, el 05 con Angular y el 06 con Reflex.

Mientras tanto, la [documentación](https://silverpointweb.vercel.app/docs/react) tiene una guía por framework, y la [galería](https://silverpointweb.vercel.app/gallery) muestra los 60 gráficos en vivo.
