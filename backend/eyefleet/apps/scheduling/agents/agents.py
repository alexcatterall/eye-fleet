from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import ReActAgent
from typing import List
from llama_index.llms.openai import OpenAI
from llama_index.core.base.llms.types import ChatMessage
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
                fn=self.tools.manage_mission_changes,
                name="manage_mission_changes",
                description="Manage and apply changes to mission parameters"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_cargo,
                name="query_cargo",
                description="Query cargo information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_clients,
                name="query_clients", 
                description="Query client information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_missions,
                name="query_missions",
                description="Query mission information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_pilots,
                name="query_pilots",
                description="Query pilot information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.tools.query_schedules,
                name="query_schedules",
                description="Query schedule information using natural language"
            ),
            FunctionTool.from_defaults(
                fn=self.knowledge_base.query,
                name="query_knowledge_base",
                description="Query the scheduling knowledge base"
            )
        ]

        # Create agent with tools and knowledge base
        llm = OpenAI(model="gpt-4o-mini", system_prompt="You are an expert scheduling analyst that helps users optimize mission schedules, routes, and delivery sequences. You can create schedules, analyze conflicts, track missions, and provide insights from historical scheduling data.")
        agent = ReActAgent.from_tools(tools=scheduling_tools, llm=llm, verbose=True)
        
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