# Import Models
import os
import streamlit as st
from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.llms import HuggingFaceHub
load_dotenv()
# api_key = os.getenv("api_key")

def get_response(user_input):
    retriever_chain = get_retrivel_chain(st.session_state.vector_store)
    conversation_rag_chain = get_convertation(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']


def get_convertation(retrieval_chain):
    llm = HuggingFaceHub(repo_id="google/flan-t5-small")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retrieval_chain, stuff_documents_chain)

def get_retrivel_chain(vector_store):
    llm = HuggingFaceHub(repo_id="google/flan-t5-small")
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retrieval_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retrieval_chain

#============================ Featch page data using URL and do chunks of data====================
def get_vectorstore_from_url(url):
    loader=WebBaseLoader(url)
    docoument=loader.load()
    # ---------------Split The Document into chunks----------------------------------
    text_spliter=RecursiveCharacterTextSplitter()
    docouments=text_spliter.split_documents(docoument)
    vector_store=Chroma.from_documents(docouments,HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))
    return vector_store


# GUI ========================GUI-PART======================== PART
st.set_page_config(page_title="Chat with websites", page_icon="🤖")
st.title("Chat With Web-Pages")

# side======================SIDE BAR===================================bar

# st.header("Settings")
website_url = st.text_input("Website URL")



#=================== Input WEB URL==================================== 
if website_url is None or website_url=='':
    st.info("Please the Website Url")
else:
# =====================Chat Storage===============================
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content='Hello, I am a bot. How can I help you?'),
        ]
    if "vector_store" not in st.session_state and website_url:
        st.session_state.vector_store = get_vectorstore_from_url(website_url) # documents=get_vectorstore_from_url()
    # retrivel_chain=get_retrivel_chain(st.session_state.vector_state)
    # conv_rag_chain=get_convertation(retrivel_chain)
    # with st.sidebar:
    #     st.write(st.session_state.vector_state)
# ===================Deal with Chat-History=========================== 
    user_qury=st.chat_input('Type your message hear...')
    if user_qury is not None and user_qury !='':
        # responce=get_response(user_qury)
        responce=get_response(user_qury)
        st.session_state.chat_history.append(HumanMessage(content=user_qury))
        st.session_state.chat_history.append(AIMessage(content=responce))
        
        
        
    
    #==================== Convartation=======================================
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message('AI'):
                st.write(message.content)   
        elif isinstance(message,HumanMessage):
            with st.chat_message('human'):
                st.write(message.content)   



