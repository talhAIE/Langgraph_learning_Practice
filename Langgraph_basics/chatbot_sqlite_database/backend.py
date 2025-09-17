from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import  TypedDict,Literal,Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import sqlite3
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

# database sqlite is restricted with multiple threads so we set check_same_thread=False to let sqlite not check for same threads
conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

#graph
# checkpointer
checkpointer=SqliteSaver(conn)
graph=StateGraph(State)

graph.add_node('Chatbot',chat_node)
graph.add_edge(START,'Chatbot')
graph.add_edge('Chatbot',END)

workflow=graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_thread=set() # choose set coz we dont want dublicate values
    for each in checkpointer.list(None):
        thread=each.config['configurable']['thread_id'] # none means we want all threads to be list not specific one
        all_thread.add(thread)
        return list(all_thread)

if __name__=='__main__':
    # print(    workflow.invoke({
    #     'messages':'what is my name'
    # },
    # config={'configurable':{'thread_id':'1'}}))
    all_thread=set() # choose set coz we dont want dublicate values
    for each in checkpointer.list(None):
        thread=each.config['configurable']['thread_id'] # none means we want all threads to be list not specific one
        all_thread.add(thread)
    print(list(all_thread))
