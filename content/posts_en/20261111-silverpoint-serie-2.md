Title: Silverpoint, article 02: the map of packages
Date: 2026-11-11 11:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: en
translation: true
Slug: silverpoint_serie_2
Authors: Ernesto Crespo
Summary: The silverpoint packages one by one: the engine, the grounds, the fonts, the React, Vue, Angular and Reflex adapters, and the optional packages. What to install in each case and why.

[Article 01](/blog/silverpoint_serie_1) explained the ideas behind [silverpoint](https://github.com/ecrespo/silverpoint): the substrate, the hatching, the single heightening and the exact geometry. This article, the last of the fundamentals level, walks through the packages that make up the library: what each one does, which ones you install and which ones arrive on their own.

By the end you will know what to install for your framework, which stylesheet to import and where each component comes from. Articles 03 to 06 start from here to draw the first chart.

## The map

The project is a monorepo with nine npm packages and a separate Python package. All the npm packages are released together with the same version number, 0.9.2 today. This is how they relate:

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

There are three layers. At the bottom is the engine, which computes. Above it, the grounds, which decide how things are drawn. On top, one adapter per framework, which turns the result into components. The four packages on the last line are optional.

| Package | What it does | Do you install it? |
|---|---|---|
| `@silverpoint/core` | The engine: geometry, scales, interaction, palettes and types | Almost never: it comes with the adapter |
| `@silverpoint/grounds` | The grounds and the stylesheet that colours the strokes | Yes, because you import its CSS |
| `@silverpoint/fonts` | The EB Garamond typeface, hosted in your own application | Optional, recommended |
| `@silverpoint/react` | The React components | Yes, if you use React |
| `@silverpoint/vue` | The Vue components | Yes, if you use Vue |
| `@silverpoint/angular` | The Angular components | Yes, if you use Angular |
| `reflex-silverpoint-react` | The components for Reflex, in Python | Yes, if you use Reflex |
| `@silverpoint/tailwind` | A Tailwind preset with the silverpoint variables | Optional |
| `@silverpoint/marp` | Markdown slide decks with live charts | Optional |
| `@silverpoint/mcp` | An MCP server for AI assistants | Optional |

## The engine: `@silverpoint/core`

Everything that is computed lives in the engine: the scales, the axes, the arcs, the paths, the interaction and the palettes. It holds not a single line of DOM or framework code, and it depends on neither. Its only dependencies are three d3 modules (`d3-scale`, `d3-shape` and `d3-chord`).

This separation is what lets the four frameworks draw exactly the same thing, as we saw in article 01: the geometry is computed once, in one place.

You rarely need to install it, because every adapter depends on it. You install it by hand when your own code imports something from the engine, such as its types or its palettes:

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

`checkPalette` measures the contrast of a palette. With `sanguine`, one of the six bundled palettes, it returns an empty list: there is nothing to fix. With an ink that is too light it returns three failures: the ink (1.35:1, below the required 4.5:1), the focus ring and the outline of the white heightening.

The engine has one main entry and four secondary ones. Each application only loads what it uses:

| Entry | Holds |
|---|---|
| `@silverpoint/core` | The engine and the types of every chart |
| `@silverpoint/core/catalog` | The 27 charts of the second catalog (histogram, box plot, sunburst, network…) |
| `@silverpoint/core/ui` | The views of the 38 UI components |
| `@silverpoint/core/palettes` | The six palettes, `checkPalette` and `contrastRatio` |
| `@silverpoint/core/timeline` | What the adapters share for the timeline |

## The grounds: `@silverpoint/grounds`

A ground is the set of drawing decisions: the substrate, the inks, how the stroke is inked and how tone is built. This package brings the two that exist today:

| Ground | Tone is built from | Substrates |
|---|---|---|
| `silverpoint` (default) | Hatching drawn by hand | `cream`, `green`, `blue`, `ochre` |
| `cyanotype` | The weight of an exact white line on Prussian blue | `prussian` |

The hand inking lives here too: the package depends on rough.js, and the engine never touches it directly.

The most important part of this package for its users is its stylesheet. Without it, the strokes have no colour. It is imported once, at the root of the application. There are three:

| Stylesheet | What for | Required? |
|---|---|---|
| `@silverpoint/grounds/styles.css` | The charts | Yes |
| `@silverpoint/grounds/ui.css` | The 38 UI components | Only if you use them |
| `@silverpoint/grounds/timeline.css` | The `SpTimeline` timeline | Only if you use it |

A note on installation: the adapter already depends on `@silverpoint/grounds`, but it is worth declaring it in your `package.json` because your code imports its CSS directly. With pnpm it is mandatory, since pnpm does not let you import packages you have not declared.

## The typeface: `@silverpoint/fonts`

The charts are designed for EB Garamond. This package includes it in three cuts (400, 500 and 400 italic) in `woff2` format, with their `@font-face` rules. Your bundler copies the files, so there is no request to a font CDN.

It is optional. Without it, the charts use `'Iowan Old Style', Georgia, serif` and, in development, report it with the `SP013` diagnostic.

## The adapters

Each framework has its adapter, and each adapter brings the same 60 charts, the 38 UI components, the dashboard and the timeline, with the same props.

| Adapter | Requirements | Particulars |
|---|---|---|
| `@silverpoint/react` | React and React DOM 18.2 or 19 | Client components and `server/` entries for React Server Components |
| `@silverpoint/vue` | Vue 3.5 | Components written with `<script setup>`; server rendering with `@vue/server-renderer` |
| `@silverpoint/angular` | Angular 21 or 22 (`@angular/core`, `@angular/common` and `@angular/forms`) | Standalone components with signal inputs and `OnPush`; they work without zone.js |

All three need a bundler: Vite, Next.js or the Angular CLI, the ones the project validates, with no extra configuration.

Installation is the same in all three: the adapter, the grounds and the typeface.

```sh
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
npm install @silverpoint/vue @silverpoint/grounds @silverpoint/fonts
npm install @silverpoint/angular @silverpoint/grounds @silverpoint/fonts
```

And the stylesheets are imported once. In React and Vue, in the entry file or in the root component:

```ts
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
```

In Angular, in `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';
```

The third line is only needed if you use the UI components. The examples below use one, so they include it.

## One entry per component

No adapter makes you load the 60 charts to use one. Each chart and each UI component has its own import path, and only what you import ends up in your application:

| You import | From |
|---|---|
| A chart | `@silverpoint/<framework>/bar-chart`, `@silverpoint/<framework>/line-chart`… |
| A UI component | `@silverpoint/<framework>/ui/button`, `@silverpoint/<framework>/ui/modal`… |
| The dashboard | `@silverpoint/<framework>/dashboard` |
| The timeline | `@silverpoint/<framework>/timeline` |
| A slide deck | `@silverpoint/<framework>/deck` |
| A chart for React Server Components | `@silverpoint/react/server/bar-chart`… |

This is a bar chart next to a button in the three frameworks. Without `data`, a chart draws its own demo data, which is handy to check that everything is installed. In React:

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

In Vue:

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

In Angular, the button is a directive on the native `<button>`, so it keeps all of its built-in behaviour:

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

Names follow a fixed rule. In React, a chart is named as in the catalog (`BarChart`) and the UI components carry the `Sp` prefix (`SpButton`). In Vue, all of them carry the `Sp` prefix (`SpBarChart`). In Angular, the class carries `Sp` and the tag, `sp-` (`<sp-bar-chart>`).

## Reflex: a single Python package

For Reflex there is a single package, `reflex-silverpoint-react`, published on PyPI with its own version number. Version 0.9.1 wraps `@silverpoint/react` 0.9.1 and requires Reflex 0.10 and Python 3.11 or later.

```sh
pip install reflex-silverpoint-react
```

Or with uv:

```sh
uv add reflex-silverpoint-react
```

There is nothing to do on the JavaScript side. When it compiles, Reflex installs `@silverpoint/react`, `@silverpoint/core`, `@silverpoint/grounds` and `@silverpoint/fonts` at the versions the package pins, and each component imports the stylesheets it needs. Nor are there import paths per component: everything comes from the same module, with `snake_case` names.

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

The two `check_palette` calls run when the application loads and print:

```text
[]
['ink #D8C8B0 on #EDE7DA: 1.33:1, below 4.5:1', 'focus #D8C8B0 on #EDE7DA: 1.33:1, below 3.0:1']
```

It is the same check as the engine's `checkPalette`. The figures differ slightly from the JavaScript example because this palette names no substrate and is measured against the default cream.

## The optional packages

None of these is needed to draw a chart. Each will come in its own article.

* **`@silverpoint/tailwind`**: a preset for Tailwind 4 (`theme.css`) and Tailwind 3.4 that names the silverpoint variables as classes (`bg-sp-substrate`, `text-sp-ink`, `font-sp-display`). It lets the rest of the page use the ink and the substrate of the charts. The library does not need Tailwind: the whole theme goes through CSS variables.
* **`@silverpoint/marp`**: slide decks written in Markdown with Marp's syntax, drawn in the silverpoint style and with live charts inside. It is used through each adapter's `deck` entry. It is an optional dependency: you only install it if you make slide decks. We will see it in article 22.
* **`@silverpoint/mcp`**: an MCP server that describes the library to an AI assistant (the catalog, the props, a chart recommendation for your data) and writes the code in React, Vue, Angular or Reflex. There is a hosted version, read-only and without an account, that connects to Claude Code like this:

```sh
claude mcp add --transport http silverpoint https://silverpointweb.vercel.app/mcp
```

It also runs locally with `npx @silverpoint/mcp`. We will see it in article 28.

The timeline has one more optional dependency, `@knight-lab/timelinejs`, which you only install if you use `SpTimeline` (article 21).

## What to install, in short

| You use | Install | Import once |
|---|---|---|
| React | `@silverpoint/react @silverpoint/grounds @silverpoint/fonts` | `fonts.css`, `styles.css` and, if you use the UI, `ui.css` |
| Vue | `@silverpoint/vue @silverpoint/grounds @silverpoint/fonts` | The same |
| Angular | `@silverpoint/angular @silverpoint/grounds @silverpoint/fonts` | The same, with `@import` in `src/styles.css` |
| Reflex | `reflex-silverpoint-react` | Nothing: the package does it |

This ends the fundamentals level. In level 1 each framework has its own article to draw the first chart with your own data: 03 with React and Vite, 04 with Vue, 05 with Angular and 06 with Reflex.

Meanwhile, the [documentation](https://silverpointweb.vercel.app/docs/react) has a guide per framework, and the [gallery](https://silverpointweb.vercel.app/gallery) shows the 60 charts live.
