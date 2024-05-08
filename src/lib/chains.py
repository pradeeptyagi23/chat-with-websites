
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from pydantic import BaseModel,ConfigDict
from langchain_community import vectorstores
from typing import Any

class ContextualRetrievalChain(BaseModel):
    system_input: str
    vector_store: Any
    def get_context_retriever_chain(self):
        retriever = self.vector_store.as_retriever()
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