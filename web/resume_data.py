# Resume data module
# Contains structured data for resume sections

import re

education_data = ["Electrical Engineer", "Carabobo University, Venezuela", "2001"]

work_experience_data = [
    [
        "Software Engineer III - Backend Developer",
        "Asistensi Global Insurance, Inc.",
        "Jul2022-present",
        [
            "Improved 50% (backend only for now) of the engineering software process in EMS emergency management systems by developing Python Clean code validation.",
            "Reduce response times through bug fixes and support services for the medical emergency management tool.",
        ],
        "Django, Django-rest framework, PostgreSQL, MongoDB, SQL, Streamlit, Docker, AWS Lambda, Python, Pandas, Numpy, FastAPI, NestJS, Knime, Serverless framework.",
    ],
    [
        "Lead Software Engineer - Team Lead EMS",
        "Asistensi Global Insurance, Inc.",
        "Oct2021-Jul2022",
        [
            "Reduce response times through bug fixes and support services for the medical emergency management tool.",
            "Improve the medical prescription service for Asistensi clients in Mexico by 60% through the design and development of the Medikit API integration with EMS.",
        ],
        "Django, Django-rest framework, postgreSQL, Docker, AWS S3, AWS Lambda, Python, pandas, numpy.",
    ],
    [
        "Tech Coach",
        "Talently, Inc.",
        "Mar2023-Sept2023",
        [
            "As a Tech Coach, I helped several people improve their skills in Data Science, Data Engineering, and Big Data."
        ],
        "AWS Athena, AWS RedShift, PostgreSQL, Python, Pandas, NumPy, Scikit-learn, Big Data Analysis with PySpark.",
    ],
    [
        "AWS Cloud Engineer",
        "Escala24x7",
        "Aug2019-Oct2021",
        [
            "Improved customer service by 80% by developing AWS APIs and automating Escala customer service.",
            "Improved 90% of bank customer call searches by developing a data lake for Banesco's call system.",
            "Improved 80% of vehicle credit sales inquiries and customer delinquencies by developing a data lake that analyzes vehicle monitoring system data.",
        ],
        "Python, pandas, numpy, S3, DynamoDB, RDS, lambda, cloudwatch Event, SNS, SQS, AWS API, step functions, cloud training, AWS SAM, AWS Athena, AWS Glue, AWS Redshift.",
    ],
    [
        "BI Developer",
        "Troc Global",
        "Jul2018-Aug2019",
        [
            "Accelerated the decision making of the company's management through the development of modules and APIs for EDA, PCA and predictive analysis as a tool for decision making in the management of electronic and mobile equipment sales stores in Walmart establishments."
        ],
        "Python, pandas, numpy, scikit-learn, pyMC3, matplotlib, Seaborn, Django-rest framework, postgresql, and rethinkDB.",
    ],
    [
        "Senior Analyst",
        "PDVSA Oil Company",
        "May2016-Sep2018",
        [
            "Developed geochemical analysis Web application to estimate the presence of compartments in oil fields.",
            "Digital oil field proof of concept.",
            "Architecture designed for web Scada.",
        ],
        "MongoDB, PostgreSQL, Python, Flask, Pandas, numpy, sciPy",
    ],
    [
        "Maintenance Analyst",
        "PDVSA Oil Company",
        "Nov2014-Apr2016",
        [
            "Network technical support.",
            "Gasoline distribution system.",
        ],
        "Linux, Python, bash, sql",
    ],
    [
        "Technology Manager",
        "Infocentro Foundation",
        "Jan2014-Jun2014",
        [
            "Lead teams of development of administrative systems, server management, and technical support."
        ],
        "API RestFull en Django y Python(Tastypie, django-rest-framework, Eve)",
    ],
    [
        "Software Developer",
        "Cenditel",
        "Jul2011-Aug2012",
        [
            "I developed an application to send text messages from Linux using Python",
            "Live-cd for managing radio stations",
        ],
        "Debian, bash, Python, GTK, Debian live, Debian package",
    ],
    [
        "Systems Administrator",
        "0269",
        "Nov2010-May2011",
        [
            "Implementation of security services: firewalls, Proxy management and content filtering, Network monitoring, Instruction Detection System, Anti-spam gateway, VPN",
        ],
        "Iptables, bash, Python, Debian, Linux, Ntop, postfix, spamassasin, nagios, squid, squidGuard, OpenVPN and Snort",
    ],
    [
        "Linux Instructor",
        "AIT DST PDVSA",
        "Apr2010-Nov2010",
        ["Debian Linux Instructor for the Scada DST project"],
        "Debian Linux, network management.",
    ],
    [
        "Software Architect",
        "AIT DST PDVSA",
        "Apr2010-Aug2010",
        [
            "Design of new architecture for the project Simulation of Gas Pipeline Networks in real-time."
        ],
        None,
    ],
    [
        "Systems Administrator",
        "AIT DST PDVSA",
        "Jan2007-Jul2010",
        [
            "Implemented: Firewalls, VPN, file server, proxy server, Web server, Instruction Detection System"
        ],
        "Debian, Apache, Samba, Squid, SquidGuard, Nagios, Iptables and OpenVPN, Snort",
    ],
    [
        "Team Lead",
        "AIT DST PDVSA",
        "Jan2010-Jun2010",
        ["Developed Live-CD Linux for blind people"],
        "Python, Debian live-cd, bash, GTK, Debian custom package",
    ],
    [
        "Team Lead",
        "AIT DST PDVSA",
        "Dec2009-Apr2010",
        ["Leading the Gas Pipeline Network Simulation Project in real-time"],
        "Fortran, C++, GTK, postgreSQL",
    ],
    [
        "Team Lead",
        "Fundabit",
        "Jun2006-Mar2007",
        ["Authoring tool developed for teaching."],
        None,
    ],
    [
        "Technology Advisor",
        "Fundabit",
        "Mar2005-Nov2005",
        ["Development of the Fundabit Educational Portal."],
        "CMS mambo PHP, Linux, Apache, mod_security",
    ],
    [
        "Professor",
        "José Antonio Páez University",
        "Aug2002-Feb2005",
        [
            "Computer network",
            "Informatic security",
            "System administration",
        ],
        None,
    ],
    [
        "Network and Systems Administrator",
        "José Antonio Páez University",
        "Jan2002-Jul2004",
        ["Implemented: Email server, Proxy server, File server, Printer server, Web server"],
        "Fedora, Sendmail, Squid, SquidGuard, Samba, NFS, CUPS, Apache.",
    ],
    [
        "Professor",
        "Carabobo University",
        "Mar2001-Aug2001",
        ["Digital Logic Laboratory"],
        None,
    ],
    [
        "Teacher Assistant",
        "Carabobo University",
        "May1998-Aug2001",
        [
            "Computer Architecture",
            "Digital Computing I",
            "Digital Computing II",
        ],
        None,
    ],
]

portfolio_data = {
    "edas": [
        [
            "Climate Change Temperature by Country, Global Temperature and CO2 ppm",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Climate_change.ipynb",
        ],
        [
            "Exploring Covid19 data with pandas",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/covid19-6.ipynb",
        ],
        [
            "Analysis of the 25 largest retailers in the United States",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Retailers_US.ipynb",
        ],
        [
            "Analysis Stanford Open Policy Project Dataset",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/police_traffic.ipynb",
        ],
        [
            "Investigating Netflix Movies and Guest Stars in The Office",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Netflix.ipynb",
        ],
    ],
    "graphs": [
        [
            "Matplotlib",
            "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Matplotlib.ipynb",
        ],
    ],
}

skills_data = [
    ["Programming", "Python, R, Golang, Javascript, Julia, Nestjs"],
    ["Data processing/wrangling", "SQL, Pandas, Numpy, Polars, Pyspark"],
    ["Data visualization", "Matplotlib, Seaborn, Plotly, Bokeh"],
    ["Dashboard", "Streamlit, Taipy, Dash, Reflex"],
    ["Machine Learning", "scikit-learn"],
    ["Deep Learning", "TensorFlow, Keras, PyTorch"],
    ["IA", "Langchain, LangGraph, CrewAI, AutoGen, BeeAI"],
    ["Web development", "Django, FastAPI, HTML, CSS"],
    ["Model deployment", "Heroku, AWS, Digital Ocean"],
    ["Operating System", "Linux, Window, MacOs"],
    ["Low code tools", "Knime, Tableu, Power BI, N8N"],
    ["Containers", "Docker, Docker-compose, Kubernetes"],
    ["Serverless Development", "AWS Cloudformation, AWS SAM, Serverless"],
    ["Database Engine", "PostgreSQL, MySQLdb, MongoDB", "DuckDB"],
]

social_media_data = [
    ["Medium", "https://seraph13.medium.com/"],
    ["LinkedIn", "https://www.linkedin.com/in/ernestocrespo/"],
    ["Twitter", "https://twitter.com/_seraph1"],
    ["GitHub", "https://github.com/ecrespo"],
    ["GitLab", "https://gitlab.com/ecrespo"],
    ["Blog", "https://blog.seraph.to"],
]

# --------------------------------------------------------------------------- #
# Spanish
#
# The data above is the English original. `ES` maps each English text that
# changes in Spanish to its translation; `translate` falls back to the English
# text (names of companies, technologies and products stay as they are).
# --------------------------------------------------------------------------- #

ES = {
    # Education
    "Electrical Engineer": "Ingeniero Electricista",
    "Carabobo University, Venezuela": "Universidad de Carabobo, Venezuela",
    # Job titles
    "Software Engineer III - Backend Developer": "Software Engineer III - Desarrollador backend",
    "Lead Software Engineer - Team Lead EMS": "Lead Software Engineer - Líder del equipo EMS",
    "Tech Coach": "Tech Coach",
    "AWS Cloud Engineer": "Ingeniero cloud de AWS",
    "BI Developer": "Desarrollador de BI",
    "Senior Analyst": "Analista sénior",
    "Maintenance Analyst": "Analista de mantenimiento",
    "Technology Manager": "Gerente de tecnología",
    "Software Developer": "Desarrollador de software",
    "Systems Administrator": "Administrador de sistemas",
    "Linux Instructor": "Instructor de Linux",
    "Software Architect": "Arquitecto de software",
    "Team Lead": "Líder de equipo",
    "Technology Advisor": "Asesor tecnológico",
    "Professor": "Profesor",
    "Network and Systems Administrator": "Administrador de redes y sistemas",
    "Teacher Assistant": "Preparador docente",
    # Companies with a Spanish name
    "PDVSA Oil Company": "PDVSA",
    "Infocentro Foundation": "Fundación Infocentro",
    "José Antonio Páez University": "Universidad José Antonio Páez",
    "Carabobo University": "Universidad de Carabobo",
    # Responsibilities
    "Improved 50% (backend only for now) of the engineering software process in EMS emergency management systems by developing Python Clean code validation.": (
        "Mejoré en un 50 % (por ahora solo el backend) el proceso de ingeniería de software de "
        "los sistemas de gestión de emergencias EMS con el desarrollo de validación de código "
        "limpio en Python."
    ),
    "Reduce response times through bug fixes and support services for the medical emergency management tool.": (
        "Reducción de los tiempos de respuesta mediante corrección de errores y servicios de "
        "soporte para la herramienta de gestión de emergencias médicas."
    ),
    "Improve the medical prescription service for Asistensi clients in Mexico by 60% through the design and development of the Medikit API integration with EMS.": (
        "Mejora en un 60 % del servicio de recetas médicas para los clientes de Asistensi en "
        "México con el diseño y desarrollo de la integración de la API de Medikit con EMS."
    ),
    "As a Tech Coach, I helped several people improve their skills in Data Science, Data Engineering, and Big Data.": (
        "Como Tech Coach, ayudé a varias personas a mejorar sus habilidades en ciencia de datos, "
        "ingeniería de datos y big data."
    ),
    "Improved customer service by 80% by developing AWS APIs and automating Escala customer service.": (
        "Mejoré en un 80 % la atención al cliente con el desarrollo de APIs en AWS y la "
        "automatización del servicio al cliente de Escala."
    ),
    "Improved 90% of bank customer call searches by developing a data lake for Banesco's call system.": (
        "Mejoré en un 90 % las búsquedas de llamadas de clientes bancarios con el desarrollo de "
        "un data lake para el sistema de llamadas de Banesco."
    ),
    "Improved 80% of vehicle credit sales inquiries and customer delinquencies by developing a data lake that analyzes vehicle monitoring system data.": (
        "Mejoré en un 80 % las consultas de ventas a crédito de vehículos y de morosidad de "
        "clientes con el desarrollo de un data lake que analiza los datos del sistema de "
        "monitoreo vehicular."
    ),
    "Accelerated the decision making of the company's management through the development of modules and APIs for EDA, PCA and predictive analysis as a tool for decision making in the management of electronic and mobile equipment sales stores in Walmart establishments.": (
        "Agilicé la toma de decisiones de la gerencia con el desarrollo de módulos y APIs de "
        "EDA, PCA y análisis predictivo como herramienta para la gestión de tiendas de venta "
        "de equipos electrónicos y móviles en establecimientos de Walmart."
    ),
    "Developed geochemical analysis Web application to estimate the presence of compartments in oil fields.": (
        "Desarrollé una aplicación web de análisis geoquímico para estimar la presencia de "
        "compartimientos en yacimientos petroleros."
    ),
    "Digital oil field proof of concept.": "Prueba de concepto de campo petrolero digital.",
    "Architecture designed for web Scada.": "Diseño de la arquitectura de un SCADA web.",
    "Network technical support.": "Soporte técnico de redes.",
    "Gasoline distribution system.": "Sistema de distribución de gasolina.",
    "Lead teams of development of administrative systems, server management, and technical support.": (
        "Dirección de los equipos de desarrollo de sistemas administrativos, administración de "
        "servidores y soporte técnico."
    ),
    "I developed an application to send text messages from Linux using Python": (
        "Desarrollé una aplicación para enviar mensajes de texto desde Linux con Python"
    ),
    "Live-cd for managing radio stations": "Live-CD para la gestión de emisoras de radio",
    "Implementation of security services: firewalls, Proxy management and content filtering, Network monitoring, Instruction Detection System, Anti-spam gateway, VPN": (
        "Implementación de servicios de seguridad: firewalls, gestión de proxy y filtrado de "
        "contenido, monitoreo de red, sistema de detección de intrusos, pasarela antispam, VPN"
    ),
    "Debian Linux Instructor for the Scada DST project": (
        "Instructor de Debian Linux para el proyecto SCADA de DST"
    ),
    "Design of new architecture for the project Simulation of Gas Pipeline Networks in real-time.": (
        "Diseño de una nueva arquitectura para el proyecto de simulación en tiempo real de redes "
        "de gasoductos."
    ),
    "Implemented: Firewalls, VPN, file server, proxy server, Web server, Instruction Detection System": (
        "Implementé: firewalls, VPN, servidor de archivos, servidor proxy, servidor web, sistema "
        "de detección de intrusos"
    ),
    "Developed Live-CD Linux for blind people": "Desarrollé un Live-CD de Linux para personas ciegas",
    "Leading the Gas Pipeline Network Simulation Project in real-time": (
        "Dirección del proyecto de simulación en tiempo real de redes de gasoductos"
    ),
    "Authoring tool developed for teaching.": "Herramienta de autor desarrollada para la enseñanza.",
    "Development of the Fundabit Educational Portal.": "Desarrollo del portal educativo de Fundabit.",
    "Computer network": "Redes de computadoras",
    "Informatic security": "Seguridad informática",
    "System administration": "Administración de sistemas",
    "Implemented: Email server, Proxy server, File server, Printer server, Web server": (
        "Implementé: servidor de correo, servidor proxy, servidor de archivos, servidor de "
        "impresión, servidor web"
    ),
    "Digital Logic Laboratory": "Laboratorio de Lógica Digital",
    "Computer Architecture": "Arquitectura del Computador",
    "Digital Computing I": "Computación Digital I",
    "Digital Computing II": "Computación Digital II",
    # Tech stacks with English words
    "Debian Linux, network management.": "Debian Linux, gestión de redes.",
    # Notebooks
    "Climate Change Temperature by Country, Global Temperature and CO2 ppm": (
        "Cambio climático: temperatura por país, temperatura global y CO2 en ppm"
    ),
    "Exploring Covid19 data with pandas": "Exploración de datos de COVID-19 con pandas",
    "Analysis of the 25 largest retailers in the United States": (
        "Análisis de los 25 mayores minoristas de Estados Unidos"
    ),
    "Analysis Stanford Open Policy Project Dataset": (
        "Análisis del dataset del Stanford Open Policing Project"
    ),
    "Investigating Netflix Movies and Guest Stars in The Office": (
        "Películas de Netflix y estrellas invitadas en The Office"
    ),
    # Skill categories
    "Programming": "Programación",
    "Data processing/wrangling": "Procesamiento y preparación de datos",
    "Data visualization": "Visualización de datos",
    "Dashboard": "Dashboards",
    "Machine Learning": "Machine learning",
    "Deep Learning": "Deep learning",
    "IA": "IA",
    "Web development": "Desarrollo web",
    "Model deployment": "Despliegue de modelos",
    "Operating System": "Sistemas operativos",
    "Low code tools": "Herramientas low-code",
    "Containers": "Contenedores",
    "Serverless Development": "Desarrollo serverless",
    "Database Engine": "Motores de bases de datos",
    "Machine Learning/Deep Learning": "Machine learning / deep learning",
    # Short labels of the comparative radar
    "Data wrangling": "Datos",
    "Data viz": "Visualización",
    "ML / DL": "ML / DL",
    "Web dev": "Web",
    "OS": "SO",
    "Low code": "Low-code",
    "Serverless": "Serverless",
    "Databases": "Bases de datos",
}


def translate(text: str, lang: str) -> str:
    """`text` in `lang`: its Spanish translation, or the English text itself."""
    return ES.get(text, text) if lang == "es" else text


_PERIOD = re.compile(r"^([A-Za-z]+)\s*(\d{4})$")
_MONTH_NUMBERS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}  # fmt: skip


def period_text(period: str, lang: str) -> str:
    """`Jul2022-present` → `Jul 2022 – Present` / `jul 2022 – actualidad`."""
    from .i18n import MONTHS_SHORT

    def _end(part: str) -> str:
        if part.lower() == "present":
            return "Present" if lang == "en" else "actualidad"
        match = _PERIOD.match(part.strip())
        if not match or match.group(1).lower() not in _MONTH_NUMBERS:
            return part
        month = _MONTH_NUMBERS[match.group(1).lower()]
        return f"{MONTHS_SHORT[lang][month - 1]} {match.group(2)}"

    start, _, end = period.partition("-")
    return f"{_end(start)} – {_end(end)}" if end else _end(start)
