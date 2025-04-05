# ui/interface.py
import gradio as gr
from chains.qa_chain import get_qa_chain
from retriever.ingest import ingest
import os
import shutil
from config import DOCS_DIR, CHROMA_DB_DIR
import json
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

qa_chain = get_qa_chain()
chat_history = []

# 对话主函数
def chatbot(user_input):
    response = qa_chain.invoke({"query": user_input})
    answer = response["result"]
    chat_history.append((user_input, answer))
    return "\n".join([f"你：{q}\n助手：{a}" for q, a in chat_history])

# 上传页面逻辑
def handle_upload(file):
    if file is None:
        return "⚠️ 没有选择文件", update_doc_list()
    try:
        target_path = os.path.join(DOCS_DIR, os.path.basename(file.name))
        shutil.copy(file.name, target_path)
        ingest()
        return "✅ 文件上传并已向量化", update_doc_list()
    except Exception as e:
        return f"❌ 上传失败: {str(e)}", update_doc_list()

# 获取当前资料清单
def update_doc_list():
    files = os.listdir(DOCS_DIR)
    files = [f for f in files if not f.endswith(".json") and os.path.isfile(os.path.join(DOCS_DIR, f))]
    if not files:
        return "📂 暂无已上传资料"
    return "\n".join([f for f in files])

# 删除文件及其向量信息
def handle_delete(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(filepath):
        return f"❌ 文件不存在：{filename}", update_doc_list()

    try:
        os.remove(filepath)

        # 同步删除 Chroma 向量（此处简单示例：重新构建）
        print("📦 正在重建向量数据库...")
        files = os.listdir(DOCS_DIR)
        files = [f for f in files if os.path.isfile(os.path.join(DOCS_DIR, f)) and not f.endswith(".json")]

        if files:
            from retriever.loader import load_documents
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            docs = load_documents(DOCS_DIR)
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(docs)
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DB_DIR)
            vectordb.persist()
        else:
            shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)

        return f"✅ 已删除：{filename}，并更新向量库", update_doc_list()
    except Exception as e:
        return f"❌ 删除失败: {str(e)}", update_doc_list()

# 启动页面UI
def launch_ui():
    with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
        with gr.Tab("🤖 智能问答"):
            gr.Markdown("# 🤖 私有知识库问答系统\n可以直接提问，系统将从已上传资料中进行回答。")
            chat_input = gr.Textbox(label="请输入你的问题", placeholder="例如：清远港的吞吐能力是多少？")
            chat_output = gr.Textbox(label="问答记录", lines=15, interactive=False)
            chat_input.submit(fn=chatbot, inputs=chat_input, outputs=chat_output)

        with gr.Tab("📚 资料库管理"):
            gr.Markdown("# 📚 上传与管理你的私有资料\n支持 PDF / Word 文档，支持删除")
            file_upload = gr.File(label="上传文件", file_types=[".pdf", ".docx"])
            upload_btn = gr.Button("上传并向量化")
            upload_status = gr.Textbox(label="状态")
            doc_list = gr.Textbox(label="📁 当前资料清单", lines=10, interactive=False)

            delete_file_name = gr.Textbox(label="要删除的文件名（含扩展名）")
            delete_btn = gr.Button("删除资料")
            delete_status = gr.Textbox(label="删除状态")

            upload_btn.click(handle_upload, inputs=[file_upload], outputs=[upload_status, doc_list])
            delete_btn.click(handle_delete, inputs=[delete_file_name], outputs=[delete_status, doc_list])
            demo.load(fn=update_doc_list, outputs=[doc_list])

        with gr.Tab("🧭 系统导航"):
            gr.Markdown("""
            ## 🧭 使用指南
            - 在“智能问答”中输入你的问题，系统会结合知识库进行回答。
            - 在“资料库管理”中上传 PDF 或 Word 文档，系统会自动向量化。
            - 可输入文件名删除资料及其向量内容。
            
            ## 🛠 后续功能预告
            - 引用原文段落来源
            - 多用户知识空间
            - 文档摘要与快速阅读
            """)

    demo.launch()