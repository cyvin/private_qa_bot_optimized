# 各类文档加载器封装
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
import os

def load_documents(doc_dir):
    docs = []
    for file in os.listdir(doc_dir):
        path = os.path.join(doc_dir, file)
        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif file.endswith(".docx"):
            docs.extend(Docx2txtLoader(path).load())
    return docs