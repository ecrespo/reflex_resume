Title: Silverpoint, artículo 17: componentes de interfaz (II), tablas, componentes compuestos y ventanas superpuestas
Date: 2026-11-11 19:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_17
Authors: Ernesto Crespo
Summary: Una tabla de incidencias que se ordena y se pagina, un modal para reconocer una incidencia y una notificación que lo confirma, con los componentes de interfaz de silverpoint en React, Vue, Angular y Reflex.

El [artículo 16](/blog/silverpoint_serie_16) llevó al panel de operaciones los componentes de [silverpoint](https://github.com/ecrespo/silverpoint) que reciben un valor y los que muestran datos. Este sigue con los que quedan: la tabla, los componentes compuestos y las ventanas superpuestas, las que se abren encima de la página.

## Lo que vas a construir

Una tabla con las incidencias del día. Se ordena por servicio, gravedad, hora o duración, y muestra cinco filas por página. Un botón abre un modal para reconocer una incidencia abierta, y al reconocerla una notificación lo confirma.

![El modal para reconocer una incidencia sobre la tabla ordenada por duración, y la tabla con la incidencia reconocida y la notificación](./images/silverpoint-serie-17.png)

A la izquierda, el modal abierto sobre la tabla ordenada por minutos, de mayor a menor. A la derecha, la misma tabla con `INC-1038` reconocida y la notificación abajo.

## La tabla

`SpTable` dibuja una tabla nativa: `<table>`, `<caption>`, `<th scope="col">`. Cada columna es una fila con `key` y `title`, y puede llevar `align`, `sortable` y `width`. Cada celda muestra el valor de su campo como texto; no hay celdas a medida.

| Prop | Qué hace |
|---|---|
| `columns` | Las columnas, en orden |
| `data` | Las filas que se dibujan |
| `caption` | El título de la tabla, que también la nombra |
| `sortKey`, `sortOrder` | La columna ordenada y su sentido, `asc` o `desc` |
| `onSort` | Se llama con la clave de la columna cuyo encabezado se pulsa |
| `striped`, `hoverable`, `bordered` | Filas tramadas alternas, realce al pasar el puntero, bordes |
| `emptyText` | El texto sin filas; por defecto, «No data» |
| `rowKey` | El campo que identifica cada fila |

La tabla no ordena: avisa. El encabezado de una columna con `sortable` es un botón, y al pulsarlo `onSort` recibe la clave. Ordenas tú, con `uiSortRows` de `@silverpoint/core/ui` (en Reflex, `sort_rows`), y le pasas a la tabla las filas ordenadas con `sortKey` y `sortOrder` para que dibuje la flecha y ponga `aria-sort` en esa columna.

`uiSortRows` es estable, pone los números antes que el texto, compara el texto en minúsculas sin tener en cuenta el idioma y deja al final las filas sin valor. Como el orden es tuyo, también puedes ordenar en el servidor o con tu propia función.

## Los datos

Doce incidencias del día, en `src/incidents.ts`. En Vue es el mismo archivo, y en Angular va en `src/app/incidents.ts`:

```ts
export type Incident = {
  id: string;
  service: string;
  severity: string;
  opened: string;
  minutes: number;
  status: string;
};

export const INCIDENTS: Incident[] = [
  { id: 'INC-1031', service: 'API', severity: 'sev2', opened: '00:42', minutes: 18, status: 'resolved' },
  { id: 'INC-1032', service: 'Search', severity: 'sev3', opened: '02:15', minutes: 7, status: 'resolved' },
  { id: 'INC-1033', service: 'Checkout', severity: 'sev1', opened: '07:58', minutes: 46, status: 'resolved' },
  { id: 'INC-1034', service: 'API', severity: 'sev3', opened: '08:20', minutes: 5, status: 'resolved' },
  { id: 'INC-1035', service: 'Checkout', severity: 'sev2', opened: '09:47', minutes: 23, status: 'resolved' },
  { id: 'INC-1036', service: 'Search', severity: 'sev2', opened: '10:31', minutes: 31, status: 'resolved' },
  { id: 'INC-1037', service: 'API', severity: 'sev1', opened: '11:56', minutes: 12, status: 'resolved' },
  { id: 'INC-1038', service: 'Checkout', severity: 'sev2', opened: '12:09', minutes: 38, status: 'open' },
  { id: 'INC-1039', service: 'Search', severity: 'sev3', opened: '13:44', minutes: 9, status: 'open' },
  { id: 'INC-1040', service: 'API', severity: 'sev2', opened: '14:02', minutes: 16, status: 'open' },
  { id: 'INC-1041', service: 'Checkout', severity: 'sev3', opened: '15:30', minutes: 4, status: 'open' },
  { id: 'INC-1042', service: 'API', severity: 'sev1', opened: '16:18', minutes: 27, status: 'open' },
];

export const COLUMNS = [
  { key: 'id', title: 'Incident' },
  { key: 'service', title: 'Service', sortable: true },
  { key: 'severity', title: 'Severity', sortable: true },
  { key: 'opened', title: 'Opened', sortable: true },
  { key: 'minutes', title: 'Minutes', sortable: true, align: 'end' as const },
  { key: 'status', title: 'Status' },
];

export const PAGE_SIZE = 5;
```

`align: 'end' as const` mantiene el literal para que el tipo encaje con el de las columnas.

## La paginación

`SpPagination` no corta las filas: dibuja los botones de página y avisa del cambio. Le das el total (`total`) y el tamaño de página (`pageSize`, 10 por defecto), y cortas tú las filas de la página actual. Con `showTotal` escribe el rango, «6–10 of 12»; `totalTemplate` cambia ese texto.

| | Controlado | Cambio |
|---|---|---|
| React | `current` | `onChange(page)` |
| Vue | `v-model:current` | `update:current` |
| Angular | `[(current)]` | `(currentChange)` |
| Reflex | `current` | `on_change` |

## Las ventanas superpuestas

| Componente | Para qué | Cómo funciona |
|---|---|---|
| `SpModal` | Un diálogo que bloquea la página | Un `<dialog>` abierto con `showModal()` |
| `SpDrawer` | Un diálogo pegado a un lado (`side`) | Un `<dialog>`, modal salvo con `modal={false}` |
| `SpPopover` | Contenido junto a su disparador, sin bloquear | Un popover de la API Popover |
| `SpTooltip` | Un texto corto al pasar el puntero o al enfocar | Un popover manual, que no cierra los demás |
| `SpSelect` | Una opción de una lista | Un combobox de solo selección |
| `SpDropdownMenu` | Un menú de acciones | `onSelect` recibe la clave de la acción |
| `SpToast` | Un aviso que se cierra solo | Un elemento de la lista de `SpToaster` |

Todas usan la plataforma: el navegador pone la ventana encima de la página, atrapa el foco del modal y lo cierra con Escape.

### El disparador es un botón nativo

Cada ventana se abre con un `<button type="button">` nativo, que recibe su ARIA (`aria-haspopup`, `aria-expanded`, `aria-controls`) y su apertura:

| Framework | Dónde va |
|---|---|
| React | La prop `trigger`, `trigger={<button type="button">…</button>}` |
| Vue | La ranura `#trigger` |
| Angular | Un `<button type="button" spTrigger>` proyectado; `SpTrigger` se importa del subpath de la ventana |
| Reflex | `trigger=rx.el.button(…, type="button")` |

En React no pases un `SpButton` como disparador: descarta el ARIA que recibe.

### El estado abierto

| | Controlado | No controlado | Cambio |
|---|---|---|---|
| React | `open` | `defaultOpen` | `onOpenChange(open)` |
| Vue | `v-model:open` | `default-open` | `update:open` |
| Angular | `[(open)]` | `[defaultOpen]` | `(openChange)` |
| Reflex | `open` | `default_open` | `on_open_change` |

`onOpenChange` también se llama cuando la plataforma cierra la ventana: con Escape o con un clic fuera. Un modal con `dismissible={false}` ignora los dos.

### Las notificaciones

Se pone un `SpToaster` cerca de la raíz y, dentro, un `SpToast` por aviso. Un aviso se cierra a los 5000 ms, la `duration` del contenedor, salvo que tenga la suya. Mientras tiene el puntero o el foco, la cuenta se para, y F8 lleva el foco al contenedor.

## La tabla de incidencias en React

```tsx
import { useState } from 'react';
import { uiSortRows } from '@silverpoint/core/ui';
import { SpButton } from '@silverpoint/react/ui/button';
import { SpModal } from '@silverpoint/react/ui/modal';
import { SpPagination } from '@silverpoint/react/ui/pagination';
import { SpSelect } from '@silverpoint/react/ui/select';
import { SpTable } from '@silverpoint/react/ui/table';
import { SpToast, SpToaster } from '@silverpoint/react/ui/toast';
import { COLUMNS, INCIDENTS, PAGE_SIZE } from './incidents';

export function Incidents() {
  const [rows, setRows] = useState(INCIDENTS);
  const [sortKey, setSortKey] = useState('opened');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [page, setPage] = useState(1);
  const [open, setOpen] = useState(false);
  const [picked, setPicked] = useState<string | null>(null);
  const [acknowledged, setAcknowledged] = useState('');
  const [toastOpen, setToastOpen] = useState(false);

  const visible = uiSortRows(rows, sortKey, sortOrder).slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const openIds = rows.filter((row) => row.status === 'open').map((row) => row.id);

  function sort(key: string) {
    setSortOrder(key === sortKey && sortOrder === 'asc' ? 'desc' : 'asc');
    setSortKey(key);
    setPage(1);
  }

  function acknowledge() {
    setRows(rows.map((row) => (row.id === picked ? { ...row, status: 'acknowledged' } : row)));
    setAcknowledged(picked ?? '');
    setPicked(null);
    setOpen(false);
    setToastOpen(true);
  }

  return (
    <section>
      <SpTable
        caption="Incidents today"
        columns={COLUMNS}
        data={visible}
        rowKey="id"
        sortKey={sortKey}
        sortOrder={sortOrder}
        onSort={sort}
        striped
      />
      <SpPagination total={rows.length} pageSize={PAGE_SIZE} current={page} onChange={setPage} showTotal />
      <SpModal
        title="Acknowledge an incident"
        description="The on-call team stops being paged for it."
        trigger={<button type="button">Acknowledge an incident</button>}
        open={open}
        onOpenChange={setOpen}
        footer={
          <SpButton variant="primary" disabled={!picked} onClick={acknowledge}>
            Acknowledge
          </SpButton>
        }
      >
        <SpSelect
          label="Incident"
          placeholder="Choose an open incident"
          items={openIds}
          value={picked}
          onChange={setPicked}
        />
      </SpModal>
      <SpToaster>
        <SpToast
          kind="success"
          title="Incident acknowledged"
          description={`${acknowledged} no longer pages the on-call team.`}
          open={toastOpen}
          onOpenChange={setToastOpen}
        />
      </SpToaster>
    </section>
  );
}
```

El orden empieza por la hora de apertura, de la más reciente a la más antigua. Pulsar una columna la ordena de menor a mayor, y pulsarla otra vez, al revés; cada cambio vuelve a la primera página. `setPage`, `setOpen`, `setPicked` y `setToastOpen` se pasan tal cual, porque los manejadores reciben el valor.

El botón `Acknowledge` está deshabilitado hasta que se elige una incidencia. Al reconocerla, la fila pasa a `acknowledged`, el modal se cierra y la notificación se abre.

En `src/index.css`, dos reglas para la tabla y el disparador:

```css
.sp-ui-table td:not([data-align]) {
  text-align: start;
}

button[aria-haspopup='dialog'] {
  padding: 6px 14px;
  border: 1px solid #3b3a36;
  border-radius: 2px;
  background: transparent;
  font: inherit;
  cursor: pointer;
}
```

La primera es un arreglo: en 0.9.2, la regla `.sp-table td` de `styles.css`, la de las tablas de datos de los gráficos, alinea a la derecha las celdas de `SpTable`. La segunda dibuja el disparador, que es un botón nativo y sale sin estilo.

## La tabla de incidencias en Vue

```vue
<script setup lang="ts">
import { computed, ref } from 'vue';
import { uiSortRows } from '@silverpoint/core/ui';
import { SpButton } from '@silverpoint/vue/ui/button';
import { SpModal } from '@silverpoint/vue/ui/modal';
import { SpPagination } from '@silverpoint/vue/ui/pagination';
import { SpSelect } from '@silverpoint/vue/ui/select';
import { SpTable } from '@silverpoint/vue/ui/table';
import { SpToast, SpToaster } from '@silverpoint/vue/ui/toast';
import { COLUMNS, INCIDENTS, PAGE_SIZE } from '../incidents';

const rows = ref(INCIDENTS);
const sortKey = ref('opened');
const sortOrder = ref<'asc' | 'desc'>('desc');
const page = ref(1);
const open = ref(false);
const picked = ref<string | null>(null);
const acknowledged = ref('');
const toastOpen = ref(false);

const visible = computed(() =>
  uiSortRows(rows.value, sortKey.value, sortOrder.value).slice((page.value - 1) * PAGE_SIZE, page.value * PAGE_SIZE),
);
const openIds = computed(() => rows.value.filter((row) => row.status === 'open').map((row) => row.id));

function sort(key: string) {
  sortOrder.value = key === sortKey.value && sortOrder.value === 'asc' ? 'desc' : 'asc';
  sortKey.value = key;
  page.value = 1;
}

function acknowledge() {
  rows.value = rows.value.map((row) => (row.id === picked.value ? { ...row, status: 'acknowledged' } : row));
  acknowledged.value = picked.value ?? '';
  picked.value = null;
  open.value = false;
  toastOpen.value = true;
}
</script>

<template>
  <section>
    <SpTable
      caption="Incidents today"
      :columns="COLUMNS"
      :data="visible"
      row-key="id"
      :sort-key="sortKey"
      :sort-order="sortOrder"
      striped
      @sort="sort"
    />
    <SpPagination v-model:current="page" :total="rows.length" :page-size="PAGE_SIZE" show-total />
    <SpModal
      v-model:open="open"
      title="Acknowledge an incident"
      description="The on-call team stops being paged for it."
    >
      <template #trigger><button type="button">Acknowledge an incident</button></template>
      <SpSelect v-model="picked" label="Incident" placeholder="Choose an open incident" :items="openIds" />
      <template #footer>
        <SpButton variant="primary" :disabled="!picked" @click="acknowledge">Acknowledge</SpButton>
      </template>
    </SpModal>
    <SpToaster>
      <SpToast
        v-model:open="toastOpen"
        kind="success"
        title="Incident acknowledged"
        :description="`${acknowledged} no longer pages the on-call team.`"
      />
    </SpToaster>
  </section>
</template>
```

`v-model:current`, `v-model:open` y `v-model` hacen el trabajo de los pares de React. El encabezado emite `sort`, y el disparador y el pie van en las ranuras `#trigger` y `#footer`.

## La tabla de incidencias en Angular

```ts
import { Component, computed, signal } from '@angular/core';
import { uiSortRows } from '@silverpoint/core/ui';
import { SpButton } from '@silverpoint/angular/ui/button';
import { SpCardFooter, SpModal, SpTrigger } from '@silverpoint/angular/ui/modal';
import { SpPagination } from '@silverpoint/angular/ui/pagination';
import { SpSelect } from '@silverpoint/angular/ui/select';
import { SpTable } from '@silverpoint/angular/ui/table';
import { SpToast, SpToaster } from '@silverpoint/angular/ui/toast';
import { COLUMNS, INCIDENTS, PAGE_SIZE } from './incidents';

@Component({
  selector: 'app-incidents-table',
  imports: [SpButton, SpCardFooter, SpModal, SpPagination, SpSelect, SpTable, SpToast, SpToaster, SpTrigger],
  template: `
    <section>
      <sp-table
        caption="Incidents today"
        [columns]="columns"
        [data]="visible()"
        rowKey="id"
        [sortKey]="sortKey()"
        [sortOrder]="sortOrder()"
        striped
        (sort)="sort($event)"
      />
      <sp-pagination [(current)]="page" [total]="rows().length" [pageSize]="pageSize" showTotal />
      <sp-modal
        [(open)]="open"
        title="Acknowledge an incident"
        description="The on-call team stops being paged for it."
      >
        <button type="button" spTrigger>Acknowledge an incident</button>
        <sp-select [(value)]="picked" label="Incident" placeholder="Choose an open incident" [items]="openIds()" />
        <ng-template spFooter>
          <button type="button" spButton variant="primary" [disabled]="!picked()" (click)="acknowledge()">
            Acknowledge
          </button>
        </ng-template>
      </sp-modal>
      <sp-toaster>
        <sp-toast
          [(open)]="toastOpen"
          kind="success"
          title="Incident acknowledged"
          [description]="acknowledged() + ' no longer pages the on-call team.'"
        />
      </sp-toaster>
    </section>
  `,
})
export class IncidentsTable {
  protected readonly columns = COLUMNS;
  protected readonly pageSize = PAGE_SIZE;
  protected readonly rows = signal(INCIDENTS);
  protected readonly sortKey = signal('opened');
  protected readonly sortOrder = signal<'asc' | 'desc'>('desc');
  protected readonly page = signal(1);
  protected readonly open = signal(false);
  protected readonly picked = signal<string | null>(null);
  protected readonly acknowledged = signal('');
  protected readonly toastOpen = signal(false);

  protected readonly visible = computed(() =>
    uiSortRows(this.rows(), this.sortKey(), this.sortOrder()).slice(
      (this.page() - 1) * PAGE_SIZE,
      this.page() * PAGE_SIZE,
    ),
  );
  protected readonly openIds = computed(() => this.rows().filter((row) => row.status === 'open').map((row) => row.id));

  protected sort(key: string) {
    this.sortOrder.set(key === this.sortKey() && this.sortOrder() === 'asc' ? 'desc' : 'asc');
    this.sortKey.set(key);
    this.page.set(1);
  }

  protected acknowledge() {
    const picked = this.picked();
    this.rows.update((rows) => rows.map((row) => (row.id === picked ? { ...row, status: 'acknowledged' } : row)));
    this.acknowledged.set(picked ?? '');
    this.picked.set(null);
    this.open.set(false);
    this.toastOpen.set(true);
  }
}
```

`[(current)]`, `[(open)]` y `[(value)]` se unen a signals. El pie del modal es un `<ng-template spFooter>`, y su botón es la directiva `spButton` sobre un `<button>` nativo, como en el artículo 16. Las reglas de `src/styles.css` son las de React.

## La tabla de incidencias en Reflex

En Reflex el orden, la página y las ventanas abiertas viven en el estado. `visible` es una variable calculada que ordena con `sort_rows` y corta la página:

```python
class IncidentsState(rx.State):
    rows: list[dict] = INCIDENTS
    sort_key: str = "opened"
    sort_order: str = "desc"
    page: int = 1
    open: bool = False
    picked: str | None = None
    acknowledged: str = ""
    toast_open: bool = False

    @rx.var
    def visible(self) -> list[dict]:
        start = (self.page - 1) * PAGE_SIZE
        return sort_rows(self.rows, self.sort_key, self.sort_order)[
            start : start + PAGE_SIZE
        ]

    @rx.var
    def open_ids(self) -> list[str]:
        return [row["id"] for row in self.rows if row["status"] == "open"]

    @rx.event
    def sort(self, key: str):
        self.sort_order = (
            "desc" if key == self.sort_key and self.sort_order == "asc" else "asc"
        )
        self.sort_key = key
        self.page = 1

    @rx.event
    def set_page(self, page: int):
        self.page = page

    @rx.event
    def set_open(self, open: bool):
        self.open = open

    @rx.event
    def set_picked(self, key: str):
        self.picked = key

    @rx.event
    def set_toast_open(self, open: bool):
        self.toast_open = open

    @rx.event
    def acknowledge(self):
        self.rows = [
            {**row, "status": "acknowledged"} if row["id"] == self.picked else row
            for row in self.rows
        ]
        self.acknowledged = self.picked or ""
        self.picked = None
        self.open = False
        self.toast_open = True


def incidents_table() -> rx.Component:
    return rx.el.section(
        sp_table(
            COLUMNS,
            IncidentsState.visible,
            caption="Incidents today",
            row_key="id",
            sort_key=IncidentsState.sort_key,
            sort_order=IncidentsState.sort_order,
            on_sort=IncidentsState.sort,
            striped=True,
        ),
        sp_pagination(
            total=IncidentsState.rows.length(),
            page_size=PAGE_SIZE,
            current=IncidentsState.page,
            on_change=IncidentsState.set_page,
            show_total=True,
        ),
        sp_modal(
            sp_select(
                IncidentsState.open_ids,
                label="Incident",
                placeholder="Choose an open incident",
                value=IncidentsState.picked,
                on_change=IncidentsState.set_picked,
            ),
            trigger=rx.el.button("Acknowledge an incident", type="button"),
            title="Acknowledge an incident",
            description="The on-call team stops being paged for it.",
            footer=sp_button(
                "Acknowledge",
                variant="primary",
                disabled=IncidentsState.picked.is_none(),
                on_click=IncidentsState.acknowledge,
            ),
            open=IncidentsState.open,
            on_open_change=IncidentsState.set_open,
        ),
        sp_toaster(
            sp_toast(
                "Incident acknowledged",
                IncidentsState.acknowledged + " no longer pages the on-call team.",
                kind="success",
                open=IncidentsState.toast_open,
                on_open_change=IncidentsState.set_toast_open,
            ),
        ),
        style={
            "display": "grid",
            "gap": "16px",
            "justify_items": "start",
            "max_width": "720px",
        },
    )


def index() -> rx.Component:
    return rx.el.main(incidents_table(), style={"padding": "32px"})


app = rx.App(
    style={
        "background": "#f4f1ea",
        ".sp-table": {"justify_self": "stretch"},
        ".sp-ui-table td:not([data-align])": {"text_align": "start"},
        "button[aria-haspopup='dialog']": {
            "padding": "6px 14px",
            "border": "1px solid #3b3a36",
            "border_radius": "2px",
            "background": "transparent",
            "font": "inherit",
            "cursor": "pointer",
        },
    }
)
app.add_page(index)
```

Las filas se definen como tuplas y se convierten en diccionarios con `FIELDS`. `sort_rows` ordena igual que `uiSortRows`, así que la tabla se ve igual que en los otros tres frameworks.

El disparador es un `rx.el.button`. La documentación permite pasar un texto, `trigger="Acknowledge an incident"`, que se convierte en un botón dibujado con `sp_trigger`; en la prueba, con Reflex 0.10.1 y `reflex-silverpoint-react` 0.9.1, la página falló con `SilverpointTrigger is not defined`, igual que con `sp_trigger` explícito.

## El teclado

* Los encabezados ordenables son botones: se alcanzan con Tab y se pulsan con Enter o con la barra espaciadora.
* Al abrir el modal, el foco entra en él, en el botón de cerrar, y no sale con Tab mientras está abierto.
* Escape cierra el modal y el foco vuelve al disparador. En la prueba, en los cuatro frameworks, el foco volvió a `Acknowledge an incident`.
* `SpSelect` sigue el patrón de combobox de solo selección de la APG: se abre con la flecha abajo o la barra espaciadora, se recorre con las flechas y se elige con Enter. Con la lista abierta, Escape cierra la lista y deja el modal abierto.

## Los componentes compuestos

| Componente | Muestra |
|---|---|
| `SpDescriptions` | Pares de etiqueta y valor, en `columns` columnas (3 por defecto) |
| `SpCollapse` | Paneles que se abren y se cierran (`SpCollapseItem`); con `accordion`, uno a la vez |
| `SpEmpty` | El estado vacío de una lista o de una tabla |
| `SpResult` | El resultado de una acción: éxito, error, información o advertencia |
| `SpBreadcrumb` | Las páginas hasta la actual |
| `SpAvatar` | Una foto o unas iniciales; `SpAvatarGroup` apila varias |
| `SpTimelineList` | Sucesos en orden, cada uno hecho, actual, pendiente o con error |

Con ellos se completa el detalle de una incidencia: `SpDescriptions` para sus campos, `SpTimelineList` para lo que pasó y `SpEmpty` cuando no hay ninguna abierta.

## Problemas comunes

* **La tabla no se ordena al pulsar el encabezado.** Es lo esperado: ordena tú en `onSort` y pásale `sortKey` y `sortOrder`.
* **Las celdas salen alineadas a la derecha.** Es la regla `.sp-table td` de `styles.css` en 0.9.2. Añade `.sp-ui-table td:not([data-align]) { text-align: start; }`.
* **En Reflex, `SilverpointTrigger is not defined`.** El disparador es un texto o un `sp_trigger`. Usa `rx.el.button`.
* **El rótulo del select no se ve.** `label` es el nombre accesible y no se dibuja, como en `SpTextarea`.

## Lo que viene

El panel ya tiene sus tablas y sus ventanas. El [artículo 18](/blog/silverpoint_serie_18) vuelve a los gráficos: exportar uno a SVG para usarlo fuera de la aplicación.

La [guía de componentes](https://silverpointweb.vercel.app/docs/ui) de la documentación tiene la referencia de cada uno.
