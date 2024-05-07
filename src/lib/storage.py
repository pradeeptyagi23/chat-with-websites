from pydantic import BaseModel,Field
from langchain.document_loaders.web_base import WebBaseLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Document(BaseModel):
    doc_type: str = Field(default="web" or "pdf",validate_default=True)
    source: str

    def __load_document(self):
        print("in load documents")
        try:
            if(self.doc_type == "web"):
                loader  = WebBaseLoader(self.source)
            elif(self.doc_type == "pdf"):
                loader = PyPDFLoader(self.source)
            document = loader.load()
        except:
            print("Failed to load document")
        else:
            return document

        
    def split_documents(self):
        try:
            document = self.__load_document()
            text_splitter = RecursiveCharacterTextSplitter()
            chunked_docs = text_splitter.split_documents(document)
        except Exception as e:
            print("Failed to split documents" +str(e))
        else:
            return chunked_docs



# if "__name__" == "__name__":
#     documentObj = Document(doc_type="web",source="https://python.org")
#     chunks = documentObj.split_documents()
#     print(chunks)