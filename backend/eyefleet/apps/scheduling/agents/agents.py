from crewai import Agent, Task, Crew
from .tools import SchedulingTools
from .knowledgebase import SchedulingIndex

class SchedulingAgents:
    """Manages AI agents for scheduling operations"""
    
    def __init__(self):
        self.tools = SchedulingTools()
        self.index = SchedulingIndex()
        self.index.build_index()
        
    def create_agents(self):
        """Create specialized scheduling agents"""
        
        # Route Optimizer Agent
        route_optimizer = Agent(
            name="Route Optimizer",
            goal="Optimize routes and delivery sequences",
            backstory="""Expert in route optimization and logistics planning with 
            deep understanding of vehicle routing problems.""",
            tools=[
                self.tools.optimize_route,
                self.tools.analyze_route_patterns
            ]
        )
        
        # Schedule Planner Agent
        schedule_planner = Agent(
            name="Schedule Planner",
            goal="Create and optimize mission schedules",
            backstory="""Scheduling expert specialized in resource allocation 
            and timeline optimization.""",
            tools=[
                self.tools.schedule_mission,
                self.tools.optimize_schedule,
                self.tools.analyze_schedule_conflicts
            ]
        )
        
        # Mission Coordinator Agent
        mission_coordinator = Agent(
            name="Mission Coordinator",
            goal="Coordinate and track mission execution",
            backstory="""Mission coordination specialist focused on real-time 
            tracking and adjustment of ongoing missions.""",
            tools=[
                self.tools.track_mission,
                self.tools.handle_mission_updates,
                self.tools.manage_mission_changes
            ]
        )
        
        # Knowledge Base Agent
        knowledge_agent = Agent(
            name="Scheduling Knowledge Base",
            goal="Provide scheduling insights and historical data",
            backstory="""Scheduling knowledge expert with access to historical 
            mission data and performance metrics.""",
            tools=[self.index.query]
        )
        
        return [route_optimizer, schedule_planner, mission_coordinator, knowledge_agent]
    
    def create_crew(self):
        """Create a scheduling crew with all agents"""
        agents = self.create_agents()
        return Crew(
            agents=agents,
            tasks=self.get_default_tasks()
        )
    
    def get_default_tasks(self):
        """Define default tasks for the scheduling crew"""
        agents = self.create_agents()
        return [
            Task(
                description="""Analyze route patterns and optimize delivery sequences""",
                agent=agents[0]  # Route Optimizer
            ),
            Task(
                description="""Create optimal mission schedules based on 
                requirements and constraints""",
                agent=agents[1]  # Schedule Planner
            ),
            Task(
                description="""Coordinate mission execution and handle real-time updates""",
                agent=agents[2]  # Mission Coordinator
            ),
            Task(
                description="""Provide relevant historical data and insights""",
                agent=agents[3]  # Knowledge Base
            )
        ]