Title: Silverpoint, artículo 24: proyecto final en Vue, el panel de operaciones de principio a fin
Date: 2026-11-11 22:15
Category: Tutorial Silverpoint
Tags: silverpoint, vue, Visualización
lang: es
translation: true
Slug: silverpoint_serie_24
Authors: Ernesto Crespo
Summary: El panel de operaciones como aplicación completa en Vue 3 con Vite y vue-router: tres rutas, datos en vivo, panel enlazado, exportación a SVG, tabla de incidentes y ajustes que cambian el tema de toda la aplicación, con la compilación, el despliegue y las comprobaciones.

El nivel 4 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) junta las piezas de los niveles anteriores en una aplicación. El [artículo 23](/blog/silverpoint_serie_23) la construyó en React con Next.js. Este la construye en Vue 3, con Vite y vue-router: la misma aplicación, con las mismas tres páginas y los mismos datos.

No vuelve a explicar cada componente. Cada sección enlaza el artículo donde se presentó y se detiene en lo que cambia al juntarlos: un almacén compartido, el tema de toda la página, las rutas y el despliegue.

![La página Overview de la aplicación en Vue: indicadores, tráfico en vivo, errores enlazados por hora, mapa de calor y ventas por canal](./images/silverpoint-serie-24.png)

La página principal a 1440 píxeles de ancho. El puntero está en las 12:00 del tráfico: el gráfico muestra su descripción emergente, la hora 12 se marca en las barras de errores y en los dos indicadores, y la lectura de debajo dice «12:00, 64 thousand hits».

## La aplicación

Se llama Operations y tiene tres rutas:

| Ruta | Página | Lo que reúne |
|---|---|---|
| `/` | Overview | El panel enlazado (13) con datos en vivo (20), la lectura del elemento activo (11) y la descarga en SVG (18) |
| `/incidents` | Incidents | La tabla de incidentes con orden, paginación, ventana modal y aviso (17) |
| `/settings` | Settings | El formulario de la regla de alerta (16) y el tema: paleta y estilo base (09 y 12) |

Los ajustes se guardan en un almacén que comparten las tres páginas. Cambiar el tema en Settings cambia los gráficos, los componentes y la propia página, y el cambio se mantiene al navegar y al recargar.

## El proyecto

Parte del proyecto del [artículo 04](/blog/silverpoint_serie_4), con dos paquetes más: el enrutador de Vue y el motor de silverpoint como dependencia directa, porque la aplicación importa sus paletas y su función de orden.

```sh
npm create vite@latest ops-panel -- --template vue-ts --no-interactive
cd ops-panel
npm install @silverpoint/vue @silverpoint/grounds @silverpoint/fonts @silverpoint/core vue-router
```

Las versiones que usé: Vue 3.5.45, vue-router 5.5.0, Vite 8.3.8 y silverpoint 0.9.2. No hace falta Pinia: un objeto `reactive` en un módulo basta como almacén.

Como en el artículo 04, el ejemplo que trae la plantilla en `src/` se sustituye por los ficheros de la aplicación. La estructura completa:

```text
ops-panel/
├── index.html
├── package.json
├── vercel.json
├── vite.config.ts
├── public/
│   └── favicon.svg
└── src/
    ├── main.ts
    ├── router.ts
    ├── settings.ts
    ├── App.vue
    ├── style.css
    ├── data/
    │   ├── ops.ts
    │   └── incidents.ts
    ├── lib/
    │   ├── live.ts
    │   └── svg.ts
    ├── components/
    │   └── AlertRuleForm.vue
    └── views/
        ├── OverviewView.vue
        ├── IncidentsView.vue
        └── SettingsView.vue
```

`vite.config.ts` y los `tsconfig` son los de la plantilla, sin cambios. En `index.html` solo cambia el título. `src/data/ops.ts` tiene las filas del panel del [artículo 13](/blog/silverpoint_serie_13) y `src/data/incidents.ts`, los 12 incidentes del [artículo 17](/blog/silverpoint_serie_17).

## La entrada y las rutas

`src/main.ts` importa las hojas de estilos una vez, como en el artículo 04, más la de los componentes de interfaz del [artículo 16](/blog/silverpoint_serie_16), y registra el enrutador:

```ts
import { createApp } from 'vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import './style.css';
import App from './App.vue';
import { router } from './router';

createApp(App).use(router).mount('#app');
```

`src/router.ts` declara las tres rutas:

```ts
import { createRouter, createWebHistory } from 'vue-router';
import OverviewView from './views/OverviewView.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'overview', component: OverviewView, meta: { title: 'Overview' } },
    {
      path: '/incidents',
      name: 'incidents',
      component: () => import('./views/IncidentsView.vue'),
      meta: { title: 'Incidents' },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('./views/SettingsView.vue'),
      meta: { title: 'Settings' },
    },
  ],
});

router.afterEach((to) => {
  document.title = `${String(to.meta.title)} · Operations`;
});
```

Overview se importa de forma normal, porque es la primera página que ve casi todo el mundo. Incidents y Settings se cargan con `import()` la primera vez que se visitan, y Vite las separa en sus propios ficheros sin más configuración. `afterEach` pone el título de la pestaña: «Incidents · Operations».

`createWebHistory` da direcciones limpias, como `/settings`, sin `#`. El precio está en el despliegue: el servidor tiene que devolver `index.html` para cualquier ruta. Lo vemos al final.

## El almacén de ajustes

`src/settings.ts` guarda el tema y la regla de alerta, y calcula a partir de ellos lo que necesita el resto de la aplicación:

```ts
import { computed, reactive, watch } from 'vue';
import type { GroundName, Palette } from '@silverpoint/core';
import { PALETTES, paletteStyle } from '@silverpoint/core/palettes';

export type AlertRule = {
  metric: string;
  threshold: number;
  channel: string;
  active: boolean;
  notes: string;
};

export type Settings = {
  palette: string;
  cyanotype: boolean;
  rule: AlertRule;
};

const KEY = 'ops-settings';

const defaults: Settings = {
  palette: 'silverpoint',
  cyanotype: false,
  rule: { metric: 'errors', threshold: 10, channel: 'email', active: true, notes: '' },
};

function load(): Settings {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) ?? 'null') as Partial<Settings> | null;
    return { ...defaults, ...saved, rule: { ...defaults.rule, ...saved?.rule } };
  } catch {
    return defaults;
  }
}

export const settings = reactive<Settings>(load());

watch(settings, (value) => {
  try {
    localStorage.setItem(KEY, JSON.stringify(value));
  } catch {
    // Private mode or blocked storage: the settings last for this visit only.
  }
});

// What the provider receives: the cyanotype ground has its own colours, so no palette.
export const theme = computed<{ ground: GroundName; palette?: Palette }>(() =>
  settings.cyanotype
    ? { ground: 'cyanotype' }
    : { ground: 'silverpoint', palette: PALETTES[settings.palette] },
);

// The cyanotype ground's colours, for the elements that are not silverpoint's.
const CYANOTYPE: Palette = {
  substrate: '#1B3F6B',
  ink: '#E2EAF2',
  rule: '#8AA8C7',
  text: '#F4F6F8',
  textMuted: '#B8CBDE',
};

// The same --sp-* properties on the page itself: nav, headings and background follow the theme.
export const shellStyle = computed(() =>
  paletteStyle(settings.cyanotype ? CYANOTYPE : PALETTES[settings.palette]),
);
```

Tiene tres partes:

* **El estado.** `settings` es un objeto `reactive` del módulo. Cualquier componente que lo importe lee y escribe el mismo objeto, y Vue vuelve a dibujar lo que depende de él.
* **La persistencia.** `watch` lo guarda en `localStorage` cada vez que cambia, y `load` lo recupera al arrancar. Las dos llamadas van en `try`/`catch`: con el almacenamiento bloqueado, los ajustes duran lo que dura la visita.
* **Los valores derivados.** `theme` es lo que recibe el proveedor del [artículo 09](/blog/silverpoint_serie_9): el estilo base y la paleta. `shellStyle` son las mismas propiedades `--sp-*` en forma de texto, para la página.

`PALETTES` está tipado como un registro de texto a paleta, así que `keyof typeof PALETTES` es `string`, no los seis nombres. Por eso `palette` es un `string`, y la lista de nombres sale de `PALETTE_NAMES`.

Con la cianotipia no se aplica ninguna paleta. Las seis paletas del [artículo 12](/blog/silverpoint_serie_12) son variaciones del estilo base `silverpoint`: todas tienen un sustrato claro y tinta oscura. Ponerlas sobre azul de Prusia rompería el contraste.

## El tema de toda la página

El proveedor solo pinta los elementos de silverpoint. El artículo 12 lo dejaba como problema común: el fondo de la página no cambia con el tema. En una aplicación completa sí tiene que cambiar, o la cianotipia queda en recuadros azules sobre papel crema.

`src/App.vue` lo resuelve con un envoltorio:

```vue
<script setup lang="ts">
import { SilverpointProvider } from '@silverpoint/vue';
import { settings, shellStyle, theme } from './settings';
</script>

<template>
  <SilverpointProvider :ground="theme.ground" :palette="theme.palette">
    <div class="app" :style="shellStyle" :data-ground="theme.ground">
      <header>
        <strong>Operations</strong>
        <nav aria-label="Main">
          <RouterLink to="/">Overview</RouterLink>
          <RouterLink to="/incidents">Incidents</RouterLink>
          <RouterLink to="/settings">Settings</RouterLink>
        </nav>
        <small>{{ settings.cyanotype ? 'cyanotype' : settings.palette }}</small>
      </header>
      <main>
        <RouterView />
      </main>
    </div>
  </SilverpointProvider>
</template>
```

`SilverpointProvider` no dibuja nada alrededor de su contenido, así que el envoltorio `div.app` es el que recibe `shellStyle`. La hoja de estilos de la aplicación usa esas propiedades para el fondo, el texto y la navegación:

```css
body {
  margin: 0;
}

/* The page takes the theme's colours from the --sp-* properties set by shellStyle. */
.app {
  min-height: 100vh;
  padding: 24px 32px;
  box-sizing: border-box;
  background: var(--sp-substrate);
  color: var(--sp-text);
  font-family: 'EB Garamond', Georgia, serif;
}

header {
  display: flex;
  align-items: baseline;
  gap: 32px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--sp-rule);
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  color: var(--sp-ink);
  text-decoration: none;
}

nav a[aria-current='page'] {
  text-decoration: underline;
}

header small {
  margin-left: auto;
  color: var(--sp-text-muted);
}
```

`RouterLink` añade `aria-current="page"` al enlace de la página actual sin código, y la regla `nav a[aria-current='page']` lo subraya. El resto de `style.css` coloca las páginas y repite el ajuste de las celdas de `SpTable` del artículo 17.

Para la cianotipia, `settings.ts` copia cinco colores del estilo base, los de `@silverpoint/grounds/styles.css`, porque no hay una paleta con ese nombre. Para el estilo base `silverpoint`, la paleta elegida ya trae su sustrato.

## La página principal

Los datos en vivo son los del [artículo 20](/blog/silverpoint_serie_20), adaptados a las filas del panel, que también llevan los errores. `src/lib/live.ts`:

```ts
import { hourly, type HourRow } from '../data/ops';

// The next reading: the hour after the last one, taken from the day's
// profile with a small variation that changes from tick to tick.
function nextReading(last: HourRow, tick: number): HourRow {
  const hour = (Number(last.hour) + 1) % 24;
  return {
    hour: String(hour).padStart(2, '0'),
    hits: hourly[hour].hits + ((tick * 7) % 9) - 4,
    errors: hourly[hour].errors,
  };
}

// A rolling window: drop the oldest hour and append the new one.
export function advance(rows: readonly HourRow[], tick: number): HourRow[] {
  return [...rows.slice(1), nextReading(rows[rows.length - 1], tick)];
}
```

La descarga es la del [artículo 18](/blog/silverpoint_serie_18), con la hoja del estilo base dentro del SVG. `src/lib/svg.ts`:

```ts
import groundCss from '@silverpoint/grounds/styles.css?raw';

// The exported SVG does not carry the ground's stylesheet: inline it (article 18).
export function downloadSvg(svg: string, filename: string) {
  const open = svg.indexOf('>') + 1;
  const standalone = `${svg.slice(0, open)}<style><![CDATA[${groundCss}]]></style>${svg.slice(open)}`;
  const url = URL.createObjectURL(new Blob([standalone], { type: 'image/svg+xml' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
```

Y la página, `src/views/OverviewView.vue`:

```vue
<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, shallowRef } from 'vue';
import { SpBarChart } from '@silverpoint/vue/bar-chart';
import { SpDashboard, SpDashboardCell, type DashboardLayout } from '@silverpoint/vue/dashboard';
import { SpDonutChart } from '@silverpoint/vue/donut-chart';
import { SpHeatmapChart } from '@silverpoint/vue/heatmap-chart';
import { SpKpiCard } from '@silverpoint/vue/kpi-card';
import { SpLineChart, type ActiveItem } from '@silverpoint/vue/line-chart';
import { blocks, errorsByDay, hourly, sales } from '../data/ops';
import { advance } from '../lib/live';
import { downloadSvg } from '../lib/svg';
import { theme } from '../settings';

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

// Live data (article 20): a new reading every 2 s on a rolling 24-hour window.
const rows = shallowRef(hourly);
const hitsToday = computed(() => rows.value.reduce((sum, row) => sum + row.hits, 0));
const errorsToday = computed(() => rows.value.reduce((sum, row) => sum + row.errors, 0));
const last = computed(() => rows.value[rows.value.length - 1]);

let timer: ReturnType<typeof setInterval> | undefined;

onMounted(() => {
  let tick = 0;
  timer = setInterval(() => {
    tick += 1;
    rows.value = advance(rows.value, tick);
  }, 2000);
});

onUnmounted(() => clearInterval(timer));

// The hour under the pointer or the keyboard (article 11).
const active = ref<ActiveItem | null>(null);

// The SVG of the hits chart, with the stylesheet inlined (article 18).
const chart = ref<InstanceType<typeof SpLineChart>>();

function exportChart() {
  const svg = chart.value?.toSVGString();
  if (svg) downloadSvg(svg, 'hits-per-hour.svg');
}
</script>

<template>
  <SpDashboard
    id="ops"
    title="Operations"
    description="Traffic, errors and sales of the web service today."
    :layout="layout"
    :link="{ key: 'hour' }"
    :ground="theme.ground"
    :palette="theme.palette"
  >
    <SpDashboardCell cell="hits-today">
      <SpKpiCard title="Hits today" :data="rows" value-key="hits" :value="hitsToday" unit="thousand hits" :delta="4.2" />
    </SpDashboardCell>
    <SpDashboardCell cell="errors-today">
      <SpKpiCard title="Errors today" :data="rows" value-key="errors" :value="errorsToday" unit="errors" :delta="-12" />
    </SpDashboardCell>
    <SpDashboardCell cell="traffic">
      <SpLineChart
        ref="chart"
        id="hits"
        title="Hits per hour"
        badge="Live"
        :data="rows"
        x-key="hour"
        value-key="hits"
        footer-left="Thousands"
        :footer-right="`Updated at ${last.hour}:00`"
        @active-change="active = $event"
      />
    </SpDashboardCell>
    <SpDashboardCell cell="errors-hour">
      <SpBarChart title="Errors per hour" :data="rows" x-key="hour" value-key="errors" />
    </SpDashboardCell>
    <SpDashboardCell cell="errors-day">
      <SpHeatmapChart
        title="Errors by day"
        :data="errorsByDay"
        label-key="day"
        values-key="values"
        :column-labels="blocks"
        :scale-max="40"
      />
    </SpDashboardCell>
    <SpDashboardCell cell="channels">
      <SpDonutChart title="Sales by channel" :data="sales" name-key="channel" value-key="sales" center-label="thousand EUR" />
    </SpDashboardCell>
  </SpDashboard>
  <div class="toolbar">
    <p role="status">
      <template v-if="active">{{ active.datum.hour }}:00, {{ active.value }} thousand hits</template>
      <template v-else>Point at the hits chart to read an hour.</template>
    </p>
    <button type="button" @click="exportChart">Download SVG</button>
  </div>
</template>
```

Lo nuevo respecto a los artículos de origen:

* **Los indicadores siguen a los datos en vivo.** «Hits today» y «Errors today» suman la ventana de 24 horas. Al cargar dan 886 y 103, las cifras del artículo 13, y cambian con cada lectura nueva. Las barras de errores también usan `rows`, así que el enlace por `hour` sigue funcionando mientras la ventana avanza.
* **El panel recibe el tema.** `SpDashboard` no lee el proveedor, igual que en React; la documentación dice lo contrario, y está abierto como [silverpoint#17](https://github.com/ecrespo/silverpoint/issues/17). Sus gráficos sí lo leen, pero el marco del panel, con su fondo y su título, se quedaba en crema bajo la cianotipia. Por eso recibe `:ground` y `:palette` del mismo `theme`.
* **La lectura y la descarga, fuera del panel.** `@active-change` guarda el elemento activo del tráfico, como en el [artículo 11](/blog/silverpoint_serie_11), y el botón llama a `toSVGString()` a través de `ref="chart"`.

El temporizador se crea en `onMounted` y se borra en `onUnmounted`. Al ir a otra página, la ventana deja de avanzar; al volver, empieza otra vez desde los datos del día. Si quieres que siga corriendo entre páginas, mueve `rows` y el temporizador a un módulo, como el almacén.

En desarrollo, el mapa de calor y el donut avisan con `SP016`: no tienen el campo `hour`. Es lo esperado, como explica el artículo 13, y el aviso no aparece en la compilación de producción.

## Los incidentes

`src/views/IncidentsView.vue` es el componente `Incidents.vue` del artículo 17 con dos cambios: importa los datos de `../data/incidents` y su `section` lleva la clase `incidents`, que usa `style.css` para el ancho y la rejilla.

Su estado es local: el orden, la página y los incidentes confirmados viven en el componente. Al salir de la página y volver, la tabla empieza de nuevo. En una aplicación real, las confirmaciones irían al servidor; aquí, para conservarlas en el navegador, bastaría con moverlas al almacén.

## Los ajustes

`src/views/SettingsView.vue` tiene el tema y el formulario:

```vue
<script setup lang="ts">
import { PALETTE_NAMES } from '@silverpoint/core/palettes';
import { SpSelect } from '@silverpoint/vue/ui/select';
import { SpSwitch } from '@silverpoint/vue/ui/switch';
import AlertRuleForm from '../components/AlertRuleForm.vue';
import { settings } from '../settings';
</script>

<template>
  <div class="settings">
    <section aria-labelledby="theme-title">
      <h2 id="theme-title">Theme</h2>
      <SpSwitch label="Cyanotype" v-model="settings.cyanotype" />
      <SpSelect
        label="Palette"
        :items="PALETTE_NAMES"
        :disabled="settings.cyanotype"
        v-model="settings.palette"
      />
      <p v-if="settings.cyanotype">The cyanotype ground has its own colours: no palette applies.</p>
    </section>
    <section aria-labelledby="rule-title">
      <h2 id="rule-title">Alert rule</h2>
      <AlertRuleForm />
    </section>
  </div>
</template>
```

`SpSwitch` y `SpSelect` escriben directamente en el almacén con `v-model`. El cambio es inmediato: los colores de la página cambian mientras eliges, sin recargar. Con la cianotipia activa, la lista de paletas queda desactivada y la página dice por qué.

El formulario es el del artículo 16, `src/components/AlertRuleForm.vue`, ahora conectado al almacén:

```vue
<script setup lang="ts">
import { reactive, ref } from 'vue';
import { SpButton } from '@silverpoint/vue/ui/button';
import { SpRadioGroup } from '@silverpoint/vue/ui/radio-group';
import { SpSegmented } from '@silverpoint/vue/ui/segmented';
import { SpSlider } from '@silverpoint/vue/ui/slider';
import { SpSwitch } from '@silverpoint/vue/ui/switch';
import { SpTextarea } from '@silverpoint/vue/ui/textarea';
import { settings } from '../settings';

const METRICS = [
  { key: 'errors', label: 'Errors' },
  { key: 'hits', label: 'Hits' },
];

const CHANNELS = [
  { key: 'email', label: 'Email' },
  { key: 'chat', label: 'Chat' },
  { key: 'sms', label: 'SMS', disabled: true },
];

// The form edits a copy; "Save rule" writes it to the store.
const draft = reactive({ ...settings.rule });
const saved = ref('');

function save() {
  Object.assign(settings.rule, draft);
  const { metric, threshold, channel, active, notes } = settings.rule;
  saved.value = `${metric} ≥ ${threshold}, by ${channel}, ${active ? 'active' : 'paused'}. Notes: ${notes || '—'}`;
}
</script>

<template>
  <form @submit.prevent="save">
    <SpSegmented label="Metric" name="metric" :items="METRICS" v-model="draft.metric" />
    <SpSlider
      label="Threshold"
      name="threshold"
      :min="0"
      :max="50"
      :step="5"
      :marks="[0, 25, 50]"
      v-model="draft.threshold"
    />
    <SpRadioGroup
      label="Notify by"
      name="channel"
      :items="CHANNELS"
      orientation="horizontal"
      v-model="draft.channel"
    />
    <SpSwitch label="Active" name="active" v-model="draft.active" />
    <SpTextarea
      label="Notes"
      placeholder="Notes for the on-call team"
      name="notes"
      :rows="2"
      :max-length="200"
      show-count
      v-model="draft.notes"
    />
    <SpButton type="submit" variant="primary">Save rule</SpButton>
    <p role="status">{{ saved }}</p>
  </form>
</template>
```

Edita una copia de la regla, `draft`, y solo la escribe en el almacén al pulsar Save rule. Así, un cambio a medias no se guarda. Las notas pasan de `default-value` a `v-model`, porque ahora el valor inicial viene de la regla guardada.

## Ejecutar, compilar y desplegar

En desarrollo:

```sh
npm run dev
```

Para producción, `npm run build` comprueba los tipos con `vue-tsc` y compila con Vite en `dist/`. `npm run preview` sirve esa carpeta para probarla.

```sh
npm run build
npm run preview
```

Lo que produjo la compilación:

| Fichero | Tamaño | Con gzip |
|---|---|---|
| `index-*.js`: la aplicación, el enrutador, Overview y sus seis gráficos | 238,3 kB | 82,7 kB |
| `chunk-*.js`: piezas comunes de los componentes de interfaz | 25,8 kB | 9,6 kB |
| `IncidentsView-*.js` | 6,6 kB | 2,6 kB |
| `SettingsView-*.js` | 5,3 kB | 1,8 kB |
| `index-*.css`: estilos base, componentes, tipografía y aplicación | 153,8 kB | 15,7 kB |

La primera visita a `/` descarga unos 98 kB comprimidos de JavaScript y CSS, más la tipografía. Las otras dos páginas se descargan cuando se visitan.

`dist/` es un sitio estático: se puede servir desde cualquier alojamiento de ficheros. La única condición viene del historial del navegador: una visita directa a `/settings` tiene que recibir `index.html`, y vue-router dibuja la página. `npm run preview` ya lo hace. En Vercel, `vercel.json` lo declara con una reescritura:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

Otros servicios tienen su equivalente. Sin esa regla, recargar la página en `/incidents` da un 404 del servidor.

## Lo que comprobé

Con la aplicación en el servidor de desarrollo y, después, con la compilación de producción en `npm run preview`, un script de Playwright con Chrome recorrió las tres páginas:

| Comprobación | Resultado |
|---|---|
| Overview | Seis gráficos con `data-status="ready"`; título «Overview · Operations» |
| Datos en vivo | Tras 4 segundos la línea es otra, el indicador cambia y el pie pasa de «Updated at 23:00» a «Updated at 01:00» |
| Elemento activo y enlace | Con el puntero en el tráfico, la lectura dice la hora y su valor, y aparece la marca enlazada en las barras y en los dos indicadores |
| Descarga | `hits-per-hour.svg`, con `<svg` al principio y la hoja del estilo base en un bloque CDATA |
| Incidents | Orden por minutos, página 2, ventana modal que se cierra con Escape y devuelve el foco, confirmación de INC-1040 y aviso |
| Formulario | Tras guardar: «hits ≥ 15, by chat, active. Notes: Page the on-call team», y la regla sigue en el formulario al volver a la página |
| Paleta | Con `sanguine`, el fondo de la página, el marco del panel, los gráficos y el botón Save rule usan sus colores |
| Cianotipia | Fondo azul de Prusia en la página y en el panel; los seis gráficos con la clase `sp-ground-cyanotype`; la lista de paletas desactivada |
| Persistencia | Tras recargar, la cianotipia sigue activa; una visita directa a `/settings` carga la página |

`npm run build` termina sin errores de tipos. En la consola de producción no hubo errores ni avisos.

## Problemas comunes

* **El marco del panel no cambia de tema.** `SpDashboard` no lee el proveedor. Pásale `:ground` y `:palette` además de ponerlo dentro de `SilverpointProvider` ([silverpoint#17](https://github.com/ecrespo/silverpoint/issues/17)). Se corregirá en una próxima versión del paquete.
* **El fondo de la página sigue crema con la cianotipia.** El proveedor solo pinta silverpoint. Pon las propiedades `--sp-*` en un elemento propio con `paletteStyle` y úsalas en tu CSS.
* **TypeScript acepta cualquier nombre de paleta.** `PALETTES` es un registro de texto, y `PALETTES['blue']` devuelve `undefined` sin error. Ofrece solo los nombres de `PALETTE_NAMES` ([silverpoint#20](https://github.com/ecrespo/silverpoint/issues/20)). Se corregirá en una próxima versión del paquete.
* **Recargar en `/incidents` da 404 en el servidor.** Falta la reescritura a `index.html` para el historial del navegador.
* **Los datos en vivo empiezan de nuevo al volver a Overview.** El temporizador vive en la página. Si tiene que seguir entre páginas, llévalo a un módulo.

## Lo que viene

El [artículo 25](/blog/silverpoint_serie_25) construye la misma aplicación en Angular, con su enrutador, componentes independientes y señales. El [artículo 27](/blog/silverpoint_serie_27) comparará las cuatro versiones con las medidas de cada una.
