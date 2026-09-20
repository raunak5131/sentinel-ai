import json
from openai import OpenAI

from app.config import settings


class QueryUnderstanding:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = "openai/gpt-oss-20b"

    def understand(self, question, available_objects):
        objects_text = "\n".join(
            f"- {object_class}"
            for object_class in available_objects
        )

        prompt = f"""
You are the query understanding component of SentinelAI,
a video intelligence system.

The user asks a question about a video.

AVAILABLE OBJECT CLASSES IN THIS VIDEO:
{objects_text}

USER QUESTION:
{question}

Determine the user's intended query.

Possible intents:
- count
- list
- timeline
- semantic

Possible event types:
- entered
- exited
- stopped
- started_moving
- scene_context
- null

Rules:

1. Only select an object_class from the AVAILABLE OBJECT CLASSES.
2. If the user refers to an object using a plural or natural-language variation,
   map it to the matching available object class.
3. Do not invent an object class.
4. If no object class is relevant, use null.
5. Use event_type only when the question clearly refers to an event.
6. For "how many", use intent = "count".
7. Questions asking "which" or "who" about specific events usually use intent = "list".
8. Questions asking what happened during a time period use intent = "timeline".
9. General questions that cannot be represented by structured event filters use intent = "semantic".
10. Extract time ranges when explicitly mentioned.

Return ONLY valid JSON:

{{
    "intent": "count | list | timeline | semantic",
    "object_class": "string or null",
    "event_type": "entered | exited | stopped | started_moving | scene_context | null",
    "time_start": "number or null",
    "time_end": "number or null"
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a structured query parser. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()

        # Handle accidental markdown code fences
        if raw.startswith("```"):
            raw = raw.replace("```json", "")
            raw = raw.replace("```", "")
            raw = raw.strip()

        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "intent": "semantic",
                "object_class": None,
                "event_type": None,
                "time_start": None,
                "time_end": None,
            }

        return self.validate(result, available_objects)

    def validate(self, result, available_objects):
        intent = result.get("intent")

        if intent not in {
            "count",
            "list",
            "timeline",
            "semantic",
        }:
            intent = "semantic"

        object_class = result.get("object_class")

        # Critical safety check:
        # Never allow the LLM to invent an object class.
        if object_class not in available_objects:
            object_class = None

        event_type = result.get("event_type")

        allowed_event_types = {
            "entered",
            "exited",
            "stopped",
            "started_moving",
            "scene_context",
            None,
        }

        if event_type not in allowed_event_types:
            event_type = None

        return {
            "intent": intent,
            "object_class": object_class,
            "event_type": event_type,
            "time_start": result.get("time_start"),
            "time_end": result.get("time_end"),
        }