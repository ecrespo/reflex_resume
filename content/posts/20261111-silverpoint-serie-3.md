Title: Silverpoint, artículo 03: tu primer gráfico en React con Vite
Date: 2026-11-11 12:00
Category: Tutorial Silverpoint
Tags: silverpoint, react, Visualización
lang: es
translation: true
Slug: silverpoint_serie_3
Authors: Ernesto Crespo
Summary: Paso a paso, de un proyecto vacío de Vite al primer gráfico de silverpoint en React: instalación, hojas de estilos, datos propios, el texto de la tarjeta y la carga de datos desde un JSON.

Con este artículo empieza el nivel 1 de la serie sobre [silverpoint](https://github.com/ecrespo/silverpoint): los primeros pasos. Los artículos 03, 04, 05 y 06 construyen exactamente el mismo gráfico, cada uno en un framework. Este es el de React, con Vite.

Si todavía no has leído el [artículo 02](/blog/silverpoint_serie_2), el mapa de paquetes, no hace falta: aquí se instala todo desde cero.

## Lo que vas a construir

El proyecto de la serie es un panel de operaciones de un servicio web. Su primera pieza es un gráfico de línea con las visitas por hora durante las últimas 24 horas, en miles:

![El gráfico de visitas por hora que se construye en este artículo](./images/silverpoint-serie-3.png)

Al terminar tendrás el gráfico con tus propios datos, con el texto de la tarjeta (título, valor destacado, pie) y cargando los datos desde un archivo JSON, como harías con una API.

## Lo que necesitas

* Node.js 20.19 o posterior, o 22.12 o posterior. Es lo que pide Vite 8.
* npm, que viene con Node.
* Un editor. No hace falta experiencia previa con silverpoint, pero sí saber lo básico de React: componentes, props y `useState`.

## 1. Crear el proyecto

Vite crea un proyecto de React con TypeScript en un solo comando:

```sh
npm create vite@latest ops-panel -- --template react-ts --no-interactive
cd ops-panel
npm install
```

La opción `--no-interactive` evita que el asistente de Vite haga preguntas. Sin ella, puede ofrecerte instalar y arrancar el proyecto; si lo hace, responde que no y sigue con estos pasos.

## 2. Instalar silverpoint

Tres paquetes: el adaptador de React, los estilos base y la tipografía.

```sh
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
```

El adaptador trae el motor, `@silverpoint/core`, como dependencia. El artículo 02 explica qué hace cada paquete.

## 3. Preparar el punto de entrada

Las hojas de estilos de silverpoint se importan una sola vez, en el archivo de entrada. Sustituye el contenido de `src/main.tsx` por este:

```tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@silverpoint/fonts/fonts.css';
import '@silverpoint/grounds/styles.css';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

La plantilla de Vite trae estilos de demostración que no necesitamos. Sustituye `src/index.css` por unas pocas reglas para la página:

```css
body {
  margin: 0;
  padding: 32px;
  background: #f4f1ea;
}
```

Y borra `src/App.css` y la carpeta `src/assets`, que solo usaba la página de bienvenida de Vite.

## 4. El primer gráfico

Sustituye `src/App.tsx` por esto:

```tsx
import { LineChart } from '@silverpoint/react/line-chart';

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart title="Hits per hour" />
    </main>
  );
}
```

Arranca el servidor de desarrollo:

```sh
npm run dev
```

Y abre `http://localhost:5173`. Verás un gráfico de línea con doce horas y dos series: la línea continua y una línea base punteada.

Esos datos no son tuyos. Cuando un gráfico no recibe la prop `data`, dibuja su propio conjunto de demostración. Sirve para comprobar que la instalación funciona antes de escribir una sola línea de datos. Si ves el gráfico con el fondo crema y el trazo fino, las hojas de estilos y la tipografía están bien cargadas.

Fíjate en la importación: `@silverpoint/react/line-chart`. Cada gráfico tiene su propia ruta, así que tu aplicación solo incluye los que usas.

## 5. Tus propios datos

Crea `src/traffic.ts` con las visitas de un día, una fila por hora:

```ts
export type HourlyTraffic = {
  hour: string;
  hits: number;
};

export const traffic: HourlyTraffic[] = [
  { hour: '00', hits: 18 },
  { hour: '01', hits: 14 },
  { hour: '02', hits: 11 },
  { hour: '03', hits: 9 },
  { hour: '04', hits: 11 },
  { hour: '05', hits: 16 },
  { hour: '06', hits: 24 },
  { hour: '07', hits: 33 },
  { hour: '08', hits: 42 },
  { hour: '09', hits: 51 },
  { hour: '10', hits: 58 },
  { hour: '11', hits: 62 },
  { hour: '12', hits: 64 },
  { hour: '13', hits: 61 },
  { hour: '14', hits: 59 },
  { hour: '15', hits: 58 },
  { hour: '16', hits: 57 },
  { hour: '17', hits: 52 },
  { hour: '18', hits: 47 },
  { hour: '19', hits: 41 },
  { hour: '20', hits: 30 },
  { hour: '21', hits: 26 },
  { hour: '22', hits: 22 },
  { hour: '23', hits: 20 },
];
```

Un detalle de TypeScript: el tipo de la fila se declara con `type`, no con `interface`. La prop `data` acepta filas de tipo `Record<string, unknown>`, y una `interface` no es compatible con ese tipo. Si usas `interface`, la compilación falla con el error «Index signature for type 'string' is missing in type 'HourlyTraffic'».

Ahora pasa los datos al gráfico y completa la tarjeta. Sustituye `src/App.tsx`:

```tsx
import { LineChart } from '@silverpoint/react/line-chart';
import { traffic } from './traffic';

const peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));

export default function App() {
  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        value={peak.hits}
        unit="k hits at the peak"
        footerLeft="Last 24 hours"
        footerRight={`Peak at ${peak.hour}:00`}
        height={200}
      />
    </main>
  );
}
```

Vite recarga la página sola. Las props que acabas de usar:

| Prop | Qué hace |
|---|---|
| `data` | Las filas que se dibujan |
| `xKey` | El campo de cada fila que va en el eje horizontal |
| `valueKey` | El campo con el valor que dibuja la línea |
| `title` | El título de la tarjeta |
| `badge` | Una etiqueta corta, arriba a la derecha |
| `value` y `unit` | El valor destacado y su unidad, bajo el título |
| `footerLeft` y `footerRight` | El pie de la tarjeta |
| `height` | El alto del área de dibujo en píxeles; por defecto, 160 |

El ancho no se indica: el gráfico toma el de su contenedor, aquí el `<main>` de 640 píxeles.

Hay un detalle visual que conviene entender. El punto realzado en blanco está al final de la línea, no en el pico. Es la regla del realce único del artículo 01: en un gráfico de línea, el elemento realzado es el valor vivo, el último de la serie. El pico lo cuentan el valor destacado y el pie.

## 6. Cargar los datos desde un JSON

En un panel real los datos llegan de una API. Para simularlo, crea `public/traffic.json` con el formato típico de una API de métricas: una marca de tiempo y el número de peticiones.

```json
[
  {"time": "2026-11-11T00:00:00Z", "requests": 17800},
  {"time": "2026-11-11T01:00:00Z", "requests": 13937},
  {"time": "2026-11-11T02:00:00Z", "requests": 11074},
  {"time": "2026-11-11T03:00:00Z", "requests": 8811},
  {"time": "2026-11-11T04:00:00Z", "requests": 10948},
  {"time": "2026-11-11T05:00:00Z", "requests": 16085},
  {"time": "2026-11-11T06:00:00Z", "requests": 23822},
  {"time": "2026-11-11T07:00:00Z", "requests": 32959},
  {"time": "2026-11-11T08:00:00Z", "requests": 42096},
  {"time": "2026-11-11T09:00:00Z", "requests": 50833},
  {"time": "2026-11-11T10:00:00Z", "requests": 57970},
  {"time": "2026-11-11T11:00:00Z", "requests": 62107},
  {"time": "2026-11-11T12:00:00Z", "requests": 63844},
  {"time": "2026-11-11T13:00:00Z", "requests": 60981},
  {"time": "2026-11-11T14:00:00Z", "requests": 59118},
  {"time": "2026-11-11T15:00:00Z", "requests": 57855},
  {"time": "2026-11-11T16:00:00Z", "requests": 56992},
  {"time": "2026-11-11T17:00:00Z", "requests": 52129},
  {"time": "2026-11-11T18:00:00Z", "requests": 46866},
  {"time": "2026-11-11T19:00:00Z", "requests": 41003},
  {"time": "2026-11-11T20:00:00Z", "requests": 30140},
  {"time": "2026-11-11T21:00:00Z", "requests": 25877},
  {"time": "2026-11-11T22:00:00Z", "requests": 22014},
  {"time": "2026-11-11T23:00:00Z", "requests": 20151}
]
```

Vite sirve lo que hay en `public/` tal cual, así que el archivo queda disponible en `/traffic.json`. Sustituye `src/App.tsx` por la versión que lo carga:

```tsx
import { useEffect, useState } from 'react';
import { LineChart } from '@silverpoint/react/line-chart';
import type { HourlyTraffic } from './traffic';

type ApiRow = { time: string; requests: number };

const toHourly = (rows: ApiRow[]): HourlyTraffic[] =>
  rows.map((row) => ({
    hour: row.time.slice(11, 13),
    hits: Math.round(row.requests / 1000),
  }));

export default function App() {
  const [traffic, setTraffic] = useState<HourlyTraffic[] | null>(null);

  useEffect(() => {
    fetch('/traffic.json')
      .then((response) => response.json())
      .then((rows: ApiRow[]) => setTraffic(toHourly(rows)));
  }, []);

  if (!traffic) {
    return <p>Loading…</p>;
  }

  const peak = traffic.reduce((max, row) => (row.hits > max.hits ? row : max));

  return (
    <main style={{ maxWidth: 640 }}>
      <LineChart
        data={traffic}
        xKey="hour"
        valueKey="hits"
        title="Hits per hour"
        badge="Today"
        value={peak.hits}
        unit="k hits at the peak"
        footerLeft="Last 24 hours"
        footerRight={`Peak at ${peak.hour}:00`}
        height={200}
      />
    </main>
  );
}
```

Tres decisiones de esta versión:

* **Los datos se adaptan antes de llegar al gráfico.** La función `toHourly` convierte cada fila de la API en una fila del gráfico: la hora sale de la marca de tiempo y las peticiones pasan a miles. El gráfico no sabe nada de la API, y `src/traffic.ts` se queda solo con el tipo.
* **Mientras no hay datos, no hay gráfico.** El componente muestra «Loading…» hasta que llega la respuesta. No le pases un array vacío: un gráfico con `data={[]}` dibuja su estado vacío, «No data», y no los datos de demostración.
* **El gráfico se redibuja solo.** Cuando `setTraffic` cambia el estado, React vuelve a renderizar y silverpoint dibuja las nuevas filas. Si mañana cargas los datos cada minuto, no hay que hacer nada más.

## 7. Compilar para producción

```sh
npm run build
npm run preview
```

`npm run build` comprueba los tipos con TypeScript y genera la versión de producción en `dist/`. Con este proyecto, el JavaScript ocupa unos 316 kB, 101 kB comprimido con gzip, incluido React. La hoja de estilos ocupa 7,5 kB, y las tres variantes de EB Garamond, unos 25 kB cada una. `npm run preview` sirve esa versión en `http://localhost:4173` para comprobarla.

## Problemas comunes

* **La línea aparece rellena de negro y hay texto suelto debajo del gráfico.** Falta `@silverpoint/grounds/styles.css`. Sin esa hoja de estilos, los trazos no tienen color y la tabla de datos, que debería estar oculta para lectores de pantalla, se ve.
* **El gráfico no aparece.** El contenedor no tiene ancho, por ejemplo un elemento en una fila flexible sin tamaño. El gráfico espera a poder medirlo y, en desarrollo, la consola muestra el diagnóstico `SP003`. Dale un ancho al contenedor.
* **La tarjeta dice «No data».** El nombre de `xKey` o de `valueKey` no coincide con los campos de las filas. En desarrollo, la consola muestra `SP002` con el nombre del campo que no encontró.
* **La compilación falla con «Index signature … is missing».** El tipo de la fila está declarado con `interface`. Cámbialo por `type`.

Los diagnósticos `SP0xx` solo aparecen en desarrollo. En producción, la librería no escribe en la consola.

## Lo que viene

Ya tienes un gráfico de silverpoint en React con tus propios datos. Los artículos 04, 05 y 06 construyen este mismo gráfico en Vue, Angular y Reflex. Si usas React, puedes saltar al 07: las propiedades que comparten los 60 gráficos, con las que ajustarás este y cualquier otro.

La [guía de React](https://silverpointweb.vercel.app/docs/react) de la documentación tiene más ejemplos.
