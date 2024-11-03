# Import Models

import streamlit as st
from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings



def get_response(user_input):
    return 'I Dont no'


#============================ Featch page data using URL and do chunks of data====================
def get_vectorstore_from_url(url):
    loader=WebBaseLoader(url)
    docoument=loader.load()
    # Split The Document into chunks
    text_spliter=RecursiveCharacterTextSplitter()
    docouments=text_spliter.split_documents(docoument)
    vector_store=Chroma.from_documents(docouments,HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))
    return vector_store


# GUI ========================GUI-PART======================== PART
st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat with websites")
# =====================Chat Storage===============================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[
        AIMessage(content='Hellow i am a bot how can i help you'),   
    ]
    
    
    
# side======================SIDE BAR===================================bar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

user_qury=st.chat_input('Type your message hear...')

#=================== Input WEB URL==================================== 
if website_url is None or website_url=='':
    st.info("Please the Website Url")
else:
    documents=get_vectorstore_from_url(url=website_url)
    with st.sidebar:
        st.write(documents)
# ===================Deal with Chat-History=========================== 
    if user_qury is not None and user_qury !='':
        responce=get_response(user_qury)
        st.session_state.chat_history.append(HumanMessage(content=user_qury))
        st.session_state.chat_history.append(AIMessage(content=responce))
        # st.write(user_qury)
        
        
    
    #==================== Convartation=======================================
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message('AI'):
                st.write(message.content)   
        elif isinstance(message,HumanMessage):
            with st.chat_message('human'):
                st.write(message.content)   



