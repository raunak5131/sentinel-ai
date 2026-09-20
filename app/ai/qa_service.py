from openai import OpenAI

from app.config import settings
from app.ai.event_search import EventSearch


class VideoQAService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = "openai/gpt-oss-20b"
        self.search = EventSearch()

    def answer(self, video_id, question, limit=8):

        # Retrieve relevant events
        events = self.search.search(
            video_id=video_id,
            query=question,
            limit=limit,
        )

        if not events:
            return {
                "answer": "I could not find relevant events in this video.",
                "sources": [],
            }

        # Convert retrieved events into context
        context_lines = []

        for event in events:

            context_lines.append(
                f"""
Timestamp: {event['timestamp']:.2f}s
Event: {event['event_type']}
Object: {event['object_class']}
Entity: {event['entity_id']}
Description: {event['description']}
Metadata: {event['metadata']}
""".strip()
            )

        context = "\n\n".join(context_lines)

        prompt = f"""
You are SentinelAI, a video intelligence assistant.

Answer the user's question using ONLY the event information
provided below.

Do not invent objects, actions, timestamps, or events.

If the available information is insufficient to answer the
question, clearly say that the available event data is
insufficient.

EVENT CONTEXT:

{context}

USER QUESTION:

{question}

Give a concise natural-language answer.

When mentioning an event, include its timestamp when useful.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a factual video analysis assistant. "
                        "You must ground every answer in the supplied "
                        "event context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
        )

        answer = response.choices[0].message.content.strip()

        return {
            "answer": answer,
            "sources": events,
        }