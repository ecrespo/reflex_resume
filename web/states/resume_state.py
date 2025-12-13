import reflex as rx


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
    
    # Skills data structure for radar charts
    skills_data = {
        'Programming': {'Python': 5, 'R': 3, 'Golang': 3, 'Javascript': 2, 'Julia': 2, "Nestjs": 2},
        'Data processing/wrangling': {'SQL': 5, 'Pandas': 5, 'Numpy': 5,'Polars':2, 'Pyspark':2, 'DuckDB':1},
        'Data visualization': {'Matplotlib': 5, 'Seaborn': 5, 'Plotly': 3, 'Bokeh': 2},
        'Dashboard': {'Streamlit': 5, 'Dash': 2, 'Taipy': 1, 'Reflex': 3},
        'Machine Learning/Deep Learning': {'scikit-learn': 5, 'TensorFlow': 2, 'Keras': 1, 'Pytorch':3},
        'IA':{'Langchain':3,'LangGraph':1,'CrewAI': 2,'AutoGen':1,'BeeAI':1},
        'Web development': {'Django': 4, 'FastAPI': 5, 'Flask': 2, 'HTML': 3, 'CSS': 3},
        'Operating System': {'Linux': 5, 'Window': 3, 'MacOs': 2},
        "Low code tools": {'Knime': 3, 'Tableu': 2, 'Power BI': 1, 'N8N': 4},
        'Containers': {'Docker': 5, 'Docker-compose': 4, 'Kubernetes': 2},
        'Serverless Development': {'AWS Cloudformation': 4, 'AWS SAM': 4, 'Serverless': 3},
        'Database Engine': {'PostgreSQL': 5, 'MySQLdb': 3, 'MongoDB': 3},
    }
    
    # Currently selected skill category
    selected_skill: str = 'Programming'
    
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
    
    @rx.var
    def individual_chart_data(self) -> list[dict]:
        """Generate individual skill radar chart data for selected category."""
        data = self.skills_data.get(self.selected_skill, {})
        return [{"subject": skill, "value": level} for skill, level in data.items()]
    
    @rx.var
    def comparative_chart_data(self) -> list[dict]:
        """Generate comparative radar chart data with all skill categories."""
        # Get all unique skills across all categories
        all_skills: set[str] = set()
        for skills in self.skills_data.values():
            all_skills.update(skills.keys())
        
        # Create data with each skill as a row
        result = []
        for skill in sorted(all_skills):
            row: dict = {"subject": skill}
            for category, skills in self.skills_data.items():
                row[category] = skills.get(skill, 0)
            result.append(row)
        return result
    
    @rx.var
    def category_colors(self) -> list[dict]:
        """Return list of category info with colors for the comparative chart."""
        colors = [
            "#636efa", "#EF553B", "#00cc96", "#ab63fa", 
            "#FFA15A", "#19d3f3", "#FF6692", "#B6E880",
            "#FF97FF", "#FECB52", "#8dd3c7", "#bebada"
        ]
        return [
            {"name": cat, "color": colors[i % len(colors)]}
            for i, cat in enumerate(self.skills_data.keys())
        ]
