import gradio as gr
import os
import shutil
from config import DOCS_DIR, CHROMA_DB_DIR, EMBEDDING_MODEL
from retriever.ingest import ingest
from retriever.loader import load_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def update_doc_list():
    files = [f for f in os.listdir(DOCS_DIR) if not f.endswith(".json")]
    return "\n".join(files) or "No documents found."

def get_doc_options():
    return [f for f in os.listdir(DOCS_DIR) if not f.endswith(".json")]

def handle_upload(file):
    if file is None:
        return "No file selected", update_doc_list(), get_doc_options()
    try:
        target_path = os.path.join(DOCS_DIR, os.path.basename(file.name))
        shutil.copy(file.name, target_path)
        ingest()
        return "Upload and vectorization successful", update_doc_list(), get_doc_options()
    except Exception as e:
        return f"Upload failed: {e}", update_doc_list(), get_doc_options()

def handle_delete(filename, confirm):
    if not confirm:
        return "Please confirm deletion", update_doc_list(), get_doc_options()

    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return "File not found", update_doc_list(), get_doc_options()

    try:
        os.remove(path)
        files = [f for f in os.listdir(DOCS_DIR) if not f.endswith(".json")]
        chunks = []
        if files:
            docs = load_documents(DOCS_DIR)
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(docs)
            embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            Chroma.from_documents(chunks, embedding=embedding, persist_directory=CHROMA_DB_DIR).persist()
        else:
            shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)

        return f"Deleted: {filename}", update_doc_list(), get_doc_options()
    except Exception as e:
        return f"Deletion failed: {e}", update_doc_list(), get_doc_options()

def library_tab():
    file_upload = gr.File(label="Upload Document", file_types=[".pdf", ".docx"])
    upload_btn = gr.Button("Upload & Vectorize")
    upload_status = gr.Textbox(label="Status")

    doc_list = gr.Textbox(label="Current Documents", lines=10, interactive=False)
    delete_dropdown = gr.Dropdown(choices=[], label="Select document to delete")
    confirm_box = gr.Checkbox(label="Confirm deletion")
    delete_btn = gr.Button("Delete Document")
    delete_status = gr.Textbox(label="Delete Status")

    upload_btn.click(handle_upload, inputs=[file_upload], outputs=[upload_status, doc_list, delete_dropdown])
    delete_btn.click(handle_delete, inputs=[delete_dropdown, confirm_box], outputs=[delete_status, doc_list, delete_dropdown])

    return doc_list, delete_dropdown
