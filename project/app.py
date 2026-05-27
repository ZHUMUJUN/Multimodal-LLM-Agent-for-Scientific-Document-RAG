import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

import config
from core.logging_utils import configure_logging
from core.tracing import initialize_tracing
from ui.css import custom_css
from ui.gradio_app import create_gradio_ui

if __name__ == "__main__":
    configure_logging()
    initialize_tracing()
    print("\nCreating Agentic RAG Platform...")
    demo = create_gradio_ui()
    print("\nLaunching Gradio UI...")
    demo.launch(
        css=custom_css,
        server_name=config.GRADIO_HOST,
        server_port=config.GRADIO_PORT,
    )
