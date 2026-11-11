Title: Silverpoint, artículo 10: modo precision y accesibilidad
Date: 2026-11-11 15:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_10
Authors: Ernesto Crespo
Summary: Qué quita el modo precision y qué deja igual, cuándo lo impone el sistema, y cómo se leen los gráficos de silverpoint sin verlos: nombre, descripción, tabla de datos, teclado y anuncios.

El [artículo 01](/blog/silverpoint_serie_1) contaba que en silverpoint la irregularidad del dibujo a mano vive solo en el ornamento, y que cada gráfico tiene un modo `precision` que la apaga. Este artículo de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) lo pone a prueba y recorre lo que hace accesible a un gráfico: su nombre, su descripción, la tabla de datos, el teclado y lo que oye quien usa un lector de pantalla.

## Lo que vas a construir

Dos gráficos del panel de operaciones, las ventas por canal y los errores por día y franja horaria, dibujados dos veces: con el entintado a mano, a la izquierda, y en modo `precision`, a la derecha.

![Las ventas por canal y los errores por día, con entintado a la izquierda y en modo precision a la derecha](./images/silverpoint-serie-10.png)

Después, el gráfico de visitas por hora con su nombre, su descripción y la tabla de datos a la vista, y el mismo trabajo en Reflex.

## Lo que necesitas

El proyecto de React del [artículo 03](/blog/silverpoint_serie_3) o el de Reflex del [artículo 06](/blog/silverpoint_serie_6), con las visitas por hora de su paso 5 (`src/traffic.ts`) o de su paso 3 (`ops_panel/traffic.py`). En Vue y Angular las props de este artículo se escriben igual: `mode="precision"` y `data-table="visible"` en Vue, `mode="precision"` y `dataTable="visible"` en Angular.

## 1. Los datos

Crea `src/sales.ts` con las ventas por canal, en miles de euros:

```ts
export type ChannelSales = {
  channel: string;
  sales: number;
};

export const sales: ChannelSales[] = [
  { channel: 'Web', sales: 46 },
  { channel: 'App', sales: 31 },
  { channel: 'Partners', sales: 15 },
  { channel: 'Phone', sales: 8 },
];
```

Y `src/errors.ts` con los errores de cada día de la semana en seis franjas de cuatro horas:

```ts
export type DayErrors = {
  day: string;
  values: number[];
};

export const blocks = ['00-04', '04-08', '08-12', '12-16', '16-20', '20-24'];

export const errors: DayErrors[] = [
  { day: 'Mon', values: [3, 5, 31, 38, 22, 8] },
  { day: 'Tue', values: [2, 6, 28, 35, 20, 7] },
  { day: 'Wed', values: [4, 7, 34, 40, 25, 9] },
  { day: 'Thu', values: [3, 5, 29, 36, 21, 8] },
  { day: 'Fri', values: [2, 6, 26, 30, 18, 10] },
  { day: 'Sat', values: [1, 2, 9, 12, 10, 6] },
  { day: 'Sun', values: [1, 1, 7, 10, 8, 5] },
];
```

## 2. Entintado y precisión, lado a lado

Sustituye `src/App.tsx`:

```tsx
import { BarChart } from '@silverpoint/react/bar-chart';
import { HeatmapChart } from '@silverpoint/react/heatmap-chart';
import { blocks, errors } from './errors';
import { sales } from './sales';

const modes = ['ink', 'precision'] as const;

export default function App() {
  return (
    <main style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, maxWidth: 1100 }}>
      {modes.map((mode) => (
        <section key={mode} style={{ display: 'grid', gap: 24 }}>
          <BarChart
            id={`sales-${mode}`}
            data={sales}
            xKey="channel"
            valueKey="sales"
            title="Sales by channel"
            badge={mode}
            mode={mode}
          />
          <HeatmapChart
            id={`errors-${mode}`}
            data={errors}
            labelKey="day"
            valuesKey="values"
            columnLabels={blocks}
            scaleMax={40}
            title="Errors by day and hour"
            badge={mode}
            mode={mode}
            height={220}
          />
        </section>
      ))}
    </main>
  );
}
```

Cada gráfico lleva su propio `id`. De él sale la semilla del trazo a mano y los identificadores de su SVG, así que dos gráficos con las mismas props no comparten nada.

Compara las dos columnas. El modo `precision` quita dos cosas:

* **El temblor de la mano.** En modo `ink`, el marco de la tarjeta, las reglas y la cuadrícula se dibujan con un trazo irregular. En `precision` son líneas exactas.
* **El tramado.** Las barras y las celdas del mapa de calor pierden su trama, y el tono desaparece con ella.

Y deja igual todo lo que representa un dato. Los trazos que codifican los valores, el contorno de cada barra y la línea de un gráfico de línea, tienen exactamente las mismas coordenadas en los dos modos: en el SVG son los `path` con `data-role="encoding"`, y su atributo `d` es idéntico. También se mantienen los textos, los números, el realce del valor vivo, la tabla de datos y la interacción.

El modo se elige en cada gráfico con la prop `mode`, o para toda una sección con el proveedor (artículo 09) o con un panel (artículo 13).

## 3. Cuando el sistema pide más contraste

Hay dos preferencias del sistema que imponen el modo `precision`: `prefers-contrast: more`, cuando el usuario pide más contraste, y `forced-colors: active`, el modo de alto contraste de Windows. Con cualquiera de las dos, todos los gráficos se dibujan sin entintado y sin tramado, aunque lleven `mode="ink"`. Ninguna prop lo deshace.

El cambio se aplica en vivo: si el usuario activa la preferencia con la página abierta, los gráficos se redibujan sin recargar. Puedes probarlo en Chrome, en las herramientas de desarrollo, panel Rendering, con «Emulate CSS media feature prefers-contrast».

La tercera preferencia es `prefers-reduced-motion: reduce`. Cada gráfico entra con una animación corta, de 280 ms, que lo descubre de izquierda a derecha. Con esa preferencia, la animación no se ejecuta y el gráfico aparece ya dibujado.

## 4. Nombre, descripción y tabla

Sustituye `src/App.tsx` por el gráfico de visitas con su información accesible:

```tsx
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from './traffic';

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        id="hits"
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        label="Hits per hour over the last 24 hours"
        description="Hits fall to 9 thousand at 03:00, peak at 64 thousand at 12:00 and close the day at 20 thousand."
        dataTable="visible"
        height={200}
      />
    </main>
  );
}
```

Así queda la estructura que lee un lector de pantalla:

| Elemento | Qué lleva |
|---|---|
| El contenedor | `role="group"`, `tabindex="0"` y `aria-label` con el nombre del gráfico |
| El SVG | `role="img"`, con un `<title>` y un `<desc>` |
| La tabla | Una fila por dato, con el nombre del gráfico como `<caption>` |

`label` es el nombre accesible. Va en el `aria-label`, en el `<title>` del SVG y en el título de la tabla. El título visible de la tarjeta sigue siendo `title`. Sin `label`, el nombre accesible es el propio `title`.

`description` sustituye a la descripción que el gráfico genera. Sin ella, el gráfico escribe una a partir de sus datos. Para este gráfico sería «Hits per hour. Line chart of 24 hour values; hits ranges from 9 to 64.». Es correcta, pero no dice lo que importa: cuándo está el pico. Una descripción propia lo cuenta.

`dataTable="visible"` muestra la tabla debajo del gráfico. Por defecto existe pero está oculta a la vista, disponible para los lectores de pantalla. Las cabeceras de sus columnas son los nombres de los campos (`hour`, `hits`), así que conviene que esos nombres se entiendan.

## 5. El teclado

Cada gráfico es una parada del tabulador. Al llegar con `Tab`, se activa el primer elemento, se dibuja su marcador y aparece la lectura emergente, igual que al pasar el puntero.

| Tecla | Qué hace |
|---|---|
| Flecha derecha o abajo | El elemento siguiente |
| Flecha izquierda o arriba | El elemento anterior |
| `Home` y `End` | El primer y el último elemento |
| `Escape` | Desactiva el elemento |
| `Enter` o espacio | Selecciona el elemento activo |

En los gráficos de rejilla, como el mapa de calor, las flechas se mueven en dos dimensiones: izquierda y derecha dentro de la fila, arriba y abajo entre filas, y `Home` y `End` van al principio y al final de la fila. Los gráficos jerárquicos, como el treemap o el sunburst, siguen el patrón de árbol de WAI-ARIA: abajo y arriba recorren los nodos en profundidad, derecha baja al primer hijo e izquierda sube al padre.

El contenedor enfocado muestra un contorno con el color de la tinta. La selección con `Enter` o espacio llega al mismo evento que un clic; el artículo 11 la usa.

## 6. Lo que se anuncia

Cada gráfico tiene una región `aria-live="polite"`. Cuando cambia el elemento activo, con el puntero o con el teclado, el lector de pantalla anuncia su valor: en el gráfico de visitas, «hour 12, hits 64». En el mapa de calor anuncia la fila, la columna y el valor: «day Wed, 08-12 34». En un treemap anuncia el camino desde la raíz, el valor y la parte de su padre: «node City budget › Public works, amount 19,197, 27.7% of City budget».

La lectura emergente que se ve está marcada con `aria-hidden`, así que no se lee dos veces. El texto del anuncio y el de la tabla salen del mismo cálculo, de modo que siempre dicen lo mismo.

## 7. Contraste y tramado

Cada estilo base garantiza un contraste mínimo contra su sustrato: 4,5:1 para el texto y 3:1 para los objetos gráficos. Es una comprobación de la integración continua del proyecto: un estilo base que no la cumple no se publica. Las seis paletas incluidas también la superan. Una paleta propia puede no hacerlo; en desarrollo, la librería avisa con `SP023`, y el artículo 12 explica cómo comprobarla antes.

La otra garantía es que ningún gráfico comunica algo solo con el tramado. En la captura se ve: en modo `precision` el mapa de calor ya no tiene tono, pero cada celda sigue escribiendo su valor. El gráfico de anillo nombra cada sector con su porcentaje en la leyenda, y las barras se leen contra el eje. El tono repite lo que ya dice un número, una etiqueta o una posición, y por eso el modo `precision` no pierde información.

## 8. En Reflex

En Reflex las props son las mismas, en `snake_case`. Crea `ops_panel/ops_data.py`:

```python
SALES = [
    {"channel": "Web", "sales": 46},
    {"channel": "App", "sales": 31},
    {"channel": "Partners", "sales": 15},
    {"channel": "Phone", "sales": 8},
]

BLOCKS = ["00-04", "04-08", "08-12", "12-16", "16-20", "20-24"]

ERRORS = [
    {"day": "Mon", "values": [3, 5, 31, 38, 22, 8]},
    {"day": "Tue", "values": [2, 6, 28, 35, 20, 7]},
    {"day": "Wed", "values": [4, 7, 34, 40, 25, 9]},
    {"day": "Thu", "values": [3, 5, 29, 36, 21, 8]},
    {"day": "Fri", "values": [2, 6, 26, 30, 18, 10]},
    {"day": "Sat", "values": [1, 2, 9, 12, 10, 6]},
    {"day": "Sun", "values": [1, 1, 7, 10, 8, 5]},
]
```

Y sustituye `ops_panel/ops_panel.py`:

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart, heatmap_chart, line_chart

from .ops_data import BLOCKS, ERRORS, SALES
from .traffic import TRAFFIC


def mode_column(mode: str) -> rx.Component:
    return rx.box(
        bar_chart(
            id=f"sales-{mode}",
            data=SALES,
            x_key="channel",
            value_key="sales",
            title="Sales by channel",
            badge=mode,
            mode=mode,
        ),
        heatmap_chart(
            id=f"errors-{mode}",
            data=ERRORS,
            label_key="day",
            values_key="values",
            column_labels=BLOCKS,
            scale_max=40,
            title="Errors by day and hour",
            badge=mode,
            mode=mode,
            height=220,
        ),
        display="grid",
        gap="24px",
    )


def index() -> rx.Component:
    return rx.box(
        rx.box(
            mode_column("ink"),
            mode_column("precision"),
            display="grid",
            grid_template_columns="1fr 1fr",
            gap="24px",
        ),
        rx.box(
            line_chart(
                id="hits",
                data=TRAFFIC,
                x_key="hour",
                value_key="hits",
                title="Hits per hour",
                label="Hits per hour over the last 24 hours",
                description=(
                    "Hits fall to 9 thousand at 03:00, peak at 64 thousand at 12:00 "
                    "and close the day at 20 thousand."
                ),
                data_table="visible",
                height=200,
            ),
            max_width="640px",
        ),
        display="grid",
        gap="32px",
        max_width="1100px",
        padding="32px",
    )


app = rx.App()
app.add_page(index)
```

`mode_column` es una función normal de Python que devuelve un componente; se llama dos veces, una por modo. Lo demás funciona igual que en React: la misma estructura accesible, el mismo teclado, los mismos anuncios y el mismo modo impuesto por el sistema, porque Reflex dibuja con el componente de React.

## Comprobarlo tú mismo

* **Con el teclado.** Pulsa `Tab` hasta llegar al gráfico y recórrelo con las flechas. El marcador y la lectura deben seguir al foco.
* **Con un lector de pantalla.** NVDA o JAWS en Windows, VoiceOver en macOS y Orca en Linux anuncian el nombre al entrar y el valor de cada elemento al moverte.
* **Con más contraste.** Activa «Aumentar contraste» en tu sistema, o emula `prefers-contrast: more` en las herramientas de desarrollo. Los gráficos deben pasar a `precision` sin recargar.
* **Sin estilos.** Si ves la tabla de datos sin haber pedido `dataTable="visible"`, falta `@silverpoint/grounds/styles.css`: es la hoja que la oculta a la vista.

## Lo que viene

El artículo 11 usa el elemento activo y la selección desde tu propio código: una lectura junto al gráfico, una lista de horas seleccionadas y una descripción emergente a medida, en los cuatro frameworks.
