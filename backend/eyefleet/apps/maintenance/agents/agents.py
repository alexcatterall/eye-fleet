from crewai import Agent, Task, Crew
from .tools import MaintenanceTools
from .index import MaintenanceIndex

class MaintenanceAgents:
    """Manages AI agents for maintenance operations"""
    
    def __init__(self):
        self.tools = MaintenanceTools()
        self.index = MaintenanceIndex()
        self.index.build_index()
        
    def create_agents(self):
        """Create specialized maintenance agents"""
        
        # Maintenance Planner Agent
        planner = Agent(
            name="Maintenance Planner",
            goal="Optimize maintenance schedules and resource allocation",
            backstory="""Expert maintenance planner with deep knowledge of 
            fleet maintenance operations and resource optimization.""",
            tools=[
                self.tools.schedule_maintenance,
                self.tools.analyze_maintenance_patterns
            ]
        )
        
        # Maintenance Analyst Agent
        analyst = Agent(
            name="Maintenance Analyst",
            goal="Analyze maintenance data and provide insights",
            backstory="""Data analyst specialized in maintenance patterns 
            and predictive maintenance.""",
            tools=[
                self.tools.get_asset_history,
                self.tools.analyze_maintenance_patterns
            ]
        )
        
        # Knowledge Base Agent
        knowledge_agent = Agent(
            name="Maintenance Knowledge Base",
            goal="Provide accurate maintenance information and documentation",
            backstory="""Maintenance knowledge expert with access to all 
            historical maintenance records and procedures.""",
            tools=[self.index.query]
        )
        
        return [planner, analyst, knowledge_agent]
    
    def create_crew(self):
        """Create a maintenance crew with all agents"""
        agents = self.create_agents()
        return Crew(
            agents=agents,
            tasks=self.get_default_tasks()
        )
    
    def get_default_tasks(self):
        """Define default tasks for the maintenance crew"""
        return [
            Task(
                description="""Analyze maintenance history and suggest 
                optimal maintenance schedule""",
                agent=self.create_agents()[1]  # Analyst
            ),
            Task(
                description="""Create maintenance schedule based on 
                analysis and available resources""",
                agent=self.create_agents()[0]  # Planner
            ),
            Task(
                description="""Provide relevant maintenance procedures 
                and documentation""",
                agent=self.create_agents()[2]  # Knowledge Base
            )
        ]