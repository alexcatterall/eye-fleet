from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from .tools import MaintenanceTools
from .knowledgebase import MaintenanceIndex

class MaintenanceAgents:
    """Manages AI agents for maintenance operations"""
    
    def __init__(self):
        self.tools = MaintenanceTools()
        self.index = MaintenanceIndex()
        self.index.build_index()
        
    def create_agent(self):
        """Create a LlamaIndex agent with maintenance tools and knowledge"""
        
        # Create function tools
        maintenance_tools = [
            FunctionTool.from_defaults(
                fn=self.tools.schedule_maintenance,
                name="schedule_maintenance",
                description="Schedule and optimize maintenance tasks based on resources and constraints"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.analyze_maintenance_patterns,
                name="analyze_maintenance_patterns",
                description="Analyze historical maintenance data to identify patterns and trends"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.get_asset_history,
                name="get_asset_history",
                description="Retrieve maintenance history for a specific asset"
            ),
            FunctionTool.from_defaults(
                fn=self.index.query,
                name="query_knowledge_base",
                description="Query the maintenance knowledge base for procedures and documentation"
            )
        ]

        # Create agent with tools and knowledge base
        agent = OpenAIAgent.from_tools(
            tools=maintenance_tools,
            system_prompt="""You are an expert maintenance analyst and planner that helps optimize 
            fleet maintenance operations. You can schedule maintenance tasks, analyze maintenance patterns,
            access asset histories, and provide maintenance documentation."""
        )
        
        return agent
    
    def query(self, query_text: str):
        """Query the agent with a natural language request"""
        agent = self.create_agent()
        response = agent.chat(query_text)
        return str(response)