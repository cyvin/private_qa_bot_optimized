import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
from ui.layout import build_ui

if __name__ == "__main__":
    build_ui()
