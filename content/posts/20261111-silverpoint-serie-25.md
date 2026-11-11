Title: Silverpoint, artículo 25: proyecto final en Angular, el panel de operaciones de principio a fin
Date: 2026-11-11 22:30
Category: Tutorial Silverpoint
Tags: silverpoint, angular, Visualización
lang: es
translation: true
Slug: silverpoint_serie_25
Authors: Ernesto Crespo
Summary: El panel de operaciones completo en Angular 22 con silverpoint: tres páginas con el router, componentes standalone y signals, datos en vivo, paneles enlazados, exportación a SVG, una tabla de incidencias con modal y aviso, un formulario de alertas y un tema que cambia toda la aplicación desde el proveedor.

Los artículos anteriores de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) enseñaron cada pieza por separado. Este las junta en una aplicación de Angular: Operations, el panel de operaciones del servicio web, con tres páginas.

Es la misma aplicación que los artículos 23 (React con Next.js), 24 (Vue) y 26 (Reflex). El 27 compara las cuatro. Aquí se construye con lo que Angular trae: el CLI, el router, componentes standalone y signals, sin librerías de estado.

![La página Overview de Operations en Angular: dos tarjetas de indicadores, las visitas por hora en vivo con la hora 12 activa, los errores por hora enlazados, el mapa de calor de errores por día y las ventas por canal](./images/silverpoint-serie-25.png)

## Lo que vas a construir

| Ruta | Página | Lo que usa |
|---|---|---|
| `/` | Overview | Un panel con indicadores, visitas en vivo, errores enlazados por hora, mapa de calor y donut; la lectura de la hora activa; la descarga en SVG |
| `/incidents` | Incidents | La tabla de incidencias ordenable y paginada, el modal para reconocer una y el aviso |
| `/settings` | Settings | El formulario de la regla de alerta y el tema: paleta y estilo base |

Cada página reúne artículos anteriores:

| Pieza | Artículo |
|---|---|
| El proyecto de Angular | [05](/blog/silverpoint_serie_5) |
| El proveedor y los estilos base | [09](/blog/silverpoint_serie_9) |
| El elemento activo | [11](/blog/silverpoint_serie_11) |
| Paletas y cambio de tema | [12](/blog/silverpoint_serie_12) |
| El panel y el enlace por hora | [13](/blog/silverpoint_serie_13) |
| El formulario | [16](/blog/silverpoint_serie_16) |
| Tabla, modal y aviso | [17](/blog/silverpoint_serie_17) |
| La exportación a SVG | [18](/blog/silverpoint_serie_18) |
| Los datos en vivo | [20](/blog/silverpoint_serie_20) |

## Lo que necesitas

El proyecto de Angular del artículo 05, creado con el CLI de Angular 22 y con `@silverpoint/angular`, `@silverpoint/grounds` y `@silverpoint/fonts` 0.9.2. El router y los formularios reactivos vienen con el proyecto.

Añade el motor como dependencia propia:

```bash
npm install @silverpoint/core
```

Ya estaba instalado, porque lo trae el adaptador. Pero la aplicación importa de él las paletas, `uiSortRows` y algunos tipos, y lo que importas debe estar en tu `package.json`.

## La estructura

```text
ops-panel
├── angular.json
├── package.json
├── package-lock.json
├── public
│   └── favicon.ico
├── README.md
├── src
│   ├── app
│   │   ├── app.config.ts
│   │   ├── app.routes.ts
│   │   ├── app.ts
│   │   ├── data
│   │   │   ├── incidents.ts
│   │   │   └── ops.ts
│   │   ├── export-svg.ts
│   │   ├── incident-log.ts
│   │   ├── live-feed.ts
│   │   ├── pages
│   │   │   ├── alert-rule-form.ts
│   │   │   ├── incidents.ts
│   │   │   ├── overview.ts
│   │   │   └── settings-page.ts
│   │   └── settings.ts
│   ├── index.html
│   ├── main.ts
│   ├── styles.css
│   └── text-imports.d.ts
├── tsconfig.app.json
├── tsconfig.json
└── tsconfig.spec.json
```

`main.ts` e `index.html` son los del CLI; en `index.html` solo cambia el título. Los datos de `src/app/data/` son los de la serie: `ops.ts`, del artículo 13, y `incidents.ts`, del 17, sin cambios. El resto se explica a continuación.

## 1. Las rutas

`src/app/app.routes.ts`:

```ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    title: 'Overview · Operations',
    loadComponent: () => import('./pages/overview').then((m) => m.Overview),
  },
  {
    path: 'incidents',
    title: 'Incidents · Operations',
    loadComponent: () => import('./pages/incidents').then((m) => m.Incidents),
  },
  {
    path: 'settings',
    title: 'Settings · Operations',
    loadComponent: () => import('./pages/settings-page').then((m) => m.SettingsPage),
  },
  { path: '**', redirectTo: '' },
];
```

Cada página se carga con `loadComponent`, así que el CLI la pone en su propio archivo y el navegador la descarga la primera vez que la visitas. `title` cambia el título de la pestaña. Cualquier otra ruta vuelve a Overview.

## 2. Los ajustes: un servicio con signals

El tema y la regla de alerta se usan en varias páginas. Viven en un servicio de toda la aplicación, `src/app/settings.ts`:

```ts
import { Injectable, computed, effect, signal } from '@angular/core';
import type { GroundName, Palette } from '@silverpoint/core';
import { indigo, ironGall, sanguine, sepia, silverpoint, verdigris } from '@silverpoint/core/palettes';

export const PALETTES: { key: string; label: string; palette: Palette }[] = [
  { key: 'silverpoint', label: 'Silverpoint', palette: silverpoint },
  { key: 'sanguine', label: 'Sanguine', palette: sanguine },
  { key: 'sepia', label: 'Sepia', palette: sepia },
  { key: 'iron-gall', label: 'Iron gall', palette: ironGall },
  { key: 'verdigris', label: 'Verdigris', palette: verdigris },
  { key: 'indigo', label: 'Indigo', palette: indigo },
];

export type AlertRule = {
  metric: string;
  threshold: number;
  channel: string;
  active: boolean;
  notes: string;
};

type Stored = { paletteKey: string; cyanotype: boolean };

const KEY = 'operations-theme';
const DEFAULTS: Stored = { paletteKey: 'silverpoint', cyanotype: false };

// localStorage can be missing or blocked: the app then keeps the theme in memory.
function load(): Stored {
  try {
    return { ...DEFAULTS, ...JSON.parse(localStorage.getItem(KEY) ?? 'null') };
  } catch {
    return DEFAULTS;
  }
}

@Injectable({ providedIn: 'root' })
export class Settings {
  readonly paletteKey = signal(load().paletteKey);
  readonly cyanotype = signal(load().cyanotype);
  readonly rule = signal<AlertRule>({
    metric: 'errors',
    threshold: 10,
    channel: 'email',
    active: true,
    notes: '',
  });

  readonly ground = computed<GroundName>(() => (this.cyanotype() ? 'cyanotype' : 'silverpoint'));
  // Cyanotype prints with its own inks on Prussian blue: no palette on top.
  readonly palette = computed(() =>
    this.cyanotype() ? undefined : PALETTES.find((p) => p.key === this.paletteKey())?.palette,
  );

  constructor() {
    effect(() => {
      const stored: Stored = { paletteKey: this.paletteKey(), cyanotype: this.cyanotype() };
      try {
        localStorage.setItem(KEY, JSON.stringify(stored));
      } catch {
        // Not saved: the theme lasts until the page is reloaded.
      }
    });
  }
}
```

Un servicio con `providedIn: 'root'` existe una vez y dura lo que dura la página. No hace falta una librería de estado: los signals ya avisan a quien los lee.

El tema se guarda en `localStorage`, dentro de `try`/`catch`. En una ventana privada o con el almacenamiento bloqueado, `localStorage` puede lanzar un error; entonces el tema dura hasta que recargues. La regla de alerta solo se guarda en memoria, para la sesión.

Con el estilo base `cyanotype` no se aplica paleta: la cianotipia imprime con sus propias tintas sobre azul de Prusia, y una paleta pensada para papel claro no se leería.

## 3. El proveedor que sigue al tema

El artículo 09 configuraba el estilo de toda la aplicación con `provideSilverpoint`. En Angular, esa función recibe un objeto fijo: no hay forma de cambiarle el estilo base después. Por eso el artículo 12 pasaba el tema a cada gráfico.

Aquí se usa otra vía. `src/app/app.config.ts` registra el mismo token que usa `provideSilverpoint`, `SILVERPOINT_CONFIG`, con un objeto cuyos campos leen los ajustes:

```ts
import { ApplicationConfig, inject, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import type { ProviderConfig } from '@silverpoint/core';
import { SILVERPOINT_CONFIG } from '@silverpoint/angular/env';
import { routes } from './app.routes';
import { Settings } from './settings';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    {
      // provideSilverpoint() takes a fixed object. This provider reads the
      // settings on every render, so every chart and component follows them.
      provide: SILVERPOINT_CONFIG,
      useFactory: (): ProviderConfig => {
        const settings = inject(Settings);
        return {
          get ground() {
            return settings.ground();
          },
          get palette() {
            return settings.palette();
          },
        };
      },
    },
  ],
};
```

Funciona porque los gráficos y los componentes de silverpoint leen el proveedor dentro de un `computed`. Al leer `ground`, el getter lee `settings.ground()`, y Angular anota esa dependencia. Cuando cambias el tema, cada gráfico y cada componente se vuelve a dibujar con el nuevo.

Lo comprobé quitando todas las demás vías: sin pasar el tema a ningún gráfico, los seis gráficos, la tabla, los botones y los controles cambian de paleta y de estilo base. Es un uso del token que la documentación no describe, así que compruébalo si actualizas silverpoint.

`SILVERPOINT_CONFIG` se importa de `@silverpoint/angular/env`. Desde `@silverpoint/angular` también existe, pero arrastra unos 42 kB más al paquete inicial, y el CLI avisa de que se pasa del presupuesto de 500 kB.

## 4. El marco de la aplicación

`src/app/app.ts` es el componente raíz: la barra de navegación, el `router-outlet` y los colores de la página.

```ts
import { Component, computed, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { paletteStyle } from '@silverpoint/core/palettes';
import { Settings } from './settings';

@Component({
  selector: 'app-root',
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  template: `
    <div class="shell" [class]="'sp-ground-' + settings.ground()" data-substrate="cream" [style]="inks()">
      <header>
        <strong>Operations</strong>
        <nav aria-label="Main">
          <a routerLink="/" routerLinkActive="current" [routerLinkActiveOptions]="{ exact: true }" ariaCurrentWhenActive="page">Overview</a>
          <a routerLink="/incidents" routerLinkActive="current" ariaCurrentWhenActive="page">Incidents</a>
          <a routerLink="/settings" routerLinkActive="current" ariaCurrentWhenActive="page">Settings</a>
        </nav>
      </header>
      <main>
        <router-outlet />
      </main>
    </div>
  `,
  styles: `
    .shell {
      min-height: 100vh;
      background: var(--sp-substrate);
      color: var(--sp-text);
      font-family: var(--sp-font-display);
    }
    header {
      display: flex;
      gap: 32px;
      align-items: baseline;
      padding: 16px 32px;
      border-bottom: 1px solid var(--sp-rule);
    }
    nav {
      display: flex;
      gap: 20px;
    }
    a {
      color: var(--sp-text-muted);
      text-decoration: none;
    }
    a.current {
      color: var(--sp-text);
      text-decoration: underline;
    }
    main {
      max-width: 1200px;
      padding: 24px 32px;
    }
  `,
})
export class App {
  protected readonly settings = inject(Settings);
  // The palette as --sp-* properties, so the page itself takes its colours.
  protected readonly inks = computed(() => paletteStyle(this.settings.palette()));
}
```

Los gráficos ya siguen al tema, pero el fondo de la página no es de silverpoint. Para que también cambie, el marco lleva la clase del estilo base, `sp-ground-silverpoint` o `sp-ground-cyanotype`, y `data-substrate="cream"`. Con ellas, la hoja de estilos de silverpoint le da las variables `--sp-*` del estilo base. `paletteStyle` añade las de la paleta, y el CSS del marco usa `var(--sp-substrate)` y `var(--sp-text)`.

`routerLinkActive` marca el enlace de la página actual, y `ariaCurrentWhenActive` le añade `aria-current="page"` para los lectores de pantalla. Overview necesita `exact: true`; si no, `/` estaría activo en todas las páginas.

## 5. Los datos en vivo

El artículo 20 movía una ventana de 24 horas cada 2 segundos. Aquí avanzan a la vez las visitas y los errores, porque las dos gráficas los comparten. `src/app/live-feed.ts`:

```ts
import { Injectable, computed, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { interval } from 'rxjs';
import { hourly, type HourRow } from './data/ops';

// The next reading: the hour after the last one, taken from the day's
// profile with a small variation that changes from tick to tick.
export function nextReading(last: HourRow, tick: number): HourRow {
  const hour = (Number(last.hour) + 1) % 24;
  return {
    hour: String(hour).padStart(2, '0'),
    hits: hourly[hour].hits + ((tick * 7) % 9) - 4,
    errors: Math.max(0, hourly[hour].errors + ((tick * 5) % 3) - 1),
  };
}

// A rolling window: drop the oldest hour and append the new one.
export function advance(rows: readonly HourRow[], tick: number): HourRow[] {
  return [...rows.slice(1), nextReading(rows[rows.length - 1], tick)];
}

const sum = (rows: readonly HourRow[], key: 'hits' | 'errors') =>
  rows.reduce((total, row) => total + row[key], 0);

// One feed for the whole app: it keeps running while you visit other pages.
@Injectable({ providedIn: 'root' })
export class LiveFeed {
  readonly rows = signal(hourly);
  readonly hits = computed(() => sum(this.rows(), 'hits'));
  readonly errors = computed(() => sum(this.rows(), 'errors'));

  constructor() {
    interval(2000)
      .pipe(takeUntilDestroyed())
      .subscribe((tick) => this.rows.update((current) => advance(current, tick + 1)));
  }
}
```

El intervalo está en un servicio de toda la aplicación, no en la página. Si vas a Incidents y vuelves, la ventana sigue donde iba. `takeUntilDestroyed` lo detiene si la aplicación se destruye.

`hits` y `errors` son los totales de la ventana: los indicadores de la página los muestran y cambian con cada lectura.

## 6. La página Overview

`src/app/pages/overview.ts`:

```ts
import { Component, computed, inject, signal, viewChild } from '@angular/core';
import type { ActiveItem } from '@silverpoint/core';
import { SpBarChart } from '@silverpoint/angular/bar-chart';
import { SpDashboard, SpDashboardCell, type DashboardLayout } from '@silverpoint/angular/dashboard';
import { SpDonutChart } from '@silverpoint/angular/donut-chart';
import { SpHeatmapChart } from '@silverpoint/angular/heatmap-chart';
import { SpKpiCard } from '@silverpoint/angular/kpi-card';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { SpButton } from '@silverpoint/angular/ui/button';
import { blocks, errorsByDay, sales } from '../data/ops';
import { downloadSvg } from '../export-svg';
import { LiveFeed } from '../live-feed';
import { Settings } from '../settings';

@Component({
  selector: 'app-overview',
  imports: [SpBarChart, SpButton, SpDashboard, SpDashboardCell, SpDonutChart, SpHeatmapChart, SpKpiCard, SpLineChart],
  template: `
    <!-- The dashboard frame reads no provider: it takes the theme as inputs. -->
    <sp-dashboard
      id="ops"
      title="Overview"
      description="Traffic, errors and sales of the web service, updated every 2 seconds."
      [layout]="layout"
      [link]="{ key: 'hour' }"
      [ground]="settings.ground()"
      [palette]="settings.palette()"
    >
      <sp-dashboard-cell cell="hits-today">
        <sp-kpi-card title="Hits today" [data]="feed.rows()" valueKey="hits" [value]="feed.hits()" unit="thousand hits" />
      </sp-dashboard-cell>
      <sp-dashboard-cell cell="errors-today">
        <sp-kpi-card title="Errors today" [data]="feed.rows()" valueKey="errors" [value]="feed.errors()" unit="errors" />
      </sp-dashboard-cell>
      <sp-dashboard-cell cell="traffic">
        <sp-line-chart
          #hits
          title="Hits per hour"
          badge="Live"
          [data]="feed.rows()"
          xKey="hour"
          valueKey="hits"
          footerLeft="Thousands, last 24 hours"
          (activeChange)="active.set($event)"
        />
      </sp-dashboard-cell>
      <sp-dashboard-cell cell="errors-hour">
        <sp-bar-chart title="Errors per hour" [data]="feed.rows()" xKey="hour" valueKey="errors" />
      </sp-dashboard-cell>
      <sp-dashboard-cell cell="errors-day">
        <sp-heatmap-chart
          title="Errors by day"
          [data]="errorsByDay"
          labelKey="day"
          valuesKey="values"
          [columnLabels]="blocks"
          [scaleMax]="40"
        />
      </sp-dashboard-cell>
      <sp-dashboard-cell cell="channels">
        <sp-donut-chart title="Sales by channel" [data]="sales" nameKey="channel" valueKey="sales" centerLabel="thousand EUR" />
      </sp-dashboard-cell>
    </sp-dashboard>
    <div class="actions">
      <p aria-live="polite">{{ readout() }}</p>
      <button type="button" spButton (click)="download()">Download SVG</button>
    </div>
  `,
  styles: `
    .actions {
      display: flex;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
    }
  `,
})
export class Overview {
  protected readonly feed = inject(LiveFeed);
  protected readonly settings = inject(Settings);
  protected readonly errorsByDay = errorsByDay;
  protected readonly blocks = blocks;
  protected readonly sales = sales;
  protected readonly layout: DashboardLayout = {
    columns: { sm: 1, md: 2, lg: 4 },
    rowHeight: 240,
    gap: 16,
    cells: [
      { id: 'hits-today' },
      { id: 'errors-today' },
      { id: 'traffic', colSpan: { md: 2, lg: 2 } },
      { id: 'errors-hour', colSpan: { md: 2, lg: 2 } },
      { id: 'errors-day' },
      { id: 'channels' },
    ],
  };

  protected readonly active = signal<ActiveItem | null>(null);
  protected readonly readout = computed(() => {
    const item = this.active();
    if (!item) return 'Point at the hits chart to read an hour.';
    const { hour, hits, errors } = item.datum;
    return `${hour}:00 · ${hits} thousand hits · ${errors} errors`;
  });

  private readonly hits = viewChild.required<SpLineChart>('hits');

  protected download() {
    downloadSvg(this.hits().toSVGString(), 'hits-per-hour.svg');
  }
}
```

Lo que hay que saber de cada parte:

* **El panel** es el del artículo 13, con la misma rejilla. `[link]="{ key: 'hour' }"` enlaza los gráficos por la hora: al pasar por una hora de las visitas, se marca la misma hora en los errores y en los indicadores.
* **El tema del panel.** Los gráficos del panel siguen al proveedor, pero el marco del panel no lo lee: el adaptador de Angular, como el de React, solo usa el estilo que recibe el panel. Por eso `[ground]` y `[palette]` van en `sp-dashboard`. Sin ellos, el fondo y los bordes del panel se quedan con la paleta de silverpoint ([silverpoint#17](https://github.com/ecrespo/silverpoint/issues/17)). Se corregirá en una próxima versión del paquete.
* **La lectura** usa `(activeChange)` del gráfico de visitas, como en el artículo 11. `item.datum` es la fila completa. La desestructuración, `const { hour, hits, errors } = item.datum`, es válida con `noPropertyAccessFromIndexSignature`; con `item.datum.hour`, la compilación fallaría.
* **La descarga.** `viewChild.required` encuentra el gráfico marcado con `#hits` aunque esté dentro de una celda del panel, y `toSVGString()` devuelve su SVG.

Los gráficos no llevan `id`: dentro de un panel, cada celda les da uno estable, como `ops--traffic`, y el trazo a mano no cambia entre lecturas.

## 7. La exportación a SVG

`src/app/export-svg.ts` junta las dos funciones del artículo 18:

```ts
import groundCss from '@silverpoint/grounds/styles.css' with { loader: 'text' };

// The SVG with the ground's stylesheet inside, so it looks the same outside the app.
export function standaloneSvg(svg: string): string {
  const open = svg.indexOf('>') + 1;
  return `${svg.slice(0, open)}<style><![CDATA[${groundCss}]]></style>${svg.slice(open)}`;
}

export function downloadSvg(svg: string, filename: string) {
  const file = new Blob([standaloneSvg(svg)], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(file);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
```

El SVG lleva dentro la hoja de estilos del estilo base, entre `<![CDATA[` y `]]>`, para que se vea igual fuera de la aplicación ([silverpoint#14](https://github.com/ecrespo/silverpoint/issues/14)). TypeScript necesita la declaración del artículo 18 para importar un `.css` como texto, `src/text-imports.d.ts`:

```ts
declare module '*.css' {
  const text: string;
  export default text;
}
```

Hay un detalle que el artículo 18 no encontró, porque allí se comprobó con `ng build`. Con `ng serve`, el servidor de desarrollo preempaqueta las dependencias con Vite, y la importación con `loader: 'text'` ya no llega como texto. La página queda en blanco y la consola dice que `styles.css` «does not provide an export named 'default'». Excluir `@silverpoint/grounds` del preempaquetado no basta. Hay que desactivarlo en `angular.json`:

```json
        "serve": {
          "builder": "@angular/build:dev-server",
          "configurations": {
            "production": {
              "buildTarget": "ops-panel:build:production"
            },
            "development": {
              "buildTarget": "ops-panel:build:development"
            }
          },
          "defaultConfiguration": "development",
          "options": {
            "prebundle": false
          }
        },
```

En esta aplicación, el arranque en frío de `ng serve` siguió en unos 3,2 segundos.

## 8. La página Incidents

La tabla, el modal y el aviso son los del artículo 17. Solo cambia dónde viven las incidencias. `src/app/incident-log.ts`:

```ts
import { Injectable, computed, signal } from '@angular/core';
import { INCIDENTS } from './data/incidents';

// The incidents live here, not in the page, so an acknowledgement
// survives a visit to another page.
@Injectable({ providedIn: 'root' })
export class IncidentLog {
  readonly rows = signal(INCIDENTS);
  readonly openIds = computed(() => this.rows().filter((row) => row.status === 'open').map((row) => row.id));

  acknowledge(id: string) {
    this.rows.update((rows) => rows.map((row) => (row.id === id ? { ...row, status: 'acknowledged' } : row)));
  }
}
```

Si reconoces una incidencia y cambias de página, sigue reconocida al volver. La plantilla de `src/app/pages/incidents.ts` es la del artículo 17, con `log.rows()` y `log.openIds()` en lugar de los signals locales, y un `h1`. La clase:

```ts
export class Incidents {
  protected readonly log = inject(IncidentLog);
  protected readonly columns = COLUMNS;
  protected readonly pageSize = PAGE_SIZE;
  protected readonly sortKey = signal('opened');
  protected readonly sortOrder = signal<'asc' | 'desc'>('desc');
  protected readonly page = signal(1);
  protected readonly open = signal(false);
  protected readonly picked = signal<string | null>(null);
  protected readonly acknowledged = signal('');
  protected readonly toastOpen = signal(false);

  protected readonly visible = computed(() =>
    uiSortRows(this.log.rows(), this.sortKey(), this.sortOrder()).slice(
      (this.page() - 1) * PAGE_SIZE,
      this.page() * PAGE_SIZE,
    ),
  );

  protected sort(key: string) {
    this.sortOrder.set(key === this.sortKey() && this.sortOrder() === 'asc' ? 'desc' : 'asc');
    this.sortKey.set(key);
    this.page.set(1);
  }

  protected acknowledge() {
    const picked = this.picked();
    if (!picked) return;
    this.log.acknowledge(picked);
    this.acknowledged.set(picked);
    this.picked.set(null);
    this.open.set(false);
    this.toastOpen.set(true);
  }
}
```

El botón que abre el modal usa `var(--sp-rule)` y `var(--sp-text)` en sus estilos, así que también cambia con el tema. La corrección de la alineación de las celdas ([silverpoint#12](https://github.com/ecrespo/silverpoint/issues/12)) está en los estilos globales.

## 9. La página Settings

`src/app/pages/settings-page.ts`:

```ts
import { Component, inject } from '@angular/core';
import { SpSelect } from '@silverpoint/angular/ui/select';
import { SpSwitch } from '@silverpoint/angular/ui/switch';
import { PALETTES, Settings } from '../settings';
import { AlertRuleForm } from './alert-rule-form';

@Component({
  selector: 'app-settings-page',
  imports: [AlertRuleForm, SpSelect, SpSwitch],
  template: `
    <h1>Settings</h1>
    <div class="columns">
      <section aria-labelledby="theme-title">
        <h2 id="theme-title">Theme</h2>
        <sp-select
          label="Palette"
          [items]="palettes"
          [value]="settings.paletteKey()"
          (valueChange)="settings.paletteKey.set($event ?? 'silverpoint')"
          [disabled]="settings.cyanotype()"
        />
        <sp-switch
          label="Cyanotype ground"
          [value]="settings.cyanotype()"
          (valueChange)="settings.cyanotype.set(!!$event)"
        />
        <p>The theme applies to every page and is kept on this device.</p>
      </section>
      <section aria-labelledby="alert-title">
        <h2 id="alert-title">Alert rule</h2>
        <app-alert-rule-form />
      </section>
    </div>
  `,
  styles: `
    .columns {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 48px;
    }
    section {
      display: grid;
      gap: 16px;
      align-content: start;
      justify-items: start;
    }
    h2 {
      margin: 0;
    }
  `,
})
export class SettingsPage {
  protected readonly settings = inject(Settings);
  protected readonly palettes = PALETTES.map(({ key, label }) => ({ key, label }));
}
```

`sp-select` y `sp-switch` reciben su valor con `[value]` y avisan con `(valueChange)`. No uso `[(value)]` porque sus modelos admiten `null` o `undefined`, y los signals de los ajustes no: `$event ?? 'silverpoint'` y `!!$event` hacen la conversión. Con `cyanotype`, el selector de paleta se desactiva.

El formulario es el del artículo 16, con la misma plantilla. Cambia la clase de `src/app/pages/alert-rule-form.ts`, que ahora empieza desde la regla guardada y la guarda en los ajustes:

```ts
export class AlertRuleForm {
  private readonly settings = inject(Settings);
  protected readonly metrics = METRICS;
  protected readonly channels = CHANNELS;
  // The form starts from the saved rule, so it survives a visit to another page.
  private readonly rule = this.settings.rule();
  protected readonly form = new FormGroup({
    metric: new FormControl(this.rule.metric, { nonNullable: true }),
    threshold: new FormControl(this.rule.threshold, { nonNullable: true }),
    channel: new FormControl(this.rule.channel, { nonNullable: true }),
    active: new FormControl(this.rule.active, { nonNullable: true }),
    notes: new FormControl(this.rule.notes, { nonNullable: true }),
  });
  protected readonly saved = computed(() => {
    const { metric, threshold, channel, active, notes } = this.settings.rule();
    return `Rule: ${metric} ≥ ${threshold}, by ${channel}, ${active ? 'active' : 'paused'}. Notes: ${notes || '—'}`;
  });

  protected save() {
    this.settings.rule.set(this.form.getRawValue());
  }
}
```

## 10. Los estilos globales

`src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';

body {
  margin: 0;
}

.sp-ui-table td:not([data-align]) {
  text-align: start;
}
```

Las fuentes, la hoja de estilos de los gráficos, la de los componentes y la corrección de las celdas de la tabla. El resto de los estilos va en cada componente.

## Ejecutar, compilar y desplegar

En desarrollo:

```bash
npx ng serve
```

La aplicación queda en `http://localhost:4200`. Para producción:

```bash
npx ng build
```

El resultado es una carpeta de archivos estáticos, `dist/ops-panel/browser`. En mi máquina, la compilación limpia tardó unos 4 segundos y produjo esto:

| Archivo | Tamaño | Comprimido (gzip) |
|---|---|---|
| `main` (Angular, router, marco, ajustes) | 345,6 kB | 109,2 kB |
| Página Overview | 69,3 kB | 21,3 kB |
| Dos trozos compartidos de silverpoint | 81,5 kB | 23,3 kB |
| Página Incidents | 12,6 kB | 4,2 kB |
| Página Settings | 10,2 kB | 2,8 kB |
| CSS | 152,7 kB | 14,7 kB |

La primera visita a `/` descarga unos 157 kB comprimidos de JavaScript y CSS, más las tres fuentes. Las páginas Incidents y Settings llegan cuando las visitas.

Para desplegar, sube `dist/ops-panel/browser` a cualquier alojamiento estático. Hay una condición: el router de Angular navega en el navegador, pero si alguien recarga `/incidents`, el servidor recibe esa ruta y no tiene ese archivo. El alojamiento debe responder con `index.html` a las rutas que no existen. Vercel, Netlify, Cloudflare Pages y nginx lo permiten con una regla de reescritura. Para las pruebas usé un servidor estático de Node con esa regla.

## Las comprobaciones

Probé la aplicación en Chrome con Playwright, 38 comprobaciones, con `ng serve` y con la compilación de producción. Pasaron todas en los dos:

| Página | Lo comprobado |
|---|---|
| Overview | Los seis gráficos llegan a `data-status="ready"`; la ventana avanza cada 2 segundos y mantiene 24 filas; el indicador cambia con ella; la lectura muestra la hora activa y se borra al salir; al pasar por las visitas se marcan los errores; el SVG descargado lleva la hoja de estilos |
| Navegación | Los enlaces cambian de página sin recargar; el enlace actual lleva `aria-current`; cada página tiene su título |
| Incidents | Cinco filas, las más recientes primero; orden por minutos en los dos sentidos; la página 3 tiene las dos últimas; el modal lista las cinco abiertas; el aviso nombra la incidencia; sigue reconocida al volver |
| Settings | El formulario guarda la regla; SMS está desactivado |
| Tema | Sanguina cambia el fondo de la página, los componentes, los seis gráficos y el marco del panel; la cianotipia cambia la página, los gráficos, la tabla y los botones; el tema sigue tras recargar |

Además, sin errores en la consola. El primer gráfico estuvo listo a los 235 ms de empezar a cargar la página, y los seis a los 279 ms (la mediana de tres cargas de la compilación de producción, en mi máquina).

Angular 22 crea los proyectos sin zone.js: la pantalla se actualiza en el siguiente fotograma, no dentro del clic. Una prueba que lee la página justo después de hacer clic ve el estado anterior. Mi primera ejecución falló cinco comprobaciones por eso; una espera corta después de cada acción lo resolvió.

## Problemas comunes

* **Con `ng serve`, la página queda en blanco y la consola habla de «export named 'default'».** Falta `"prebundle": false` en `angular.json`. Con `ng build` no pasa ([silverpoint#19](https://github.com/ecrespo/silverpoint/issues/19)). Se corregirá en una próxima versión del paquete.
* **El tema cambia la página, pero no los gráficos.** Se usó `provideSilverpoint` con un objeto fijo. Registra `SILVERPOINT_CONFIG` con getters, como en `app.config.ts`.
* **Los gráficos cambian, pero el marco del panel no.** Faltan `[ground]` y `[palette]` en `sp-dashboard`.
* **El CLI avisa de que el paquete inicial pasa de 500 kB.** `SILVERPOINT_CONFIG` se importó de `@silverpoint/angular`. Impórtalo de `@silverpoint/angular/env`.
* **Al dejar el puntero sobre un gráfico, puede aparecer también la descripción emergente del navegador.** Angular copia los atributos con texto literal al elemento, y `title="Hits per hour"` queda como atributo `title` de `sp-line-chart`. Si te molesta, escríbelo como expresión, `[title]="'Hits per hour'"`: el gráfico recibe el título y el elemento no lleva el atributo ([silverpoint#18](https://github.com/ecrespo/silverpoint/issues/18)). Se corregirá en una próxima versión del paquete.
* **Al recargar `/settings` en producción, el servidor responde 404.** Falta la regla que devuelve `index.html`.

## Lo que viene

Operations ya funciona en Angular. El [artículo 26](/blog/silverpoint_serie_26) construye la misma aplicación en Reflex, en Python, y le da datos reales: la latencia medida de servicios públicos.
