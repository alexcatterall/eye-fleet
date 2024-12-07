from crewai import Agent, Task, Crew
from .tools import LivetrackingTools
from llama_index import VectorStoreIndex, Document

class LivetrackingAgents:
    """Manages AI agents for livetracking operations"""
    
    def __init__(self):
        self.tools = LivetrackingTools()
        
    def create_agents(self):
        """Create specialized livetracking agents"""
        
        # Data Collection Agent
        data_collector = Agent(
            name="Data Collector",
            goal="Collect and organize telemetry data",
            backstory="""Expert in data collection and organization with deep 
            understanding of telemetry systems and time-series data.""",
            tools=[
                self.tools.fetch_telemetry_data,
                self.tools.generate_csv_dataset
            ]
        )
        
        # Data Analyst Agent
        data_analyst = Agent(
            name="Data Analyst",
            goal="Analyze telemetry data and identify patterns",
            backstory="""Data analysis expert specialized in vehicle telemetry 
            and performance metrics.""",
            tools=[
                self.tools.query_telemetry,
                self.tools.analyze_patterns
            ]
        )
        
        return [data_collector, data_analyst]
    
    def create_crew(self):
        """Create a livetracking crew with all agents"""
        agents = self.create_agents()
        return Crew(
            agents=agents,
            tasks=self.get_default_tasks()
        )
    
    def get_default_tasks(self):
        """Define default tasks for the livetracking crew"""
        agents = self.create_agents()
        return [
            Task(
                description="""Collect recent telemetry data and generate 
                updated CSV dataset""",
                agent=agents[0]  # Data Collector
            ),
            Task(
                description="""Analyze telemetry data and provide insights""",
                agent=agents[1]  # Data Analyst
            )
        ]