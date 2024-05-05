from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage,HumanMessage 
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()


def get_vectorstore_from_url(url):
    # load the document
    loader = WebBaseLoader(url)
    document = loader.load()
    # Split the document
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents=document)

    #embed document chunks and create a vectorstore from chunks 
    vector_store = Chroma.from_documents(documents=document_chunks,embedding=OpenAIEmbeddings())

    return vector_store

def get_context_retriever_chain(vector_store):
    retriever = vector_store.as_retriever()
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","Given the above conversation,generate a search query to lookup in order to get information relevant to the conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm,retriever,prompt)
    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system","Answer the user's question based on the below context. Only answer based on the context. Do not refer to other sources. If you do not know the answer, reply with a formal message to convey that you dont have the answer based on the source\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}")
    ])

    #chain the history aware retriver chain with the document chain.
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt=prompt)
    return create_retrieval_chain(retriever_chain,stuff_documents_chain)

def get_response(user_query):
    #create conversation chain    
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
        "chat_history":st.session_state.chat_history,
        "input":user_query
    })
    return response['answer']

# app config
st.set_page_config(page_title="Chat with Websites",page_icon=":robot:")
st.title("Chat with Websites")


# side bar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

# dont enable chat bot if website url is not entered
if website_url is None or website_url == "":
    st.info("Please enter website url")
else:
    # chat history init only if it is a new session (refresh of site)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot, how can I help you!")
        ]
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(website_url)


    #user input
    user_query = st.chat_input("message")

    if user_query and user_query != "":
        response = get_response(user_query)
        
        #append user query
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        #append response from AI
        st.session_state.chat_history.append(AIMessage(content=response))


    # conversation
    for message in st.session_state.chat_history:
        if(isinstance(message,AIMessage)):
            with st.chat_message("AI"):
                st.write(message.content)
        elif(isinstance(message,HumanMessage)):
            with st.chat_message("Human"):
                st.write(message.content)
