from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from .tools import LivetrackingTools
from .knowledgebase import LivetrackingIndex
import os
class LivetrackingAgents:
    """Manages AI agents for livetracking operations"""
    
    def __init__(self):
        self.tools = LivetrackingTools()
        self.knowledge_base = LivetrackingIndex()
        
    def create_agent(self):
        """Create a LlamaIndex agent with telemetry tools and knowledge"""
        
        # Create function tools
        telemetry_tools = [
            FunctionTool.from_defaults(
                fn=self.tools.fetch_telemetry_data,
                name="fetch_telemetry_data",
                description="Fetch recent telemetry data for a device and indicator"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.generate_csv_dataset,
                name="generate_csv_dataset", 
                description="Generate CSV dataset from telemetry data"
            ),
            FunctionTool.from_defaults(
                fn=self.knowledge_base.query,
                name="query_knowledge_base",
                description="Query the telemetry knowledge base"
            )
        ]

        # Create agent with tools and knowledge base
        agent = OpenAIAgent.from_tools(
            tools=telemetry_tools,
            system_prompt="""You are an expert telemetry analyst that helps users 
            understand and work with vehicle telemetry data. You can fetch and analyze
            telemetry data, generate datasets, and answer questions about the system."""
        )
        
        return agent
    
    def query(self, query_text: str):
        """Query the agent with a natural language request"""
        agent = self.create_agent()
        response = agent.chat(query_text)
        return str(response)