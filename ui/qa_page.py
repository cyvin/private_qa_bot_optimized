import gradio as gr
import sqlite3
import os
import time
from chains.qa_chain import get_qa_chain

qa_chain = get_qa_chain()
DB_PATH = os.path.abspath("chat_history.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def save_to_db(q, a):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO chat (question, answer) VALUES (?, ?)", (q, a))
    conn.commit()
    conn.close()

init_db()

def stream_response(user_input):
    response = qa_chain.invoke({"query": user_input})
    answer = response["result"]
    save_to_db(user_input, answer)
    buffer = ""
    for char in answer:
        buffer += char
        time.sleep(0.01)
        yield buffer

def qa_tab():
    gr.Markdown("## 💬 Private Q&A Chat")
    answer_box = gr.Textbox(label="Answer", lines=15, interactive=False, show_copy_button=True)
    user_input = gr.Textbox(label="Ask your question", placeholder="e.g. What is the capacity of Qingyuan Port?")
    user_input.submit(fn=stream_response, inputs=user_input, outputs=answer_box)
