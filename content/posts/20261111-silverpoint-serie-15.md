Title: Silverpoint, artículo 15: jerarquías, flujos y redes, con navegación por niveles
Date: 2026-11-11 18:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_15
Authors: Ernesto Crespo
Summary: Los gráficos de silverpoint para datos con estructura: un mapa de árbol y un sunburst que bajan de nivel juntos, un árbol de nodos, un diagrama de Sankey y un grafo de red, con la navegación por teclado y el mismo código en React, Vue, Angular y Reflex.

Este artículo cierra el nivel 2 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) con los datos que no caben en una tabla plana de filas y columnas: una jerarquía, un flujo entre etapas y una red de dependencias. Los tres salen del panel de operaciones: lo que cuesta cada mes la infraestructura del servicio, por dónde llegan las visitas y qué servicios se llaman entre sí.

La parte central es la navegación por niveles. Un mapa de árbol y un sunburst muestran la misma jerarquía y bajan de nivel juntos, con el ratón o con el teclado.

## Lo que vas a construir

![El mapa de árbol y el sunburst abiertos en el nivel Storage, con el árbol de costes, el Sankey de visitas y la red de servicios debajo](./images/silverpoint-serie-15.png)

Arriba, el coste mensual de la infraestructura, en miles de euros. Al elegir un área, el mapa de árbol y el sunburst pasan a mostrar solo sus servicios: en la imagen, los de Storage. Debajo, la misma jerarquía como árbol, las visitas de un día de canal a página y a resultado, y las llamadas por segundo entre servicios.

## Los datos

Una jerarquía en silverpoint es una lista plana de filas. Cada fila tiene un `id` y el `id` de su padre, `parent`, que es `null` en la raíz. No se anidan los hijos dentro de los padres.

El valor solo se escribe en las hojas. El de un nodo interno es la suma de sus hijos: Storage vale 7,2 + 2,6 + 1,4 = 11,2. En React y Vue, este archivo es `src/infra.ts`; en Angular, `src/app/infra.ts`:

```ts
export type CostRow = { id: string; parent: string | null; name: string; cost?: number };
export type FlowRow = { from: string; to: string; visits: number };
export type CallRow = { caller: string; callee: string; rps: number };

export const costs: CostRow[] = [
  { id: 'infra', parent: null, name: 'Infrastructure' },
  { id: 'compute', parent: 'infra', name: 'Compute' },
  { id: 'api', parent: 'compute', name: 'API servers', cost: 12.4 },
  { id: 'workers', parent: 'compute', name: 'Workers', cost: 6.8 },
  { id: 'search', parent: 'compute', name: 'Search', cost: 4.1 },
  { id: 'storage', parent: 'infra', name: 'Storage' },
  { id: 'database', parent: 'storage', name: 'Database', cost: 7.2 },
  { id: 'objects', parent: 'storage', name: 'Object storage', cost: 2.6 },
  { id: 'backups', parent: 'storage', name: 'Backups', cost: 1.4 },
  { id: 'network', parent: 'infra', name: 'Network' },
  { id: 'cdn', parent: 'network', name: 'CDN', cost: 3.9 },
  { id: 'balancers', parent: 'network', name: 'Load balancers', cost: 1.8 },
  { id: 'egress', parent: 'network', name: 'Egress', cost: 2.2 },
  { id: 'observability', parent: 'infra', name: 'Observability' },
  { id: 'logs', parent: 'observability', name: 'Logs', cost: 2.4 },
  { id: 'metrics', parent: 'observability', name: 'Metrics', cost: 1.6 },
  { id: 'traces', parent: 'observability', name: 'Traces', cost: 0.9 },
];

export const visits: FlowRow[] = [
  { from: 'Search', to: 'Home', visits: 30 },
  { from: 'Search', to: 'Product', visits: 22 },
  { from: 'Social', to: 'Home', visits: 18 },
  { from: 'Social', to: 'Pricing', visits: 6 },
  { from: 'Email', to: 'Product', visits: 10 },
  { from: 'Email', to: 'Pricing', visits: 8 },
  { from: 'Direct', to: 'Home', visits: 12 },
  { from: 'Direct', to: 'Pricing', visits: 6 },
  { from: 'Home', to: 'Signup', visits: 9 },
  { from: 'Home', to: 'Exit', visits: 51 },
  { from: 'Product', to: 'Purchase', visits: 7 },
  { from: 'Product', to: 'Signup', visits: 5 },
  { from: 'Product', to: 'Exit', visits: 20 },
  { from: 'Pricing', to: 'Purchase', visits: 6 },
  { from: 'Pricing', to: 'Signup', visits: 6 },
  { from: 'Pricing', to: 'Exit', visits: 8 },
];

export const calls: CallRow[] = [
  { caller: 'web', callee: 'api', rps: 120 },
  { caller: 'api', callee: 'database', rps: 80 },
  { caller: 'api', callee: 'cache', rps: 150 },
  { caller: 'api', callee: 'search', rps: 40 },
  { caller: 'api', callee: 'queue', rps: 25 },
  { caller: 'queue', callee: 'workers', rps: 25 },
  { caller: 'workers', callee: 'database', rps: 18 },
  { caller: 'workers', callee: 'objects', rps: 12 },
  { caller: 'search', callee: 'database', rps: 6 },
];
```

Las otras dos listas son enlaces: cada fila une un origen con un destino y lleva un valor. `visits` son miles de visitas de un día, y `calls`, llamadas por segundo.

Si la jerarquía tiene un `id` repetido, un `parent` que no existe, un ciclo o más de una raíz, el gráfico descarta las filas que fallan y, en desarrollo, avisa con `SP020`.

## La página en React

Sustituye `src/App.tsx`:

```tsx
import { useState } from 'react';
import { NetworkChart } from '@silverpoint/react/network-chart';
import { SankeyChart } from '@silverpoint/react/sankey-chart';
import { SquarifiedTreemap } from '@silverpoint/react/squarified-treemap';
import { SunburstChart } from '@silverpoint/react/sunburst-chart';
import { TreeChart } from '@silverpoint/react/tree-chart';
import { calls, costs, visits } from './infra';

const keys = { idKey: 'id', parentKey: 'parent', labelKey: 'name', valueKey: 'cost' };
const parents = new Set(costs.map((row) => row.parent));

export default function App() {
  const [root, setRoot] = useState<string | null>(null);
  const showing = costs.find((row) => row.id === (root ?? 'infra'))?.name;

  // Drill into areas only: a service has no children to show.
  const drill = (id: string | null) => {
    if (id === null || parents.has(id)) setRoot(id);
  };

  return (
    <main>
      <p>
        Showing: {showing}{' '}
        <button type="button" disabled={root === null} onClick={() => setRoot(null)}>
          Back to top
        </button>
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: '3fr 2fr', gap: 16 }}>
        <SquarifiedTreemap
          title="Monthly infrastructure cost"
          data={costs}
          {...keys}
          rootId={root}
          onRootChange={drill}
          depth={1}
          height={260}
        />
        <SunburstChart
          title="Cost by area"
          data={costs}
          {...keys}
          rootId={root}
          onRootChange={drill}
          height={260}
        />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginTop: 16 }}>
        <TreeChart title="Cost structure" data={costs} {...keys} height={260} />
        <SankeyChart
          title="Visits by channel"
          data={visits}
          sourceKey="from"
          targetKey="to"
          valueKey="visits"
          height={260}
        />
        <NetworkChart
          title="Service calls"
          data={calls}
          sourceKey="caller"
          targetKey="callee"
          valueKey="rps"
          height={260}
        />
      </div>
    </main>
  );
}
```

## Bajar de nivel

`SquarifiedTreemap` y `SunburstChart` se pueden recorrer por niveles, pero no guardan el nivel actual: lo guardas tú.

| Prop | Qué hace |
|---|---|
| `rootId` | El `id` del nodo que se dibuja como raíz; `null` es la raíz de los datos |
| `onRootChange` | Recibe el `id` del nodo que el usuario quiere abrir |
| `depth` | Los niveles que se dibujan bajo la raíz; todos, por defecto |

Al hacer clic en un nodo, o al pulsar `Enter` o la barra espaciadora sobre él, el gráfico llama a `onRootChange` con su `id`. Tú decides si lo aceptas y lo devuelves en `rootId`. Como los dos gráficos reciben el mismo `rootId`, bajan juntos: elegir Storage en uno abre Storage en los dos.

Que el estado sea tuyo permite reglas propias. El gráfico también envía el `id` de una hoja, y abrir una hoja deja un rectángulo solo. Por eso `drill` acepta únicamente los nodos que son padre de alguna fila. Con `depth={1}`, el mapa de árbol dibuja solo un nivel bajo la raíz: las cuatro áreas arriba del todo y los servicios del área abierta. El sunburst no fija `depth` y dibuja todos los anillos.

Para subir hay dos caminos. El botón «Back to top» pone `null`. Y, con la raíz actual activa, `Enter` sube un nivel: envía el `id` de su padre, o `null` cuando el padre es la raíz de los datos. Desde Storage, la flecha abajo activa Storage y `Enter` vuelve arriba.

## El teclado

Los gráficos de jerarquía siguen el patrón de árbol de WAI-ARIA. Con el foco en el mapa de árbol:

| Tecla | Lleva a |
|---|---|
| Flecha abajo y flecha arriba | El nodo siguiente o el anterior, en profundidad |
| Flecha derecha | El primer hijo |
| Flecha izquierda | El padre |
| Inicio y Fin | El primer nodo y el último |
| `Enter` o barra espaciadora | Abrir el nodo |

Cada nodo se anuncia con su ruta desde la raíz, su valor y su parte del padre. Este es el recorrido medido en el navegador, desde la raíz:

| Pulsación | Anuncio |
|---|---|
| `Tab` | node Infrastructure, cost 47.3 |
| Flecha abajo | node Infrastructure › Compute, cost 23.3, 49.3% of Infrastructure |
| Flecha abajo | node Infrastructure › Storage, cost 11.2, 23.7% of Infrastructure |
| `Enter` | Abre Storage |
| Flecha abajo, dos veces | node Infrastructure › Storage › Database, cost 7.2, 64.3% of Storage |

El árbol de nodos, `TreeChart`, se recorre con las mismas teclas.

## El árbol, el Sankey y la red

Los otros tres gráficos de la página no tienen estado.

* **`TreeChart`** dibuja la misma jerarquía como nodos unidos por líneas, con las mismas props de acceso (`idKey`, `parentKey`, `labelKey`, `valueKey`). Sirve cuando importa la estructura más que el tamaño de cada parte.
* **`SankeyChart`** lee enlaces con `sourceKey`, `targetKey` y `valueKey`. Los nodos salen de los extremos de los enlaces y se colocan por etapas: los canales, las páginas y los resultados. Cada nodo muestra su total (Home 60, Exit 79), y el teclado recorre los flujos: «flow Search → Home, visits 30».
* **`NetworkChart`** lee los mismos tres campos y coloca los nodos con una simulación de fuerzas con semilla, así que el dibujo es el mismo en cada carga. Solo nombra los tres nodos con más enlaces, aquí `api`, `database` y `workers`. Los demás se leen en la descripción emergente y en la tabla de datos. Su prop `nodes` acepta la lista de nodos con su `label`, su `group` o su posición, si no quieres que salgan de los enlaces.

## La página en Vue

En Vue el evento es `@root-change`, y el estado, un `ref`. Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { computed, ref } from 'vue';
import { SpNetworkChart } from '@silverpoint/vue/network-chart';
import { SpSankeyChart } from '@silverpoint/vue/sankey-chart';
import { SpSquarifiedTreemap } from '@silverpoint/vue/squarified-treemap';
import { SpSunburstChart } from '@silverpoint/vue/sunburst-chart';
import { SpTreeChart } from '@silverpoint/vue/tree-chart';
import { calls, costs, visits } from './infra';

const parents = new Set(costs.map((row) => row.parent));
const root = ref<string | null>(null);
const showing = computed(() => costs.find((row) => row.id === (root.value ?? 'infra'))?.name);

// Drill into areas only: a service has no children to show.
function drill(id: string | null) {
  if (id === null || parents.has(id)) root.value = id;
}
</script>

<template>
  <main>
    <p>
      Showing: {{ showing }}
      <button type="button" :disabled="root === null" @click="root = null">Back to top</button>
    </p>
    <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 16px">
      <SpSquarifiedTreemap
        title="Monthly infrastructure cost"
        :data="costs"
        id-key="id"
        parent-key="parent"
        label-key="name"
        value-key="cost"
        :root-id="root"
        :depth="1"
        :height="260"
        @root-change="drill"
      />
      <SpSunburstChart
        title="Cost by area"
        :data="costs"
        id-key="id"
        parent-key="parent"
        label-key="name"
        value-key="cost"
        :root-id="root"
        :height="260"
        @root-change="drill"
      />
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px">
      <SpTreeChart title="Cost structure" :data="costs" id-key="id" parent-key="parent" label-key="name" value-key="cost" :height="260" />
      <SpSankeyChart title="Visits by channel" :data="visits" source-key="from" target-key="to" value-key="visits" :height="260" />
      <SpNetworkChart title="Service calls" :data="calls" source-key="caller" target-key="callee" value-key="rps" :height="260" />
    </div>
  </main>
</template>
```

## La página en Angular

En Angular, `rootId` recibe un signal y el evento es la salida `(rootChange)`. Sustituye `src/app/app.ts`:

```ts
import { Component, computed, signal } from '@angular/core';
import { SpNetworkChart } from '@silverpoint/angular/network-chart';
import { SpSankeyChart } from '@silverpoint/angular/sankey-chart';
import { SpSquarifiedTreemap } from '@silverpoint/angular/squarified-treemap';
import { SpSunburstChart } from '@silverpoint/angular/sunburst-chart';
import { SpTreeChart } from '@silverpoint/angular/tree-chart';
import { calls, costs, visits } from './infra';

const parents = new Set(costs.map((row) => row.parent));

@Component({
  selector: 'app-root',
  imports: [SpSquarifiedTreemap, SpSunburstChart, SpTreeChart, SpSankeyChart, SpNetworkChart],
  template: `
    <main>
      <p>
        Showing: {{ showing() }}
        <button type="button" [disabled]="root() === null" (click)="root.set(null)">Back to top</button>
      </p>
      <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 16px">
        <sp-squarified-treemap
          title="Monthly infrastructure cost"
          [data]="costs"
          idKey="id"
          parentKey="parent"
          labelKey="name"
          valueKey="cost"
          [rootId]="root()"
          [depth]="1"
          [height]="260"
          (rootChange)="drill($event)"
        />
        <sp-sunburst-chart
          title="Cost by area"
          [data]="costs"
          idKey="id"
          parentKey="parent"
          labelKey="name"
          valueKey="cost"
          [rootId]="root()"
          [height]="260"
          (rootChange)="drill($event)"
        />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px">
        <sp-tree-chart title="Cost structure" [data]="costs" idKey="id" parentKey="parent" labelKey="name" valueKey="cost" [height]="260" />
        <sp-sankey-chart title="Visits by channel" [data]="visits" sourceKey="from" targetKey="to" valueKey="visits" [height]="260" />
        <sp-network-chart title="Service calls" [data]="calls" sourceKey="caller" targetKey="callee" valueKey="rps" [height]="260" />
      </div>
    </main>
  `,
})
export class App {
  protected readonly costs = costs;
  protected readonly visits = visits;
  protected readonly calls = calls;
  protected readonly root = signal<string | null>(null);
  protected readonly showing = computed(() => costs.find((row) => row.id === (this.root() ?? 'infra'))?.name);

  // Drill into areas only: a service has no children to show.
  protected drill(id: string | null) {
    if (id === null || parents.has(id)) this.root.set(id);
  }
}
```

## La página en Reflex

En Reflex, los datos en `ops_panel/infra.py`:

```python
COSTS = [
    {"id": "infra", "parent": None, "name": "Infrastructure"},
    {"id": "compute", "parent": "infra", "name": "Compute"},
    {"id": "api", "parent": "compute", "name": "API servers", "cost": 12.4},
    {"id": "workers", "parent": "compute", "name": "Workers", "cost": 6.8},
    {"id": "search", "parent": "compute", "name": "Search", "cost": 4.1},
    {"id": "storage", "parent": "infra", "name": "Storage"},
    {"id": "database", "parent": "storage", "name": "Database", "cost": 7.2},
    {"id": "objects", "parent": "storage", "name": "Object storage", "cost": 2.6},
    {"id": "backups", "parent": "storage", "name": "Backups", "cost": 1.4},
    {"id": "network", "parent": "infra", "name": "Network"},
    {"id": "cdn", "parent": "network", "name": "CDN", "cost": 3.9},
    {"id": "balancers", "parent": "network", "name": "Load balancers", "cost": 1.8},
    {"id": "egress", "parent": "network", "name": "Egress", "cost": 2.2},
    {"id": "observability", "parent": "infra", "name": "Observability"},
    {"id": "logs", "parent": "observability", "name": "Logs", "cost": 2.4},
    {"id": "metrics", "parent": "observability", "name": "Metrics", "cost": 1.6},
    {"id": "traces", "parent": "observability", "name": "Traces", "cost": 0.9},
]

VISITS = [
    {"from": "Search", "to": "Home", "visits": 30},
    {"from": "Search", "to": "Product", "visits": 22},
    {"from": "Social", "to": "Home", "visits": 18},
    {"from": "Social", "to": "Pricing", "visits": 6},
    {"from": "Email", "to": "Product", "visits": 10},
    {"from": "Email", "to": "Pricing", "visits": 8},
    {"from": "Direct", "to": "Home", "visits": 12},
    {"from": "Direct", "to": "Pricing", "visits": 6},
    {"from": "Home", "to": "Signup", "visits": 9},
    {"from": "Home", "to": "Exit", "visits": 51},
    {"from": "Product", "to": "Purchase", "visits": 7},
    {"from": "Product", "to": "Signup", "visits": 5},
    {"from": "Product", "to": "Exit", "visits": 20},
    {"from": "Pricing", "to": "Purchase", "visits": 6},
    {"from": "Pricing", "to": "Signup", "visits": 6},
    {"from": "Pricing", "to": "Exit", "visits": 8},
]

CALLS = [
    {"caller": "web", "callee": "api", "rps": 120},
    {"caller": "api", "callee": "database", "rps": 80},
    {"caller": "api", "callee": "cache", "rps": 150},
    {"caller": "api", "callee": "search", "rps": 40},
    {"caller": "api", "callee": "queue", "rps": 25},
    {"caller": "queue", "callee": "workers", "rps": 25},
    {"caller": "workers", "callee": "database", "rps": 18},
    {"caller": "workers", "callee": "objects", "rps": 12},
    {"caller": "search", "callee": "database", "rps": 6},
]
```

Y la página, `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import (
    network_chart,
    sankey_chart,
    squarified_treemap,
    sunburst_chart,
    tree_chart,
)

from .infra import CALLS, COSTS, VISITS

KEYS = {
    "id_key": "id",
    "parent_key": "parent",
    "label_key": "name",
    "value_key": "cost",
}
NAMES = {row["id"]: row["name"] for row in COSTS}
PARENTS = {row["parent"] for row in COSTS}


class CostState(rx.State):
    root: str | None = None

    @rx.event
    def drill(self, node_id: str | None):
        # Drill into areas only: a service has no children to show.
        if node_id is None or node_id in PARENTS:
            self.root = node_id

    @rx.var
    def showing(self) -> str:
        return NAMES[self.root or "infra"]


def index() -> rx.Component:
    return rx.el.main(
        rx.el.p(
            "Showing: ",
            CostState.showing,
            " ",
            rx.el.button(
                "Back to top",
                type="button",
                disabled=CostState.root.is_none(),
                on_click=CostState.drill(None),
            ),
        ),
        rx.el.div(
            squarified_treemap(
                title="Monthly infrastructure cost",
                data=COSTS,
                **KEYS,
                root_id=CostState.root,
                on_root_change=CostState.drill,
                depth=1,
                height=260,
            ),
            sunburst_chart(
                title="Cost by area",
                data=COSTS,
                **KEYS,
                root_id=CostState.root,
                on_root_change=CostState.drill,
                height=260,
            ),
            display="grid",
            grid_template_columns="3fr 2fr",
            gap="16px",
        ),
        rx.el.div(
            tree_chart(title="Cost structure", data=COSTS, **KEYS, height=260),
            sankey_chart(
                title="Visits by channel",
                data=VISITS,
                source_key="from",
                target_key="to",
                value_key="visits",
                height=260,
            ),
            network_chart(
                title="Service calls",
                data=CALLS,
                source_key="caller",
                target_key="callee",
                value_key="rps",
                height=260,
            ),
            display="grid",
            grid_template_columns="1fr 1fr 1fr",
            gap="16px",
            margin_top="16px",
        ),
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

El nivel vive en el estado, `CostState.root`, y `on_root_change` es un evento del backend que recibe el `id` o `None`. El botón llama al mismo evento con `None`, y `CostState.root.is_none()` lo desactiva arriba del todo.

Los cuatro adaptadores se comprobaron en el navegador con el mismo recorrido: bajar a Storage con el teclado, intentar abrir la hoja Database (no pasa nada), volver arriba con el botón y abrir Network con un clic en el mapa de árbol.

## Problemas comunes

* **`SP020` en la consola.** La jerarquía tiene un `id` repetido, un `parent` que no existe, un ciclo o varias raíces. El aviso nombra la fila; el gráfico la descarta y dibuja el resto.
* **El gráfico no baja de nivel.** Falta devolver el `id` en `rootId`. El gráfico no guarda el nivel: si `onRootChange` no actualiza tu estado, nada cambia.
* **Un clic deja un rectángulo solo.** Se abrió una hoja. Filtra los `id` en tu manejador, como hace `drill`.
* **El mapa de árbol y el sunburst no van juntos.** Cada uno tiene su propio estado. Pásales la misma variable.
* **La red solo nombra tres nodos.** Es el diseño: los demás nombres están en la descripción emergente y en la tabla de datos.

## Lo que viene

Con este artículo termina el nivel 2. Ya tienes un panel con varios gráficos, un estilo común, interacción y navegación por niveles. El nivel 3 lo lleva a una aplicación completa, y empieza con el artículo 16: los componentes de interfaz para formularios y visualización.

La [galería](https://silverpointweb.vercel.app/gallery) muestra en vivo los gráficos de jerarquías, flujos y redes junto al resto del catálogo.
