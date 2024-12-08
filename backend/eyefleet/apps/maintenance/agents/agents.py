from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from typing import List
from llama_index.core.base.llms.types import ChatMessage
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
                fn=self.tools.add_vehicle,
                name="add_vehicle",
                description="Add a new vehicle to the fleet with registration details"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_assets,
                name="query_assets",
                description="Query asset information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_maintenance,
                name="query_maintenance", 
                description="Query maintenance records using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_parts,
                name="query_parts",
                description="Query parts inventory using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_inspections,
                name="query_inspections",
                description="Query inspection records using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.ask_followup,
                name="ask_followup",
                description="Ask follow-up questions to the user"
            ),
            FunctionTool.from_defaults(
                fn=self.index.query,
                name="query_knowledge_base",
                description="Query the maintenance knowledge base for procedures and documentation"
            )
        ]

        # Create agent with tools and knowledge base
        llm = OpenAI(model="gpt-4o-mini", system_prompt="You are an expert maintenance analyst and planner that helps optimize fleet maintenance operations. You can schedule maintenance tasks, analyze maintenance patterns, access asset histories, query various maintenance records, and provide maintenance documentation.")
        agent = ReActAgent.from_tools( tools=maintenance_tools, llm=llm, verbose=True)  
        return agent
    
    def query(self, query_text: str, chat_history: List[ChatMessage] = None):
        """Query the agent with a natural language request"""
        agent = self.create_agent()
        print("--- making query to agents ----")
        response = agent.chat(query_text, chat_history)


        print("the tools used are: ", response.sources)
        tools = []

        for source in response.sources:
                tools.append(source.tool_name)

        