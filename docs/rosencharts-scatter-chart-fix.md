# Prompt: arreglar los ejes de `scatter_chart` en reflex-rosencharts

> Copia este documento completo como prompt en una sesión abierta sobre el repositorio de
> **reflex-rosencharts**. Describe el problema detectado en `reflex_resume` (página
> `/dev-stats`, sección "Sprints and marathons"), la causa en el código y el resultado
> esperado.

---

## Estado

**Resuelto en reflex-rosencharts 0.2.2**, ya aplicado en `reflex_resume`:
- **Ejes:** se calculan desde la extensión de los datos, con marcas regulares y margen.
- **Orden de los datos:** ya no hace falta ordenarlos.
- **Escalas y margen:** hay props `x_scale`/`y_scale` y `margin_left`.
- **Parche CSS:** se eliminó el de `web/web.py`.

**Resuelto en reflex-rosencharts 0.2.3: margen izquierdo automático.** En 0.2.2,
`axisMarginLeft` calculaba `longitud × 7px + 10px` (31px para 3 dígitos). Como la etiqueta lleva
`pr-2` (8px), al texto le quedaban 23px y ticks como `500` o `180` se partían en dos líneas.
La 0.2.3 cambia el cálculo y blinda las etiquetas:
- 8px por carácter, 4px para los separadores y 12px de relleno.
- `whitespace-nowrap` en las etiquetas.

`reflex_resume` fijaba `margin_left="46px"` como parche; se retiró con la 0.2.3. Medido en la
página: margen de 36px, 28px disponibles para el texto frente a 23,3px del número más ancho,
sin etiquetas partidas a 1440px ni a 390px.

**Pendiente en `line_chart_pulse`: solape de etiquetas del eje X en móvil.** Solo se etiquetan el
primer punto, el último y el máximo. En pantallas estrechas el máximo (junio 2026) y el último
(septiembre 2026) quedan tan cerca que se solapan ("6/19/1" a 390px). Arreglo propuesto: omitir
la etiqueta del máximo cuando esté a menos de su ancho de la del último o del primer punto, o
usar marcas regulares con `responsiveTickCount` como en `scatter_chart`.

---

## Contexto

`reflex-rosencharts` (versión publicada **0.2.1**) envuelve los componentes de rosencharts
(D3 + Tailwind) como componentes de Reflex. El gráfico de dispersión vive en:

- `reflex_rosencharts/components/scatter/scatter_chart.tsx` (implementación)
- `reflex_rosencharts/components/scatter/scatter_chart.py` (wrapper `ScatterChart`, `NoSSRComponent`)

Esquema de datos: `list[{"revenue": float, "value": float, "company": str}]`, donde
`revenue` es el eje X, `value` el eje Y y `company` la etiqueta del tooltip.

Con datos reales, que están agrupados y tienen valores extremos, el gráfico tiene cuatro defectos.
La app consumidora solo puede disimularlos manipulando los datos, así que hay que corregirlos
en el componente.

## Datos para reproducir

Días de vida (`revenue`) contra número de commits (`value`) de 13 repositorios:

```python
data = [
    {"company": "omagnome", "revenue": 1, "value": 53},
    {"company": "reflex-mapcn", "revenue": 1, "value": 38},
    {"company": "mcp-joke-server", "revenue": 1, "value": 34},
    {"company": "fastapi_todos", "revenue": 16, "value": 43},
    {"company": "vigia-eew", "revenue": 19, "value": 46},
    {"company": "quiz", "revenue": 28, "value": 47},
    {"company": "prismal", "revenue": 143, "value": 440},
    {"company": "python-android_sms", "revenue": 229, "value": 138},
    {"company": "ecrespo-localpaquetes", "revenue": 273, "value": 46},
    {"company": "reflex_resume", "revenue": 287, "value": 50},
    {"company": "python-autoaccesibilidad", "revenue": 403, "value": 49},
    {"company": "tutorial_fastAPI", "revenue": 1409, "value": 45},
    {"company": "pysms-send", "revenue": 2345, "value": 29},
]
```

Para el caso extremo, añade `{"company": "ecrespo.github.io", "revenue": 2609, "value": 1451}`.

## Defectos y causa

### 1. Las etiquetas del eje X son puntos de los datos, no marcas regulares

```tsx
{data.map((d, i) => {
  const isFirst = i === 0;
  const isLast = i === data.length - 1;
  if (!isFirst && !isLast && i % 5 !== 0) return null;
  // ... renderiza {d.revenue} en left: xScale(d.revenue)%
})}
```

Se etiquetan el índice 0, uno de cada cinco y el último. Con los datos de arriba salen
`1`, `28`, `403` y `2345`:

- **Saltos irregulares:** el eje no se puede leer como escala.
- **Solape:** en una escala 1–2345, `1` y `28` quedan a un 1 % de distancia y se leen como `128`.
- **Dependencia del orden y de la cantidad de datos:** las etiquetas cambian si cambia cualquiera de los dos.

En cambio, las líneas verticales de la rejilla ya usan `xScale.ticks(8)`, así que la rejilla y
las etiquetas no coinciden.

### 2. El dominio X se toma del primer y último elemento, no del mínimo y máximo

```tsx
let xScale = scaleLinear()
  .domain([data[0].revenue, data[data.length - 1].revenue])
  .range([0, 100]);
```

El componente depende de que los datos lleguen ordenados de forma ascendente por `revenue`. Si
no, el eje sale roto. Las bandas invisibles del tooltip, que se calculan con
`data[index - 1]` y `data[index + 1]`, también tienen anchos negativos. Además, el dominio no
tiene margen: el punto con el X máximo queda pegado al borde derecho y se corta a la mitad.

### 3. El dominio Y no deja margen arriba

```tsx
let yScale = scaleLinear()
  .domain([(min(data.map((d) => d.value)) ?? 0) - 1, (max(data.map((d) => d.value)) ?? 0) + 1])
  .range([100, 0]);
```

El `±1` es absoluto, así que con valores de cientos es despreciable. El punto con el Y máximo
(prismal, 440) queda en el borde superior y el círculo (`strokeWidth="10"`) se corta. Tampoco
se aplica `.nice()`, por lo que las marcas no llegan al extremo y el valor más alto no tiene
etiqueta de referencia.

### 4. El margen izquierdo fijo de 25px no cabe en etiquetas de 3 o más dígitos

```tsx
"--marginLeft": "25px",
```

Las etiquetas del eje Y, como `400` o `1000`, se parten en dos líneas. `reflex_resume` lo
parchea por CSS global con
`.dev-stats-page [style*="--marginLeft"] { --marginLeft: 46px !important; }`. El mismo
margen fijo aparece en los gráficos de línea.

## Cambios requeridos

1. **Eje X con marcas regulares.** Genera las etiquetas con
   `xScale.ticks(n).map(xScale.tickFormat(n, ...))`, igual que la rejilla, para que
   etiquetas y líneas coincidan.
   - **Número de marcas:** limítalo según el ancho disponible, para que no se solapen en móvil.
   - **Extremos:** conserva el ajuste de `translateX` para que la primera y la última etiqueta no se salgan del área.
2. **Dominios desde mínimo y máximo, con margen y `.nice()`.**
   - X: `extent(data, d => d.revenue)` más un margen proporcional (p. ej. 5 % del rango), luego `.nice()`.
   - Y: lo mismo con `d.value`. El margen tiene que ser proporcional al rango y suficiente para que el círculo completo quepa dentro del área.
   - Datos con un solo punto, o con todos los valores iguales: evita un dominio de ancho cero.
3. **No depender del orden de entrada.** Ordena una copia de los datos por `revenue` antes de
   calcular las bandas del tooltip, o calcula las bandas sobre la copia ordenada. No mutes la
   prop.
4. **Margen izquierdo configurable o calculado.** Expón una prop (p. ej. `margin_left`) o
   calcula el margen a partir de la etiqueta Y más larga, para no depender de CSS externo.
   Revisa si los gráficos de línea necesitan el mismo cambio.
5. **Opcional:** una prop `x_scale` / `y_scale` con `"linear" | "log"` para datos con valores
   extremos, usando `scaleLog` o `scaleSymlog` si hay ceros. Documenta el comportamiento con
   valores ≤ 0.

Mantén el esquema de datos (`revenue`/`value`/`company`) y la apariencia actual: colores, rejilla
discontinua y tooltip. La API de Python debe seguir siendo compatible: cualquier prop nueva
tiene que ser opcional y con un valor por defecto que no rompa los usos existentes.

## Criterios de aceptación

- [ ] Con los datos de arriba, el eje X muestra marcas regulares (p. ej. `0, 500, 1000, 1500, 2000, 2500`) sin solapes a 1440px ni a 390px de ancho.
- [ ] Ningún punto queda cortado: prismal (Y máximo) y pysms-send (X máximo) se ven completos.
- [ ] El eje Y tiene una marca en o por encima del valor máximo, y ninguna etiqueta se parte en dos líneas.
- [ ] Mezclar los datos (orden aleatorio) produce exactamente el mismo gráfico y tooltips que funcionan.
- [ ] Datos con un solo punto y datos vacíos no rompen el render (vacío: contenedor del mismo tamaño, como hoy).
- [ ] El conjunto por defecto (`DEFAULT_DATA`) se sigue viendo igual o mejor.
- [ ] Hay una nueva versión publicada en PyPI (p. ej. `0.2.2`) con el cambio anotado en el changelog.

## Después de publicar, en reflex_resume

1. Sube la dependencia en `pyproject.toml` (`reflex-rosencharts>=0.2.2`) y ejecuta `uv lock`.
2. Si hay prop de margen, quita el parche CSS `.dev-stats-page [style*="--marginLeft"]` de
   `web/web.py`.
3. Decide si ecrespo.github.io vuelve a la gráfica: está en `REPO_LIFECYCLE_EXCLUDED` en
   `web/dev_stats_data.py`. Con escala logarítmica podría volver sin aplastar al resto.
4. Quita de `web/dev_stats_data.py` la advertencia sobre el orden obligatorio de
   `REPO_LIFECYCLE`, y de `specs/dev-stats-page.md` la nota de pendientes.
5. Comprueba `/dev-stats` en escritorio y móvil antes de desplegar.
