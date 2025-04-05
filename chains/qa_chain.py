# 构建带有Prompt的 RetrievalQA chain
# chains/qa_chain.py
from langchain.chains import RetrievalQA
from config import CHROMA_DB_DIR, EMBEDDING_MODEL
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from llm.deepseek_llm import DeepSeekLLM
from utils.memory import get_memory


def get_qa_chain():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding)
    retriever = vectordb.as_retriever()
    llm = DeepSeekLLM()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        memory=get_memory(),
        return_source_documents=True,
        output_key="result"  # ✅ 显式指定要存储的输出字段
    )
    return qa
