from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import os

os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')

class state(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

llm=ChatOpenAI(model='gpt-4o')

def default_graph():
    graph=StateGraph(state)
    def call_model(state):
        return {
            'messages':llm.invoke(state['messages'])
        }

    graph.add_node('agent',call_model)
    graph.add_edge(START,'agent')
    graph.add_edge('agent',END)
    agent=graph.compile()
    return agent

agent=default_graph()
