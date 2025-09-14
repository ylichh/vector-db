import os
from dotenv import load_dotenv
import uuid

from ..domain.repositories.vector_db.i_vector_db import IVectorDBManager
from ..domain.services.embedder.i_embedder import IEmbedder
from ..domain.services.document_processor.i_processor import (
    IDocumentProcessor,
)


class App:
    def __init__(
        self,
        vector_db_manager=IVectorDBManager,
        embedder=IEmbedder,
        document_processor=IDocumentProcessor,
    ):
        self.pinecone_manager = vector_db_manager
        self.embedder = embedder
        self.document_processor = document_processor

    def upload_vectors(self):
        try:
            self.pinecone_manager.create_if_not_exists_index()
            document_chunk_generator = (
                self.document_processor.document_chunk_generator()
            )
        except Exception as e:
            print(f"Error while tuning upload app: {e}")

        while True:
            try:
                chunk = next(document_chunk_generator)
                vector = self.embedder.generate_embedding(chunk.text)
                metadata = chunk.metadata.model_dump()

                id = str(uuid.uuid4())
                pinecone_document = {
                    "id": id,
                    "values": vector,
                    "metadata": metadata,
                }
                self.pinecone_manager.upload_vector(pinecone_document)
            except StopIteration:
                print("All document chunks have been processed.")
                break

    def search_vector_by_text(self, text, top_k=5):
        try:
            query_vector = self.embedder.generate_embedding(text)
            results = self.pinecone_manager.query(
                search_vector=query_vector, top_k_docs=top_k
            )
            return results
        except Exception as e:
            print(f"Error during search: {e}")
            return None

    def search_vector_by_vector(self, text: str, vector=None, top_k=5):
        try:
            if vector is None:
                vector = self.embedder.generate_embedding(text)
            results = self.pinecone_manager.query(
                search_vector=vector, top_k_docs=top_k
            )
            return results
        except Exception as e:
            print(f"Error during vector search: {e}")
            return None


if __name__ == "__main__":

    from src.infrastructure.external_services.openai_embedder import (
        OpenAIEmbedder,
        OpenAIConfiguration,
    )
    from src.infrastructure.adapters.markdown import MarkdownCommandProcessor
    from src.infrastructure.persistance.pinecone import (
        PineconeManager,
        IndexConfiguration,
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "./documents/markdown/commands.md")
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

    app.upload_vectors()
