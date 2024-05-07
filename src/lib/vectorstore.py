from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from .storage import Document
from pydantic import BaseModel

class VectorStore(BaseModel):
    doc_chunks:list

    def get_vectorstore(self) -> OpenAIEmbeddings:
        try:
            vectorstore = Chroma.from_documents(documents=self.doc_chunks,embedding=OpenAIEmbeddings())
        except:
            print("failed to create vector store")
        else:
            return vectorstore

if "__name__" == "__main__":

    documentObj = Document(doc_type="web",source="https://blog.langchain.dev/langgraph")
    chunks = documentObj.split_documents()
    vectorObj = VectorStore(doc_chunks=chunks)
    vectorstore = vectorObj.get_vectorstore()
    