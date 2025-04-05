import gradio as gr
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.abspath("chat_history.db")

def load_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT id, question, answer, timestamp FROM chat ORDER BY timestamp DESC", conn)
        conn.close()
        if df.empty:
            return "No history yet."
        return df.to_markdown(index=False)
    except Exception as e:
        return f"Error reading history: {e}"

def history_tab():
    gr.Markdown("## 📜 Chat History")
    gr.Markdown("This section displays all previous Q&A interactions.")
    history_display = gr.Textbox(label="History Log", lines=20, interactive=False)
    return history_display
