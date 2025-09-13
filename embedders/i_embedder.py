from abc import ABC, abstractmethod


class IEmbedder(ABC):
    @abstractmethod
    def generate_embedding(self, text: str):
        """Genera el embedding para el texto dado."""
        pass
