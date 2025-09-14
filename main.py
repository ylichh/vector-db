from dotenv import load_dotenv
import os


from src.application.app import App
from src.infrastructure.external_services.openai_embedder import (
    OpenAIEmbedder,
    OpenAIConfiguration,
)
from src.infrastructure.adapters.markdown import MarkdownCommandProcessor
from src.infrastructure.persistance.pinecone import (
    PineconeManager,
    IndexConfiguration,
)


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
        vector_db_manager=pinecone_manager,
        embedder=OpenAIEmbedder(
            config=OpenAIConfiguration(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name=os.getenv("OPENAI_EMBEDDER_MODEL"),
            )
        ),
        document_processor=MarkdownCommandProcessor(document_path=file_path),
    )
    # app.upload_vectors()
    result = app.search_vector_by_text(
        "oye levantame el docker compose, solo la app de genai", top_k=3
    )

    print(result)
