from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from typing import List
from llama_index.core.base.llms.types import ChatMessage
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
                fn=self.tools.analyze_patterns,
                name="analyze_patterns",
                description="Analyze patterns in telemetry data"
            ),
            # FunctionTool.from_defaults(
            #     fn=self.knowledge_base.query,
            #     name="query_knowledge_base",
            #     description="Query the telemetry knowledge base"
            # )
            FunctionTool.from_defaults(
                fn=self.tools.query_device_info,
                name="query_device_info",
                description="Query fleet device information using natural language when asked about devices use this tool"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_data_indicator_info,
                name="query_indicator_info",
                description="Query fleet data indicator information using natural language when asked about indicators use this tool"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.validate_indicator_value,
                name="validate_indicator_value",
                description="Validate indicator value when asked about indicator values use this tool"
            )

        ]

        # Create agent with tools and knowledge base
        
        # agent = OpenAIAgent.from_tools(
        #     tools=telemetry_tools,
        #     system_prompt="""You are an expert telemetry analyst that helps users 
        #     understand and work with vehicle telemetry data. You can fetch and analyze
        #     telemetry data, generate datasets, and answer questions about the system."""
        # )
        llm = OpenAI(model="gpt-4o-mini")
        agent = ReActAgent.from_tools(tools=telemetry_tools, llm=llm, verbose=True)  
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

        
        return {
            'response': str(response),
            'tools_used': tools
        }