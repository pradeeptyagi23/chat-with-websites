from pydantic import BaseModel
from langchain.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from abc import ABC,abstractmethod

class Document(ABC,BaseModel):
    source:str
    @abstractmethod
    def load():
        pass

class WebDocument(Document):
    def load(self):
        try:
            loader  = WebBaseLoader(self.source)
            document = loader.load()
            text_splitter = RecursiveCharacterTextSplitter()
            chunked_docs = text_splitter.split_documents(document)         
        except:
            print("Failed to load document")
        else:
            return chunked_docs


# if "__name__" == "__name__":
#     webDocObj = WebDocument(source="https://python.org")
#     print(webDocObj.load())
#     # chunks = documentObj.split_documents()
#     # print(chunks)