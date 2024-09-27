import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from .astra_tools import get_scheduled_flights, get_flight_detail


class TheFlightAgent:
    agent = None
    tools = [get_scheduled_flights, get_flight_detail]
    
    def __init__(self):
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assistant. Make sure to use the available tools for information.
                    Customer ID: {customer_id}""",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        # Construct the Tools agent
        self.agent = create_tool_calling_agent(llm, self.tools, prompt)
        print("="*50)
        print("THE FLIGHT AGENT - Initialized")
        print(os.getenv("OPENAI_API_KEY"))
        print("="*50)
        
    def invoke(self, question):
        agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        return agent_executor.invoke({"input": question, "customer_id": os.getenv("CUSTOMER_ID")})
        