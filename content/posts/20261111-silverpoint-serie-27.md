Title: Silverpoint, artículo 27: el mismo panel en cuatro frameworks
Date: 2026-11-11 23:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, nextjs, vue, angular, reflex, Visualización
lang: es
translation: true
Slug: silverpoint_serie_27
Authors: Ernesto Crespo
Summary: La aplicación Operations de los artículos 23 a 26 comparada en React con Next.js, Vue, Angular y Reflex: cuánto código pide, qué dependencias añade, cuánto pesa, cuánto tarda en compilar y en dibujar, y qué resultó más fácil o más difícil en cada framework.

Los artículos 23 a 26 construyen la misma aplicación con [silverpoint](https://github.com/ecrespo/silverpoint) en cuatro frameworks: React con Next.js, Vue, Angular y Reflex. Las tres páginas son las mismas, con los mismos datos y las mismas comprobaciones en el navegador. Eso permite compararlas con números.

Este artículo no elige un ganador. Cada cifra depende de decisiones que no son de silverpoint: el empaquetador, el renderizado en el servidor o dónde vive el estado. Lo útil es saber qué cuesta cada cosa y por qué.

![La página Overview de la aplicación Operations en los cuatro frameworks](./images/silverpoint-serie-27.png)

Arriba, React con Next.js y Vue. Abajo, Angular y Reflex. Son capturas reales de cada proyecto, con el puntero sobre una hora del gráfico de visitas. Reflex tiene un gráfico más, debajo de lo que se ve: los tiempos de respuesta medidos de verdad.

## Lo que construye cada artículo

| Artículo | Framework | Proyecto |
|---|---|---|
| [23](/blog/silverpoint_serie_23) | React con Next.js 16 | App Router, Turbopack, páginas prerrenderizadas |
| [24](/blog/silverpoint_serie_24) | Vue 3 | Vite y vue-router |
| [25](/blog/silverpoint_serie_25) | Angular 22 | CLI, router, componentes independientes y signals |
| [26](/blog/silverpoint_serie_26) | Reflex 0.10 | Python, con tiempos de respuesta reales medidos por el backend |

Las tres páginas:

* **Overview.** El panel con dos indicadores, las visitas por hora en vivo, los errores por hora enlazados por `hour`, el mapa de calor de errores por día y el donut de ventas por canal. Debajo, la hora activa y el botón que descarga el gráfico de visitas en SVG.
* **Incidents.** Las 12 incidencias del artículo 17 en una tabla ordenable y paginada, con el modal para confirmarlas y el aviso.
* **Settings.** El formulario de la regla de alerta del artículo 16 y el tema: una paleta y un interruptor de cianotipia que cambian toda la aplicación.

Las cuatro usan silverpoint 0.9.2, salvo Reflex: reflex-silverpoint-react 0.9.1 trae su propia copia de `@silverpoint/react` 0.9.1.

## El mismo panel en cuatro sintaxis

El panel de Overview es el mismo componente en las cuatro. En React:

```tsx
<Dashboard
  id="ops"
  title="Operations"
  description="Traffic, errors and sales of the web service today."
  layout={layout}
  link={{ key: 'hour' }}
  ground={settings.ground}
  palette={palette}
>
```

En Vue:

```vue
<SpDashboard
  id="ops"
  title="Operations"
  description="Traffic, errors and sales of the web service today."
  :layout="layout"
  :link="{ key: 'hour' }"
  :ground="theme.ground"
  :palette="theme.palette"
>
```

En Angular:

```html
<sp-dashboard
  id="ops"
  title="Overview"
  description="Traffic, errors and sales of the web service, updated every 2 seconds."
  [layout]="layout"
  [link]="{ key: 'hour' }"
  [ground]="settings.ground()"
  [palette]="settings.palette()"
>
```

Y en Reflex, los argumentos con nombre al final de la llamada a `dashboard(...)`:

```python
id="ops",
title="Operations",
description="Traffic, errors and sales of the web service today.",
layout=LAYOUT,
link="hour",
ground=ThemeState.ground,
palette=ThemeState.palette,
```

Las cuatro pasan `ground` y `palette` al panel, además de ponerlos en el proveedor. El marco del panel no lee el proveedor: sus gráficos sí, pero sin esas dos props el fondo y el título del panel se quedan en crema con la cianotipia. Es un fallo abierto como [silverpoint#17](https://github.com/ecrespo/silverpoint/issues/17); se corregirá en una próxima versión del paquete.

## Cuánto código

Líneas no vacías que escribí, comentarios incluidos. No cuentan los archivos que genera cada plantilla ni los datos de la serie, que son los mismos en las cuatro:

| | React · Next.js | Vue | Angular | Reflex |
|---|---|---|---|---|
| Código propio | 514 | 473 | 582 | 609 |
| Con los datos | 590 | 549 | 658 | 670 |
| Archivos de código | 16 | 12 | 13 | 10 |

Las cuatro cifras están cerca. Lo que las separa:

* **Vue** es la más corta. `v-model` funciona con todos los controles de silverpoint, y un `reactive()` de módulo basta como almacén.
* **Angular** escribe la plantilla y los estilos dentro de cada componente, así que sus líneas los incluyen.
* **Reflex** hace algo más: 46 líneas miden los tiempos de respuesta de tres sitios reales con httpx, y el panel muestra un séptimo gráfico con ellos. Sin eso, queda en unas 560.
* **React** reparte el código entre componentes de servidor y de cliente. Cada página es un archivo de servidor pequeño que monta un componente de cliente.

## Las dependencias

| | Añadidas sobre la plantilla |
|---|---|
| React · Next.js | `@silverpoint/react`, `@silverpoint/core`, `@silverpoint/grounds`, `@silverpoint/fonts` |
| Vue | `vue-router` y `@silverpoint/core` |
| Angular | `@silverpoint/core` |
| Reflex | `reflex`, `reflex-silverpoint-react` y `httpx` |

Ninguna necesitó una librería de estado. En Vue y Angular, `@silverpoint/core` ya estaba instalado como dependencia del adaptador; se declara porque la aplicación importa sus paletas y sus tipos.

## Cuánto pesa

Todo el JavaScript de la compilación de producción, comprimido con gzip. Paso todas las cifras a kB (1000 bytes), porque cada proyecto las midió con su herramienta:

| | JS (gzip) | CSS (gzip) | Prerrenderizado |
|---|---|---|---|
| React · Next.js | 327 kB | 16 kB | Sí, con los gráficos dibujados |
| Vue | 97 kB | 16 kB | No |
| Angular | 161 kB | 15 kB | No |
| Reflex | 219 kB | 17 kB | Sí, con los gráficos dibujados |

Lo que explica las diferencias:

* **Next.js** lleva su propio enrutador y React, y además una parte que no debería: `SilverpointProvider` solo se exporta desde la entrada general de `@silverpoint/react`, que contiene los 60 gráficos, y Turbopack no descarta los que no se usan. Sustituir el proveedor por un componente vacío bajó el JavaScript unos 80 kB con gzip. Es un fallo abierto como [silverpoint#21](https://github.com/ecrespo/silverpoint/issues/21); se corregirá en una próxima versión del paquete.
* **Vue** con Vite descarta los gráficos que no usas y separa cada página en su propio archivo. La primera visita a `/` descarga unos 98 kB con el CSS.
* **Angular** carga cada página aparte con `loadComponent`. La primera visita a `/` descarga unos 157 kB con el CSS.
* **Reflex** añade su cliente de estado y el socket que lo conecta con el backend.

El CSS es casi igual en las cuatro: es sobre todo la hoja de estilos de los estilos base y la de los componentes. Las tres fuentes EB Garamond suman otros 75 kB.

## Cuánto tarda

En mi equipo, en local, sin limitar la red. Mediana de tres medidas:

| | Compilación de producción | Servidor de desarrollo, en frío | Primer gráfico listo (producción) |
|---|---|---|---|
| React · Next.js | 7,6 s | 3,8 s hasta servir la primera página | 25 ms |
| Vue | 3,4 s | 0,3 s hasta estar listo | 288 ms |
| Angular | 4 s | 3,2 s hasta servir la primera página | 235 ms |
| Reflex | 3,7 s | 2,7 s hasta responder frontend y backend | 294 ms |

* **El primer gráfico de Next.js** llega dibujado en el HTML. Dentro de `Dashboard`, los gráficos de cliente reciben su tamaño de la celda, así que el prerrenderizado estático los dibuja. Vue y Angular los dibujan en el navegador. `reflex export` también los prerrenderiza, menos el de tiempos de respuesta, que espera al backend; los 294 ms de Reflex se midieron con `reflex run --env prod`.
* **Vite** arranca casi al instante porque no compila nada hasta que pides una página. Su primera página tarda algo más.
* **Reflex** en desarrollo tarda alrededor de 1 s en dibujar. En producción baja a 294 ms.

Las cifras sirven para comparar entre sí, no como promesa: en una red real pesa más el tamaño que el tiempo en local.

## Dónde vive el estado

| | El tema y la regla | La ventana en vivo | Al cambiar de página |
|---|---|---|---|
| React · Next.js | Un contexto de cliente en el diseño común | Un intervalo en la página | Next guarda las tres últimas páginas ocultas; la ventana se pausa y sigue |
| Vue | Un `reactive()` de módulo | Un intervalo en la página | La página se desmonta; la ventana vuelve a empezar |
| Angular | Servicios raíz con signals | Un servicio raíz | La ventana sigue corriendo |
| Reflex | El estado en el servidor, por pestaña | Una tarea de fondo | Reflex cancela la tarea y la vuelve a lanzar al volver |

Next.js oculta las páginas que dejas con `display: none`. En desarrollo, sus gráficos miden 0 px y avisan con `SP003` aunque no pasa nada malo. Es un fallo abierto como [silverpoint#22](https://github.com/ecrespo/silverpoint/issues/22); se corregirá en una próxima versión del paquete.

## El tema en toda la aplicación

El proveedor colorea los gráficos y los componentes de silverpoint, pero no la página: no añade ningún elemento al DOM. Las cuatro resuelven el fondo y el texto de la página por su cuenta, con las mismas propiedades `--sp-*`:

| | El proveedor que cambia | El fondo de la página |
|---|---|---|
| React · Next.js | `SilverpointProvider` con valores del contexto | `paletteStyle` como objeto de estilo |
| Vue | `SilverpointProvider` con valores reactivos | `paletteStyle` en un elemento propio |
| Angular | `SILVERPOINT_CONFIG` propio, con getters que leen signals | La clase del estilo base y `paletteStyle` |
| Reflex | `silverpoint_provider` con variables de estado | Colores calculados en el estado |

Angular es el caso difícil: `provideSilverpoint` recibe un objeto fijo. El artículo 25 lo resuelve dando `SILVERPOINT_CONFIG` con getters, algo que la documentación de silverpoint no cubre.

## Lo más fácil y lo más difícil en cada uno

| | Lo más fácil | Lo más difícil |
|---|---|---|
| React · Next.js | Páginas prerrenderizadas con los gráficos dibujados, y el estado se conserva al navegar | Exportar el SVG: Turbopack no tiene `?raw` y pide una regla con una ruta relativa |
| Vue | `v-model` en todos los controles, `aria-current` gratis en `RouterLink` | Pintar la página con la cianotipia, que no tiene paleta propia |
| Angular | Servicios con signals como almacén, `[(open)]` y `[(value)]` directos a los signals | El tema en el proveedor, y `ng serve` con la hoja de estilos importada como texto |
| Reflex | Datos reales sin API ni CORS: el backend ya existe | Cada interacción es un viaje al servidor, y `rx.App(style=...)` no se aplica sin `RadixThemesPlugin` |

Dos fallos más de silverpoint aparecieron solo en Angular: el texto literal `title="…"` queda como atributo y el navegador muestra su propia descripción emergente ([silverpoint#18](https://github.com/ecrespo/silverpoint/issues/18)), e importar la hoja de estilos como texto rompe `ng serve` ([silverpoint#19](https://github.com/ecrespo/silverpoint/issues/19)). Los dos se corregirán en una próxima versión del paquete.

## Cuál elegir

silverpoint no decide por ti: los 60 gráficos, las props y los componentes son los mismos en los cuatro adaptadores, y el código del panel cambia solo de sintaxis.

* **Si tu equipo ya usa uno de los cuatro**, quédate con él. Ninguna diferencia de esta tabla justifica cambiar de framework por los gráficos.
* **Si el peso de la página importa más que nada**, Vue con Vite dio el paquete más pequeño.
* **Si la primera vista tiene que llegar dibujada**, Next.js prerrenderiza los gráficos dentro de un panel.
* **Si los datos están en Python**, Reflex evita escribir una API: el panel lee el estado del backend.

## Lo que viene

El [artículo 28](/blog/silverpoint_serie_28) deja los frameworks y trabaja con asistentes de IA: el servidor MCP de silverpoint y sus habilidades, con llamadas y salidas reales.
