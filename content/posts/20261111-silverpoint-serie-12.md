Title: Silverpoint, artículo 12: paletas y cambio de tema
Date: 2026-11-11 16:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_12
Authors: Ernesto Crespo
Summary: Qué es una paleta en silverpoint, las seis paletas incluidas, cómo comprobar el contraste de una paleta propia y cómo cambiar el tema de un panel mientras la aplicación corre, en React, Vue, Angular y Reflex.

El [artículo 09](/blog/silverpoint_serie_9) dio un estilo común a toda la aplicación con el proveedor: el estilo base, el sustrato y el idioma de los números. Este se ocupa del quinto campo del proveedor, `palette`: los colores.

Es un artículo del nivel 2 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint). Explica qué es una paleta, cómo usar las seis que trae la librería, cómo comprobar el contraste de una propia y cómo cambiar de tema con un selector, sin volver a dibujar los datos.

## Qué es una paleta

silverpoint no escribe ningún color en el dibujo. Cada trazo y cada relleno se pinta con CSS, a través de propiedades personalizadas `--sp-*`. Una paleta es un objeto que da valor a esas propiedades, y el gráfico las escribe en el `style` de su raíz.

| Campo | Propiedad CSS | Qué pinta |
|---|---|---|
| `substrate` | `--sp-substrate` | El papel sobre el que se dibuja |
| `ink` | `--sp-ink` | La serie principal y los marcos de los componentes |
| `inkSecondary` | `--sp-ink-secondary` | La segunda serie y el tramado |
| `heighten` | `--sp-heighten` | El realce blanco del valor vivo |
| `rule` | `--sp-rule` | Las reglas y las líneas base |
| `grid` | `--sp-grid` | La rejilla |
| `text` | `--sp-text` | Las cifras grandes y las etiquetas principales |
| `textMuted` | `--sp-text-muted` | Las etiquetas de los ejes y el texto secundario |
| `focus` | `--sp-ui-focus-color` | El anillo de foco de los componentes; por defecto, `ink` |

Todos los campos son opcionales. Los que no declaras mantienen el color del estilo base.

Una paleta tiene dos tintas, `ink` e `inkSecondary`, y no un color por serie. Es una decisión de diseño: en el estilo base `silverpoint`, las categorías se distinguen por la densidad del tramado, no por el color.

## Las seis paletas

La librería trae seis paletas con nombres de técnicas de dibujo, todas comprobadas contra su propio sustrato.

| Paleta | En Reflex | Sustrato | Tinta |
|---|---|---|---|
| `silverpoint` | `"silverpoint"` | `#EDE7DA` | `#5A5E65` |
| `sanguine` | `"sanguine"` | `#F2E8DC` | `#8A3A24` |
| `sepia` | `"sepia"` | `#F0E6D2` | `#6B4C2C` |
| `ironGall` | `"iron_gall"` | `#EEEAE0` | `#3C4858` |
| `verdigris` | `"verdigris"` | `#E7EDE6` | `#2C6355` |
| `indigo` | `"indigo"` | `#E9EAF1` | `#3A4884` |

Este es el gráfico de ventas por canal del panel con cada una:

![El mismo gráfico de barras con las seis paletas: silverpoint, sanguine, sepia, ironGall, verdigris e indigo](./images/silverpoint-serie-12.png)

## Usar una paleta

En React, Vue y Angular, una paleta es un objeto que se importa de `@silverpoint/core/palettes`. Se pasa el objeto, nunca su nombre: así, una aplicación que no nombra ninguna paleta no incluye ninguna. Como tu código importa del motor, decláralo en tu proyecto:

```sh
npm install @silverpoint/core
```

En Reflex no hay nada que importar: `palette` acepta el nombre de la paleta como texto.

| Framework | Un gráfico con la paleta `sanguine` |
|---|---|
| React | `palette={sanguine}` |
| Vue | `:palette="sanguine"` |
| Angular | `[palette]="sanguine"`, con `sanguine` como campo del componente |
| Reflex | `palette="sanguine"` |

La paleta se puede poner en un gráfico, en un panel o en el proveedor. Como el resto de campos del artículo 09, se combina campo a campo: lo que declara el gráfico gana a lo del proveedor, y lo que no declara lo hereda.

## Una paleta propia

Una paleta propia es un objeto con los campos que quieras cambiar, por ejemplo los colores de tu marca. Antes de usarla, comprueba su contraste. `checkPalette` mide los mismos pares que la librería exige a sus paletas: cada tinta y cada texto contra el sustrato (4,5:1), las reglas, la rejilla y el foco (3:1), y el realce blanco contra su contorno.

```js
import { checkPalette } from '@silverpoint/core/palettes';

const brand = {
  substrate: '#F7F3EA',
  ink: '#1F4E79',
  inkSecondary: '#7A5C3E',
  text: '#1B2B3A',
  textMuted: '#9AA8B5',
};

console.log(checkPalette(brand));
```

El resultado es una lista con un hallazgo por par que no llega a su umbral:

```text
[
  {
    pair: 'text-muted',
    foreground: '#9AA8B5',
    background: '#F7F3EA',
    ratio: 2.19,
    threshold: 4.5
  }
]
```

El gris azulado de las etiquetas secundarias se queda en 2,19:1. Con `textMuted: '#4F6275'` la lista sale vacía.

En Python es la misma comprobación, con los campos en `snake_case`:

```python
from reflex_silverpoint_react import Palette, check_palette

BRAND = Palette(
    substrate="#F7F3EA",
    ink="#1F4E79",
    ink_secondary="#7A5C3E",
    text="#1B2B3A",
    text_muted="#9AA8B5",
)

print(check_palette(BRAND))
```

```text
['text-muted #9AA8B5 on #F7F3EA: 2.19:1, below 4.5:1']
```

Si usas la paleta sin corregirla, el gráfico la dibuja tal cual, pero en desarrollo la consola avisa:

```text
[SP023] Palette: a palette colour is below its contrast threshold against its substrate; it is drawn as given (`text-muted`). #9AA8B5 on #F7F3EA is 2.19:1, below 4.5:1. Recompute the palette with checkPalette(); colours are not chosen by eye. (REQ-466)
```

Un valor que no es un color seguro, como `'#2C6355; display: none'`, no se dibuja: el campo se descarta y la consola muestra `SP024`. En Reflex, un campo que no existe o un nombre de paleta desconocido fallan antes, al construir la página, con un `ValueError` que lista los nombres válidos.

## Cambiar de tema

Un tema es un estilo base y una paleta. El panel del artículo 09 tendrá un selector con cuatro: tres paletas sobre `silverpoint` y la cianotipia, que no necesita paleta. En React, Vue y Angular, los temas van en `themes.ts`:

```ts
import type { GroundName, Palette } from '@silverpoint/core';
import { indigo, sanguine, silverpoint } from '@silverpoint/core/palettes';

export type Theme = {
  key: string;
  label: string;
  ground: GroundName;
  palette?: Palette;
};

export const themes: Theme[] = [
  { key: 'silverpoint', label: 'Silverpoint', ground: 'silverpoint', palette: silverpoint },
  { key: 'sanguine', label: 'Sanguine', ground: 'silverpoint', palette: sanguine },
  { key: 'indigo', label: 'Indigo', ground: 'silverpoint', palette: indigo },
  { key: 'cyanotype', label: 'Cyanotype', ground: 'cyanotype' },
];
```

### React

El tema elegido es estado del componente, y el proveedor lo recibe como props:

```tsx
import { useState } from 'react';
import { SilverpointProvider } from '@silverpoint/react';
import { Panel } from './Panel';
import { themes } from './themes';

export default function App() {
  const [key, setKey] = useState('silverpoint');
  const theme = themes.find((t) => t.key === key) ?? themes[0];

  return (
    <main style={{ maxWidth: 640 }}>
      <label>
        Theme{' '}
        <select value={key} onChange={(event) => setKey(event.target.value)}>
          {themes.map((t) => (
            <option key={t.key} value={t.key}>
              {t.label}
            </option>
          ))}
        </select>
      </label>
      <SilverpointProvider ground={theme.ground} palette={theme.palette}>
        <Panel />
      </SilverpointProvider>
    </main>
  );
}
```

`Panel` es el del artículo 09, sin cambios.

### Vue

`SilverpointProvider` sigue a sus props como cualquier componente de Vue:

```vue
<script setup lang="ts">
import { computed, ref } from 'vue';
import { SilverpointProvider } from '@silverpoint/vue';
import Panel from './Panel.vue';
import { themes } from './themes';

const key = ref('silverpoint');
const theme = computed(() => themes.find((t) => t.key === key.value) ?? themes[0]);
</script>

<template>
  <main style="max-width: 640px">
    <label>
      Theme
      <select v-model="key">
        <option v-for="t in themes" :key="t.key" :value="t.key">{{ t.label }}</option>
      </select>
    </label>
    <SilverpointProvider :ground="theme.ground" :palette="theme.palette">
      <Panel />
    </SilverpointProvider>
  </main>
</template>
```

### Angular

En Angular, `provideSilverpoint` recibe un objeto fijo al crear el inyector, así que no sirve para un tema que cambia. El tema se pasa a las entradas de los gráficos, que sí siguen a los signals. El panel recibe el estilo base y la paleta como entradas, `src/app/panel.ts`:

```ts
import { Component, input } from '@angular/core';
import type { GroundName, Palette } from '@silverpoint/core';
import { SpBarChart } from '@silverpoint/angular/bar-chart';
import { SpLineChart } from '@silverpoint/angular/line-chart';
import { sales } from './sales';
import { traffic } from './traffic';

@Component({
  selector: 'app-panel',
  imports: [SpLineChart, SpBarChart],
  template: `
    <section style="display: grid; gap: 16px">
      <sp-line-chart
        [data]="traffic"
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        [value]="63844"
        unit="requests at the peak"
        [ground]="ground()"
        [palette]="palette()"
      />
      <sp-bar-chart
        [data]="sales"
        xKey="channel"
        valueKey="sales"
        title="Sales by channel"
        [ground]="ground()"
        [palette]="palette()"
      />
    </section>
  `,
})
export class Panel {
  readonly ground = input<GroundName>();
  readonly palette = input<Palette>();
  protected readonly traffic = traffic;
  protected readonly sales = sales;
}
```

Y `src/app/app.ts` guarda el tema en un signal:

```ts
import { Component, computed, signal } from '@angular/core';
import { Panel } from './panel';
import { themes } from './themes';

@Component({
  selector: 'app-root',
  imports: [Panel],
  template: `
    <main style="max-width: 640px">
      <label>
        Theme
        <select #select (change)="key.set(select.value)">
          @for (t of themes; track t.key) {
            <option [value]="t.key" [selected]="t.key === key()">{{ t.label }}</option>
          }
        </select>
      </label>
      <app-panel [ground]="theme().ground" [palette]="theme().palette" />
    </main>
  `,
})
export class App {
  protected readonly themes = themes;
  protected readonly key = signal('silverpoint');
  protected readonly theme = computed(() => themes.find((t) => t.key === this.key()) ?? themes[0]);
}
```

### Reflex

En Reflex, el tema es estado. La paleta del proveedor es una variable calculada con los campos de la paleta elegida, como diccionario:

```python
import reflex as rx
from reflex_silverpoint_react import PALETTES, bar_chart, line_chart, silverpoint_provider

from .sales import SALES
from .traffic import TRAFFIC

THEMES = {
    "silverpoint": {"label": "Silverpoint", "ground": "silverpoint", "palette": "silverpoint"},
    "sanguine": {"label": "Sanguine", "ground": "silverpoint", "palette": "sanguine"},
    "indigo": {"label": "Indigo", "ground": "silverpoint", "palette": "indigo"},
    "cyanotype": {"label": "Cyanotype", "ground": "cyanotype", "palette": None},
}


class ThemeState(rx.State):
    theme: str = "silverpoint"

    @rx.event
    def set_theme(self, value: str):
        self.theme = value

    @rx.var
    def ground(self) -> str:
        return THEMES[self.theme]["ground"]

    @rx.var
    def palette(self) -> dict[str, str]:
        name = THEMES[self.theme]["palette"]
        return PALETTES[name].to_dict() if name else {}


def panel() -> rx.Component:
    return rx.el.section(
        line_chart(
            data=TRAFFIC,
            x_key="hour",
            value_key="hits",
            title="Hits per hour",
            value=63844,
            unit="requests at the peak",
        ),
        bar_chart(data=SALES, x_key="channel", value_key="sales", title="Sales by channel"),
        style={"display": "grid", "gap": "16px"},
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.label(
            "Theme ",
            rx.el.select(
                *[rx.el.option(theme["label"], value=key) for key, theme in THEMES.items()],
                value=ThemeState.theme,
                on_change=ThemeState.set_theme,
            ),
        ),
        silverpoint_provider(panel(), ground=ThemeState.ground, palette=ThemeState.palette),
        style={"max_width": "640px", "padding": "32px"},
    )


app = rx.App()
app.add_page(index)
```

Para la cianotipia, la paleta es un diccionario vacío: ningún campo declarado, así que se usan los colores del estilo base.

### Qué se vuelve a dibujar

Cambiar de paleta no vuelve a dibujar el gráfico. Solo cambian los valores de las propiedades `--sp-*` en la raíz de cada gráfico; los trazados del SVG son los mismos, carácter por carácter. Lo comprobé en los cuatro frameworks pasando de `silverpoint` a `sanguine` y a `indigo`.

Cambiar de estilo base sí vuelve a dibujar, porque la cianotipia construye el tono de otra manera: sin tramado, con el grosor de la línea. Al volver a `silverpoint`, el gráfico dibuja exactamente las mismas líneas que antes, porque el trazo a mano sale de la semilla, no del azar.

## Problemas comunes

* **TypeScript rechaza `palette="sanguine"`.** En React, Vue y Angular, `palette` recibe el objeto importado de `@silverpoint/core/palettes`, no su nombre. El nombre solo funciona en Reflex.
* **La consola muestra `SP023` y el gráfico se ve bien.** Uno de los colores no llega al contraste mínimo contra el sustrato. Se dibuja igual, pero alguien con baja visión puede no leerlo. Corrígelo con `checkPalette`.
* **Un color de la paleta no aparece.** Si en desarrollo la consola muestra `SP024`, el valor no es un color seguro o el campo no existe, y se descartó.
* **El fondo de la página no cambia con el tema.** La paleta solo pinta los elementos de silverpoint. Para tus propios elementos, `paletteStyle` en JavaScript y `palette_css` en Python devuelven las mismas propiedades `--sp-*`.

## Lo que viene

Ya tienes el panel con un tema que el usuario elige. El artículo 13 lo ordena en una rejilla responsiva con el componente `Dashboard`, que también acepta estilo base, sustrato y paleta para todos los gráficos que contiene.

La [documentación de las paletas](https://silverpointweb.vercel.app/docs/palettes) tiene las seis paletas y la comprobación de contraste.
