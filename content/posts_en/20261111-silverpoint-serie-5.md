Title: Silverpoint, article 05: your first chart in Angular
Date: 2026-11-11 13:00
Category: Tutorial Silverpoint
Tags: silverpoint, angular, Visualización
lang: en
translation: true
Slug: silverpoint_serie_5
Authors: Ernesto Crespo
Summary: Step by step, from a new Angular CLI project to the first silverpoint chart in Angular 22: installation, global styles, your own data, the card text and loading the data with HttpClient and signals.

This is the Angular article of level 1 of the series on [silverpoint](https://github.com/ecrespo/silverpoint). It builds the same chart that [article 03](/blog/silverpoint_serie_3) builds in React and [04](/blog/silverpoint_serie_4) in Vue. You can read this one alone: everything is installed from scratch here.

## What you will build

The first piece of the series' operations panel: a line chart with the hits per hour to a web service over the last 24 hours, in thousands.

![The hits-per-hour chart, drawn with Angular](./images/silverpoint-serie-5.png)

By the end you will have the chart with your own data, the card text and the data loaded with `HttpClient` from a JSON file, as you would with an API.

## What you need

* Node.js 22.22 or later, or 24.15 or later. That is what Angular 22 asks for.
* npm, which comes with Node.
* Knowing the basics of Angular: standalone components, templates and signals.

The silverpoint adapter works with Angular 21 and 22. This article uses 22.

## 1. Create the project

```sh
npx @angular/cli@22 new ops-panel --defaults --skip-git
cd ops-panel
```

`--defaults` accepts the default options without asking, and the CLI installs the dependencies. The project it generates does not use zone.js: change detection runs on signals, and so do the silverpoint components.

## 2. Install silverpoint

The Angular adapter, the base styles and the typeface:

```sh
npm install @silverpoint/angular @silverpoint/grounds @silverpoint/fonts
```

The adapter brings the engine, `@silverpoint/core`, as a dependency.

## 3. The global styles

In Angular, the silverpoint stylesheets go in the global styles. Replace the contents of `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';

body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

The two `@import` lines load the typeface and the base styles. The other rules are only for the page.

## 4. The first chart

The root component will carry its template inline, so delete `src/app/app.html`, `src/app/app.css` and `src/app/app.spec.ts`. The template test looks for the welcome page title, which no longer exists.

Replace `src/app/app.ts`:

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

Start the development server:

```sh
npm start
```

And open `http://localhost:4200`. You will see a line chart with twelve hours and two series: the solid line and a dotted baseline.

It is the chart's demo data: when it does not receive `data`, it draws its own. It is there to check that the installation works. If you see the cream background and the fine stroke, the global styles are right.

Each chart is a standalone component with its own entry point (`@silverpoint/angular/line-chart`), so your application only includes the ones you import. The class carries the `Sp` prefix and the tag, `sp-`.

## 5. Your own data

Create `src/app/traffic.ts` with one day of hits, one row per hour:

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

Declare the row type with `type`, not with `interface`. The `data` input accepts rows of type `Record<string, unknown>`, and an `interface` is not compatible with that type. If you use `interface`, the build fails with "Type 'HourlyTraffic[]' is not assignable to type 'readonly Readonly<Record<string, unknown>>[]'".

Pass the data to the chart and complete the card. Replace `src/app/app.ts`:

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

The inputs have the same names as the React props. The ones that receive a literal text are written as attributes (`xKey="hour"`). The ones that receive an expression carry brackets (`[data]`, `[height]`).

| Input | What it does |
|---|---|
| `data` | The rows that are drawn |
| `xKey` | The field of each row that goes on the horizontal axis |
| `valueKey` | The field with the value the line draws |
| `title` | The card title |
| `badge` | A short label, top right |
| `value` and `unit` | The highlighted value and its unit, below the title |
| `footerLeft` and `footerRight` | The card footer |
| `height` | The height of the drawing area in pixels; 160 by default |

The width is not set: the chart takes its container's, the 640-pixel `<main>`.

The white heightened point is at the end of the line, not at the peak. It is the single heightening rule from article 01: in a line chart, the live value is heightened, the last one of the series. The peak is told by the highlighted value and the footer.

## 6. Load the data with HttpClient

In a real panel the data comes from an API. To simulate it, create `public/traffic.json` with a timestamp and the number of requests per hour:

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

The CLI serves the `public/` folder at the root, so the file ends up at `/traffic.json`.

To request it with `HttpClient`, the application needs its provider. Replace `src/app/app.config.ts`:

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

And replace `src/app/app.ts` with the version that loads the data:

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

Three decisions in this version:

* **The data is adapted before it reaches the chart.** `toHourly` turns each API row into a chart row: the hour comes from the timestamp and the requests become thousands.
* **While there is no data, there is no chart.** `peak` is `null` while `traffic` is empty, and the `@if` block shows "Loading…". Do not pass an empty array to the chart: with empty data it draws its empty state, "No data", not the demo data.
* **The chart follows the signals.** When `traffic.set` changes the signal, `peak` is recomputed and the chart's inputs change. The silverpoint components use `OnPush` and signal inputs, so they redraw without zone.js.

## 7. Build for production

```sh
npm run build
```

The output lands in `dist/ops-panel/browser`. With this project, the initial bundle weighs about 362 kB, about 101 kB in the estimated transfer size the CLI reports, Angular included. The global stylesheet weighs 7.7 kB.

## Common problems

* **The line appears filled in black and there is loose text below the chart.** The `@import` lines are missing from `src/styles.css`. Without `@silverpoint/grounds/styles.css`, the strokes have no colour and the data table that should be hidden shows.
* **The chart does not appear.** Its container has no width. The chart waits until it can measure it and, in development, the console shows the `SP003` diagnostic.
* **The card says "No data".** The name in `xKey` or `valueKey` does not match the fields of the rows. In development, the console shows `SP002` with the name of the field.
* **The build fails with "Type 'string' is not assignable to type 'number'".** A numeric input is written as an attribute. `height="200"` passes the text `"200"`; the right form is `[height]="200"`.
* **The page stays blank and the console shows an injection error about `HttpClient`.** `provideHttpClient()` is missing from `src/app/app.config.ts`.
* **When you rest the pointer on the chart, the browser's own tooltip with the title also appears.** Angular leaves the literal text `title="Hits per hour"` as a `title` attribute of the `sp-line-chart` element. If it bothers you, write it as an expression, `[title]="'Hits per hour'"`. It is a bug open as [silverpoint#18](https://github.com/ecrespo/silverpoint/issues/18); it will be fixed in a coming version of the package.

The `SP0xx` diagnostics only appear in development.

## What comes next

You now have a silverpoint chart in Angular with your own data. If you use Angular, the next one on your route is 07: the properties the 60 charts share. Article 06 builds this same chart in Reflex, with Python only.

The [Angular guide](https://silverpointweb.vercel.app/docs/angular) in the documentation has more examples.
