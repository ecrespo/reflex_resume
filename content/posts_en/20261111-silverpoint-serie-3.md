Title: Silverpoint, article 03: your first chart in React with Vite
Date: 2026-11-11 12:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, Visualización
lang: en
translation: true
Slug: silverpoint_serie_3
Authors: Ernesto Crespo
Summary: Step by step, from an empty Vite project to the first silverpoint chart in React: installation, stylesheets, your own data, the card text and loading the data from a JSON file.

This article starts level 1 of the series on [silverpoint](https://github.com/ecrespo/silverpoint): the first steps. Articles 03, 04, 05 and 06 build exactly the same chart, each one in a framework. This is the React one, with Vite.

If you have not read [article 02](/blog/silverpoint_serie_2), the map of packages, you do not need to: everything is installed from scratch here.

## What you will build

The project of the series is an operations panel for a web service. Its first piece is a line chart with the hits per hour over the last 24 hours, in thousands:

![The hits-per-hour chart built in this article](./images/silverpoint-serie-3.png)

By the end you will have the chart with your own data, with the card text (title, highlighted value, footer) and loading the data from a JSON file, as you would with an API.

## What you need

* Node.js 20.19 or later, or 22.12 or later. That is what Vite 8 asks for.
* npm, which comes with Node.
* An editor. No previous experience with silverpoint is needed, but you should know the basics of React: components, props and `useState`.

## 1. Create the project

Vite creates a React project with TypeScript in a single command:

```sh
npm create vite@latest ops-panel -- --template react-ts --no-interactive
cd ops-panel
npm install
```

The `--no-interactive` option keeps Vite's wizard from asking questions. Without it, it may offer to install and start the project; if it does, answer no and go on with these steps.

## 2. Install silverpoint

Three packages: the React adapter, the base styles and the typeface.

```sh
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
```

The adapter brings the engine, `@silverpoint/core`, as a dependency. Article 02 explains what each package does.

## 3. Prepare the entry point

The silverpoint stylesheets are imported once, in the entry file. Replace the contents of `src/main.tsx` with this:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

The Vite template brings demo styles we do not need. Replace `src/index.css` with a few rules for the page:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

And delete `src/App.css` and the `src/assets` folder, which only Vite's welcome page used.

## 4. The first chart

Replace `src/App.tsx` with this:

```tsx
import { LineChart } from '@silverpoint/react/line-chart';

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart title="Hits per hour" />
    </main>
  );
}
```

Start the development server:

```sh
npm run dev
```

And open `http://localhost:5173`. You will see a line chart with twelve hours and two series: the solid line and a dotted baseline.

That data is not yours. When a chart does not receive the `data` prop, it draws its own demo set. It is there to check that the installation works before you write a single line of data. If you see the chart with the cream background and the fine stroke, the stylesheets and the typeface are loaded correctly.

Look at the import: `@silverpoint/react/line-chart`. Each chart has its own path, so your application only includes the ones you use.

## 5. Your own data

Create `src/traffic.ts` with one day of hits, one row per hour:

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

A TypeScript detail: the row type is declared with `type`, not with `interface`. The `data` prop accepts rows of type `Record<string, unknown>`, and an `interface` is not compatible with that type. If you use `interface`, the build fails with the error "Index signature for type 'string' is missing in type 'HourlyTraffic'".

Now pass the data to the chart and complete the card. Replace `src/App.tsx`:

```tsx
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from './traffic';

const peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        value={peak.hits}
        unit="k hits at the peak"
        footerLeft="Last 24 hours"
        footerRight={`Peak at ${peak.hour}:00`}
        height={200}
      />
    </main>
  );
}
```

Vite reloads the page on its own. The props you just used:

| Prop | What it does |
|---|---|
| `data` | The rows that are drawn |
| `xKey` | The field of each row that goes on the horizontal axis |
| `valueKey` | The field with the value the line draws |
| `title` | The card title |
| `badge` | A short label, top right |
| `value` and `unit` | The highlighted value and its unit, below the title |
| `footerLeft` and `footerRight` | The card footer |
| `height` | The height of the drawing area in pixels; 160 by default |

The width is not set: the chart takes its container's, here the 640-pixel `<main>`.

There is a visual detail worth understanding. The white heightened point is at the end of the line, not at the peak. It is the single heightening rule from article 01: in a line chart, the heightened element is the live value, the last one of the series. The peak is told by the highlighted value and the footer.

## 6. Load the data from a JSON file

In a real panel the data comes from an API. To simulate it, create `public/traffic.json` with the typical format of a metrics API: a timestamp and the number of requests.

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

Vite serves what is in `public/` as is, so the file is available at `/traffic.json`. Replace `src/App.tsx` with the version that loads it:

```tsx
import { useEffect, useState } from 'react';
import { LineChart } from '@silverpoint/react/line-chart';
import type { HourlyTraffic } from './traffic';

type ApiRow = { time: string; requests: number };

const toHourly = (rows: ApiRow[]): HourlyTraffic[] =>
  rows.map((row) => ({
    hour: row.time.slice(11, 13),
    hits: Math.round(row.requests / 1000),
  }));

export default function App() {
  const [traffic, setTraffic] = useState<HourlyTraffic[] | null>(null);

  useEffect(() => {
    fetch('/traffic.json')
      .then((response) => response.json())
      .then((rows: ApiRow[]) => setTraffic(toHourly(rows)));
  }, []);

  if (!traffic) {
    return <p>Loading…</p>;
  }

  const peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        value={peak.hits}
        unit="k hits at the peak"
        footerLeft="Last 24 hours"
        footerRight={`Peak at ${peak.hour}:00`}
        height={200}
      />
    </main>
  );
}
```

Three decisions in this version:

* **The data is adapted before it reaches the chart.** The `toHourly` function turns each API row into a chart row: the hour comes from the timestamp and the requests become thousands. The chart knows nothing about the API, and `src/traffic.ts` keeps only the type.
* **While there is no data, there is no chart.** The component shows "Loading…" until the response arrives. Do not pass it an empty array: a chart with `data={[]}` draws its empty state, "No data", not the demo data.
* **The chart redraws on its own.** When `setTraffic` changes the state, React renders again and silverpoint draws the new rows. If tomorrow you load the data every minute, there is nothing else to do.

## 7. Build for production

```sh
npm run build
npm run preview
```

`npm run build` checks the types with TypeScript and generates the production version in `dist/`. With this project, the JavaScript weighs about 316 kB, 101 kB gzipped, React included. The stylesheet weighs 7.5 kB, and the three cuts of EB Garamond about 25 kB each. `npm run preview` serves that version at `http://localhost:4173` to check it.

## Common problems

* **The line appears filled in black and there is loose text below the chart.** `@silverpoint/grounds/styles.css` is missing. Without that stylesheet, the strokes have no colour and the data table, which should be hidden for screen readers, shows.
* **The chart does not appear.** The container has no width, for example an element in a flexible row with no size. The chart waits until it can measure it and, in development, the console shows the `SP003` diagnostic. Give the container a width.
* **The card says "No data".** The name in `xKey` or `valueKey` does not match the fields of the rows. In development, the console shows `SP002` with the name of the field it did not find.
* **The build fails with "Index signature … is missing".** The row type is declared with `interface`. Change it to `type`.

The `SP0xx` diagnostics only appear in development. In production, the library does not write to the console.

## What comes next

You now have a silverpoint chart in React with your own data. Articles 04, 05 and 06 build this same chart in Vue, Angular and Reflex. If you use React, you can skip to 07: the properties the 60 charts share, with which you will tune this one and any other.

The [React guide](https://silverpointweb.vercel.app/docs/react) in the documentation has more examples.
