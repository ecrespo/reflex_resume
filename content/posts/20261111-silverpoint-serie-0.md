Title: Silverpoint, artículo 0: el mapa de la serie
Date: 2026-11-11 10:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, python, Visualización
lang: es
translation: true
Slug: silverpoint_serie_0
Authors: Ernesto Crespo
Summary: Punto de partida de la serie de tutoriales sobre silverpoint: qué es, qué cubre cada uno de los 29 artículos y qué ruta seguir si usas React, Vue, Angular o Reflex.

Con este artículo empieza una serie de tutoriales sobre [silverpoint](https://github.com/ecrespo/silverpoint), una librería de gráficos y componentes de interfaz que vengo desarrollando para React, Vue, Angular y, desde Python, para Reflex.

Este es el artículo 0. No instala nada ni dibuja nada: explica qué es silverpoint, cómo está organizada la serie y qué artículos te conviene leer según el framework que uses. Si solo tienes cinco minutos, ve directo a la sección «Rutas de lectura».

## Qué es silverpoint

Silverpoint dibuja gráficos con el lenguaje visual de una técnica de dibujo histórica: la punta de plata del Renacimiento. Un sustrato preparado de tono medio, una línea fina, el tono construido con tramado y un realce en blanco reservado para el valor que importa.

![Arriba, el estilo de boceto habitual; abajo, tres gráficos de silverpoint](./images/silverpoint-serie-0.png)

Lo que la distingue de otras librerías de aspecto «dibujado a mano» es dónde vive la irregularidad: solo en el ornamento. La geometría que representa el dato es exacta, y cada gráfico tiene un modo `precision` que apaga el entintado por completo.

En su versión 0.9.2, la librería trae:

* 60 gráficos, cada uno importable por separado.
* 38 componentes de interfaz (formularios, tablas, navegación, modales) dibujados en el mismo estilo.
* Un componente `Dashboard` para componer paneles responsivos.
* Dos estilos base, `silverpoint` y `cyanotype`, y seis paletas de color con contraste verificado.
* Una línea de tiempo, presentaciones en Markdown y un servidor MCP para trabajar con asistentes de IA.

## Un paquete por framework

El motor es el mismo para todos; cambia el adaptador que instalas.

| Si usas | Instala | Requisitos |
|---|---|---|
| React | `@silverpoint/react` | React 18.2 o 19 |
| Vue | `@silverpoint/vue` | Vue 3.5 |
| Angular | `@silverpoint/angular` | Angular 21 o 22 |
| Reflex (Python) | `reflex-silverpoint-react` | Reflex 0.10, Python 3.11 |

Para adelantar cómo se ve la instalación, este es el caso de React y el de Reflex:

```sh
npm install @silverpoint/react @silverpoint/grounds @silverpoint/fonts
```

```sh
pip install reflex-silverpoint-react
```

Los cuatro adaptadores dibujan exactamente lo mismo con las mismas propiedades. Por eso la mayoría de los artículos de la serie explican un concepto una sola vez y muestran el código en los cuatro frameworks.

## Cómo está organizada la serie

Son 29 artículos en cinco niveles. Cada nivel termina con algo que ya puedes usar. Cada artículo se publica en este blog, en español y en inglés, y va acompañado de un vídeo con el mismo recorrido.

| Nivel | Artículos | Al terminar puedes |
|---|---|---|
| 0. Fundamentos | 01 y 02 | Explicar las ideas de la librería y saber qué instalar |
| 1. Primeros pasos | 03 a 07 | Dibujar un gráfico con tus propios datos |
| 2. Intermedio | 08 a 15 | Construir un panel con estilo propio e interacción |
| 3. Avanzado | 16 a 22 | Llevar el panel a una aplicación con formularios, tablas y render en servidor |
| 4. Proyectos y ecosistema | 23 a 29 | Publicar una aplicación completa y trabajar con asistentes de IA |

Toda la serie construye un mismo proyecto: un panel de operaciones de un servicio web, con tráfico por hora, errores y ventas por canal. Empieza como un solo gráfico y termina como una aplicación completa.

## La lista completa

### Nivel 0. Fundamentos

* **01.** Qué es silverpoint: gráficos con técnica de dibujo histórico.
* **02.** El mapa de paquetes: el motor, los estilos y los adaptadores.

### Nivel 1. Primeros pasos

* **03.** Tu primer gráfico en React con Vite.
* **04.** Tu primer gráfico en Vue 3.
* **05.** Tu primer gráfico en Angular.
* **06.** Tu primer gráfico en Reflex, solo con Python.
* **07.** Las propiedades que comparten los 60 gráficos.

### Nivel 2. Intermedio

* **08.** Cómo elegir el gráfico: las familias del catálogo.
* **09.** Estilos base, sustratos y el proveedor: un estilo para toda la aplicación.
* **10.** Modo `precision` y accesibilidad.
* **11.** Interacción: elemento activo, selección y descripción emergente a medida.
* **12.** Paletas y cambio de tema.
* **13.** Paneles: una rejilla responsiva definida como datos.
* **14.** Distribuciones, comparaciones e incertidumbre.
* **15.** Jerarquías, flujos y redes, con navegación por niveles.

### Nivel 3. Avanzado

* **16.** Componentes de interfaz (I): formularios y visualización.
* **17.** Componentes de interfaz (II): tablas, componentes compuestos y ventanas superpuestas.
* **18.** Exportar un gráfico a SVG.
* **19.** Render en servidor y determinismo.
* **20.** Datos en vivo y rendimiento.
* **21.** Líneas de tiempo con TimelineJS.
* **22.** Presentaciones en Markdown con gráficos vivos.

### Nivel 4. Proyectos y ecosistema

* **23.** Proyecto final en React con Next.js: el panel de operaciones de principio a fin.
* **24.** Proyecto final en Vue: el panel de operaciones de principio a fin.
* **25.** Proyecto final en Angular: el panel de operaciones de principio a fin.
* **26.** Proyecto final en Reflex: una aplicación completa en Python con datos reales.
* **27.** El mismo panel en cuatro frameworks.
* **28.** Silverpoint con IA: el servidor MCP y las habilidades para asistentes.
* **29.** Cómo se construyó silverpoint.

## Rutas de lectura

No hace falta leer los 29. Elige la ruta que corresponde a tu caso; todas empiezan en el artículo 01.

| Tu caso | Ruta corta | Para seguir |
|---|---|---|
| Desarrollas en React | 01, 03, 07, 09, 11, 13 | 16, 17, 19, 23 |
| Desarrollas en Vue | 01, 04, 07, 09, 11, 13 | 16, 17, 19, 24 |
| Desarrollas en Angular | 01, 05, 07, 09, 11, 13 | 16, 17, 19, 25 |
| Desarrollas en Python con Reflex | 01, 06, 07, 09, 11, 13 | 15, 18, 26 |
| Estás evaluando la librería | 01, 02, 08, 10 | 27 |
| Te interesa el uso con IA | 01, 28 | 08 |

La ruta corta de cada framework son seis artículos: al terminarla tienes un panel con varios gráficos, un estilo común e interacción. La columna «Para seguir» lo lleva a una aplicación completa: cada framework tiene su propio proyecto final.

Un detalle para quien viene de Python: la ruta de Reflex no toca JavaScript en ningún momento. Reflex instala los paquetes necesarios por su cuenta.

## Mientras llegan los artículos

La documentación ya está publicada y tiene una guía por framework:

* [React](https://silverpointweb.vercel.app/docs/react)
* [Vue](https://silverpointweb.vercel.app/docs/vue)
* [Angular](https://silverpointweb.vercel.app/docs/angular)
* [Reflex](https://silverpointweb.vercel.app/docs/reflex)

También puedes ver los 60 gráficos en vivo en la [galería](https://silverpointweb.vercel.app/gallery).

El siguiente artículo, el 01, entra en la idea de fondo: por qué una técnica de dibujo de hace seiscientos años sirve para leer datos hoy.
