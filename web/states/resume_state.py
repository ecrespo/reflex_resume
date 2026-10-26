import reflex as rx

from ..resume_data import translate

# Skill levels per category, 1 to 5: the radar charts of the Resume page.
SKILL_LEVELS = {
    "Programming": {"Python": 5, "R": 3, "Golang": 4, "Javascript": 3, "Julia": 3, "Nestjs": 2},
    "Data processing/wrangling": {
        "SQL": 5,
        "Pandas": 5,
        "Numpy": 5,
        "Polars": 3,
        "Pyspark": 3,
        "DuckDB": 3,
    },
    "Data visualization": {"Matplotlib": 5, "Seaborn": 5, "Plotly": 5, "Bokeh": 4},
    "Dashboard": {"Streamlit": 4, "Dash": 2, "Taipy": 1, "Reflex": 5, "GRadio": 3},
    "Machine Learning/Deep Learning": {
        "scikit-learn": 5,
        "TensorFlow": 1,
        "Keras": 1,
        "Pytorch": 4,
    },
    "IA": {"Langchain": 5, "LangGraph": 5, "CrewAI": 4, "AutoGen": 1, "BeeAI": 1},
    "Web development": {"Django": 4, "FastAPI": 5, "Flask": 2, "HTML": 3, "CSS": 3},
    "Operating System": {"Linux": 5, "Window": 3, "MacOs": 2},
    "Low code tools": {"Knime": 4, "Tableu": 2, "Power BI": 1, "N8N": 5},
    "Containers": {"Docker": 5, "Docker-compose": 5, "Kubernetes": 1},
    "Serverless Development": {"AWS Cloudformation": 4, "AWS SAM": 4, "Serverless": 3},
    "Database Engine": {"PostgreSQL": 5, "MySQLdb": 3, "MongoDB": 5},
}


class ResumeState(rx.State):
    """Resume state with skills data and mobile menu control."""

    # Mobile menu state
    mobile_menu_open: bool = False

    def toggle_mobile_menu(self):
        """Toggle mobile menu state."""
        self.mobile_menu_open = not self.mobile_menu_open

    def close_mobile_menu(self):
        """Close mobile menu."""
        self.mobile_menu_open = False

    @rx.event
    def set_mobile_menu_open(self, value: bool):
        """Follow the drawer when it closes itself (Escape, backdrop, close button)."""
        self.mobile_menu_open = value

    # Skills data structure for radar charts
    skills_data = SKILL_LEVELS

    # Currently selected skill category
    selected_skill: str = "Programming"

    def set_selected_skill(self, skill: str):
        """Update the selected skill category."""
        self.selected_skill = skill

    @rx.var
    def skill_categories(self) -> list[str]:
        """Get list of skill categories."""
        return list(self.skills_data.keys())

    @rx.var
    def current_skill_data(self) -> dict:
        """Get data for currently selected skill."""
        return self.skills_data.get(self.selected_skill, {})

    # Shorter axis labels for the 12-axis comparative radar, where the full
    # category names would overlap.
    category_short_labels = {
        "Data processing/wrangling": "Data wrangling",
        "Data visualization": "Data viz",
        "Machine Learning/Deep Learning": "ML / DL",
        "Web development": "Web dev",
        "Operating System": "OS",
        "Low code tools": "Low code",
        "Serverless Development": "Serverless",
        "Database Engine": "Databases",
    }

    @rx.var
    def current_skill_radar(self) -> list[dict]:
        """Selected category as radar data: one axis per skill."""
        return [
            {"topic": name, "value": level}
            for name, level in self.skills_data.get(self.selected_skill, {}).items()
        ]

    @rx.var
    def category_average_radar(self) -> list[dict]:
        """One axis per category, valued by the average level of its skills.

        A single series keeps every category on the same radial scale, so the
        axes stay comparable.
        """
        return [
            {
                "topic": self.category_short_labels.get(category, category),
                "value": round(sum(levels.values()) / len(levels), 1),
            }
            for category, levels in self.skills_data.items()
            if levels
        ]

    # Spanish pages read these; skill names stay as they are in both languages.
    @rx.var
    def selected_skill_es(self) -> str:
        """The selected category's Spanish name, the title of the Spanish radar."""
        return translate(self.selected_skill, "es")

    @rx.var
    def category_average_radar_es(self) -> list[dict]:
        """`category_average_radar` with Spanish axis labels."""
        return [
            {**row, "topic": translate(row["topic"], "es")} for row in self.category_average_radar
        ]
