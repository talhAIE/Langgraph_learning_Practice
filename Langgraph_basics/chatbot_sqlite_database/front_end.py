import streamlit as st
from backend import workflow,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid
import os
os.environ['LANGCHAIN_PROJECT']='chatbot_project_obervebility'

def gen_thread_id():
    return uuid.uuid4()

def add_thread(thread):
    if thread not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread)


user_input=st.chat_input('Type here....')
# session state to store message histor 
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=gen_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=retrieve_all_threads()
add_thread(st.session_state['thread_id'])
CONFIG={
    'configurable':{'thread_id':st.session_state['thread_id']}
    ,
    'metadata':st.session_state['thread_id'],
    'run_name':'chat_turn'}

def reset():
    thread_id=gen_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def load_chat(thread_id):
    return workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']

st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New Chat'):
    reset()
st.sidebar.header('My Conversations')

for id in st.session_state['chat_thread'][::-1]:
    st.session_state['thread_id']=id
    if st.sidebar.button(str(id)):
        msgs=load_chat(id)
        temp_msgs=[]
        for msg in msgs:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='ai'
            temp_msgs.append({'role':role,'content':msg.content})
        st.session_state['message_history']=temp_msgs


for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

if user_input:
    # append the user message to history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # response=workflow.invoke({'messages':[HumanMessage(content=user_input)]},config={'configurable':{'thread_id':'1'}})
    # ai_msg=response['messages'][-1].content
    # st.session_state['message_history'].append({'role':'ai','content':ai_msg})
    # with st.chat_message('AI'):
    #     st.text(ai_msg)

    # streaming
    with st.chat_message('ai'):
        ai_msg=st.write_stream(
            message_chunk.content for message_chunk,metat_data in workflow.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        )
        )
        st.session_state['message_history'].append({'role':'ai','content':ai_msg})
