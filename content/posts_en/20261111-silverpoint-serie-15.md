Title: Silverpoint, article 15: hierarchies, flows and networks, with level navigation
Date: 2026-11-11 18:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: en
translation: true
Slug: silverpoint_serie_15
Authors: Ernesto Crespo
Summary: silverpoint's charts for structured data: a treemap and a sunburst that drill down together, a node tree, a Sankey diagram and a network graph, with keyboard navigation and the same code in React, Vue, Angular and Reflex.

This article closes level 2 of the series on [silverpoint](https://github.com/ecrespo/silverpoint) with data that does not fit in a flat table of rows and columns: a hierarchy, a flow between stages and a network of dependencies. All three come from the operations panel: what the service's infrastructure costs each month, where visits come from and which services call each other.

The core is navigating by levels. A treemap and a sunburst show the same hierarchy and drill down together, with the mouse or with the keyboard.

## What you will build

![The treemap and the sunburst opened at the Storage level, with the cost tree, the visits Sankey and the services network below](./images/silverpoint-serie-15.png)

At the top, the monthly cost of the infrastructure, in thousands of euros. When you pick an area, the treemap and the sunburst switch to showing only its services: in the image, those of Storage. Below, the same hierarchy as a tree, a day's visits from channel to page to outcome, and the calls per second between services.

## The data

A hierarchy in silverpoint is a flat list of rows. Each row has an `id` and the `id` of its parent, `parent`, which is `null` at the root. Children are not nested inside their parents.

The value is written only on the leaves. That of an internal node is the sum of its children: Storage is 7.2 + 2.6 + 1.4 = 11.2. In React and Vue this file is `src/infra.ts`; in Angular, `src/app/infra.ts`:

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

The other two lists are links: each row joins a source to a target and carries a value. `visits` are thousands of visits in a day, and `calls`, calls per second.

If the hierarchy has a repeated `id`, a `parent` that does not exist, a cycle or more than one root, the chart drops the failing rows and, in development, warns with `SP020`.

## The page in React

Replace `src/App.tsx`:

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

## Drilling down

`SquarifiedTreemap` and `SunburstChart` can be explored by levels, but they do not keep the current level: you keep it.

| Prop | What it does |
|---|---|
| `rootId` | The `id` of the node drawn as the root; `null` is the root of the data |
| `onRootChange` | Receives the `id` of the node the user wants to open |
| `depth` | The levels drawn below the root; all of them, by default |

When you click a node, or press `Enter` or the space bar on it, the chart calls `onRootChange` with its `id`. You decide whether to accept it and pass it back in `rootId`. Since both charts receive the same `rootId`, they drill down together: choosing Storage in one opens Storage in both.

Owning the state allows your own rules. The chart also sends the `id` of a leaf, and opening a leaf leaves a single rectangle. That is why `drill` accepts only the nodes that are the parent of some row. With `depth={1}`, the treemap draws only one level below the root: the four areas at the very top and the services of the open area. The sunburst does not set `depth` and draws every ring.

There are two ways to go up. The "Back to top" button sets `null`. And, with the current root active, `Enter` goes up one level: it sends the `id` of its parent, or `null` when the parent is the root of the data. From Storage, the down arrow activates Storage and `Enter` goes back to the top.

## The keyboard

Hierarchy charts follow the WAI-ARIA tree pattern. With focus on the treemap:

| Key | Moves to |
|---|---|
| Down arrow and up arrow | The next or the previous node, depth first |
| Right arrow | The first child |
| Left arrow | The parent |
| Home and End | The first node and the last |
| `Enter` or space bar | Open the node |

Each node is announced with its path from the root, its value and its share of the parent. This is the route measured in the browser, from the root:

| Keystroke | Announcement |
|---|---|
| `Tab` | node Infrastructure, cost 47.3 |
| Down arrow | node Infrastructure › Compute, cost 23.3, 49.3% of Infrastructure |
| Down arrow | node Infrastructure › Storage, cost 11.2, 23.7% of Infrastructure |
| `Enter` | Opens Storage |
| Down arrow, twice | node Infrastructure › Storage › Database, cost 7.2, 64.3% of Storage |

The node tree, `TreeChart`, is explored with the same keys.

## The tree, the Sankey and the network

The other three charts on the page have no state.

* **`TreeChart`** draws the same hierarchy as nodes joined by lines, with the same accessor props (`idKey`, `parentKey`, `labelKey`, `valueKey`). It is useful when the structure matters more than the size of each part.
* **`SankeyChart`** reads links with `sourceKey`, `targetKey` and `valueKey`. The nodes come from the ends of the links and are placed in stages: the channels, the pages and the outcomes. Each node shows its total (Home 60, Exit 79), and the keyboard goes through the flows: "flow Search → Home, visits 30".
* **`NetworkChart`** reads the same three fields and places the nodes with a seeded force simulation, so the drawing is the same on every load. It names only the three nodes with the most links, here `api`, `database` and `workers`. The others are read in the tooltip and in the data table. Its `nodes` prop accepts the list of nodes with their `label`, their `group` or their position, if you do not want them to come from the links.

## The page in Vue

In Vue the event is `@root-change`, and the state, a `ref`. Replace `src/App.vue`:

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

## The page in Angular

In Angular, `rootId` receives a signal and the event is the `(rootChange)` output. Replace `src/app/app.ts`:

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

## The page in Reflex

In Reflex, the data goes in `ops_panel/infra.py`:

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

And the page, `ops_panel/ops_panel.py`:

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

The level lives in the state, `CostState.root`, and `on_root_change` is a backend event that receives the `id` or `None`. The button calls the same event with `None`, and `CostState.root.is_none()` disables it at the very top.

The four adapters were checked in the browser with the same route: drill down to Storage with the keyboard, try to open the Database leaf (nothing happens), go back up with the button and open Network with a click on the treemap.

## Common problems

* **`SP020` in the console.** The hierarchy has a repeated `id`, a `parent` that does not exist, a cycle or several roots. The warning names the row; the chart drops it and draws the rest.
* **The chart does not drill down.** The `id` is not being passed back in `rootId`. The chart does not keep the level: if `onRootChange` does not update your state, nothing changes.
* **A click leaves a single rectangle.** A leaf was opened. Filter the `id` values in your handler, as `drill` does.
* **The treemap and the sunburst do not move together.** Each one has its own state. Pass them the same variable.
* **The network names only three nodes.** That is by design: the other names are in the tooltip and in the data table.

## What comes next

With this article level 2 ends. You now have a panel with several charts, a common style, interaction and level navigation. Level 3 takes it to a complete application, and starts with article 16: the interface components for forms and display.

The [gallery](https://silverpointweb.vercel.app/gallery) shows the hierarchy, flow and network charts live alongside the rest of the catalogue.
