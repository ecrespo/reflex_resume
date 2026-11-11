Title: Silverpoint, artículo 04: tu primer gráfico en Vue 3
Date: 2026-11-11 12:30
Category: Tutorial Silverpoint
Tags: silverpoint, vue, Visualización
lang: es
translation: true
Slug: silverpoint_serie_4
Authors: Ernesto Crespo
Summary: Paso a paso, de un proyecto vacío de Vite al primer gráfico de silverpoint en Vue 3: instalación, hojas de estilos, datos propios, el texto de la tarjeta y la carga de datos desde un JSON con ref y computed.

Este es el artículo de Vue del nivel 1 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint). Construye el mismo gráfico que el [artículo 03](/blog/silverpoint_serie_3) construye en React, así que puedes leer solo este: aquí se instala todo desde cero.

## Lo que vas a construir

La primera pieza del panel de operaciones de la serie: un gráfico de línea con las visitas por hora a un servicio web durante las últimas 24 horas, en miles.

![El gráfico de visitas por hora, dibujado con Vue](./images/silverpoint-serie-4.png)

Al terminar tendrás el gráfico con tus propios datos, el texto de la tarjeta y los datos cargados desde un archivo JSON, como harías con una API.

## Lo que necesitas

* Node.js 20.19 o posterior, o 22.12 o posterior. Es lo que pide Vite 8.
* npm, que viene con Node.
* Conocer lo básico de Vue 3: componentes con `<script setup>`, `ref` y `computed`.

## 1. Crear el proyecto

```sh
npm create vite@latest ops-panel -- --template vue-ts --no-interactive
cd ops-panel
npm install
```

La opción `--no-interactive` evita que el asistente de Vite haga preguntas. Sin ella, puede ofrecerte instalar y arrancar el proyecto; si lo hace, responde que no y sigue con estos pasos.

## 2. Instalar silverpoint

El adaptador de Vue, los estilos base y la tipografía:

```sh
npm install @silverpoint/vue @silverpoint/grounds @silverpoint/fonts
```

El adaptador requiere Vue 3.5 o posterior, que es la versión que instala la plantilla, y trae el motor, `@silverpoint/core`, como dependencia.

## 3. Preparar el punto de entrada

Las hojas de estilos se importan una sola vez. Sustituye el contenido de `src/main.ts`:

```ts
import { createApp } from 'vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './style.css';
import App from './App.vue';

createApp(App).mount('#app');
```

Sustituye `src/style.css`, que trae los estilos de la página de bienvenida, por unas pocas reglas:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

Y borra las carpetas `src/components` y `src/assets`, que solo usaba esa página de bienvenida.

## 4. El primer gráfico

Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { SpLineChart } from '@silverpoint/vue/line-chart';
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart title="Hits per hour" />
  </main>
</template>
```

Arranca el servidor de desarrollo:

```sh
npm run dev
```

Y abre `http://localhost:5173`. Verás un gráfico de línea con doce horas y dos series: la línea continua y una línea base punteada.

Son los datos de demostración del gráfico: cuando no recibe `data`, dibuja los suyos. Sirven para comprobar que la instalación funciona. Si ves el fondo crema y el trazo fino, las hojas de estilos y la tipografía están bien cargadas.

En Vue, todos los componentes de silverpoint llevan el prefijo `Sp`, y cada uno tiene su propia ruta de importación (`@silverpoint/vue/line-chart`), así que tu aplicación solo incluye los que usas.

## 5. Tus propios datos

Crea `src/traffic.ts` con las visitas de un día, una fila por hora:

```ts
export type HourlyTraffic = {
  hour: string;
  hits: number;
};

export const traffic: HourlyTraffic[] = [
  { hour: '00', hits: 18 },
  { hour: '01', hits: 14 },
  { hour: '02', hits: 11 },
  { hour: '03', hits: 9 },
  { hour: '04', hits: 11 },
  { hour: '05', hits: 16 },
  { hour: '06', hits: 24 },
  { hour: '07', hits: 33 },
  { hour: '08', hits: 42 },
  { hour: '09', hits: 51 },
  { hour: '10', hits: 58 },
  { hour: '11', hits: 62 },
  { hour: '12', hits: 64 },
  { hour: '13', hits: 61 },
  { hour: '14', hits: 59 },
  { hour: '15', hits: 58 },
  { hour: '16', hits: 57 },
  { hour: '17', hits: 52 },
  { hour: '18', hits: 47 },
  { hour: '19', hits: 41 },
  { hour: '20', hits: 30 },
  { hour: '21', hits: 26 },
  { hour: '22', hits: 22 },
  { hour: '23', hits: 20 },
];
```

Pasa los datos al gráfico y completa la tarjeta. Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { SpLineChart } from '@silverpoint/vue/line-chart';
import { traffic } from './traffic';

const peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart
      :data="traffic"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      badge="Today"
      :value="peak.hits"
      unit="k hits at the peak"
      footer-left="Last 24 hours"
      :footer-right="`Peak at ${peak.hour}:00`"
      :height="200"
    />
  </main>
</template>
```

En las plantillas de Vue, las props se escriben en `kebab-case` (`x-key`, `footer-left`). Las que reciben un valor de JavaScript, y no un texto literal, llevan dos puntos delante (`:data`, `:height`).

| Prop | Qué hace |
|---|---|
| `data` | Las filas que se dibujan |
| `x-key` | El campo de cada fila que va en el eje horizontal |
| `value-key` | El campo con el valor que dibuja la línea |
| `title` | El título de la tarjeta |
| `badge` | Una etiqueta corta, arriba a la derecha |
| `value` y `unit` | El valor destacado y su unidad, bajo el título |
| `footer-left` y `footer-right` | El pie de la tarjeta |
| `height` | El alto del área de dibujo en píxeles; por defecto, 160 |

El ancho no se indica: el gráfico toma el de su contenedor, el `<main>` de 640 píxeles.

El punto realzado en blanco está al final de la línea, no en el pico. Es la regla del realce único del artículo 01: en un gráfico de línea, se realza el valor vivo, el último de la serie. El pico lo cuentan el valor destacado y el pie.

## 6. Cargar los datos desde un JSON

En un panel real los datos llegan de una API. Para simularlo, crea `public/traffic.json` con una marca de tiempo y el número de peticiones por hora:

```json
[
  {"time": "2026-11-11T00:00:00Z", "requests": 17800},
  {"time": "2026-11-11T01:00:00Z", "requests": 13937},
  {"time": "2026-11-11T02:00:00Z", "requests": 11074},
  {"time": "2026-11-11T03:00:00Z", "requests": 8811},
  {"time": "2026-11-11T04:00:00Z", "requests": 10948},
  {"time": "2026-11-11T05:00:00Z", "requests": 16085},
  {"time": "2026-11-11T06:00:00Z", "requests": 23822},
  {"time": "2026-11-11T07:00:00Z", "requests": 32959},
  {"time": "2026-11-11T08:00:00Z", "requests": 42096},
  {"time": "2026-11-11T09:00:00Z", "requests": 50833},
  {"time": "2026-11-11T10:00:00Z", "requests": 57970},
  {"time": "2026-11-11T11:00:00Z", "requests": 62107},
  {"time": "2026-11-11T12:00:00Z", "requests": 63844},
  {"time": "2026-11-11T13:00:00Z", "requests": 60981},
  {"time": "2026-11-11T14:00:00Z", "requests": 59118},
  {"time": "2026-11-11T15:00:00Z", "requests": 57855},
  {"time": "2026-11-11T16:00:00Z", "requests": 56992},
  {"time": "2026-11-11T17:00:00Z", "requests": 52129},
  {"time": "2026-11-11T18:00:00Z", "requests": 46866},
  {"time": "2026-11-11T19:00:00Z", "requests": 41003},
  {"time": "2026-11-11T20:00:00Z", "requests": 30140},
  {"time": "2026-11-11T21:00:00Z", "requests": 25877},
  {"time": "2026-11-11T22:00:00Z", "requests": 22014},
  {"time": "2026-11-11T23:00:00Z", "requests": 20151}
]
```

Vite sirve `public/` tal cual, en `/traffic.json`. Sustituye `src/App.vue` por la versión que lo carga:

```vue
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { SpLineChart } from '@silverpoint/vue/line-chart';
import type { HourlyTraffic } from './traffic';

type ApiRow = { time: string; requests: number };

const toHourly = (rows: ApiRow[]): HourlyTraffic[] =>
  rows.map((row) => ({
    hour: row.time.slice(11, 13),
    hits: Math.round(row.requests / 1000),
  }));

const traffic = ref<HourlyTraffic[] | null>(null);

const peak = computed(() =>
  traffic.value?.reduce((max, row) => (row.hits > max.hits ? row : max)),
);

onMounted(async () => {
  const response = await fetch('/traffic.json');
  traffic.value = toHourly(await response.json());
});
</script>

<template>
  <main style="max-width: 640px">
    <p v-if="!traffic || !peak">Loading…</p>
    <SpLineChart
      v-else
      :data="traffic"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      badge="Today"
      :value="peak.hits"
      unit="k hits at the peak"
      footer-left="Last 24 hours"
      :footer-right="`Peak at ${peak.hour}:00`"
      :height="200"
    />
  </main>
</template>
```

Tres decisiones de esta versión:

* **Los datos se adaptan antes de llegar al gráfico.** `toHourly` convierte cada fila de la API en una fila del gráfico: la hora sale de la marca de tiempo y las peticiones pasan a miles.
* **Mientras no hay datos, no hay gráfico.** La plantilla muestra «Loading…» hasta que llega la respuesta. No le pases un array vacío: un gráfico con datos vacíos dibuja su estado vacío, «No data», y no los datos de demostración.
* **El gráfico es reactivo.** `traffic` es un `ref` y `peak` un `computed`. Cuando cambian, Vue actualiza las props y silverpoint redibuja. Si mañana cargas los datos cada minuto, no hay que hacer nada más.

## 7. Compilar para producción

```sh
npm run build
npm run preview
```

`npm run build` comprueba los tipos con `vue-tsc` y genera la versión de producción en `dist/`. Con este proyecto, el JavaScript ocupa unos 166 kB, 59 kB comprimido con gzip, incluido Vue. La hoja de estilos ocupa 7,5 kB. `npm run preview` sirve esa versión en `http://localhost:4173`.

## Problemas comunes

* **La línea aparece rellena de negro y hay texto suelto debajo del gráfico.** Falta `@silverpoint/grounds/styles.css` en `src/main.ts`. Sin esa hoja, los trazos no tienen color y se ve la tabla de datos que debería estar oculta.
* **El gráfico no aparece.** Su contenedor no tiene ancho. El gráfico espera a poder medirlo y, en desarrollo, la consola muestra el diagnóstico `SP003`.
* **La tarjeta dice «No data».** El nombre de `x-key` o de `value-key` no coincide con los campos de las filas. En desarrollo, la consola muestra `SP002` con el nombre del campo.
* **La compilación falla con «Type 'string' is not assignable to type 'number'».** A una prop que recibe un número, un array o un objeto le faltan los dos puntos. `height="200"` pasa el texto `"200"`; lo correcto es `:height="200"`.

Los diagnósticos `SP0xx` solo aparecen en desarrollo.

## Lo que viene

Ya tienes un gráfico de silverpoint en Vue con tus propios datos. Si usas Vue, el siguiente de tu ruta es el 07: las propiedades que comparten los 60 gráficos. Los artículos 05 y 06 construyen este mismo gráfico en Angular y en Reflex.

La [guía de Vue](https://silverpointweb.vercel.app/docs/vue) de la documentación tiene más ejemplos.
