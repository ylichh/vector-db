from dotenv import load_dotenv
import os


from use_cases.app import App
from pinecone_manager.pinecone import (
    PineconeManager,
    IndexConfiguration,
)
from embedders.openai import OpenAIEmbedder, OpenAIConfiguration
from document_processors.markdown import MarkdownCommandProcessor


if __name__ == "__main__":
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "./documents/markdown/commands.md",
    )
    load_dotenv()

    pinecone_manager = PineconeManager(
        index_configuration=IndexConfiguration(
            name=os.getenv("PINECONE_INDEX_NAME"),
            dimension=int(os.getenv("PINECONE_INDEX_DIMENSION")),
            api_key=os.getenv("PINECONE_API_KEY"),
        )
    )

    app = App(
        pinecone_manager=pinecone_manager,
        embedder=OpenAIEmbedder(
            config=OpenAIConfiguration(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name=os.getenv("OPENAI_EMBEDDER_MODEL"),
            )
        ),
        document_processor=MarkdownCommandProcessor(document_path=file_path),
    )

    app.search_vector_by_text(
        "oye levantame el docker compose, solo la app de genai", top_k=3
    )
    app.search_vector_by_vector()
