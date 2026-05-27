import gradio as gr

import config
from services import PlatformService


def create_gradio_ui():
    platform_service = PlatformService()

    def collection_choices():
        items = [item["name"] for item in platform_service.list_collections()]
        if config.DEFAULT_COLLECTION not in items:
            items.append(config.DEFAULT_COLLECTION)
        return sorted(set(items))

    def dropdown_update(selected: str | None = None):
        choices = collection_choices()
        value = config.normalize_collection_name(selected or config.DEFAULT_COLLECTION)
        return gr.update(choices=choices, value=value)

    def format_file_list(collection_name: str):
        files = platform_service.get_documents(collection_name)
        if not files:
            return "No documents available in the selected knowledge base."
        return "\n".join(files)

    def sync_collection_selection(selected):
        selected = config.normalize_collection_name(selected)
        return format_file_list(selected), dropdown_update(selected), dropdown_update(selected)

    def upload_handler(collection_name, files, progress=gr.Progress()):
        collection_name = config.normalize_collection_name(collection_name)
        if not files:
            return None, format_file_list(collection_name), dropdown_update(collection_name), dropdown_update(collection_name)

        result = platform_service.add_documents(
            collection_name,
            files,
            progress_callback=lambda p, desc: progress(p, desc=desc),
        )
        gr.Info(f"Added: {result['added']} | Skipped: {result['skipped']}")
        return None, format_file_list(collection_name), dropdown_update(collection_name), dropdown_update(collection_name)

    def refresh_handler(collection_name):
        return sync_collection_selection(collection_name)

    def clear_handler(collection_name):
        collection_name = config.normalize_collection_name(collection_name)
        result = platform_service.clear_collection(collection_name)
        gr.Info(f"Removed all documents from collection '{result['collection']}'")
        return format_file_list(collection_name), dropdown_update(collection_name), dropdown_update(collection_name)

    def chat_handler(message, history, collection_name):
        result = platform_service.chat(collection_name, message)
        return result["answer"]

    initial_choices = collection_choices()

    with gr.Blocks(title="Agentic RAG Platform") as demo:
        with gr.Tab("Documents", elem_id="doc-management-tab"):
            gr.Markdown("## Knowledge Base")
            gr.Markdown("Choose an existing collection or type a new one to isolate documents by project or customer.")

            document_collection = gr.Dropdown(
                label="Collection",
                choices=initial_choices,
                value=config.DEFAULT_COLLECTION,
                allow_custom_value=True,
            )

            files_input = gr.File(
                label="Drop PDF or Markdown files here",
                file_count="multiple",
                type="filepath",
                height=200,
                show_label=False,
            )

            add_btn = gr.Button("Add Documents", variant="primary", size="md")

            gr.Markdown("## Documents in Current Collection")
            file_list = gr.Textbox(
                value=format_file_list(config.DEFAULT_COLLECTION),
                interactive=False,
                lines=7,
                max_lines=10,
                elem_id="file-list-box",
                show_label=False,
            )

            with gr.Row():
                refresh_btn = gr.Button("Refresh", size="md")
                clear_btn = gr.Button("Clear All", variant="stop", size="md")

        with gr.Tab("Chat"):
            chat_collection = gr.Dropdown(
                label="Collection",
                choices=initial_choices,
                value=config.DEFAULT_COLLECTION,
                allow_custom_value=True,
            )

            chatbot = gr.Chatbot(
                height=600,
                placeholder="Ask a specific question about the documents in this collection.",
                show_label=False,
            )

            gr.ChatInterface(
                fn=chat_handler,
                chatbot=chatbot,
                additional_inputs=[chat_collection],
            )

        add_btn.click(
            upload_handler,
            [document_collection, files_input],
            [files_input, file_list, document_collection, chat_collection],
            show_progress="corner",
        )
        refresh_btn.click(
            refresh_handler,
            [document_collection],
            [file_list, document_collection, chat_collection],
        )
        clear_btn.click(
            clear_handler,
            [document_collection],
            [file_list, document_collection, chat_collection],
        )
        document_collection.change(
            sync_collection_selection,
            [document_collection],
            [file_list, document_collection, chat_collection],
        )

    return demo
