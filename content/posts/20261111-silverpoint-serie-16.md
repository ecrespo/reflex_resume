Title: Silverpoint, artículo 16: componentes de interfaz (I), formularios y visualización
Date: 2026-11-11 18:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_16
Authors: Ernesto Crespo
Summary: Los componentes de interfaz de silverpoint para formularios y para mostrar datos: un formulario de reglas de alerta y una tarjeta de estado del servicio, con el valor controlado en React, v-model en Vue, formularios reactivos en Angular y estado en Reflex.

Con este artículo empieza el nivel 3 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint): llevar el panel de operaciones a una aplicación. Una aplicación no solo muestra gráficos; también pide datos y avisa de lo que pasa. Para eso silverpoint trae 38 componentes de interfaz dibujados en el mismo estilo que los gráficos.

Este artículo cubre los que reciben un valor (campos, interruptores, deslizadores) y los que solo muestran algo (tarjetas, cifras, etiquetas, avisos). El [artículo 17](/blog/silverpoint_serie_17) sigue con las tablas, los componentes compuestos y las ventanas superpuestas.

## Lo que vas a construir

Dos piezas para el panel: un formulario para configurar una regla de alerta y una tarjeta con el estado del servicio.

![El formulario de la regla de alerta y la tarjeta de estado del servicio](./images/silverpoint-serie-16.png)

El formulario elige la métrica, el umbral, el canal de aviso y si la regla está activa, y guarda unas notas. Al enviarlo, una línea de estado resume la regla. La tarjeta muestra los errores del día, el presupuesto de errores consumido, los servicios afectados y un aviso.

## La hoja de estilos de los componentes

Los componentes necesitan una tercera hoja de estilos, `@silverpoint/grounds/ui.css`, después de `styles.css`. En React, en `src/main.tsx`:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import './index.css';
```

En Vue, igual en `src/main.ts`:

```ts
import { createApp } from 'vue';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import '@silverpoint/grounds/ui.css';
import './style.css';
```

En Angular, en `src/styles.css`:

```css
@import '@silverpoint/fonts/fonts.css';
@import '@silverpoint/grounds/styles.css';
@import '@silverpoint/grounds/ui.css';
```

En Reflex no hay nada que importar: cada componente carga las hojas que necesita.

Sin `ui.css`, los componentes salen sin estilo: se ven los controles nativos del navegador y los glifos se dibujan como figuras negras enormes.

## Los componentes que reciben un valor

| Componente | Para qué | Su valor |
|---|---|---|
| `SpInput` | Una línea de texto | Un texto |
| `SpTextarea` | Varias líneas, con contador | Un texto |
| `SpInputNumber` | Un número con botones y límites | Un número |
| `SpCheckbox` | Sí o no, con estado indeterminado | Un booleano |
| `SpSwitch` | Encendido o apagado | Un booleano |
| `SpRadioGroup` | Una opción entre pocas | La clave de la opción |
| `SpSegmented` | Una opción entre pocas, en segmentos unidos | La clave de la opción |
| `SpTabs` | Pestañas con su panel | La clave de la pestaña |
| `SpSlider` | Un valor en un rango | Un número |
| `SpRate` | Una valoración de 1 a 5, con rombos | Un número |

Debajo de cada uno hay un control nativo: un `<input type="range">` en el deslizador, radios nativos en el grupo y en los segmentos, una casilla con `role="switch"` en el interruptor. Por eso funcionan con el teclado como cualquier control del navegador, y por eso un `<form>` normal los envía: cada uno se envía con su `name`.

El valor se puede llevar de dos formas, como los campos de React:

| | Controlado | No controlado | Cambio |
|---|---|---|---|
| React | `value` (`checked` en la casilla y el interruptor) | `defaultValue` (`defaultChecked`) | `onChange(value)`: el valor, no el evento |
| Vue | `v-model` | sin `v-model`, con `default-value` | `update:modelValue` |
| Angular | `[(value)]`, `formControlName` o `ngModel` | `defaultValue` | `(valueChange)` |
| Reflex | `value` (`checked`) y `on_change` | `default_value` (`default_checked`) | `on_change` recibe el valor |

Los eventos de valor solo se disparan cuando el usuario cambia el control. Si cambias el valor desde tu código, no se llama a `onChange`, así que no hay bucles. Un componente o una opción deshabilitados tampoco los disparan.

## El formulario en React

La regla tiene cuatro valores controlados y uno no controlado. Las notas solo hacen falta al enviar, así que se leen del formulario con `FormData`, por su `name`:

```tsx
import { useState, type FormEvent } from 'react';
import { SpButton } from '@silverpoint/react/ui/button';
import { SpRadioGroup } from '@silverpoint/react/ui/radio-group';
import { SpSegmented } from '@silverpoint/react/ui/segmented';
import { SpSlider } from '@silverpoint/react/ui/slider';
import { SpSwitch } from '@silverpoint/react/ui/switch';
import { SpTextarea } from '@silverpoint/react/ui/textarea';

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
  const [metric, setMetric] = useState('errors');
  const [threshold, setThreshold] = useState(10);
  const [channel, setChannel] = useState('email');
  const [active, setActive] = useState(true);
  const [saved, setSaved] = useState('');

  function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const notes = new FormData(event.currentTarget).get('notes');
    setSaved(`${metric} ≥ ${threshold}, by ${channel}, ${active ? 'active' : 'paused'}. Notes: ${notes || '—'}`);
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
        defaultValue=""
      />
      <SpButton type="submit" variant="primary">
        Save rule
      </SpButton>
      <p role="status">{saved}</p>
    </form>
  );
}
```

Las opciones de `SpSegmented` y `SpRadioGroup` son filas con `key` y `label`, y una opción puede ir deshabilitada: el canal `SMS` se ve, pero no se puede elegir ni se envía. Los manejadores reciben el valor directamente, así que `setMetric` o `setThreshold` se pasan tal cual.

En `src/index.css`, unas reglas para que los campos queden en columna:

```css
form {
  display: grid;
  gap: 20px;
  align-content: start;
}
```

## El formulario en Vue

`v-model` en cada componente controlado, y `default-value` en las notas:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { SpButton } from '@silverpoint/vue/ui/button';
import { SpRadioGroup } from '@silverpoint/vue/ui/radio-group';
import { SpSegmented } from '@silverpoint/vue/ui/segmented';
import { SpSlider } from '@silverpoint/vue/ui/slider';
import { SpSwitch } from '@silverpoint/vue/ui/switch';
import { SpTextarea } from '@silverpoint/vue/ui/textarea';

const METRICS = [
  { key: 'errors', label: 'Errors' },
  { key: 'hits', label: 'Hits' },
];

const CHANNELS = [
  { key: 'email', label: 'Email' },
  { key: 'chat', label: 'Chat' },
  { key: 'sms', label: 'SMS', disabled: true },
];

const metric = ref('errors');
const threshold = ref(10);
const channel = ref('email');
const active = ref(true);
const saved = ref('');

function save(event: Event) {
  const notes = new FormData(event.currentTarget as HTMLFormElement).get('notes');
  saved.value = `${metric.value} ≥ ${threshold.value}, by ${channel.value}, ${active.value ? 'active' : 'paused'}. Notes: ${notes || '—'}`;
}
</script>

<template>
  <form @submit.prevent="save">
    <SpSegmented label="Metric" name="metric" :items="METRICS" v-model="metric" />
    <SpSlider
      label="Threshold"
      name="threshold"
      :min="0"
      :max="50"
      :step="5"
      :marks="[0, 25, 50]"
      v-model="threshold"
    />
    <SpRadioGroup
      label="Notify by"
      name="channel"
      :items="CHANNELS"
      orientation="horizontal"
      v-model="channel"
    />
    <SpSwitch label="Active" name="active" v-model="active" />
    <SpTextarea
      label="Notes"
      placeholder="Notes for the on-call team"
      name="notes"
      :rows="2"
      :max-length="200"
      show-count
      default-value=""
    />
    <SpButton type="submit" variant="primary">Save rule</SpButton>
    <p role="status">{{ saved }}</p>
  </form>
</template>
```

Los props llevan dos puntos cuando reciben una expresión (`:items`, `:min`, `:max-length`), como en el resto de la serie.

## El formulario en Angular

Los componentes de valor de Angular implementan `ControlValueAccessor`, así que funcionan con los formularios reactivos sin adaptadores. Aquí la regla es un `FormGroup` y cada componente se une a su control con `formControlName`:

```ts
import { Component, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { SpButton } from '@silverpoint/angular/ui/button';
import { SpRadioGroup } from '@silverpoint/angular/ui/radio-group';
import { SpSegmented } from '@silverpoint/angular/ui/segmented';
import { SpSlider } from '@silverpoint/angular/ui/slider';
import { SpSwitch } from '@silverpoint/angular/ui/switch';
import { SpTextarea } from '@silverpoint/angular/ui/textarea';

const METRICS = [
  { key: 'errors', label: 'Errors' },
  { key: 'hits', label: 'Hits' },
];

const CHANNELS = [
  { key: 'email', label: 'Email' },
  { key: 'chat', label: 'Chat' },
  { key: 'sms', label: 'SMS', disabled: true },
];

@Component({
  selector: 'app-alert-rule-form',
  imports: [ReactiveFormsModule, SpButton, SpRadioGroup, SpSegmented, SpSlider, SpSwitch, SpTextarea],
  template: `
    <form [formGroup]="rule" (ngSubmit)="save()">
      <sp-segmented label="Metric" name="metric" [items]="metrics" formControlName="metric" />
      <sp-slider
        label="Threshold"
        name="threshold"
        [min]="0"
        [max]="50"
        [step]="5"
        [marks]="[0, 25, 50]"
        formControlName="threshold"
      />
      <sp-radio-group
        label="Notify by"
        name="channel"
        [items]="channels"
        orientation="horizontal"
        formControlName="channel"
      />
      <sp-switch label="Active" name="active" formControlName="active" />
      <sp-textarea
        label="Notes"
        placeholder="Notes for the on-call team"
        name="notes"
        [rows]="2"
        [maxLength]="200"
        showCount
        formControlName="notes"
      />
      <button type="submit" spButton variant="primary">Save rule</button>
      <p role="status">{{ saved() }}</p>
    </form>
  `,
})
export class AlertRuleForm {
  protected readonly metrics = METRICS;
  protected readonly channels = CHANNELS;
  protected readonly rule = new FormGroup({
    metric: new FormControl('errors', { nonNullable: true }),
    threshold: new FormControl(10, { nonNullable: true }),
    channel: new FormControl('email', { nonNullable: true }),
    active: new FormControl(true, { nonNullable: true }),
    notes: new FormControl('', { nonNullable: true }),
  });
  protected readonly saved = signal('');

  protected save() {
    const { metric, threshold, channel, active, notes } = this.rule.getRawValue();
    this.saved.set(`${metric} ≥ ${threshold}, by ${channel}, ${active ? 'active' : 'paused'}. Notes: ${notes || '—'}`);
  }
}
```

En Angular el botón no es un componente propio: es la directiva `spButton` sobre un `<button>` nativo, que sigue siendo el control. Si prefieres no usar formularios, cada componente acepta `[(value)]` con un signal.

## El formulario en Reflex

En Reflex el valor vive en el estado, y cada componente controlado recibe `value` y su manejador `on_change`. Las notas usan `default_value`, y `on_submit` recibe el formulario como un diccionario con los campos por su `name`:

```python
import reflex as rx
from reflex_silverpoint_react import (
    sp_alert,
    sp_button,
    sp_card,
    sp_progress,
    sp_radio_group,
    sp_segmented,
    sp_slider,
    sp_statistic,
    sp_switch,
    sp_tag,
    sp_textarea,
)

METRICS = [
    {"key": "errors", "label": "Errors"},
    {"key": "hits", "label": "Hits"},
]

CHANNELS = [
    {"key": "email", "label": "Email"},
    {"key": "chat", "label": "Chat"},
    {"key": "sms", "label": "SMS", "disabled": True},
]


class RuleState(rx.State):
    metric: str = "errors"
    threshold: int = 10
    channel: str = "email"
    active: bool = True
    saved: str = ""

    @rx.event
    def set_metric(self, value: str):
        self.metric = value

    @rx.event
    def set_threshold(self, value: float):
        self.threshold = int(value)

    @rx.event
    def set_channel(self, value: str):
        self.channel = value

    @rx.event
    def set_active(self, value: bool):
        self.active = value

    @rx.event
    def save(self, form: dict):
        state = "active" if self.active else "paused"
        notes = form.get("notes") or "—"
        self.saved = f"{self.metric} ≥ {self.threshold}, by {self.channel}, {state}. Notes: {notes}"


def alert_rule_form() -> rx.Component:
    return rx.el.form(
        sp_segmented(
            label="Metric",
            name="metric",
            items=METRICS,
            value=RuleState.metric,
            on_change=RuleState.set_metric,
        ),
        sp_slider(
            label="Threshold",
            name="threshold",
            min=0,
            max=50,
            step=5,
            marks=[0, 25, 50],
            value=RuleState.threshold,
            on_change=RuleState.set_threshold,
        ),
        sp_radio_group(
            label="Notify by",
            name="channel",
            items=CHANNELS,
            orientation="horizontal",
            value=RuleState.channel,
            on_change=RuleState.set_channel,
        ),
        sp_switch(
            label="Active",
            name="active",
            checked=RuleState.active,
            on_change=RuleState.set_active,
        ),
        sp_textarea(
            label="Notes",
            placeholder="Notes for the on-call team",
            name="notes",
            rows=2,
            max_length=200,
            show_count=True,
            default_value="",
        ),
        sp_button("Save rule", type="submit", variant="primary"),
        rx.el.p(RuleState.saved, role="status"),
        on_submit=RuleState.save,
        style={"display": "grid", "gap": "20px", "align_content": "start"},
    )
```

Cada cambio de un componente controlado viaja al backend y vuelve. Si el usuario pulsa dos veces la flecha del deslizador más rápido que ese viaje, la segunda pulsación parte del valor anterior. En la prueba, dos pulsaciones seguidas dejaron el umbral en 15 en lugar de 20; con una pausa entre ellas, en 20. Para un campo que solo necesitas al enviar, usa `default_value` y léelo en `on_submit`, como las notas.

## Los componentes que muestran datos

| Componente | Muestra |
|---|---|
| `SpCard` | Un marco con título, un hueco a la derecha y un pie |
| `SpStatistic` | Una cifra con título, prefijo, sufijo y tendencia |
| `SpProgress` | Un progreso en línea o en círculo, o indeterminado |
| `SpTag` | Una etiqueta corta, que se puede cerrar |
| `SpBadge` | Un número o un punto sobre su contenido |
| `SpAlert` | Un aviso de información, éxito, advertencia o error |
| `SpSteps` | Los pasos de un proceso y el actual |
| `SpSkeleton` | El hueco de un contenido que está cargando |
| `SpDivider` | Una línea de separación, con texto opcional |

La tarjeta de estado del servicio usa cinco. En React:

```tsx
import { SpAlert } from '@silverpoint/react/ui/alert';
import { SpCard } from '@silverpoint/react/ui/card';
import { SpProgress } from '@silverpoint/react/ui/progress';
import { SpStatistic } from '@silverpoint/react/ui/statistic';
import { SpTag } from '@silverpoint/react/ui/tag';

export function ServiceStatus() {
  return (
    <SpCard title="Service status">
      <SpStatistic title="Errors today" value={103} trend="down" delta="-12" />
      <SpProgress label="Error budget used" value={62} />
      <p>
        <SpTag>api</SpTag> <SpTag tone={2}>checkout</SpTag>
      </p>
      <SpAlert kind="warning" title="Checkout above its latency budget">
        p95 at 682 ms against a budget of 300 ms.
      </SpAlert>
    </SpCard>
  );
}
```

En Vue:

```vue
<script setup lang="ts">
import { SpAlert } from '@silverpoint/vue/ui/alert';
import { SpCard } from '@silverpoint/vue/ui/card';
import { SpProgress } from '@silverpoint/vue/ui/progress';
import { SpStatistic } from '@silverpoint/vue/ui/statistic';
import { SpTag } from '@silverpoint/vue/ui/tag';
</script>

<template>
  <SpCard title="Service status">
    <SpStatistic title="Errors today" :value="103" trend="down" delta="-12" />
    <SpProgress label="Error budget used" :value="62" />
    <p>
      <SpTag>api</SpTag> <SpTag :tone="2">checkout</SpTag>
    </p>
    <SpAlert kind="warning" title="Checkout above its latency budget">
      p95 at 682 ms against a budget of 300 ms.
    </SpAlert>
  </SpCard>
</template>
```

En Angular:

```ts
import { Component } from '@angular/core';
import { SpAlert } from '@silverpoint/angular/ui/alert';
import { SpCard } from '@silverpoint/angular/ui/card';
import { SpProgress } from '@silverpoint/angular/ui/progress';
import { SpStatistic } from '@silverpoint/angular/ui/statistic';
import { SpTag } from '@silverpoint/angular/ui/tag';

@Component({
  selector: 'app-service-status',
  imports: [SpAlert, SpCard, SpProgress, SpStatistic, SpTag],
  template: `
    <sp-card title="Service status">
      <sp-statistic title="Errors today" [value]="103" trend="down" delta="-12" />
      <sp-progress label="Error budget used" [value]="62" />
      <p>
        <sp-tag>api</sp-tag> <sp-tag [tone]="2">checkout</sp-tag>
      </p>
      <sp-alert kind="warning" title="Checkout above its latency budget">
        p95 at 682 ms against a budget of 300 ms.
      </sp-alert>
    </sp-card>
  `,
})
export class ServiceStatus {}
```

Y en Reflex:

```python
def service_status() -> rx.Component:
    return sp_card(
        sp_statistic(title="Errors today", value=103, trend="down", delta="-12"),
        sp_progress(label="Error budget used", value=62),
        rx.el.p(sp_tag("api"), " ", sp_tag("checkout", tone=2)),
        sp_alert(
            "p95 at 682 ms against a budget of 300 ms.",
            kind="warning",
            title="Checkout above its latency budget",
        ),
        title="Service status",
    )
```

`SpStatistic` imprime el valor tal cual, sin formatearlo. La tendencia `down` dibuja la flecha ↓ junto a `delta`, y el aviso `warning` dibuja su triángulo. El texto de la tarjeta (`p95 at 682 ms`) es el percentil 95 de `Checkout` del [artículo 14](/blog/silverpoint_serie_14).

## Accesibilidad

* **Cada control tiene nombre.** En los controles con texto visible (`SpCheckbox`, `SpSwitch`, `SpSlider`, `SpRadioGroup`, `SpSegmented`, `SpProgress`), `label` es obligatorio: en TypeScript, un `SpSwitch` sin `label` no compila. En `SpInput` y `SpTextarea`, `label` es el nombre accesible y no se dibuja; si quieres un rótulo visible, usa tu propio `<label for>`.
* **Un botón o una insignia sin texto avisan.** Un `SpButton` sin texto ni `label` se dibuja igual, pero en desarrollo la consola muestra `SP018`.
* **El foco se ve siempre igual.** El anillo de foco es un contorno exacto, nunca entintado a mano, con el color del campo `focus` de la paleta, que por defecto es la tinta. El [artículo 12](/blog/silverpoint_serie_12) explica cómo cambiarlo.
* **Ningún estado se dice solo con el tramado.** Marcado, seleccionado, error o deshabilitado llevan también un glifo, una forma, un texto o un estado nativo: la flecha de la tendencia, el triángulo del aviso, el ⚠ de un campo inválido.

## Problemas comunes

* **Los componentes salen con los controles nativos y glifos negros gigantes.** Falta `@silverpoint/grounds/ui.css`.
* **`onChange` no se llama al cambiar el valor desde el código.** Es lo esperado: los eventos de valor solo responden al usuario.
* **En Reflex, el deslizador se salta valores con el teclado.** Es el viaje de ida y vuelta al backend de un componente controlado. Usa `default_value` si el valor solo se necesita al enviar.
* **La consola muestra `SP018`.** Un botón o una insignia no tienen texto ni `label`.

## Lo que viene

El panel ya puede pedir datos y mostrar su estado. El [artículo 17](/blog/silverpoint_serie_17) sigue con los componentes de interfaz: una tabla de incidencias que se ordena y se pagina, un modal para reconocer una incidencia y una notificación que lo confirma.

La [guía de componentes](https://silverpointweb.vercel.app/docs/ui) de la documentación tiene la referencia de los 38.
