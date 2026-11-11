Title: Silverpoint, artículo 05: tu primer gráfico en Angular
Date: 2026-11-11 13:00
Category: Tutorial Silverpoint
Tags: silverpoint, angular, Visualización
lang: es
translation: true
Slug: silverpoint_serie_5
Authors: Ernesto Crespo
Summary: Paso a paso, de un proyecto nuevo del Angular CLI al primer gráfico de silverpoint en Angular 22: instalación, estilos globales, datos propios, el texto de la tarjeta y la carga de datos con HttpClient y signals.

Este es el artículo de Angular del nivel 1 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint). Construye el mismo gráfico que el [artículo 03](/blog/silverpoint_serie_3) construye en React y el [04](/blog/silverpoint_serie_4) en Vue. Puedes leer solo este: aquí se instala todo desde cero.

## Lo que vas a construir

La primera pieza del panel de operaciones de la serie: un gráfico de línea con las visitas por hora a un servicio web durante las últimas 24 horas, en miles.

![El gráfico de visitas por hora, dibujado con Angular](./images/silverpoint-serie-5.png)

Al terminar tendrás el gráfico con tus propios datos, el texto de la tarjeta y los datos cargados con `HttpClient` desde un archivo JSON, como harías con una API.

## Lo que necesitas

* Node.js 22.22 o posterior, o 24.15 o posterior. Es lo que pide Angular 22.
* npm, que viene con Node.
* Conocer lo básico de Angular: componentes standalone, plantillas y signals.

El adaptador de silverpoint funciona con Angular 21 y 22. Este artículo usa la 22.

## 1. Crear el proyecto

```sh
npx @angular/cli@22 new ops-panel --defaults --skip-git
cd ops-panel
```

`--defaults` acepta las opciones por defecto sin preguntar, y el CLI instala las dependencias. El proyecto que genera no usa zone.js: la detección de cambios funciona con signals, y los componentes de silverpoint también.

## 2. Instalar silverpoint

El adaptador de Angular, los estilos base y la tipografía:

```sh
npm install @silverpoint/angular @silverpoint/grounds @silverpoint/fonts
```

El adaptador trae el motor, `@silverpoint/core`, como dependencia.

## 3. Los estilos globales

En Angular, las hojas de estilos de silverpoint van en los estilos globales. Sustituye el contenido de `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';

body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

Las dos líneas `@import` cargan la tipografía y los estilos base. Las demás reglas son solo para la página.

## 4. El primer gráfico

El componente raíz llevará la plantilla en línea, así que borra `src/app/app.html`, `src/app/app.css` y `src/app/app.spec.ts`. La prueba de la plantilla busca el título de la página de bienvenida, que deja de existir.

Sustituye `src/app/app.ts`:

```ts
import { Component } from '@angular/core';
import { SpLineChart } from '@silverpoint/angular/line-chart';

@Component({
  selector: 'app-root',
  imports: [SpLineChart],
  template: `
    <main style="max-width: 640px">
      <sp-line-chart title="Hits per hour" />
    </main>
  `,
})
export class App {}
```

Arranca el servidor de desarrollo:

```sh
npm start
```

Y abre `http://localhost:4200`. Verás un gráfico de línea con doce horas y dos series: la línea continua y una línea base punteada.

Son los datos de demostración del gráfico: cuando no recibe `data`, dibuja los suyos. Sirven para comprobar que la instalación funciona. Si ves el fondo crema y el trazo fino, los estilos globales están bien.

Cada gráfico es un componente standalone con su propio punto de entrada (`@silverpoint/angular/line-chart`), así que tu aplicación solo incluye los que importas. La clase lleva el prefijo `Sp` y la etiqueta, `sp-`.

## 5. Tus propios datos

Crea `src/app/traffic.ts` con las visitas de un día, una fila por hora:

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

Declara el tipo de la fila con `type`, no con `interface`. El input `data` acepta filas de tipo `Record<string, unknown>`, y una `interface` no es compatible con ese tipo. Si usas `interface`, la compilación falla con «Type 'HourlyTraffic[]' is not assignable to type 'readonly Readonly<Record<string, unknown>>[]'».

Pasa los datos al gráfico y completa la tarjeta. Sustituye `src/app/app.ts`:

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
        [data]="traffic"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        [value]="peak.hits"
        unit="k hits at the peak"
        footerLeft="Last 24 hours"
        [footerRight]="'Peak at ' + peak.hour + ':00'"
        [height]="200"
      />
    </main>
  `,
})
export class App {
  protected readonly traffic = traffic;
  protected readonly peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));
}
```

Los inputs se llaman igual que las props de React. Los que reciben un texto literal se escriben como atributos (`xKey="hour"`). Los que reciben una expresión llevan corchetes (`[data]`, `[height]`).

| Input | Qué hace |
|---|---|
| `data` | Las filas que se dibujan |
| `xKey` | El campo de cada fila que va en el eje horizontal |
| `valueKey` | El campo con el valor que dibuja la línea |
| `title` | El título de la tarjeta |
| `badge` | Una etiqueta corta, arriba a la derecha |
| `value` y `unit` | El valor destacado y su unidad, bajo el título |
| `footerLeft` y `footerRight` | El pie de la tarjeta |
| `height` | El alto del área de dibujo en píxeles; por defecto, 160 |

El ancho no se indica: el gráfico toma el de su contenedor, el `<main>` de 640 píxeles.

El punto realzado en blanco está al final de la línea, no en el pico. Es la regla del realce único del artículo 01: en un gráfico de línea, se realza el valor vivo, el último de la serie. El pico lo cuentan el valor destacado y el pie.

## 6. Cargar los datos con HttpClient

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

El CLI sirve la carpeta `public/` en la raíz, así que el archivo queda en `/traffic.json`.

Para pedirlo con `HttpClient`, la aplicación necesita su proveedor. Sustituye `src/app/app.config.ts`:

```ts
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(),
  ],
};
```

Y sustituye `src/app/app.ts` por la versión que carga los datos:

```ts
import { Component, computed, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import type { HourlyTraffic } from './traffic';

type ApiRow = { time: string; requests: number };

const toHourly = (rows: ApiRow[]): HourlyTraffic[] =>
  rows.map((row) => ({
    hour: row.time.slice(11, 13),
    hits: Math.round(row.requests / 1000),
  }));

@Component({
  selector: 'app-root',
  imports: [SpLineChart],
  template: `
    <main style="max-width: 640px">
      @if (peak(); as peak) {
        <sp-line-chart
          [data]="traffic()"
          xKey="hour"
          valueKey="hits"
          title="Hits per hour"
          badge="Today"
          [value]="peak.hits"
          unit="k hits at the peak"
          footerLeft="Last 24 hours"
          [footerRight]="'Peak at ' + peak.hour + ':00'"
          [height]="200"
        />
      } @else {
        <p>Loading…</p>
      }
    </main>
  `,
})
export class App {
  protected readonly traffic = signal<HourlyTraffic[]>([]);
  protected readonly peak = computed(() =>
    this.traffic().reduce<HourlyTraffic | null>(
      (max, row) => (max && max.hits >= row.hits ? max : row),
      null,
    ),
  );

  constructor() {
    inject(HttpClient)
      .get<ApiRow[]>('/traffic.json')
      .subscribe((rows) => this.traffic.set(toHourly(rows)));
  }
}
```

Tres decisiones de esta versión:

* **Los datos se adaptan antes de llegar al gráfico.** `toHourly` convierte cada fila de la API en una fila del gráfico: la hora sale de la marca de tiempo y las peticiones pasan a miles.
* **Mientras no hay datos, no hay gráfico.** `peak` vale `null` mientras `traffic` está vacío, y el bloque `@if` muestra «Loading…». No le pases un array vacío al gráfico: con datos vacíos dibuja su estado vacío, «No data», y no los datos de demostración.
* **El gráfico sigue a los signals.** Cuando `traffic.set` cambia el signal, `peak` se recalcula y los inputs del gráfico cambian. Los componentes de silverpoint usan `OnPush` y signal inputs, así que redibujan sin zone.js.

## 7. Compilar para producción

```sh
npm run build
```

El resultado queda en `dist/ops-panel/browser`. Con este proyecto, el paquete inicial ocupa unos 362 kB, unos 101 kB en la transferencia estimada que informa el CLI, incluido Angular. La hoja de estilos global ocupa 7,7 kB.

## Problemas comunes

* **La línea aparece rellena de negro y hay texto suelto debajo del gráfico.** Faltan los `@import` en `src/styles.css`. Sin `@silverpoint/grounds/styles.css`, los trazos no tienen color y se ve la tabla de datos que debería estar oculta.
* **El gráfico no aparece.** Su contenedor no tiene ancho. El gráfico espera a poder medirlo y, en desarrollo, la consola muestra el diagnóstico `SP003`.
* **La tarjeta dice «No data».** El nombre de `xKey` o de `valueKey` no coincide con los campos de las filas. En desarrollo, la consola muestra `SP002` con el nombre del campo.
* **La compilación falla con «Type 'string' is not assignable to type 'number'».** Un input numérico está escrito como atributo. `height="200"` pasa el texto `"200"`; lo correcto es `[height]="200"`.
* **La página se queda en blanco y la consola muestra un error de inyección sobre `HttpClient`.** Falta `provideHttpClient()` en `src/app/app.config.ts`.
* **Al dejar el puntero sobre el gráfico aparece también la descripción emergente del navegador con el título.** Angular deja el texto literal `title="Hits per hour"` como atributo `title` del elemento `sp-line-chart`. Si te molesta, escríbelo como expresión, `[title]="'Hits per hour'"`. Es un fallo abierto como [silverpoint#18](https://github.com/ecrespo/silverpoint/issues/18); se corregirá en una próxima versión del paquete.

Los diagnósticos `SP0xx` solo aparecen en desarrollo.

## Lo que viene

Ya tienes un gráfico de silverpoint en Angular con tus propios datos. Si usas Angular, el siguiente de tu ruta es el 07: las propiedades que comparten los 60 gráficos. El artículo 06 construye este mismo gráfico en Reflex, solo con Python.

La [guía de Angular](https://silverpointweb.vercel.app/docs/angular) de la documentación tiene más ejemplos.
