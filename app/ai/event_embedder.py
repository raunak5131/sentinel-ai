from openai import OpenAI
from app.config import settings


class EventEmbedder:
    """
    Converts SentinelAI events into vector embeddings.

    Embedding model:
    sentence-transformers/all-MiniLM-L6-v2

    Output dimension:
    384
    """

    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"

        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(self.model_name)

    def create_event_text(self, event):
        """
        Convert an EventRecord into natural language text.
        """

        text = (
            f"At {event.start_timestamp:.1f} seconds, "
            f"{event.object_class or 'unknown object'} "
            f"{event.event_type.replace('_', ' ')}."
        )

        if event.description:
            text += f" Description: {event.description}."

        if event.metadata_json:
            metadata = event.metadata_json

            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if value is not None:
                        text += f" {key}: {value}."

        return text

    def embed(self, text):
        """
        Generate a 384-dimensional embedding.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()