from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from .tools import SchedulingTools
from .knowledgebase import SchedulingIndex

class SchedulingAgents:
    """Manages AI agents for scheduling operations"""
    
    def __init__(self):
        self.tools = SchedulingTools()
        self.knowledge_base = SchedulingIndex()
        self.knowledge_base.build_index()
        
    def create_agent(self):
        """Create a LlamaIndex agent with scheduling tools and knowledge"""
        
        # Create function tools
        scheduling_tools = [
            FunctionTool.from_defaults(
                fn=self.tools.optimize_route,
                name="optimize_route",
                description="Optimize routes and delivery sequences for missions"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.schedule_mission,
                name="schedule_mission",
                description="Create and optimize mission schedules based on requirements"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.track_mission,
                name="track_mission",
                description="Track and monitor ongoing mission execution"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.handle_mission_updates,
                name="handle_mission_updates",
                description="Process and handle real-time mission updates"
            ),
            FunctionTool.from_defaults(
                fn=self.knowledge_base.query,
                name="query_knowledge_base",
                description="Query the scheduling knowledge base"
            )
        ]

        # Create agent with tools and knowledge base
        agent = OpenAIAgent.from_tools(
            tools=scheduling_tools,
            system_prompt="""You are an expert scheduling analyst that helps users 
            optimize mission schedules, routes, and delivery sequences. You can create
            schedules, analyze conflicts, track missions, and provide insights from
            historical scheduling data."""
        )
        
        return agent
    
    def query(self, query_text: str):
        """Query the agent with a natural language request"""
        agent = self.create_agent()
        response = agent.chat(query_text)
        return str(response)