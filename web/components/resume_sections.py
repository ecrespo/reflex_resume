import reflex as rx


def section_heading(text: str) -> rx.Component:
    return rx.el.h2(
        text,
        class_name="text-3xl font-bold text-gray-800 mb-8 border-b-2 border-gray-200 pb-2",
    )


def education_section() -> rx.Component:
    return rx.el.section(
        section_heading("Education"),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Electrical Engineer", class_name="font-bold text-gray-900 text-lg"
                ),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(
                    "Carabobo University, Venezuela", class_name="italic text-gray-700"
                ),
                class_name="flex-1",
            ),
            rx.el.span("2001", class_name="text-gray-600 font-medium"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center mb-6",
        ),
        id="education",
        class_name="mb-12 scroll-mt-24",
    )


def experience_item(
    title: str,
    company: str,
    date: str,
    responsibilities: list[str],
    tech_stack: str | None = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(title, class_name="font-bold text-gray-900 text-lg"),
                rx.el.span(", ", class_name="text-gray-800"),
                rx.el.span(company, class_name="italic text-gray-700"),
            ),
            rx.el.span(date, class_name="text-gray-600 font-medium whitespace-nowrap"),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-baseline mb-3",
        ),
        rx.el.ul(
            rx.foreach(
                responsibilities,
                lambda r: rx.el.li(r, class_name="mb-1 leading-relaxed"),
            ),
            class_name="list-disc list-outside ml-5 text-gray-700 mb-4 space-y-1",
        ),
        rx.cond(
            tech_stack is not None,
            rx.el.p(
                rx.el.span("Tech Stack: ", class_name="font-semibold text-gray-800"),
                tech_stack,
                class_name="text-sm text-gray-600 bg-gray-100/50 p-3 rounded-lg",
            ),
            rx.fragment(),
        ),
        class_name="mb-10 last:mb-0",
    )


def work_experience_section() -> rx.Component:
    return rx.el.section(
        section_heading("Work Experience"),
        experience_item(
            "Software Engineer III - Backend Developer",
            "Asistensi Global Insurance, Inc.",
            "Jul2022-present",
            [
                "Improved 50% (backend only for now) of the engineering software process in EMS emergency management systems by developing Python Clean code validation.",
                "Reduce response times through bug fixes and support services for the medical emergency management tool.",
            ],
            "Django, Django-rest framework, PostgreSQL, MongoDB, SQL, Streamlit, Docker, AWS Lambda, Python, Pandas, Numpy, FastAPI, NestJS, Knime, Serverless framework.",
        ),
        experience_item(
            "Lead Software Engineer - Team Lead EMS",
            "Asistensi Global Insurance, Inc.",
            "Oct2021-Jul2022",
            [
                "Reduce response times through bug fixes and support services for the medical emergency management tool.",
                "Improve the medical prescription service for Asistensi clients in Mexico by 60% through the design and development of the Medikit API integration with EMS.",
            ],
            "Django, Django-rest framework, postgreSQL, Docker, AWS S3, AWS Lambda, Python, pandas, numpy.",
        ),
        experience_item(
            "Tech Coach",
            "Talently, Inc.",
            "Mar2023-Sept2023",
            [
                "As a Tech Coach, I helped several people improve their skills in Data Science, Data Engineering, and Big Data."
            ],
            "AWS Athena, AWS RedShift, PostgreSQL, Python, Pandas, NumPy, Scikit-learn, Big Data Analysis with PySpark.",
        ),
        experience_item(
            "AWS Cloud Engineer",
            "Escala24x7",
            "Aug2019-Oct2021",
            [
                "Improved customer service by 80% by developing AWS APIs and automating Escala customer service.",
                "Improved 90% of bank customer call searches by developing a data lake for Banesco's call system.",
                "Improved 80% of vehicle credit sales inquiries and customer delinquencies by developing a data lake that analyzes vehicle monitoring system data.",
            ],
            "Python, pandas, numpy, S3, DynamoDB, RDS, lambda, cloudwatch Event, SNS, SQS, AWS API, step functions, cloud training, AWS SAM, AWS Athena, AWS Glue, AWS Redshift.",
        ),
        experience_item(
            "BI Developer",
            "Troc Global",
            "Jul2018-Aug2019",
            [
                "Accelerated the decision making of the company's management through the development of modules and APIs for EDA, PCA and predictive analysis as a tool for decision making in the management of electronic and mobile equipment sales stores in Walmart establishments."
            ],
            "Python, pandas, numpy, scikit-learn, pyMC3, matplotlib, Seaborn, Django-rest framework, postgresql, and rethinkDB.",
        ),
        experience_item(
            "Senior Analyst",
            "PDVSA Oil Company",
            "May2016-Sep2018",
            [
                "Developed geochemical analysis Web application to estimate the presence of compartments in oil fields.",
                "Digital oil field proof of concept.",
                "Architecture designed for web Scada.",
            ],
            "MongoDB, PostgreSQL, Python, Flask, Pandas, numpy, sciPy",
        ),
        experience_item(
            "Maintenance Analyst",
            "PDVSA Oil Company",
            "Nov2014-Apr2016",
            [
                "Network technical support.",
                "Gasoline distribution system.",
            ],
            "Linux, Python, bash, sql",
        ),
        experience_item(
            "Technology Manager",
            "Infocentro Foundation",
            "Jan2014-Jun2014",
            [
                "Lead teams of development of administrative systems, server management, and technical support."
            ],
            "API RestFull en Django y Python(Tastypie, django-rest-framework, Eve)",
        ),
        experience_item(
            "Software Developer",
            "Cenditel",
            "Jul2011-Aug2012",
            [
                "I developed an application to send text messages from Linux using Python",
                "Live-cd for managing radio stations",
            ],
            "Debian, bash, Python, GTK, Debian live, Debian package",
        ),
        experience_item(
            "Systems Administrator",
            "0269",
            "Nov2010-May2011",
            [
                "Implementation of security services: firewalls, Proxy management and content filtering, Network monitoring, Instruction Detection System, Anti-spam gateway, VPN",
            ],
            "Iptables, bash, Python, Debian, Linux, Ntop, postfix, spamassasin, nagios, squid, squidGuard, OpenVPN and Snort",
        ),
        experience_item(
            "Linux Instructor",
            "AIT DST PDVSA",
            "Apr2010-Nov2010",
            [
                "Debian Linux Instructor for the Scada DST project"
            ],
            "Debian Linux, network management.",
        ),
        experience_item(
            "Software Architect",
            "AIT DST PDVSA",
            "Apr2010-Aug2010",
            [
                "Design of new architecture for the project Simulation of Gas Pipeline Networks in real-time."
            ],
            None,
        ),
        experience_item(
            "Systems Administrator",
            "AIT DST PDVSA",
            "Jan2007-Jul2010",
            [
                "Implemented: Firewalls, VPN, file server, proxy server, Web server, Instruction Detection System"
            ],
            "Debian, Apache, Samba, Squid, SquidGuard, Nagios, Iptables and OpenVPN, Snort",
        ),
        experience_item(
            "Team Lead",
            "AIT DST PDVSA",
            "Jan2010-Jun2010",
            [
                "Developed Live-CD Linux for blind people"
            ],
            "Python, Debian live-cd, bash, GTK, Debian custom package",
        ),
        experience_item(
            "Team Lead",
            "AIT DST PDVSA",
            "Dec2009-Apr2010",
            [
                "Leading the Gas Pipeline Network Simulation Project in real-time"
            ],
            "Fortran, C++, GTK, postgreSQL",
        ),
        experience_item(
            "Team Lead",
            "Fundabit",
            "Jun2006-Mar2007",
            [
                "Authoring tool developed for teaching."
            ],
            None,
        ),
        experience_item(
            "Technology Advisor",
            "Fundabit",
            "Mar2005-Nov2005",
            [
                "Development of the Fundabit Educational Portal."
            ],
            "CMS mambo PHP, Linux, Apache, mod_security",
        ),
        experience_item(
            "Professor",
            "José Antonio Páez University",
            "Aug2002-Feb2005",
            [
                "Computer network",
                "Informatic security",
                "System administration",
            ],
            None,
        ),
        experience_item(
            "Network and Systems Administrator",
            "José Antonio Páez University",
            "Jan2002-Jul2004",
            [
                "Implemented: Email server, Proxy server, File server, Printer server, Web server"
            ],
            "Fedora, Sendmail, Squid, SquidGuard, Samba, NFS, CUPS, Apache.",
        ),
        experience_item(
            "Professor",
            "Carabobo University",
            "Mar2001-Aug2001",
            [
                "Digital Logic Laboratory"
            ],
            None,
        ),
        experience_item(
            "Teacher Assistant",
            "Carabobo University",
            "May1998-Aug2001",
            [
                "Computer Architecture",
                "Digital Computing I",
                "Digital Computing II",
            ],
            None,
        ),
        id="work-experience",
        class_name="mb-12 scroll-mt-24",
    )


def portfolio_section() -> rx.Component:
    """Portfolio section with notebook links."""
    return rx.el.section(
        section_heading("Portfolio"),
        rx.el.h3(
            "Notebooks",
            class_name="text-2xl font-bold text-gray-700 mb-4",
        ),
        rx.el.h4(
            "EDAs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.el.li(
                rx.el.a(
                    "Climate Change Temperature by Country, Global Temperature and CO2 ppm",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Climate_change.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            rx.el.li(
                rx.el.a(
                    "Exploring Covid19 data with pandas",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/covid19-6.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            rx.el.li(
                rx.el.a(
                    "Analysis of the 25 largest retailers in the United States",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Retailers_US.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            rx.el.li(
                rx.el.a(
                    "Analysis Stanford Open Policy Project Dataset",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/police_traffic.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            rx.el.li(
                rx.el.a(
                    "Investigating Netflix Movies and Guest Stars in The Office",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Netflix.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        rx.el.h4(
            "Graphs",
            class_name="text-xl font-semibold text-gray-600 mb-3 mt-6",
        ),
        rx.el.ul(
            rx.el.li(
                rx.el.a(
                    "Matplotlib",
                    href="https://github.com/ecrespo/data_science_portfoliio/blob/main/notebooks/Matplotlib.ipynb",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-2",
            ),
            class_name="list-disc list-outside ml-5 text-gray-700",
        ),
        id="portfolio",
        class_name="mb-12 scroll-mt-24",
    )


def skills_list_section() -> rx.Component:
    """Skills list section (text-based)."""
    return rx.el.section(
        section_heading("Skills List"),
        rx.el.div(
            rx.el.div(
                rx.el.span("Programming: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Python`, `R`, `Golang`, `Javascript`, `Julia`, `Nestjs`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Data processing/wrangling: ", class_name="font-bold text-gray-800"),
                rx.el.code("`SQL`, `Pandas`, `Numpy`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Data visualization: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Matplotlib`, `Seaborn`, `Plotly`, `Bokeh`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Dashboard: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Streamlit`, `Taipy`, `Dash`, `Reflex`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Machine Learning: ", class_name="font-bold text-gray-800"),
                rx.el.code("`scikit-learn`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Deep Learning: ", class_name="font-bold text-gray-800"),
                rx.el.code("`TensorFlow`, `Keras`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Web development: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Django`, `FastAPI`, `HTML`, `CSS`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Model deployment: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Heroku`, `AWS`, `Digital Ocean`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Operating System: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Linux`, `Window`, `MacOs`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Low code tools: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Knime`, `Tableu`, `Power BI`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Containers: ", class_name="font-bold text-gray-800"),
                rx.el.code("`Docker`, `Docker-compose`, `Kubernetes`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Serverless Development: ", class_name="font-bold text-gray-800"),
                rx.el.code("`AWS Cloudformation`, `AWS SAM`, `Serverless`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span("Database Engine: ", class_name="font-bold text-gray-800"),
                rx.el.code("`PostgreSQL`, `MySQLdb`, `MongoDB`", class_name="text-sm text-gray-700"),
                class_name="mb-3",
            ),
            class_name="space-y-2",
        ),
        id="skills-list",
        class_name="mb-12 scroll-mt-24",
    )


def social_media_section() -> rx.Component:
    """Social media links section."""
    return rx.el.section(
        section_heading("Social Media"),
        rx.el.div(
            rx.el.div(
                rx.el.span("Medium: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://seraph13.medium.com/",
                    href="https://seraph13.medium.com/",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            rx.el.div(
                rx.el.span("LinkedIn: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://www.linkedin.com/in/ernestocrespo/",
                    href="https://www.linkedin.com/in/ernestocrespo/?locale=en_US",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            rx.el.div(
                rx.el.span("Twitter: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://twitter.com/_seraph1",
                    href="https://twitter.com/_seraph1",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            rx.el.div(
                rx.el.span("GitHub: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://github.com/ecrespo",
                    href="https://github.com/ecrespo",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            rx.el.div(
                rx.el.span("GitLab: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://gitlab.com/ecrespo",
                    href="https://gitlab.com/ecrespo",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            rx.el.div(
                rx.el.span("Blog: ", class_name="font-semibold text-gray-800 inline-block w-32"),
                rx.el.a(
                    "https://blog.seraph.to",
                    href="https://blog.seraph.to",
                    target="_blank",
                    class_name="text-blue-600 hover:text-blue-800 hover:underline",
                ),
                class_name="mb-3 flex items-start",
            ),
            class_name="space-y-1",
        ),
        id="social-media",
        class_name="mb-12 scroll-mt-24",
    )