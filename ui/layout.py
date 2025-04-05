import gradio as gr
from ui.qa_page import qa_tab
from ui.library_page import library_tab, update_doc_list, get_doc_options
from ui.help_page import help_tab
from ui.history_page import history_tab, load_history

def build_ui():
    with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
        with gr.Tab("💬 Chat"):
            qa_tab()
        with gr.Tab("📁 Documents"):
            doc_list, delete_dropdown = library_tab()
            demo.load(fn=update_doc_list, outputs=[doc_list])
            demo.load(fn=get_doc_options, outputs=[delete_dropdown])
        with gr.Tab("📜 History"):
            history_display = history_tab()
            demo.load(fn=load_history, outputs=[history_display])
        with gr.Tab("ℹ️ Help"):
            help_tab()
    demo.launch()
