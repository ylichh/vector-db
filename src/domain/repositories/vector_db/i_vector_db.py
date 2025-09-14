from abc import ABC, abstractmethod
from .schemas import VectorMatches


class IVectorDBManager(ABC):
    @abstractmethod
    def upload_vector(self, vector_data: dict):
        """Sube un vector al almacenamiento."""
        pass

    @abstractmethod
    def query(
        self, search_vector: list, top_k: int = 5
    ) -> VectorMatches | None:
        """Busca los vectores más similares."""
        pass
