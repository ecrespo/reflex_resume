Title: Silverpoint, artículo 11: interacción, elemento activo, selección y descripción emergente a medida
Date: 2026-11-11 16:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_11
Authors: Ernesto Crespo
Summary: Los eventos de los gráficos de silverpoint en React, Vue, Angular y Reflex: el elemento activo para una lectura junto al gráfico, la selección para una lista de horas y una descripción emergente propia.

Todos los gráficos de [silverpoint](https://github.com/ecrespo/silverpoint) responden al puntero y al teclado: marcan el elemento activo, muestran una lectura emergente y anuncian su valor. El [artículo 10](/blog/silverpoint_serie_10) recorrió esa parte desde la accesibilidad. Este artículo de la serie la lleva a tu código, con dos eventos y una prop que comparten los 60 gráficos.

## Lo que vas a construir

El gráfico de visitas por hora del panel de operaciones con tres añadidos: una línea de texto bajo el gráfico que dice la hora activa y sus visitas, una lista de horas seleccionadas con clic o con el teclado, y una descripción emergente propia en lugar de la que trae el gráfico.

![El gráfico de visitas con la descripción emergente propia sobre las 14:00, la lectura de esa hora y dos horas seleccionadas debajo](./images/silverpoint-serie-11.png)

## Lo que necesitas

El proyecto de tu framework de los artículos 03 a 06, con las visitas por hora de su paso de datos propios: `src/traffic.ts` en React y Vue, `src/app/traffic.ts` en Angular y `ops_panel/traffic.py` en Reflex. Primero se construye en React, paso a paso; después, la versión completa en Vue, Angular y Reflex.

## Los dos eventos

| React | Vue | Angular | Reflex | Cuándo |
|---|---|---|---|---|
| `onActiveChange` | `@active-change` | `(activeChange)` | `on_active_change` | El elemento activo cambia, con el puntero o con el teclado |
| `onSelect` | `@select` | `(select)` | `on_select` | Un clic, `Enter` o espacio sobre un elemento |

Los dos reciben el mismo objeto, un `ActiveItem`. Al pasar por la hora 01 del gráfico de visitas, llega esto:

```json
{"seriesKey":"hits","index":1,"datum":{"hour":"01","hits":14},"value":14,"point":{"x":59.25,"y":193.55}}
```

| Campo | Qué es |
|---|---|
| `seriesKey` | La serie del elemento: el campo que lee `valueKey` |
| `index` | La posición de la fila en `data` |
| `datum` | La fila completa, tal como la pasaste |
| `value` | El valor dibujado |
| `point` | La posición del elemento en las coordenadas del SVG, no de la pantalla |

`onActiveChange` recibe `null` cuando no hay elemento activo: al sacar el puntero del gráfico, al pulsar `Escape` o cuando el gráfico pierde el foco. En los gráficos que calculan lo que dibujan, como el histograma, `datum` no es una fila tuya sino un resumen: el intervalo y su recuento, por ejemplo. El artículo 14 los recorre.

## 1. Una lectura junto al gráfico

Sustituye `src/App.tsx`:

```tsx
import { useState } from 'react';
import type { ActiveItem } from '@silverpoint/core';
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from './traffic';

export default function App() {
  const [active, setActive] = useState<ActiveItem | null>(null);

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        id="hits"
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        height={200}
        onActiveChange={setActive}
      />
      <p>
        {active
          ? `${active.datum.hour}:00, ${active.value} thousand hits`
          : 'Point at an hour, or focus the chart and use the arrow keys.'}
      </p>
    </main>
  );
}
```

El estado guarda el último elemento activo y el párrafo lo escribe. Pasa el puntero por la línea, o llega al gráfico con `Tab` y recórrelo con las flechas: el párrafo cambia igual en los dos casos. Al llegar con `Tab`, el gráfico activa el primer elemento.

`ActiveItem` es un tipo del motor, `@silverpoint/core`, que se instala con el adaptador. La importación es solo de tipo y no añade nada al paquete. Si usas pnpm, declara `@silverpoint/core` en tu `package.json`, como explicaba el artículo 02.

## 2. Una selección y una descripción emergente propia

Sustituye `src/App.tsx` por la versión completa:

```tsx
import { useState } from 'react';
import type { ActiveItem } from '@silverpoint/core';
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from './traffic';

export default function App() {
  const [active, setActive] = useState<ActiveItem | null>(null);
  const [picked, setPicked] = useState<string[]>([]);

  const toggle = (item: ActiveItem) => {
    const hour = String(item.datum.hour);
    setPicked((hours) => (hours.includes(hour) ? hours.filter((h) => h !== hour) : [...hours, hour]));
  };

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        id="hits"
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        height={200}
        onActiveChange={setActive}
        onSelect={toggle}
        tooltip={(item) => (
          <span>
            {String(item.datum.hour)}:00 · {item.value}k hits
          </span>
        )}
      />
      <p>
        {active
          ? `${active.datum.hour}:00, ${active.value} thousand hits`
          : 'Point at an hour, or focus the chart and use the arrow keys.'}
      </p>
      <p>Picked hours: {picked.length > 0 ? picked.join(', ') : 'none'}</p>
    </main>
  );
}
```

* **`onSelect` alterna la hora en la lista.** Un clic, `Enter` o espacio sobre una hora la añade; otro la quita. El gráfico no guarda ni dibuja la selección: es estado de tu aplicación, y decides tú qué hacer con ella.
* **`tooltip` sustituye la lectura emergente.** Es una función que recibe el elemento activo y devuelve lo que se pinta dentro del recuadro. La posición, el marcador y el recuadro siguen siendo los del gráfico. La función recibe un segundo argumento con la lectura que habría escrito el gráfico (`heading` y `text`), por si quieres partir de ella.

La descripción emergente propia solo cambia lo que se ve. Está marcada con `aria-hidden`, y lo que anuncia el lector de pantalla sigue siendo el texto del gráfico, «hour 14, hits 59», calculado igual que la tabla de datos.

## En Vue

Sustituye `src/App.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpLineChart, type ActiveItem } from '@silverpoint/vue/line-chart';
import { traffic } from './traffic';

const active = ref<ActiveItem | null>(null);
const picked = ref<string[]>([]);

function toggle(item: ActiveItem) {
  const hour = String(item.datum.hour);
  picked.value = picked.value.includes(hour)
    ? picked.value.filter((h) => h !== hour)
    : [...picked.value, hour];
}
</script>

<template>
  <main style="max-width: 640px">
    <SpLineChart
      id="hits"
      :data="traffic"
      x-key="hour"
      value-key="hits"
      title="Hits per hour"
      :height="200"
      @active-change="active = $event"
      @select="toggle"
    >
      <template #tooltip="{ active: item }">
        <span>{{ item.datum.hour }}:00 · {{ item.value }}k hits</span>
      </template>
    </SpLineChart>
    <p v-if="active">{{ active.datum.hour }}:00, {{ active.value }} thousand hits</p>
    <p v-else>Point at an hour, or focus the chart and use the arrow keys.</p>
    <p>Picked hours: {{ picked.length > 0 ? picked.join(', ') : 'none' }}</p>
  </main>
</template>
```

Los eventos se escuchan con `@active-change` y `@select`, y `$event` es el `ActiveItem`, o `null` cuando no hay elemento activo. La descripción emergente es una ranura con nombre, `#tooltip`, que recibe `active` y `readout`. Aquí `active` se renombra a `item` para no confundirlo con la variable del componente. En Vue, el tipo `ActiveItem` se importa de la misma entrada que el gráfico.

## En Angular

Sustituye `src/app/app.ts`:

```ts
import { Component, signal } from '@angular/core';
import { SpTooltip } from '@silverpoint/angular';
import { SpLineChart, type ActiveItem } from '@silverpoint/angular/line-chart';
import { traffic } from './traffic';

@Component({
  selector: 'app-root',
  imports: [SpLineChart, SpTooltip],
  template: `
    <main style="max-width: 640px">
      <sp-line-chart
        id="hits"
        [data]="traffic"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        [height]="200"
        (activeChange)="active.set($event)"
        (select)="toggle($event)"
      >
        <ng-template spTooltip let-item>
          <span>{{ item.datum['hour'] }}:00 · {{ item.value }}k hits</span>
        </ng-template>
      </sp-line-chart>
      @if (active(); as item) {
        <p>{{ item.datum['hour'] }}:00, {{ item.value }} thousand hits</p>
      } @else {
        <p>Point at an hour, or focus the chart and use the arrow keys.</p>
      }
      <p>Picked hours: {{ picked().length > 0 ? picked().join(', ') : 'none' }}</p>
    </main>
  `,
})
export class App {
  protected readonly traffic = traffic;
  protected readonly active = signal<ActiveItem | null>(null);
  protected readonly picked = signal<string[]>([]);

  protected toggle(item: ActiveItem) {
    const hour = String(item.datum['hour']);
    this.picked.update((hours) =>
      hours.includes(hour) ? hours.filter((h) => h !== hour) : [...hours, hour],
    );
  }
}
```

Los eventos son salidas, `(activeChange)` y `(select)`. La descripción emergente es una plantilla marcada con la directiva `spTooltip`, que se importa de `@silverpoint/angular`; `let-item` recibe el elemento activo.

Fíjate en `item.datum['hour']`. El proyecto que crea el Angular CLI activa `noPropertyAccessFromIndexSignature` en `tsconfig.json`, y `datum` es un registro con claves de texto, así que sus campos se leen con corchetes. Con `item.datum.hour`, la compilación falla con «Property 'hour' comes from an index signature, so it must be accessed with ['hour']».

## En Reflex

Sustituye `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import line_chart, tooltip_template

from .traffic import TRAFFIC


class InteractionState(rx.State):
    active: str = ""
    picked: list[str] = []

    @rx.event
    def show(self, item: dict | None):
        if item is None:
            self.active = ""
        else:
            self.active = f"{item['datum']['hour']}:00, {item['value']} thousand hits"

    @rx.event
    def toggle(self, item: dict):
        hour = str(item["datum"]["hour"])
        if hour in self.picked:
            self.picked = [h for h in self.picked if h != hour]
        else:
            self.picked = [*self.picked, hour]

    @rx.var
    def picked_text(self) -> str:
        return ", ".join(self.picked) if self.picked else "none"


def index() -> rx.Component:
    return rx.box(
        line_chart(
            id="hits",
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            height=200,
            on_active_change=InteractionState.show,
            on_select=InteractionState.toggle,
            tooltip=tooltip_template("{datum.hour}:00 · {value}k hits"),
        ),
        rx.text(
            rx.cond(
                InteractionState.active,
                InteractionState.active,
                "Point at an hour, or focus the chart and use the arrow keys.",
            )
        ),
        rx.text("Picked hours: ", InteractionState.picked_text),
        max_width="640px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

En Reflex, los manejadores reciben el `ActiveItem` como un diccionario: `item["datum"]["hour"]` lee el campo de la fila. `show` recibe `None` cuando no hay elemento activo, por eso su argumento es `dict | None`.

La descripción emergente se construye con `tooltip_template`, a partir de un texto con marcadores:

| Marcador | Qué escribe |
|---|---|
| `{datum.<field>}` | Un campo de la fila activa, como `{datum.hour}` |
| `{value}` | El valor dibujado |
| `{index}` y `{series}` | La posición de la fila y la serie |
| `{heading}` y `{text}` | Las dos líneas de la lectura del gráfico |
| `{announcement}` | La frase que se anuncia |

Hay una diferencia con los otros tres frameworks. `tooltip_template` se convierte en una función de JavaScript y se ejecuta en el navegador, pero `on_active_change` y `on_select` son eventos del backend: cada cambio del elemento activo viaja por el WebSocket de Reflex y vuelve con el estado nuevo. Para una lectura junto al gráfico va bien. Si solo necesitas cambiar el texto del recuadro, usa `tooltip_template` y no `on_active_change`.

## Problemas comunes

* **El párrafo no cambia al usar el teclado.** El gráfico no tiene el foco. Llega a él con `Tab` antes de usar las flechas.
* **La descripción emergente propia no aparece en Vue.** La ranura se llama `tooltip` y va dentro del componente del gráfico: `<template #tooltip="{ active }">`.
* **La plantilla de Angular se ignora.** Falta `SpTooltip` en `imports`, o la plantilla no lleva el atributo `spTooltip`.
* **En TypeScript, `active.datum.hour` no es un texto.** `datum` es un registro con valores de tipo `unknown`. Conviértelo con `String(...)` antes de mostrarlo en JSX o de compararlo.

## Lo que viene

El artículo 12 cambia los colores: las seis paletas incluidas, una paleta propia comprobada y un selector de tema para todo el panel.
