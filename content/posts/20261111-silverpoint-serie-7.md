Title: Silverpoint, artículo 07: las propiedades que comparten los 60 gráficos
Date: 2026-11-11 14:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_7
Authors: Ernesto Crespo
Summary: Las props comunes a todos los gráficos de silverpoint, agrupadas por función: datos, estilo, tamaño, texto de la tarjeta, accesibilidad y formato de números, con su sintaxis en React, Vue, Angular y Reflex.

Los artículos 03 a 06 dibujaron el mismo gráfico de línea en cuatro frameworks. Este cierra el nivel 1 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint) con lo que esos gráficos tienen en común: un conjunto de props que acepta cualquiera de los 60 gráficos, del de barras al sunburst.

Aprenderlas una vez sirve para todos. Lo que cambia de un gráfico a otro son sus accesores, las props que dicen qué campo de cada fila dibujar (`xKey` y `valueKey` en el gráfico de línea), y sus opciones propias. Eso lo verá cada artículo del catálogo.

## La misma prop en cuatro sintaxis

Las props se llaman igual en los cuatro adaptadores. Solo cambia cómo se escriben:

| Framework | Texto literal | Expresión |
|---|---|---|
| React | `footerLeft="Last 24 hours"` | `height={200}` |
| Vue | `footer-left="Last 24 hours"` | `:height="200"` |
| Angular | `footerLeft="Last 24 hours"` | `[height]="200"` |
| Reflex | `footer_left="Last 24 hours"` | `height=200` |

Un número, un objeto o una variable siempre van como expresión. En Vue y Angular, si escribes `height="200"` sin `:` o sin corchetes, el gráfico recibe el texto `"200"` y la comprobación de tipos falla.

Las tablas de este artículo usan el nombre de React. En Vue se pasa a kebab-case (`data-table`), en Angular es el mismo y en Reflex se pasa a snake_case (`data_table`).

## Los datos

| Prop | Qué hace |
|---|---|
| `data` | Las filas que se dibujan, un array de objetos |

Sin `data`, el gráfico dibuja su conjunto de demostración, y con un array vacío dibuja su estado vacío, «No data». Los accesores de cada gráfico (`xKey`, `valueKey`, `keys`…) se ignoran con los datos de demostración; las demás props se aplican.

## El estilo

| Prop | Valores | Por defecto |
|---|---|---|
| `ground` | `silverpoint`, `cyanotype` | `silverpoint`, o el del proveedor de la aplicación |
| `substrate` | `cream`, `green`, `blue`, `ochre` en `silverpoint`; `prussian` en `cyanotype` | El primero del ground |
| `mode` | `ink`, `precision` | `ink` |
| `palette` | Un objeto con los colores que sustituyes | Los del ground |

El ground y el sustrato son las ideas del artículo 01: el conjunto de decisiones de dibujo y el papel preparado. `mode="precision"` desactiva el entintado a mano y deja los trazos exactos. Las paletas y su comprobación de contraste tienen su propio artículo.

![El mismo gráfico con los cuatro sustratos de silverpoint, sin tarjeta y en cianotipia](./images/silverpoint-serie-7.png)

Es el mismo gráfico seis veces. Arriba y a la izquierda abajo, los cuatro sustratos del ground `silverpoint`. En el centro abajo, con `chrome="bare"`. A la derecha abajo, con `ground="cyanotype"`: líneas blancas sobre azul de Prusia.

## El tamaño y la tarjeta

| Prop | Qué hace | Por defecto |
|---|---|---|
| `height` | El alto del área de dibujo en píxeles | 160 |
| `width` | Un ancho fijo en píxeles | El del contenedor |
| `chrome` | `card` dibuja la tarjeta completa; `bare`, solo el área de dibujo | `card` |

Normalmente no se fija `width`: el gráfico mide su contenedor y se redibuja cuando cambia. Por eso un contenedor sin ancho deja el gráfico sin dibujar.

Con `chrome="bare"` desaparece todo el marco, el título incluido: es para cuando el gráfico va dentro de otra tarjeta o de un panel que ya tiene el suyo.

## El texto de la tarjeta

| Prop | Dónde aparece |
|---|---|
| `title` | El título, arriba a la izquierda |
| `badge` | Una etiqueta corta, arriba a la derecha |
| `value` | El valor destacado, bajo el título |
| `unit` | La unidad, junto al valor |
| `footerLeft` | El pie, a la izquierda |
| `footerRight` | El pie, a la derecha |

`value` acepta un número o un texto. Si es un número, se formatea con `locale` y `numberFormat`, igual que los ejes.

## La accesibilidad

| Prop | Qué hace | Por defecto |
|---|---|---|
| `label` | El nombre accesible del gráfico | El `title` |
| `description` | La descripción larga para lectores de pantalla | Una que el gráfico genera con sus datos |
| `dataTable` | La tabla con los datos: `visible`, `hidden` o `none` | `hidden` |

Cada gráfico es un SVG con su nombre y su descripción, y lleva al lado una tabla con los mismos datos. Con `hidden`, la tabla existe para las tecnologías de apoyo pero no se ve. Con `visible`, aparece debajo del gráfico. Con `none`, no se genera; úsalo solo si la página ya ofrece los datos de otra forma.

## Los números

| Prop | Qué hace |
|---|---|
| `locale` | El idioma y la región de los números, como `es-ES` o `en-US` |
| `numberFormat` | Las opciones de `Intl.NumberFormat` |

Las dos se aplican a todo lo que muestra el gráfico: el valor destacado, las marcas de los ejes y la tabla de datos. Con `locale="es-ES"` y `{ notation: 'compact' }`, 63844 se escribe «64 mil».

## El dibujo

| Prop | Qué hace | Por defecto |
|---|---|---|
| `id` | Un identificador estable | Uno generado de forma determinista |
| `seed` | La semilla del trazo a mano | Derivada de `id` |
| `hatchFill` | Cómo se rellenan las áreas: `tile` o `per-shape` | `tile` |
| `className` | Una clase CSS para la raíz del gráfico | Ninguna |

El trazo a mano no es aleatorio en cada render: sale de la semilla. El mismo gráfico con el mismo `id` se dibuja siempre igual, en el servidor y en el navegador. Si dos gráficos con los mismos datos tienen que verse distintos, dales semillas distintas. En Reflex se escribe `class_name`, como en cualquier componente de Reflex.

Los eventos, `onActiveChange` y `onSelect`, también son comunes, pero tienen su propio artículo: el 11, sobre la interacción.

## Todo junto

Las peticiones por hora del panel de operaciones, ahora sin pasarlas a miles, sobre el sustrato verde, con la tabla de datos visible y los números en español compacto. Los datos son filas como `{ hour: '12', requests: 63844 }`.

En React:

```tsx
<main style={{ maxWidth: 640 }}>
  <LineChart
    data={requests}
    xKey="hour"
    valueKey="requests"
    substrate="green"
    height={200}
    title="Requests per hour"
    badge="Today"
    value={63844}
    unit="requests at the peak"
    footerLeft="Last 24 hours"
    footerRight="Peak at 12:00"
    description="Requests to the web service per hour over the last 24 hours."
    dataTable="visible"
    locale="es-ES"
    numberFormat={{ notation: 'compact' }}
  />
</main>
```

En Vue:

```vue
<main style="max-width: 640px">
  <SpLineChart
    :data="requests"
    x-key="hour"
    value-key="requests"
    substrate="green"
    :height="200"
    title="Requests per hour"
    badge="Today"
    :value="63844"
    unit="requests at the peak"
    footer-left="Last 24 hours"
    footer-right="Peak at 12:00"
    description="Requests to the web service per hour over the last 24 hours."
    data-table="visible"
    locale="es-ES"
    :number-format="{ notation: 'compact' }"
  />
</main>
```

En Angular:

```html
<main style="max-width: 640px">
  <sp-line-chart
    [data]="requests"
    xKey="hour"
    valueKey="requests"
    substrate="green"
    [height]="200"
    title="Requests per hour"
    badge="Today"
    [value]="63844"
    unit="requests at the peak"
    footerLeft="Last 24 hours"
    footerRight="Peak at 12:00"
    description="Requests to the web service per hour over the last 24 hours."
    dataTable="visible"
    locale="es-ES"
    [numberFormat]="{ notation: 'compact' }"
  />
</main>
```

Y en Reflex:

```python
rx.box(
    line_chart(
        data=REQUESTS,
        x_key="hour",
        value_key="requests",
        substrate="green",
        height=200,
        title="Requests per hour",
        badge="Today",
        value=63844,
        unit="requests at the peak",
        footer_left="Last 24 hours",
        footer_right="Peak at 12:00",
        description="Requests to the web service per hour over the last 24 hours.",
        data_table="visible",
        locale="es-ES",
        number_format={"notation": "compact"},
    ),
    max_width="640px",
)
```

Los cuatro dibujan el mismo gráfico: «64 mil» como valor destacado, marcas como «20 mil» y «40 mil» en el eje y la tabla de 24 filas debajo. La descripción sustituye a la que el gráfico genera.

## Lo que viene

Con este artículo termina el nivel 1. Ya sabes instalar silverpoint en tu framework, pasarle tus datos y configurar cualquier gráfico con las props comunes.

El nivel 2 construye un panel con estilo propio e interacción. Empieza por el 08: cómo elegir el gráfico entre las familias del catálogo. La [referencia de props](https://silverpointweb.vercel.app/docs/react) de la documentación tiene la lista completa de cada gráfico.
