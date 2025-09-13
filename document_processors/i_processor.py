from abc import ABC, abstractmethod
from typing import Generator
from .schemas import DocumentChunkData


DOCUMENT_TYPES = [
    "pdf",
    "docx",
    "txt",
]


class IDocumentProcessor(ABC):
    @abstractmethod
    def document_chunk_generator(
        self,
    ) -> Generator[DocumentChunkData, None, None]:
        """Procesa un documento y devuelve un generador
        de trozos procesados."""
        pass
