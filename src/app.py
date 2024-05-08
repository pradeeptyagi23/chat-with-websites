from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage,HumanMessage 
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from lib.storage import WebDocument
from lib.vectorstore import chromaVectorStore
from lib.prompts import ChatPromptTmpl
from lib.chains import ContextualRetrievalChain

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()


def get_vectorstore_from_url(url):

    # load the document and get the chunks
    doc_obj = WebDocument(source=url)
    chunks = doc_obj.load()

    # get the vector from the chunks
    vector_store_obj = chromaVectorStore(documents=chunks)
    vector_store = vector_store_obj.get_vectorstore()

    return vector_store

    system_input = """
        Given the above conversation,generate a search query to lookup 
        in order to get information relevant to the conversation
    """
    chainObj = ContextualRetrievalChain(system_input=system_input,llm=ChatOpenAI(),vectorstore=vector_store)

    retriever = vector_store.as_retriever()
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("system","Given the above conversation,generate a search query to lookup in order to get information relevant to the conversation")
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
    # retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    system_input = """
        Given the above conversation,generate a search query to lookup 
        in order to get information relevant to the conversation
    """
    chainObj = ContextualRetrievalChain(system_input=system_input,llm=ChatOpenAI(),vector_store=st.session_state.vector_store)
    retriever_chain = chainObj.get_context_retriever_chain()
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
