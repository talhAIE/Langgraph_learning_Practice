from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import  TypedDict,Literal,Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# state

class State(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

llm=ChatOpenAI(model='gpt-4o')

def chat_node(state:State)->State:
    prompt=state['messages']
    prompt=ChatPromptTemplate.from_messages(
        [
            ('system','You are a helpful assistant to answer short to the point and in day to day simple English answer.you have to only answer in English '),
            ('user','{user_text}')
        ]
    )
    chain=prompt | llm
    response=chain.invoke(
        {'user_text':state['messages']}
    )
    return {
        'messages':[response]
    }

#graph
# checkpointer
checkpointer=InMemorySaver()
graph=StateGraph(State)

graph.add_node('Chatbot',chat_node)
graph.add_edge(START,'Chatbot')
graph.add_edge('Chatbot',END)

workflow=graph.compile(checkpointer=checkpointer)