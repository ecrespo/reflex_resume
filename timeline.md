# Guía para Agregar un Certificado al Timeline

Este documento describe el proceso completo para agregar un nuevo certificado o curso completado al timeline de la aplicación Reflex Resume.

## Tecnología Utilizada

El timeline utiliza **TimelineJS** de Knight Lab, una librería open-source para crear líneas de tiempo interactivas.

- Documentación oficial: [TimelineJS](https://timeline.knightlab.com/)
- Los datos se almacenan en formato JSON

---

## Estructura del Timeline

```
assets/
├── timeline.html    # Página HTML que renderiza el timeline
└── timeline.json    # Datos de los certificados (EDITAR ESTE ARCHIVO)
```

---

## Paso 1: Abrir el Archivo de Datos

El archivo a editar es:

```
assets/timeline.json
```

Este archivo contiene un objeto JSON con un array `events` que almacena todos los certificados.

---

## Paso 2: Estructura de un Certificado

Cada certificado es un objeto JSON con la siguiente estructura:

```json
{
    "start_date": {
        "year": "2024",
        "month": "12",
        "day": "14"
    },
    "media": {
        "url": "https://drive.google.com/file/d/ID_DEL_ARCHIVO/view?usp=sharing",
        "credit": "Nombre de la Plataforma"
    },
    "text": {
        "headline": "Nombre del Certificado",
        "text": "Descripción del certificado o curso"
    }
}
```

### Campos Explicados

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `start_date.year` | Año de obtención (string) | `"2024"` |
| `start_date.month` | Mes de obtención (01-12, string) | `"12"` |
| `start_date.day` | Día de obtención (01-31, string) | `"14"` |
| `media.url` | URL al certificado (preferiblemente Google Drive) | Ver ejemplo abajo |
| `media.credit` | Nombre de la plataforma/institución | `"Datacamp"`, `"Udemy"`, `"Coursera"` |
| `text.headline` | Título del certificado (visible en el timeline) | `"Machine Learning with Python"` |
| `text.text` | Descripción o texto adicional | Puede ser igual al headline |

---

## Paso 3: Agregar el Nuevo Certificado

### 3.1 Subir el Certificado a Google Drive

1. Sube el archivo PDF/imagen del certificado a Google Drive
2. Haz clic derecho → "Compartir" → "Obtener enlace"
3. Configura como "Cualquier persona con el enlace puede ver"
4. Copia el enlace

El enlace debe tener el formato:

```
https://drive.google.com/file/d/ID_DEL_ARCHIVO/view?usp=sharing
```

### 3.2 Agregar el Evento al JSON

Abre `assets/timeline.json` y agrega el nuevo objeto al array `events`.

**Importante:** Agrega el nuevo certificado al **inicio** del array para mantener el orden cronológico (más recientes primero).

### Ejemplo de ubicación

```json
{
    "events": [
        {
            "start_date": {
                "year": "2024",
                "month": "12",
                "day": "14"
            },
            "media": {
                "url": "https://drive.google.com/file/d/TU_ID_AQUI/view?usp=sharing",
                "credit": "Coursera"
            },
            "text": {
                "headline": "Tu Nuevo Certificado",
                "text": "Tu Nuevo Certificado"
            }
        },
        // ... resto de certificados existentes
    ]
}
```

---

## Paso 4: Validar el JSON

Antes de guardar, verifica que el JSON sea válido:

### Errores Comunes

1. **Coma faltante:** Cada objeto debe estar separado por coma (excepto el último)
2. **Coma extra:** No debe haber coma después del último objeto del array
3. **Comillas:** Todos los valores deben usar comillas dobles `"`, no simples `'`

### Validación Rápida

Puedes validar el JSON usando:

```bash
# Con jq (si está instalado)
cat assets/timeline.json | jq .

# Con Python
python3 -c "import json; json.load(open('assets/timeline.json'))"
```

---

## Ejemplo Completo

### Certificado de Datacamp

```json
{
    "start_date": {
        "year": "2023",
        "month": "11",
        "day": "22"
    },
    "media": {
        "url": "https://drive.google.com/file/d/1-E0m8xv8m19O3hL1hmlEz1K2kpqzf0WV/view?usp=sharing",
        "credit": "Datacamp"
    },
    "text": {
        "headline": "Data Scientist Professional with Python",
        "text": "Data Scientist Professional with Python"
    }
}
```

### Certificado de Udemy

```json
{
    "start_date": {
        "year": "2018",
        "month": "11",
        "day": "06"
    },
    "media": {
        "url": "https://drive.google.com/file/d/1AmthAXQEKmxSuIkZ9zUWmmKyowAyDuZr/view?usp=sharing",
        "credit": "Udemy"
    },
    "text": {
        "headline": "Data Science, Deep Learning and Machine learning with Python",
        "text": "Data Science, Deep Learning and Machine learning with Python"
    }
}
```

### Certificado de Platzi

```json
{
    "start_date": {
        "year": "2020",
        "month": "10",
        "day": "03"
    },
    "media": {
        "url": "https://drive.google.com/file/d/1hDg8YSjRQvQTlx5ZnBD-aTFMWQu28OGz/view?usp=sharing",
        "credit": "Platzi"
    },
    "text": {
        "headline": "Curso de Web Scraping: Extracción de Datos en la Web",
        "text": "Curso de Web Scraping: Extracción de Datos en la Web"
    }
}
```

---

## Plataformas Comunes (Credit)

Usa estos nombres para mantener consistencia:

| Plataforma | Valor de `credit` |
|------------|-------------------|
| Datacamp | `"Datacamp"` |
| Udemy | `"Udemy"` |
| Coursera | `"Coursera"` |
| Platzi | `"Platzi"` |
| EDX | `"EDX"` |
| LinkedIn Learning | `"LinkedIn Learning"` |
| Google | `"Google"` |
| AWS | `"AWS"` |
| Microsoft | `"Microsoft"` |

---

## Paso 5: Reiniciar la Aplicación

Después de modificar el archivo JSON, reinicia el servidor de Reflex:

```bash
# Detener el servidor actual (Ctrl+C)
# Reiniciar
reflex run
```

---

## Formato de Fecha

### Reglas Importantes

- **year, month, day** deben ser strings, no números
- **month** debe tener dos dígitos: `"01"` para enero, `"12"` para diciembre
- **day** debe tener dos dígitos: `"01"` a `"31"`

### Ejemplos

| Fecha | year | month | day |
|-------|------|-------|-----|
| 14 de diciembre de 2024 | `"2024"` | `"12"` | `"14"` |
| 5 de marzo de 2023 | `"2023"` | `"03"` | `"05"` |
| 22 de noviembre de 2023 | `"2023"` | `"11"` | `"22"` |

---

## Campos Opcionales Avanzados

TimelineJS soporta campos adicionales que puedes usar:

### Rango de Fechas (para cursos que duraron varios días)

```json
{
    "start_date": {
        "year": "2024",
        "month": "01",
        "day": "15"
    },
    "end_date": {
        "year": "2024",
        "month": "03",
        "day": "20"
    },
    "text": {
        "headline": "Curso de 2 meses",
        "text": "Desde enero hasta marzo"
    }
}
```

### Imagen de Fondo

```json
{
    "start_date": { ... },
    "background": {
        "url": "https://url-a-imagen.jpg",
        "color": "#f5f5dc"
    },
    "text": { ... }
}
```

---

## Solución de Problemas

### El certificado no aparece

1. Verifica que el JSON sea válido
2. Confirma que hayas guardado el archivo
3. Limpia la caché del navegador (Ctrl+F5)
4. Reinicia el servidor de Reflex

### Error al cargar el timeline

1. Revisa la consola del navegador (F12 → Console)
2. Verifica que `timeline.json` sea accesible en `/timeline.json`
3. Valida la sintaxis JSON

### El enlace del certificado no funciona

1. Verifica que el enlace de Google Drive esté configurado como público
2. Prueba el enlace directamente en el navegador
3. Asegúrate de usar el formato correcto del enlace

---

## Resumen Rápido

| Paso | Acción |
|------|--------|
| 1 | Subir certificado a Google Drive y obtener enlace público |
| 2 | Abrir `assets/timeline.json` |
| 3 | Agregar nuevo objeto JSON al inicio del array `events` |
| 4 | Llenar campos: `start_date`, `media`, `text` |
| 5 | Validar que el JSON sea correcto |
| 6 | Guardar y reiniciar Reflex: `reflex run` |
| 7 | Verificar en el timeline que aparece el nuevo certificado |

---

## Plantilla Rápida para Copiar

```json
{
    "start_date": {
        "year": "YYYY",
        "month": "MM",
        "day": "DD"
    },
    "media": {
        "url": "https://drive.google.com/file/d/ID_ARCHIVO/view?usp=sharing",
        "credit": "PLATAFORMA"
    },
    "text": {
        "headline": "NOMBRE DEL CERTIFICADO",
        "text": "NOMBRE DEL CERTIFICADO"
    }
},
```

> **Nota:** No olvides la coma al final si hay más certificados después.
