from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from .schemas import VectorMatches

load_dotenv()


class IndexConfiguration:
    name: str
    dimension: int
    api_key: str

    def __init__(self, name: str, dimension: int, api_key: str):
        self.name = name
        self.dimension = dimension
        self.api_key = api_key


class PineconeManager:
    def __init__(self, index_configuration: IndexConfiguration):

        self.index_name = index_configuration.name
        self.index_dimension = index_configuration.dimension
        self.api_key = index_configuration.api_key
        self.pc = Pinecone(api_key=self.api_key)

    def create_if_not_exists_index(self):
        try:
            if not self.pc.has_index(self.index_name):
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.index_dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1",
                    ),
                    deletion_protection="disabled",
                )
            else:
                print(f"El índice {self.index_name} ya existe.")
            self.index = self.pc.Index(self.index_name)
            print("Conectado al índice existente")
        except Exception as e:
            print(f"Error al crear o conectar con el índice: {e}")
            raise

    def upload_vectors(self, vector_data):
        """
        Sube una lista de vectores a Pinecone.
        Cada vector debe ser una tupla (id, vector, metadata).
        """
        pinecone_document = {
            "id": vector_data.get("id"),
            "values": vector_data.get("values"),
            "metadata": vector_data.get("metadata"),
        }
        try:
            self.pc.Index(self.index_name).upsert(vectors=[pinecone_document])
        except Exception as e:
            print(f"Error processing document chunk: {e}")
        else:
            print(
                f"Vector with ID {vector_data.get('id')} uploaded successfully."
            )

    def query(self, search_vector, top_k_docs=5):
        """
        Realiza una consulta de similitud en Pinecone.
        Devuelve los top_k vectores más similares.
        """
        try:
            nearest_vector = self.pc.Index(self.index_name).query(
                vector=search_vector, top_k=top_k_docs, include_metadata=True
            )
            return VectorMatches(**nearest_vector.to_dict())
        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            return None


if __name__ == "__main__":
    import os
    from document_processors.markdown import MarkdownCommandProcessor
    from embedders.openai import OpenAIEmbedder, OpenAIConfiguration

    load_dotenv()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../documents/markdown/commands.md")

    doc_processor = MarkdownCommandProcessor(document_path=file_path)
    embedder = OpenAIEmbedder(
        config=OpenAIConfiguration(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=os.getenv("OPENAI_EMBEDDER_MODEL"),
        )
    )
    pinecone_manager = PineconeManager(
        index_configuration=IndexConfiguration(
            name=os.getenv("PINECONE_INDEX_NAME"),
            dimension=os.getenv("PINECONE_INDEX_DIMENSION"),
            api_key=os.getenv("PINECONE_API_KEY"),
        ),
        embedder=embedder,
        doc_processor=doc_processor,
    )
    pinecone_manager.create_if_not_exists_index()
    pinecone_manager.upload_vectors()
