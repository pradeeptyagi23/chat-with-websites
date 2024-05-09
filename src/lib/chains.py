
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
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

class ConversationalRetrievalChain(BaseModel):
    retriever_chain: Any
    system_input: str

    def get_conversational_rag_chain(self):
        llm = ChatOpenAI()
        prompt = ChatPromptTemplate.from_messages([
            ("system","Answer the user's question based on the below context. Only answer based on the context. Do not refer to other sources. If you do not know the answer, reply with a formal message to convey that you dont have the answer based on the source\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user","{input}")
        ])

        #chain the history aware retriver chain with the document chain.
        stuff_documents_chain = create_stuff_documents_chain(llm,prompt=prompt)
        return create_retrieval_chain(self.retriever_chain,stuff_documents_chain)
