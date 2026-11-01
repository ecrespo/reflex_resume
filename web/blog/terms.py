"""English names of the blog's categories and tags.

The posts keep their Spanish `Category:` and `Tags:` in both languages (the
translation in `content/posts_en/` copies them as they are), so the English
pages translate them here, in one place, instead of in 407 files. A term that
is not listed (a product or library name: Python, Docker, Pandas…) is the same
in both languages.
"""

CATEGORIES_EN = {
    "": "General",
    "Accesibilidad": "Accessibility",
    "Anuncio": "Announcement",
    "Anuncios": "Announcements",
    "Aplicación Android": "Android app",
    "Charla": "Talk",
    "Charla Python": "Python talk",
    "Demostración Aplicación para Android": "Android app demo",
    "Desarrollo,Movil": "Development, Mobile",
    "Evento": "Event",
    "general": "General",
    "Linux,Desarrollo": "Linux, Development",
    "Linux,Empaquetado": "Linux, Packaging",
    "Linux,Ofimatica,Desarrollo": "Linux, Office, Development",
    "Linux,Debian": "Linux, Debian",
    "Movil, Nokia": "Mobile, Nokia",
    "Resumen 2010": "2010 review",
    "Sistemas Operativos": "Operating systems",
    "Tutorial Android": "Android tutorial",
    "Tutorial Data Engineer": "Data engineering tutorial",
    "Tutorial Debian BSD y Python": "Debian, BSD and Python tutorial",
    "Tutorial Linux": "Linux tutorial",
    "Tutorial Linux y Python": "Linux and Python tutorial",
    "Tutorial Python": "Python tutorial",
    "Tutorial Python en Android": "Python on Android tutorial",
    "Tutorial Python y Linux": "Python and Linux tutorial",
    "Tutorial de Arduino": "Arduino tutorial",
    "Tutorial de Data Science": "Data science tutorial",
    "Tutorial de Docker": "Docker tutorial",
    "Tutorial de LInux": "Linux tutorial",
    "Tutorial de Linux": "Linux tutorial",
    "Tutorial de Python": "Python tutorial",
    "Tutorial de Python en Android": "Python on Android tutorial",
    "Tutorial de Python y Linux": "Python and Linux tutorial",
    "Tutorial de Python y PyQt": "Python and PyQt tutorial",
    "Tutorial de integración continua": "Continuous integration tutorial",
    "Tutorial,Desarrollo": "Tutorial, Development",
}

TAGS_EN = {
    "Accesibilidad": "Accessibility",
    "accesibilidad": "accessibility",
    "Acelerometro": "Accelerometer",
    "Análisis de Sentimiento": "Sentiment analysis",
    "Aplicaciones": "Applications",
    "Aplicación": "Application",
    "asincrono": "asynchronous",
    "Camara": "Camera",
    "Cambio Climático": "Climate change",
    "Ciencia de datos": "Data science",
    "Ciencia de Datos": "Data Science",
    "Control de versiones": "Version control",
    "Código QR": "QR code",
    "Despliegue Continuo": "Continuous deployment",
    "Dia Debian": "Debian Day",
    "Empaquetado": "Packaging",
    "Entorno Desarrollo": "Development environment",
    "Estructura de datos": "Data structures",
    "grafos": "graphs",
    "Ingeniería de Datos": "Data engineering",
    "Instalación": "Installation",
    "Integración Continua": "Continuous integration",
    "Internet de las cosas": "Internet of Things",
    "Inteligencia Aritifical": "Artificial intelligence",
    "Inteligencia Artificial": "Artificial intelligence",
    "Magnetometro": "Magnetometer",
    "Método de Montecarlo": "Monte Carlo method",
    "Nube": "Cloud",
    "Pantalla táctil": "Touchscreen",
    "Paquetes": "Packages",
    "paquetes": "packages",
    "POO": "OOP",
    "Prueba de cobertura": "Test coverage",
    "Pruebas unitarias": "Unit testing",
    "Red Neuronal": "Neural network",
    "Redes": "Networking",
    "Redes neuronales": "Neural networks",
    "Reproductor Música": "Music player",
    "Resumen": "Review",
    "Seguridad": "Security",
    "Series de Tiempo": "Time series",
    "Tareas": "Tasks",
    "Tareas periodicas": "Periodic tasks",
    "Teclado": "Keyboard",
    "tiflotecnologia": "assistive technology",
    "Visualización": "Visualization",
    "Árbol de decisión": "Decision tree",
}


def category_in(category: str, lang: str) -> str:
    """The post's category as shown in `lang`."""
    if lang == "es":
        return category or "General"
    return CATEGORIES_EN.get(category, category)


def tag_in(tag: str, lang: str) -> str:
    """A tag as shown in `lang`."""
    return tag if lang == "es" else TAGS_EN.get(tag, tag)
