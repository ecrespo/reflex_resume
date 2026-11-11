Title: Silverpoint, artículo 29: cómo se construyó silverpoint
Date: 2026-11-11 23:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, IA, Visualización
lang: es
translation: true
Slug: silverpoint_serie_29
Authors: Ernesto Crespo
Summary: El último artículo de la serie cuenta cómo se hizo silverpoint con lo que guarda su repositorio: la especificación con requisitos EARS, los cambios como deltas, las decisiones de arquitectura, las puertas de CI, nueve versiones en siete semanas, el papel de los asistentes de IA y lo que costó.

Los 28 artículos anteriores explicaron cómo usar [silverpoint](https://github.com/ecrespo/silverpoint). Este, el último de la serie, cuenta cómo se hizo. No hay recuerdos en él: cada dato sale del repositorio, de sus especificaciones, de su historial de git o de su CI. Los números son del 1 de noviembre de 2026, el día de la versión 0.9.2.

## Los números

| Qué | Cuánto |
|---|---|
| Del primer commit a la 0.9.2 | Del 12 de septiembre al 1 de noviembre de 2026 |
| Commits hasta el 1 de noviembre | 250 |
| Versiones publicadas en npm | 10, de la 0.1.0 a la 0.9.2 |
| Paquetes, todos con la misma versión | 9 |
| Requisitos en el PRD | 369: 343 MUST, 23 SHOULD, 3 COULD |
| Decisiones de diseño técnico | 60, de DD-001 a DD-060 |
| Códigos de diagnóstico | 29, de `SP001` a `SP029` |
| Archivos de prueba | 237 |
| Archivos bajo `fixtures/` | 8.708 |
| Líneas del núcleo, `@silverpoint/core` | Unas 20.800 |
| Líneas de cada adaptador | 3.907 en React, 5.065 en Vue, 5.894 en Angular |

Las líneas cuentan los archivos fuente sin las pruebas, con comentarios. La diferencia entre el núcleo y los adaptadores no es casual: es la regla que más pesa en el proyecto, y está más abajo.

## Primero, la especificación

El repositorio empieza por `specs/`, no por el código. El [archivo de contexto para agentes](https://github.com/ecrespo/silverpoint/blob/main/CLAUDE.md) lo dice en su primera línea: antes de proponer o escribir código, lee la constitución.

La metodología es la que el propio repositorio llama *Spec-Driven Design*: la especificación es la verdad vigente, y el código la implementa. Son siete documentos:

| Documento | Qué fija |
|---|---|
| `constitution.md` | Nueve artículos que obligan a todo lo demás |
| `prd.md` | Qué hace la librería, como requisitos con identificador `REQ-NNN` |
| `api-spec.md` | El contrato público: paquetes, props, eventos, diagnósticos |
| `technical-design.md` | Cómo se construye: las 60 decisiones `DD-NNN` |
| `data-model.md` | La forma de los datos de cada gráfico y sus invariantes |
| `implementation-plan.md` | Las fases, de la 0 a la 10 |
| `tasks.md` | Las tareas, cada una con el requisito que cumple |

La [constitución](https://github.com/ecrespo/silverpoint/blob/main/specs/constitution.md) se ratificó el 12 de septiembre, el día del primer commit. Sus nueve artículos son las ideas que esta serie fue mostrando: la geometría de los datos es exacta (1), hay un solo motor de geometría (2), los cuatro adaptadores dibujan lo mismo (3), el render es determinista (4), hay modo `precision` y alternativa accesible (5), el tono se hace con densidad de tramado (6), los estilos base son datos (7), no se impone ningún framework de CSS (8) y la especificación es la fuente (9).

### Los requisitos en EARS

Cada requisito del [PRD](https://github.com/ecrespo/silverpoint/blob/main/specs/prd.md) se escribe con EARS (*Easy Approach to Requirements Syntax*): una plantilla según el tipo de requisito. De los 309 que no son filas del catálogo de gráficos, 189 son ubicuos (siempre se cumplen), 48 de comportamiento no deseado, 45 de evento, 23 opcionales y 4 de estado.

El artículo 28 mostró un aviso `SP002` con la etiqueta `REQ-008`. Ese es el requisito, de tipo no deseado:

> IF a datum contains `null`, `undefined` or `NaN`, THEN THE SYSTEM SHALL omit that point from the stroke, honour the declared `connectNulls` policy and warn only in development builds.

Y este, ubicuo, es el `REQ-124`, el que impide que el tramado sea la única forma de leer un dato:

> No chart SHALL encode information solely by hatch style.

Las fases 1 a 4 terminaron con una revisión de `REQ-124` gráfico por gráfico, guardada en `changes/`. La de la fase 2 lista cada canal visual de los catorce gráficos y qué dato lleva, y cada hallazgo tiene una prueba que dibuja el gráfico en `precision`, sin tramado, y lee el dato de otro canal.

### Analyze: revisar la especificación antes del código

`specs/analyze.md` es una validación cruzada de los siete documentos, de solo lectura. Su cuarta pasada, del 13 de septiembre, contó 105 requisitos, ningún identificador citado sin definir y ninguna tarea sin requisito. Y deja escrita la regla: «Analyze presents findings; approval and correction are human decisions.»

Esa pasada también registra un cambio de alcance antes de escribir código. La tercera se lanzó por una pregunta mal planteada: el framework que había que añadir era Vue, no Vite. La especificación absorbió los dos cambios seguidos, Vite como integración validada y Vue como tercer framework.

## Los cambios: deltas y funcionalidades

Una vez aprobada, la especificación no se edita a mano. Un cambio entra en `changes/` y se incorpora a `specs/` cuando se aprueba. Hay dos tamaños:

* **Deltas**, 15, para cambios a algo ya especificado. Por ejemplo, el `delta-007` amplió `SP002` a cualquier valor que un gráfico no puede dibujar tal como llega, y el `delta-015` cambió cómo el catálogo del agente fija la versión de Reflex.
* **Funcionalidades**, 6, para trabajo nuevo: el panel, los componentes de interfaz, el segundo catálogo de gráficos, los componentes compuestos, el acceso para agentes y las presentaciones.

Cada funcionalidad pasa por puertas de aprobación. La de las presentaciones, [`feature-006-deck`](https://github.com/ecrespo/silverpoint/tree/main/changes/feature-006-deck), tiene esta secuencia:

| Puerta | Documento | Qué decide |
|---|---|---|
| 0 | `research.md` | Qué hay para construir encima; Marpit medido; riesgos |
| 1 | `prd-delta.md` | El qué: los requisitos `REQ-570` a `REQ-628` |
| 2 | `api-delta.md` | El contrato: `@silverpoint/marp`, `SpDeck` en los tres adaptadores, directivas, bloques |
| PoC | `poc.md` | Cómo escalar las diapositivas en Chromium, Firefox y WebKit |
| 3 | `technical-design-delta.md` y `data-model-delta.md` | El cómo: `DD-051` a `DD-060` |
| 4 | `plan-and-tasks.md` | Las tareas `T-252` a `T-289` |

Todas se aprobaron el 31 de octubre, el mismo día en que se implementó la fase 10 y se incorporó a `specs/`. Ese día tiene 51 commits. La 0.9.0 salió al día siguiente.

## Las decisiones de arquitectura

Cuatro decisiones explican casi todo lo que la serie mostró.

**Un motor sin DOM.** Toda la geometría se calcula en `@silverpoint/core`, que no conoce el DOM ni ningún framework. Un adaptador traduce lo que da el núcleo a nodos de su framework y nada más: no calcula escalas, ejes, arcos ni trazados. La CI falla si un adaptador importa `d3-*` o `roughjs`. Por eso el núcleo tiene unas 20.800 líneas y cada adaptador entre 3.900 y 5.900. El artículo 2 de la constitución da la razón: dos implementaciones del mismo dibujo siempre acaban divergiendo.

**Los estilos base son datos.** Un estilo base es un conjunto de tokens: sustrato, tintas, parámetros del entintado, tipografía y mecanismo de tono. Añadir uno no toca el código de ningún gráfico. `cyanotype`, el segundo, llegó en la 0.2.0 con su propio mecanismo de tono: el grosor de la línea en lugar del tramado.

**Los adaptadores se comparan con un render canónico.** Cada adaptador se compara con la serialización canónica guardada con cada caso de prueba, no con los otros adaptadores. Añadir un framework cuesta una comparación, no una por pareja.

**Determinismo.** En el camino del render no hay `Math.random()` ni `Date.now()`. El trazo a mano sale de una semilla pública, derivada del `id`. Sin eso no habría comparación visual posible, ni render en servidor que coincida con el del navegador.

## Las puertas de CI

Cada push a `develop` y cada PR pasa por el [flujo de CI](https://github.com/ecrespo/silverpoint/blob/main/.github/workflows/ci.yml). La publicación vuelve a pasar todo antes de subir nada a npm. Las puertas principales:

| Puerta | Qué comprueba | Requisitos |
|---|---|---|
| Contraste | Cada tinta de cada estilo base contra cada sustrato | `REQ-126`, `REQ-127` |
| Cadena SVG | Cada adaptador contra el render canónico de cada caso, con tolerancia cero | `REQ-180` |
| Píxeles | Tres comparaciones de imagen, con umbrales fijos, en un navegador fijado por digest | `REQ-181` |
| Peso | Cada paquete dentro de su presupuesto de tamaño | `REQ-164` |
| Catálogo del agente | Se regenera sin diferencias y coincide con lo que exportan los adaptadores | `REQ-535`, `REQ-536` |
| Código generado | Los archivos de referencia de `generate_code` compilan en las aplicaciones de ejemplo | `REQ-557` |
| Trazabilidad | Cada requisito MUST tiene al menos una prueba que lo cita | `REQ-183`, `REQ-184` |

La puerta de píxeles tiene tres umbrales, escritos en la constitución: contra el render canónico del mismo commit, contra la imagen de referencia guardada y un máximo para cualquier píxel suelto. Las comparaciones solo valen con un navegador fijado, escala 1, animaciones apagadas y fuentes cargadas.

El [informe de trazabilidad](https://github.com/ecrespo/silverpoint/blob/main/reports/traceability.md) se genera de 237 archivos de prueba: 342 de los 343 MUST tienen prueba, y el que falta, `REQ-564`, está aplazado a otro repositorio. Ninguno bloquea.

El peso del trazado tiene su propio [informe](https://github.com/ecrespo/silverpoint/blob/main/reports/path-weight.md): un presupuesto de 40.000 bytes de datos de trazado por gráfico.

## La historia de versiones

![Commits por versión de silverpoint: 82 hasta la 0.1.1, 39 en la 0.2.0, 15 en la 0.3.0, 12 en la 0.6.0, 25 en la 0.7.0, 16 en la 0.8.0, 53 en la 0.9.0, 4 en la 0.9.1 y 3 en la 0.9.2](./images/silverpoint-serie-29.png)

El gráfico lo dibujó la herramienta `render_chart` del artículo 28, con los commits entre cada etiqueta y la anterior. La llamada:

```json
{"chart":"bar-chart","props":{"xKey":"release","valueKey":"commits","title":"Commits per release","footerLeft":"2026-09-12 to 2026-11-01","footerRight":"249 commits"},"data":[{"release":"0.1.1","commits":82},{"release":"0.2.0","commits":39},{"release":"0.3.0","commits":15},{"release":"0.6.0","commits":12},{"release":"0.7.0","commits":25},{"release":"0.8.0","commits":16},{"release":"0.9.0","commits":53},{"release":"0.9.1","commits":4},{"release":"0.9.2","commits":3}],"width":720,"height":280,"id":"commits","embedFonts":true}
```

Las versiones, con la fecha de npm:

| Versión | Fecha | Qué trajo |
|---|---|---|
| 0.1.0 | 25 de septiembre | El primer catálogo, 33 gráficos, en React, Vue y Angular |
| 0.1.1 | 25 de septiembre | Un README por paquete; desde aquí, se publica solo desde la CI |
| 0.2.0 | 26 de septiembre | El `Dashboard`, el estilo base `cyanotype` y `@silverpoint/tailwind` |
| 0.3.0 | 1 de octubre | Los 17 componentes de interfaz |
| 0.6.0 | 10 de octubre | El segundo catálogo: 27 gráficos más |
| 0.7.0 | 20 de octubre | Paletas, componentes compuestos, ventanas superpuestas y la línea de tiempo |
| 0.8.0 | 21 de octubre | El acceso para agentes: `@silverpoint/mcp`, el catálogo y la habilidad |
| 0.9.0 | 1 de noviembre | Las presentaciones: `@silverpoint/marp` y `SpDeck` |
| 0.9.1 | 1 de noviembre | `SpDeck` de React bajo `<StrictMode>` (issues #7 y #8) |
| 0.9.2 | 1 de noviembre | El catálogo de Reflex con `sp_deck` (issue #10) |

No hubo 0.4.0 ni 0.5.0. El segundo catálogo se hizo en tres tandas, y se decidió publicarlas juntas como 0.6.0. La 1.0.0 está aparcada a propósito: pondría en vigor la especificación de la API como contrato estable. Su conjunto de cambios espera en `changes/release-1.0.0-changeset.md`.

Desde la 0.1.1, las versiones las publica la CI con *npm Trusted Publishing* y procedencia, sin token. Los nueve paquetes comparten versión.

## El envoltorio de Reflex y la documentación

Hay dos repositorios más.

[`reflex-silverpoint-react`](https://github.com/ecrespo/reflex-silverpoint-react) empezó el 25 de septiembre y lleva diez versiones, de la 0.1.0 a la 0.9.1. Envuelve los componentes de `@silverpoint/react` como constructores de Python. Tiene una historia curiosa: las paletas, los componentes compuestos y la línea de tiempo se dibujaron primero ahí, en su 0.7, fuera del contrato de paridad. La constitución de silverpoint lo registra como la fuente del inventario de la 0.7.0, donde se reescribieron sobre el núcleo. Desde la 0.7.1 del envoltorio, son los componentes de npm detrás de los constructores.

El [sitio de documentación](https://silverpointweb.vercel.app/) está hecho en Reflex con ese mismo envoltorio ([`silverpoint_web`](https://github.com/ecrespo/silverpoint_web)). Es solo frontend: se exporta estático a Vercel, sin backend, y sus controles son componentes de silverpoint. Su `vercel.json` también publica el servidor MCP del artículo 28: reescribe `/mcp` al proyecto de Vercel que lo despliega desde `apps/mcp-vercel`.

## Los asistentes de IA

El repositorio no lo esconde. 244 de los 250 commits de silverpoint llevan la línea `Co-Authored-By` de Claude. En el envoltorio son 27 de 59, y en el sitio de documentación, 13 de 49.

La especificación explica por qué está hecha así. El artículo 9 de la constitución, el que obliga a citar un requisito en cada tarea y cada prueba, da esta razón: «the project is implemented in large part with agents; without traceability there is no way to answer why a line of code exists.»

Lo que muestran los archivos es un reparto de papeles:

* **Las decisiones son de la persona.** El archivo de contexto marca cada una con su fecha: «user decision, 2026-10-10» para publicar las tres tandas como 0.6.0, «user decision 2026-11-01» para comparar versiones por línea. Analyze presenta hallazgos; aprobarlos es decisión humana. Cada puerta de las funcionalidades tiene su fecha de aprobación.
* **El agente trabaja por tandas.** `tasks.md` lo pide: la primera tanda es de T-001 a T-004; después, revisar, ajustar y solo entonces escalar. «Do not launch all 29 unsupervised.»
* **El contexto vive en el repositorio.** El plan dice que es un proyecto de una sola persona y sin ceremonias. `tasks.md` se marca con fecha al cerrar cada tarea, para que cualquier sesión, humana o de agente, pueda seguir sin contexto previo. El archivo de contexto tiene una sección titulada «Settled decisions — do not rediscover them».
* **Una desviación detiene el trabajo.** Si el código no puede cumplir la especificación, se actualiza la especificación o se abre un delta, y solo entonces se sigue.

Las puertas de CI son la otra mitad. Un agente puede escribir código que parece correcto; la cadena SVG, los píxeles, el contraste y la trazabilidad dicen si lo es.

## Lo que costó

El repositorio también guarda lo que salió mal o costó más de lo previsto.

* **El tramado pesa.** Tramar cada forma por separado dio 913 KB para un panel de 12 tarjetas. El informe de peso lo muestra por gráfico: con tramado por forma, el mapa de calor grande ocupa 61.348 bytes, por encima del presupuesto de 40.000. La decisión fue un patrón de tramado por nivel de tono, `hatchFill: 'tile'`, que deja ese mapa en 3.909 bytes.
* **Un campo que ya existía.** `cyanotype` necesitaba un peso de línea por tono. Existía `Stroke.weight`, pero era el de la marca de objetivo del `BulletChart`, y reutilizarlo cambiaba 48 renders canónicos. Se creó un campo aparte.
* **Publicar también es código.** El publicador de confianza de `@silverpoint/mcp` en npm caducó antes de la 0.9.0, y npm respondió `E404`. La 0.8.0 de ese paquete se había publicado a mano, sin procedencia, porque aún no tenía publicador.
* **El modo estricto de React.** `SpDeck` quedaba inerte bajo `<StrictMode>`: el doble montaje destruía su controlador. Se arregló en la 0.9.1, el mismo día que la 0.9.0.
* **Lo que sigue abierto.** La revisión manual con NVDA y VoiceOver de los componentes necesita Windows o macOS y está pendiente. El flujo nocturno está desactivado. Y escribir esta serie destapó cinco issues, de la #12 a la #16, como las celdas de `SpTable` alineadas a la derecha o el SVG exportado sin su hoja de estilos.

## Fin de la serie

Aquí termina la serie. Empezó con una técnica de dibujo del Renacimiento y terminó con un servidor que dibuja gráficos para un asistente, pasando por un mismo panel de operaciones en cuatro frameworks.

Si llegaste aquí directamente, vuelve al [artículo 0](/blog/silverpoint_serie_0). Su sección «Rutas de lectura» tiene una ruta corta para cada framework, otra para evaluar la librería y otra para el uso con IA. Si ya la seguiste, la [documentación](https://silverpointweb.vercel.app/) y la [galería](https://silverpointweb.vercel.app/gallery) siguen al día con cada versión.
