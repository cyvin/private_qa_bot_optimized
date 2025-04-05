import gradio as gr

def help_tab():
    gr.Markdown("""## ℹ️ How to Use

- 💬 Ask questions in the Chat tab.
- 📁 Upload or delete documents in the Documents tab.
- 📜 View previous Q&A in the History tab.

This private Q&A assistant is powered by LangChain + DeepSeek API + Chroma DB.
""")
