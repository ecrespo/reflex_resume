# Guía para Agregar un Nuevo Post al Blog

Este documento describe el proceso completo para agregar un nuevo artículo al blog de la aplicación Reflex Resume.

## Estructura del Blog

El blog utiliza **flexdown** para procesar archivos Markdown con metadatos estilo Pelican. Los archivos se encuentran en:

```
content/
├── posts/           # Archivos Markdown de los posts
│   ├── images/      # Imágenes locales de los posts
│   └── *.md         # Archivos de posts
└── images/          # Imágenes generales
```

---

## Paso 1: Crear el Archivo Markdown

### Nomenclatura del Archivo

Los archivos deben seguir el formato:

```
YYYYMMDD-nombre-del-post.md
```

**Ejemplos:**

- `20250812-regreso.md`
- `2024-mi-nuevo-articulo.md`

### Ubicación

Crear el archivo en:

```
content/posts/
```

---

## Paso 2: Definir los Metadatos

Los metadatos van al inicio del archivo, cada uno en una línea separada. **Debe haber una línea en blanco después de los metadatos** para separar el contenido.

### Campos Requeridos

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `Title` | Título del artículo | `Title: Mi Nuevo Artículo` |
| `Date` | Fecha y hora de publicación | `Date: 2025-12-14 10:00` |
| `Category` | Categoría del post | `Category: Python` |

### Campos Opcionales

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `Tags` | Etiquetas separadas por comas | `Tags: python, flask, api` |
| `Authors` | Autor(es) del artículo | `Authors: Ernesto Crespo` |
| `Summary` | Resumen corto del contenido | `Summary: Una introducción a...` |
| `Slug` | URL amigable personalizada | `Slug: mi-nuevo-articulo` |
| `lang` | Idioma del post | `lang: es` |
| `translation` | Si tiene traducción | `translation: true` |

### Plantilla de Metadatos

```markdown
Title: Título del Artículo
Date: 2025-12-14 10:00
Category: Python
Tags: python, flask, desarrollo
lang: es
translation: true
Slug: titulo-del-articulo
Authors: Ernesto Crespo
Summary: Breve descripción del contenido del artículo.

# Contenido del artículo aquí...
```

---

## Paso 3: Escribir el Contenido

El contenido se escribe después de la línea en blanco que sigue a los metadatos, usando sintaxis Markdown estándar.

### Sintaxis Soportada

#### Encabezados

```markdown
# Título Principal
## Subtítulo
### Sección
```

#### Texto

```markdown
**Negrita**
*Cursiva*
`código en línea`
```

#### Bloques de Código

````markdown
```python
def hola_mundo():
    print("Hola, mundo!")
```
````

#### Enlaces

```markdown
[Texto del enlace](https://ejemplo.com)
```

#### Imágenes

**Importante:** Las imágenes locales deben usar rutas relativas con `./images/`:

```markdown
![Descripción de la imagen](./images/nombre-imagen.png)
```

El sistema automáticamente convierte `./images/` a `/blog/images/` al renderizar.

---

## Paso 4: Agregar Imágenes (Opcional)

Si el post incluye imágenes locales:

1. **Ubicación:** Colocar las imágenes en `content/posts/images/`
2. **Formato:** Se recomienda PNG o JPG
3. **Referencia:** Usar la sintaxis `![alt](./images/nombre.png)`

### Ejemplo de estructura con imágenes

```
content/posts/
├── 20251214-mi-articulo.md
└── images/
    ├── diagrama-1.png
    └── captura-pantalla.jpg
```

En el archivo Markdown:

```markdown
![Diagrama explicativo](./images/diagrama-1.png)
```

---

## Paso 5: Verificar el Slug

El **slug** es el identificador único que forma la URL del post:

- URL resultante: `/blog/{slug}`

### Generación del Slug

Si no se proporciona `Slug` en los metadatos, se genera automáticamente:

1. Se toma el nombre del archivo
2. Se elimina el prefijo de fecha (ej: `20251214-`)
3. Se elimina la extensión `.md`
4. Se convierte a minúsculas

### Caracteres Válidos

El slug solo puede contener:

- Letras minúsculas (`a-z`)
- Números (`0-9`)
- Guiones (`-`)
- Guiones bajos (`_`)

Los caracteres especiales, acentos y espacios se eliminan automáticamente.

---

## Paso 6: Reiniciar la Aplicación

Después de agregar un nuevo post, reiniciar el servidor de Reflex para que se carguen los cambios:

```bash
# Detener el servidor actual (Ctrl+C)
# Reiniciar
reflex run
```

Los posts se cargan al iniciar la aplicación desde `web/blog/paths.py`.

---

## Ejemplo Completo

### Archivo: `content/posts/20251214-introduccion-reflex.md`

```markdown
Title: Introducción a Reflex Framework
Date: 2025-12-14 15:30
Category: Python
Tags: python, reflex, framework, web
lang: es
translation: true
Slug: introduccion-reflex
Authors: Ernesto Crespo
Summary: Una guía introductoria al framework Reflex para crear aplicaciones web con Python puro.

# Introducción a Reflex Framework

Reflex es un framework increíble para crear aplicaciones web usando solo Python.

## ¿Por qué Reflex?

Algunas ventajas:

- **100% Python**: Sin necesidad de JavaScript
- **Reactivo**: Estado sincronizado automáticamente
- **Flexible**: Usa cualquier librería de Python

## Ejemplo de código

```python
import reflex as rx

def index():
    return rx.text("¡Hola, Reflex!")
```

## Conclusión

Reflex simplifica el desarrollo web moderno.

![Logo de Reflex](./images/reflex-logo.png)

```

---

## Arquitectura del Sistema de Blog

```

web/blog/
├── blog.py          # Componentes y páginas del blog
└── paths.py         # Carga de posts con flexdown

web/states/
└── blog_state.py    # Estado y paginación

```

### Flujo de Carga

1. `paths.py` escanea `content/posts/*.md` al iniciar
2. Cada archivo se parsea para extraer metadatos y contenido
3. Se crea un objeto `BlogPost` por cada archivo válido
4. Los posts se ordenan por fecha (más recientes primero)
5. Se generan rutas estáticas para cada post

---

## Formatos de Fecha Soportados

El sistema reconoce automáticamente estos formatos:

| Formato | Ejemplo |
|---------|---------|
| `%Y-%m-%d %H:%M` | `2025-12-14 10:00` |
| `%Y-%m-%d` | `2025-12-14` |
| `%Y/%m/%d %H:%M` | `2025/12/14 10:00` |
| `%Y/%m/%d` | `2025/12/14` |

---

## Solución de Problemas

### El post no aparece

1. Verificar que el archivo tiene extensión `.md`
2. Confirmar que existe el campo `Title` en los metadatos
3. Reiniciar el servidor de Reflex

### Las imágenes no se muestran

1. Verificar que las imágenes están en `content/posts/images/`
2. Usar rutas relativas: `./images/nombre.png`
3. Revisar que los nombres no tengan espacios o caracteres especiales

### Caracteres raros en el slug

El sistema sanitiza automáticamente los slugs eliminando:
- Acentos y caracteres especiales
- Espacios (reemplazados por guiones)
- Caracteres no ASCII

---

## Resumen Rápido

| Paso | Acción |
|------|--------|
| 1 | Crear archivo `YYYYMMDD-nombre.md` en `content/posts/` |
| 2 | Agregar metadatos al inicio (Title, Date, Category obligatorios) |
| 3 | Escribir contenido en Markdown después de línea en blanco |
| 4 | Copiar imágenes a `content/posts/images/` si es necesario |
| 5 | Reiniciar Reflex: `reflex run` |
| 6 | Verificar en `/blog` que aparece el nuevo post |
