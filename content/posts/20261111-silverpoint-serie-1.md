Title: Silverpoint, artículo 01: gráficos con una técnica de dibujo histórica
Date: 2026-11-11 11:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_1
Authors: Ernesto Crespo
Summary: Qué es silverpoint: la técnica renacentista Silverpoint, cómo se traduce en reglas para dibujar gráficos y por qué el dato nunca se dibuja a mano alzada.

En el [artículo 0](/blog/silverpoint_serie_0) vimos el mapa de la serie. Este artículo, el primero del nivel de fundamentos, explica la idea de fondo de [silverpoint](https://github.com/ecrespo/silverpoint): por qué una técnica de dibujo del siglo XV sirve para leer datos hoy, y qué reglas salen de ella.

Al final hay un ejemplo con el mismo gráfico en React, Vue, Angular y Reflex. No hace falta instalar nada para seguir el artículo: la instalación llega en el 02 y, con más detalle, en los artículos 03 a 06.

## La técnica Silverpoint

Silverpoint es una técnica de dibujo anterior al lápiz de grafito. El artista dibuja con un estilete de plata sobre un papel que antes ha preparado con una capa fina de imprimación: hueso calcinado molido, cola y, muchas veces, un pigmento que tiñe el papel de crema, verde, azul u ocre. Sin esa capa, la plata no deja marca.

La técnica impone sus propias reglas:

* **La línea es fina y de grosor fijo.** El estilete no permite apretar más para oscurecer, así que el trazo apenas cambia.
* **El tono se construye con tramado.** Para oscurecer una zona se acumulan líneas paralelas o cruzadas; más densidad, más tono.
* **No se borra.** Cada línea queda, así que el dibujo exige decidir antes de trazar.
* **Las luces se añaden en blanco.** Sobre el papel teñido, el artista pinta con blanco los puntos de máxima luz. Ese realce se usa con mucha economía.

Jan van Eyck, Leonardo da Vinci y Alberto Durero dibujaron así. El autorretrato que Durero hizo con trece años, en 1484, está dibujado con Silverpoint.

## De la técnica a las reglas de la librería

La librería toma esas cuatro reglas y las convierte en reglas de dibujo para gráficos. Están escritas en la [constitución del proyecto](https://github.com/ecrespo/silverpoint/blob/main/specs/constitution.md), y el código las verifica con pruebas.

| En el papel | En silverpoint |
|---|---|
| Papel preparado de tono medio | El sustrato: `cream`, `green`, `blue` u `ochre`, la prop `substrate` |
| Línea fina de plata | Un trazo de grosor fijo, la variable CSS `--sp-stroke-width` |
| Tono por tramado | El valor se construye con la densidad y el ángulo de las líneas, nunca con un relleno plano y transparencia |
| Realce en blanco | Un único elemento realzado por gráfico, el que importa |

La última regla es la más visible. En un gráfico de línea, el elemento realzado es el último punto, el valor vivo de la serie. Cada gráfico declara qué elemento realza, y la librería no permite realzar dos.

## El problema de los gráficos dibujados a mano

Hay otras librerías con aspecto de dibujo a mano. La más conocida es rough.js, que silverpoint usa por dentro. Su estilo, el llamado *sketchy*, tiene un problema: si el trazo de una barra tiembla, su altura ya no es exacta. El estudio de Wood y colaboradores sobre el dibujo *sketchy* en visualización (IEEE VIS 2012), que la constitución cita como justificación, muestra que los trazos irregulares empeoran la lectura de áreas y proporciones.

La librería resuelve esto separando dos tipos de trazo:

* **El ornamento**: el marco de la tarjeta, las reglas, las líneas de rejilla y el tramado. Aquí vive la irregularidad de la mano.
* **La geometría del dato**: la posición, la longitud, el ángulo y el área que codifican un valor. Esta se calcula siempre de forma exacta.

Por eso cada gráfico tiene un modo `precision` que apaga el entintado por completo, y la librería garantiza que el modo `ink` (el normal) y el modo `precision` dibujan los datos con los mismos vértices.

## Tres variaciones del mismo gráfico

Esta imagen muestra las visitas por hora de un servicio web, el dato con el que empieza el proyecto de la serie, dibujado tres veces:

![El mismo gráfico de barras en modo ink, en modo precision y con el estilo base cyanotype](./images/silverpoint-serie-1.png)

* **`mode="ink"`**: el modo por defecto. Las barras llevan tramado y el marco y las reglas tienen el pulso de la mano.
* **`mode="precision"`**: sin entintado. Las barras son las mismas, sin tramado.
* **`ground="cyanotype"`**: el segundo estilo base. La cianotipia, un proceso fotográfico de 1842, da una línea blanca sobre azul de Prusia. Aquí el tono no se construye con tramado sino con el grosor de una línea exacta.

El código es el mismo en los cuatro frameworks; solo cambia la sintaxis de cada uno. En React:

```tsx
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import { BarChart } from '@silverpoint/react/bar-chart';

const data = [
  { hour: '00', hits: 18 },
  { hour: '04', hits: 11 },
  { hour: '08', hits: 42 },
  { hour: '12', hits: 64 },
  { hour: '16', hits: 57 },
  { hour: '20', hits: 30 },
];

export default function App() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 320px)', gap: 24 }}>
      <BarChart data={data} xKey="hour" valueKey="hits" title="ink" />
      <BarChart data={data} xKey="hour" valueKey="hits" title="precision" mode="precision" />
      <BarChart data={data} xKey="hour" valueKey="hits" title="cyanotype" ground="cyanotype" />
    </div>
  );
}
```

En Vue:

```vue
<script setup lang="ts">
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import { SpBarChart } from '@silverpoint/vue/bar-chart';

const data = [
  { hour: '00', hits: 18 },
  { hour: '04', hits: 11 },
  { hour: '08', hits: 42 },
  { hour: '12', hits: 64 },
  { hour: '16', hits: 57 },
  { hour: '20', hits: 30 },
];
</script>

<template>
  <div style="display: grid; grid-template-columns: repeat(3, 320px); gap: 24px">
    <SpBarChart :data="data" x-key="hour" value-key="hits" title="ink" />
    <SpBarChart :data="data" x-key="hour" value-key="hits" title="precision" mode="precision" />
    <SpBarChart :data="data" x-key="hour" value-key="hits" title="cyanotype" ground="cyanotype" />
  </div>
</template>
```

En Angular, con las dos hojas de estilo importadas en `src/styles.css`:

```ts
import { Component } from '@angular/core';
import { SpBarChart } from '@silverpoint/angular/bar-chart';

@Component({
  selector: 'app-root',
  imports: [SpBarChart],
  template: `
    <div style="display: grid; grid-template-columns: repeat(3, 320px); gap: 24px">
      <sp-bar-chart [data]="data" xKey="hour" valueKey="hits" title="ink" />
      <sp-bar-chart [data]="data" xKey="hour" valueKey="hits" title="precision" mode="precision" />
      <sp-bar-chart [data]="data" xKey="hour" valueKey="hits" title="cyanotype" ground="cyanotype" />
    </div>
  `,
})
export class App {
  protected readonly data = [
    { hour: '00', hits: 18 },
    { hour: '04', hits: 11 },
    { hour: '08', hits: 42 },
    { hour: '12', hits: 64 },
    { hour: '16', hits: 57 },
    { hour: '20', hits: 30 },
  ];
}
```

Y en Reflex, solo con Python:

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart

DATA = [
    {"hour": "00", "hits": 18},
    {"hour": "04", "hits": 11},
    {"hour": "08", "hits": 42},
    {"hour": "12", "hits": 64},
    {"hour": "16", "hits": 57},
    {"hour": "20", "hits": 30},
]


def index() -> rx.Component:
    return rx.grid(
        bar_chart(data=DATA, x_key="hour", value_key="hits", title="ink"),
        bar_chart(data=DATA, x_key="hour", value_key="hits", title="precision", mode="precision"),
        bar_chart(data=DATA, x_key="hour", value_key="hits", title="cyanotype", ground="cyanotype"),
        columns="3",
        spacing="5",
        width="1000px",
    )


app = rx.App()
app.add_page(index)
```

Un detalle que conviene saber desde ya: el gráfico toma el ancho de su contenedor. Si el contenedor no tiene ancho, por ejemplo un `rx.hstack` sin tamaño, el gráfico espera a tenerlo y no dibuja nada. Por eso los cuatro ejemplos le dan un ancho a la rejilla.

## Compruébalo tú mismo

La promesa de que el modo `ink` no toca el dato se puede verificar. Este script de Node dibuja el gráfico en el servidor con la entrada `server` del adaptador de React y compara los dos modos:

```js
import { createElement as h } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { BarChart } from '@silverpoint/react/server/bar-chart';

const data = [
  { hour: '00', hits: 18 },
  { hour: '04', hits: 11 },
  { hour: '08', hits: 42 },
  { hour: '12', hits: 64 },
  { hour: '16', hits: 57 },
  { hour: '20', hits: 30 },
];

const render = (mode) =>
  renderToStaticMarkup(
    h(BarChart, { data, xKey: 'hour', valueKey: 'hits', id: 'hits', width: 320, mode }),
  );

const bars = (svg) => [...svg.matchAll(/d="([^"]+)"[^>]*data-role="encoding"/g)].map((m) => m[1]);
const hatches = (svg) => (svg.match(/data-role="hatch"/g) ?? []).length;

const ink = render('ink');
const precision = render('precision');

console.log('same bars:', JSON.stringify(bars(ink)) === JSON.stringify(bars(precision)));
console.log('hatch strokes:', hatches(ink), 'in ink,', hatches(precision), 'in precision');
console.log('same strokes on every render:', ink === render('ink'));
```

Guárdalo como `verify.mjs` en un proyecto con `@silverpoint/react` instalado y ejecútalo con `node verify.mjs`. La salida es:

```text
same bars: true
hatch strokes: 12 in ink, 0 in precision
same strokes on every render: true
```

Las seis barras tienen exactamente el mismo trazado en los dos modos. El tramado, con sus doce líneas, existe solo en el modo `ink`. Y la tercera línea adelanta la siguiente idea.

En el servidor, un gráfico no puede medir su contenedor, así que el script fija `width`. También fija un `id`: fuera de un panel, un gráfico de servidor lo necesita, y si falta la librería usa uno fijo y lo avisa con el diagnóstico `SP002`.

## El trazo no cambia entre renders

La mano de silverpoint no es aleatoria. Cada gráfico tiene una semilla, la prop `seed`. Si no la pasas, se deriva de forma estable del `id` del gráfico. La librería no llama a `Math.random()` ni a `Date.now()` mientras dibuja. Con las mismas props, el trazo es el mismo en cada render, en el servidor y en cualquier navegador.

Esto tiene dos consecuencias prácticas. Un gráfico no tiembla cuando React, Vue o Angular lo vuelven a dibujar. Y un gráfico renderizado en el servidor se hidrata en el navegador sin diferencias.

## Accesible por defecto

El estilo a mano es una elección estética y no puede dejar fuera a nadie. Por eso cada gráfico:

* Expone un rol y un nombre accesibles. En el ejemplo, el SVG lleva `role="img"` y una descripción generada a partir de los datos: «Bar chart in columns of 6 hour values; hits from 11 to 64».
* Incluye una tabla de datos oculta para lectores de pantalla, que se controla con la prop `dataTable` (`data_table` en Reflex).
* Se navega con el teclado.
* Pasa automáticamente al modo `precision` cuando el sistema pide más contraste (`prefers-contrast: more`) o colores forzados (`forced-colors: active`).

Además, ningún gráfico codifica información solo con el estilo del tramado. El artículo 10 de la serie entra en detalle.

## Un motor, cuatro frameworks

Queda una pieza: ¿cómo dibujan React, Vue, Angular y Reflex exactamente lo mismo?

Toda la geometría (escalas, ejes, arcos, trazados) se calcula en un único motor, `@silverpoint/core`, que no depende del DOM ni de ningún framework. Cada adaptador solo traduce lo que el motor calcula en nodos de su framework. La integración continua compara el SVG que produce cada adaptador con una versión de referencia, carácter a carácter y sin tolerancia. Reflex usa por dentro el adaptador de React, así que hereda la misma garantía.

Por eso los cuatro ejemplos de arriba producen el mismo SVG: tres gráficos, doce líneas de tramado y las mismas barras.

Y el estilo es un dato, no código. Un estilo base como `silverpoint` o `cyanotype` es un conjunto de valores (sustrato, tintas, parámetros de entintado, tipografía, mecanismo tonal), y añadir uno nuevo no obliga a cambiar ningún gráfico.

## Lo que viene

Ya conoces las ideas: el sustrato, la línea, el tramado, el realce único, la geometría exacta, el determinismo y la accesibilidad. El artículo 02 recorre el mapa de paquetes: qué hace el motor, qué aportan los estilos y las fuentes, qué adaptador instalar y qué paquetes son opcionales.

Mientras tanto, puedes ver los estilos base y los sustratos en la [documentación](https://silverpointweb.vercel.app/docs/grounds) y los 60 gráficos en la [galería](https://silverpointweb.vercel.app/gallery).
