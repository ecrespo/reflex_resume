Title: Silverpoint, artículo 23: proyecto final en React con Next.js, el panel de operaciones de principio a fin
Date: 2026-11-11 22:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, nextjs, Visualización
lang: es
translation: true
Slug: silverpoint_serie_23
Authors: Ernesto Crespo
Summary: El panel de operaciones completo como una aplicación de Next.js con el App Router: una vista general con datos en vivo, gráficos enlazados y descarga en SVG, una página de incidencias y otra de ajustes que cambia el tema de toda la aplicación. Qué va en el servidor, qué en el cliente, cómo se compila y cómo se despliega en Vercel.

El nivel 4 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) junta todo en un proyecto final. Los niveles anteriores construyeron el panel de operaciones pieza a pieza: el panel en rejilla, los componentes de interfaz, la exportación, el render en servidor y los datos en vivo. Este artículo los reúne en una aplicación de React con [Next.js](https://nextjs.org/) y su App Router, con tres páginas y un tema común.

Los artículos 24, 25 y 26 construyen la misma aplicación en Vue, Angular y Reflex, y el 27 las compara. Por eso las tres páginas son iguales en los cuatro.

![La vista general del panel de operaciones en Next.js: los indicadores, el tráfico por hora en vivo con el puntero en las 11, los errores por hora enlazados, los errores por día y las ventas por canal](./images/silverpoint-serie-23.png)

## Lo que vas a construir

| Ruta | Página | Viene de |
|---|---|---|
| `/` | La vista general: indicadores, tráfico en vivo, errores enlazados por hora, errores por día, ventas por canal, una lectura de la hora activa y un botón de descarga en SVG | Artículos [11](/blog/silverpoint_serie_11), [13](/blog/silverpoint_serie_13), [18](/blog/silverpoint_serie_18) y [20](/blog/silverpoint_serie_20) |
| `/incidents` | La tabla de incidencias ordenable y paginada, con la ventana para reconocer una incidencia y el aviso | Artículo [17](/blog/silverpoint_serie_17) |
| `/settings` | El tema, un estilo base y una paleta que cambian toda la aplicación, y el formulario de la regla de alerta | Artículos [09](/blog/silverpoint_serie_9), [12](/blog/silverpoint_serie_12) y [16](/blog/silverpoint_serie_16) |

Una barra de navegación con tres enlaces las une. Los ajustes se conservan mientras dura la sesión: al ir y volver entre páginas, el tema y la regla guardada siguen ahí. Al recargar la página vuelven a los valores por defecto.

## Lo que necesitas

* Node.js 20.9 o superior, el mínimo de Next.js 16. Lo probé con Node.js 24.
* Next.js 16.4.6, React 19.3.0 y silverpoint 0.9.2.

## El proyecto

Crea la aplicación e instala silverpoint:

```bash
npx create-next-app@latest ops-panel --ts --app --no-tailwind --no-eslint --no-src-dir --no-react-compiler --import-alias "@/*" --use-npm --yes
cd ops-panel
npm install @silverpoint/react @silverpoint/core @silverpoint/grounds @silverpoint/fonts
```

`@silverpoint/core` va aparte porque el código importa de él las paletas y el tipo `ActiveItem`, como en el [artículo 12](/blog/silverpoint_serie_12). Borra `app/page.module.css` y las imágenes de `public/`, que la plantilla trae de ejemplo. Al terminar, el proyecto tiene esta forma:

```text
ops-panel/
├── app/
│   ├── layout.tsx                server: stylesheets, title, navigation
│   ├── globals.css
│   ├── settings-provider.tsx     client: settings and SilverpointProvider
│   ├── page.tsx                  server: the / route
│   ├── overview.tsx              client: the dashboard
│   ├── incidents/
│   │   ├── page.tsx              server: the /incidents route
│   │   └── incidents.tsx         client: table, modal and toast
│   └── settings/
│       ├── page.tsx              server: the /settings route
│       ├── theme-form.tsx        client: ground and palette
│       └── alert-rule-form.tsx   client: the alert rule
├── lib/
│   ├── ops.ts                    the panel's data
│   ├── live.ts                   the rolling window
│   ├── incidents.ts              the 12 incidents
│   ├── rule.ts                   the alert rule
│   ├── download.ts               the SVG download
│   └── standalone.ts             the stylesheet inside the SVG
├── raw.d.ts
├── next.config.ts
├── package.json
└── tsconfig.json
```

Tres archivos de `lib/` vienen sin cambios de artículos anteriores: `lib/ops.ts` es el del [artículo 13](/blog/silverpoint_serie_13), con las filas por hora, los errores por día y las ventas por canal; `lib/incidents.ts` es el del [artículo 17](/blog/silverpoint_serie_17), y `lib/download.ts`, el del [artículo 18](/blog/silverpoint_serie_18).

## Servidor o cliente

En el App Router, cada archivo es un componente de servidor salvo que empiece por `'use client'`. Un componente de servidor no envía JavaScript al navegador, pero tampoco puede tener estado, efectos, eventos ni leer un contexto de React.

| Archivo | Dónde | Por qué |
|---|---|---|
| `app/layout.tsx` | Servidor | Las hojas de estilos, el título y la navegación no cambian |
| `app/page.tsx`, `app/incidents/page.tsx`, `app/settings/page.tsx` | Servidor | El título de cada página y los encabezados |
| `app/settings-provider.tsx` | Cliente | Guarda los ajustes en estado y los reparte con un contexto |
| `app/overview.tsx` | Cliente | El intervalo de los datos en vivo, la lectura, la descarga y el tema |
| `app/incidents/incidents.tsx` | Cliente | El orden, la página, la ventana y el aviso son estado |
| `app/settings/theme-form.tsx`, `app/settings/alert-rule-form.tsx` | Cliente | Son formularios |

El [artículo 19](/blog/silverpoint_serie_19) dibujaba los gráficos con las entradas de servidor, `@silverpoint/react/server/...`. Aquí no sirven: el tema vive en el estado del cliente y llega por el contexto de `SilverpointProvider`, que un componente de servidor no puede leer. Un gráfico de servidor se quedaría con el tema por defecto al cambiarlo en `/settings`. Por eso todos los gráficos son componentes de cliente.

Eso no los deja fuera del HTML. Next.js también renderiza los componentes de cliente al compilar, y dentro de un `Dashboard` cada gráfico recibe el tamaño de su celda. El artículo 19 contaba que un gráfico de cliente sin `width` llega al HTML como un hueco con `data-status="deferred"`. Dentro del panel no pasa: el HTML de `/` trae los seis gráficos dibujados, con `data-status="ready"`, antes de que cargue una línea de JavaScript.

## La configuración

La descarga en SVG del [artículo 18](/blog/silverpoint_serie_18) mete la hoja de estilos del estilo base dentro del archivo. En Vite, la hoja se importaba como texto con `?raw`. Turbopack, el empaquetador de Next.js, no entiende `?raw` por sí solo: hay que decirle qué hacer con una regla en `next.config.ts`:

```ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      // Any file imported with `?raw` is loaded as a string, as in Vite.
      '*': { condition: { query: '?raw' }, type: 'text' },
    },
  },
};

export default nextConfig;
```

`cacheComponents` y `partialPrefetching` vienen de la plantilla de `create-next-app`. La regla nueva es `turbopack.rules`: cualquier archivo importado con `?raw` se carga como texto.

Con la regla, `lib/standalone.ts` es el del artículo 18 con otra ruta:

```ts
import groundCss from '../node_modules/@silverpoint/grounds/dist/styles.css?raw';

export function standaloneSvg(svg: string): string {
  const open = svg.indexOf('>') + 1;
  return `${svg.slice(0, open)}<style><![CDATA[${groundCss}]]></style>${svg.slice(open)}`;
}
```

La ruta del paquete, `@silverpoint/grounds/styles.css?raw`, no funciona en Turbopack. La compilación falla con «Module not found: Can't resolve '@silverpoint/grounds/styles.css'», aunque la misma ruta sin `?raw` se resuelve bien en `app/layout.tsx`. Con la ruta relativa al archivo dentro de `node_modules` funciona. Si tu proyecto está en un monorepo con `node_modules` en la raíz, ajusta los `../`.

TypeScript tampoco conoce `?raw`. En Vite lo declaraban los tipos de `vite/client`; aquí lo declara `raw.d.ts`, en la raíz del proyecto:

```ts
declare module '*?raw' {
  const content: string;
  export default content;
}
```

El SVG sale sin la hoja de estilos del estilo base porque `toSVGString()` no la incluye. Es un fallo de la librería, registrado en el [issue #14](https://github.com/ecrespo/silverpoint/issues/14), y se corregirá en una próxima versión del paquete.

## El diseño común

`app/layout.tsx` es el único sitio donde se cargan las hojas de estilos: las fuentes, el estilo base y la de los componentes de interfaz del [artículo 16](/blog/silverpoint_serie_16). Envuelve todas las páginas con los ajustes y pone la navegación:

```tsx
import type { Metadata } from 'next';
import Link from 'next/link';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import './globals.css';
import { SettingsProvider } from './settings-provider';

export const metadata: Metadata = {
  title: { default: 'Operations', template: '%s · Operations' },
  description: 'Traffic, errors, incidents and alert rules of the web service.',
};

export default function RootLayout({ children }: LayoutProps<'/'>) {
  return (
    <html lang="en">
      <body>
        <SettingsProvider>
          <nav aria-label="Main">
            <Link href="/">Overview</Link>
            <Link href="/incidents">Incidents</Link>
            <Link href="/settings">Settings</Link>
          </nav>
          <main>{children}</main>
        </SettingsProvider>
      </body>
    </html>
  );
}
```

`LayoutProps<'/'>` es un tipo global que Next.js genera a partir de las rutas. `title.template` hace que el título de `/incidents` sea «Incidents · Operations».

La navegación y `main` son componentes de servidor, pero van dentro de `SettingsProvider`, que es de cliente. Next.js lo permite: un componente de cliente puede recibir componentes de servidor como `children`. Lo que no se puede es importar un componente de servidor desde uno de cliente.

`Link` navega sin recargar la página. El diseño no se vuelve a montar al cambiar de ruta, así que el estado de `SettingsProvider` se conserva.

## El tema y los ajustes

`app/settings-provider.tsx` guarda los ajustes en estado: el estilo base, la paleta y la regla de alerta. Los reparte con un contexto y pasa el tema a `SilverpointProvider`:

```tsx
'use client';

import { createContext, useContext, useState, type CSSProperties, type ReactNode } from 'react';
import type { GroundName, Palette } from '@silverpoint/core';
import { PALETTES, paletteStyle } from '@silverpoint/core/palettes';
import { SilverpointProvider } from '@silverpoint/react';
import { DEFAULT_RULE, type AlertRule } from '@/lib/rule';

export type Settings = {
  ground: GroundName;
  palette: string;
  rule: AlertRule;
};

type SettingsContextValue = {
  settings: Settings;
  palette: Palette | undefined;
  update: (change: Partial<Settings>) => void;
};

const SettingsContext = createContext<SettingsContextValue | null>(null);

export function useSettings(): SettingsContextValue {
  const value = useContext(SettingsContext);
  if (!value) throw new Error('useSettings() needs a <SettingsProvider> above it');
  return value;
}

// The palette's --sp-* declarations as a React style object, so the page
// itself is painted with the same substrate and text colours as the charts.
function paletteVars(palette: Palette | undefined): CSSProperties {
  const pairs = paletteStyle(palette)
    .split(';')
    .filter(Boolean)
    .map((declaration) => declaration.split(':'));
  return Object.fromEntries(pairs);
}

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<Settings>({
    ground: 'silverpoint',
    palette: 'silverpoint',
    rule: DEFAULT_RULE,
  });

  const update = (change: Partial<Settings>) => setSettings((current) => ({ ...current, ...change }));
  // Cyanotype brings its own colours; a palette only applies to silverpoint.
  const palette = settings.ground === 'silverpoint' ? PALETTES[settings.palette] : undefined;

  return (
    <SettingsContext value={{ settings, palette, update }}>
      <SilverpointProvider ground={settings.ground} palette={palette}>
        <div className={`shell sp-ground-${settings.ground}`} data-substrate="cream" style={paletteVars(palette)}>
          {children}
        </div>
      </SilverpointProvider>
    </SettingsContext>
  );
}
```

Tres decisiones de este archivo:

* **La cianotipia no lleva paleta.** Trae sus propios colores, como contaba el [artículo 12](/blog/silverpoint_serie_12). Con `ground="cyanotype"`, `palette` es `undefined`, y en `/settings` el selector de paleta se desactiva.
* **La página también cambia de color.** `SilverpointProvider` no dibuja ningún elemento: solo reparte la configuración a los gráficos y componentes que tiene debajo. Para que el fondo de la página acompañe al tema, el `div` que envuelve la aplicación lleva la clase del estilo base, `sp-ground-silverpoint` o `sp-ground-cyanotype`, y las propiedades `--sp-*` de la paleta. `paletteStyle` devuelve esas declaraciones como texto; `paletteVars` las convierte en un objeto de estilo de React. Con eso, `background: var(--sp-substrate)` en `globals.css` pinta la página con el sustrato del tema.
* **El contexto también da la paleta resuelta.** El panel de la vista general la necesita, como se ve más abajo.

Las hojas del estilo base declaran sus propiedades dentro de `:where()`, sin peso, precisamente para que una regla tuya pueda cambiarlas. Por eso la clase del estilo base sirve también en un elemento que no es un gráfico.

## Los estilos

`app/globals.css` completo:

```css
body {
  margin: 0;
}

.shell {
  min-height: 100vh;
  padding: 24px 32px;
  background: var(--sp-substrate);
  color: var(--sp-text);
  font-family: var(--sp-font-display);
}

nav {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  font-size: 18px;
}

nav a {
  color: inherit;
}

h1 {
  margin: 0 0 16px;
  font-weight: 500;
}

.toolbar {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-top: 16px;
}

.stack {
  display: grid;
  gap: 16px;
  align-content: start;
  justify-items: start;
  max-width: 720px;
}

.sp-table {
  justify-self: stretch;
}

.sp-ui-table td:not([data-align]) {
  text-align: start;
}

button[aria-haspopup='dialog'] {
  padding: 6px 14px;
  border: 1px solid currentColor;
  border-radius: 2px;
  background: transparent;
  color: inherit;
  font: inherit;
  cursor: pointer;
}

form {
  display: grid;
  gap: 20px;
  align-content: start;
}

.settings {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 48px;
}

h2 {
  margin: 0;
  font-weight: 500;
}
```

`.stack` es una columna para el contenido de las incidencias y de cada bloque de ajustes. Al principio era una regla sobre `section`, como en el artículo 17, pero `Dashboard` también es una `section`: con `max-width: 720px` el panel pasaba de cuatro columnas a dos.

La regla `.sp-ui-table td:not([data-align])` alinea a la izquierda las celdas de la tabla. Sin ella, una regla de los gráficos las alinea a la derecha. Es un fallo de la librería, registrado en el [issue #12](https://github.com/ecrespo/silverpoint/issues/12), y se corregirá en una próxima versión del paquete.

## Los datos en vivo y la regla de alerta

`lib/live.ts` es la ventana que avanza del [artículo 20](/blog/silverpoint_serie_20), ahora sobre las filas del panel. Cada lectura nueva copia la fila de esa hora, con sus errores, y cambia las visitas:

```ts
import { hourly, type HourRow } from './ops';

// The next reading: the hour after the last one, taken from the day's
// profile with a small variation that changes from tick to tick.
export function nextReading(last: HourRow, tick: number): HourRow {
  const hour = (Number(last.hour) + 1) % 24;
  return { ...hourly[hour], hits: hourly[hour].hits + ((tick * 7) % 9) - 4 };
}

// A rolling window: drop the oldest hour and append the new one.
export function advance(rows: readonly HourRow[], tick: number): HourRow[] {
  return [...rows.slice(1), nextReading(rows[rows.length - 1], tick)];
}
```

`lib/rule.ts` describe la regla de alerta del [artículo 16](/blog/silverpoint_serie_16). Antes era el estado del formulario; ahora es un ajuste más, para que la regla guardada siga ahí al volver a `/settings`:

```ts
export type AlertRule = {
  metric: string;
  threshold: number;
  channel: string;
  active: boolean;
  notes: string;
};

export const DEFAULT_RULE: AlertRule = {
  metric: 'errors',
  threshold: 10,
  channel: 'email',
  active: true,
  notes: '',
};

export function describeRule(rule: AlertRule): string {
  const state = rule.active ? 'active' : 'paused';
  return `${rule.metric} ≥ ${rule.threshold}, by ${rule.channel}, ${state}. Notes: ${rule.notes || '—'}`;
}
```

## La vista general

`app/page.tsx` es un componente de servidor que solo pone el panel:

```tsx
import { Overview } from './overview';

export default function OverviewPage() {
  return <Overview />;
}
```

Y `app/overview.tsx`, el panel del [artículo 13](/blog/silverpoint_serie_13) con los datos en vivo, la lectura y la descarga:

```tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import type { ActiveItem } from '@silverpoint/core';
import { BarChart } from '@silverpoint/react/bar-chart';
import { Dashboard, DashboardCell, type DashboardLayout } from '@silverpoint/react/dashboard';
import { DonutChart } from '@silverpoint/react/donut-chart';
import { HeatmapChart } from '@silverpoint/react/heatmap-chart';
import { KpiCard } from '@silverpoint/react/kpi-card';
import { LineChart, type ChartHandle } from '@silverpoint/react/line-chart';
import { SpButton } from '@silverpoint/react/ui/button';
import { downloadSvg } from '@/lib/download';
import { advance } from '@/lib/live';
import { blocks, errorsByDay, hourly, sales } from '@/lib/ops';
import { useSettings } from './settings-provider';

const layout: DashboardLayout = {
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

export function Overview() {
  const { settings, palette } = useSettings();
  const [rows, setRows] = useState(hourly);
  const [active, setActive] = useState<ActiveItem | null>(null);
  const chart = useRef<ChartHandle>(null);

  useEffect(() => {
    let tick = 0;
    const timer = setInterval(() => {
      tick += 1;
      setRows((current) => advance(current, tick));
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  const last = rows[rows.length - 1];

  const exportChart = () => {
    const svg = chart.current?.toSVGString();
    if (svg) downloadSvg(svg, 'hits-per-hour.svg');
  };

  return (
    <>
      <Dashboard
        id="ops"
        title="Operations"
        description="Traffic, errors and sales of the web service today."
        layout={layout}
        link={{ key: 'hour' }}
        ground={settings.ground}
        palette={palette}
      >
        <DashboardCell cell="hits-today">
          <KpiCard title="Hits today" data={hourly} valueKey="hits" value={886} unit="thousand hits" delta={4.2} />
        </DashboardCell>
        <DashboardCell cell="errors-today">
          <KpiCard title="Errors today" data={hourly} valueKey="errors" value={103} unit="errors" delta={-12} />
        </DashboardCell>
        <DashboardCell cell="traffic">
          <LineChart
            ref={chart}
            id="live-hits"
            title="Hits per hour"
            badge="Live"
            data={rows}
            xKey="hour"
            valueKey="hits"
            footerLeft="Thousands"
            footerRight={`Updated at ${last.hour}:00`}
            onActiveChange={setActive}
          />
        </DashboardCell>
        <DashboardCell cell="errors-hour">
          <BarChart title="Errors per hour" data={hourly} xKey="hour" valueKey="errors" />
        </DashboardCell>
        <DashboardCell cell="errors-day">
          <HeatmapChart
            title="Errors by day"
            data={errorsByDay}
            labelKey="day"
            valuesKey="values"
            columnLabels={blocks}
            scaleMax={40}
          />
        </DashboardCell>
        <DashboardCell cell="channels">
          <DonutChart title="Sales by channel" data={sales} nameKey="channel" valueKey="sales" centerLabel="thousand EUR" />
        </DashboardCell>
      </Dashboard>
      <div className="toolbar">
        <SpButton onClick={exportChart}>Download SVG</SpButton>
        <p>{active ? `${String(active.datum.hour)}:00, ${active.value}k hits` : 'Point at an hour'}</p>
      </div>
    </>
  );
}
```

Lo que hace cada parte:

* **Los datos en vivo.** El intervalo del artículo 20 añade una lectura cada 2 segundos y descarta la más antigua. El gráfico de tráfico lleva `id="live-hits"`, un identificador estable: sin él, cada render podría cambiar la semilla y el trazo temblaría de otra forma en cada lectura. El pie dice la hora de la última lectura.
* **Los gráficos enlazados.** Con `link={{ key: 'hour' }}`, el puntero sobre una hora del tráfico marca la misma hora en los errores y en las curvas de los dos indicadores, y al revés. Los errores por día y las ventas por canal no tienen el campo `hour`: no muestran marca y en desarrollo avisan con `SP016`, como explicaba el artículo 13.
* **La lectura.** `onActiveChange` del gráfico de tráfico guarda el elemento activo, como en el [artículo 11](/blog/silverpoint_serie_11), y el párrafo escribe «11:00, 62k hits». Solo sigue al gráfico de tráfico: las marcas que pone el enlace no lo cambian. Para seguir el valor enlazado, usa `onLinkChange`, del artículo 13.
* **La descarga.** `ref` da el manejador del gráfico, y `toSVGString()` el SVG, como en el artículo 18. El archivo lleva la paleta del tema elegido.
* **El tema del panel.** `ground` y `palette` se pasan al `Dashboard`, además de llegar por el proveedor. Los gráficos de dentro siguen al proveedor, pero el marco del panel no: con la cianotipia, los gráficos se volvían azules y el fondo del panel seguía color crema. Es un fallo de la librería, registrado en el [issue #17](https://github.com/ecrespo/silverpoint/issues/17), y se corregirá en una próxima versión del paquete. Mientras tanto, pasa los dos valores al panel.

## Las incidencias

`app/incidents/page.tsx` es de servidor, con su título y su encabezado:

```tsx
import type { Metadata } from 'next';
import { Incidents } from './incidents';

export const metadata: Metadata = { title: 'Incidents' };

export default function IncidentsPage() {
  return (
    <>
      <h1>Incidents</h1>
      <Incidents />
    </>
  );
}
```

`app/incidents/incidents.tsx` es el componente `Incidents` del [artículo 17](/blog/silverpoint_serie_17) con tres cambios: la primera línea, `'use client'`; la ruta de los datos, que ahora están en `lib/`; y la clase `stack` en la `section`. El principio del archivo queda así:

```tsx
'use client';

import { useState } from 'react';
import { uiSortRows } from '@silverpoint/core/ui';
import { SpButton } from '@silverpoint/react/ui/button';
import { SpModal } from '@silverpoint/react/ui/modal';
import { SpPagination } from '@silverpoint/react/ui/pagination';
import { SpSelect } from '@silverpoint/react/ui/select';
import { SpTable } from '@silverpoint/react/ui/table';
import { SpToast, SpToaster } from '@silverpoint/react/ui/toast';
import { COLUMNS, INCIDENTS, PAGE_SIZE } from '@/lib/incidents';
```

El resto es igual: la tabla ordenable, la paginación de cinco en cinco, la ventana con su botón nativo como disparador y el aviso.

## Los ajustes

`app/settings/page.tsx` pone los dos bloques, uno junto al otro en una pantalla ancha:

```tsx
import type { Metadata } from 'next';
import { AlertRuleForm } from './alert-rule-form';
import { ThemeForm } from './theme-form';

export const metadata: Metadata = { title: 'Settings' };

export default function SettingsPage() {
  return (
    <>
      <h1>Settings</h1>
      <div className="settings">
        <section className="stack">
          <h2>Theme</h2>
          <ThemeForm />
        </section>
        <section className="stack">
          <h2>Alert rule</h2>
          <AlertRuleForm />
        </section>
      </div>
    </>
  );
}
```

`app/settings/theme-form.tsx` cambia el tema. No tiene botón de guardar: cada cambio se aplica al momento.

```tsx
'use client';

import { PALETTE_NAMES } from '@silverpoint/core/palettes';
import { SpSegmented } from '@silverpoint/react/ui/segmented';
import { SpSelect } from '@silverpoint/react/ui/select';
import { useSettings } from '../settings-provider';

const GROUNDS = [
  { key: 'silverpoint', label: 'Silverpoint' },
  { key: 'cyanotype', label: 'Cyanotype' },
];

export function ThemeForm() {
  const { settings, update } = useSettings();

  return (
    <>
      <SpSegmented
        label="Ground"
        name="ground"
        items={GROUNDS}
        value={settings.ground}
        onChange={(ground) => update({ ground: ground === 'cyanotype' ? 'cyanotype' : 'silverpoint' })}
      />
      <SpSelect
        label="Palette"
        items={PALETTE_NAMES}
        value={settings.palette}
        onChange={(palette) => update({ palette })}
        disabled={settings.ground === 'cyanotype'}
      />
    </>
  );
}
```

`PALETTE_NAMES` son los nombres de las seis paletas, de `silverpoint` a `indigo`. Al elegir uno, `update` lo guarda, el proveedor recibe la paleta nueva y todo lo que está debajo se vuelve a pintar: los gráficos, el panel, la tabla, los botones y el fondo de la página. Al cambiar de paleta, los datos no se vuelven a dibujar: solo cambian las propiedades `--sp-*`.

`app/settings/alert-rule-form.tsx` es el formulario del artículo 16. Sus campos empiezan con la regla guardada y, al enviar, la guardan en los ajustes:

```tsx
'use client';

import { useState, type FormEvent } from 'react';
import { SpButton } from '@silverpoint/react/ui/button';
import { SpRadioGroup } from '@silverpoint/react/ui/radio-group';
import { SpSegmented } from '@silverpoint/react/ui/segmented';
import { SpSlider } from '@silverpoint/react/ui/slider';
import { SpSwitch } from '@silverpoint/react/ui/switch';
import { SpTextarea } from '@silverpoint/react/ui/textarea';
import { describeRule } from '@/lib/rule';
import { useSettings } from '../settings-provider';

const METRICS = [
  { key: 'errors', label: 'Errors' },
  { key: 'hits', label: 'Hits' },
];

const CHANNELS = [
  { key: 'email', label: 'Email' },
  { key: 'chat', label: 'Chat' },
  { key: 'sms', label: 'SMS', disabled: true },
];

export function AlertRuleForm() {
  const { settings, update } = useSettings();
  const [metric, setMetric] = useState(settings.rule.metric);
  const [threshold, setThreshold] = useState(settings.rule.threshold);
  const [channel, setChannel] = useState(settings.rule.channel);
  const [active, setActive] = useState(settings.rule.active);

  function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const notes = String(new FormData(event.currentTarget).get('notes') ?? '');
    update({ rule: { metric, threshold, channel, active, notes } });
  }

  return (
    <form onSubmit={save}>
      <SpSegmented label="Metric" name="metric" items={METRICS} value={metric} onChange={setMetric} />
      <SpSlider
        label="Threshold"
        name="threshold"
        min={0}
        max={50}
        step={5}
        marks={[0, 25, 50]}
        value={threshold}
        onChange={setThreshold}
      />
      <SpRadioGroup
        label="Notify by"
        name="channel"
        items={CHANNELS}
        orientation="horizontal"
        value={channel}
        onChange={setChannel}
      />
      <SpSwitch label="Active" name="active" checked={active} onChange={setActive} />
      <SpTextarea
        label="Notes"
        placeholder="Notes for the on-call team"
        name="notes"
        rows={2}
        maxLength={200}
        showCount
        defaultValue={settings.rule.notes}
      />
      <SpButton type="submit" variant="primary">
        Save rule
      </SpButton>
      <p role="status">Saved rule: {describeRule(settings.rule)}</p>
    </form>
  );
}
```

## Lo que Next.js conserva al navegar

La plantilla activa `cacheComponents`. Con esa opción, Next.js no desmonta la página que dejas: la oculta con el componente `<Activity>` de React y conserva su estado y su HTML. Lo hace con las tres últimas rutas visitadas, que en esta aplicación son todas.

Lo comprobé en la versión de producción:

* Reconocí INC-1038, ordené por minutos, pasé por las otras dos páginas y volví: la tabla seguía ordenada por minutos e INC-1038 seguía como `acknowledged`.
* Mientras la vista general está oculta, React desmonta sus efectos, así que el intervalo se detiene. Al volver tras 6,5 segundos, el pie seguía en «Updated at 01:00», y 2 segundos después pasó a «Updated at 02:00»: la ventana sigue desde donde se quedó, sin saltos.
* En desarrollo, al salir de la vista general, cada gráfico oculto avisa en la consola con `SP003`: «the container measures 0 px; the render is deferred». Es lo que mide un elemento con `display: none`. Al volver, los gráficos se dibujan de nuevo a su tamaño. En producción no aparece ningún aviso. El aviso sobra, y está abierto como [silverpoint#22](https://github.com/ecrespo/silverpoint/issues/22). Se corregirá en una próxima versión del paquete.

Por eso guardar la regla en los ajustes no es imprescindible con tres rutas: el formulario también se conservaría oculto. Pero una aplicación con más páginas pierde las más antiguas, y los ajustes deben vivir en un sitio que no dependa de eso.

## Ejecutar, compilar y desplegar

En desarrollo:

```bash
npm run dev
```

La aplicación queda en `http://localhost:3000`. Para la versión de producción:

```bash
npm run build
npm run start
```

`npm run build` compiló en 7,6 segundos y marcó las cuatro rutas como estáticas:

```text
Route (app)
┌ ○ /
├ ○ /_not-found
├ ○ /incidents
└ ○ /settings


○  (Static)  prerendered as static content
```

Las cuatro se generan como HTML al compilar. No hay nada que calcular por petición: los datos son fijos y los datos en vivo se generan en el navegador.

Para desplegar en [Vercel](https://vercel.com/), sube el proyecto a un repositorio de Git e impórtalo desde [vercel.com/new](https://vercel.com/new). Vercel reconoce Next.js y usa `next build` sin configuración. También puedes desplegar desde la carpeta del proyecto con su línea de comandos, `npx vercel`. Las páginas estáticas se sirven desde la red de Vercel, y cada envío al repositorio crea un despliegue nuevo con su propia dirección. No hay variables de entorno que configurar. Yo no lo desplegué; lo probé con `npm run start`.

## Las comprobaciones

Probé la aplicación con Playwright y Chrome, primero contra `npm run dev` y después contra la versión de producción, con 29 comprobaciones. Todas pasaron en los dos casos. Las principales:

| Qué | Cómo | Resultado |
|---|---|---|
| El panel | Esperar los seis `.sp-root` con `data-status="ready"` | Los seis listos, también en el HTML sin JavaScript |
| Los datos en vivo | Leer el pie del tráfico, esperar 4,5 s y volver a leerlo | «Updated at 23:00» pasa a «Updated at 01:00» |
| El enlace | Pasar el puntero por las barras de errores | La hora se marca en el tráfico y en los dos indicadores |
| La lectura | Pasar el puntero por el tráfico | «14:00, 59k hits»; al salir, «Point at an hour» |
| La descarga | Pulsar «Download SVG» | `hits-per-hour.svg`, con `<style><![CDATA[` y el estilo base; abierto solo en Chrome, se ve igual que en la página |
| La tabla | Pulsar el encabezado «Minutes» | La primera fila pasa de INC-1042 a INC-1041 |
| La ventana y el aviso | Elegir INC-1038 y pulsar «Acknowledge» | La ventana se cierra y aparece «INC-1038 no longer pages the on-call team.» |
| El formulario | Elegir Hits, desactivar Active, escribir una nota y guardar | «Saved rule: hits ≥ 10, by email, paused. Notes: Page the database team», y sigue igual al volver a la página |
| La cianotipia | Elegirla en `/settings` y volver a la vista general | El fondo de la página y del panel pasa a `rgb(27, 63, 107)`, los seis gráficos llevan `sp-ground-cyanotype` y la tabla escribe en blanco |
| Una paleta | Volver a Silverpoint y elegir `sanguine` | El fondo pasa a `rgb(242, 232, 220)`, los gráficos llevan `--sp-ink: #8A3A24`, y el SVG descargado también |
| La consola | Recoger errores y avisos | En producción, ninguno. En desarrollo, solo `SP016` y `SP003`, los dos explicados arriba |

También pasaron `npx tsc --noEmit` y la compilación de producción, que comprueba los tipos.

## Lo que cuesta

Medí la versión de producción con gzip:

| Ruta | HTML | JavaScript | CSS |
|---|---|---|---|
| `/` | 78,4 kB (11,8 kB con gzip) | 995,2 kB (309,7 kB con gzip) | 150,0 kB (15,3 kB con gzip) |
| `/incidents` | 18,8 kB (3,9 kB con gzip) | 987,1 kB (307,9 kB con gzip) | 150,0 kB (15,3 kB con gzip) |
| `/settings` | 18,4 kB (3,8 kB con gzip) | 985,3 kB (307,1 kB con gzip) | 150,0 kB (15,3 kB con gzip) |

El HTML de `/` pesa más porque trae los seis gráficos dibujados. Los seis gráficos estaban listos 25 ms después de empezar la navegación, en mediana de tres cargas en mi máquina y en local: llegan en el HTML.

El JavaScript es casi igual en las tres rutas, y una parte se debe a `SilverpointProvider`. El proveedor solo se exporta desde la entrada general, `@silverpoint/react`, que contiene todos los gráficos. El [artículo 20](/blog/silverpoint_serie_20) midió que Vite descarta en producción los gráficos que no usas. Turbopack no lo hace con esta entrada: compilé la misma aplicación con el proveedor sustituido por un componente que solo devuelve sus hijos, y el JavaScript bajó de 1025 kB a 762 kB, unos 80 kB menos con gzip. Como el proveedor está en el diseño común, ese peso va en todas las rutas. Está abierto como [silverpoint#21](https://github.com/ecrespo/silverpoint/issues/21). Se corregirá en una próxima versión del paquete.

La hoja de los componentes de interfaz, `ui.css`, es la mayor parte del CSS.

## Problemas comunes

* **`Can't resolve '@silverpoint/grounds/styles.css'` con `?raw`.** Turbopack no aplica la consulta a la ruta del paquete. Usa la ruta relativa a `node_modules` y la regla de `next.config.ts`.
* **Un gráfico no cambia con el tema.** Es un componente de servidor, que no lee el contexto. Pasa el gráfico a un componente de cliente.
* **El marco del panel no cambia con el tema.** Pasa `ground` y `palette` al `Dashboard` ([issue #17](https://github.com/ecrespo/silverpoint/issues/17)).
* **El panel tiene dos columnas en una pantalla ancha.** Una regla de tu CSS sobre `section` le pone un ancho máximo: `Dashboard` es una `section`.
* **Avisos `SP003` al cambiar de página en desarrollo.** Son los gráficos de la página oculta. Se dibujan de nuevo al volver ([silverpoint#22](https://github.com/ecrespo/silverpoint/issues/22)).
* **`useSettings() needs a <SettingsProvider> above it`.** El componente se renderiza fuera de `SettingsProvider`. Todo lo que use `useSettings()` tiene que estar dentro de una página o del diseño común, bajo `app/layout.tsx`.

## Lo que viene

El [artículo 24](/blog/silverpoint_serie_24) construye la misma aplicación en Vue, con Vite y vue-router. Las páginas, los datos y las comprobaciones son los mismos, para que el [artículo 27](/blog/silverpoint_serie_27) pueda comparar las cuatro versiones.
