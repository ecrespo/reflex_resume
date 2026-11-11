Title: Silverpoint, artículo 28: silverpoint con IA, el servidor MCP y las habilidades para asistentes
Date: 2026-11-11 23:15
Category: Tutorial Silverpoint
Tags: silverpoint, react, reflex, MCP, IA, Visualización
lang: es
translation: true
Slug: silverpoint_serie_28
Authors: Ernesto Crespo
Summary: El servidor MCP de silverpoint, alojado o local, sus 13 herramientas con llamadas y respuestas reales, y las habilidades silverpoint y reflex-silverpoint para Claude Code. Con ellos, un asistente elige, genera, comprueba y dibuja un gráfico nuevo para el panel de operaciones.

Un asistente de código que no conoce [silverpoint](https://github.com/ecrespo/silverpoint) escribe props que suenan bien y no existen: `valueKey` donde el gráfico pide `actualKey`, o un sustrato que ningún estilo base tiene. El código compila y el gráfico sale vacío.

silverpoint trae dos piezas para evitarlo. Un servidor MCP, `@silverpoint/mcp`, que responde con el catálogo de la versión que describe: qué gráfico usar, qué props tiene, qué código lo dibuja y qué falla en tus props. Y dos habilidades (*skills*) que el asistente lee antes de escribir: `silverpoint` para React, Vue y Angular, y `reflex-silverpoint` para Reflex.

Este artículo las usa para añadir un gráfico al panel de operaciones. Todas las respuestas que aparecen son las que dio el servidor alojado, con silverpoint 0.9.2.

## Lo que vas a construir

Un gráfico nuevo para el panel: el porcentaje de peticiones que cada servicio responde en menos de 300 ms, frente a su objetivo. El asistente lo elige con `recommend_chart`, escribe el código con `generate_code`, lo revisa con `validate_props` y lo dibuja con `render_chart` antes de tocar el proyecto.

![El gráfico Requests under 300 ms que devolvió render_chart: tres barras tramadas, API, Search y Checkout, con 96, 88 y 71, cada una con la marca de su objetivo](./images/silverpoint-serie-28.png)

La imagen es el SVG que devolvió `render_chart`, sin pasar por ningún framework.

## Lo que necesitas

Un cliente MCP: Claude Code, Claude, Cursor o VS Code. Para el último paso, el proyecto de React del artículo 03 o el de Reflex del 06.

## 1. El servidor: alojado o local

El servidor está alojado en `https://silverpointweb.vercel.app/mcp`. Es de solo lectura y no pide cuenta. En Claude Code se conecta así:

```sh
claude mcp add --transport http silverpoint https://silverpointweb.vercel.app/mcp
```

Si prefieres que corra en tu máquina, el mismo servidor se instala desde npm y habla por la entrada y la salida estándar (stdio):

```sh
claude mcp add silverpoint -- npx -y @silverpoint/mcp
```

Los dos exponen lo mismo. Conecté un cliente a cada uno y la lista de herramientas, recursos y prompts salió idéntica. La diferencia es la versión: el alojado describe la última publicada, y el local, la del paquete que instalaste.

La [página «Use with AI»](https://silverpointweb.vercel.app/docs/ai) de la documentación da la configuración de otros clientes:

| Cliente | Dónde |
|---|---|
| Claude | Settings → Connectors → Add custom connector, con la dirección del servidor |
| Cursor | `~/.cursor/mcp.json`, o `.cursor/mcp.json` en el proyecto |
| VS Code | `.vscode/mcp.json` |

En Cursor:

```json
{
  "mcpServers": {
    "silverpoint": {
      "url": "https://silverpointweb.vercel.app/mcp"
    }
  }
}
```

En VS Code:

```json
{
  "servers": {
    "silverpoint": {
      "type": "http",
      "url": "https://silverpointweb.vercel.app/mcp"
    }
  }
}
```

No hace falta ningún cliente para probarlo. El servidor alojado no guarda sesiones: cada petición POST es un mensaje JSON-RPC completo, así que `curl` basta:

```sh
curl -s https://silverpointweb.vercel.app/mcp \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_version","arguments":{}}}'
```

La respuesta trae, entre otras cosas, este objeto:

```json
{"version":"0.9.2","reflex":{"version":"0.9.1","wraps":"0.9.1","stale":false},"protocol":"2025-11-25"}
```

Cada respuesta del servidor lleva la versión de silverpoint que describe. `reflex` dice qué versión de `reflex-silverpoint-react` conoce el catálogo y qué versión de silverpoint envuelve. Volveremos a `stale` en la sección de las habilidades.

## 2. Las herramientas

El servidor declara 13 herramientas, todas de solo lectura (`readOnlyHint`). Esta es la lista que devuelve, con sus argumentos:

| Herramienta | Argumentos | Qué responde |
|---|---|---|
| `get_version` | ninguno | La versión de silverpoint, la del envoltorio de Reflex y la del protocolo |
| `list_charts` | `family`, `intent`, `shape` | Los gráficos, filtrados por familia, intención o forma de los datos |
| `get_chart` | `slug`, `framework` | Un gráfico: forma de los datos, campos, props con sus valores por defecto, nombre e importación |
| `list_components` | `family`, `group` | Los componentes de interfaz |
| `get_component` | `slug`, `framework` | Un componente: props, eventos, ranuras y estados |
| `recommend_chart` | `shape`, `intent`, `rows`, `fields` | Hasta cinco gráficos para una forma y una intención, con sus razones |
| `generate_code` | `target`, `framework`, `fields`, `props`, `ground`, `substrate`, `mode`, `palette` | Las importaciones, las hojas de estilo y el código de un gráfico, un componente o una presentación |
| `search_catalog` | `query`, `limit` | Una búsqueda en nombres, resúmenes, props y códigos de diagnóstico |
| `validate_props` | `chart`, `props`, `width`, `height` | Los diagnósticos que da el motor con esas props, y las props que el gráfico no declara |
| `render_chart` | `chart`, `props`, `data`, `width`, `height`, `id`, `ground`, `substrate`, `mode`, `palette`, `embedFonts` | El gráfico como un SVG autónomo |
| `check_palette` | `palette`, `substrate` | Los pares de colores de una paleta que no llegan al contraste mínimo |
| `validate_deck` | `markdown` | El número de diapositivas de una presentación y sus avisos |
| `render_deck` | `markdown`, `slide`, `ground`, `substrate`, `mode`, `palette`, `size`, `embedFonts` | La presentación como un documento HTML autónomo |

Ninguna herramienta usa un modelo de lenguaje. `recommend_chart` lee una tabla revisada, `validate_props` construye el gráfico con el motor y `render_chart` lo dibuja con el mismo código que los adaptadores. Por eso la misma pregunta da siempre la misma respuesta.

Un nombre que el catálogo no tiene es un error de la herramienta, con los nombres más cercanos. Con `get_chart` y el slug `bar-chrt`:

```json
{"version":"0.9.2","code":"unknown_name","message":"No chart named \"bar-chrt\".","suggestions":["bar-chart","area-chart","radar-chart"]}
```

## 3. Los recursos y los prompts

Además de herramientas, el servidor ofrece recursos, documentos que el cliente puede leer:

| Recurso | Qué tiene |
|---|---|
| `silverpoint://catalog` | El catálogo completo |
| `silverpoint://diagnostics` | Los códigos de diagnóstico, de `SP001` en adelante |
| `silverpoint://deck` | La referencia de las presentaciones |
| `silverpoint://charts/{slug}` | Un gráfico; hay 60 |
| `silverpoint://components/{slug}` | Un componente; hay 38 |
| `silverpoint://guides/{topic}` | Una guía en Markdown |

Las guías son 11: `choosing-charts`, `grounds-and-palettes`, `dashboard`, `ui-components`, `overlays`, `timeline`, `deck`, `react`, `vue`, `angular` y `reflex`. Son las mismas referencias que trae la habilidad `silverpoint`.

Los prompts son dos plantillas de conversación: `choose-chart`, que recibe una descripción de los datos, y `build-dashboard`, que recibe el framework y los gráficos.

## 4. Elegir el gráfico

Los datos del gráfico nuevo son tres filas, una por servicio:

```json
[{"service":"API","fast":96,"objective":95},{"service":"Search","fast":88,"objective":95},{"service":"Checkout","fast":71,"objective":90}]
```

`fast` es el porcentaje de peticiones respondidas en menos de 300 ms, y `objective`, el objetivo de ese servicio. En el vocabulario del catálogo, la forma de los datos es `categories` (una fila por categoría) y la intención es `progress` (cuánto falta para una meta). Esa es la pregunta para `recommend_chart`:

```json
{"shape":"categories","intent":"progress","rows":3}
```

La respuesta:

| Gráfico | Puntuación | Razón |
|---|---|---|
| `bullet-chart` | 0.9 | Each bar against its own target. |
| `radial-rings` | 0.75 | Concentric rings, each swept to its percent. |
| `funnel-chart` | 0.7 | Stages that narrow, such as a conversion. |
| `radial-arc-group` | 0.5 | Tracks swept relative to the largest. |
| `gauge-arc` | 0.15 | Serves progress, with its data reshaped. |

`bullet-chart` dibuja una barra por fila con una marca en su objetivo. `get_chart` con el slug `bullet-chart` dice qué campos lee:

| Papel | Prop | Tipo | Obligatorio |
|---|---|---|---|
| `title` | `titleKey` | `string` | Sí |
| `actual` | `actualKey` | `number` | Sí |
| `target` | `targetKey` | `number` | Sí |

Y su resumen: «One bar per target, with a marker at the target. Values in 0-100.» Los porcentajes del panel caben en esa escala. Con `"framework":"reflex"`, la misma respuesta da el nombre del constructor, `bullet_chart`, y las props en Python, como `title_key`.

## 5. Generar el código

`generate_code` recibe el gráfico, el framework, el campo de tus filas que corresponde a cada papel y las props:

```json
{"target":{"chart":"bullet-chart"},"framework":"react","fields":{"title":"service","actual":"fast","target":"objective"},"props":{"title":"Requests under 300 ms"}}
```

Devolvió las importaciones, las hojas de estilo y este código:

```tsx
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import { BulletChart } from '@silverpoint/react/bullet-chart';

export function BulletChartView({ rows }: { rows: readonly Record<string, unknown>[] }) {
  return (
    <BulletChart
      data={rows}
      titleKey="service"
      actualKey="fast"
      targetKey="objective"
      title="Requests under 300 ms"
    />
  );
}
```

Con una nota: «The rows are the `rows` prop: plain objects, one per datum, read through the accessor props.» Lo usé tal cual en el proyecto de React, con las filas tipadas:

```tsx
import { BulletChartView } from './BulletChartView';

type ServiceLatency = { service: string; fast: number; objective: number };

const latency: ServiceLatency[] = [
  { service: 'API', fast: 96, objective: 95 },
  { service: 'Search', fast: 88, objective: 95 },
  { service: 'Checkout', fast: 71, objective: 90 },
];

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <BulletChartView rows={latency} />
    </main>
  );
}
```

Las filas se declaran con `type`, no con `interface`: un `type` es asignable a `Record<string, unknown>`, y una `interface` no.

Con `"framework":"reflex"` y los mismos campos y props, devolvió:

```python
import reflex as rx
from reflex_silverpoint_react import bullet_chart


class State(rx.State):
    rows: list[dict] = []


def bullet_chart_view() -> rx.Component:
    return bullet_chart(
        data=State.rows,
        title_key="service",
        actual_key="fast",
        target_key="objective",
        title="Requests under 300 ms",
    )
```

Y dos notas: «`State` is a placeholder name: merge its fields into your own state class.» y «Fill `State.rows` with the rows, a list of dicts, from an event handler.» Siguiendo la segunda, este es el archivo completo del proyecto de Reflex:

```python
import reflex as rx
from reflex_silverpoint_react import bullet_chart


LATENCY = [
    {"service": "API", "fast": 96, "objective": 95},
    {"service": "Search", "fast": 88, "objective": 95},
    {"service": "Checkout", "fast": 71, "objective": 90},
]


class State(rx.State):
    rows: list[dict] = []

    @rx.event
    def load(self):
        self.rows = LATENCY


def bullet_chart_view() -> rx.Component:
    return bullet_chart(
        data=State.rows,
        title_key="service",
        actual_key="fast",
        target_key="objective",
        title="Requests under 300 ms",
    )


def index() -> rx.Component:
    return rx.box(bullet_chart_view(), max_width="640px", padding="32px")


app = rx.App()
app.add_page(index, on_load=State.load)
```

Los dos proyectos compilaron y dibujaron el gráfico con `data-status="ready"`, y la descripción accesible fue la misma en los dos: «Requests under 300 ms. Bullet chart of 3 targets on a 0 to 100 scale; 1 of 3 reach their target.»

## 6. Comprobar las props

Ahora el error del principio. Las props de abajo tienen dos fallos: `actualKey` apunta a `fast_pct`, un campo que las filas no tienen, y sobra `valueKey`, que es la prop del gráfico de línea:

```json
{"chart":"bullet-chart","props":{"data":[{"service":"API","fast":96,"objective":95},{"service":"Search","fast":88,"objective":95},{"service":"Checkout","fast":71,"objective":90}],"titleKey":"service","actualKey":"fast_pct","targetKey":"objective","valueKey":"fast","title":"Requests under 300 ms"}}
```

`validate_props` devolvió `"valid": false`, `"unknownProps": ["valueKey"]` y tres diagnósticos `SP002`, uno por fila. El primero:

```text
[SP002] BulletChart: a value cannot be drawn as given (null, not finite, or outside the data contract); it is corrected or omitted (`fast_pct`). Row 0 has no finite value; its bar is omitted. Check the value against the chart's data contract (Data Model §2). (REQ-008)
```

Cada diagnóstico trae su código, su gravedad (`warn`), el requisito de la especificación que lo define (`REQ-008`) y qué hacer. Con `"actualKey":"fast"` y sin `valueKey`, la respuesta fue `"valid": true`, sin diagnósticos y con `unknownProps` vacío.

En React, TypeScript habría marcado `valueKey`. El campo `fast_pct` no lo marca nadie: es un texto válido, y el gráfico simplemente no dibuja las barras. Esa clase de error es la que `validate_props` encuentra.

## 7. Dibujar antes de escribir

`render_chart` dibuja el gráfico sin ningún framework:

```json
{"chart":"bullet-chart","props":{"titleKey":"service","actualKey":"fast","targetKey":"objective","title":"Requests under 300 ms"},"data":[{"service":"API","fast":96,"objective":95},{"service":"Search","fast":88,"objective":95},{"service":"Checkout","fast":71,"objective":90}],"width":640,"height":200,"id":"under-300","embedFonts":true}
```

Devolvió un SVG de 640 × 260 píxeles, sin diagnósticos: el alto de 200 es el del área de dibujo, y el resto es la tarjeta. Es la imagen del principio del artículo. El SVG es autónomo: lleva la hoja del estilo base en un `<style>` y, con `embedFonts`, la fuente EB Garamond dentro. Su raíz tiene `role="img"` y `aria-labelledby`, que apunta a un `<title>` y a un `<desc>` con ids que empiezan por `under-300`, el `id` de la llamada.

Le sirve al asistente para mirar el gráfico antes de escribir el código, y a ti para meter un gráfico en un documento o en un correo.

## 8. Paletas y presentaciones

`check_palette` revisa el contraste de una paleta sobre un sustrato. Con un preset, `{"palette":"verdigris"}`, no hay hallazgos. Con una paleta propia con el texto secundario demasiado claro:

```json
{"palette":{"ink":"#2C6355","textMuted":"#A8B8B2"},"substrate":"cream"}
```

La respuesta:

```json
{
  "version": "0.9.2",
  "findings": [
    {
      "pair": "text-muted",
      "foreground": "#A8B8B2",
      "background": "#EDE7DA",
      "ratio": 1.68,
      "threshold": 4.5
    }
  ],
  "substrate": "#EDE7DA"
}
```

`#A8B8B2` sobre el crema da 1.68 a 1, y el mínimo para texto es 4.5. Con `"textMuted":"#3E6A5E"`, el color de `verdigris`, no hay hallazgos.

`validate_deck` hace lo mismo con una presentación del artículo 22. Esta tiene dos errores, un sustrato que no existe y un gráfico mal escrito:

````markdown
---
ground: silverpoint
substrate: chalk
---

# Operations

---

## Errors by hour

```silverpoint
{"chart":"bar-chrt","data":[{"hour":"10","errors":9},{"hour":"11","errors":8},{"hour":"12","errors":11}],"props":{"xKey":"hour","valueKey":"errors"}}
```
````

La respuesta:

```json
{
  "version": "0.9.2",
  "valid": false,
  "total": 2,
  "diagnostics": [
    {
      "code": "SP027",
      "severity": "warn",
      "req": "REQ-586",
      "message": "Slide 1: substrate \"chalk\" is not a substrate of any registered ground; the inherited value holds.",
      "todo": "Use a registered ground, one of its substrates, and `ink` or `precision`",
      "slide": 1
    },
    {
      "code": "SP026",
      "severity": "warn",
      "req": "REQ-591",
      "message": "Chart fence on slide 2: unknown chart \"bar-chrt\". Did you mean \"bar-chart\"?",
      "todo": "Fix the fence: a JSON object whose `chart` is a catalog slug, with props the chart declares",
      "slide": 2,
      "slot": "s2-c1"
    }
  ]
}
```

Con `green` y `bar-chart`, la respuesta fue `"valid": true`, con 2 diapositivas y sin diagnósticos.

## 9. Las habilidades

Una habilidad es una carpeta con un `SKILL.md` y sus referencias, que el asistente carga cuando la tarea lo pide. Sirve sin el servidor: tiene las mismas tablas en Markdown.

| Habilidad | Para | Dónde está |
|---|---|---|
| `silverpoint` | React, Vue y Angular | [`skills/silverpoint`](https://github.com/ecrespo/silverpoint/tree/main/skills/silverpoint) en el repositorio de silverpoint |
| `reflex-silverpoint` | Reflex | [`skills/reflex-silverpoint`](https://github.com/ecrespo/reflex-silverpoint-react/tree/main/skills/reflex-silverpoint) en el repositorio de `reflex-silverpoint-react` |

En Claude Code, cada una se instala como un plugin que trae la habilidad y conecta el servidor alojado en un paso:

```text
/plugin marketplace add ecrespo/silverpoint
/plugin install silverpoint@silverpoint
```

```text
/plugin marketplace add ecrespo/reflex-silverpoint-react
/plugin install reflex-silverpoint@reflex-silverpoint
```

La habilidad `silverpoint` describe silverpoint 0.9.2. Su `SKILL.md` da el flujo de trabajo (elegir el gráfico, leer su entrada, escribir el código, comprobarlo) y las reglas que más fallan: las props se llaman igual en los tres frameworks, cada gráfico se importa desde su propia ruta, sin `data` el gráfico dibuja sus filas de demostración y el disparador de una ventana superpuesta es un `<button>` nativo. En `references/` hay una guía por framework, una por familia de gráficos, los componentes, los estilos base y las paletas, el panel, la línea de tiempo, las presentaciones, los diagnósticos y los errores comunes.

La habilidad `reflex-silverpoint` describe `reflex-silverpoint-react` 0.9.1. Añade lo que solo existe en Python: los constructores en snake_case, los patrones de `rx.State` y los datos que llegan a los manejadores de eventos.

Las dos se generan, no se escriben a mano. El texto de `silverpoint` sale de sus plantillas y del catálogo del agente, el mismo que lee el servidor; la cabecera de cada referencia dice que se regenera con `pnpm --filter @silverpoint/agent-catalog generate`. La de Reflex sale de `scripts/make_skill.py` y del catálogo del paquete, `reflex-catalog.json`.

Las dos dicen lo mismo: si el servidor está conectado, usa sus herramientas antes que los archivos.

### Nombres de Reflex desactualizados

El servidor conoce los nombres de Reflex porque el catálogo de silverpoint incorpora `reflex-catalog.json`. Pero los dos paquetes se publican por separado, y el catálogo puede quedarse con una versión anterior del envoltorio. `get_version` lo dice con `reflex.stale`.

`stale` es `true` cuando el envoltorio envuelve otra línea de versiones: el código compara solo los dos primeros números. Hoy el servidor describe silverpoint 0.9.2 y conoce `reflex-silverpoint-react` 0.9.1, que envuelve 0.9.1. Las dos son de la línea 0.9, así que `stale` es `false`.

La habilidad de Reflex da la regla: si `stale` es `true`, o si `reflex.version` no es la versión que instala tu proyecto, los nombres de Python del servidor describen otra versión, y mandan la habilidad y los archivos `.pyi` del paquete instalado.

Lo mismo vale para las habilidades instaladas como plugin: se actualizan cuando actualizas el plugin. Si la cabecera del `SKILL.md` que tienes dice otra versión que la de tu proyecto, actualízalo.

## Problemas comunes

* **El asistente no usa las herramientas.** Comprueba que el servidor aparece en la lista de servidores MCP de tu cliente y pídele que lo use.
* **`curl` devuelve 405.** El servidor alojado solo acepta POST: GET y DELETE responden 405, porque no hay sesiones.
* **Una herramienta responde con `unknown_name`.** El slug no existe en esa versión; la respuesta trae los más cercanos.
* **El código de Reflex usa un nombre que tu versión no tiene.** Mira `reflex.stale` y `reflex.version` en `get_version`, y compara con tu `.pyi`.
* **El SVG de `render_chart` sale con otra letra.** Sin `embedFonts`, el SVG nombra EB Garamond con una serif de respaldo, y donde la fuente no está instalada se ve la de respaldo. Pasa `"embedFonts":true`.

## Lo que viene

El servidor y las habilidades describen la librería a partir de un catálogo que se genera del código. Esa forma de trabajar, especificación primero y todo lo demás generado y comprobado, es el tema del último artículo de la serie: el [29, cómo se construyó silverpoint](/blog/silverpoint_serie_29).
