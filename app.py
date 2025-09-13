import os
from dotenv import load_dotenv

from pinecone_manager.pinecone_uploader import (
    PineconeManager,
    IndexConfiguration,
)
from embedders.openai import OpenAIEmbedder, OpenAIConfiguration
from document_processors.markdown import MarkdownCommandProcessor


class App:
    def __init__(self, pinecone_manager=PineconeManager):
        self.pinecone_manager = pinecone_manager

    def upload_vector(self):
        try:
            self.pinecone_manager.create_if_not_exists_index()
            self.pinecone_manager.upload_vectors()
        except Exception as e:
            print(f"Error while tunning upload app: {e}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "./documents/markdown/commands.md")
    load_dotenv()
    pinecone_manager = PineconeManager(
        index_configuration=IndexConfiguration(
            name=os.getenv("PINECONE_INDEX_NAME"),
            dimension=int(os.getenv("PINECONE_INDEX_DIMENSION")),
            api_key=os.getenv("PINECONE_API_KEY"),
        ),
        embedder=OpenAIEmbedder(
            config=OpenAIConfiguration(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name=os.getenv("OPENAI_EMBEDDER_MODEL"),
            )
        ),
        doc_processor=MarkdownCommandProcessor(document_path=file_path),
    )
    configurator = App(pinecone_manager=pinecone_manager)
    configurator.upload_vector()
