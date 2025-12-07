# Resume data module
# Contains structured data for resume sections

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
        [
            "Debian Linux Instructor for the Scada DST project"
        ],
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
        [
            "Developed Live-CD Linux for blind people"
        ],
        "Python, Debian live-cd, bash, GTK, Debian custom package",
    ],
    [
        "Team Lead",
        "AIT DST PDVSA",
        "Dec2009-Apr2010",
        [
            "Leading the Gas Pipeline Network Simulation Project in real-time"
        ],
        "Fortran, C++, GTK, postgreSQL",
    ],
    [
        "Team Lead",
        "Fundabit",
        "Jun2006-Mar2007",
        [
            "Authoring tool developed for teaching."
        ],
        None,
    ],
    [
        "Technology Advisor",
        "Fundabit",
        "Mar2005-Nov2005",
        [
            "Development of the Fundabit Educational Portal."
        ],
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
        [
            "Implemented: Email server, Proxy server, File server, Printer server, Web server"
        ],
        "Fedora, Sendmail, Squid, SquidGuard, Samba, NFS, CUPS, Apache.",
    ],
    [
        "Professor",
        "Carabobo University",
        "Mar2001-Aug2001",
        [
            "Digital Logic Laboratory"
        ],
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
        ["Climate Change Temperature by Country, Global Temperature and CO2 ppm", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Climate_change.ipynb"],
        ["Exploring Covid19 data with pandas", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/covid19-6.ipynb"],
        ["Analysis of the 25 largest retailers in the United States", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Retailers_US.ipynb"],
        ["Analysis Stanford Open Policy Project Dataset", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/police_traffic.ipynb"],
        ["Investigating Netflix Movies and Guest Stars in The Office", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Netflix.ipynb"],
    ],
    "graphs": [
        ["Matplotlib", "https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Matplotlib.ipynb"],
    ]
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
    ["Database Engine", "PostgreSQL, MySQLdb, MongoDB","DuckDB"],
]

social_media_data = [
    ["Medium", "https://seraph13.medium.com/"],
    ["LinkedIn", "https://www.linkedin.com/in/ernestocrespo/"],
    ["Twitter", "https://twitter.com/_seraph1"],
    ["GitHub", "https://github.com/ecrespo"],
    ["GitLab", "https://gitlab.com/ecrespo"],
    ["Blog", "https://blog.seraph.to"],
]