import streamlit as st
from chatbot_backend import workflow
from langchain_core.messages import HumanMessage

user_input=st.chat_input('Type here....')
# session state to store message histor 
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

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
            config={'configurable':{'thread_id':'1'}},
            stream_mode='messages'
        )
        )
        st.session_state['message_history'].append({'role':'ai','content':ai_msg})
