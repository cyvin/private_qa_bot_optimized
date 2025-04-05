# 文档向量化逻辑，支持多种文档格式
# retriever/ingest.py
import os
import json
import hashlib
from retriever.loader import load_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from config import DOCS_DIR, CHROMA_DB_DIR, EMBEDDING_MODEL

META_PATH = os.path.join(DOCS_DIR, "vector_meta.json")

# 获取文件哈希值（用于去重）
def get_file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# 载入已向量化记录
def load_vector_meta():
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 保存向量化记录
def save_vector_meta(meta):
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def ingest():
    vector_meta = load_vector_meta()
    new_docs = []
    updated_meta = vector_meta.copy()

    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        if not os.path.isfile(path):
            continue

        file_hash = get_file_hash(path)
        if vector_meta.get(file) == file_hash:
            print(f"✅ 跳过已处理文档：{file}")
            continue

        print(f"📄 处理新文档：{file}")
        docs = load_documents(DOCS_DIR)
        new_docs.extend(docs)
        updated_meta[file] = file_hash
        break  # 每次只处理一个新文件，避免重复加载全部（可自定义）

    if not new_docs:
        print("✅ 无新文档需要处理")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(new_docs)
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectordb = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding)
    vectordb.add_documents(chunks)

    save_vector_meta(updated_meta)
    print("✅ 新文档向量化完成")

if __name__ == '__main__':
    ingest()
