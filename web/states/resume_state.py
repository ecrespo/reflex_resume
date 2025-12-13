import reflex as rx
import plotly.graph_objects as go


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
    def individual_chart(self) -> go.Figure:
        """Generate individual skill radar chart for selected category."""
        data = self.skills_data.get(self.selected_skill, {})
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(data.values()),
            theta=list(data.keys()),
            fill='toself',
            name=self.selected_skill
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False,
            title=self.selected_skill,
            autosize=True,
            height=400,  # Smaller height for mobile
            margin=dict(l=40, r=40, t=80, b=40)  # Reduced margins for mobile
        )
        
        return fig
    
    @rx.var
    def comparative_chart(self) -> go.Figure:
        """Generate comparative radar chart with all skill categories."""
        fig = go.Figure()
        
        for category, skills in self.skills_data.items():
            fig.add_trace(go.Scatterpolar(
                r=list(skills.values()),
                theta=list(skills.keys()),
                fill='toself',
                name=category
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=True,
            title="All Skills Comparison",
            autosize=True,
            height=700,  # Increased height even more
            margin=dict(l=40, r=40, t=80, b=240),  # Significantly increased bottom margin
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="bottom",
                y=-0.55,  # Position much further below the chart
                xanchor="center",
                x=0.5,
                font=dict(size=9)  # Smaller font for mobile
            )
        )
        
        return fig
