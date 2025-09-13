from openai import OpenAI

from .i_embedder import IEmbedder


class OpenAIConfiguration:
    def __init__(self, model_name: str, api_key: str):
        if not model_name or not api_key:
            raise ValueError("model_name and api_key must be provided")
        self.model_name = model_name
        self.api_key = api_key


class OpenAIEmbedder(IEmbedder):
    def __init__(self, config: OpenAIConfiguration):
        self.model_name = config.model_name
        try:
            self.client = OpenAI(api_key=config.api_key)
        except Exception as e:
            raise ValueError(f"Error initializing OpenAI client: {e}")

    def generate_embedding(self, text: str):
        try:
            response = self.client.embeddings.create(
                input=text, model=self.model_name
            )
            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"Error generating embedding: {e}")


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()

    config = OpenAIConfiguration(
        model_name="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    embedder = OpenAIEmbedder(config)
    vector = embedder.generate_embedding("Hola, ¿cómo estás?")
    pass
